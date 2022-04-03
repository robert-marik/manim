from manim import *
import numpy as np
import common_definitions

from manim_editor import PresentationSectionType
template = TexTemplate(preamble=r'\usepackage{url}\usepackage[czech]{babel}\usepackage{amsmath}\usepackage{amssymb}')

class PrubehFunkce(Scene):

    def construct(self):

        self.next_section("Nadpis")
        title = Title(r"Derivace při popisu chování funkce")
        self.play(GrowFromCenter(title))
        domain = np.linspace(0,1,300)
        funkce = [
            [lambda x:0.8*x+0.15, r"Funkce roste stále stejnou rychlostí. Její derivace je konstantní a kladná."],
            [lambda x:0.05*np.sin(6*x)+0.1*x+0.2, r"Funkce roste velmi pomalu. Změna ve vstupních datech má malý vliv na funkční hodnoty. Derivace této funkce je blízká nule."],
            [lambda x:-.51+0.2*np.sin(6*x)+3*x-1, r"Funkce roste velmi rychle. I malá změna ve vstupních datech má velký vliv vliv na funkční hodnoty. Derivace funkce je kladná a numericky velká."],
            [lambda x:(x+0.1)**2+0.02, r"Funkce roste a růst se zrychluje. Derivace takové funkce je kladná a roste."],
            [lambda x:.7-np.exp(-3*x), r"Funkce roste a růst se zpomaluje. Derivace funkce je kladná, ale směrem doprava čím dál menší."]
        ]
        barvy = [RED,BLUE,GREEN,YELLOW,ORANGE]
        funkce = [[*i,j] for i,j in zip(funkce, barvy)]

        def MujTex(text,barva):
            return(Tex(r"\begin{minipage}[t]{6cm}"+text+"\end{minipage}", tex_template=template
            ).set_color(barva).scale(.8).add_background_rectangle(buff=0.5, opacity=.8).next_to(title,DOWN).to_edge(LEFT))
 
        axes = Axes(
            x_range=[0,1,100],
            y_range=[-0.1,1.1,100],
            tips = False
            )

        self.add(axes)
        self.add(Tex(r"$x$").next_to(axes.get_x_axis(),RIGHT))
        self.remove(axes.get_y_axis())
        grafy = VGroup()
        komentar = VGroup()
        predchozi = None
        for f,t,barva in funkce:
            self.remove(komentar)
            soucasny = axes.plot(f,x_range=[0,1,0.01]).set_color(barva)
            if predchozi is None:
                self.play(Create(soucasny))
            else:
                self.play(TransformFromCopy(predchozi, soucasny),FadeToColor(predchozi,GRAY))
            predchozi = soucasny
            grafy.add(soucasny)
            komentar = MujTex(t,barva)
            self.play(FadeIn(komentar))
            self.wait()

        self.remove(komentar)
        popis = VGroup(
            *[Tex(i).scale(.7) for i in
            [r"lineární funkce s konstantní derivací",
            r"pomalu se měnící funkce s numericky malou derivací",
            r"rychle se měnící funkce s numericky velkou derivací",
            r"konvexní funkce s kladnou rostoucí derivací",
            r"konkávní funkce s kladnou klesající derivací"] 
            ]).arrange(DOWN, aligned_edge=LEFT, buff=0.1)
        for i,j in zip(popis,barvy):
            i.set_color(j)
        popis[-1].shift(0.05*DOWN)
        popis.next_to(title,DOWN).to_edge(LEFT)
        self.play(*[FadeToColor(i,j) for i,j in zip(grafy,barvy)])
        self.play(AnimationGroup(*[TransformFromCopy(i,j) for i,j in zip(grafy,popis)],lag_ratio=.4), run_time=5)
        popis.add_background_rectangle()
        self.wait()   