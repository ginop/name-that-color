import pandas as pd
from tqdm import trange

from name_that_color.name_that_color import ntc


def main():
    ntc_object = ntc()
    colors = []
    for r in trange(0, 256, 16):
        for g in range(0, 256, 16):
            for b in range(0, 256, 16):
                hex_code = f'#{r:02x}{g:02x}{b:02x}'
                new_entry = {
                    'r': r,
                    'g': g,
                    'b': b,
                    'hex_code': hex_code,
                }

                color_info = ntc_object.name(hex_code)
                new_entry.update({
                    'closest_color_ntc': color_info[1],
                    'category_ntc': color_info[3],
                })

                color_info = ntc_object.name_by_rgb(hex_code)
                new_entry.update({
                    'closest_color_rgb': color_info[1],
                    'category_rgb': color_info[3],
                })

                color_info = ntc_object.name_by_hsl(hex_code)
                new_entry.update({
                    'closest_color_hsl': color_info[1],
                    'category_hsl': color_info[3],
                })

                colors.append(new_entry)

    colors = pd.DataFrame(colors)

    print(
        colors.loc[colors['category_ntc'] != colors['category_hsl']][['closest_color_ntc', 'closest_color_hsl', 'category_ntc', 'category_hsl']],
        colors.loc[colors['category_rgb'] != colors['category_hsl']][['closest_color_rgb', 'closest_color_hsl', 'category_rgb', 'category_hsl']]
    )


if __name__ == '__main__':
    main()
