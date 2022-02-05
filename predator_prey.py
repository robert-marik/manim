from operator import eq
from typing_extensions import runtime
from manim import *
import colorsys
import random

config.max_files_cached = 200

import numpy as np
from sqlalchemy import null
from common_definitions import *
import os
from scipy.integrate import solve_ivp  # řešení diferenciálních rovnic
np.random.seed(0)
random.seed(0)

# https://scipy-cookbook.readthedocs.io/items/LoktaVolterraTutorial.html
# Definition of parameters
a = 1.
b = 0.1
c = 1.5
d = 0.75*b
higher_a = 1.5
def dX_dt(X, t=0, a=a):
    """ Return the growth rate of fox and rabbit populations. """
    return np.array([ a*X[0] -   b*X[0]*X[1] ,
                  -c*X[1] + d*X[0]*X[1] ])

X_f0 = np.array([     0. ,  0.])
X_f1 = np.array([ c/(d), a/b])
X_f1_higher_a = np.array([ c/(d), higher_a/b])

tmin = 0
tmax = 16.6 # maximum for time on graph
ymax = 60 # maximum on y axis´for graphs in time
tnumber = 1000
max_step_IC = tmax/tnumber*2
t = np.linspace(tmin, tmax,  tnumber)              # time

curves = {}
curves_higher_a = {}
number_of_curves = 9
for i in range(1,number_of_curves):
    X0 = np.array([60+i/number_of_curves*(-60+c/(d)), a/b]) 
    curves[i] = solve_ivp(
        lambda t, X: dX_dt(X,t), 
        [tmin,tmax], [*X0], t_eval=t, max_step=max_step_IC 
    ).y
    curves_higher_a[i] = solve_ivp(
        lambda t, X: dX_dt(X,t,a=higher_a), 
        [tmin,tmax], [*X0], t_eval=t, max_step=max_step_IC 
    ).y
X = curves.pop(4)
X_higher_a = curves_higher_a.pop(4)

bunny = os.path.join("icons","bunny_black")
fox = os.path.join("icons","fox-sitting")
myaxis_config={'tips':False}

my_wait_time = 5

class Intro(Scene):

    def construct(self):
        title = Title(r"Model dravce a kořisti")
        autor = VGroup(Tex("Robert Mařík"),Tex("Mendel University")).arrange(DOWN).next_to(title,DOWN)
        self.play(GrowFromCenter(title))
        self.play(GrowFromCenter(autor[0]))
        self.play(GrowFromCenter(autor[1]))
        self.wait(4)

        fox_img = ImageMobject(fox)
        bunny_img = ImageMobject(bunny)
        imgs = Group(
            fox_img.scale_to_fit_width(1.5).set_color(RED),
            bunny_img.scale_to_fit_width(1).set_color(WHITE)
        ).arrange(buff=1)
        self.play(FadeIn(imgs), run_time=10)
        self.wait(10)

