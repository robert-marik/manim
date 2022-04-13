import numpy as np
from manim import *
from manim_editor import PresentationSectionType


class Derivace(ZoomedScene):
    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor=0.5,
            zoomed_display_height=3,
            zoomed_display_width=5,
            image_frame_stroke_width=2,
            zoomed_display_corner=DOWN,            
            zoomed_camera_config={
                "default_frame_stroke_width": 1,
            },
            **kwargs
        )

    def construct(self):

        self.next_section("")        
        ax1 = Axes(
            x_range=(-0.1,1,10),
            y_range=(-0.1,1,10),
            x_length=6,
            y_length=4,
            tips=False
            )
        ax1.to_corner((UL))
        ax2=ax1.copy().to_corner(UR)
        ax1.add(Tex(r"Lineární růst").move_to(ax1,aligned_edge=UP))
        ax2.add(Tex(r"Nelineární růst").move_to(ax2,aligned_edge=UP))
        self.add(ax1,ax2)
        g1 = ax1.plot(lambda x:0.2+0.5*x)
        g1.set_color(GREEN)

        x_values = np.linspace(-0.05, 1, 1000)
        y_values = 0.9-0.8*np.exp(-4*x_values)
        dy = np.gradient(y_values,x_values)
        g2 = ax2.plot_line_graph(x_values, y_values, add_vertex_dots=False)
        g2.set_color(BLUE)

        self.play(Create(g1))
        self.play(Create(g2))
        self.wait()


        self.next_section("")        
        zoomed_camera = self.zoomed_camera
        zoomed_display = self.zoomed_display
        frame = zoomed_camera.frame
        zoomed_display_frame = zoomed_display.display_frame

        for n,color,posun in zip([200,500],[YELLOW,ORANGE],[100,200]):

            frame.move_to(ax2.c2p(x_values[n],y_values[n],0))
            self.activate_zooming(animate=False)
            self.wait()

            self.play(self.zoomed_camera.frame.animate.scale(0.1))
            self.wait()

            self.next_section("")        
            def_t = x_values[n-posun:n+posun]
            x0 = x_values[n]
            y0 = y_values[n]
            dydx = dy[n]
            t = (def_t-x0)*dydx + y0
            g3 = ax2.plot_line_graph(def_t, t, add_vertex_dots=False)
            g3.set_color(color)
            self.add(g3)
            self.wait()
            self.next_section("")        

            self.play(self.zoomed_camera.frame.animate.scale(10))
            self.wait()

            self.next_section("")        
            self.remove(frame,zoomed_display)

        self.wait() 