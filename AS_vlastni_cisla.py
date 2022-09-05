from manim import *

import matplotlib.pyplot as plt
import numpy as np
from scipy.integrate import solve_ivp  # řešení diferenciálních rovnic

xmax = 1
ymax = 1
myaxis_config={'tips':False}


   
class Nadpis(Scene):
    def construct(self):
        self.next_section("Nadpis")        
        title = Title(r"Lineární autonomní systémy")
        autor = VGroup(Tex("Robert Mařík"),Tex("Mendel University")).arrange(DOWN).next_to(title,DOWN)
        self.play(GrowFromCenter(title))
        self.play(GrowFromCenter(autor[0]))
        self.play(GrowFromCenter(autor[1]))
        self.wait()
        aplikace = VGroup(*[Tex(_) for _ in ["mechanické kmity", "tepelná výměna mezi více vrstvami", "linearizace obecnějších nelineárních systémů"]]).arrange(DOWN).next_to(autor,DOWN, buff=2)
        for i,c in enumerate([RED,BLUE,ORANGE]):
            aplikace[i].set_color(c)
        self.play(AnimationGroup(*[GrowFromCenter(_) for _ in aplikace], lag_ratio=0.95), run_time=5)

        self.wait()


class Ukazky(Scene):
    def construct(self):

        rovnice =VGroup(
            Tex(r"Mechanické kmitání"),
            Tex(r"""
            \begin{align*}
            x'&=v\\
            v'&=-kx - bv
            \end{align*}
            """),
            Tex(r"""
            \begin{align*}
            x'&=0\cdot x+1\cdot v\\
            v'&=-k\cdot x - b\cdot v
            \end{align*}
            """),
            MathTex(r"""
            \begin{pmatrix}
            x \\ v
            \end{pmatrix}'
            =
            \begin{pmatrix}
            0 & 1 \\ -k & -b
            \end{pmatrix}
            \begin{pmatrix}
            x \\ v
            \end{pmatrix}
            """),
            MathTex(r"X'=AX")
            ).scale(0.8).arrange(DOWN,buff=0.5).to_corner(UL)
        
        rovnice2 =VGroup(
            Tex(r"Tepelná výměna s mezivrstvou"),
            Tex(r"""
            \begin{align*}
            T_1'&=k_1(T_0-T_1)-k_2(T_1-T_2)\\
            T_2'&=k_3(T_1-T_2)
            \end{align*}
            """),
            Tex(r"""
            \begin{align*}
            T_1'&=-(k_1+k_2)\cdot T_1+k_2\cdot T_2 + k_1T_0\\
            T_2'&=k_3\cdot T_1 - k_3\cdot T_2
            \end{align*}
            """),
            MathTex(r"""
            \begin{pmatrix}
            T_1 \\ T_2
            \end{pmatrix}'
            =
            \begin{pmatrix}
            -(k_1+k_2) & k_2 \\ k_3 & -k_3
            \end{pmatrix}
            \begin{pmatrix}
            T_1 \\ T_2
            \end{pmatrix}
            +
            \begin{pmatrix}
            k_1T_0 \\ 0
            \end{pmatrix}
            """),
            Tex(r"$T'=AT$ (pro $T_0=0$)")
            ).scale(0.8).arrange(DOWN,buff=0.5).to_corner(UR)

        rovnice[0].set_color(BLUE)
        rovnice2[0].set_color(BLUE)

        self.next_section("")
        self.play(FadeIn(rovnice[:2]))
        for i in range(2,len(rovnice)):
            self.wait(.5)
            self.next_section("")
            self.play(TransformMatchingShapes(rovnice[i-1].copy(),rovnice[i]))
        self.wait()

        self.next_section("")
        self.play(FadeIn(rovnice2[:2]))
        for i in range(2,len(rovnice2)):
            self.wait(0.5)
            self.next_section("")
            self.play(TransformMatchingShapes(rovnice2[i-1].copy(),rovnice2[i]))
        self.wait()

        

