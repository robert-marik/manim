from typing_extensions import runtime
from manim import *
import colorsys
import random

import numpy as np
from common_definitions import *
import os
from scipy.integrate import solve_ivp  # řešení diferenciálních rovnic


# https://scipy-cookbook.readthedocs.io/items/LoktaVolterraTutorial.html
# Definition of parameters
a = 1.
b = 0.1
c = 1.5
d = 0.75*b
higher_a = 1.5
def dX_dt(X, t=0, a=a):
    """ Return the growth rate of fox and rabbit populations. """
    return np.array([ a*X[0] -   b*X[0]*X[1] ,
                  -c*X[1] + d*X[0]*X[1] ])

X_f0 = np.array([     0. ,  0.])
X_f1 = np.array([ c/(d), a/b])
X_f1_higher_a = np.array([ c/(d), higher_a/b])

tmin = 0
tmax = 16.6 # maximum for time on graph
ymax = 60 # maximum on y axis´for graphs in time
tnumber = 1000
max_step_IC = tmax/tnumber*2
t = np.linspace(tmin, tmax,  tnumber)              # time

curves = {}
curves_higher_a = {}
number_of_curves = 9
for i in range(1,number_of_curves):
    X0 = np.array([60+i/number_of_curves*(-60+c/(d)), a/b]) 
    curves[i] = solve_ivp(
        lambda t, X: dX_dt(X,t), 
        [tmin,tmax], [*X0], t_eval=t, max_step=max_step_IC 
    ).y
    curves_higher_a[i] = solve_ivp(
        lambda t, X: dX_dt(X,t,a=higher_a), 
        [tmin,tmax], [*X0], t_eval=t, max_step=max_step_IC 
    ).y
X = curves.pop(4)
X_higher_a = curves_higher_a.pop(4)

bunny = os.path.join("icons","rabbit-shape")
fox = os.path.join("icons","fox-sitting")
myaxis_config={'tips':False}

class Intro(Scene):

    def construct(self):
        title = Title(r"Model dravce a kořisti")
        autor = VGroup(Tex("Robert Mařík"),Tex("Mendel University")).arrange(DOWN).next_to(title,DOWN)
        self.play(GrowFromCenter(title))
        self.play(GrowFromCenter(autor[0]))
        self.play(GrowFromCenter(autor[1]))
        self.wait(4)

        fox_img = ImageMobject(fox)
        bunny_img = ImageMobject(bunny)
        imgs = Group(
            fox_img.scale_to_fit_width(1.5).set_color(RED),
            bunny_img.scale_to_fit_width(1).set_color(WHITE)
        ).arrange(buff=1)
        self.play(FadeIn(imgs), run_time=10)
        self.wait(10)

