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

        ax = Axes(x_range=(-0.8,0.8),y_range=(-0.6,0.6), tips=False)
        ax.next_to(title,DOWN)

        predpis = VGroup(
            MathTex(r"f(x)=\frac 1{\sqrt{1-x}}-1"),
            MathTex(r"f(x)\approx \frac 12 x"),
        ).arrange(DOWN, aligned_edge=LEFT).next_to(title, DOWN).to_edge(LEFT, buff=0.5)
        predpis[0].set_color(BLUE)
        predpis[1].set_color(RED)
        #predpis.next_to(ax.c2p(0,0,0),LEFT, buff=0)        
        predpis.set_z_index(10)
        predpis.add_background_rectangle() 
        self.add(predpis)        
          
        graf1 = ax.plot(lambda x: 1/np.sqrt(1-x)-1).set_color(BLUE)
        graf1.set_stroke(width=8)
        graf2 = ax.plot(lambda x: 1/2*x).set_color(RED)
        self.add(ax,graf1,graf2)
        zavorka = Line(start=ax.c2p(0,-0.01,0), end=ax.c2p(0.01,-0.01,0))
        zavorka.set_color(YELLOW)
        self.add(zavorka)
        self.wait()

        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.scale(0.05).move_to(ax.c2p(0,0,0)))
        self.remove(predpis)
        self.add(predpis)
        self.wait()

        self.play(Restore(self.camera.frame))
        self.wait()   

class Ek(MovingCameraScene):
    def construct(self):
        postup = VGroup(
            MathTex(r"E_k=\frac{mc^2}{\sqrt{\displaystyle 1-\frac{v^2}{c^2}}} - mc^2"),
            MathTex(r"E_k=mc^2\left(\frac{1}{\sqrt{\displaystyle 1-\frac{v^2}{c^2}}} - 1\right)"),
            MathTex(r"E_k=mc^2 f\left(\frac{v^2}{c^2}\right), \quad f(x)=\frac {1}{\sqrt{1-x}}-1"),
            MathTex(r"E_k=mc^2 f\left(\frac{v^2}{c^2}\right), \quad f(x)\approx\frac {1}{2}x"),
            MathTex(r"E_k\approx mc^2 \frac 12 \frac{v^2}{c^2}"),
            MathTex(r"E_k\approx \frac 12 mv^2")
        ).scale(0.5).arrange(DOWN)

        self.camera.frame.save_state()
        self.add(postup)
        for i in range(len(postup)):
            if i==0:
                zvetseni=0.4
            else:
                zvetseni=1
            self.play(
                self.camera.frame.animate.scale(zvetseni).move_to(postup[i]),
                Circumscribe(postup[i])
                )
            self.play(
                Circumscribe(postup[i])
                )
            self.wait()

        self.wait()

