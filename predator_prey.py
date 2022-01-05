from typing_extensions import runtime
from manim import *
from scipy.integrate import solve_ivp  # řešení diferenciálních rovnic
import colorsys
import random
from common_definitions import *

# https://scipy-cookbook.readthedocs.io/items/LoktaVolterraTutorial.html
# Definition of parameters
a = 1.
b = 0.1
c = 1.5
d = 0.75
def dX_dt(X, t=0):
    """ Return the growth rate of fox and rabbit populations. """
    return np.array([ a*X[0] -   b*X[0]*X[1] ,
                  -c*X[1] + d*b*X[0]*X[1] ])

X_f0 = np.array([     0. ,  0.])
X_f1 = np.array([ c/(d*b), a/b])

print(X_f1)

from scipy import integrate
tmax = 16.6 # maximum for time on graph
ymax = 60 # maximum on y axis´for graphs in time
tnumber = 1000
t = np.linspace(0, tmax,  tnumber)              # time
# X0 = np.array([10, 5])                     # initials conditions: 10 rabbits and 5 foxes
# X, infodict = integrate.odeint(dX_dt, X0, t, full_output=True)

curves = {}
number_of_curves = 9
for i in range(1,number_of_curves):
    X0 = np.array([60+i/number_of_curves*(-60+c/(d*b)), a/b]) 
    curves[i],infodict = integrate.odeint(dX_dt, X0, t, full_output=True)

X = curves.pop(4)
# c:\Users\marik\Documents\GitHub\manim
bunny = r"icons\rabbit-shape"
fox = r"icons\fox-sitting"

myaxis_config={'tips':False}

class Phase_portarit(Scene):
    def construct(self):

        equations = VGroup(
            Tex(r"$\displaystyle\frac{\mathrm dx}{\mathrm dt}=ax-bxy$"),
            Tex(r"$\displaystyle\frac{\mathrm dy}{\mathrm dt}=-cy+dxy$").set_color(RED)
        ).arrange(DOWN, aligned_edge=LEFT)
        equations.to_corner(UL)
        self.add(equations)

        axes = Axes(
            x_range=[0,60,1e6],
            y_range=[0,40,1e6],
            x_length=6,
            y_length=4, 
            **myaxis_config
        ).to_corner(DL)
        self.add(axes)

        stationary_point = Dot(axes.c2p(*X_f1))
        self.add(stationary_point)

        x,y = X.T
        graph = axes.plot_line_graph(x_values=x, y_values=y, add_vertex_dots=False)
        self.add(graph)
        fox_img = ImageMobject(fox).scale_to_fit_width(1.5).set_color(RED).next_to(axes.y_axis,RIGHT, aligned_edge=UP)
        bunny_img = ImageMobject(bunny).scale_to_fit_width(1).set_color(WHITE).next_to(axes.x_axis,RIGHT)
        self.add(fox_img,bunny_img)

        time = ValueTracker(0)
        
        allcurves = VGroup(
            *[axes.plot_line_graph(x_values=curves[i][:450,0], y_values=curves[i][:450,1], add_vertex_dots=False) for i in curves.keys()]
        )
        allcurves.set_stroke(color=BLUE, width=1)

        self.play(AnimationGroup(*[Create(_) for _ in allcurves],lag_ratio=0.3, run_time=4))
        self.add(allcurves)

        axes2 = Axes(
            x_range=[0,tmax,1e6],
            y_range=[0,60,1e6],
            x_length=8,
            y_length=2,
            **myaxis_config,

        )
        labels2 = VGroup(Tex(r"$t$").next_to(axes2.x_axis))
        graph2 = VGroup(axes2,labels2)
        graph2.to_corner(UR)
        self.add(graph2)
        graph_foxes = axes2.plot_line_graph(x_values=t, y_values=X[:,1], add_vertex_dots=False).set_color(RED)
        graph_bunnies = axes2.plot_line_graph(x_values=t, y_values=X[:,0], add_vertex_dots=False).set_color(WHITE)

        self.add(graph_foxes,graph_bunnies)

        def draw_for_animation(t_index):
            watches = VGroup(
                analog_indicator(x[t_index],value_max = 60,values = [0,10,20,30,40,50,60]),
                analog_indicator(y[t_index],value_max = 60,values = [0,10,20,30,40,50,60])
            ).arrange().to_edge(RIGHT)
            
            line_marker = VGroup(
                RegularPolygon(n=3, start_angle=np.pi / 2, stroke_width=0).set_fill(
                color=WHITE,
                opacity=1,
                ).scale(0.1).move_to(axes2.coords_to_point(t[t_index], 0), UP),
                DashedLine(start = axes2.coords_to_point(t[t_index], 0), end = axes2.coords_to_point(t[t_index], ymax))
            )
            line_marker[1].set_color(GRAY)
            line_marker[1].set_z_index(-1)
            dot_in_phase_space = Dot(axes.coords_to_point(x[t_index], y[t_index]))
            dot_in_phase_space.set_color(YELLOW)
            return(VGroup(line_marker,watches,dot_in_phase_space))

        report = always_redraw(lambda: draw_for_animation(int(time.get_value())) )
        fox_img_watches = ImageMobject(fox).scale_to_fit_width(0.5).set_color(RED).next_to(report[1][1],DOWN)
        bunny_img_watches = ImageMobject(bunny).scale_to_fit_width(.3).set_color(WHITE).next_to(report[1][0],DOWN)


        self.add(report, fox_img_watches, bunny_img_watches)

        for i in range(5):
            self.play(time.animate.set_value(tnumber-1), run_time=5, rate_func=linear)
            time.set_value(0)

        
        self.wait()

    
                  