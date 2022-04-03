from manim import *

from scipy.integrate import odeint
import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import fsolve
from scipy.interpolate import interp1d



xmax = 1.5
ymax = 1.5
myaxis_config={'tips':False}

class Pokus(MovingCameraScene):
    def construct(self):
        self.camera.frame.save_state()
        axes = Axes(
            x_range=[0,xmax,1e6],
            y_range=[0,ymax,1e6],
            x_length=4*xmax,
            y_length=4*ymax, 
            **myaxis_config
        )
        self.add(axes)
        napis = always_redraw(lambda : Group(
            Tex(r"Lineární systém").scale_to_fit_width(self.camera.frame_width/3).move_to(
            self.camera.frame_center-self.camera.frame_width/2*0.95*RIGHT+self.camera.frame_height/2*0.95*UP,
            aligned_edge=UL
            ).set_color(BLUE).add_background_rectangle(),
            Tex(r"Nelineární systém").scale_to_fit_width(self.camera.frame_width/3).move_to(
            self.camera.frame_center+self.camera.frame_width/2*0.95*RIGHT+self.camera.frame_height/2*0.95*UP,
            aligned_edge=UR
            ).set_color(RED).add_background_rectangle(),
            ))
        self.add(napis)
        self.play(self.camera.frame.animate.scale(0.2).move_to(ORIGIN))
        self.wait()     

        self.play(Restore(self.camera.frame))        

class PhasePortrait(MovingCameraScene):
    def construct(self):

        self.next_section("Fazovy portret")        

        axes = Axes(
            x_range=[0,xmax,1e6],
            y_range=[0,ymax,1e6],
            x_length=4*xmax,
            y_length=4*ymax, 
            **myaxis_config
        )
        axes.set_z_index(-2)
        axes2 = axes.copy()
        Y, X = np.mgrid[0:ymax:400j, 0:xmax:400j]
   
        def F(X):
            x,y = X
            return np.array([x-.85*x**2-0.44*x*y, 2.5*y-2.2*y**2-1*x*y])

        SPall = [] # stationary points
        Jall = [] # Jacobi matrices
        for start in [(1,1),(1.2,0),(0,1.2),(0.01,0.01)]:
            SP = fsolve(F, start)
            SPall = SPall + [SP]
            x0,y0 = SP

            h=0.001
            dx = h*np.array([1,0])
            dy = h*np.array([0,1])

            DX = (F(SP+dx)-F(SP-dx))/(2*h) 
            DY = (F(SP+dy)-F(SP-dy))/(2*h) 

            J = np.matrix([DX,DY]).T
            Jall = Jall + [J]

        def get_phase_plot(F=F,axes=axes, small_arrows=False):
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
                    ).add_tip(tip_length=0.05)
                )
            return(phase_portarit_arrows)

        # def zjemni(pole):
        #     pole = np.array(pole)
        #     x = pole[:,0]
        #     y = pole[:,1]
        #     df = [i for i in range(len(x))]
        #     df1=df[:-1]
        #     df2=df[1:]
        #     out = []
        #     for i,j in zip(df1,df2):
        #         out = out + [i,(2*i+j)/3,(i+2*j)/3]
        #     out = out + [j]
        #     out = np.array(out)
        #     fx = interp1d(df,pole[:,0],kind = 'quadratic')
        #     fy = interp1d(df,pole[:,1],kind = 'quadratic')
        #     return([i for i in np.array([fx(out),fy(out)]).T])
        # def zjemni(pole):
        #     return(pole)

        def plot_streams(F=F, axes=axes):
            U,V = F([X,Y])
            
            speed = np.sqrt(U*U + V*V)
            stream_img = plt.streamplot(X, Y, U, V, density = 2)
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

        rovnice = VGroup(
            MathTex(r"\frac{\mathrm dx}{\mathrm dt}=f_1(x,y)"),
            MathTex(r"\frac{\mathrm dy}{\mathrm dt}=f_2(x,y)"),
            MathTex(r"f_1(x_0,y_0)=f_2(x_0,y_0)=0"),
            MathTex(r"J=\begin{pmatrix}\nabla f_1(x_0,y_0)\\\nabla f_2(x_0,y_0)\end{pmatrix}"),
            MathTex(r"\frac{\mathrm d}{\mathrm dt}\begin{pmatrix}x\\y\end{pmatrix}=J\begin{pmatrix}x-x_0\\y-y_0\end{pmatrix}")
            ).arrange(DOWN).to_edge(LEFT)
        

        axes.to_corner(UR)
        pplot = get_phase_plot().set_color(RED)    
        krivky = plot_streams(F=F, axes=axes).set_color(RED)
        self.play(*[FadeIn(i) for i in [axes,pplot,krivky]])
        self.play(FadeIn(rovnice))
        self.wait()

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
            #self.wait()

            #self.next_section()
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
                        ).arrange(RIGHT))
                vl.arrange(DOWN).to_corner(UL)
                self.play(FadeIn(konec),FadeIn(vl))    

            self.wait()

        