class Odvozeni(Scene):

    def construct(self):
        
        assumptions = VGroup(*[Tex(r"\begin{minipage}{12cm}$\bullet$ "+_+r"\end{minipage}").scale(0.8) for _ in  [
                r"Rychlost růstu populace kořisti je úměrná velikosti její populace.",
                r"Rychlost s jakou dravec hubí kořist je úměrná velikosti obou populací.",
                r"Rychlost poklesu populace dravce je úměrná velikosti jeho populace.",
                r"Rychlost s jakou přístup ke kořisti posiluje populaci dravce je úměrná velikosti obou populací.",
            ]]
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(UP)
        self.wait()

        equations = VGroup(
            MathTex(r"\displaystyle\frac{\mathrm dx}{\mathrm dt}","{}=ax","{}-bxy"),
            MathTex(r"\displaystyle\frac{\mathrm dy}{\mathrm dt}{}","{}=-cy","{}+dxy").set_color(RED)
        ).arrange(DOWN, aligned_edge=LEFT,buff=1)
        equations.next_to(assumptions,DOWN)

        fox_img = ImageMobject(fox)
        bunny_img = ImageMobject(bunny)
        imgs = Group(
            bunny_img.scale_to_fit_width(1).set_color(WHITE),
            fox_img.scale_to_fit_width(1.5).set_color(RED)
        ).arrange(DOWN,buff=0.5)
        imgs.next_to(equations,LEFT, buff=1)

        self.add(imgs)

        count = 0
        for i,j in [
            [assumptions[0],equations[0][:2]],
            [assumptions[1],equations[0][2]],
            [assumptions[2],equations[1][:2]],
            [assumptions[3],equations[1][2]],
            ]:
            self.play(FadeIn(i,j))
            r1 = SurroundingRectangle(i)
            r2 = SurroundingRectangle(j)
            count += 1
            self.play(
                AnimationGroup(
                    Create(r1),Create(r2),
                    lag_ratio=.2
                ), run_time=2
            ) 
            self.wait()
            self.play(
                AnimationGroup(
                    FadeOut(r1),FadeOut(r2),
                    lag_ratio=.2
                ), run_time=2
            ) 
            self.wait()



class PhasePortrait(Scene):
    def construct(self):

        equations = VGroup(
            MathTex(r"\displaystyle\frac{\mathrm dx}{\mathrm dt}","{}={}","ax-bxy"),
            MathTex(r"\displaystyle\frac{\mathrm dy}{\mathrm dt}{}","{}={}","-cy+dxy").set_color(RED)
        ).arrange(DOWN, aligned_edge=LEFT)
        equations.to_corner(UL)
        self.add(equations)

        phase_portarit = Group()
        axes = Axes(
            x_range=[0,60,1e6],
            y_range=[0,40,1e6],
            x_length=6,
            y_length=4, 
            **myaxis_config
        )
        axes.y_axis.set_color(RED).set(stroke_width=6)
        axes.x_axis.set(stroke_width=6)
        phase_portarit.add(axes)
        stationary_point = Dot(axes.c2p(*X_f1)).set_z_index(2)
        phase_portarit.add(stationary_point)

        fox_img = ImageMobject(fox)
        fox_img.scale_to_fit_width(1.5).set_color(RED).next_to(axes.y_axis, LEFT, aligned_edge=UP)
        fox_img.set_z_index(-1)
        bunny_img = ImageMobject(bunny)
        bunny_img.scale_to_fit_width(1).set_color(WHITE).next_to(axes.x_axis,RIGHT)
        bunny_img.set_z_index(-1)
        phase_portarit.add(fox_img,bunny_img)
        phase_portarit.to_corner(DL)
        self.add(phase_portarit)

        phase_portarit_arrows = VGroup()
        delka = 3

        data = []        
        for i in np.linspace(*axes.x_range[:2],12):
            for j in np.linspace(*axes.y_range[:2],12):
                if i*j == 0:
                    continue
                start = np.array([i,j])
                rhs = dX_dt([i,j])
                norm = np.sqrt(rhs[0]**2+rhs[1]**2)
                end = start + rhs/norm*delka
                data += [[start,end,norm]]

        maximum = np.max([i[2] for i in data])
        for i in data:                                
            phase_portarit_arrows.add(
                Arrow(
                    start=axes.c2p(*i[0],0), 
                    end=axes.c2p(*i[1],0), 
                    buff=0, 
                    max_stroke_width_to_length_ratio = 20, 
                    max_tip_length_to_length_ratio = 0.4,
                    color = temperature_to_color(i[2]*5, min_temp=0, max_temp=maximum),
                    stroke_width=10,
                )
            )

        self.add(phase_portarit_arrows)        
        self.wait()
        self.play(AnimationGroup(
            *[i.animate.set_fill(opacity = 0.5).set_stroke(opacity=0.5) for i in phase_portarit_arrows]
            ))

        x,y = X
        graph = axes.plot_line_graph(*X, add_vertex_dots=False)
        self.add(graph)

        time = ValueTracker(0)
        
        allcurves = VGroup(
            *[axes.plot_line_graph(*curves[i][:][:450], add_vertex_dots=False) for i in curves.keys()]
        )
        allcurves.set_stroke(color=BLUE, width=2)

        self.play(AnimationGroup(*[Create(_) for _ in allcurves],lag_ratio=0.1, run_time=3))
        self.add(allcurves)

        axes2 = Axes(
            x_range=[0,tmax,1e6],
            y_range=[0,60,1e6],
            x_length=8,
            y_length=2,
            **myaxis_config
        )
        labels2 = VGroup(Tex(r"$t$").next_to(axes2.x_axis))
        graph2 = VGroup(axes2,labels2)
        graph2.to_corner(UR)
        self.add(graph2)

        graph_foxes = axes2.plot_line_graph(
            x_values=t, 
            y_values=X[1], 
            add_vertex_dots=False
        ).set_color(RED)
        graph_bunnies = axes2.plot_line_graph(
            x_values=t, 
            y_values=X[0], 
            add_vertex_dots=False
        ).set_color(WHITE)
        self.add(graph_foxes,graph_bunnies)

        kwds = {
                'value_max' : 60, 
                'values' : [0,10,20,30,40,50,60]
                }
        def draw_for_animation(t_index):
            watches = VGroup(
                analog_indicator(x[t_index],**kwds),
                analog_indicator(y[t_index],**kwds)
            ).arrange().to_edge(RIGHT).shift(DOWN*0.5)
            
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
        fox_img_watches = ImageMobject(fox).scale_to_fit_width(0.65).set_color(RED).next_to(report[1][1],DOWN)
        bunny_img_watches = ImageMobject(bunny).scale_to_fit_width(.3).set_color(WHITE).next_to(report[1][0],DOWN)
        self.add(report, fox_img_watches, bunny_img_watches)

        for i in range(5):
            self.play(time.animate.set_value(tnumber-1), run_time=5, rate_func=linear)
            time.set_value(0)
        
        self.wait()

        self.play(AnimationGroup(
            *[FadeOut(_) for _ in [*axes2, labels2, *report, fox_img_watches, 
                                    bunny_img_watches, 
                                    graph_foxes,graph_bunnies, phase_portarit_arrows]
            ],
            Group(
                allcurves, phase_portarit, graph, 
            ).animate.scale(1.2).to_corner(UR, buff=.1),
            lag_ratio=0.05)
        )
        self.play(fox_img.animate.next_to(axes.y_axis, RIGHT, aligned_edge=UP))

        # stability_conditions=VGroup(
        #     MathTex(r"\displaystyle\frac{\mathrm dx}{\mathrm dt}=0 \implies y=\frac ba"),
        #     MathTex(r"\displaystyle\frac{\mathrm dy}{\mathrm dt}=0 \implies x=\frac cd"),
        # ).arrange(DOWN).to_corner(UR)

        # stability_derivation = equations.copy()
        # self.play(stability_derivation.animate.next_to(stability_conditions,DOWN).set_color(WHITE))

        equations2 = VGroup(
            MathTex(r"0","{}={}","ax-bxy"),
            MathTex(r"0","{}={}","-cy+dxy")
        ).arrange(DOWN, aligned_edge=LEFT)
        equations2.next_to(equations, DOWN, buff=1)

        equations3 = VGroup(
            MathTex(r"0","{}={}","a-by"),
            MathTex(r"0","{}={}","-c+dx")
        ).arrange(DOWN, aligned_edge=LEFT)
        equations3.move_to(equations2)

        equations3b = VGroup(
            MathTex(r"by","{}={}","a"),
            MathTex(r"c","{}={}","dx")
        ).arrange(DOWN, aligned_edge=LEFT)
        equations3b.move_to(equations2)

        equations4 = VGroup(
            MathTex(r"y","{}={}",r"\displaystyle\frac ab"),
            MathTex(r"x","{}={}",r"\displaystyle\frac cd")
        ).arrange(DOWN, aligned_edge=LEFT)
        equations4.move_to(equations3)

        self.play(AnimationGroup(
            FadeIn(equations2[0][0]),
            FadeIn(equations2[0][1]),
            FadeIn(equations2[1][0]),
            FadeIn(equations2[1][1])))
        self.play(AnimationGroup(
            ReplacementTransform(equations[0][2].copy(),equations2[0][2]),
            ReplacementTransform(equations[1][2].copy(),equations2[1][2]),
            lag_ratio=1
        ))
        
        self.play(AnimationGroup(
            *[TransformMatchingShapes(_,__) for _,__ in zip(equations2,equations3)],
            lag_ratio=1
        ))

        self.play(AnimationGroup(
            *[TransformMatchingShapes(_,__) for _,__ in zip(equations3,equations3b)],
            lag_ratio=1
        ))

        self.play(AnimationGroup(
            *[TransformMatchingShapes(_,__) for _,__ in zip(equations3b,equations4)],
            lag_ratio=1
        ))

        self.wait()

        line_x = axes.get_vertical_line(stationary_point.get_center())
        line_y = axes.get_horizontal_line(stationary_point.get_center())
        label_x = MathTex("c/d").scale(.7).next_to(line_x,DOWN).set_color(RED)
        label_y = MathTex("a/b").scale(.7).next_to(line_y,LEFT)

        self.add(line_x,line_y)

        self.play(AnimationGroup(
            TransformMatchingShapes(equations4[0][2].copy(),label_y),
            TransformMatchingShapes(equations4[1][2].copy(),label_x),
            lag_ratio=1
        ))

        self.wait()

        graph_higher_a = axes.plot_line_graph(*X_higher_a, add_vertex_dots=False)
        allcurves_higher_a = VGroup(
            *[axes.plot_line_graph(*curves_higher_a[i][:][:450], add_vertex_dots=False) for i in curves.keys()]
        )
        allcurves_higher_a.set_stroke(color=PURPLE, width=2)
        stationary_point_higher_a = Dot(axes.c2p(*X_f1_higher_a)).set_z_index(2)
        
        allcurves.set_stroke(color=BLUE, width=4)
        allcurves_higher_a.set_stroke(color=BLUE, width=4)


        self.play(
            AnimationGroup(
                FadeOut(line_x, line_y, label_x, label_y),
                FadeIn(stationary_point_higher_a),
                *[
                    AnimationGroup(FadeOut(_),FadeIn(__)) for _,__ in zip(
                        [*allcurves[:4], graph, *allcurves[4:]],
                        [*allcurves_higher_a[:4], graph_higher_a, *allcurves_higher_a[4:]] 
                        )
                ],
                FadeToColor(stationary_point,GRAY),
                lag_ratio=1,
                run_time=5
            )
        )
        # self.play(
        #     AnimationGroup(
        #         FadeOut(line_x, line_y, label_x, label_y),
        #         *[
        #             ReplacementTransform(_,__) for _,__ in zip(
        #                 [*allcurves, stationary_point.copy(), graph],
        #                 [*allcurves_higher_a, stationary_point_higher_a, graph_higher_a] 
        #                 )
        #         ],
        #         FadeToColor(stationary_point,GRAY),
        #         lag_ratio=0.2
        #     )
        # )


        self.wait()

    
                  