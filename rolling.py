from tkinter import CENTER
from manim import *
from common_definitions import *
from scipy.interpolate import interp1d
from scipy.signal import argrelmin
from scipy.signal import argrelmax
from scipy import optimize

xmin = -7 
xmax = 7
dx = 0.3
a=4.6

x = np.linspace(xmin,xmax,1000)
y = 4.5  + np.cos(x/a*PI-PI/8)
dy = np.gradient(y,x)

mins = argrelmin(y)[0]
maxs = argrelmax(y)[0]

print(mins)
print(maxs)
st_points = [mins[0],maxs[0],mins[1]]
x_s = [ x[:mins[0]+1], x[mins[0]:maxs[0]+1],  x[maxs[0]:mins[1]+1], x[mins[1]:] ]
y_s = [ y[:mins[0]+1], y[mins[0]:maxs[0]+1],  y[maxs[0]:mins[1]+1], y[mins[1]:] ]
dy_s = [ dy[:mins[0]+1], dy[mins[0]:maxs[0]+1],  dy[maxs[0]:mins[1]+1], dy[mins[1]:] ]

radius = 0.2    
zvetseni = 1

p=np.array([np.array([x_,y_])+radius*1.5/zvetseni*np.array([-dy_,1])/np.sqrt(1+dy_**2) for x_,y_,dy_ in zip (x,y,dy)])
f1 = interp1d(p[:,0], p[:,1], kind='quadratic', fill_value='extrapolate', assume_sorted=True)
rustova_funkce = interp1d(x, -dy, kind='quadratic', fill_value='extrapolate', assume_sorted=True)

tl = 0.2  # tip length at the axis


class Intro(Scene):
    def construct(self):

        title = Title(r"Stabilita stacionárních bodů diferenciální rovnice")
        autor = VGroup(Tex("Robert Mařík"),Tex("Mendel University")).arrange(DOWN).next_to(title,DOWN)
        self.play(GrowFromCenter(title))
        self.play(GrowFromCenter(autor[0]))
        self.play(GrowFromCenter(autor[1]))
        self.wait(10)


