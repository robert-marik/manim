from logging import NullHandler
from telnetlib import DO
from tkinter import CENTER
from manim import *
from common_definitions import *

T = np.loadtxt('solution_heat_1D.txt')
n = 101
nT = 11
dxT = 0.1
xmin, xmax = 0,1
dx = (xmax-xmin)/(n-1)
x_interval = np.linspace(xmin,xmax,n)

class HeatTransfer(Scene):
    def construct(self):

        ax2 = Axes(x_range=[0,1,2],y_range=[-1,1,2], y_length=1, x_length=12)
        ax3 = ax2.copy()
        ax4 = ax2.copy()

        def plot_rod(
                ax_, 
                x, 
                temperature_field, 
                t = 0, 
                draw_thermometers = False, 
                dx = dx, 
                numbers = True, 
                time_label = None, 
                temperature_labels = None,
                grad_limits = None
            ):
            txt0 = Tex(r"Termosnímek tyče")
            temperature = temperature_field[t]
            rod = VGroup()
            for i,j in zip(x,temperature):
                rod.add(Line(start = ax_.c2p(i-0.55*dx,0,0),end=ax_.c2p(i+0.55*dx,0,0), 
                color=temperature_to_color(j, min_temp=0, max_temp=100)
                ))
            rod.set_stroke(width=20)
            if numbers:
                if temperature_labels is None:
                    temperature_labels = temperature[::10]
                for i,j in zip(x[::10],temperature_labels):
                    rod.add(Tex(round(j,1)).scale(.85).next_to(ax_.c2p(i,0,0),DOWN))  
                    rod.add(Circle(radius=0.01).move_to(ax_.c2p(i,0,0)).set_color(WHITE))  
            dTdx = np.gradient(temperature,x)
            if grad_limits is not None:
                minimum, maximum = grad_limits
            else:
                maximum = max(dTdx)
                minimum = min(dTdx)

            scene = VGroup(txt0, rod).arrange(DOWN).to_edge(UP)
            scale = 2
            dTdx = scale * dTdx/max(abs(maximum),abs(minimum))
            T = scale * temperature/100
            txt1 = Tex(r"Teplotní profil").shift(UP)
            txt2 = Tex(r"Tok tepla").shift(DOWN)
            txt3 = Tex(r"min: $%s$, max: $%s$"%(round(-maximum),round(-minimum))).scale(.75)
            
            teplota_graf = VGroup(
                ax_.plot_line_graph(x, T, add_vertex_dots=False).set_color(WHITE),
                ax_.plot_line_graph(x, [0 for i in x], add_vertex_dots=False).set_color(GRAY).set_stroke(width=2),
                ax_.plot_line_graph(x, [2 for i in x], add_vertex_dots=False).set_color(GRAY).set_stroke(width=1)
            ).next_to(txt1,DOWN)
            gradient = VGroup(
                ax_.plot_line_graph(x, -dTdx, add_vertex_dots=False).set_color(YELLOW),
                ax_.plot_line_graph(x, [0 for i in x], add_vertex_dots=False).set_color(GRAY).set_stroke(width=2)
            ).next_to(txt2,DOWN)
            grafy = VGroup(
                txt1,teplota_graf,
                txt2, gradient
                )
            txt3.next_to(txt2)
            scene.add(grafy,txt3)
            #for j in np.linspace(0,1,11)[:-1]:
            #    rod.add(Tex(round(temperature(j+0.1)-temperature(j),1)).scale(.85).next_to(ax_.c2p(j+0.05,0,0),DOWN).set_color(BLUE))
            # if draw_thermometers:
            #     for j in np.linspace(0,1,11):
            #         rod.add((round(temperature(j),1)).scale(.85).next_to(ax_.c2p(j,0,0),UP))    

            if time_label is not None:
                timetext = time_label
            else:
                timetext = str(t)
            scene.add(MathTex("t="+timetext).to_corner(UL))
            return scene

        rod = VGroup()

        numbers = True
        kwds = {}
        for t in [0,1,2,3,4,5,6,7,8,9,10,12,15,20,30,40,60,80,100,150,200,300,400,1000]:
            self.remove(rod)
            if t>800:
                numbers = True
                kwds = {'time_label':r"\infty", 'temperature_labels':[80-i*6 for i in range(11)], 'grad_limits':[-60,-60]}
            rod = plot_rod(ax2, x_interval, T, t=t, numbers=numbers, **kwds )
            self.add(rod)
            if t<5:
                self.wait()
            else:
                numbers = False
                self.wait(.5)
        
        self.wait(20)
        self.play(*[FadeOut(i) for i in self.mobjects])

