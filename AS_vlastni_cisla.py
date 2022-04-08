from tkinter import LEFT, TOP
from manim import *

from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import fsolve
from scipy.interpolate import interp1d



xmax = 1
ymax = 1
myaxis_config={'tips':False}
   

class PhasePortrait(MovingCameraScene):
    def construct(self):

        self.next_section("Fazovy portret")        

        axes = Axes(
            x_range=[-xmax,xmax,1e6],
            y_range=[-ymax,ymax,1e6],
            x_length=7*xmax,
            y_length=7*ymax, 
            **myaxis_config
        )
        axes.set_z_index(-2)
        axes2 = Axes(
            x_range=[-1.5,1.5,1e6],
            y_range=[-1.5,1.5,1e6],
            x_length=1.5,
            y_length=1.5, 
            **myaxis_config
        )
        Y, X = np.mgrid[-ymax:ymax:400j, -xmax:xmax:400j]
   
        # trace = ValueTracker(0.5)
        # determinant = ValueTracker(0.05)
        lambda1 = ValueTracker(1.2)
        lambda2 = ValueTracker(0.7)
        lambdaIm = ValueTracker(0)
        zkoseni = ValueTracker(.1)
        otoceni = ValueTracker(-20)

        def get_characteristics():
            l1,l2,zk,ot,lI = [i.get_value() for i in [lambda1,lambda2,zkoseni,otoceni,lambdaIm]]
            if lI!=0:
                reals = False
                vecs = None
                t = l1*2
                d = l1**2+lI**2
                pom = np.sqrt(d - t**2/4)
                A = np.matrix([[t/2,pom],[-pom,t/2]])
                vals, vecs = np.linalg.eig(A)
            else:    
                # l1 = (-t + np.sqrt(t**2-4*d) )/2
                # l2 = (-t - np.sqrt(t**2-4*d) )/2
                Aori = np.array([[l1,zk],[0,l2]])
                uhel = ot*DEGREES
                R = np.array([[np.cos(uhel),-np.sin(uhel)],[np.sin(uhel),np.cos(uhel)]])
                A = np.matmul(R.T,Aori)
                A = np.matmul(A,R)
                vals, vecs = np.linalg.eig(A)
                reals=True
            return [A, vecs, vals, reals]

        def F(X):
            x,y = X
            A = get_characteristics()[0]
            return np.array([A[0,0]*x+A[0,1]*y,A[1,0]*x+A[1,1]*y])


        def get_phase_plot(F=F,axes=axes, axes2 = axes2, small_arrows=False, deleni = 10):
            """
            In axes draws vector field defined by the function F. In axes2
            """
            phase_portrait_arrows = VGroup()

            delka = .07
            data = []        
            for i in np.linspace(*axes.x_range[:2],deleni):
                for j in np.linspace(*axes.y_range[:2],deleni):
                    start = np.array([i,j])
                    rhs = F([i,j])
                    norm = np.sqrt(rhs[0]**2+rhs[1]**2)
                    if norm>0.0000001:
                        end = start + rhs/norm*delka
                        data += [[start,end,norm]]

            maximum = np.max([i[2] for i in data])
            for i in data:             
                sw = 4
                phase_portrait_arrows.add(
                    Line(
                        start=axes.c2p(*i[0],0), 
                        end=axes.c2p(*i[1],0), 
                        buff=0, 
                        stroke_width=sw,
                    ).add_tip(tip_length=0.1)
                )
            matice,A,vals,isreal = get_characteristics()
            if not isreal:
                reseni = VGroup(
                    MathTex(r'X(t)=e^{'+'{:.2f}'.format(vals[0].real)+r't}\varphi(t)'),
                    Tex(r'$\varphi(t)$ osciluje s úhlovou frekvencí $'+'{:.2f}'.format(vals[0].imag)+r'$')
                    ).scale(0.75).arrange(DOWN, aligned_edge=LEFT)
                reseni.scale_to_fit_width(6)                
                reseni.next_to(system, DOWN, aligned_edge=LEFT, buff=0.25)
                reseni.add_background_rectangle()
                hodnoty = VGroup(
                    MathTex(r"\lambda_{1} = "+'{:.2f} {:+.2f}i'.format(np.round(vals[0].real,2), vals[0].imag)).set_color(c[0]),
                    MathTex(r"\lambda_{2} = "+'{:.2f} {:+.2f}i'.format(np.round(vals[1].real,2), vals[1].imag)).set_color(c[1])
                ).arrange(DOWN).to_edge(UL).shift(2*DOWN)
                phase_portrait_arrows.add(hodnoty)
                phase_portrait_arrows.add(Dot(axes2.c2p(np.real(vals[0]),np.imag(vals[0]),0)).set_color(c[0]))
                phase_portrait_arrows.add(Dot(axes2.c2p(np.real(vals[1]),np.imag(vals[1]),0)).set_color(c[1]))
                phase_portrait_arrows.add(reseni)
            else:
                if np.abs(vals[0]-vals[1])>0.0001:
                    for v,col in zip([[A[0,0],A[1,0]],[A[0,1],A[1,1]]],c):
                        v_ = np.array(v)
                        start = v_/np.sqrt(v[0]**2+v[1]**2)
                        end = -start
                        phase_portrait_arrows.add(Line(start = axes.c2p(*start,0), end = axes.c2p(*end,0)).set_color(col))
                    reseni = MathTex(r'X(t)={{C_1 \vec u_1 e^{'+'{:.2f}'.format(vals[0])+r't}}}+{{C_2 \vec u_2 e^{'+'{:.2f}'.format(vals[1])+r't}}}').scale(0.75)
                    reseni[1].set_color(c[0])
                    reseni[3].set_color(c[1])
                    reseni.scale_to_fit_width(5.5)                
                    reseni.next_to(system, DOWN, aligned_edge=LEFT, buff=0.25)
                    reseni.add_background_rectangle()
                else:
                    reseni=VGroup().next_to(system,DOWN)
                hodnoty = VGroup(
                    MathTex(r"\lambda_1 = "+'{:.2f}'.format(np.round(vals[0],2))).set_color(c[0]),
                    MathTex(r"\lambda_2 = "+'{:.2f}'.format(np.round(vals[1],2))).set_color(c[1])
                ).arrange(DOWN, aligned_edge = LEFT).to_edge(UL).shift(2*DOWN)
                phase_portrait_arrows.add(hodnoty)
                phase_portrait_arrows.add(Dot(axes2.c2p(vals[0],0,0)).set_color(c[0]))
                phase_portrait_arrows.add(Dot(axes2.c2p(vals[1],0,0)).set_color(c[1]))
                phase_portrait_arrows.add(reseni)

            return(phase_portrait_arrows)

        c = [BLUE,YELLOW]

        def plot_streams(F=F, axes=axes, minlength=None, maxlength=None):
            U,V = F([X,Y])
            
            speed = np.sqrt(U*U + V*V)
            #return VGroup()
            if minlength is None:
                stream_img = plt.streamplot(X, Y, U, V, density = 1)
            else:
                stream_img = plt.streamplot(X, Y, U, V, minlength=minlength, maxlength=maxlength)
            sgm = stream_img.lines.get_segments()
            krivky = []
            lastpoint = sgm[0]
            aktualni_krivka = [lastpoint[1,:]]
            n = 0
            for i in sgm[1:]:
                n = n+1
                if all(i[0,:] == lastpoint[1,:]):
                    aktualni_krivka = aktualni_krivka + [i[0,:],i[1,:]]
                else:
                    krivky = krivky + [aktualni_krivka]
                    aktualni_krivka = [i[0,:],i[1,:]]
                lastpoint = i
            krivky = krivky + [aktualni_krivka]
            ciste_krivky = [np.array(i) for i in krivky if len(i)>2]
            return (VGroup(*[
                axes.plot_line_graph(t[:,0],t[:,1], add_vertex_dots=False).set_stroke(width=2).set_z_index(-5) 
                    for t in ciste_krivky
            ]))

        def odstranit(co):
            self.remove(co)

        def typ(text):
            out = Tex(text).set_color(YELLOW).add_background_rectangle(buff=0.25).move_to(axes, aligned_edge=UP)
            return out

        def podgraf(tmin=-1,tmax=1,ymin=-0.1,ymax=1,popisek=r"e^{\lambda_i t}",x_values=None,y_values=None,posun=0*DOWN):
            l1 = lambda1.get_value()
            l2 = lambda2.get_value()
            axes3 = Axes(
                x_range=[tmin,tmax,1e6],
                y_range=[ymin,ymax,1e6],
                x_length=3,
                y_length=1.5, 
                **myaxis_config
            ).to_edge(LEFT).shift(DOWN)
            if x_values is None:
                t = np.linspace(tmin,tmax,500)
                y1 = np.exp(l1*t)
                y2 = np.exp(l2*t)
                factor = max(max(y1),max(y2))
                g1 = axes3.plot_line_graph(x_values=t,y_values=y1/factor, add_vertex_dots=False, line_color=c[0])
                g2 = axes3.plot_line_graph(x_values=t,y_values=y2/factor, add_vertex_dots=False, line_color=c[1])
            else:
                g1 = axes3.plot_line_graph(x_values=x_values,y_values=y_values, add_vertex_dots=False, line_color=c[0])
                g2 = VGroup()
            popisekG = VGroup()
            popisekG.add(MathTex("t").scale(0.5).move_to(axes3.get_x_axis(),DR).shift(0.05*UP))
            popisekG.add(MathTex(popisek).scale(0.5).move_to(axes3.get_y_axis(),UL).shift(0.05*RIGHT))
            output = VGroup(axes3,g1,g2,popisekG).shift(posun)
            return output

        system = MathTex(r"X'=AX").to_corner(UL)
        self.add(system)

        axes.to_corner(UR)
        axes2.move_to((-2,0.5,0))
        axes2.add(Tex(r"$\Re(\lambda)$").scale(0.5).next_to(axes2.get_x_axis(),buff=0))
        axes2.add(Tex(r"$\Im(\lambda)$").scale(0.5).next_to(axes2.get_y_axis(),UP,buff=0))
        pplot = always_redraw(lambda : get_phase_plot())
        self.add(pplot,axes2)



        krivky = plot_streams(F=F, axes=axes).set_color(ORANGE)
        krivky.add(typ(r"Nestabilní uzel"))
        krivky.add(podgraf())
        self.add(krivky)
        self.wait()

        self.next_section()
        odstranit(krivky)
        self.play(lambda1.animate.set_value(0.4))
        krivky = plot_streams(F=F, axes=axes).set_color(ORANGE)
        krivky.add(typ(r"Nestabilní uzel"))
        krivky.add(podgraf(tmin=-2,tmax=2))
        self.add(krivky)
        self.wait()

        self.next_section()
        odstranit(krivky)
        self.play(lambda1.animate.set_value(-0.7))
        krivky = plot_streams(F=F, axes=axes).set_color(ORANGE)
        krivky.add(typ(r"Sedlo"))
        krivky.add(podgraf(tmin=-2,tmax=2))
        self.add(krivky)
        self.wait()

        self.next_section()
        odstranit(krivky)
        self.play(lambda2.animate.set_value(-0.2),otoceni.animate.set_value(0))
        krivky = plot_streams(F=F, axes=axes).set_color(ORANGE)
        krivky.add(typ(r"Stabilní uzel"))
        krivky.add(podgraf(tmin=-2,tmax=2))
        self.add(krivky)
        self.wait()

        self.next_section()
        odstranit(krivky)
        self.play(lambda2.animate.set_value(-0.7),zkoseni.animate.set_value(0))
        krivky = plot_streams(F=F, axes=axes).set_color(ORANGE)
        krivky.add(typ(r"Stabilní uzel"))
        krivky.add(podgraf(tmin=-2,tmax=2))
        self.add(krivky)
        self.wait()

        self.next_section()
        odstranit(krivky)
        self.play(lambdaIm.animate.set_value(0.6))
        krivky = plot_streams(F=F, axes=axes).set_color(ORANGE)
        krivky.add(typ(r"Stabilní ohnisko"))
        self.add(krivky)
        self.wait()

        self.next_section()
        odstranit(krivky)
        self.play(lambda1.animate.set_value(0.7))
        krivky = plot_streams(F=F, axes=axes).set_color(ORANGE)
        krivky.add(typ(r"Nestabilní ohnisko"))
        self.add(krivky)
        self.wait()

        self.next_section()
        odstranit(krivky)
        _l_real = 0.15
        _l_imag = 1.2
        self.play(lambdaIm.animate.set_value(_l_imag),lambda1.animate.set_value(_l_real))
        krivky = plot_streams(F=F, axes=axes, minlength=4, maxlength=8).set_color(ORANGE)
        krivky.add(typ(r"Nestabilní ohnisko"))
        domain = np.linspace(-1,20,1000)
        krivky.add(
            podgraf(
                tmin=-1,
                tmax=20,
                ymin=-15,
                ymax=10,
                popisek=r"e^{\Re(\lambda) t}\cos(\Im(\lambda)t)",
                x_values=domain,
                y_values=np.exp(_l_real*domain)*np.cos(_l_imag*domain)
                )
                )

        self.add(krivky)
        self.wait()

        

