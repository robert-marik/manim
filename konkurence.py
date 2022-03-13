from manim import *
import random

config.max_files_cached = 200

import numpy as np
from common_definitions import *
import os
from scipy.integrate import solve_ivp  # řešení diferenciálních rovnic
import matplotlib.pyplot as plt

np.random.seed(0)
random.seed(0)

MOOSE = os.path.join("icons","moose.png")
DEER = os.path.join("icons","deer.png")

from manim_editor import PresentationSectionType

myaxis_config={'tips':False}

xmax = 5.8
ymax = 3



class Intro(Scene):

    def construct(self):

        self.next_section("Nadpis")

        title = Title(r"Model konkurence dvou živočišných druhů")
        autor = VGroup(Tex("Robert Mařík"),Tex("Mendel University")).arrange(DOWN).next_to(title,DOWN)
        self.play(GrowFromCenter(title))
        self.play(GrowFromCenter(autor[0]))
        self.play(GrowFromCenter(autor[1]))
        self.wait()


class Rovnice(Scene):

    def construct(self):

        self.next_section("Nadpis")

        title = Title(r"Matematický model konkurence")
        self.play(GrowFromCenter(title))

        system = VGroup(
            MathTex(r"{{\frac{\mathrm dx}{\mathrm dt}=r_1 x}}{{\left(1-\frac {x}{K_1}-\alpha y\right)}}").set_color(RED),
            MathTex(r"{{\frac{\mathrm dy}{\mathrm dt}=r_2 y\left(1-\frac {y}{K_2}-\beta x\right)}}").set_color(BLUE),
        ).scale(0.7).arrange(DOWN,aligned_edge=LEFT)
        system.add_background_rectangle(buff=0.4).set_z_index(5)
        system.next_to(title, DOWN)
        self.play(FadeIn(system))

        self.wait()