class Graphs2D(Scene):
    def construct(self):

        ###### 2D graph T(t) for various x
        graphs_t = VGroup()
        tmax=200 
        trange=range(tmax)
        ax_t = Axes(x_range=[0,tmax,100 ], y_range=[0,110,20],tips=False)
        labels_tn=VGroup(Tex(r"Poloha $x$"))
        labels_tt = VGroup()
        for i,j in zip([4,20,40,60,80,96],[RED,GREEN,BLUE,WHITE,YELLOW,ORANGE]):
            graphs_t.add(ax_t.plot_line_graph(x_values=trange, y_values=T.T[i][trange], add_vertex_dots=False ).set_stroke(color=j))
            poloha = i/100
            labels_tt.add(VGroup(
                VGroup(Line(start=(0,0,0), end=(0.5,0,0), buff=0).set_stroke(color=j), Tex("$%s$"%poloha)).arrange(RIGHT)
            ))
        l_t=ax_t.get_axis_labels(x_label='t', y_label='T(t)')
        labels_tt.arrange_in_grid(rows=2,cell_alignment=LEFT)
        labels_t=VGroup(labels_tn, labels_tt).arrange(DOWN, aligned_edge=LEFT).add_background_rectangle().to_corner(UR)
        self.add(ax_t,graphs_t,labels_t,l_t) 
        self.wait()        
        self.play(*[FadeOut(i) for i in self.mobjects])

        ### 2D graph T(x) for various t
        graphs = VGroup()
        ax = Axes(x_range=[0,1.05,1], y_range=[0,110,20],tips=False)
        labels=VGroup()
        for i,j in zip([0,1,2,10,20,40,80,1000],[RED,GREEN,BLUE,WHITE,YELLOW,ORANGE,PURPLE,PINK]):
            graphs.add(ax.plot_line_graph(x_values=x_interval, y_values=T[i], add_vertex_dots=False ).set_stroke(color=j))
            labels.add(
                VGroup(
                    Line(start=(0,0,0), end=(0.5,0,0), buff=0).set_stroke(color=j), 
                    Tex("$%s$"%i)
                ).arrange(RIGHT)
                )
        labels.arrange_in_grid(rows=2, cell_alignment=LEFT)
        labels = VGroup(Tex(r"Čas"),labels).arrange(DOWN, aligned_edge=LEFT).to_corner(UR)
        l=ax.get_axis_labels(x_label='x', y_label='T(x)')
        #labels.arrange(DOWN, aligned_edge=LEFT).to_corner(UR)
        self.add(ax,graphs,labels,l)
        self.wait(20)
        self.play(*[FadeOut(i) for i in self.mobjects])