class Description(Scene):
    def construct(self):
        
        rovnice = VGroup(
            Tex(r"Maticová formulace"),
            MathTex(r"X'=AX").set_color(YELLOW),
            MathTex(r"X(t)=e^{\lambda t}\vec u"),
            VGroup(
                MathTex(r"\lambda e^{\lambda t}\vec u=Ae^{\lambda t}\vec u"),
                MathTex(r"A\vec u =\lambda \vec u"),
                MathTex(r"(A-\lambda I)\vec u = 0").set_color(BLUE),
                MathTex(r"|A-\lambda I|=0").set_color(RED)).arrange(DOWN, aligned_edge=LEFT)
        ).arrange(DOWN, buff=0.5, aligned_edge=LEFT).scale(0.9).to_corner(UL)
        rovnice[-1].shift(RIGHT)

        komponenty=VGroup(
            Tex(r"Formulace v komponentách"),
            Tex(r"""
            \begin{align*}
            x_1'&=a_{11}x_1+a_{12}x_2\\
            x_2'&=a_{21}x_1+a_{22}x_2
            \end{align*}
            """).set_color(YELLOW),
            MathTex(r"\lambda^2-(a_{11}+a_{22})\lambda+a_{11}a_{22}-a_{12}a_{21}=0").scale(1).set_color(RED),
            MathTex(r"\lambda_{1,2}=\cdots"),
            Tex(r"""\begin{align*}(a_{11}-\lambda_i) u_{i1} + a_{12}u_{i2}&=0\\
            a_{21}u_{i1}+(a_{22}-\lambda_i)u_{i2}&=0
            \end{align*}
            """).set_color(BLUE),
        ).arrange(DOWN,buff=0.5).scale(0.9).to_corner(UR)

        self.next_section()
        self.play(FadeIn(rovnice[:3]))
        self.wait()

        self.next_section()
        self.play(FadeIn(rovnice[-1][:2]))
        self.wait()
        self.next_section()
        self.play(FadeIn(rovnice[-1][2:]))
        self.wait()

        self.next_section()
        self.play(
            FadeIn(komponenty),
                )
        self.wait()

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

        def get_phase_plot(F=F,axes=axes, axes2 = axes2, small_arrows=False, deleni = 10, kreslit_poloprimky = True):
            """
            In axes draws vector field defined by the function F. In axes2
            """
            phase_plot = VGroup()

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
            phase_plot.sipky = VGroup()
            for i in data:             
                sw = 4
                phase_plot.sipky.add(
                    Line(
                        start=axes.c2p(*i[0],0), 
                        end=axes.c2p(*i[1],0), 
                        buff=0, 
                        stroke_width=sw,
                    ).add_tip(tip_length=0.1)
                )
            phase_plot.add(phase_plot.sipky)
            matice,A,vals,isreal = get_characteristics()
            if not isreal:
                reseni = VGroup(
                    MathTex(r'X(t)=e^{'+'{:.2f}'.format(vals[0].real)+r't}\varphi(t)'),
                    Tex(r'$\varphi(t)$ periodická s úhlovou frekvencí $'+'{:.2f}'.format(vals[0].imag)+r'$')
                    ).scale(0.75).arrange(DOWN, aligned_edge=LEFT)
                reseni.scale_to_fit_width(6)                
                reseni.next_to(system, DOWN, aligned_edge=LEFT, buff=0.25)
                reseni.add_background_rectangle()
                hodnoty = VGroup(
                    MathTex(r"\lambda_{1} = "+'{:.2f} {:+.2f}i'.format(np.round(vals[0].real,2), vals[0].imag)).set_color(c[0]),
                    MathTex(r"\lambda_{2} = "+'{:.2f} {:+.2f}i'.format(np.round(vals[1].real,2), vals[1].imag)).set_color(c[1])
                ).arrange(DOWN).to_edge(UL).shift(2*DOWN)
                phase_plot.hodnoty = hodnoty
                phase_plot.dots=VGroup(
                    Dot(axes2.c2p(np.real(vals[0]),np.imag(vals[0]),0)).set_color(c[0]),
                    Dot(axes2.c2p(np.real(vals[1]),np.imag(vals[1]),0)).set_color(c[1]))
                phase_plot.reseni = reseni
                phase_plot.add(
                    phase_plot.hodnoty,
                    phase_plot.reseni,
                    phase_plot.dots)
            else:
                if np.abs(vals[0]-vals[1])>0.0001:
                    phase_plot.smery = VGroup()
                    if poloprimky:
                        for v,col in zip([[A[0,0],A[1,0]],[A[0,1],A[1,1]]],c):
                            v_ = np.array(v)
                            end = v_/np.sqrt(v[0]**2+v[1]**2)
                            #start = -end
                            #start = np.array([0,0])
                            phase_plot.smery.add(Line(start = axes.c2p(0,0,0), end = axes.c2p(*end,0)).set_color(col))
                            end = -end
                            phase_plot.smery.add(Line(start = axes.c2p(0,0,0), end = axes.c2p(*end,0)).set_color(col))
                    phase_plot.add(phase_plot.smery)    
                    reseni = MathTex(r'X(t)={{C_1}} {{\vec u_1 e^{'+'{:.2f}'.format(vals[0])+r't}}}+{{C_2}}{{\vec u_2 e^{'+'{:.2f}'.format(vals[1])+r't}}}').scale(0.75)
                    reseni[1:4].set_color(c[0])
                    reseni[5:].set_color(c[1])
                    reseni.scale_to_fit_width(5.5)                
                    reseni.next_to(system, DOWN, aligned_edge=LEFT, buff=0.25)
                    reseni.add_background_rectangle()
                else:
                    reseni=VGroup().next_to(system,DOWN)
                hodnoty = VGroup(
                    MathTex(r"\lambda_1 = "+'{:.2f}'.format(np.round(vals[0],2))).set_color(c[0]),
                    MathTex(r"\lambda_2 = "+'{:.2f}'.format(np.round(vals[1],2))).set_color(c[1])
                ).arrange(DOWN, aligned_edge = LEFT).to_edge(UL).shift(2*DOWN)
                phase_plot.hodnoty = hodnoty
                phase_plot.dots = VGroup(
                        Dot(axes2.c2p(vals[0],0,0)).set_color(c[0]),
                        Dot(axes2.c2p(vals[1],0,0)).set_color(c[1]))
                phase_plot.reseni = reseni
                phase_plot.add(
                    phase_plot.hodnoty,
                    phase_plot.reseni,
                    phase_plot.dots)

            return(phase_plot)

        c = [BLUE,YELLOW]

        def plot_streams(F=F, axes=axes, minlength=None, maxlength=None):
            U,V = F([X,Y])
            
            speed = np.sqrt(U*U + V*V)
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
            #self.remove(co)
            self.play(FadeOut(co))

        def odstranit_(co):
            #for i in co:
            #    self.remove(i)
            self.play(*[FadeOut(_) for _ in co])

        def pridat(co):
            #self.add(co)
            self.play(*[FadeIn(_) for _ in co])

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
            popisekG.add(MathTex("t").scale(0.5).next_to(axes3.get_x_axis(),buff=0.05))
            popisekG.add(MathTex(popisek).scale(0.5).move_to(axes3.get_y_axis(),UL).shift(0.05*RIGHT))
            if realna_cast_dodatek:
                dodatek = r"\\(reálná část)"
            else:
                dodatek = ""
            popisekG.add(Tex(r"Graf exponenciální funkce"+dodatek).scale(0.5).next_to(axes3,DOWN))
            
            output = VGroup(axes3,g1,g2,popisekG).shift(posun)
            return output

        realna_cast_dodatek = False
        poloprimky = True
        system = MathTex(r"X'=AX").to_corner(UL)
        self.add(system)
        self.wait()

        self.next_section()
        axes.to_corner(UR)
        axes2.move_to((-2.2,-1.3,0))
        axes2.add(Tex(r"$\Re(\lambda)$").scale(0.5).next_to(axes2.get_x_axis(),buff=0))
        axes2.add(Tex(r"$\Im(\lambda)$").scale(0.5).next_to(axes2.get_y_axis(),UP,buff=0))
        axes2.add(Tex(r"Vlastní čísla\\ v Gaussově rovině").scale(0.5).next_to(axes2,DOWN))
        krivky = plot_streams(F=F, axes=axes).set_color(ORANGE)
        info = VGroup(typ(r"Nestabilní uzel"))
        info.add(podgraf())
        pplot = get_phase_plot()
        self.add(pplot.hodnoty)
        self.wait()

        self.next_section()
        fund_system = VGroup(pplot.reseni[3:5],pplot.reseni[7:])
        self.add(fund_system)
        self.add(axes2,info[-1],pplot.dots)
        self.wait()

        self.next_section()
        self.add(axes)
        _, vecs, __, ___ = get_characteristics()
        self.play(AnimationGroup(
            Create(pplot.smery[0]),
            Create(pplot.smery[2])))
        self.wait()

        self.next_section()
        self.play(AnimationGroup(
            Create(pplot.smery[1]),
            Create(pplot.smery[3])))
        self.wait()

        self.next_section()
        self.play(FadeIn(pplot.sipky))
        self.wait()

        self.next_section()
        self.remove(
            pplot.dots,
            pplot.hodnoty,
            pplot.smery[0],
            pplot.smery[1],
            pplot.smery[2],
            pplot.smery[3],
            pplot.sipky,
            axes,
            fund_system
            )
        pplot = always_redraw(lambda : get_phase_plot(kreslit_poloprimky = poloprimky))
        self.add(pplot)
        self.add(info)
        pridat(krivky)
        self.add(Tex(r"Fázový portrét").scale(0.7).add_background_rectangle(buff=0.2).move_to(axes,DOWN))
        self.wait()
       
        self.next_section()
        odstranit_(krivky)
        odstranit(info)
        self.play(lambda1.animate.set_value(0.4))
        krivky = plot_streams(F=F, axes=axes).set_color(ORANGE)
        info = VGroup(typ(r"Nestabilní uzel"))
        info.add(podgraf(tmin=-2,tmax=2))
        self.add(info)
        pridat(krivky)
        self.wait()

        self.next_section()
        odstranit_(krivky)
        odstranit(info)
        self.play(lambda1.animate.set_value(-0.7))
        krivky = plot_streams(F=F, axes=axes).set_color(ORANGE)
        info = VGroup(typ(r"Sedlo"))
        info.add(podgraf(tmin=-2,tmax=2))
        self.add(info)
        pridat(krivky)
        self.wait()

        self.next_section()
        odstranit_([*krivky,info])
        self.play(lambda2.animate.set_value(-0.2),otoceni.animate.set_value(0))
        krivky = plot_streams(F=F, axes=axes).set_color(ORANGE)
        info = VGroup(typ(r"Stabilní uzel"))
        info.add(podgraf(tmin=-2,tmax=2))
        self.add(info)
        pridat(krivky)
        self.wait()

        self.next_section()
        odstranit_(krivky)
        odstranit(info)
        poloprimky = False
        self.play(lambda2.animate.set_value(-0.7),zkoseni.animate.set_value(0))
        #return False
        krivky = plot_streams(F=F, axes=axes).set_color(ORANGE)
        info = VGroup(typ(r"Stabilní uzel"))
        info.add(podgraf(tmin=-2,tmax=2))
        self.add(info)
        pridat(krivky)
        self.wait()

        self.next_section()
        realna_cast_dodatek = True
        odstranit_(krivky)
        odstranit(info)
        self.play(lambdaIm.animate.set_value(0.6))
        krivky = plot_streams(F=F, axes=axes).set_color(ORANGE)
        info = VGroup(typ(r"Stabilní ohnisko"))
        domain = np.linspace(-1,10,1000)
        ft = np.exp(lambda1.get_value()*domain)*np.cos(lambdaIm.get_value()*domain)
        info.add(
            podgraf(
                tmin=0,
                tmax=10,
                ymin=np.min(ft),
                ymax=np.max(ft),
                popisek=r"\Re(e^{\lambda t})",
                x_values=domain,
                y_values=ft
                )
                )
        self.add(info)
        pridat(krivky)
        self.wait()

        self.next_section()
        odstranit_(krivky)
        odstranit(info)
        self.play(lambda1.animate.set_value(0.7))
        krivky = plot_streams(F=F, axes=axes).set_color(ORANGE)
        info = VGroup(typ(r"Nestabilní ohnisko"))
        ft = np.exp(lambda1.get_value()*domain)*np.cos(lambdaIm.get_value()*domain)
        info.add(
            podgraf(
                tmin=0,
                tmax=10,
                ymin=np.min(ft),
                ymax=np.max(ft),
                popisek=r"\Re(e^{\lambda t})",
                x_values=domain,
                y_values=ft
                )
                )
        self.add(info)
        pridat(krivky)
        self.wait()

        self.next_section()
        odstranit_(krivky)
        odstranit(info)
        _l_real = -0.15
        _l_imag = 1.2
        self.play(lambdaIm.animate.set_value(_l_imag),lambda1.animate.set_value(_l_real))

        reseni = solve_ivp(lambda t,X:F(X), [0, 35], [-.7,-1], dense_output=True, max_step=0.005)
        krivky = VGroup(
            axes.plot_line_graph(x_values=reseni.y[0], y_values=reseni.y[1], add_vertex_dots = False).set_stroke(width=2).set_color(ORANGE)
        )
        #krivky = plot_streams(F=F, axes=axes, minlength=4.15, maxlength=8).set_color(ORANGE)
        
        info = VGroup(typ(r"Stabilní ohnisko"))
        domain = np.linspace(-1,20,1000)
        y_val = np.exp(_l_real*domain)*np.cos(_l_imag*domain)
        info.add(
            podgraf(
                tmin=-1,
                tmax=20,
                ymin=np.min(y_val),
                ymax=np.max(y_val),
                popisek=r"\Re(e^{\lambda t})",
                x_values=domain,
                y_values=y_val
                )
                )
        self.add(info)
        pridat([krivky])
        self.wait()


