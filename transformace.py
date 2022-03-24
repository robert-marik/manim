from tkinter import CENTER
from turtle import fillcolor
from manim import *
from scipy.integrate import solve_ivp  # řešení diferenciálních rovnic
import colorsys
import random
import os
from manim_editor import PresentationSectionType
from common_definitions import *

template = TexTemplate(preamble=r'\usepackage{url}\usepackage[czech]{babel}\usepackage{amsmath}\usepackage{amssymb}')

class TransformaceJenotek(Scene):
    def construct(self):
        
        def MujTex(text):
            return(Tex(r"$\bullet$ \quad \begin{minipage}[t]{10cm}"+text+"\end{minipage}", tex_template=template).scale(.9))

        text = VGroup(
            MujTex(r"Pokud zvětšíme jednotku veličiny, její numerická hodnota se zmenší stejným násobkem. Například $2400\,\mathrm m = 2{,}4\mathrm{km}.$"),
            MujTex(r"Pokud zvětšíme jednotku derivované veličiny, numerická hodnota derivace se zmenší stejným násobkem. Například $2400\,\mathrm m \,\mathrm{min}^{-1}= 2{,}4\,\mathrm{km}\,\mathrm{min}^{-1}.$"),
            MujTex(r"Pokud zmenšíme jednotku veličiny podle níž derivujeme, numerická hodnota derivace se zmenší stejným násobkem. Například $2400\,\mathrm m \,\mathrm{min}^{-1}= 40\,\mathrm{m}\,\mathrm{s}^{-1}.$"),
            MujTex(r"Změnou jednotek dokážeme měnit hodnoty veličin. Většinou chceme mít standardizované jednotky, aby se daly sdílet měřící přístroje a porovnávat hodnoty. Někdy se ale hodí mít jednotky vlastní související třeba jen s jedním konkrétním problémem.")
        ).arrange(DOWN, aligned_edge=LEFT)

        for i in text:
            self.play(FadeIn(i))
            self.wait()