class Graphs3D(ThreeDScene):
    def construct(self):
        
        ### 2D graph T(x) for various t
        graphs = VGroup()
        ax = ThreeDAxes(
            x_range=[-.1,1.05,1], 
            z_range=[-10,120,20], 
            y_range=[0,190,1e6],
            z_length = 4,
            y_length = 20,
            x_length = 8,
            ).scale(0.75).shift(2*RIGHT-1.05*DOWN)
        self.set_camera_orientation(phi=2*PI/5, theta=-PI/3)
        tmax = 100
        tstep = 4
        for i in range(0,tmax,tstep):
            graphs.add(
                ax.plot_line_graph(
                    x_values=x_interval, z_values=T[i], y_values=[i for j in x_interval],
                    add_vertex_dots=False 
                )
            )
        t_interval = range(tmax)
        for i in range(0,101,5):
            graphs.add(
                ax.plot_line_graph(
                    x_values=[i/100 for j in t_interval], z_values=T.T[i][t_interval], y_values=t_interval,
                    add_vertex_dots=False 
                )
            )
        graphs.set_stroke(color=WHITE, width=2)
        Tlab = Tex(r"$T(x,t)$").move_to([-5,3,0])
        xlab = Tex(r"$x$").move_to([3,-3.5,0])
        tlab = Tex(r"$t$").move_to([3.5,2.5,0])
        self.add_fixed_in_frame_mobjects(Tlab)
        self.add_fixed_in_frame_mobjects(tlab)
        self.add_fixed_in_frame_mobjects(xlab)
        #labz = ax.get_z_axis_label(Tex(r"$T(x,t)$"), direction=OUT)#.rotate(PI/2,axis=RIGHT)
        #labx = ax.get_x_axis_label(Tex(r"$x$"), direction=-50*UP)#.rotate(PI/2,axis=RIGHT)
        #laby = ax.get_y_axis_label(Tex(r"$t$"))#.rotate(PI/2,axis=RIGHT)

        self.add(ax)
        self.play(AnimationGroup(
            *[Create(i) for i in graphs],
            lag_ratio=.8
            ), run_time=15
        )
        self.wait(20)
        self.play(*[FadeOut(i) for i in self.mobjects])

class Table(Scene):
    def construct(self):

        ##### Table
        trange = [0,30,60,120,240,500,1000]
        xrange = [5,20,40,60,80,95]
        T_small = T[np.ix_(trange,xrange)]
        t0 = DecimalTable(T_small, top_left_entry=Tex(r"$T(x,t)$"),
            col_labels=[Tex(r"$x=%s$"%i) for i in [0.05,0.2,0.4,0.6,0.8,0.95]],
            row_labels=[Tex(r"$t=%s$"%i) for i in trange],
            include_outer_lines=True,
            line_config={'color':BLACK, 'stroke_width':0.1},
        ).scale(.7).to_edge(UP)
        lab = t0.get_labels()
        lab.set_color(BLUE)
        t0.get_horizontal_lines()[2].set_stroke(width=8, color=BLUE)
        self.play(Create(t0.get_labels()))
        self.play(Create(t0.get_horizontal_lines()[2]))
        self.play(
            AnimationGroup(
                *[Create(i) for i in t0.get_entries_without_labels()],
                lag_ratio=0.8
            ),
            run_time = 5
            )
        self.wait(10)



        

