from manim import *

import numpy as np
import matplotlib.pyplot as plt

from common_definitions import temperature_to_color

class Ohyb(MovingCameraScene):
    def construct(self):

        def transform_(X,R=5):
            x,y = X
            return np.array([(R-y)*np.sin(x/R), R-(R-y)*np.cos(x/R)])

        def transform(X,R=5):
            return transform_(X,R=R)-np.array([0, transform_([xmax,ymin],R=R)[1]])
            
        xmin,xmax = -1,1
        ymin,ymax = -0.1,0.1

        x = np.linspace(xmin,xmax,200)
        x_rezy = np.linspace(xmin,xmax,11)
        y_vrstvy = np.linspace(ymin,ymax,31)
        y_deleni = np.linspace(ymin,ymax,8)
                
        R = 5
        cary = np.array([[ [i,j] for i in x] for j in y_vrstvy])
        cary_odelovace = np.array([[ [i,j] for i in x] for j in y_deleni[1:-1]])
        osa = np.array([ [i,(ymax+ymin)/2] for i in x ])
        pricky = np.array([[ [i,j] for j in y_vrstvy] for i in x_rezy])

        axes = Axes(x_range=(-1,1,10),y_range=(-1,1,20),x_length=6,y_length=6)
        axes.shift(3*UP+3*LEFT)

        #self.add(NumberPlane())
        def draw_beam(R=R, axes=axes, kreslit_vrstvy=False, oddelovace=False):        
            cary_t = np.array([ 
                [transform(X, R=R) for X in cara] for cara in cary
                ])  

            osa_t =  np.array(
                [transform(X, R=R) for X in osa]
                )                

            pricky_t = np.array([ 
                [transform(X, R=R) for X in pricka] for pricka in pricky
                ])                 

            output = VGroup()
            output.cara = VGroup()
            output.pricky = VGroup()
            output.outline = VGroup()
            output.support = VGroup()
            output.support.add(Triangle(fill_color=BLUE, fill_opacity=1).scale(.1).next_to(axes.c2p(xmax,0,0), DOWN, buff=0.1))
            output.support.add(Triangle(fill_color=BLUE, fill_opacity=1).scale(.1).next_to(axes.c2p(xmin,0,0), DOWN, buff=0.1))

            if not kreslit_vrstvy:
                cary_t_ = [cary_t[0],cary_t[-1]]                
            else:
                cary_t_ = cary_t

            for i,cara in enumerate(cary_t_):
                if i<len(y_vrstvy)/2:
                    barva = RED
                else:
                    barva = BLUE
                barva = temperature_to_color(i,min_temp=0,max_temp=len(y_vrstvy),colors=["#ff0000",WHITE,"#0000ff"])
                output.cara.add(axes.plot_line_graph(cara[:,0],cara[:,1], add_vertex_dots=False).set_stroke(width=2).set_color(barva))

            for pricka in pricky_t:
                output.pricky.add(axes.plot_line_graph(pricka[:,0],pricka[:,1],add_vertex_dots=False))
            
            output.oddelovace = VGroup()
            if oddelovace:
                oddelovace_t = np.array([ 
                    [transform(X, R=R) for X in cara] for cara in cary_odelovace
                    ])               
                for cara in oddelovace_t:   
                    output.oddelovace.add(
                        axes.plot_line_graph(cara[:,0],cara[:,1], add_vertex_dots=False).set_stroke(width=1).set_color(BLACK)
                    )

            output.outline.add(
                output.cara[0],
                output.cara[-1],
                output.pricky[0],
                output.pricky[-1],
            ).set_color(WHITE).set_stroke(width=2)
            output.add(output.pricky,output.cara,output.outline,output.support,output.oddelovace)
            return(output)

        beam=VGroup()
        beam.outline = VGroup()
        beam.pricky = VGroup()
        
        Rs = [100,80,50,30,20,10,9,8,7,6,5,4.5,4,3.5,3]
        #Rs = [3]
        beam = draw_beam(R=500)
        self.camera.frame.save_state()
        self.camera.frame.scale(0.55).move_to(beam).shift(DOWN)
        self.wait()           
        self.play(FadeIn(beam.outline, beam.support))

        for R in Rs:
            self.remove(beam, beam.outline)
            beam = draw_beam(R=R)
            self.add(beam.outline, beam.support)
            self.wait(.2)
        self.wait()

        self.play(FadeOut(beam.outline))
        beam = draw_beam(R=500)
        self.play(FadeIn(beam.outline, beam.pricky))

        for R in Rs:
            self.remove(beam, beam.outline, beam.pricky)
            beam = draw_beam(R=R)
            self.add(beam.outline, beam.pricky)
            self.wait(.2)
        self.wait()

        for R in [Rs[-1]]:
            #self.remove(beam, beam.outline, beam.pricky)
            beam = draw_beam(R=R, kreslit_vrstvy=True, oddelovace=True)
            self.play(FadeIn(beam))
            self.wait(.2)
        self.wait()

        osa_y = Line(
            start = axes.c2p(*transform([xmax,0],R=R),0), 
            end = axes.c2p(*transform([xmax,2*ymax],R=R),0)
        ).add_tip(tip_length=0.1).shift(0.1*RIGHT)
        osa_y.set_color(PURPLE)
        osa_y.add(MathTex("y").scale(.6).next_to(osa_y, UP,aligned_edge=RIGHT, buff=0.05))

        osa_x = Line(
            start = axes.c2p(*transform([xmax,0],R=R),0), 
            end = axes.c2p(*transform([xmax+2*ymax,0],R=R),0)
        ).add_tip(tip_length=0.1).shift(0.1*RIGHT)
        osa_x.set_color(PURPLE)
        osa_x.add(MathTex("x").scale(.6).next_to(osa_x,buff=0.05))
        #osa_y.add_tip(tip_length=0.2)
        self.add(osa_y, osa_x)
        self.wait()


        text = VGroup(
            MathTex(r"\varepsilon_i = -\frac{\theta}{l}y_i"),
            MathTex(r"F_i = S_i \sigma_i = S_i E \varepsilon_i = -S_i E\frac{\theta}{l}y_i"),
            MathTex(r"0=\sum F_i = -E\frac{\theta}{l} \sum y_i S_i"),
            MathTex(r"M = \sum y_i F_i = -E\frac{\theta}{l}\sum y^2_i S_i"),
            MathTex(r"0 = -E\frac{\theta}{l}\iint y \,\mathrm dS"),
            MathTex(r"M = -E\frac{\theta}{l}\iint y^2 \,\mathrm dS"),
        ).scale(0.75).arrange(DOWN)
        text.next_to(beam,DOWN)

        self.play(FadeIn(text[0]))
        self.play(FadeIn(text[1]))
        self.wait()

        
        self.play(Restore(self.camera.frame))

        self.play(FadeIn(text[2]))
        self.play(FadeIn(text[3]))
        self.wait()

        self.play(FadeIn(text[4]))
        self.play(FadeIn(text[5]))
        self.wait()


        text2 = VGroup(
            MathTex(r"I:=\iint y^2\,\mathrm dS"),
            MathTex(r"M=-\frac{\theta}{l}EI"),
        ).scale(0.75).arrange(DOWN, aligned_edge=LEFT)

        text3 = VGroup(
            MathTex(r"\frac{\theta}{l}=-\frac{M}{EI} \text{ (pro konstantní $M$ podél nosníku)}"),
            MathTex(r"\frac{\Delta\theta}{\Delta x}=-\frac{M}{EI} \text{ (pro úsek nosníku s konstantním $M$)}"),
            MathTex(r"\frac{\mathrm d\theta}{\mathrm dx}=-\frac{M(x)}{EI}\text{ (pro nekonečně malý kousek nosníku a libovolné $M$)}"),
            MathTex(r"\frac{\mathrm d^2u}{\mathrm dx^2}=-\frac{M(x)}{EI}\text{ (jako výše, ale pomocí výchylky místo úhlu natočení)}")
        ).scale(0.75).arrange(DOWN, aligned_edge=LEFT)

        text3.next_to(beam, DOWN, buff=1).shift(2*RIGHT)
        text2.next_to(beam, buff=2)

        self.play(FadeIn(text2))
        self.wait()

        self.play(FadeOut(text))
        for i in text3:
            self.play(FadeIn(i))
            self.wait()