class Teplota(Scene):
    def construct(self):
        
        merak = VGroup()
        merak.add(Dot(
            radius=0.1,
            stroke_color=WHITE,
            stroke_width=4,
            fill_color=RED,
            fill_opacity=1
        ))
        merak.add(
            Line(
                start = (0,0,0), 
                end = 3*UP
                ).set_z_index(-1).set_stroke(width=10)
        )
        merak.add(
            Line(
                start = (0,0,0), 
                end = 2.6*UP, 
                color=RED
            ).set_stroke(width=6)
        )
        merak.shift(0.2*DOWN)

        carka = Line(start = RIGHT*0, end=LEFT*0.13, buff=0)
        carka_delsi = Line(start = RIGHT*0, end=LEFT*0.18, buff=0)
        stupnice = VGroup()
        for i in range(27):
            if (i-3)%10 == 0:
                carka_stupnice = carka_delsi
            else:
                carka_stupnice = carka
            stupnice.add(carka_stupnice.copy().shift(-0.1*RIGHT+i/10*UP) )
        stupnice[3].set_color(ORANGE)
        nova_stupnice=stupnice.copy()
        # nova_stupnice[-3].set_color(WHITE)
        # nova_stupnice[6].set_color(WHITE)
        stupnice[-3].set_color(YELLOW).set_stroke(width=7).add_tip(at_start=True, tip_length=0.08)
        stupnice[6].set_color(YELLOW).set_stroke(width=7).add_tip(at_start=True, tip_length=0.08)
        nova_stupnice.flip()
        nova_stupnice.shift(0.35*RIGHT)
        merak.add(
            MathTex("T/^{\circ} \mathrm C").scale(0.5).next_to(stupnice, UP, aligned_edge=RIGHT)
        )

        merak2 = VGroup(
            MathTex(r"\tau").scale(0.5).next_to(nova_stupnice, UP, aligned_edge=LEFT)
        )
        
        teplomer = VDict([("merak",merak),("stupnice",stupnice),("nova_stupnice",nova_stupnice),("merak2",merak2)])
        stupnice.add(Tex(r"$0$").scale(0.5).next_to(stupnice[3],LEFT, buff=0.1).set_color(ORANGE))
        stupnice.add(Tex(r"$T_0$").scale(0.5).next_to(stupnice[-4],LEFT, buff=0.1).set_color(YELLOW))
        stupnice.add(Tex(r"$T_\infty$").scale(0.5).next_to(stupnice[6],LEFT, buff=0.1).set_color(YELLOW))

        teplomer.scale(2)
        teplomer.to_corner(UL)
        nova_stupnice_popisek=VGroup(
            Tex(r"0").scale(1).next_to(nova_stupnice[3],RIGHT, buff=0.1).set_color(ORANGE)
            )

        uloha = VGroup(
            Tex("Základní model v jednotkách SI:"),
            MathTex(r"\frac{\mathrm dT}{\mathrm dt}=-k(T-T_\infty), \quad T(0)=T_0"),
            Tex("V nových jednotkách teploty,"),
            MathTex(r"{{\frac{\mathrm d\tau}{\mathrm dt}=}}{{-k}}{{(\tau-0),}} \quad \tau(0)={{\tau_0}}"),
            Tex(r"V nových jednotkách teploty a času, $\theta=kt$:"),
            MathTex(r"{{\frac{\mathrm d\tau}{\mathrm d\theta}=}}{{-}}{{\tau,}} \quad \tau(0)={{1}}"),
            Tex(r"Trojparametrická úloha je redukována na úlohu bez parametru.")
        ).arrange(DOWN, aligned_edge=LEFT).next_to(teplomer, aligned_edge=UP, buff=2)

        for i in [0,2,4]:
            uloha[i].shift(LEFT)

        self.play(*[Create(i) for i in 
            [teplomer['merak'], teplomer['stupnice'], teplomer['nova_stupnice'], nova_stupnice_popisek]])

        self.play(FadeIn(uloha[0],uloha[1]))
        self.wait()


        # stupnice.add(Tex(r"1").scale(0.5).next_to(nova_stupnice[22],RIGHT, buff=0.1).set_color(ORANGE))
        komentar = Tex(r"Posuneme stupnici. Bude začínat na teplotě okolí.").next_to(teplomer, aligned_edge=DOWN)
        self.play(FadeIn(komentar))
        self.play(VGroup(nova_stupnice,nova_stupnice_popisek).animate().shift(3/10*2*UP))
        self.play(FadeIn(teplomer["merak2"].add_background_rectangle()))
        temp = Tex(r"$\tau_0$").scale(1).next_to(nova_stupnice[21],RIGHT,buff=0.1)
        self.play(FadeIn(temp))
        prevod = Tex(r"$\tau = T - T_\infty$:").next_to(uloha[2],RIGHT)
        self.play(FadeIn(uloha[2],uloha[3],prevod))
        self.wait()
        self.play(Transform(uloha[3][2],MathTex(r"\tau,").next_to(uloha[3][1], aligned_edge=DOWN).shift(0.07*DOWN)))
        self.wait()



        self.remove(komentar)
        komentar = Tex(r"Změníme dílek stupnice. Počáteční teplota bude 1.").next_to(teplomer, aligned_edge=DOWN)
        self.play(FadeIn(komentar))
        self.play(
            FadeOut(temp),
            *[FadeOut(nova_stupnice[i]) for i in range(len(nova_stupnice)) if (i!=3) and (i!= 4)]
            )
        self.play(nova_stupnice[4].animate().move_to(nova_stupnice[21]))
        zacatek = nova_stupnice[3].get_center()[1]
        konec = nova_stupnice[21].get_center()[1]
        print (str(zacatek)+" po "+str(konec))
        delta = (konec-zacatek)/10

        dilky = VGroup()
        for i in [1,2,3,4,5,6,7,8,9,-1,-2]:
            dilky.add(
                Line(start=RIGHT*0, end=RIGHT*0.2).set_stroke(width=2).move_to(
                    nova_stupnice[3], aligned_edge=LEFT).shift(delta*UP*i)
            )
        dilky[4].set_stroke(width=5)    

        self.play(Create(dilky), FadeIn(Tex(r"$1$").scale(1).next_to(nova_stupnice[21],RIGHT,buff=0.1)))
        self.play(Transform(uloha[3][-1],MathTex(r"1").next_to(uloha[3][-2])))
        self.play(Transform(prevod,Tex(r"$\tau = \frac{T - T_\infty}{T_0-T_\infty}$:").next_to(uloha[2],RIGHT)))
        self.wait()


        self.remove(komentar)
        self.play(FadeIn(uloha[4],uloha[5]))
        self.play(FadeIn(uloha[6].scale(0.75).shift(3*LEFT).set_color(RED)))
        self.wait()