komentar_old = """
Dobrý den, v tomto videu si ukážeme, jak je možné použít prostředky lineární algebry k řešení soustav lineárních diferenciálních rovnic s koeficienty nezávislými na čase. Využití najdeme například při studiu kmitajících mechanických soustav, při tepelné výměně s okolním prostředím přes mezivrstvu. Lineární soustavy jsou díky linearitě jednoduché a proto často studujeme nelineární systémy tak, že je aproximujeme pomocí systémů lineárních. 

Uvažujme mechanické kmitání v přímce okolo rovnovážného stavu. Polohu označme x, rychlost označme v. Z mechaniky víme, že derivace polohy je rychlost a derivace rychlosti je úměrná působící síla. Síla má komponentu, která vrací těleso do rovnovážné polohy a komponentu udávající odpor prostředí. Použijeme lineární aproximaci a zápornýám znaménkem vyjádříme, že síla vrací těleso do rovnovážné polohy a že odporová síla působí proti směru pohybu. Tímto dostáváme soustavu dvou rovnic, kterou je možno zapsat i maticově jako je na obrazovce. Derivace sloupcové matice s komponentami poloha a rychlost je rovna násobku této matice s jistou čtvercovou 2-krát-2 maticí.

Uvažujme tepelnou výměnu pomocí Newtonova zákona tepelné výměny, tedy bez vedení tepla. Teplota okolí je T_0. Okolí si vyměňuje teplo s mezivrstvou o teplotě T_1 a tato mezivrstva si vyměňuje teplo s vnitřní vrstvou o teplotě T_2. Intenzita tepelné výměny je úměrná rozdílu teplot, což nám dává diferenciální rovnici pro vývoj teploty v každé vrstvě. Po roznásobení závorek je možné soustavu upravit a zapsat maticově podobně jako soustavu v předchozím případě. Aditivní člen n můžeme vynechat, pokud posuneme stupnici teploty tak, že teplota okolí je nulová.

Předchozí příklady byly speciálním případem soustavy X'=AX pro sloupcový vektor X a čtvercovou matici A. Pokud by se jednalo o skalární veličiny, byla by řešením exponenciální funkce. Pokusíme se o něco podobného a budeme hledat řešení ve tvaru exponenciální funkce s parametrem lambda a vektoru u. Tento předpis můžeme rovnou dostadit do rovnice. Přitom derivace exponenciální funkce je tatáž funkce vynásobená derivací vnitřní složky, což je zde lambda. Po vydělení rovnice exponenciálním členem vidíme stejnou úlohu na hledání vlastních směrů a vlastních čísel matice A. Tato úloha má řešení s nenulovým vektorem u, pokud determinant A-lambda*I bude nulový. Po rozepsání do složek pro soustavu se dvěma rovnicemi a dvěma neznámými je rovnice pro nulovost determinantu kvadratickou rovnicí. Tato rovnice má dva kořeny a každý z nich použijeme v odpovídající modré soustavě rovnic k nalezení vlastních vektorů. Toto platí v nejoptimističtějším případě, kdy existují dvě reálná vlastní čísla. Pokud jsou čísla komplexně sdružená, bereme reálné části. V optimálním případě tedy máme dvě vlastní čísla a k nium vlastní vektory a tím máme dvě řešení. Pojďme si ukázat, jak to může dopadnout. 

"""


        
komentar = """
Dobrý den, v tomto videu si ukážeme, jak umíme u lineárních autonomních systémů v rovině analyzovat chování jednotlivých řešení.

Nejprve si připomeňme maticovou formulaci autonomního systému. Například mechanické kmity tělesa o jednotkové hmotnosti na pružině o tuhosti 'k' je možné popsat pomocí následujících dvou pohybových rovnic, kde 'x' a 'v' jsou poloha a rychlost tělesa. První rovnice udává rychlost jako časovou změnu polohy a druhá rovnice udává zrychlení způsobené silou pružiny a odporem prostředí se součinitelem odporu 'b'. Tuto soustavu je možné pomocí maticového násobení zapsat v kompaktnějším tvaru X'=AX.

Jiný proces vedoucí na rovnici téhož typu je model popisující tepelnou výměnu ve vrstvených tělesech či materiálech. Předpokládejme například vnější prostředí o teplotě T0, ve kterém je těleso o teplotě T2 a tepelná výměna probíhá prostřednictvím obalu o teplotě T1. Protože výměna tepla na jednotlivých rozhraních probíhá rychlostí úměrnou rozdílu teplot, máme pro dvě rozhraní dvě lineární rovnice. Pokud přeuspořádáme členy na pravé straně, je možné opět zapsat soustavu pomocí maticového součinu. Volíme-li navíc počátek teplotní stupnice tak, aby teplota okolí byla nulová, redukuje se model na T'=AT.

V obou případech je řešením funkce mající tu vlastnost, že její derivace je rovna součinu této funkce s maticí A. Pokud budeme hledat takovou funkci ve tvaru součinu exponenciální funkce "e na lambda t" a vektoru "u", je možné derivaci vypočítat a po dosazení do rovnice vidíme, že vektor "u" musí být vlastním vektorem příslušným vlastní hodnotě lambda a musí tedy vyhovovat příslušné soustavě rovnic zapsané modře. Vlastní hodnoty určíme standardně jako hodnoty vyhovující charakteristické rovnici zapsané červeně. Soustavu pro vlastní vektory a vlastní čísla můžeme vyjádřit i v komponentách, jak je vidět na obrazovce v pravém sloupci. Je zde zejména vidět kvadratická rovnice, sloužící pro určení vlastních hodnot vyjádřená pomocí koeficientů soustavy.

Uvažujme soustavu X'=AX a nechť jsou vlastní čísla lambda1 a lambda2. Pokud k nim najdeme vlastní vektory, máme dvě řešení ve tvaru součinu vlastního vektoru s exponenciálním faktorem. Tato exponenciální část v závislosti na hodnotě parametru t probíhá kladná reálná čísla. Toto si budeme znázorňovat v grafu exponenciální funkce vlevo dole. Kromě toho budeme znázorňovat vlastní čísla v gaussově rovině. To znamená, že vodorovně vynášíme reálnou část a svisle imaginární část každého z vlastních čísel. Pokud řešení budeme chápat jako parametrické křivky s parametrem t a pokud tyto křivky zakreslíme v rovině, dostanem polopřímky ze středu mířící vlastním směrem.

Ukážeme si jednotlivé možnosti, jak se mohou řešení chovat. Budeme se zabývat jenom případem, kdy vlastní čísla jsou obě nenulová. 

Může například nastat situace na obrazovce, kdy obě vlastní čísla jsou kladná. Pro t jdoucí do nekonečna obě řešení numericky rostou, pro t jdoucí do minus nekonečna jdou k nule. Ve fázové rovině řešení představují polopřímky ve směrech u1 a u2 mířící směrem od počátku. Samozřejmě další řešení budou mířit opačným směrem, protože i opačné vektory k vlastním vektorům jsou vlastními vektory. Díky tomu v obrázku každá dvojice polopřímek vytvoří jednu přímku. V průsečíku těchto přímek je stacionární bod. Ostatní řešení jsou lineárními kombinacemi těchto dvou. To dává dobrou představu o chování všech dalších řešení. Všechna další řešení vychází z počátku směrem příslušným žluté barvě, vzdalují se od počátku a postupně se přiklání ke směru modré barvy. V takovém případě se bod, ze kterého trajektorie vychází, nazývá nestabilní uzel. 

Pokud hodnotu lambda1 snížíme pod hodnotu lambda2, změní se fázový portrét pouze v tom, že od stacionárního bodu vychází trajektorie modrým směrem a odklání se do směru žlutého. Stacionární bod je stále nestabilní uzel. 

Pokud však jedna vlastní hodnota klesne do záporných čísel, příslušné řešení (v tomto případě modré) jde pro t jdoucí do nekonečna k nule a směr trajektorií na modrých polopřímkách se otočí. Trajektorie ve žlutých polopřímkách zůstávají a ostatní trajektorie jsou lineárními kombinacemi. Vznikne situace, kdy jenom konečný počet trajektorií (jenom modré a žluté polopřímky) prochází stacionárním bodem a takový stacionární bod se nazývá sedlo. 

Pokud budou obě vlastní čísla záporná, situace se opět kvalitativně mění. Tentokrát do stacionárního bodu směrují i trajektorie v modrých polopřímkách, i trajektorie ve žlutých polopřímkách, a i všechny lineární kombinace těchto trajektorií. Takový stacionární bod se nazývá stabilní uzel. 

Pokud v málo pravděpodobném ale možném případě budou obě vlastní čísla stejná, je situace analogická, ale trajektorie míří do počátku za všech směrů. To je jenom jiná varianta stabilního uzlu. Důležité je, že se trajektorie přibližují bez oscilací. 

Oscilace v prostoru řešení vzniknou, pokud budou vlastní čísla nabývat komplexních hodnot. Jestli se oscilace stahují ke stacionárnímu bodu, nebo rozmotávají, je řízeno reálnou částí vlastního čísla. Na našem obrázku je reálná část záporná, rovna -0.7. To znamená, že řešení oscilují s stahují se ke stacionárnímu bodu. Takový bod se nazývá stabilní ohnisko.

Bude-li reálná část vlastních hodnot kladná, dojde naopak k rozvíjení trajektorií od stacionárního bodu a dostáváme nestabilní ohnisko. 

Chceme-li lépe vidět oscilace a spirálu mířící do stacionárního bodu, stačí zařídit, aby reálná část byla numericky malá, tedy blízko k nule. Takto by to vypadalo pro stabilní případ a na obrázku je pro přehlednost nakreslena jenom jedna trajektorie. 

Vidíme tedy, že chování trajektorií je možné posoudit pomocí vlastních čísel matice lineárního autonomního systému. Podobně pracujeme i s nelineárními systémy, které umíme linearizovat pomocí Jacobiho matice.

"""
