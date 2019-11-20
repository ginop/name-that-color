import pandas as pd

from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Dropout

from name_that_color.name_that_color import ntc

colors = pd.DataFrame(ntc().names)
colors.columns = ['hex_code', 'shade_name', 'basic_name', 'r', 'g', 'b', 'h', 's', 'l']
print(colors.head())

X = colors[['r', 'g', 'b']]
y = colors['basic_name']

num_classes = y.nunique()
y = pd.get_dummies(y)

network = Sequential()
network.add(Dense(64, input_shape=(3, )))
network.add(Dropout(0.3))
network.add(Dense(64))
network.add(Dropout(0.3))
network.add(Dense(num_classes, activation='softmax'))

network.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

network.fit(X, y, epochs=5, validation_split=0.2)
