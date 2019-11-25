# This module was translated to Python and updated by Gino Perrotta - https://github.com/ginop/name-that-color

# based on the JavaScript "Name that Color" by Chirag Mehta - http://chir.ag/tech/download/ntc
# which was released under the Creative Commons License Attribution 2.5 http://creativecommons.org/licenses/by/2.5/

# "Name that Color" was partially based on Farbtastic 1.2 - http://acko.net/dev/farbtastic

#     var n_match  = ntc.name("#6195ED");
#     n_rgb = n_match[0]; // This is the RGB value of the closest matching color
#     n_name = n_match[1]; // This is the text string for the name of the match
#     n_shade_rgb = n_match[2]; // This is the RGB value for the name of colors shade
#     n_shade_name = n_match[3]; // This is the text string for the name of colors shade
#     n_exactmatch = n_match[4]; // True if exact color match, False if close-match

import math
import pandas as pd
from name_that_color import SHADES, NAMES


class ntc:

    def __init__(self):
        colors = pd.DataFrame(NAMES)
        colors.columns = ['hex_code', 'shade_name', 'basic_name']
        colors['hex_code'] = colors['hex_code'].apply(lambda code: '#' + code)

        colors[['r', 'g', 'b']] = pd.DataFrame(colors['hex_code'].apply(self.rgb).to_list())
        colors[['h', 's', 'l']] = pd.DataFrame(colors['hex_code'].apply(self.hsl).to_list())
        colors['max_color'] = colors[['r', 'g', 'b']].apply(max, axis=1)
        colors['min_color'] = colors[['r', 'g', 'b']].apply(min, axis=1)
        colors['chroma'] = colors['max_color'] - colors['min_color']
        colors['hsl_x'] = (colors['h'] * 360 / 255).apply(math.radians).apply(math.cos) * colors['s'] * colors['chroma'] / 255
        colors['hsl_y'] = (colors['h'] * 360 / 255).apply(math.radians).apply(math.sin) * colors['s'] * colors['chroma'] / 255

        colors.set_index(colors['hex_code'], inplace=True)

        self.names = colors

    # This has become functionally different from source, "Name that Color" by Chirag Mehta
    # Distance in HSL space was treated as Cartesian, but has now been updated to "bi-hexcone" model
    def name(self, color: str):

        if len(color) < 3 or len(color) > 7:
            return ["#000000", "Invalid Color: " + color, "#000000", "", False]
        elif len(color) % 3 == 0:
            color = "#" + color
        elif len(color) == 4:
            color = "#" + color[1] + color[1] + color[2] + color[2] + color[3] + color[3]

        r, g, b = self.rgb(color)

        h, s, l = self.hsl(color)
        hue_deg = h / 255 * 360
        hue_rad = math.radians(hue_deg)
        hsl_x = math.cos(hue_rad) * s * (max(r, g, b) - min(r, g, b)) / 255
        hsl_y = math.sin(hue_rad) * s * (max(r, g, b) - min(r, g, b)) / 255

        rgb_dist = (r - self.names['r']) ** 2 + (g - self.names['g']) ** 2 + (b - self.names['b']) ** 2
        hsl_dist = (hsl_x - self.names['hsl_x']) ** 2 + (hsl_y - self.names['hsl_y']) ** 2 + (l - self.names['l']) ** 2
        combined_dist = rgb_dist + hsl_dist * 2  # why is hsl distance doubled?

        closest_index = combined_dist.idxmin()

        return [
            "#" + closest_index,
            self.names['shade_name'][closest_index],
            self.shadergb(self.names['basic_name'][closest_index]),
            self.names['basic_name'][closest_index],
            closest_index == color
        ]

    # // adopted from: Farbtastic 1.2
    # // http://acko.net/dev/farbtastic
    @staticmethod
    def hsl(color):

        r, g, b = [n / 255 for n in ntc.rgb(color)]

        min_color = min(r, g, b)
        max_color = max(r, g, b)
        delta = max_color - min_color
        l = (min_color + max_color) / 2

        s = 0
        if 0 < l < 1:
            s = delta / ((2 * l) if l < 0.5 else (2 - 2 * l))

        h = 0
        if delta > 0:
            if max_color == r:
                h += (g - b) / delta
            elif max_color == g:
                h += 2 + (b - r) / delta
            elif max_color == b:
                h += 4 + (r - g) / delta
            h /= 6
        return [int(h * 255), int(s * 255), int(l * 255)]

    # // adopted from: Farbtastic 1.2
    # // http://acko.net/dev/farbtastic
    @staticmethod
    def rgb(color):
        return [int('0x' + color[1:3], 0), int('0x' + color[3:5], 0),  int('0x' + color[5:7], 0)]

    def shadergb(self, shadename):
        return "#" + self.names.loc[self.names['shade_name'] == shadename]['hex_code'][0]
