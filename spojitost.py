from manim import *
import numpy as np
import common_definitions

from manim_editor import PresentationSectionType
template = TexTemplate(preamble=r'\usepackage{url}\usepackage[czech]{babel}\usepackage{amsmath}\usepackage{amssymb}')

class Spojitost(Scene):

    def construct(self):

        self.next_section("Nadpis")
        title = Title(r"Spojitost a limita funkce (pro $x=0$)")
        title.set_z_index(5).add_background_rectangle(buff=1)
        self.play(GrowFromCenter(title))
        domain = np.linspace(0,1,300)
        funkce = [
            [lambda x:x+1, r"Spojitá funkce."],
            [lambda x:1/x, r"Nespojitost v nule (diverguje do nekonečna)."],
            [lambda x:(x+np.abs(x))/x, r"Nespojitost v nule (konečný skok)."],
            [lambda x:(x**2+x)/(x), r"Ostranitelná nespojitost."],
        ]

        formulas = [
            r"f_1(x)=x+1",
            r"f_2(x)=\frac {1}x",
            r"f_3(x)=\frac {x+|x|}x",
            r"f_4(x)=\frac {x^2+x}{x}",
        ]

        axes = Axes(
            x_range=[-10.5,10.5,1],
            y_range=[-0.5,4.1,1],
            tips = False,
            y_length=5
            ).to_edge(DOWN, buff=.7)

        #self.remove(axes.get_y_axis())
        grafy = VGroup()
        komentar = VGroup()
        predchozi = None
        colors = [YELLOW,RED,GREEN,BLUE]
        ranges = [
            [[-2,0],[0,3]],
            [[-11,-0.05],[0.25,11]],
            [[-11,-0.015],[0.015,11]],
            [[-2,-0.015],[0.015,3]]
        ]        
        dots = [[],[],[0,2],[1]]

        texty = VGroup()
        for i,j in zip(formulas, colors):
            texty.add(MathTex(i).set_color(j))
        texty.arrange(DOWN, aligned_edge=LEFT)
        texty.next_to(title,DOWN, aligned_edge=LEFT)
        texty.shift(RIGHT*0.5+UP)
        texty.set_z_index(1000).add_background_rectangle()

        self.play(FadeIn(texty),FadeIn(axes))
        self.add(Tex(r"$x$").next_to(axes.get_x_axis(),DOWN, aligned_edge=RIGHT).set_z_index(10).add_background_rectangle())

        zapis_ = [
            r"$x+1$ je spojitá",
            r"$$\lim_{x\to 0^+}\frac 1x=\infty$$",
            r"$$\lim_{x\to 0^+}\frac{x+|x|}{x}=2$$",
            r"$$\lim_{x\to 0}\frac{x^2+x}{x}=1$$",
            ]

        zapis_ = [r"""\begin{minipage}{4cm}\raggedright Žlutá funkce je spojitá v~nule, 
           ostatní funkce mají v~nule nespojitost. V~případě modré funkce jde o~odstranitelnou 
           nespojitost (funkce jde učinit spojitou dodefinováním jedné funkční hodnoty). 
           \par
           \end{minipage}
           """]
        
        zapis = VGroup(*[
            Tex(_).scale(0.95).set_color(c) for _,c in zip(zapis_, colors)
            ])
        zapis.arrange(DOWN, aligned_edge=LEFT)
        zapis.set_z_index(100).set_color(WHITE).add_background_rectangle() 
        zapis.to_corner(UR).shift(DOWN)

        #i_ = 0       
        for f,t,c,ranges,dot in [[*i,j,k,l] for i,j,k,l in zip(funkce,colors,ranges,dots)]:            
            self.remove(komentar)
            soucasny = VGroup()
            for range in ranges:
                soucasny.add(axes.plot(f,x_range=[*range,0.01]).set_color(c).set_stroke(width=10))

            #self.play(FadeIn(texty[i_]))
            #i_ = i_ + 1
            dot_ = VGroup()
            for _ in dot:
                dot_.add(Circle(radius=0.1).set_stroke(width=6).set_color(c).move_to(axes.c2p(0,_)))

            if predchozi is None:
                self.play(Create(soucasny),FadeIn(dot_))
            else:
                self.play(TransformFromCopy(predchozi, soucasny),FadeIn(dot_))
            
            predchozi = soucasny
            grafy.add(soucasny)
            self.wait()
            self.next_section()

        self.wait()   
        self.next_section()
        self.play(FadeIn(zapis))
        self.wait()   

class Spojitost(Scene):
    def construct(self):
        self.next_section("Nadpis")
        title = Title(r"Ostranitelná nespojitost")
        title.set_z_index(5).add_background_rectangle(buff=1)
        self.play(GrowFromCenter(title))            
        #self.wait()


        axes = Axes(
            x_range=[-10.5,10.5,1],
            y_range=[-0.5,1.1,1],
            tips = False,
            y_length=2
            ).next_to(title, DOWN, buff=.7)        

        axes2 = axes.copy()
        axes2.next_to(axes,DOWN)

        def f(x):
            return np.sin(x)/x

        c = RED
        graf = axes.plot(f,x_range=[-10,10,0.01]).set_color(c)
        graf2 = VGroup()
        graf2.add(axes2.plot(f,x_range=[-10,-0.05,0.01]).set_color(c))
        graf2.add(axes2.plot(f,x_range=[0.05,10,0.01]).set_color(c))


        self.add(axes,axes2)
        self.play(Create(graf))
        for i in graf2:
            self.play(Create(i))
        self.wait()
