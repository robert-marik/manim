from manim import *
import colorsys

def temperature_to_color(
    temp, 
    min_temp=-1, 
    max_temp=1,
    colors = [BLUE, TEAL, GREEN, YELLOW, "#ff0000"]
    ):

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


def analog_indicator(value, **kwargs):
    """
    Draws analog indicator to the screen. 

    class CircleToSquare(Scene):
        def construct(self):
            moje = analog_indicator(1)
            moje.marks.set_color(BLUE)
            self.add(moje)
            self.wait()    

    """

    options = {
            'value_min' : 0,
            'value_max' : 1,
            'values' : [0,0.2,0.4,0.6,0.8,1],
            'radius' : 1,
            'color_pointer_func' : lambda x:WHITE,
            'stretch' : 0.75,
            'title' : None, 
            'title_scale' : 0.7,
            'label_min' : None,
            'label_max' : None,
            'label_scale' : 0.7
    }
    options.update(kwargs)
    
    output = VGroup()
    output.add(Arc(radius=options['radius'], start_angle=20*DEGREES, angle=140*DEGREES, fill_color=BLACK))
    output.marks = VGroup()
    interval = options['value_max'] - options['value_min']
    for i in options['values']:
        output.marks.add(Line(start = [0.9,0,0], end=[1,0,0]).rotate(160*DEGREES - i / interval * 140 * DEGREES, about_point = ORIGIN))
    output.labels = VGroup()
    if options['label_min'] is not None:
        output.labels.add(Tex(options['label_min']).scale(options['label_scale']).next_to(output.marks[0],DOWN,buff=0.3))
    if options['label_max'] is not None:
        output.labels.add(Tex(options['label_max']).scale(options['label_scale']).next_to(output.marks[-1],DOWN,buff=0.3))    
    output.add(output.marks,output.labels)   
    output.pointer = Line(start = [0,0,0], end=[0.8,0,0])
    output.pointer.rotate(160*DEGREES - value / interval * 140 * DEGREES, about_point = ORIGIN)
    output.pointer.set_color(options['color_pointer_func'](value))
    output.add(output.pointer)
    output.stretch(options['stretch'],1,about_point=ORIGIN)
    output.dot = Dot()
    output.add(output.dot)
    if options['title'] is not None:
        output.title = Tex(options['title']).scale(options['title_scale']).next_to(output,UP)
        output.add(output.title)
    return output