class Logisticka(Scene):

    def construct(self):

        # model = VGroup(
        #     #Tex(r"Logistická rovnice s lovem"),
        #     MathTex(r"\displaystyle  { {{\ \mathrm d x \}} \over {{ \mathrm dt }} } = {{r}}\ {{x}}\ \left(1- {{\frac {x}{K}}} \right) - {{h}}")   
        # )
        # model.arrange(DOWN, buff=0.6)
        # self.add(model)
        # rovnice = model[0]
        # rovnice[1].set_color(YELLOW)
        # self.add(index_labels(rovnice).set_color(PURE_RED))        
        # self.wait()

        eq0 = MathTex(r"{{\frac{\mathrm dx}{\mathrm dt} }} {{=}} {{r}} {{x}} {{\left(1-\frac xK\right)}} {{-}} {{h}}")   
        eq1 = MathTex(r"{{\frac 1K\frac{\mathrm dx}{\mathrm dt} }} {{=}} {{r}} {{\frac xK}} {{\left(1-\frac xK\right)}} {{-}} {{\frac hK}}")   
        eq2 = MathTex(r"{{ \frac{1}{rK} \frac{\mathrm dx}{\mathrm dt} }} {{=}} {{}} {{ \frac{x}{K} }} {{\left(1-\frac xK\right)}} {{-}} {{ {h\over rK} }}")   
        eq3 = MathTex(r"{{\frac{\mathrm d \frac xK}{\mathrm d(rt)} }} {{=}} {{}} {{\frac xK}} {{\left(1-\frac xK\right)}} {{-}} {{\frac {h}{rK}}}")   
        eq4 = MathTex(r"{{\frac{\mathrm d X}{\mathrm dT} }} {{=}} {{}} {{X}} {{\left(1-X\right)}} {{-}} {{H}}")   

        eq = VGroup(eq0,eq1,eq2,eq3,eq4).arrange(DOWN).to_edge(LEFT, buff=.5)

        k = VGroup(
            Tex(r"vydělit rovnici parametrem $K$"),
            Tex(r"vydělit rovnici parametrem $r$"),
            Tex(r"začlenit konstanty do derivace"),
            Tex(r"přeznačit proměnné"),
            Tex(r"$X=\frac xK$, $T=rt$, $H=\frac {h}{rK}$"),
        )

        self.add(eq[0])

        for i in range(len(k)-1):
            k[i].next_to(eq[i],RIGHT, buff=0.5)
            self.wait()
            self.play(GrowFromCenter(k[i]))
            self.play(
                *[Transform(j.copy(),jj) for j,jj in zip(eq[i],eq[i+1])]
            )

        self.wait()
        k[-1].next_to(eq[-1],RIGHT, buff=1.5)
        self.play(GrowFromCenter(k[-1]))

        self.wait()


        self.wait()