class Stabilita(Scene):
    def construct(self):

        ax = Axes(axis_config={'color':'BLUE'}).scale(zvetseni).shift(2*DOWN)
        func_graphs = [ ax.plot_line_graph(i,j,add_vertex_dots=False) for i,j in zip(x_s,y_s) ]
        full_curve = ax.plot_line_graph(x,y,add_vertex_dots=False)
        ball_graph = ax.plot_line_graph(p[:,0],p[:,1],add_vertex_dots=False)

        pozice = ValueTracker(-0.2)
        ball=Dot(radius=radius).move_to(ax.c2p(pozice.get_value(),f1(pozice.get_value()),0))
        ball_shadow=ball.copy().set_color(GRAY).set_opacity(0.75)
        
        def posun():
            return ball.move_to(ax.c2p(pozice.get_value(),f1(pozice.get_value()),0))

        def posun_shadow():
            return ball_shadow.move_to(ax.c2p(pozice.get_value(),0,0))

        self.play(AnimationGroup(Create(full_curve), GrowFromCenter(ball), lag_ratio=1))
        kulicka = always_redraw(posun)
        kulicka_shadow = always_redraw(posun_shadow)

        self.add(kulicka)
        self.play(pozice.animate.set_value(x[mins[0]]), rate_func=rate_functions.linear)
        self.play(Flash(kulicka))
        self.wait()
        self.play(FadeOut(kulicka))
        
        pozice.set_value(x[maxs[0]])
        posun()
        self.play(FadeIn(kulicka))
        self.play(Flash(kulicka))
        self.wait()  
        self.play(AnimationGroup(
            *[ApplyWave(i, ripples=10, amplitude=.02) for i in [full_curve]],
            lag_ratio=0)
        )
        self.play(pozice.animate.set_value(x[mins[1]]), rate_func=rate_functions.linear)
        self.play(Flash(kulicka))
        self.wait()

        ball.generate_target()

        for dx in [0.5,-1,0.7,-0.3]:
            pozice.set_value(x[mins[1]]+dx)
            ball.target.move_to(ax.c2p(pozice.get_value(),f1(pozice.get_value()),0))
            self.play(AnimationGroup(
                *[ApplyWave(i, ripples=8, amplitude=.02) for i in [full_curve]],
                MoveToTarget(ball), 
                lag_ratio=0.5, rate_func=rate_functions.ease_out_bounce)
            )
            self.play(pozice.animate.set_value(x[mins[1]]), rate_func=rate_functions.linear)
        self.wait()

        # pozice.set_value(-2)  
        # self.play(pozice.animate.set_value(x[mins[0]]), rate_func=rate_functions.linear)


        colors = [BLUE,RED,BLUE,RED]
        for i,j in zip(func_graphs,colors):
            self.play(FadeToColor(i,j))

        self.remove(full_curve)    

        osax = Line(start=ax.c2p(xmin,0,0), end=ax.c2p(xmax-0.5,0,0), buff=0
        ).set_stroke(width=2
        ).add_tip(tip_length=tl)
        labelx = MathTex("x").next_to(osax)
        osay = Line(start=ax.c2p(xmin,-2,0), end=ax.c2p(xmin,6,0), buff=0).set_stroke(width=2).add_tip(tip_length=tl)
        labely = MathTex(r"\frac {\mathrm dx}{\mathrm dt}").next_to(osay,UP)
        self.add(osax,labelx)
        self.play(FadeOut(ball))

        self.wait()

        ineqs = [MathTex(r"\frac {\mathrm dx}{\mathrm dt}"+s+"0") for s in [">","<",">","<"]]
        for i,g,c in zip(ineqs,func_graphs,colors):
            i.set_color(c).scale(0.7)
            i.next_to(g,DOWN)

        portrait_arrows = VGroup()
        division = np.linspace(xmin,xmax-0.5,40)
        delta = division[1]-division[0]
        for i in range(len(division)-1):
            if rustova_funkce(division[i])*rustova_funkce(division[i+1])<=0:
                continue
            if rustova_funkce(division[i])>0:
                portrait_arrows.add(
                    Arrow(start=ax.c2p(division[i],0,0),end=ax.c2p(division[i+1],0,0),stroke_width=5, buff=0.01,
                    max_stroke_width_to_length_ratio=30, max_tip_length_to_length_ratio=0.6)
                    .set_color(BLUE)
                    .shift(0.1*DOWN))
            else:
                portrait_arrows.add(
                    Arrow(end=ax.c2p(division[i],0,0),start=ax.c2p(division[i+1],0,0),stroke_width =5, buff=0.01,
                    max_stroke_width_to_length_ratio=30, max_tip_length_to_length_ratio=0.6)
                    .set_color(RED)
                    .shift(0.1*UP))        

        self.play(FadeIn(portrait_arrows) )
        for i in range(4):
            self.play(GrowFromCenter(ineqs[i]))

        self.wait()
        
        dlines=VGroup()
        st_points_labels=VGroup()
        for i in st_points:
            dlines.add(DashedLine(start=ax.c2p(x[i],0,0), end=ax.c2p(x[i],y[i],0)))
            st_points_labels.add(Line(start=ax.c2p(x[i],-0.1,0), end=ax.c2p(x[i],0.1,0)))


        pozice.set_value(xmin)
        posun()
        posun_shadow()
        self.play(*[FadeIn(_) for _ in [ball,ball_shadow]])

        self.play(pozice.animate.set_value(x[mins[0]]), rate_func=rate_functions.linear)        
        self.play(Flash(kulicka), Flash(kulicka_shadow))

        self.wait()
        self.play(*[FadeOut(_) for _ in [ball,ball_shadow]])


        st_points_texts=VGroup()
        for i,j in enumerate(st_points_labels):
            st_points_texts.add(MathTex(r"x_{"+str(i+1)+r"}").next_to(j,DOWN))
        self.play(FadeIn(st_points_texts))   

        self.wait()

        for i in range(3):
            self.play(*[Indicate(_) for _ in [dlines[0],dlines[2]]])
        self.wait()
        for i in range(3):
            self.play(*[Indicate(_) for _ in [dlines[1]]])

        self.wait()
        self.play(FadeOut(*func_graphs, dlines))
        
        self.wait(5)
        self.play(*[FadeIn(_) for _ in [osay,labely,st_points_labels]])
        fx = ax.plot_line_graph(x,-2*dy,add_vertex_dots=False).set_color(YELLOW)
        graph_label = MathTex('f(x)').next_to(ax.c2p(x[0],-2*dy[0]),UP, aligned_edge=LEFT)
        graph_label.set_color(YELLOW).add_background_rectangle()
        self.play(Create(fx), FadeIn(graph_label))
        self.wait(3)
        
        ode = MathTex(r"\frac{\mathrm dx}{\mathrm dt}","=","f(x)").to_edge(UP)

        self.play(AnimationGroup(
            ReplacementTransform(labely.copy(),ode[0]),
            FadeIn(ode[1]),
            ReplacementTransform(graph_label.copy(),ode[2])
        ))



        zbytek=VGroup(st_points_labels,fx, osax, portrait_arrows, labelx, graph_label, st_points_texts)
        self.play(
            *[FadeOut(i) for i in [osay,labely,*ineqs]], 
            )

        self.play(zbytek.animate.shift(2*UP))

        for i in range(4):
            self.play(AnimationGroup(
                Flash(VGroup(Dot().set_color(BLACK).next_to(osax,LEFT),st_points_labels[0])),
                Flash(VGroup(st_points_labels[1],st_points_labels[2]))
                ))

        self.wait()

        for i in range(4):
            self.play(AnimationGroup(
                Flash(VGroup(st_points_labels[1],st_points_labels[0])),
                Flash(VGroup(st_points_labels[2],osax.tip))
                )
            )
        
        self.wait()
        for i in range(3):
            self.play(AnimationGroup(*[Flash(_) for _ in [#st_points_labels[0],st_points_labels[2], 
            st_points_texts[0], st_points_texts[2]]], lag_ratio=.05)
            )
        self.wait()
        for i in range(3):
            self.play(*[Flash(_) for _ in [#st_points_labels[1], 
            st_points_texts[1]]])

        self.wait()

    
