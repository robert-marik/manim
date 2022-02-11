from asyncio import proactor_events
from manim import *
import numpy as np
import common_definitions
import random
random.seed(10)
np.random.seed(10)

wait_time = 2
a = 3
b = 3
alpha = 0.7
beta = 0.5
gamma = 0.4
delta = 0.8
def F(X):
    x = X[0]
    y = X[1]
    """ Return the vector field. """    
    result = np.sin(x) * RIGHT 
    return result

def F(X):
    x = X[0]
    y = X[1]
    """ Return the vector field. """    
    #return np.array([x*y-1/3*x**3,-x])
    #return np.array([x*(y+4)-6*np.sin(x),(x+7)/7])
    # x = x +7
    # y = y + 3.5
    # x = x/14
    # y = y/7
    #return np.array([a*x*(1-alpha*x-beta*y),b*y*(1-gamma*x-delta*y),0])
    result = np.sin(x + y) * RIGHT + np.sin(x*y / 3) * UP
    return result

# from https://github.com/3b1b/videos/blob/4716f5b75911af25c4ec24ad3e0d3dd83e28fabf/_2018/div_curl.py#L55
def divergence(vector_func, point, dt=1e-7):
    value = vector_func(point)
    point2 = np.array([point[0],point[1],0])
    return sum([
            (vector_func(point2 + dt * vect) - value)[i] / dt
            for i, vect in enumerate([RIGHT, UP, OUT])
        ])

class VektorovePole(MovingCameraScene):
    
    def construct(self):
        vectors = ArrowVectorField(lambda p:F(p)[0]*RIGHT+F(p)[1]*UP,
            x_range=[-7,7,0.35],
            y_range=[-4,4,0.35],
            colors = [RED, YELLOW, BLUE, DARK_GRAY],
            #min_color_scheme_value=gradient_min, 
            #max_color_scheme_value=gradient_max, 
            length_func = lambda norm: min(norm, 0.4*sigmoid(norm)),
            stroke_width = 10,
        vector_config={"max_stroke_width_to_length_ratio":10, "max_tip_length_to_length_ratio":0.3}
        )

        self.add(vectors)
        self.wait()

        draw_streamlines = False
        draw_streamlines = True
        if draw_streamlines:
            stream_lines = StreamLines(F, stroke_width=3, max_anchors_per_line=30)
            self.add(stream_lines)        
            stream_lines.start_animation(warm_up=False, flow_speed=1.5)
            self.wait(stream_lines.virtual_time / stream_lines.flow_speed)        
            self.play(stream_lines.end_animation())        
            self.wait()
            self.remove(stream_lines)
        else:
            stream_lines = VGroup()

        self.remove(*[i for i in self.mobjects])            
        self.add(vectors)

        self.play(FadeToColor(vectors, GRAY), FadeToColor(stream_lines, GRAY))

        self.add(NumberPlane())
        circles = {}
        streams = {}
        texts = {}
        arrows_all = {}
        for i,point in enumerate([[2,-1.5,0],[-4.8,-2,0],[-1,1,0],[0.5,3,0],[-2.6,-0.3,0]]):
            circle = Circle(color=WHITE, radius=0.2)
            circle.add(Dot(circle.get_center(), radius=0.02))
            circle.move_to(point)
            self.add(circle)
            Delta = 0.3
            if draw_streamlines:
                stream_lines = StreamLines(F, stroke_width=2, max_anchors_per_line=10, 
                    x_range=[point[0]-Delta, point[0]+Delta, 0.2], 
                    y_range=[point[1]-Delta, point[1]+Delta, 0.2], 
                    padding=0.2, 
                    dt = 0.01,
                    ).set_z_index(-2)
                self.add(stream_lines)
            else:
                stream_lines = VGroup()
            hodnota = MathTex(r"\nabla \cdot \vec{F} = "+str(round(divergence(F,point),2))).next_to(circle)
            hodnota.add_background_rectangle()
            self.play(FadeIn(hodnota))
            arrows = VGroup()
            for i in range(12):
                uhel = i*2*PI/12
                bod = np.array(point)+np.array([np.cos(uhel),np.sin(uhel),0])*0.2
                arrows.add(Arrow(start=bod, end=bod+F(bod)*0.2, # /np.linalg.norm(F(bod))
                buff=0, 
                max_stroke_width_to_length_ratio=15, 
                max_tip_length_to_length_ratio = 0.3
                ).set_color(YELLOW))
            self.add(arrows)    
            self.wait()

            self.camera.frame.save_state()
            detail_frame = SurroundingRectangle(circle, color=BLUE, buff=.3)
            detail_frame.set_stroke(width=1, opacity=0.5)
            self.play(Create(detail_frame))
            self.wait(wait_time)
            self.play(self.camera.frame.animate.set(width=detail_frame.width*2).move_to(circle), running_time = 2)
            self.wait(2*wait_time)
            self.play(Restore(self.camera.frame),FadeOut(detail_frame), running_time = 2)   

            circles[i] = circle
            streams[i] = stream_lines
            texts[i] = hodnota
            arrows_all[i] = arrows



        self.wait()            

