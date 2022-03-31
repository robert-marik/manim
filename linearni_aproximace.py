from manim import *
import numpy as np
import common_definitions

from manim_editor import PresentationSectionType
template = TexTemplate(preamble=r'\usepackage{url}\usepackage[czech]{babel}\usepackage{amsmath}\usepackage{amssymb}')

class Obrazek(MovingCameraScene):

    def construct(self):

        self.next_section("Nadpis")
        title = Title(r"Lineární aproximace")
        self.play(GrowFromCenter(title))

        ax = Axes(x_range=(-0.75,0.75,.1),y_range=(-0.6,0.6), tips=False)
        label = MathTex("0.1").scale(0.5).next_to(ax.c2p(0.1,-0.07,0),DOWN) 
        ax.next_to(title,DOWN)

        predpis = VGroup(
            MathTex(r"f(x)=\frac 1{\sqrt{1-x}}-1"),
            MathTex(r"f(x)\approx \frac 12 x,\quad (\text{pokud }|x|\ll 1)    "),
        ).arrange(DOWN, aligned_edge=LEFT).next_to(title, DOWN).to_edge(LEFT, buff=0.5)
        predpis[0].set_color(BLUE)
        predpis[1].set_color(RED)
        #predpis.next_to(ax.c2p(0,0,0),LEFT, buff=0)        
        predpis.set_z_index(10)
        #predpis.add_background_rectangle() 


        postup = VGroup(
            MathTex(r"E_k=\frac{mc^2}{\sqrt{\displaystyle 1-\frac{v^2}{c^2}}} - mc^2"),
            MathTex(r"E_k=mc^2\left(\frac{1}{\sqrt{\displaystyle 1-\frac{v^2}{c^2}}} - 1\right)"),
            MathTex(r"E_k=mc^2 f\left(\frac{v^2}{c^2}\right), \quad f(x)=\frac {1}{\sqrt{1-x}}-1"),
            MathTex(r"E_k=mc^2 f\left(\frac{v^2}{c^2}\right), \quad f(x)\approx\frac {1}{2}x, \quad |x|\ll 1"),
            MathTex(r"E_k\approx mc^2 \frac 12 \frac{v^2}{c^2}, \quad \text{pro }v\ll c"),
            MathTex(r"E_k\approx \frac 12 mv^2, \quad \text{pro }v\ll c")
        ).scale(0.7).arrange(DOWN).next_to(ax, buff=1)

        graf1 = ax.plot(lambda x: 1/np.sqrt(1-x)-1,  x_range=[-0.75, .6],).set_color(BLUE)
        graf1.set_stroke(width=8)
        graf2 = ax.plot(lambda x: 1/2*x).set_color(RED)

        self.play(FadeIn(predpis[0]))
        self.play(FadeIn(ax,label),FadeIn(graf1))
        self.wait()
        self.next_section("")

        self.camera.frame.save_state()

        self.play(self.camera.frame.animate.scale(0.6).move_to(postup[0]).shift(UP))
        for i in range(3):
            if i==0:
                zdroj=VGroup()
            else:
                zdroj=postup[i-1].copy() 
            self.play(
                TransformMatchingShapes(zdroj,postup[i]),
                self.camera.frame.animate.move_to(postup[i]).shift(UP),
                Circumscribe(postup[i])
                )
            self.play(
                Circumscribe(postup[i])
                )
            self.wait()
            self.next_section("")
 
        t0 = MobjectTable([
            [Tex(r"Auto na dálnici"),MathTex(r"1.5\times 10^{-14}")],
            [Tex(r"Šhinkansen"),MathTex(r"8.8\times 10^{-14}")],
            [Tex(r"NASA X43"),MathTex(r"9.0\times 10^{-11}")],
            [Tex(r"Sonda Pioneer 10"),MathTex(r"2.3\times 10^{-9}")],
            ], 
            col_labels=[VGroup(), MathTex(r"v^2/c^2")],
            include_outer_lines=True,
            line_config={'color':BLACK, 'stroke_width':0.1},
        ).scale(.7).to_edge(UP)
        nadpis = Tex(r"Jak je velký podíl $v^2/c^2$?")
        t = VGroup(nadpis,t0).arrange(DOWN, buff=1).next_to(postup, buff=1)

        self.add(t)
        self.play(
            self.camera.frame.animate.scale(2).move_to(t),
        )
        self.wait()
        self.next_section("")

        zavorka = DoubleArrow(start=ax.c2p(0,-0.01,0), end=ax.c2p(0.01,-0.01,0),buff=0,  max_stroke_width_to_length_ratio=30, max_tip_length_to_length_ratio=0.2)
        zavorka.set_color(PURPLE).set_stroke(width=2)

        self.play(self.camera.frame.animate.scale(0.1).move_to(ax.c2p(0,0,0)))
        self.play(FadeIn(zavorka))
        self.play(Wiggle(zavorka))
        self.wait()
        self.next_section("")

        self.play(FadeIn(graf2))
        self.wait()
        self.next_section("")

        self.play(Restore(self.camera.frame))
        self.remove(predpis[0])
        self.add(predpis[0])
        self.play(FadeIn(predpis[1]))
        self.wait()
        self.next_section("")

        self.play(self.camera.frame.animate.scale(0.5).move_to(postup[3]).shift(UP))
        for ii in range(3):
            i = ii+3
            self.play(
                TransformMatchingShapes(postup[i-1].copy(),postup[i]),
                self.camera.frame.animate.move_to(postup[i]).shift(UP),
                Circumscribe(postup[i])
                )
            self.play(
                Circumscribe(postup[i])
                )
            self.wait()
            self.next_section("")

        self.play(Restore(self.camera.frame))
        self.wait()   
        self.next_section("")

        all = Group(*[i for i in self.mobjects])
        self.play(self.camera.frame.animate.scale(2).move_to(all))
        #self.wait()
        #self.next_section("")

        vysledek = VGroup(
            MathTex(r"f(x)\approx f'(0)x"),
            MathTex(r"f(x)\approx f(0) + f'(0)x"),
            MathTex(r"f(x)\approx f(x_0) + f'(x_0)(x-x_0)"),
            MathTex(r"f(x_0+h)\approx f(x_0) + f'(x_0)h"),
            MathTex(r"f(x+h)\approx f(x) + f'(x)h")
        ).scale(2).shift(UP*4.5+RIGHT*6).set_color(YELLOW) 

        self.play(FadeIn(vysledek[0]))
        self.wait()
        self.next_section("")

        for i in range(1,len(vysledek)):
            if i==3:
                self.play(vysledek[i-1].copy().animate.shift(1.4*UP))
            self.play(TransformMatchingShapes(vysledek[i-1],vysledek[i]))
            self.wait()
            self.next_section("")