class PhasePortrait(Scene):
    def construct(self):

        self.next_section("Fazovy portret")        

        axes = Axes(
            x_range=[0,xmax,1e6],
            y_range=[0,ymax,1e6],
            x_length=1.85*xmax,
            y_length=1.85*ymax, 
            **myaxis_config
        )

        Y, X = np.mgrid[0.1:ymax:100j, 0.1:xmax:100j]

        b = ValueTracker(0.1)
        a = ValueTracker(0.2)
        r = ValueTracker(1)
        kx = ValueTracker(4.5)
        ky = ValueTracker(2.5)
    
        def dX_dt(X,t=0):
            """ Return the growth rate of species. """
            return np.array(
                [
                    r.get_value()*X[0]*(1 - 1/kx.get_value()*X[0] - a.get_value()*X[1]),
                    X[1]*(1 - 1/ky.get_value()*X[1] - b.get_value()*X[0])
                ]
                )

        def get_phase_plot():
            streams = VGroup()
            streams.add(
                axes.plot(
                    lambda x: (1 - 1/kx.get_value()*x )/a.get_value(), 
                    x_range=[max(0,(1-a.get_value()*ymax)*kx.get_value()),kx.get_value(),0.01],
                    color=RED,
                    ).set_stroke(width=5)
                )
            streams.add(
                axes.plot(
                    lambda x: (1 - b.get_value()*x )*ky.get_value(), 
                    x_range=[0,min(xmax,1/b.get_value()),0.01],
                    color=BLUE,                    
                    ).set_stroke(width=5)
                )
            phase_portarit_arrows = VGroup()
            delka = .1
            data = []        
            for i in np.linspace(*axes.x_range[:2],25):
                for j in np.linspace(*axes.y_range[:2],25):
                    if i*j == 0:
                        continue
                    start = np.array([i,j])
                    rhs = dX_dt([i,j])
                    norm = np.sqrt(rhs[0]**2+rhs[1]**2)
                    if norm>0.0001:
                        end = start + rhs/norm*delka
                        data += [[start,end,norm]]

            maximum = np.max([i[2] for i in data])
            for i in data:                                
                phase_portarit_arrows.add(
                    Arrow(
                        start=axes.c2p(*i[0],0), 
                        end=axes.c2p(*i[1],0), 
                        buff=0, 
                        max_stroke_width_to_length_ratio = 50, 
                        max_tip_length_to_length_ratio = 0.4,
                        color = temperature_to_color(i[2]*5, min_temp=0, max_temp=maximum),
                        stroke_width=4,
                    )
                )
            streams.add(phase_portarit_arrows)
            streams.add(MathTex(r"K_1").scale(0.6).set_color(RED).next_to(axes.c2p(kx.get_value(),0,0),DOWN))
            streams.add(MathTex(r"1/\alpha").scale(0.6).set_color(RED).next_to(axes.c2p(0,1/a.get_value(),0),LEFT))
            streams.add(MathTex(r"K_2").scale(0.6).set_color(BLUE).next_to(axes.c2p(0,ky.get_value(),0),LEFT))
            streams.add(MathTex(r"1/\beta").scale(0.6).set_color(BLUE).next_to(axes.c2p(1/b.get_value(),0,0),DOWN))
            return(streams)

        def plot_streams():
            U = r.get_value()*X*(1 - 1/kx.get_value()*X - a.get_value()*Y)
            V = Y*(1 - 1/ky.get_value()*Y - b.get_value()*X)
            speed = np.sqrt(U*U + V*V)
            stream_img = plt.streamplot(X, Y, U, V)
            sgm = stream_img.lines.get_segments()
            krivky = []
            lastpoint = sgm[0]
            aktualni_krivka = [lastpoint[1,:]]
            n = 0
            for i in sgm[1:]:
                n = n+1
                #print("Bod "+str(n)+" \n"+str(i))
                if all(i[0,:] == lastpoint[1,:]):
                    aktualni_krivka = aktualni_krivka + [i[0,:],i[1,:]]
                    #print ("            Pridavam k predchozi vetvi, delka je "+str(len(aktualni_krivka)))
                else:
                    krivky = krivky + [aktualni_krivka]
                    aktualni_krivka = [i[0,:],i[1,:]]
                    #print ("Zakladam novou vetev")
                lastpoint = i
            krivky = krivky + aktualni_krivka
            ciste_krivky = [np.array(i) for i in krivky if len(i)>3]
            #streams = VGroup()
            #for t in ciste_krivky:
            #    streams.add(axes.plot_line_graph(t[:,0],t[:,1], add_vertex_dots=False))
            #return(streams)
            return ([
                axes.plot_line_graph(t[:,0],t[:,1], add_vertex_dots=False).set_stroke(width=2).set_z_index(-5) 
                    for t in ciste_krivky
            ])

        axes.to_corner(UR)

        system = VGroup(
            MathTex(r"{{\frac{\mathrm dx}{\mathrm dt}=r_1 x}}{{\left(1-\frac {x}{K_1}-\alpha y\right)}}").set_color(RED),
            MathTex(r"{{\frac{\mathrm dy}{\mathrm dt}=r_2 y\left(1-\frac {y}{K_2}-\beta x\right)}}").set_color(BLUE),
        ).scale(0.7).arrange(DOWN,aligned_edge=LEFT)
        system.add_background_rectangle(buff=0.4).set_z_index(5)
        system.to_corner(UR, buff=0)
        self.add(system)

        pplot = always_redraw(get_phase_plot)    
        self.add(axes)
        self.add(pplot)
        MOOSE_mob = ImageMobject(MOOSE).scale_to_fit_width(2.1).set_color(BLUE).next_to(axes,LEFT,aligned_edge=UP,buff=.8)
        DEER_mob = ImageMobject(DEER).scale_to_fit_width(1.5).set_color(RED).flip(RIGHT).move_to(axes,aligned_edge=DR)
        self.add(MOOSE_mob,DEER_mob)
        self.wait()

        def pridej_krivky(text):
            summary=VGroup()
            summary = Tex(r"\begin{minipage}{10cm} \rightskip 0 pt plus 1 fill \footnotesize "+text+"\end{minipage}")
            summary.scale(0.95).add_background_rectangle().to_corner(DL)
            self.play(FadeIn(summary))
            krivky = plot_streams()#.shuffle_submobjects()
            self.play(*[Create(i) for i in krivky],run_time=5)
            self.wait()
            self.next_section("")        
            self.play(*[FadeOut(i) for i in krivky],FadeOut(summary))
            self.wait()
        def pridej_komentar(text):
            summary=VGroup()
            summary = Tex(r"\begin{minipage}{10cm} \rightskip 0 pt plus 1 fill \footnotesize "+text+"\end{minipage}")
            summary.scale(0.95).add_background_rectangle().to_corner(DL)
            return(summary)

        self.next_section("Trajektorie, slaba konkurence")        
        pridej_krivky(r"Slabá konkurence. Obě populace koexistují, stacionární bod je stabilní.")

        self.next_section("Navyseni parametru alpha")        
        kom = pridej_komentar(r"Navýšení parametru $\alpha$. Přítomnost losa silněji ovlivňuje populaci jelena.")
        self.play(FadeIn(kom))
        self.play(a.animate.set_value(.5), run_time=5, rate_func=linear)
        self.wait()

        self.next_section("Trajektorie, dominance losa")        
        self.remove(kom)
        pridej_krivky(r"Po dostatečném navýšení parametru $\alpha$ dojde k dominanci populace losa. Populace jelenů vyhyne.")

        self.next_section("Navyseni parametru beta")        
        kom = pridej_komentar(r"Navýšení parametru $\beta$. Přítomnost jelena silněji ovlivňuje populaci losa.")
        self.play(FadeIn(kom))
        self.play(b.animate.set_value(.3), run_time=5, rate_func=linear)
        self.wait()

        self.next_section("Trajektorie, silna konkurence")        
        self.remove(kom)
        pridej_krivky("Silná konkurence a vysoké oba mezidruhové parametry. Přežije jenom jeden druh. Který? To závisí na počátečních podmínkách.")

        self.next_section("Snizeni nosne kapacity pro losa")        
        kom = pridej_komentar(r"Snížení nosné kapacity populace losa, tj. parametru $K_2$.")
        self.play(FadeIn(kom))
        self.play(ky.animate.set_value(1.7), run_time=5, rate_func=linear)

        self.next_section("Trajektorie, dominance jelena")        
        self.remove(kom)
        pridej_krivky("I změna nosné kapacity prostředí mění fázový portrét. Zde modelujeme snížení nosné kapacity pro populaci losa. Skromnější druh dominuje. ")
