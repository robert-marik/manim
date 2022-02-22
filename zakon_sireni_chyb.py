from manim import *
from scipy.integrate import solve_ivp  # řešení diferenciálních rovnic
import colorsys
import random
from common_definitions import *
import os
from manim_editor import PresentationSectionType
config.max_files_cached = 400
random.seed(10)


class Intro(Scene):

    def construct(self):
        self.next_section("Nadpis")
        title = Title(r"Zákon šíření chyb")
        autor = VGroup(Tex("Robert Mařík"),Tex("Mendel University")).arrange(DOWN).next_to(title,DOWN)
        self.play(GrowFromCenter(title))
        self.play(GrowFromCenter(autor[0]))
        self.play(GrowFromCenter(autor[1]))
        self.wait()

class Grafy(Scene):
    def construct(self):
        axes = Axes( 
            x_range=[0, 2, 10], 
            y_range=[0, 2, 10], 
            x_length=8, 
            y_length=4,
            tips = False,
        ).shift(UP) 
        self.play(Create(axes))
        graph = axes.plot_parametric_curve(lambda t: np.array([t**2,t]), t_range=[0,np.sqrt(2)], color=BLUE) 
        graph2 = axes.plot(lambda x: x**2, x_range=[0,np.sqrt(2),0.01] , color=RED) 

        def linka(bod):
            linky = VGroup()
            linky.add(Line(axes.c2p(bod[0],0,0),axes.c2p(*bod)))
            linky.add(Line(axes.c2p(*bod),axes.c2p(0,bod[1],0)))
            return linky

        delta_x = Line(axes.c2p(0.9,0,0),axes.c2p(1.1,0,0)).set_stroke(width=8)
        self.play(GrowFromCenter(delta_x))

        b1 = Brace(delta_x,DOWN)
        b1.add(Tex(r"Rozptyl\\na vstupu").scale(0.7).next_to(b1,DOWN))
        self.play(Create(b1))
        lines_1 = linka([1,1,0]).set_color(GRAY)
        lines_1b = linka([1.1,np.sqrt(1.1),0]).set_color(GRAY)
        lines_1a = linka([0.9,np.sqrt(0.9),0]).set_color(GRAY)
        
        delta_fx = Line(
            axes.c2p(0,np.sqrt(1.1),0),
            axes.c2p(0,np.sqrt(0.9),0),
            buff=0
            ).set_color(BLUE)
        delta_fx.set_stroke(width=8).shift(0.05*LEFT)
        delta_gx = Line(
            axes.c2p(0,(1.1)**2,0),
            axes.c2p(0,(0.9)**2,0),
            buff=0
            ).set_color(RED)
        delta_gx.set_stroke(width=8).shift(0.05*RIGHT)

        texty = VGroup(
                Tex(r"Rozptyl na výstupu:"),
                Tex(r"pomalu se měnící funkce (malá derivace)"),
                Tex(r"rychle se měnící funkce (velká derivace)")
        ).scale(0.7).arrange(DOWN, aligned_edge=LEFT).to_corner(UL).set_z_index(2)
        texty[1].shift(RIGHT)
        texty[2].shift(RIGHT)
        for i in range(3):
            texty[i].add_background_rectangle()


        lines_2 = linka([1,1,0]).set_color(GRAY)
        lines_2b = linka([1.1,(1.1)**2,0]).set_color(GRAY)
        lines_2a = linka([0.9,(0.9)**2,0]).set_color(GRAY)

        self.play(Create(graph))
        self.play(Create(lines_1)) 
        self.play(Create(lines_1a),Create(lines_1b)) 
        self.play(GrowFromCenter(delta_fx))
        self.play(
            delta_fx.copy().animate.rotate(PI/2).next_to(texty[1],LEFT),
            FadeIn(texty[:2])
            )

        self.play(FadeOut(lines_1b,lines_1a,lines_1))

        self.play(Create(graph2))
        self.play(Create(lines_2)) 
        self.play(Create(lines_2a),Create(lines_2b)) 
        self.play(GrowFromCenter(delta_gx))

        self.play(
            delta_gx.copy().animate.rotate(PI/2).next_to(texty[2],LEFT),
            FadeIn(texty[ 2])
        )
    
        self.wait()     

class Zakon1(Scene):

    def construct(self):
        self.font_size = 10

        self.next_section("Zakon sireni chyb")
        title = Title(r"Zákon šíření chyb pro funkci $y=f(x)$ jedné proměnné $x$")
        texty=VGroup()
        texty.add(            
            Tex(r"$\bullet$ Z měření máme $x=\overline x\pm\Delta x.$"),
            Tex(r"""
                $\bullet$ Výpočtem stanovíme $\overline y=f(\overline x)$ 
                a $\displaystyle\Delta y = 
                \left|\frac{\mathrm df}{\mathrm dx}(\overline x)\right|\Delta x$."""),
            Tex(r"$\bullet$ Hodnota veličiny $y$ je $y=\overline y\pm \Delta y$.")            
            )
        texty.arrange(DOWN, aligned_edge=LEFT).next_to(title,DOWN)

        self.play(GrowFromCenter(title))
        self.add(texty)
        self.wait()

class Zakon2(Scene):

    def construct(self):
        self.font_size = 10

        self.next_section("Zakon sireni chyb 2")
        title = Title(r"Zákon šíření chyb pro funkci $y=f(x_1,x_2)$\\  dvou proměnných $x_1$ a $x_2$")
        texty=VGroup()
        texty.add(            
            Tex(r"""
                $\bullet$ Z měření máme $x_1=\overline x\pm\Delta x_1$ a 
                $x_2=\overline x\pm\Delta x_2$."""),
            Tex(r"""
                $\bullet$ Vypočteme $\overline y=f(\overline x_1,\overline x_2)$ a
                $\displaystyle\Delta y_i = 
                \left|\frac{\partial f}{\partial x_i}(\overline x_1,\overline x_2)
                \right|\Delta x_i$.
                """),
            Tex(r"""$\bullet$ Celková chyba se vypočte 
            pomocí Eklidovské metriky 
            $$ \Delta y = \sqrt{ 
                \left(\frac{\partial f}{\partial x_1}(\overline x_1,\overline x_2) \Delta x_1
                \right)^2
                +
                \left(\frac{\partial f}{\partial x_2}(\overline x_1,\overline x_2) \Delta x_2
                \right)^2.
             }$$
            """),
            Tex(r"$\bullet$ Hodnota veličiny $y$ je $y=\overline y\pm \Delta y$.")            
            )
        texty.arrange(DOWN, aligned_edge=LEFT).next_to(title,DOWN)

        self.play(GrowFromCenter(title))
        self.add(texty)
        self.wait()