class Odvozeni(Scene):

    def construct(self):
        
        assumptions = VGroup(*[Tex(r"\begin{minipage}{12cm}$\bullet$ "+_+r"\end{minipage}").scale(0.8) for _ in  [
                r"Rychlost růstu populace kořisti je úměrná velikosti její populace.",
                r"Rychlost s jakou dravec hubí kořist je úměrná velikosti obou populací.",
                r"Rychlost poklesu populace dravce je úměrná velikosti jeho populace.",
                r"Rychlost s jakou přístup ke kořisti posiluje populaci dravce je úměrná velikosti obou populací.",
            ]]
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(UP)

        equations = VGroup(
            MathTex(r"\displaystyle\frac{\mathrm dx}{\mathrm dt}","{}=ax","{}-bxy"),
            MathTex(r"\displaystyle\frac{\mathrm dy}{\mathrm dt}{}","{}=-cy","{}+dxy").set_color(RED)
        ).arrange(DOWN, aligned_edge=LEFT,buff=1)
        equations.next_to(assumptions,DOWN)

        fox_img = ImageMobject(fox)
        bunny_img = ImageMobject(bunny)
        imgs = Group(
            bunny_img.scale_to_fit_width(1).set_color(WHITE),
            fox_img.scale_to_fit_width(1.5).set_color(RED)
        ).arrange(DOWN,buff=0.5)
        imgs.next_to(equations,LEFT, buff=1)

        self.play(FadeIn(imgs[0]))

        count = 0
        for i,j in [
            [assumptions[0],equations[0][:2]],
            [assumptions[1],equations[0][2]],
            [assumptions[2],equations[1][:2]],
            [assumptions[3],equations[1][2]],
            ]:
            if count == 1:
                self.play(FadeIn(imgs[1]))
            self.play(FadeIn(i,j))
            r1 = SurroundingRectangle(i)
            r2 = SurroundingRectangle(j)
            count += 1
            self.play(
                AnimationGroup(
                    Create(r1),Create(r2),
                    lag_ratio=.2
                ), run_time=2
            ) 
            self.wait(my_wait_time)
            self.play(
                AnimationGroup(
                    FadeOut(r1),FadeOut(r2),
                    lag_ratio=.2
                ), run_time=2
            ) 
            self.wait(my_wait_time)

        self.wait(5)

class PhasePortrait(Scene):
    def construct(self):

        equations = VGroup(
            MathTex(r"\displaystyle\frac{\mathrm dx}{\mathrm dt}","{}={}","ax-bxy"),
            MathTex(r"\displaystyle\frac{\mathrm dy}{\mathrm dt}{}","{}={}","-cy+dxy",             
               background_stroke_width=2).set_color(RED)
        ).arrange(DOWN, aligned_edge=LEFT).set_z_index(10)
        equations.to_corner(UL)
        self.play(AnimationGroup(*[GrowFromCenter(_) for _ in equations], lag_ratio=0.7))
        rh_sides = VGroup(equations[0][2], equations[1][2])

        phase_portarit = Group()
        axes = Axes(
            x_range=[0,60,1e6],
            y_range=[0,40,1e6],
            x_length=6,
            y_length=4, 
            **myaxis_config
        )
        axes.y_axis.set_color(RED).set(stroke_width=6)
        axes.x_axis.set(stroke_width=6)
        phase_portarit.add(axes)
        stationary_point = Dot(axes.c2p(*X_f1)).set_z_index(2)
        phase_portarit.add(stationary_point)

        fox_img = ImageMobject(fox)
        fox_img.scale_to_fit_width(1.5).set_color(RED).next_to(axes.y_axis, LEFT)
        fox_img.set_z_index(-10)
        bunny_img = ImageMobject(bunny)
        bunny_img.scale_to_fit_width(0.8).set_color(WHITE)
        bunny_img.next_to(axes.x_axis,RIGHT, buff=0)
        bunny_img.set_z_index(-10)
        phase_portarit.add(fox_img,bunny_img)

        phase_portarit.scale(1.5)
        phase_portarit.to_corner(DR)

        #self.add(phase_portarit)
        self.play(Create(axes.x_axis), SpinInFromNothing(bunny_img, angle=4 * PI))
        self.wait(my_wait_time)
        self.play(Create(axes.y_axis), SpinInFromNothing(fox_img, angle=4 * PI))
        self.wait(my_wait_time)

        phase_portarit_arrows = VGroup()
        delka = 3

        data = []        
        for i in np.linspace(*axes.x_range[:2],12):
            for j in np.linspace(*axes.y_range[:2],12):
                if i*j == 0:
                    continue
                start = np.array([i,j])
                rhs = dX_dt([i,j])
                norm = np.sqrt(rhs[0]**2+rhs[1]**2)
                end = start + rhs/norm*delka
                data += [[start,end,norm]]

        maximum = np.max([i[2] for i in data])
        for i in data:                                
            phase_portarit_arrows.add(
                Arrow(
                    start=axes.c2p(*i[0],0), 
                    end=axes.c2p(*i[1],0), 
                    buff=0, 
                    max_stroke_width_to_length_ratio = 20, 
                    max_tip_length_to_length_ratio = 0.4,
                    color = temperature_to_color(i[2]*5, min_temp=0, max_temp=maximum),
                    stroke_width=10,
                )
            )

        x,y = X

        ini = 30
        bod = Dot(axes.coords_to_point(x[ini], y[ini]))
        bod.set_color(YELLOW)
        scale = 0.3
        zacatek = np.array([x[ini],y[ini]])
        rhs = dX_dt(zacatek)
        norma = np.sqrt(rhs[0]**2+rhs[1]**2)
        posun = rhs/norma*delka
        konec = zacatek + posun
        sipka = Arrow(
                    start=axes.c2p(*zacatek,0), 
                    end=axes.c2p(*konec,0), 
                    buff=0, 
                    max_stroke_width_to_length_ratio = 20, 
                    max_tip_length_to_length_ratio = 0.4,
                    color = temperature_to_color(norma*5, min_temp=0, max_temp=maximum),
                    stroke_width=10,
                )

        self.play(FadeIn(bod))
        self.wait(my_wait_time)
        rectangle = SurroundingRectangle(rh_sides)
        self.play(FadeIn(rectangle))
        self.wait(my_wait_time)
        self.play(FadeIn(sipka))
        self.wait(my_wait_time)

        phase_portarit_arrows.shuffle_submobjects()
        self.play(AnimationGroup(*[
            Create(_) for _ in phase_portarit_arrows
            ], lag_ratio=0.05), run_time=4)
        self.wait(my_wait_time)
        self.play(FadeOut(rectangle))
        self.wait(my_wait_time)
        
        self.play(AnimationGroup(
            *[i.animate.set_fill(opacity = 0.5).set_stroke(opacity=0.5) for i in VGroup(*phase_portarit_arrows,sipka)]
            ))

        graph = axes.plot_line_graph(*X, add_vertex_dots=False)
        graph.set_stroke(width=3)
        # self.play(Create(graph))

        # self.wait(my_wait_time)

        time = ValueTracker(ini)
        
        axes2 = Axes(
            x_range=[0,tmax,1e6],
            y_range=[0,60,1e6],
            x_length=8,
            y_length=2,
            **myaxis_config
        )#.add_background_rectangle(buff=0.5)
        labels2 = VGroup(Tex(r"$t$").next_to(axes2.x_axis))
        graph2 = VGroup(axes2,labels2)
        graph2.to_corner(UR)

        graph_foxes = axes2.plot_line_graph(
            x_values=t, 
            y_values=X[1], 
            add_vertex_dots=False
        ).set_color(RED)
        graph_bunnies = axes2.plot_line_graph(
            x_values=t, 
            y_values=X[0], 
            add_vertex_dots=False
        ).set_color(WHITE)

        kwds = {
                'value_max' : 60, 
                'values' : [0,10,20,30,40,50,60]
                }

        draw_dot = True
        only_dot = True
        def draw_for_animation(t_index):
            watches = VGroup(
                analog_indicator(x[t_index],**kwds),
                analog_indicator(y[t_index],**kwds)
            ).arrange().to_edge(RIGHT).shift(DOWN*0.15)#.add_background_rectangle()
            
            line_marker = VGroup(
                RegularPolygon(n=3, start_angle=np.pi / 2, stroke_width=0).set_fill(
                color=WHITE,
                opacity=1,
                ).scale(0.1).move_to(axes2.coords_to_point(t[t_index], 0), UP),
                DashedLine(
                    start = axes2.coords_to_point(t[t_index], 0), 
                    end = axes2.coords_to_point(t[t_index], ymax),
                    color=WHITE)
            )
            #line_marker[1].set_color(GRAY)
            #line_marker[1].set_z_index(20)
            if draw_dot:
                dot_in_phase_space = Dot(axes.coords_to_point(x[t_index], y[t_index]))
                dot_in_phase_space.set_color(YELLOW)
            else:
                dot_in_phase_space = VGroup()                
            if only_dot:
                watches.set_opacity(0)
                line_marker.set_opacity(0)
            else:
                watches.set_opacity(1)
                line_marker.set_opacity(1)
            return(VGroup(line_marker,dot_in_phase_space,watches))

        report = always_redraw(lambda: draw_for_animation(int(time.get_value())) )
        self.add(report)
        self.remove(bod)
        self.play(time.animate.set_value(tnumber-1), run_time=5, rate_func=linear)
        time.set_value(0)

        self.wait(my_wait_time)
        self.play(Create(graph))
        self.wait(my_wait_time)
        self.play(Group(
            phase_portarit,graph,phase_portarit_arrows,sipka
            ).animate.scale(1/1.5).to_edge(DL))

        self.play(GrowFromEdge(graph2, RIGHT))
        self.play(AnimationGroup(*[
            Create(_) for _ in  [graph_foxes,graph_bunnies]
        ]))

        only_dot = False

        self.wait(0.1)
        fox_img_watches = ImageMobject(fox).scale_to_fit_width(0.75).set_color(RED).next_to(report[-1][1],DOWN)
        bunny_img_watches = ImageMobject(bunny).scale_to_fit_width(.4).set_color(WHITE).next_to(report[-1][0],DOWN)
        #bunny_img_watches.shift(RIGHT)

        self.wait(0.1)
        #temp = draw_for_animation(int(time.get_value()))
        #self.play(AnimationGroup(*[SpinInFromNothing(_) for _ in temp[-1]], lag_ratio=0.05))
        #temp.set_color(BLACK).set_z_index(-10)
        #self.wait(my_wait_time)
        self.play(AnimationGroup(
            *[SpinInFromNothing(_,angle=3*PI) for _ in [fox_img_watches, bunny_img_watches]]
            ),lag_ratio=0.3
            )
        self.wait(my_wait_time)

        for i in range(5):
            self.play(time.animate.set_value(tnumber-1), run_time=5, rate_func=linear)
            time.set_value(0)
        
        self.wait(my_wait_time)

        allcurves = VGroup(
            *[axes.plot_line_graph(*curves[i][:][:450], add_vertex_dots=False) for i in curves.keys()]
        )
        allcurves.set_stroke(color=BLUE, width=3)

        draw_dot = False
        # self.wait(0.1)
        # self.play(Create(graph))
        self.wait(my_wait_time)

        self.play(AnimationGroup(*[Create(_) for _ in allcurves],lag_ratio=0.1, run_time=3))
        self.add(stationary_point)

        self.wait(my_wait_time)

        self.play(AnimationGroup(
            *[FadeOut(_) for _ in [*axes2, labels2, *report, fox_img_watches, 
                                    bunny_img_watches, 
                                    graph_foxes,graph_bunnies, phase_portarit_arrows, sipka]
            ],
            Group(
                allcurves, phase_portarit, graph, 
            ).animate.scale(1.2).to_corner(UR, buff=.1),
            lag_ratio=0.05)
        )
        self.play(fox_img.animate.next_to(axes.y_axis, LEFT, aligned_edge=UP))

        # stability_conditions=VGroup(
        #     MathTex(r"\displaystyle\frac{\mathrm dx}{\mathrm dt}=0 \implies y=\frac ba"),
        #     MathTex(r"\displaystyle\frac{\mathrm dy}{\mathrm dt}=0 \implies x=\frac cd"),
        # ).arrange(DOWN).to_corner(UR)

        # stability_derivation = equations.copy()
        # self.play(stability_derivation.animate.next_to(stability_conditions,DOWN).set_color(WHITE))

        equations2 = VGroup(
            MathTex(r"0","{}={}","ax-bxy"),
            MathTex(r"0","{}={}","-cy+dxy")
        ).arrange(DOWN, aligned_edge=LEFT)
        equations2.next_to(equations, DOWN, buff=1)

        equations3 = VGroup(
            MathTex(r"0","{}={}","a-by"),
            MathTex(r"0","{}={}","-c+dx")
        ).arrange(DOWN, aligned_edge=LEFT)
        equations3.move_to(equations2)

        equations3a = VGroup(
            MathTex(r"-a","{}={}","-by"),
            MathTex(r"0","{}={}","-c+dx")
        ).arrange(DOWN, aligned_edge=LEFT)
        equations3a.move_to(equations2)

        equations3aa = VGroup(
            MathTex(r"a","{}={}","by"),
            MathTex(r"c","{}={}","dx")
        ).arrange(DOWN, aligned_edge=LEFT)
        equations3aa.move_to(equations2)

        equations3b = VGroup(
            MathTex(r"by","{}={}","a"),
            MathTex(r"dx","{}={}","c")
        ).arrange(DOWN, aligned_edge=LEFT)
        equations3b.move_to(equations2)

        equations4 = VGroup(
            MathTex(r"y","{}={}",r"\displaystyle\frac ab"),
            MathTex(r"x","{}={}",r"\displaystyle\frac cd")
        ).arrange(DOWN, aligned_edge=LEFT)
        equations4.move_to(equations3)

        self.play(AnimationGroup(
            FadeIn(equations2[0][0]),
            FadeIn(equations2[0][1]),
            FadeIn(equations2[1][0]),
            FadeIn(equations2[1][1])))
        self.play(AnimationGroup(
            ReplacementTransform(equations[0][2].copy(),equations2[0][2]),
            ReplacementTransform(equations[1][2].copy(),equations2[1][2]),
            lag_ratio=1
        ))
        
        self.wait(my_wait_time)

        self.play(AnimationGroup(
            *[TransformMatchingShapes(_,__) for _,__ in zip(equations2,equations3)],
            lag_ratio=1
        ))

        self.play(AnimationGroup(
            *[TransformMatchingShapes(_,__, path_arc=PI/2, run_time=1) for _,__ in zip(equations3,equations3a)],
            lag_ratio=1
        ))

        self.play(AnimationGroup(
            *[TransformMatchingShapes(_,__, path_arc=PI/2, run_time=1) for _,__ in zip(equations3a,equations3aa)],
            lag_ratio=1
        ))
        self.play(AnimationGroup(
            *[TransformMatchingShapes(_,__, path_arc=PI/2, run_time=1) for _,__ in zip(equations3aa,equations3b)],
            lag_ratio=1
        ))

        self.play(AnimationGroup(
            *[TransformMatchingShapes(_,__) for _,__ in zip(equations3b,equations4)],
            lag_ratio=1
        ))

        self.wait(my_wait_time)

        line_x = axes.get_vertical_line(stationary_point.get_center())
        line_y = axes.get_horizontal_line(stationary_point.get_center())
        label_x = MathTex("c/d").scale(.7).next_to(line_x,DOWN).set_color(RED)
        label_y = MathTex("a/b").scale(.7).next_to(line_y,LEFT)

        self.add(line_x,line_y)

        self.play(AnimationGroup(
            TransformMatchingShapes(equations4[0][2].copy(),label_y),
            TransformMatchingShapes(equations4[1][2].copy(),label_x),
            AnimationGroup(FadeToColor(equations4[0][0],RED),
            FadeToColor(equations4[1][2],RED)),
            lag_ratio=1
        ))


        self.wait(my_wait_time)
        for i in range(3):
            #self.play(Indicate(equations[0][2], scale_factor=2.5), Indicate(label_y, scale_factor=3))
            self.play(Indicate(equations4[0]))
        self.wait(my_wait_time)
        for i in range(3):
            #self.play(Indicate(equations[1][2], scale_factor=2.5), Indicate(label_x, scale_factor=3))
            self.play(Indicate(equations4[1]))
        

        self.wait(my_wait_time)

        dravec = os.path.join("icons","drava_ryba")
        korist = os.path.join("icons","ryba")

        dravec_img = ImageMobject(dravec)
        korist_img = ImageMobject(korist)
        dravec_img.set_color(RED).scale_to_fit_width(2)
        dravec_img.move_to(fox_img, aligned_edge=UP).set_z_index(-2)
        korist_img.set_color(WHITE).scale_to_fit_width(.9)
        korist_img.move_to(bunny_img, aligned_edge=LEFT).set_z_index(-2)

        self.play(FadeOut(fox_img),SpinInFromNothing(dravec_img, angle=8 * PI), runtime=3)
        self.wait(my_wait_time)
        self.play(FadeOut(bunny_img),SpinInFromNothing(korist_img, angle=8 * PI), runtime=3)
        self.wait(my_wait_time)

        graph_higher_a = axes.plot_line_graph(*X_higher_a, add_vertex_dots=False)
        allcurves_higher_a = VGroup(
            *[axes.plot_line_graph(*curves_higher_a[i][:][:450], add_vertex_dots=False) for i in curves.keys()]
        )
        allcurves_higher_a.set_stroke(color=PURPLE, width=2)
        stationary_point_higher_a = Dot(axes.c2p(*X_f1_higher_a)).set_z_index(2)
        
        allcurves.set_stroke(color=BLUE, width=3)
        allcurves_higher_a.set_stroke(color=BLUE, width=3)

        komentar = Tex(r"Zlepšení reprodukční schopnosti kořisti podpoří\\ populaci predátora. Na populaci kořisti nemá vliv.")
        komentar.to_edge(DOWN)
        self.play(FadeIn(komentar))

        self.play(
            AnimationGroup(
                FadeOut(line_x, line_y, label_x, label_y),
                ReplacementTransform(stationary_point, stationary_point_higher_a),
                *[
                    AnimationGroup(FadeOut(_),FadeIn(__)) for _,__ in zip(
                        [*allcurves[:4], graph, *allcurves[4:]],
                        [*allcurves_higher_a[:4], graph_higher_a, *allcurves_higher_a[4:]] 
                        )
                ],
                lag_ratio=.1,
                run_time=5
            )
        )


        self.wait(my_wait_time)

komentar = """

Dobrý den, vítejte u videa, ve kterém si ukážeme, jak umíme modelovat vzájemné
působení dvou populací a jak například umíme vysvětlit existenci cyklů v
přírodě.

Představíme si klasický model dravce a kořisti.

Populace kořisti, mysleme si například králíky, se může rozmnožovat.
Předpokládejme dostatek místa v životním prostředí a tedy růst úměrný velikosti
populace. To je přirozený předpoklad, protože například dvojnásobně velká
populace má dvojnásobný počet potomků a množí se proto dvojnásobnou rychlostí.

Přítomnost dravce, třeba lišek, růst populace kořisti zpomalí. Toto zpomalení
souvisí s počtem predátorů, protože více lišek uloví více králíků. Souvisí také
s množstvím kořisti, protože každé lišce se lépe loví v revíru přeplněném
králíci než tam, kde o králíka sotva zavadí. Přirozené je použít do základního
modelu nejjednodušší funkční závislost, přímou úměrnost vzhledem k oběma
populacím.

Rychlost, s jakou klesá populace predátora, je úměrná velikosti této populace.
To je opět přirozený předpoklad, protože dvojnásobek hladových lišek znamená
dvojnásobek lišek, které zemřou na nedostatek potravy. V přítomnosti potravy se
však pokles zastaví a při dostatku potravy dokonce změní v růst. Opět tento
efekt roste jak s počtem lišek, tak s počtem králíků. Opět je nepřirozenější
pro tento efekt použít nejjednodušší rostoucí funkci, přímou úměrnost vzhledem
ke každé z populací.

Takto jsme sestavili soustavu dvou rovnic. Neznámými jsou funkce popisující
velikost populace lišek a králíků. Rovnice vyjadřují, jak se aktuální počet
lišek a králíků projeví na tom, zda jejich populace rostou či vymírají a jak
rychle.

Pravé strany neobsahují čas. Jsou stejné v úterý jako ve čtvrtek, letos stejně
jako předloni. Tím je situace velice zjednodušená a chování řešení je možné
prozkoumat jednoduchými grafickými metodami.

=========================

Dvojice čísel, jako třeba počet králíků a lišek definuje bod v rovině, kde je
vodorovně množství králíků a svisle množství lišek.
 
Bod v takové rovině definuje stav s určitým počtem králíků a lišek. Pravé
strany rovnic ukážou další vývoj. Například teď máme bod celkem nahoře, tedy
hodně lišek. Ty hodně uloví. V první rovnici dominuje člen bxy a počet králíků
bude klesat. Zatím je však králíků pořád relativně dost na to, aby se lišky
uživily a množily. Proto počet lišek roste a proto si v tomto bodě nakreslíme
šipku doleva nahoru. Podobnou úvahu můžeme provést v dalších bodech roviny a
dostaneme tak směrové pole systému. Aby směrové pole vypadalo přehledně,
zkrátíme všechny šipky na stejnou délku a informaci o jejich původní délce
zachytíme barvou šipky. Červenou použijeme pro vysoké a modrou pro nízké
hodnoty.

Pokud vyjdeme z počátečního stavu, šipky ukazují, jak se budou hodnoty populací
měnit. Kterým směrem a jak rychle. Ve směrovém poli poté můžeme sledovat, jak
se bod popisující stav systému pohybuje podle šipek.

Kulička létající ve fázovém prostoru není vhodná pro statické obrázky. Proto
raději kreslíme křivku spojující jednotlivé polohy této kuličky při pohybu
fázovým prostorem. Fyzikálně se taková křivka při pohybu těles nazývá
trajektorie a stejná terminologie se přenáší i do světa autonomních systémů.

Není to jediná možnost vizualizace. Vpravo nahoře budeme sledovat grafy
ukazující velikosti populací v závislosti na čase, nebo o něco níže jenom
jednoduché indikátory velikosti obou populací. Všimněte si, že děj je
periodický a stále se opakuje maximum kořisti, následované maximem dravce. Toto
maximum dravce ale velmi rychle zdecimuje populaci kořisti a s nedostatkem
kořisti následně vymírá i populace dravce. Tím se uvolní prostor pro nový
nárůst. V tuto chvíli jsou velikosti populací na nízké úrovni. Proto jsou pravé
strany diferenciální rovnice numericky blízké nule a rychlost růstu obou
populací je sice malá, ale populace kořisti i tak doroste do svého maxima, čímž
se uzavře cyklus. Takové cykly v přírodě opravdu pozorujeme a k jedné historce
s tím související se vrátíme na konci videa.

Pro jiné počáteční podmínky dostaneme jiné trajektorie, ty vyznačíme do obrázku
modře. Všimněte si, že všechny trajektorie tohoto systému jsou cyklické. Pouze
uprostřed je jedna trajektorie, která zdegenerovala do jediného bílého bodu. To
je stacionární bod. Odpovídá situaci, kdy jsou velikosti obou populací
konstantní. Protože derivace konstantní funkce je nula, najdeme tento bod
řešením soustavy, která vznikne tak, že derivace podle času nahradíme nulou. 

Tato soustava je poměrně jednoduchá, protože první rovnici můžeme vydělit
hodnotou x a druhou rovnici hodnotou y. Tím soustava přejde na dvě samostatné
rovnice, které vyřešit je hračka.

Nadmíru zajímavé je to, že první rovnice, definující hodnotu okolo které kmitá
hodnota y, obsahuje jenom koeficienty a,b. Tedy hodnota, okolo které kmitá
populace dravce souvisí s parametry popisujícími vývoj populace kořisti. A
podobně, druhá rovnice, rovnice pro rovnovážnou polohu populace kořisti,
obsahuje výlučně parametry populace dravce.

To je překvapivé. Hodnota, okolo které kolísá velikost populace lišek souvisí
ne s porodností lišek, ale s porodností králíků. A tady už jsme slíbené
historky. Je to příběh, který stál za zrodem nové oblasti matematiky, za zrodem
matematické biologie.

Hlavními aktéry v příběhu byli mořstí predátoři, tedy dravé ryby, a jejich
kořist, sardinky. Během první světové války se snížil rybolov. Očekávatelným
efektem by bylo, že sardinek bude více. K velkému překvapení se však přemnožily
dravé ryby.

V našem modelu vidíme proč. Omezením rybolovu ubylo na intenzitě umělé
snižování populace sradinek rybolovem. V modelu se proto navýšila konstanta a.
To znamená, že se navýšil i podíl a/b a rovnovážný stav i všechny trajektorie
se posunou směrem nahoru. Velikost populace sardinek kolísá kolem původní
hodnoty, ale velikost populace dravých ryb okolo hodnoty vyšší. Pro vnějšího
pozorovatele to znamená, že zatímco sardinek je stejně jako předtím, dravé ryby
se oproti předchozím letům přemnožily. Na první pohled záhada. My však víme, že
matematický rozbor tento zdánlivý rozpor vysvětluje jako přirozené chování
našeho modelu, popisujícího interakce mezi populacemi.

Tento rozbor provedl v roce 1926 italský matematik a fyzik Vito Volterra.
Popudem byl výzkum jeho pozdějšího zetě, mořského biologa Umberta d'Ancony. Ten
si všiml, že ve válečných letech se zvýšilo procento dravých ryb v rybářských
sítích. Volterrova práce tento jev vysvětlila. Jinou cestou již dříve ke
stejným rovnicím dospěl Alfred Lotka a proto se model dnes nazývá Lotkův
Volterrův model. Model je velmi flexibilní, dokáže se přizpůsobit mnoha
situacím, kdy například predátoři mají omezenou žravost, nebo kdy hraje roli
nosná kapacita prostředí.

Ukázali jsme si jednoduchý model dravce a kořisti, z jakých předpokladů je
odvozen a jak se chovají řešení tohoto modelu. Také jsme si ukázali, jak se
změna parametrů projeví ve změně chování řešení.

"""                    

# drava ryba: https://freesvg.org/trout-silhouette-vector-image
# mala ryba: https://freesvg.org/