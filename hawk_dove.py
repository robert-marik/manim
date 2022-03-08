from manim import *
from scipy.integrate import solve_ivp  # řešení diferenciálních rovnic
import colorsys
import random
import os
from manim_editor import PresentationSectionType

config.max_files_cached = 200
random.seed(10)


class Intro(Scene):

    def construct(self):

        self.next_section("Nadpis")

        title = Title(r"Model soupeření jedinců jestřábí a holubičí povahy")
        autor = VGroup(Tex("Robert Mařík"),Tex("Mendel University")).arrange(DOWN).next_to(title,DOWN)
        self.play(GrowFromCenter(title))
        self.play(GrowFromCenter(autor[0]))
        self.play(GrowFromCenter(autor[1]))
        self.wait()


def rhs(V,D):
    return (D*(1-D)*(1-V/D))

class Simulace(Scene):

    def construct(self):

        self.next_section("")
        self.portrety()
        self.wait()

        self.next_section("Opatrny lov")
        self.clear()
        self.portrety(h=0.19, IC=0.35, wait_duration=0.5)
        self.wait()

        self.next_section("Intenzivni lov")
        self.clear()
        self.portrety(h=0.3, IC=0.4, max_step_IC=0.01, wait_duration=0.5)
        self.wait()

    def portrety(self, h=0, IC=0.1, max_step_IC=0.05, wait_duration=1):

        tmin = 0
        tmax = 10
        ymin = -0.2
        ymax = 1.3
        dymin = -0.5
        dymax = 0.5
        t = np.linspace(tmin,tmax,200)
        r = 1
        K = 1

        text = Tex(r"Časový vývoj").scale(1.5).scale(0.5)
        ax = Axes(                    
            x_range=[tmin-1, tmax, 100],
            y_range=[ymin, ymax, 100],                    
            tips=True,                    
            axis_config={"include_numbers": False},
            ).scale(0.5)
        
        axt = VGroup(text,ax).arrange(DOWN)
        axt.to_corner(UL, buff=0.5)

        ax2 = Axes(                    
            x_range=[ymin, ymax, K],
            y_range=[dymin,dymax, 10],                    
            tips=True,                    
            axis_config={"include_numbers": False},
            )

        if h==0:
            nadpis = r"Fázový portrét bez lovu, $h=0$"
            y_points = [0,0,K,ymax]
        elif h<(r*K)/4:
            nadpis = r"Fázový portrét s malým lovem"
            y_points = [0, K*(1-np.sqrt(1-4*h/(r*K)))/2, K*(1+np.sqrt(1-4*h/(r*K)))/2,ymax]
        else:
            nadpis = r"Fázový portrét s velkým lovem"
            y_points = [0,0,0,ymax]

        text2 = Tex(nadpis).scale(1.5)
        axt2 = VGroup(text2,ax2).arrange(DOWN, buff=1.5).to_edge(UP)

        rovnice = MathTex(r"\displaystyle \frac{\mathrm dy}{\mathrm dt}=ry\left(1-\frac yK\right)-h").scale(1.5).set_color(YELLOW).next_to(text2,DOWN,aligned_edge=RIGHT, buff=0.4)
        rovnice.shift(RIGHT)
        axt2.add(rovnice)


        labels = []
        labels += [MathTex("K").scale(1.5).scale(0.5).next_to(ax.c2p(0,K,0), LEFT, buff=0.1)]       
        labels += [MathTex("t").scale(1.5).scale(0.5).next_to(ax.c2p(tmax,0,0), RIGHT, buff=0.2)]       
        labels += [MathTex("y").scale(1.5).scale(0.5).next_to(ax.c2p(0,ymax,0), UP, buff=0.2)]       

        labels2= []
        labels2 += [MathTex("K").scale(1.5).next_to(ax2.c2p(K,0,0), DOWN, buff=0.2)]
        labels2 += [MathTex("y").scale(1.5).next_to(ax2.c2p(ymax,0,0), RIGHT, buff=0.1)]       
        labels2 += [MathTex(r"\textstyle\frac{\mathrm dy}{\mathrm dt}").scale(1.5).next_to(ax2.c2p(0,dymax,0), UP, buff=0.1)]

        def rustova_funkce(x):
            return(r*x*(1-x/K)-h)


        rust = VGroup(
            ax2.plot(rustova_funkce, x_range=(y_points[0], y_points[1], 0.001), stroke_width=8).set_color(RED),
            ax2.plot(rustova_funkce, x_range=(y_points[1], y_points[2], 0.01), stroke_width=8).set_color(BLUE),
            ax2.plot(rustova_funkce, x_range=(y_points[2], y_points[3], 0.01), stroke_width=8).set_color(RED),
        )

        self.add(axt2,*labels2)
        self.wait()
        self.add(rust)
        self.wait()
        self.next_section("")
        self.play(VGroup(axt2,*labels2,rust).animate.scale(0.5).to_corner(UR))

        sp = ax.plot_line_graph([tmin,tmax],[K,K],add_vertex_dots=False).set_color(GREEN)

        self.play(FadeIn(axt,sp,*labels))

        increase = []
        increase += [ax2.plot_line_graph([y_points[1],y_points[2]],[0,0],add_vertex_dots=False, stroke_width=8).set_color(BLUE)]
        increase += [ax.plot_line_graph([0,0],[y_points[1],y_points[2]],add_vertex_dots=False, stroke_width=8).set_color(BLUE)]

        decrease = []
        decrease += [ax2.plot_line_graph([y_points[0],y_points[1]],[0,0],add_vertex_dots=False, stroke_width=8).set_color(RED)]
        decrease += [ax.plot_line_graph([0,0],[y_points[0],y_points[1]],add_vertex_dots=False, stroke_width=8).set_color(RED)]
        decrease += [ax2.plot_line_graph([y_points[2],y_points[3]],[0,0],add_vertex_dots=False, stroke_width=8).set_color(RED)]
        decrease += [ax.plot_line_graph([0,0],[y_points[2],y_points[3]],add_vertex_dots=False, stroke_width=8).set_color(RED)]

        portrait_arrows = VGroup()
        division = np.linspace(0,ymax,15)
        delta = division[1]-division[0]
        for i in range(len(division)-1):
            if rustova_funkce(division[i])*rustova_funkce(division[i+1])<=0:
                continue
            if rustova_funkce(division[i])>0:
                portrait_arrows.add(Arrow(start=ax2.c2p(division[i],0,0),end=ax2.c2p(division[i+1],0,0),stroke_width=10, buff=0.05,
                    max_stroke_width_to_length_ratio=15, max_tip_length_to_length_ratio=0.6)
                    .set_color(BLUE)
                    .shift(0.1*DOWN))
            else:
                portrait_arrows.add(Arrow(end=ax2.c2p(division[i],0,0),start=ax2.c2p(division[i+1],0,0),stroke_width =10, buff=0.05,
                max_stroke_width_to_length_ratio=15, max_tip_length_to_length_ratio=0.6)
                .set_color(RED)
                .shift(0.1*UP))

        transforms1 = [
            ReplacementTransform(rust[0].copy(),decrease[0]),
            ReplacementTransform(rust[1].copy(),increase[0]),
            ReplacementTransform(rust[2].copy(),decrease[2]),
            FadeIn(portrait_arrows)
        ]

        transforms2 = [
            ReplacementTransform(decrease[0],decrease[1]),
            ReplacementTransform(increase[0],increase[1]),
            ReplacementTransform(decrease[2],decrease[3])
        ]

        self.play(AnimationGroup(*transforms1, lag_ratio=0.2))
        self.play(AnimationGroup(*transforms2, lag_ratio=0.2))
        self.wait()

        self.next_section("")
        # Solve IVP
        def event(x, y):
            return y

        event.terminal = True    

        sol = [solve_ivp(lambda t, x: r*x*(1-x/K)-h, [tmin,tmax], [i], t_eval=t, events=[event], max_step=0.1) for i in np.linspace(0.05,1.5,20)]
        solIC = solve_ivp(lambda t, x: r*x*(1-x/K)-h, [tmin,tmax], [IC], t_eval=t, events=[event], max_step=max_step_IC )

        s = solIC
        x = s.t
        y = s.y[0]
        if len(x)<len(t):
            x = np.append(x,x[-1])
            y = np.append(y,0)
        #print(y)

        # Increasing and decreasing solutions are drawn with different colors
        def n2c(number):
            if number > y_points[1] and number < y_points[2]:
                return(YELLOW)
            else:
                return(WHITE)    

        cs = [n2c(s.y[0][0]) for s in sol]
        p = [ax.plot_line_graph(s.t,s.y[0],add_vertex_dots=False,stroke_width=2).set_color(c) for s,c in zip(sol,cs)]

        self.play(AnimationGroup(
            *[Create(_) for _ in p],
        lag_ratio=0.2))

        self.next_section("")
        mouse= ImageMobject(obrazek).scale_to_fit_width(.8).set_color(WHITE).to_corner(DL)

        ax3xmax=24.5
        ax3ymax=5.5
        ax3 = Axes(                    
            x_range=[0, ax3xmax, 10],
            y_range=[0, ax3ymax, 1],                    
            y_length=2,
            tips=False,                    
            axis_config={"include_numbers": False},
            ).to_edge(DOWN, buff=1.5)
        
        pocet = 10
        mouses = Group(*[mouse.copy() for i in range(pocet)]).arrange().set_color(GRAY).to_edge(DOWN)

        self.add(*mouses)

        poloha = ValueTracker(1)

        def barva(procento,i,j):
            pocet = 6*25
            if procento*pocet>i*6+j+1:
                barva = "#FFA500"
            else:
                barva = GRAY
            #print(procento,pocet*procento,i,j,i*6+j+1,barva)
            return(barva)

        def barva(procento,srovnani):
            if procento*100>srovnani:
                barva = "#FFA500"
            else:
                barva = GRAY
            #print(procento,pocet*procento,i,j,i*6+j+1,barva)
            return(barva)

        mouss = [mouse.copy().scale(0.6).move_to(ax3.c2p(i,j,0)).set_color(RED) for i in range(25) for j in range(6)]
        
        self.add(poloha)

        H = 1.5
        W = 8
        r0 = Rectangle(width=W,height=H, fill_opacity=0.5).set_color(GRAY).to_edge(DOWN,buff=1.5)
        self.add(r0)
        r1 = always_redraw(lambda: Rectangle(width=W*y[int(np.round(poloha.get_value()/K))],height=H, fill_opacity=0.5)
            .set_color("#FFA500").move_to(r0,aligned_edge=DL))
        self.add(r1)
        
        text_nosna_kapacita = Tex(" Obsazenost: ").move_to(r0).shift(LEFT)
        self.add(text_nosna_kapacita)
        value_nosna_kapacita = always_redraw(
            lambda: DecimalNumber(num_decimal_places=1)
            .set_value(100*y[int(np.round(poloha.get_value()/K))])
            .next_to(text_nosna_kapacita, RIGHT, buff=0.5)
        )
        text_procenta = Tex(r"\%\,$K$").next_to(value_nosna_kapacita)
        self.add(value_nosna_kapacita,text_procenta)

        pIC = always_redraw(lambda: ax
            .plot_line_graph(x[:int(np.round(poloha.get_value()))],y[:int(np.round(poloha.get_value()))],
                add_vertex_dots=False,stroke_width=2)
            .set_color("#FFA500"))
        mouse_curve = always_redraw(lambda: mouse.copy().scale(0.5).set_color("#FFA500")
            .move_to(ax.c2p(x[int(np.round(poloha.get_value()))],y[int(np.round(poloha.get_value()))],0)))
        mouse_phase = always_redraw(lambda: mouse.copy().scale(0.5).set_color("#FFA500")
            .move_to(ax2.c2p(y[int(np.round(poloha.get_value()))],rustova_funkce(y[int(np.round(poloha.get_value()))]),0)))
            
        self.add(mouse_curve,mouse_phase,pIC)
        self.wait()

        self.next_section("")
        self.play(poloha.animate.set_value(len(x)-1), run_time=6, rate_func=linear)
        self.wait()

komentar = """

"""