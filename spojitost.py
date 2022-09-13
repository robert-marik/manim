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
            [[-2,0.1],[0,3]],
            [[-11,-0.05],[0.25,11]],
            [[-11,-0.05],[0.05,11]],
            [[-2,-0.05],[0.05,3]]
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

        zapis_ = [r"""\begin{minipage}{7cm}\raggedright Žlutá funkce je spojitá v~nule. 
           Ostatní funkce mají v~nule bod nespojitosti. 
           V~případě modré funkce jde funkci učinit spojitou 
           dodefinováním jedné funkční hodnoty. Jedná se 
           o~odstranitelnou nespojitost. 
           \par
           \end{minipage}
           """]
        
        zapis = VGroup(*[
            Tex(_).scale(0.95).set_color(c) for _,c in zip(zapis_, colors)
            ])
        zapis.arrange(DOWN, aligned_edge=LEFT)
        zapis.set_z_index(1000).set_color(WHITE).add_background_rectangle(color=GRAY_BROWN, buff=0.2) 
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
                dot_.add(Circle(radius=0.07).set_stroke(width=6).set_color(c).move_to(axes.c2p(0,_)))

            if predchozi is None:
                self.play(Create(soucasny),FadeIn(dot_))
            else:
                self.play(TransformFromCopy(predchozi, soucasny),FadeIn(dot_))
            
            predchozi = soucasny
            grafy.add(soucasny)
            self.wait()
            self.next_section()

        self.play(FadeIn(zapis))
        self.wait()   



class Limita(Scene):
    def construct(self):
        self.next_section("Nadpis")
        title = Title(r"Ostranitelná nespojitost")
        title.set_z_index(5).add_background_rectangle(buff=.1)
        self.play(GrowFromCenter(title))            
        #self.wait()


        axes = Axes(
            x_range=[-8.5,8.5,1],
            y_range=[-0.1,1.1,1],
            tips = False,
            y_length=2,
            x_length=8
            ).to_corner(DR, buff=0.7)        

        axes2 = axes.copy()
        axes2.next_to(axes,UP, buff=1)

        limity = [r"1",r"1",r"{\displaystyle \frac 12}"]
        limity_num = [1,1,0.5]
        predpisy = [
            r"{\displaystyle \frac{\sin x}{x}}",
            r"{\displaystyle \frac{e^x-1}{x}}",
            r"{\displaystyle \frac{1-\cos x}{x^2}}"
        ]

        funkce = [
            lambda x:np.sin(x)/x, 
            lambda x:(np.exp(x)-1)/x, 
            lambda x:(1-np.cos(x))/x**2, 
            ]

        for i in range(3):

            def f(x):
                return funkce[i](x)
            limita = limity[i]
            limita_num = limity_num[i]
            predpis = predpisy[i]

            c = RED
            c2 = BLUE
            graf = axes.plot(f,x_range=[-8,8,0.03]).set_color(c)
            graf2 = VGroup()
            graf2.add(axes2.plot(f,x_range=[-8,-0.1,0.01]).set_color(c2))
            graf2.add(Circle(radius=0.05).set_stroke(width=3).move_to(axes2.c2p(0,limita_num)).set_color(c2))
            graf2.add(axes2.plot(f,x_range=[0.1,8,0.01]).set_color(c2))


            popisek2 = VGroup()
            popisek2.add(Tex(r"$$y="+predpis+r"$$"))
            popisek2.add(Tex(r"$$\lim_{x\to 0}"+predpis+r"="+limita+r"$$"))
            popisek2.set_color(c2).arrange(DOWN, aligned_edge=LEFT).next_to(axes2, LEFT).to_edge(LEFT)

            popisek = VGroup(
                Tex(r"$$y=\begin{cases}"+limita+r"&\text{pro $x=0$}\\[6pt]"+predpis+r" & \text{jinak} \end{cases}$$").set_color(c),
            ).arrange(DOWN, aligned_edge=LEFT).add_background_rectangle().next_to(axes, LEFT).to_edge(LEFT)

            self.play(FadeIn(popisek2[0]))
            self.add(axes2)
            self.play(Create(graf2[0]))
            self.add(graf2[1])
            self.play(Create(graf2[2]))
            self.play(FadeIn(popisek2[1]))

            self.next_section()
            self.wait()

            self.play(FadeIn(popisek))
            self.add(axes)
            self.play(Create(graf))

            self.next_section()
            self.wait()

            self.play(FadeOut(axes,axes2,graf,graf2,popisek,popisek2))

