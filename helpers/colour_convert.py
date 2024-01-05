from colormath.color_objects import sRGBColor, LabColor, CMYKColor
from colormath.color_conversions import convert_color
import colorsys


class ColorConverter:
    def __init__(self, hex_string):
        self.hex_string = hex_string
        self.color_info = self.convert_formats()

    @staticmethod
    def is_valid_hex(s):
        return isinstance(s, str) and len(s) == 6 and all(c in "0123456789abcdefABCDEF" for c in s)

    def hex_to_rgb(self):
        return tuple(int(self.hex_string[i:i + 2], 16) for i in (0, 2, 4))

    @staticmethod
    def rgb_to_hsl(rgb):
        return colorsys.rgb_to_hls(rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0)

    @staticmethod
    def rgb_to_lab(rgb):
        rgb_color = sRGBColor(rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0)
        lab_color = convert_color(rgb_color, LabColor)
        return lab_color.lab_l, lab_color.lab_a, lab_color.lab_b

    @staticmethod
    def rgb_to_xyz(rgb):
        rgb_color = sRGBColor(rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0)
        xyz_color = convert_color(rgb_color, sRGBColor)
        return xyz_color.rgb_r, xyz_color.rgb_g, xyz_color.rgb_b

    @staticmethod
    def rgb_to_cmyk(rgb):
        rgb_color = sRGBColor(rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0)
        cmyk_color = convert_color(rgb_color, CMYKColor)
        return cmyk_color.cmyk_c, cmyk_color.cmyk_m, cmyk_color.cmyk_y, cmyk_color.cmyk_k

    @staticmethod
    def rgb_to_hsv(rgb):
        hsv_color = colorsys.rgb_to_hsv(rgb[0] / 255.0, rgb[1] / 255.0, rgb[2] / 255.0)
        return hsv_color[0], hsv_color[1], hsv_color[2]

    def convert_formats(self):
        rgb = self.hex_to_rgb()
        hsl = self.rgb_to_hsl(rgb)
        lab = self.rgb_to_lab(rgb)
        xyz = self.rgb_to_xyz(rgb)
        cmyk = self.rgb_to_cmyk(rgb)
        hsv = self.rgb_to_hsv(rgb)

        return {
            "RGB": rgb,
            "HSL": hsl,
            "LAB": lab,
            "XYZ": xyz,
            "CMYK": cmyk,
            "HSV": hsv
        }
