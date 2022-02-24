from curses.ascii import CR
from manim import *

from manim_editor import PresentationSectionType
config.max_files_cached = 400


class Model(ZoomedScene):

    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor=0.3,
            zoomed_display_height=7.5,
            zoomed_display_width=5,
            image_frame_stroke_width=20,
            zoomed_camera_config={
                "default_frame_stroke_width": 3,
                },
            **kwargs
        )

    def construct(self):
        
        tmax = 12.5
        r = 0.57
        K = ValueTracker(6)

        axes = Axes(
            x_range=[0,tmax,1e6], 
            y_range=[0,1.75,1e6],
            tips = False)

        t = np.linspace(0,12.5,500)
        predatori = t**2/(1+t**2)
        c_predatori = axes.plot_line_graph(x_values=t,y_values=predatori, add_vertex_dots=False, line_color=RED)

        def kresli_parabolu():
            t_pos = np.linspace(0,K.get_value(),500) 
            logisticky_rust = r*t_pos*(1-t_pos/K.get_value()) 
            return axes.plot_line_graph(x_values=t_pos,y_values=logisticky_rust, add_vertex_dots=False, line_color=BLUE)
        c_logisticky_rust =  always_redraw(lambda : kresli_parabolu())

        self.play(Create(axes))
        self.play(Create(c_logisticky_rust))
        self.play(Create(c_predatori))

        zoomed_camera = self.zoomed_camera
        zoomed_display = self.zoomed_display
        frame = zoomed_camera.frame
        zoomed_display_frame = zoomed_display.display_frame
        frame.move_to(axes.c2p(0,0,0)).shift(1.2*RIGHT+1.75*UP)
        zoomed_display.to_corner(UR)

        self.play(Create(frame))
        zd_rect = BackgroundRectangle(zoomed_display, fill_opacity=0, buff=MED_SMALL_BUFF)        

        self.activate_zooming()        

        unfold_camera = UpdateFromFunc(zd_rect, lambda rect: rect.replace(zoomed_display))
        self.play(self.get_zoomed_display_pop_out_animation(), unfold_camera)        

        self.play(K.animate.set_value(7.5))
        self.wait()
        self.play(K.animate.set_value(9))
        self.wait()
        self.play(K.animate.set_value(13))

        self.wait()
        self.play(FadeOut(frame), FadeOut(zoomed_display), FadeOut(zoomed_display_frame))



        self.wait()

 
class Example(ZoomedScene):  
    def __init__(self, **kwargs):   #HEREFROM
        ZoomedScene.__init__( 
            self, 
            zoom_factor=0.1, 
            zoomed_display_height=6, 
            zoomed_display_width=3,  
            image_frame_stroke_width=20,  
            zoomed_camera_config={  
                'default_frame_stroke_width': 3,  
            },  
            **kwargs  
        )      
      
    def construct(self):  
        self.activate_zooming(animate=False)  
      
        ax = Axes(  
            x_range=[0, 10, 2],  
            y_range=[0,10, 2],  
            x_length=2,  
            y_length=2,  
            x_axis_config={'color': ORANGE},  
            y_axis_config={'color': ORANGE},  
        )  
        ax.shift(DL)  
        x_vals = [0, 1, 2, 3,4,5]  
        y_vals = [2, -1, 4, 2, 4, 1]  
        graph = ax.plot_line_graph(x_values=x_vals, y_values=y_vals)  
        self.zoomed_camera.frame.move_to(graph.get_top()+0.1*DL)  
        self.zoomed_display.shift(3*LEFT+0.4*UP)  
        self.camera.frame.scale(1/2)  
        self.camera.frame.shift(UR*1)  
        self.add(ax, graph)  #HERETO
