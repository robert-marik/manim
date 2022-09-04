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
            x_length=6*xmax,
            y_length=6*ymax, 
            **myaxis_config
        )
        axes.set_z_index(-2)

        Y, X = np.mgrid[-ymax:ymax:400j, -xmax:xmax:400j]
   
        Det = ValueTracker(.6)
        Stopa = ValueTracker(-2)
        zkoseni = ValueTracker(0.5)
        otoceni = ValueTracker(30*DEGREES)

        def matice_a_vektory():
            theta = otoceni.get_value()
            R=np.matrix([[np.cos(theta), -np.sin(theta)],[np.sin(theta),np.cos(theta)]])
            St = Stopa.get_value()
            Dt = Det.get_value()
            zk = zkoseni.get_value()
            if St**2-4*Dt > 0:
                l1 = (-St+np.sqrt(St**2-4*Dt))/2
                l2 = (-St-np.sqrt(St**2-4*Dt))/2
                A = np.matrix([[l1, zk],[0,l2]])
                A = np.matmul(A,R)
                A = np.matmul(R.T,A)
                vektory = [np.matmul(R.T,np.array([1,0])),np.matmul(R.T,np.array([-zk,l1]))]
                vl_cisla = [l1,l2]
            else:
                A = np.matrix([[St/2,1],[-Dt+St**2/4,St/2]])   
                vl_cisla = [-St/2,np.sqrt(4*Dt - St**2)/2]
                vektory = None
            return [A,vektory,vl_cisla]

        def F(X):
            x,y = X
            A, vektory,vl_cisla = matice_a_vektory()
            return np.array([A[0,0]*x+A[0,1]*y, A[1,0]*x + A[1,1]*y])

        print (F([1,0]))
        print (F([0,1]))

        def get_phase_plot(F=F,axes=axes, small_arrows=False):
            phase_portarit_arrows = VGroup()
            delka = .1
            data = []        
            for i in np.linspace(*axes.x_range[:2],16):
                for j in np.linspace(*axes.y_range[:2],16):
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
                sw = 4
                if small_arrows:
                    sw = 4                   
                phase_portarit_arrows.add(
                    Line(
                        start=axes.c2p(*i[0],0), 
                        end=axes.c2p(*i[1],0), 
                        buff=0, 
                        stroke_width=sw,
                    ).add_tip(tip_length=0.1).set_color(RED)
                )
            A, vektory,vl_cisla = matice_a_vektory()
            print ("Vlastni vektory")
            print (vektory)
            for vektor,barva in zip(vektory,barvy):
                konec = np.array([vektor[0,0],vektor[0,1],0])/(np.sqrt(vektor[0,0]**2+vektor[0,1]**2))
                zacatek = -konec
                print(konec)
                phase_portarit_arrows.add(Line(start=axes.c2p(*zacatek), end=axes.c2p(*konec)).set_color(barva))    
            return(phase_portarit_arrows)

        barvy = [BLUE,YELLOW]
        def plot_streams(F=F, axes=axes):
            U,V = F([X,Y])
            
            speed = np.sqrt(U*U + V*V)
            stream_img = plt.streamplot(X, Y, U, V, density=2)
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

       

        axes.to_corner(UR)
        pplot = get_phase_plot()
        krivky = plot_streams(F=F, axes=axes).set_color(WHITE)
        self.play(*[FadeIn(i) for i in [pplot,krivky]])
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

