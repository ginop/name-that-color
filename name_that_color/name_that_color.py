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

from name_that_color import SHADES, NAMES


class ntc:

  def __init__(self):
    self.names = NAMES.copy()
    for i, name in enumerate(self.names):
      color = "#" + self.names[i][0]
      rgb = self.rgb(color)
      hsl = self.hsl(color)
      self.names[i].extend([rgb[0], rgb[1], rgb[2], hsl[0], hsl[1], hsl[2]])

  def name(self, color: str):

    color = color.upper()
    if len(color) < 3 or len(color) > 7:
      return ["#000000", "Invalid Color: " + color, "#000000", "", False]
    elif len(color) % 3 == 0:
      color = "#" + color
    elif len(color) == 4:
      color = "#" + color[1] + color[1] + color[2] + color[2] + color[3] + color[3]

    rgb = self.rgb(color)
    r, g, b = rgb
    hsl = self.hsl(color)
    h, s, l = hsl
    ndf1 = ndf2 = ndf = 0
    cl = df = -1

    for i, name in enumerate(self.names):
      if color == "#" + name[0]:
        return ["#" + name[0], name[1], self.shadergb(name[2]), name[2], True]

      ndf1 = (r - name[3]) ** 2 + (g - name[4]) ** 2 + (b - name[5]) ** 2
      ndf2 = abs((h - name[6]) ** 2) + (s - name[7]) ** 2 + abs((l - name[8]) ** 2)
      ndf = ndf1 + ndf2 * 2
      if df < 0 or df > ndf:
        df = ndf
        cl = i

    return ["#000000", "Invalid Color: " + color, "#000000", "", False] if cl < 0 else \
      ["#" + self.names[cl][0], self.names[cl][1], self.shadergb(self.names[cl][2]), self.names[cl][2], False]

  # // adopted from: Farbtastic 1.2
  # // http://acko.net/dev/farbtastic
  def hsl(self, color):

    rgb = [int('0x' + color[1:3], 0) / 255, int('0x' + color[3:5], 0) / 255, int('0x' + color[5:7], 0) / 255]
    r, g, b = rgb

    min_color = min(r, min(g, b))
    max_color = max(r, max(g, b))
    delta = max_color - min_color
    l = (min_color + max_color) / 2

    s = 0
    if 0 < l < 1:
      s = delta / ((2 * l) if l < 0.5 else (2 - 2 * l))

    h = 0
    if delta > 0:
      if max_color == r and max_color != g:
        h += (g - b) / delta
      if max_color == g and max_color != b:
        h += (2 + (b - r) / delta)
      if max_color == b and max_color != r:
        h += (4 + (r - g) / delta)
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
