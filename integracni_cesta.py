from tkinter import LEFT
from manim import *
import numpy as np
import common_definitions

from manim_editor import PresentationSectionType
from common_definitions import *

template = TexTemplate(preamble=r'\usepackage{url}\usepackage[czech]{babel}\usepackage{amsmath}\usepackage{amssymb}')

myaxis_config={'tips':False}

class Intro(Scene):

    def construct(self):
        title = Title("(Ne-)závislost na integrační cestě")
        self.play(GrowFromCenter(title))
        self.wait()

        popis = VGroup(
            MathTex(r"F_1(x,y)=\frac{-y\vec \imath+x\vec \jmath}{\sqrt{x^2+y^2}}"),
            MathTex(r"F_2(x,y)=\frac{-y\vec \imath+x\vec \jmath}{x^2+y^2}"),
            Tex(r"""
            \begin{minipage}{10cm}
            Obě vektorová pole obíhají počátek proti směru hodinových ručiček.
            První vektorové pole má všechny vektory jednotkové délky. Druhé vektorové pole 
            je gradientem skalární funkce $\varphi(x,y)=\arctan\frac yx.$ V každém poli budeme 
            integrovat po třech křivkách, které začínají a končí všechny
            ve stejném bodě.
            \end{minipage}
            """)
        ).scale(.8).arrange(DOWN, aligned_edge=LEFT)
        popis.next_to(title,DOWN)
        self.add(popis)
        self.wait()

class Obrazek(Scene):

    def construct(self):

        xmax = 1.1
        ymax = 1.1
        axes = Axes(
            x_range=[-0.1,xmax,1e6],
            y_range=[-0.1,ymax,1e6],
            x_length=4*xmax,
            y_length=4*ymax, 
            **myaxis_config
        )
        axes.to_edge(RIGHT)

        Y, X = np.mgrid[0:ymax:400j, 0:xmax:400j]
   
        def F1(X):
            x,y = X
            return np.array([-y,x])/np.sqrt(x**2+y**2)
        def F2(X):
            x,y = X
            return np.array([-y,x])/(x**2+y**2)

        def get_vfield(F,axes=axes, small_arrows=False):
            phase_portarit_arrows = VGroup()
            delka = .04
            data = []        
            for i in np.linspace(*axes.x_range[:2],25):
                for j in np.linspace(*axes.y_range[:2],25):
                    #if i*j == 0:
                    #    continue
                    start = np.array([i,j])
                    rhs = F([i,j])
                    norm = np.sqrt(rhs[0]**2+rhs[1]**2)
                    if norm>0.0001:
                        end = start + rhs/norm*delka
                        if all(F(start)*F(end)>=0):
                            data += [[start,end,norm]]

            maximum = np.max([i[2] for i in data])
            for i in data:             
                sw = 2
                if small_arrows:
                    sw = 2                   
                phase_portarit_arrows.add(
                    Line(
                        start=axes.c2p(*i[0],0), 
                        end=axes.c2p(*i[1],0), 
                        buff=0, 
                        stroke_width=sw,
                    ).add_tip(
                        tip_length=0.05).set_color(
                            temperature_to_color(i[2]*5, min_temp=0, max_temp=maximum))
                )
            return(phase_portarit_arrows)    

        for curF,TexF in zip(
            [F1,F2],
            [r"$$\frac{-y\vec \imath+x\vec \jmath}{\sqrt{x^2+y^2}}$$",r"$$\frac{-y\vec \imath+x\vec \jmath}{x^2+y^2}$$"]
            ):

            t = np.linspace(0,1,150)
            k1fun = lambda t: np.array([1-t,t])
            k2fun = lambda t: np.array([np.cos(np.pi/2*t),np.sin(np.pi/2*t)])
            k3fun = lambda t: np.array([1-t,t**3])
            k3fun = lambda t: np.array([1-np.cos(np.pi/2*(1-t)),1-np.sin(np.pi/2*(1-t))])

            r = [np.array(k1fun(t)), np.array(k2fun(t)), np.array(k3fun(t))]
            dr = [np.gradient(i, axis=1) for i in r]
            Fr = [np.array([curF(X) for X in r_.T ]) for r_ in r]
            I = [ np.multiply(x1.T, x2) for x1,x2 in zip(dr,Fr) ]
            Int = [ [ i+j for i,j in I_] for I_ in I]
            Out = [ np.trapz(y) for y in Int]        

            self.remove(*[i for i in self.mobjects])

            self.add(axes)
            self.add(get_vfield(F=curF))

            axes2 = Axes(
                x_range=[0,1,1],
                y_range=[np.min(Int),np.max(Int),1e6],
                x_length=6*xmax,
                y_length=4*ymax, 
                tips = None
            )
            axes2.to_edge(LEFT)
            self.add(axes2)

            self.add(Tex(TexF).next_to(axes,UP))
            self.add(Tex(r"$\vec F(\vec r(t))\frac{\mathrm d\vec r}{\mathrm dt}$").next_to(axes2,UP))

            poloha = ValueTracker(1)

            c = [RED,BLUE,YELLOW]

            sol = always_redraw(lambda: 
                VGroup(*[axes.plot_line_graph(
                    r[i][0][:int(poloha.get_value())],
                    r[i][1][:int(poloha.get_value())],
                    add_vertex_dots=False).set_color(c[i]) for i in range(3)]))
            self.add(sol)

            cur = always_redraw(lambda: 
                VGroup(*[axes2.plot_line_graph(
                    t[:int(poloha.get_value())],
                    Int[i][:int(poloha.get_value())],
                    add_vertex_dots=False).set_color(c[i]) for i in range(3)]))
            self.add(cur)

            self.wait()

            self.next_section("")        
            self.play(poloha.animate.set_value(len(t)/3))
            self.wait()

            self.next_section("")        
            self.play(poloha.animate.set_value(len(t)/2))
            self.wait()

            self.next_section("")        
            self.play(poloha.animate.set_value(len(t)))
            self.play(FadeIn(
                VGroup(*[MathTex(i.round(5)).set_color(j) for i,j in zip(Out,c)]).arrange(RIGHT,buff=1).next_to(VGroup(axes,axes2),DOWN)
            ))
            self.wait() 
            self.next_section("")        

    