class Bifurkace(Scene):
    def construct(self):
        rovnice = MathTex(r"\frac{\mathrm dx}{\mathrm dt}=f(x,\alpha)")
        rovnice.to_edge(UP)

        alpha = ValueTracker(0)
        bifurkace = 0.58

        def funkce(x):
            return 2*np.sin(x/a*PI-PI/8)*PI/a - x*alpha.get_value()

        ax = Axes(axis_config={'color':'BLUE'}).scale(zvetseni)
        #ax.shift(UP)

        self.play(FadeIn(rovnice))
        osax = Line(start=ax.c2p(xmin,0,0), end=ax.c2p(xmax-0.5,0,0), buff=0
            ).set_stroke(width=2
            ).add_tip(tip_length=tl)
        popisek = MathTex("x").next_to(osax)
        self.play(FadeIn(osax, popisek))

        graf = always_redraw(lambda: ax.plot(funkce,x_range=[xmin,xmax-0.5]).set_color(YELLOW) )
        hodiny = always_redraw(lambda: 
                VGroup(
                    VGroup(
                        Arc(radius=1.05, start_angle=20*DEGREES, angle=140*DEGREES)
                           .set_color(GREEN).set_stroke(width=10).stretch(0.75,1,about_point=ORIGIN),
                        Arc(radius=1.05, start_angle=20*DEGREES, angle=140*(1-bifurkace)*DEGREES)
                           .set_color(RED).set_stroke(width=10).stretch(0.75,1,about_point=ORIGIN),
                        analog_indicator(alpha.get_value(), values = [0,bifurkace,1], title=r"Parametr $\alpha$"),
                    ),
                    VGroup(
                            VGroup(Line(start=(0,0,0),end=(1,0,0)).set_color(GREEN).set_stroke(width=10),
                            Tex(r"dva stabilní stavy")
                            ).arrange().scale(0.65),
                            VGroup(Line(start=(0,0,0),end=(1,0,0)).set_color(RED).set_stroke(width=10),
                            Tex(r"jeden stabilní stav")
                            ).arrange().scale(0.65)
                        ).arrange(DOWN, aligned_edge=LEFT)
                    ).arrange(DOWN).next_to(rovnice, aligned_edge=UP)
        )

        def kresli_sipky():
            sol1 = optimize.broyden1(funkce, xmin)
            try:
                sol2 = optimize.broyden1(funkce, xmax)
            except:
                sol2 = sol1
            sol = [sol1,sol2]
            if abs(sol[1]-sol[0])<0.1:
                color = RED
            else:
                color = GREEN
            pointers = VGroup()
            for i in sol:
                pointers.add(
                    Arrow(
                        start=(0,1,0), 
                        end=(0,0,0),
                        stroke_width =5, 
                        color=color,
                        max_stroke_width_to_length_ratio=30, max_tip_length_to_length_ratio=0.3        
                    ).next_to(ax.c2p(i,0,0),UP)
                )
            return pointers         

        sipky = always_redraw(lambda: kresli_sipky())

        self.play(Create(graf),Create(hodiny), Create(sipky))

        self.play(alpha.animate.set_value(bifurkace), run_time=10)
        self.wait()
        self.play(alpha.animate.set_value(0.95), run_time=5)
        self.wait()

        self.play(alpha.animate.set_value(bifurkace-0.2), run_time=10)
        self.wait()

