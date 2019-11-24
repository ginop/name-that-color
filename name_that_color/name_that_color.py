# (Translated to Python by Gino Perrotta)
# /*
#
# +-----------------------------------------------------------------+
# |   Created by Chirag Mehta - http://chir.ag/tech/download/ntc    |
# |-----------------------------------------------------------------|
# |               ntc js (Name that Color JavaScript)               |
# +-----------------------------------------------------------------+
#
# All the functions, code, lists etc. have been written specifically
# for the Name that Color JavaScript by Chirag Mehta unless otherwise
# specified.
#
# This script is released under the: Creative Commons License:
# Attribution 2.5 http://creativecommons.org/licenses/by/2.5/
#
# Sample Usage:
#
#   <script type="text/javascript" src="ntc.js"></script>
#
#   <script type="text/javascript">
#
#     var n_match  = ntc.name("#6195ED");
#     n_rgb = n_match[0]; // This is the RGB value of the closest matching color
#     n_name = n_match[1]; // This is the text string for the name of the match
#     n_shade_rgb = n_match[2]; // This is the RGB value for the name of colors shade
#     n_shade_name = n_match[3]; // This is the text string for the name of colors shade
#     n_exactmatch = n_match[4]; // True if exact color match, False if close-match
#
#     alert(n_match);
#
#   </script>
#
# */

import math
from name_that_color import SHADES, NAMES


class ntc:

    def __init__(self):
        self.names = NAMES.copy()
        for i, name in enumerate(self.names):
            color = "#" + self.names[i][0]
            rgb = self.rgb(color)
            hsl = self.hsl(color)
            self.names[i].extend([rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]])

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
        print(h, s, l, hue_deg, hsl_x, hsl_y)

        closest_index = closest_dist = -1

        for i, name in enumerate(self.names):
            if color == "#" + name[0]:
                return ["#" + name[0], name[1], self.shadergb(name[2]), name[2], True]

            color_r, color_g, color_b = name[3:6]
            rgb_dist = (r - color_r) ** 2 + (g - color_g) ** 2 + (b - color_b) ** 2

            color_h, color_s, color_l = name[6:9]
            color_hue_deg = color_h / 255 * 360
            color_hue_rad = math.radians(color_hue_deg)
            color_hsl_x = math.cos(color_hue_rad) * color_s * (max(color_r, color_g, color_b) - min(color_r, color_g, color_b)) / 255
            color_hsl_y = math.sin(color_hue_rad) * color_s * (max(color_r, color_g, color_b) - min(color_r, color_g, color_b)) / 255
            hsl_dist = (hsl_x - color_hsl_x) ** 2 + (hsl_y - color_hsl_y) ** 2 + (l - color_l) ** 2

            combined_dist = rgb_dist + hsl_dist * 2  # why is hsl distance doubled?
            print(rgb_dist, hsl_dist, combined_dist, name)
            if closest_dist < 0 or closest_dist > combined_dist:
                closest_dist = combined_dist
                closest_index = i

        return ["#000000", "Invalid Color: " + color, "#000000", "", False] if closest_index < 0 else \
            ["#" + self.names[closest_index][0], self.names[closest_index][1], self.shadergb(self.names[closest_index][2]), self.names[closest_index][2], False]

    # // adopted from: Farbtastic 1.2
    # // http://acko.net/dev/farbtastic
    def hsl(self, color):

        r, g, b = [n / 255 for n in self.rgb(color)]

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
    def rgb(self, color):
        return [int('0x' + color[1:3], 0), int('0x' + color[3:5], 0),  int('0x' + color[5:7], 0)]

    def shadergb(self, shadename):
        for i, shade in enumerate(SHADES):
            if shadename == shade[1]:
                return "#" + shade[0]
        return "#000000"
