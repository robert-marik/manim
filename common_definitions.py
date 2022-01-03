from manim import *
import colorsys

def temperature_to_color(temp, min_temp=-1, max_temp=1):
    colors = [BLUE, TEAL, GREEN, YELLOW, "#ff0000"]

    alpha = inverse_interpolate(min_temp, max_temp, temp)
    index, sub_alpha = integer_interpolate(
        0, len(colors) - 1, alpha
    )

    return interpolate_color(
        colors[index], colors[index + 1], sub_alpha
    )


def rgb2hex(a):
    r,g,b = a 
    return "#{:02x}{:02x}{:02x}".format(int(255*r),int(255*g),int(255*b))

def value2hex(value):
    """
    The function converts value from the interval from 0 to 1 into a color.
    """
    temp = 0.99*(value)*0.8+0.2
    if temp<0:
        temp = 0
    if temp>0.99:
        temp = 0.99
    return rgb2hex(colorsys.hsv_to_rgb(temp, 0.99, 0.99))
