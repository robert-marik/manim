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
            x_length=2,
            y_length=2, 
            **myaxis_config
        )
        Y, X = np.mgrid[-ymax:ymax:400j, -xmax:xmax:400j]
   
        # trace = ValueTracker(0.5)
        # determinant = ValueTracker(0.05)
        lambda1 = ValueTracker(1)
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
            _,A,vals,isreal = get_characteristics()
            if not isreal:
                hodnoty = VGroup(
                    #MathTex(r"\lambda_{1} = "+str(round(vals[0],2))).set_color(c[0]),
                    #MathTex(r"\lambda_{2} = "+str(round(vals[1],2))).set_color(c[1])
                    MathTex(r"\lambda_{1} = "+'{:.2f} {:+.2f}i'.format(np.round(vals[0].real,2), vals[0].imag)).set_color(c[0]),
                    MathTex(r"\lambda_{2} = "+'{:.2f} {:+.2f}i'.format(np.round(vals[1].real,2), vals[1].imag)).set_color(c[1]),
                ).arrange(DOWN).to_edge(UL)
                phase_portrait_arrows.add(hodnoty)
                phase_portrait_arrows.add(Dot(axes2.c2p(np.real(vals[0]),np.imag(vals[0]),0)).set_color(c[0]))
                phase_portrait_arrows.add(Dot(axes2.c2p(np.real(vals[1]),np.imag(vals[1]),0)).set_color(c[1]))
            else:
                if np.abs(vals[0]-vals[1])>0.0001:
                    for v,col in zip([[A[0,0],A[1,0]],[A[0,1],A[1,1]]],c):
                        v_ = np.array(v)
                        start = v_/np.sqrt(v[0]**2+v[1]**2)
                        end = -start
                        phase_portrait_arrows.add(Line(start = axes.c2p(*start,0), end = axes.c2p(*end,0)).set_color(col))
                hodnoty = VGroup(
                    MathTex(r"\lambda_1 = "+str(round(vals[0],2))).set_color(c[0]),
                    MathTex(r"\lambda_2 = "+str(round(vals[1],2))).set_color(c[1])
                ).arrange(DOWN, aligned_edge = LEFT).to_edge(UL)
                phase_portrait_arrows.add(hodnoty)
                phase_portrait_arrows.add(Dot(axes2.c2p(vals[0],0,0)).set_color(c[0]))
                phase_portrait_arrows.add(Dot(axes2.c2p(vals[1],0,0)).set_color(c[1]))


            return(phase_portrait_arrows)

        c = [BLUE,YELLOW]

        def plot_streams(F=F, axes=axes):
            U,V = F([X,Y])
            
            speed = np.sqrt(U*U + V*V)
            #return VGroup()
            stream_img = plt.streamplot(X, Y, U, V, density = 1)
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

        axes.to_corner(UR)
        axes2.to_edge(LEFT)
        axes2.add(Tex(r"$\Re(\lambda)$").next_to(axes2.get_x_axis()))
        axes2.add(Tex(r"$\Im(\lambda)$").next_to(axes2.get_y_axis(),UP))
        pplot = always_redraw(lambda : get_phase_plot())
        self.add(pplot,axes2)

        krivky = plot_streams(F=F, axes=axes).set_color(ORANGE)
        self.add(krivky)
        self.wait()

        self.next_section()
        odstranit(krivky)
        self.play(lambda1.animate.set_value(0.7))
        krivky = plot_streams(F=F, axes=axes).set_color(ORANGE)
        self.add(krivky)
        self.wait()

        self.next_section()
        odstranit(krivky)
        self.play(lambda1.animate.set_value(-0.7))
        krivky = plot_streams(F=F, axes=axes).set_color(ORANGE)
        self.add(krivky)
        self.wait()

        self.next_section()
        odstranit(krivky)
        self.play(lambda2.animate.set_value(-0.2),otoceni.animate.set_value(0))
        krivky = plot_streams(F=F, axes=axes).set_color(ORANGE)
        self.add(krivky)
        self.wait()

        self.next_section()
        odstranit(krivky)
        self.play(lambda2.animate.set_value(-0.7),zkoseni.animate.set_value(0))
        krivky = plot_streams(F=F, axes=axes).set_color(ORANGE)
        self.add(krivky)
        self.wait()

        self.next_section()
        odstranit(krivky)
        self.play(lambdaIm.animate.set_value(0.6))
        krivky = plot_streams(F=F, axes=axes).set_color(ORANGE)
        self.add(krivky)
        self.wait()

        self.next_section()
        odstranit(krivky)
        self.play(lambda1.animate.set_value(0.7))
        krivky = plot_streams(F=F, axes=axes).set_color(ORANGE)
        self.add(krivky)
        self.wait()

        self.next_section()
        odstranit(krivky)
        self.play(lambdaIm.animate.set_value(1.2),lambda1.animate.set_value(0.3))
        krivky = plot_streams(F=F, axes=axes).set_color(ORANGE)
        self.add(krivky)
        self.wait()


        return False
        self.next_section()
        self.play(FadeOut(krivky))
        self.play(trace.animate.set_value(-0.5),determinant.animate.set_value(0.5))
        krivky = plot_streams(F=F, axes=axes).set_color(ORANGE)
        self.add(krivky)
        self.wait()

        self.next_section()
        self.play(FadeOut(krivky))
        self.play(trace.animate.set_value(0.5),determinant.animate.set_value(0.5))
        krivky = plot_streams(F=F, axes=axes).set_color(ORANGE)
        self.add(krivky)
        self.wait()

        return False
        self.next_section()       
        body = VGroup(*[Dot(axes.c2p(i,j,0)).set_color(YELLOW) for i,j in SPall])
        self.play(FadeIn(body))
        self.play(*[Flash(i) for i in body])
        self.wait()

        self.next_section()
        self.play(FadeOut(body), FadeOut(rovnice))
        # SPall = [SPall[0]]
        # Jall = [Jall[0]]

        i = 0
        for SP,J in zip(SPall,Jall):
            i = i+1
            x0,y0 = SP
            def F2(X):
                x,y = X
                return np.array([
                    J[0,0]*(x-x0) + J[0,1]*(y-y0),
                    J[1,0]*(x-x0) + J[1,1]*(y-y0)
                    ])

            axes2.to_corner(UL)
            StacBod = Dot(axes.c2p(x0,y0,0)).set_color(ORANGE)
            StacBod2 = Dot(axes2.c2p(x0,y0,0)).set_color(BLUE)
            pplot2 = get_phase_plot(F=F2,axes=axes2,small_arrows=True).set_color(BLUE)   
            krivky2 = plot_streams(F=F2, axes=axes2).set_color(BLUE)
            vals, vecs = np.linalg.eig(J)
            vektory = {}
            vektory['ori']=VGroup()
            vektory['lin']=VGroup()
            P = np.array(vecs)
            sx,sy = np.array(SP)-.2*P[:,0]
            ex,ey = np.array(SP)+.2*P[:,0]
            for a,w in zip([axes,axes2],['ori','lin']):
                vektory[w].add(Line(
                    start=a.c2p(sx,sy,0), 
                    end=a.c2p(ex,ey,0), 
                    buff = 0).set_color(GRAY))
            sx,sy = np.array(SP)-.2*P[:,1]
            ex,ey = np.array(SP)+.2*P[:,1]
            for a,w in zip([axes,axes2],['ori','lin']):
                vektory[w].add(Line(
                    start=a.c2p(sx,sy,0), 
                    end=a.c2p(ex,ey,0), 
                    buff = 0).set_color(GREEN))
            vektory['hodnoty'] = VGroup(
                    MathTex(r"\lambda_1 = "+str(round(vals[0],3))).set_color(GRAY).scale(.7),
                    MathTex(r"\lambda_2 = "+str(round(vals[1],3))).set_color(GREEN).scale(.7)
                    ).arrange(RIGHT) 
            self.play(*[FadeIn(i) for i in [axes2,pplot2,StacBod,StacBod2]])
            self.wait()

            self.next_section()
            napis = always_redraw(lambda :
                Tex(r"Lineární systém "+str(i)).scale_to_fit_width(self.camera.frame_width/3).move_to(
                self.camera.frame_center-self.camera.frame_width/2*0.95*RIGHT+self.camera.frame_height/2*0.95*UP,
                aligned_edge=UL
                ).set_color(BLUE).set_z_index(10).add_background_rectangle(opacity=1)
                )
            napis2 = always_redraw(lambda :
                Tex(r"Nelineární systém").scale_to_fit_width(self.camera.frame_width/3).move_to(
                self.camera.frame_center+self.camera.frame_width/2*0.95*RIGHT+self.camera.frame_height/2*0.95*UP,
                aligned_edge=UR
                ).set_color(RED).set_z_index(10).add_background_rectangle(opacity=1)
                )
            vektory['hodnoty'].add_background_rectangle(
                    buff=0.2, opacity=1).next_to(napis,DOWN).to_edge(
                LEFT)
            if i==3:
                vektory['hodnoty'].move_to(axes2,aligned_edge=DOWN)
            self.play(*[FadeIn(i) for i in 
                [krivky2,vektory['ori'],vektory['lin'],vektory['hodnoty'],napis,napis2]])
            self.play(Flash(StacBod),Flash(StacBod2))
            self.wait()

            self.next_section()
            self.play(
                FadeOut(vektory['lin']),
                FadeOut(vektory['hodnoty']),
                VGroup(axes2,pplot2,krivky2,StacBod2).animate.shift(axes.c2p(0,0,0)-axes2.c2p(0,0,0))
                )
            self.wait()

            self.next_section()
            self.camera.frame.save_state()
            self.play(self.camera.frame.animate.scale(0.2).move_to(StacBod))
            self.wait()     

            self.next_section()
            self.play(Restore(self.camera.frame))
            self.play(FadeOut(pplot2,krivky2,StacBod,StacBod2,napis,vektory['ori'],axes2))  
            if i==4:
                konec = VGroup()
                vl = VGroup()
                for sp,j,c in zip(SPall,Jall,[YELLOW,GREEN,BLUE,WHITE]):
                    bod=Dot(axes.c2p(sp[0],sp[1],0)).set_color(c)
                    konec.add(bod)
                    vals, vecs = np.linalg.eig(j)
                    vl.add(VGroup(
                        MathTex(r"\lambda_1 = "+str(round(vals[0],3))).set_color(c),
                        MathTex(r"\lambda_2 = "+str(round(vals[1],3))).set_color(c)
                        ).arrange(DOWN, aligned_edge=LEFT))
                vl.arrange(DOWN, buff=0.5, aligned_edge=LEFT).to_corner(UL).shift(RIGHT)
                self.play(FadeIn(konec),FadeIn(vl))    

            self.wait()

        

