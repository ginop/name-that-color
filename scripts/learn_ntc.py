import math
import pandas as pd
from tqdm import trange
import os

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

from name_that_color.name_that_color import ntc


def get_colors(force_reprocess: bool = False):
    ntc_object = ntc()
    df_filepath = '../colors_categorized.pkl'
    if force_reprocess or not os.path.exists(df_filepath):
        colors = []
        for r in trange(0, 256, 2):
            for g in range(0, 256, 2):
                for b in range(0, 256, 2):
                    hex_code = f'#{r:02x}{g:02x}{b:02x}'
                    color_info = ntc_object.name_by_hsl(hex_code)
                    h, s, l = ntc_object.hsl(hex_code)
                    new_entry = {
                        'r': r,
                        'g': g,
                        'b': b,
                        'h': h,
                        's': s,
                        'l': l,
                        'shade_name': color_info[1],
                        'basic_name': color_info[3],
                        'hex_code': hex_code,
                    }
                    # print(new_entry)
                    colors.append(new_entry)

        colors = pd.DataFrame(colors)
        colors['max_color'] = colors[['r', 'g', 'b']].apply(max, axis=1)
        colors['min_color'] = colors[['r', 'g', 'b']].apply(min, axis=1)
        colors['chroma'] = colors['max_color'] - colors['min_color']
        colors['hsl_x'] = (colors['h'] * 360 / 255).apply(math.radians).apply(math.cos) * colors['s'] * colors['chroma'] / 255
        colors['hsl_y'] = (colors['h'] * 360 / 255).apply(math.radians).apply(math.sin) * colors['s'] * colors['chroma'] / 255

        colors.to_pickle(df_filepath)
    else:
        colors = pd.read_pickle(df_filepath)
    return colors


def learn_colors(colors: pd.DataFrame):
    colors = colors.sample(frac=1)  # shuffle row order so that validation_split takes random entries
    print(colors.head())

    X = colors[['r', 'g', 'b']] / 255 * 2 - 1
    y = colors['basic_name']

    num_classes = y.nunique()
    y = pd.get_dummies(y)

    network = Sequential()
    network.add(Dense(64, input_shape=(3, )))
    network.add(Dropout(0.3))
    for _ in range(10):
        network.add(Dense(64, activation='relu'))
        network.add(Dropout(0.3))
    network.add(Dense(num_classes, activation='softmax'))

    network.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

    network.fit(X, y, epochs=50, validation_split=0.2)


if __name__ == '__main__':
    learn_colors(get_colors(force_reprocess=False))