class Equation(Scene):

    def construct(self):
        
        def MyTex(s):
            return Tex(r"$\bullet$\quad \begin{minipage}[t]{10cm}\rightskip 0 pt plus 1 fill "+s+r"\end{minipage}")

        statements = Group(
            MyTex(r"Teplota ($T$) řídí tok tepla ($q$). Teplo teče do míst s~menší teplotou.").scale(0.8),
            MyTex(r"Tok tepla řídí teplotu. V místě, kam víc tepla přitéká, než odtéká, teplota roste. To je tam, kde tok tepla slábne.").scale(0.8),
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(UP)

        ax = Axes(
                x_range=[-1,1,10],                 
                y_range=[-1,1,10],
                x_length=10,
                y_length=3, 
                tips = False,
                x_axis_config = {}
                ).next_to(statements,DOWN)

        labels = ax.get_axis_labels(
                    MathTex(r"\frac{\partial T}{\partial x}").scale(1),
                    MathTex(r"q").scale(1), 
                )
        self.add(statements)
        self.wait(10)

        self.play(FadeOut(statements[1]), FadeIn(ax,labels))
        self.wait()

        Tr = Tex(r"Teplota doprava roste")    
        Tk = Tex(r"Teplota doprava klesá")    
        Qp = Tex(r"Teplo teče doprava")    
        Ql = Tex(r"Teplo teče doleva")    

        Kvadranty = [
            VGroup(Tr.copy(),Qp.copy()).scale(0.8).arrange(DOWN).move_to(ax.c2p(0.5,0.5,0)),
            VGroup(Tr.copy(),Ql.copy()).scale(0.8).arrange(DOWN).move_to(ax.c2p(0.5,-0.5,0)),
            VGroup(Tk.copy(),Ql.copy()).scale(0.8).arrange(DOWN).move_to(ax.c2p(-0.5,-0.5,0)),
            VGroup(Tk.copy(),Qp.copy()).scale(0.8).arrange(DOWN).move_to(ax.c2p(-0.5,0.5,0)),
            ]

        self.wait(5)
        self.add(Kvadranty[0][0],Kvadranty[1][0])
        self.wait(5)
        self.add(Kvadranty[2][0],Kvadranty[3][0])
        self.wait(5)
        self.add(Kvadranty[0][1],Kvadranty[3][1])
        self.wait(5)
        self.add(Kvadranty[2][1],Kvadranty[1][1])
        self.wait(5)
        for i in [0,2]:
            Kvadranty[i].set_color(RED)
        self.wait(5)
        self.play(FadeOut(*[Kvadranty[i] for  i in [0,2]]))
        self.wait(10)
        center = Dot(ax.c2p(0,0,0), radius=0.1)
        graf = ax.plot(lambda x:-np.arctan(x*5)/2, x_range=[-1,1,0.1])
        self.add(center)
        self.wait(10)
        self.play(ReplacementTransform(
            VGroup(Kvadranty[1],Kvadranty[3],center),
            graf)
            )
        self.wait(10)

        lingraf = ax.plot(lambda x:-(x*5)/2, x_range=[-.2,.2,0.1]).set_color(YELLOW)
        self.play(FadeIn (lingraf))
        self.play(FadeOut(graf))
        self.wait(10)

        FourierI = MathTex(r" = - k").next_to(labels[1])
        FourierIa = MathTex(r"\frac{\partial T}{\partial x}").next_to(FourierI)
        self.play(FadeIn(FourierI))
        kopie = labels[1].copy()
        self.play(ReplacementTransform(labels[0].copy(),FourierIa))
        self.wait(10)
        self.play(*[FadeOut(i) for i in self.mobjects])


        statements[1].to_edge(UP)
        self.play(FadeIn(statements[1]))
        self.wait(5)

        def trubka(vlevo=2, vpravo=7, scale=.2):
            output = VGroup()
            obdelnik = Rectangle(height=0.5, width=1)
            sipka_vpravo=Arrow(start=(0,0,0), end=(vpravo*scale,0,0)).next_to(obdelnik)
            sipka_vlevo=Arrow(start=(0,0,0), end=(vlevo*scale,0,0)).next_to(obdelnik,LEFT)
            cislo_vpravo = MathTex(vpravo).next_to(sipka_vpravo,UP)
            cislo_vlevo = MathTex(vlevo).next_to(sipka_vlevo,UP)
            output.add(obdelnik, sipka_vpravo, sipka_vlevo, cislo_vlevo, cislo_vpravo)
            return output

        t1 = trubka()
        t2 = trubka(vlevo = 7, vpravo=2)
        t3 = trubka(vlevo=-7, vpravo=-2)
        t4 = trubka(vlevo=-2, vpravo=-7)

        tbl = VGroup(t1,t2,t3,t4).arrange_in_grid(rows=2, buff = 1).shift(DOWN)

        large = 0.8
        text = [
            MathTex(r"q>0").next_to(t1,LEFT, buff=large),
            MathTex(r"q<0").next_to(t3,LEFT, buff=large),
            Tex(r"$q(x)$ roste\\$T(t)$ klesá").scale(0.9).next_to(t1,UP, buff=.5*large),
            Tex(r"$q(x)$ klesá\\$T(t)$ roste").scale(0.9).next_to(t2,UP, buff=.5*large),
            ]
   
        col1 = [t2,t4]
        col2 = [t1,t3]

        self.add(tbl,text[0],text[1])
        self.wait(10)

        row1 = [t1,t2,text[0]]
        row2 = [t3,t4,text[1]]

        self.play(*[Indicate(i) for i in row1])
        self.wait(5)
        self.play(*[Indicate(i) for i in row2])
        self.wait(5)
        self.play(*[Indicate(i) for i in col2])
        self.wait(5)
        for i in col2:
            i.set_color(BLUE)
        self.play(FadeIn(text[2]))
        self.wait(5)
        self.play(*[Indicate(i) for i in col1])
        self.wait(5)
        for i in col1:
            i.set_color(RED)
        self.play(FadeIn(text[3]))
        self.wait(10)


        self.play(FadeOut(tbl,*text))



        ax2 = Axes(
                x_range=[-1,1,10],                 
                y_range=[-1,1,10],
                x_length=10,
                y_length=4, 
                tips = False,
                x_axis_config = {}
                )

        labels2 = ax2.get_axis_labels(
                    MathTex(r"\frac{\partial q}{\partial x}").scale(1),
                    MathTex(r"\frac{\partial T}{\partial t}").scale(1), 
                )
        VGroup(ax2,labels2).next_to(statements[1],DOWN)

        self.add(
            ax2,
            labels2, 
            )

        Tr = Tex(r"Místo se zahřívá")    
        Tk = Tex(r"Místo se ochlazuje")    
        Qr = Tex(r"Tok tepla sílí")    
        Qk = Tex(r"Tok tepla slábne")    

        Kvadranty = [
            VGroup(Tr.copy(),Qr.copy()).scale(0.8).arrange(DOWN).move_to(ax2.c2p(0.5,0.5,0)),
            VGroup(Tk.copy(),Qr.copy()).scale(0.8).arrange(DOWN).move_to(ax2.c2p(0.5,-0.5,0)),
            VGroup(Tk.copy(),Qk.copy()).scale(0.8).arrange(DOWN).move_to(ax2.c2p(-0.5,-0.5,0)),
            VGroup(Tr.copy(),Qk.copy()).scale(0.8).arrange(DOWN).move_to(ax2.c2p(-0.5,0.5,0)),
            ]

        self.wait()
        self.add(Kvadranty[0][0],Kvadranty[1][0])
        self.wait()
        self.add(Kvadranty[2][0],Kvadranty[3][0])
        self.wait()
        self.add(Kvadranty[0][1],Kvadranty[3][1])
        self.wait()
        self.add(Kvadranty[2][1],Kvadranty[1][1])
        self.wait()
        for i in [0,2]:
            Kvadranty[i].set_color(RED)
        self.wait()
        self.play(FadeOut(*[Kvadranty[i] for  i in [0,2]]))
        self.wait()
        center = Dot(ax2.c2p(0,0,0), radius=0.1)
        graf = ax2.plot(lambda x:-np.arctan(x*5)/2, x_range=[-1,1,0.1])
        self.add(center)
        self.wait()
        self.play(ReplacementTransform(
            VGroup(Kvadranty[1],Kvadranty[3],center),
            graf)
            )
        self.wait()

        lingraf = ax2.plot(lambda x:-(x*5)/2, x_range=[-.2,.2,0.1]).set_color(YELLOW)
        self.play(FadeIn (lingraf))
        self.play(FadeOut(graf))
        self.wait()
        FourierIIa = MathTex(r"c\varrho").next_to(labels2[1],LEFT) 
        FourierIIb = MathTex(r"= -{}").next_to(labels2[1],RIGHT)
        FourierIIc = MathTex(r"\frac{\partial q}{\partial x}").next_to(FourierIIb)
        self.play(FadeIn(FourierIIb),FadeIn(FourierIIa))
        self.play(ReplacementTransform(labels2[0].copy(), FourierIIc))
        self.wait(10)
        self.play(*[FadeOut(i) for i in self.mobjects])

        self.wait(10)

class Sestaveni(Scene):
    def construct(self):

        title = Title(r"Rovnice vedení tepla").to_edge(UP)
        self.play(GrowFromCenter(title))        
        self.wait(.5)        

        Rce1 = MathTex(r"{{ \varrho c\frac{\partial T}{\partial t} }} = {{-}} { {{ \partial}} {{q}}  \over \partial x }}")
        Rce2 = MathTex(r"{{q}}={{-}}{{k}}{{ \frac{\partial T}{\partial x} }}")

        both = VGroup(Rce1,Rce2).arrange(buff=2).next_to(title,DOWN)
        indices1 = index_labels(Rce1)
        indices2 = index_labels(Rce2)

        self.add(Rce1,Rce2)
        # self.add(indices1,indices2)

        self.wait(5)
        self.play(Rce1.animate.move_to([-1,0,0]))
        self.play(Rce1[6].animate.next_to(Rce1[2]).shift(1.5*RIGHT))

        self.wait(5)
        dif = MathTex(r"\left(-k\frac{\partial T}{\partial x}\right)").move_to(Rce1[6])
        self.play(Rce2[2:].animate.move_to(dif), FadeOut(Rce1[6]), FadeOut(Rce2[:2]))
        self.play(FadeOut(Rce2[2:]),FadeIn(dif))
        self.play(*[ i.animate.shift(2*UP) for i in self.mobjects])

        self.wait()
        final = MathTex(
            r"""\varrho c\frac{\partial T}{\partial t} }} 
            =\frac{\partial }{\partial x} 
            \left(k\frac{\partial T}{\partial x}\right)
            """
            )
        final2 = MathTex(
            r"""\varrho c\frac{\partial T}{\partial t} }} 
            =k\frac{\partial^2 T}{\partial x^2} 
            """
            ).next_to(final,DOWN)

        self.play(FadeIn(final))
        self.wait(5)
        self.play(FadeIn(final2))

        self.wait(20)

komentar = """

Dobrý den, vítejte u videa, kde si ukážeme matematický popis vedení tepla. Je
to nádherné cvičení na využití funkcí více proměnných, ale také krok do světa
reálných aplikací, protože se jedná o speciální případ difuzní rovnice,
popisující téměř veškeré transportní jevy v přírodě.

Ukážeme si, jak funguje vedení tepla. Spíš si vlastně jenom detailněji popíšeme
to co zná každý z běžného života. Ukážeme si, jak matematika umí detailně
popsat proces vedení tepla a jak dokáže fyzikální principy řídící tento děj
transformovat do modelu umožňujícího dělat experimenty v počítači, takzvaně "in
silico".

Uvažujme vedení tepla v tyči. Tyč sestavíme ze tří kousků o teplotách 100, 50 a
0 stupňů a přidáme na koníc krátké kousky o teplotách osmdesát a dvacet stupňů.
Teploty osmdesát a dvace na koncích udržujeme a sledujeme, co se děje s
teplotou podél tyče.

Příroda má tendenci vyrovnávat teploty a z místa o vyšší teplotě teče teplo do
místa s nižší teplotou. Intenzita toku souvisí s teplotním spádem. Vysoký
teplotní rozdíl způsobí vysoký teplotní tok. Na začátku je teplotní rozdíl
jenom na rozhraní částí s různou teplotou. Jak se však teplo předává, reaguje
tyč na dodávání tepla navyšováním teploty a na úbytek tepla snižováním teploty.

Budeme sledovat na termosnímku tyče teplotu, v některých místech budeme
vypisovat teploty. Pro grafické znázornění si vykreslíme teplotní profil a
intenzitu toku tepla. Ten je kladný, pokud teplo teče doprava a záporný, pokud
teče doleva. Protože jsou oba grafy pod sebou, je snadné zkontrolovat, že
kladný tok je tam, kde teplota směrem doprava klesá a záporný tam, kde roste.

Protože tok se během pokusu mění příliš, měníme na dolním grafu měřítko a
vypisujeme hodnoty pro maximum a minimum. Všímejme si, jak se teploty
vyrovnávají, to snižuje intenzitu toku a nakonec teplota v tyči klesá
rovnoměrně po celé délce, což způsobí konstantní tok podél celé tyče. To
znamená, že se nikde v tyči nehromadí teplo, žádná část se již dál neohřívá ani
naopak. Jenom dodáváme teplo na udržení teplotního rozdílu mezi osmdesáti a
dvaceti stupni.

Animace není příliš šikovná na detailní informace, co se děje během našeho
pokusu. Pro vizualizaci je lepší si informace lépe vizualizovat. Například pro
různé časy zachytit průběh teploty podél tyče, nebo v různých místech sledovat
časový vývoj teploty. Můžeme dokonce mít i obojí současně ve 3D grafu, avšak to
je spíše na efekt než pro detailní zpracování. Jednodušší řešení jsou často
efektivnější, například můžeme vypsat data do tabulky a z ní potřebné vizuální
informace generovat.

"""