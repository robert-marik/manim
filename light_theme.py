# Put this file in the same folder than your manim script
# and start your script with:
#
# import light_theme

from manim import *

config.background_color = WHITE

# Those are objects which are WHITE by default
# Define the wanted color for each one
white_objects ={
    Angle: ('dot_color', BLACK),
    AnnotationDot: ('stroke_color', BLACK),
    AnnularSector: ('color', BLACK),
    Annulus: ('color', BLACK),
    Arrow: ('color', BLACK),
    Arrow3D: ('color', BLACK),
    ArrowVectorField: ('color', BLACK),
    Code: ('background_stroke_color', BLACK),
    CubicBezier: ('color', BLACK),
    DashedVMobject: ('color', BLACK),
    Dot: ('color', BLACK),
    Dot3D: ('color', BLACK),
    Line: ('color', BLACK),
    Line3D: ('color', BLACK),
    MarkupText: ('color', BLACK),
    Polygon: ('color', BLACK),
    Rectangle: ('color', BLACK),
    SingleStringMathTex: ('color', BLACK),
    StreamLines: ('color', BLACK),
    Text: ('color', BLACK),
    TracedPath: ('stroke_color', BLACK),
    VectorField: ('color', BLACK),
}

for obj, (attr, color) in white_objects.items():
    obj.set_default(**{attr: color})

# Other configurations
Table.set_default(line_config=
    {"stroke_width": 1, "stroke_opacity": 0.5, "color": BLACK})

Code.set_default(style="pastie")
YELLOW="#ebe534"

