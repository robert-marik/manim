from manim import *
from scipy.integrate import solve_ivp  # řešení diferenciálních rovnic
import colorsys
import random
import os
from manim_editor import PresentationSectionType

config.max_files_cached = 200
random.seed(10)

AnimationRuntime = 1.5
WaitTime = 2
obrazek = os.path.join("icons","mouse")

def rgb2hex(a):
    r,g,b = a 
    return "#{:02x}{:02x}{:02x}".format(int(255*r),int(255*g),int(255*b))

def hex2rgb(hexcode):
    return tuple(map(ord,hexcode[1:].decode('hex')))

def value2hex(value):
    """
    The function converts value from the interval from 0 to 1 into a color.
    """
    #print("value2hex ",value)
    return rgb2hex(colorsys.hsv_to_rgb(0.99*value*0.75, 0.95, 0.95))

class Intro(Scene):

    def construct(self):

        self.next_section("Nadpis")

        title = Title(r"Modelování populací logistickou rovnicí")
        autor = VGroup(Tex("Robert Mařík"),Tex("Mendel University")).arrange(DOWN).next_to(title,DOWN)
        self.play(GrowFromCenter(title))
        self.play(GrowFromCenter(autor[0]))
        self.play(GrowFromCenter(autor[1]))
        self.wait()

        # func = lambda pos: ((pos[1]+1)*(2-(pos[1]+1)) )  * UP + RIGHT
        # stream_lines = StreamLines(func, stroke_width=1, max_anchors_per_line=30, 
        #     y_range=[-1,1.2,.1],
        #     x_range=[-3,3,.1], 
        #     padding=.5,
        #     opacity=1)

        # self.add(stream_lines)
        # stream_lines.start_animation(warm_up=True, flow_speed=1.5)
        # self.wait(stream_lines.virtual_time / stream_lines.flow_speed*10)


        #self.clear()

class Odvozeni(Scene):

    def construct(self):

        self.next_section("Odvozeni logisticke rovnice")

        title = Title(r"Odvození logistické rovnice").to_edge(UP)

        definice = VGroup(
            Tex(r"$\bullet$ Velikost populace označíme ",r"$y$","."),
            Tex(r"\begin{flushleft}$\bullet$ Populace se množí rychlostí úměrnou velikosti populace\\\phantom{$\bullet$ } a volné kapacitě prostředí, označené $K$.\end{flushleft}"),
            Tex(r"$\bullet$ Volná kapacita je ","rozdíl ","100\%"," a ","obsazeného procenta","."),
            Tex(r"$\bullet$ Populace je vystavena lovu konstantní intenzity ",r"$h$","."),
            Tex(r"Rychlost růstu"," je úměrná"," velikosti populace"," a volnému místu.")
            )

        definice.arrange(DOWN, aligned_edge = LEFT, buff=0.3).next_to(title,DOWN).to_edge(LEFT,buff=0.3)
        rovnice = definice[-1].shift(DOWN)


        self.play(FadeIn(title))

        for i in definice:
            self.play(FadeIn(i))
            self.wait()

        self.next_section("")
        rovnice.set_color(YELLOW)
        a1 = Tex(r"$\frac yK$").move_to(definice[2][4])
        a2 = Tex(r"$1$").move_to(definice[2][2])
        a3 = Tex(r"$\bullet$ Volná kapacita je ", r"$1-\frac yK$",".").move_to(definice[2][0],aligned_edge=LEFT)
        a4 = Tex(r"$1-\frac yK$").move_to(definice[2][3])
        a5 = Tex(r"$\displaystyle\frac{\mathrm dy}{\mathrm dt}=ry\left(1-\frac yK\right)$","${}-h$").next_to(definice[3],DOWN)
        a6 = Tex(r"$\displaystyle\frac{\mathrm dy}{\mathrm dt}$").move_to(rovnice[0]).set_color(YELLOW)
        a7 = Tex(r"$\displaystyle\left(1-\frac{y}{K}\right)$").move_to(rovnice[3]).set_color(YELLOW)
        a8 = Tex(r"$=r$").move_to(rovnice[1]).set_color(YELLOW)
        a9 = Tex(r"$y$").move_to(rovnice[2]).set_color(YELLOW)
        
        for i in [
            ReplacementTransform(definice[2][4],a1),
            ReplacementTransform(definice[2][2],a2),
            ReplacementTransform(VGroup(a1,a2,definice[2][1],definice[2][2],definice[2][3],definice[2][4]),a4),
            ReplacementTransform(VGroup(a1,a2,definice[2],a4),a3),
            ReplacementTransform(VGroup(rovnice[2],definice[0].copy()),a9),
            ReplacementTransform(rovnice[0],a6),
            ReplacementTransform(VGroup(rovnice[3],a3[1].copy()),a7),
            ReplacementTransform(rovnice[1],a8),
            ReplacementTransform(VGroup(rovnice,a6,a7,a8,a9),a5[0]),
            ReplacementTransform(definice[3][1].copy(),a5[1])
        ]:
            self.play(i, run_time = 3) 
            self.wait()
        self.wait()

class Simulace(Scene):

    def construct(self):

        self.next_section("Bez lovu")
        self.portrety()
        self.wait()

        self.next_section("Opatrny lov")
        self.clear()
        self.portrety(h=0.19, IC=0.35, wait_duration=0.5)
        self.wait()

        self.next_section("Intenzivni lov")
        self.clear()
        self.portrety(h=0.3, IC=0.4, max_step_IC=0.01, wait_duration=0.5)
        self.wait()

    def portrety(self, h=0, IC=0.1, max_step_IC=0.05, wait_duration=1):

        tmin = 0
        tmax = 10
        ymin = -0.2
        ymax = 1.3
        dymin = -0.5
        dymax = 0.5
        t = np.linspace(tmin,tmax,200)
        r = 1
        K = 1

        text = Tex(r"Časový vývoj").scale(1.5).scale(0.5)
        ax = Axes(                    
            x_range=[tmin-1, tmax, 100],
            y_range=[ymin, ymax, 100],                    
            tips=True,                    
            axis_config={"include_numbers": False},
            ).scale(0.5)
        
        axt = VGroup(text,ax).arrange(DOWN)
        axt.to_corner(UL, buff=0.5)

        ax2 = Axes(                    
            x_range=[ymin, ymax, K],
            y_range=[dymin,dymax, 10],                    
            tips=True,                    
            axis_config={"include_numbers": False},
            )

        if h==0:
            nadpis = r"Fázový portrét bez lovu, $h=0$"
            y_points = [0,0,K,ymax]
        elif h<(r*K)/4:
            nadpis = r"Fázový portrét s malým lovem"
            y_points = [0, K*(1-np.sqrt(1-4*h/(r*K)))/2, K*(1+np.sqrt(1-4*h/(r*K)))/2,ymax]
        else:
            nadpis = r"Fázový portrét s velkým lovem"
            y_points = [0,0,0,ymax]

        text2 = Tex(nadpis).scale(1.5)
        axt2 = VGroup(text2,ax2).arrange(DOWN, buff=1.5).to_edge(UP)

        rovnice = MathTex(r"\displaystyle \frac{\mathrm dy}{\mathrm dt}=ry\left(1-\frac yK\right)-h").scale(1.5).set_color(YELLOW).next_to(text2,DOWN,aligned_edge=RIGHT, buff=0.4)
        rovnice.shift(RIGHT)
        axt2.add(rovnice)


        labels = []
        labels += [MathTex("K").scale(1.5).scale(0.5).next_to(ax.c2p(0,K,0), LEFT, buff=0.1)]       
        labels += [MathTex("t").scale(1.5).scale(0.5).next_to(ax.c2p(tmax,0,0), RIGHT, buff=0.2)]       
        labels += [MathTex("y").scale(1.5).scale(0.5).next_to(ax.c2p(0,ymax,0), UP, buff=0.2)]       

        labels2= []
        labels2 += [MathTex("K").scale(1.5).next_to(ax2.c2p(K,0,0), DOWN, buff=0.2)]
        labels2 += [MathTex("y").scale(1.5).next_to(ax2.c2p(ymax,0,0), RIGHT, buff=0.1)]       
        labels2 += [MathTex(r"\textstyle\frac{\mathrm dy}{\mathrm dt}").scale(1.5).next_to(ax2.c2p(0,dymax,0), UP, buff=0.1)]

        def rustova_funkce(x):
            return(r*x*(1-x/K)-h)


        rust = VGroup(
            ax2.plot(rustova_funkce, x_range=(y_points[0], y_points[1], 0.001), stroke_width=8).set_color(RED),
            ax2.plot(rustova_funkce, x_range=(y_points[1], y_points[2], 0.01), stroke_width=8).set_color(BLUE),
            ax2.plot(rustova_funkce, x_range=(y_points[2], y_points[3], 0.01), stroke_width=8).set_color(RED),
        )

        self.add(axt2,*labels2)
        self.wait()
        self.add(rust)
        self.wait()
        self.next_section("")
        self.play(VGroup(axt2,*labels2,rust).animate.scale(0.5).to_corner(UR))

        sp = ax.plot_line_graph([tmin,tmax],[K,K],add_vertex_dots=False).set_color(GREEN)

        self.play(FadeIn(axt,sp,*labels))

        increase = []
        increase += [ax2.plot_line_graph([y_points[1],y_points[2]],[0,0],add_vertex_dots=False, stroke_width=8).set_color(BLUE)]
        increase += [ax.plot_line_graph([0,0],[y_points[1],y_points[2]],add_vertex_dots=False, stroke_width=8).set_color(BLUE)]

        decrease = []
        decrease += [ax2.plot_line_graph([y_points[0],y_points[1]],[0,0],add_vertex_dots=False, stroke_width=8).set_color(RED)]
        decrease += [ax.plot_line_graph([0,0],[y_points[0],y_points[1]],add_vertex_dots=False, stroke_width=8).set_color(RED)]
        decrease += [ax2.plot_line_graph([y_points[2],y_points[3]],[0,0],add_vertex_dots=False, stroke_width=8).set_color(RED)]
        decrease += [ax.plot_line_graph([0,0],[y_points[2],y_points[3]],add_vertex_dots=False, stroke_width=8).set_color(RED)]

        portrait_arrows = VGroup()
        division = np.linspace(0,ymax,15)
        delta = division[1]-division[0]
        for i in range(len(division)-1):
            if rustova_funkce(division[i])*rustova_funkce(division[i+1])<=0:
                continue
            if rustova_funkce(division[i])>0:
                portrait_arrows.add(Arrow(start=ax2.c2p(division[i],0,0),end=ax2.c2p(division[i+1],0,0),stroke_width=10, buff=0.05,
                    max_stroke_width_to_length_ratio=15, max_tip_length_to_length_ratio=0.6)
                    .set_color(BLUE)
                    .shift(0.1*DOWN))
            else:
                portrait_arrows.add(Arrow(end=ax2.c2p(division[i],0,0),start=ax2.c2p(division[i+1],0,0),stroke_width =10, buff=0.05,
                max_stroke_width_to_length_ratio=15, max_tip_length_to_length_ratio=0.6)
                .set_color(RED)
                .shift(0.1*UP))

        transforms1 = [
            ReplacementTransform(rust[0].copy(),decrease[0]),
            ReplacementTransform(rust[1].copy(),increase[0]),
            ReplacementTransform(rust[2].copy(),decrease[2]),
            FadeIn(portrait_arrows)
        ]

        transforms2 = [
            ReplacementTransform(decrease[0],decrease[1]),
            ReplacementTransform(increase[0],increase[1]),
            ReplacementTransform(decrease[2],decrease[3])
        ]

        self.play(AnimationGroup(*transforms1, lag_ratio=0.2))
        self.play(AnimationGroup(*transforms2, lag_ratio=0.2))
        self.wait()

        self.next_section("")
        # Solve IVP
        def event(x, y):
            return y

        event.terminal = True    

        sol = [solve_ivp(lambda t, x: r*x*(1-x/K)-h, [tmin,tmax], [i], t_eval=t, events=[event], max_step=0.1) for i in np.linspace(0.05,1.5,20)]
        solIC = solve_ivp(lambda t, x: r*x*(1-x/K)-h, [tmin,tmax], [IC], t_eval=t, events=[event], max_step=max_step_IC )

        s = solIC
        x = s.t
        y = s.y[0]
        if len(x)<len(t):
            x = np.append(x,x[-1])
            y = np.append(y,0)
        #print(y)

        # Increasing and decreasing solutions are drawn with different colors
        def n2c(number):
            if number > y_points[1] and number < y_points[2]:
                return(YELLOW)
            else:
                return(WHITE)    

        cs = [n2c(s.y[0][0]) for s in sol]
        p = [ax.plot_line_graph(s.t,s.y[0],add_vertex_dots=False,stroke_width=2).set_color(c) for s,c in zip(sol,cs)]

        self.play(AnimationGroup(
            *[Create(_) for _ in p],
        lag_ratio=0.2))

        self.next_section("")
        mouse= ImageMobject(obrazek).scale_to_fit_width(.8).set_color(WHITE).to_corner(DL)

        ax3xmax=24.5
        ax3ymax=5.5
        ax3 = Axes(                    
            x_range=[0, ax3xmax, 10],
            y_range=[0, ax3ymax, 1],                    
            y_length=2,
            tips=False,                    
            axis_config={"include_numbers": False},
            ).to_edge(DOWN, buff=1.5)
        
        pocet = 10
        mouses = Group(*[mouse.copy() for i in range(pocet)]).arrange().set_color(GRAY).to_edge(DOWN)

        self.add(*mouses)

        poloha = ValueTracker(1)

        def barva(procento,i,j):
            pocet = 6*25
            if procento*pocet>i*6+j+1:
                barva = "#FFA500"
            else:
                barva = GRAY
            #print(procento,pocet*procento,i,j,i*6+j+1,barva)
            return(barva)

        def barva(procento,srovnani):
            if procento*100>srovnani:
                barva = "#FFA500"
            else:
                barva = GRAY
            #print(procento,pocet*procento,i,j,i*6+j+1,barva)
            return(barva)

        mouss = [mouse.copy().scale(0.6).move_to(ax3.c2p(i,j,0)).set_color(RED) for i in range(25) for j in range(6)]
        
        self.add(poloha)

        H = 1.5
        W = 8
        r0 = Rectangle(width=W,height=H, fill_opacity=0.5).set_color(GRAY).to_edge(DOWN,buff=1.5)
        self.add(r0)
        r1 = always_redraw(lambda: Rectangle(width=W*y[int(np.round(poloha.get_value()/K))],height=H, fill_opacity=0.5)
            .set_color("#FFA500").move_to(r0,aligned_edge=DL))
        self.add(r1)
        
        text_nosna_kapacita = Tex(" Obsazenost: ").move_to(r0).shift(LEFT)
        self.add(text_nosna_kapacita)
        value_nosna_kapacita = always_redraw(
            lambda: DecimalNumber(num_decimal_places=1)
            .set_value(100*y[int(np.round(poloha.get_value()/K))])
            .next_to(text_nosna_kapacita, RIGHT, buff=0.5)
        )
        text_procenta = Tex(r"\%\,$K$").next_to(value_nosna_kapacita)
        self.add(value_nosna_kapacita,text_procenta)

        pIC = always_redraw(lambda: ax
            .plot_line_graph(x[:int(np.round(poloha.get_value()))],y[:int(np.round(poloha.get_value()))],
                add_vertex_dots=False,stroke_width=2)
            .set_color("#FFA500"))
        mouse_curve = always_redraw(lambda: mouse.copy().scale(0.5).set_color("#FFA500")
            .move_to(ax.c2p(x[int(np.round(poloha.get_value()))],y[int(np.round(poloha.get_value()))],0)))
        mouse_phase = always_redraw(lambda: mouse.copy().scale(0.5).set_color("#FFA500")
            .move_to(ax2.c2p(y[int(np.round(poloha.get_value()))],rustova_funkce(y[int(np.round(poloha.get_value()))]),0)))
            
        self.add(mouse_curve,mouse_phase,pIC)
        self.wait()

        self.next_section("")
        self.play(poloha.animate.set_value(len(x)-1), run_time=6, rate_func=linear)
        self.wait()

komentar = """

Dobrý den, v tomto videu si ukážeme, jak matematika dokáže modelovat růst
populací živočišných či rostlinných druhů. Ukážeme si odvození logistické
rovnice, která je základním východiskem pro modelování populací. Ukážeme si
chování řešení této rovnice. Také rovnici doplníme o lov konstantní intenzity a
zjistíme, jaký má tento lov vliv na schopnost populace přežít.

Logistická rovnice je rovnice založená na představě populace žijící v lokalitě s
omezenou nosnou kapacitou. Dynamika růstu populace je pomalá, pokud je populace
malá nebo pokud je v lokalitě již plno. Využijeme nejjednodušší závislost a to
přímou úměrnost. V následujícím už budeme přesnější.

==========================================

Velikost populace budeme sledovat v proměnné y. Velikost populace roste
rychlostí úměrnou současně velikosti populace a současně volné kapacitě
prostředí. Volnou kapacitu prostředí budeme chápat jako doplněk obsazené
kapacity prostředí do sta procent. A na závěr do modelu zahrneme možnost lovu
konstantní intenzitou h.

Základní předpoklad definující náš model je, že rychlost růstu je úměrná
současně velikosti populace a volnému místu v prostředí. Obsazené procento je
podílem velikosti populace a nosné kapacity, tedy y/K. Volná kapacita je doplněk
obsazeného procenta do sta procent, tedy 1-y/K.

Velikost populace dosadíme do naší slovní formulace modelu. Rychlost růstu je
derivace velikosti populace podle času. Volné místo máme vyjádřeno z
předchozího. Mezi navzájem úměrnými veličinami je matematicky vztah
představovaný násobením konstantou. 

Takto získaná rovnice se nazývá logistická rovnice a je to základní rovnice pro
modelování populací. Modifikovat ji nebývá težké, například omezení dynamiky
vlivem lovu s konstantní intenzitou je jenom přidání člene, který příslušným
způsobem sníží pravou stranu.

=============================================

Numerický model spustíme nejprve bez lovu, tedy s nulovou hodnotou h. Pravá
strana rovnice je parabola a po jejím nakreslení vidíme, kdy je parabola nad
osou a kdy je pod osou. Takto vidíme, kdy populace roste a kdy klesá. Modrá část
odpovídá hodnotám velikosti populace, kdy populace roste. Červená část hodnotám
velikosti populace, kdy velikost klesá. To je v případě, že velikost populace je
nad nosnou kapacitou prostředí. Stacionární bod na rozhraní modré a červené
křivky je stabilní, protože parabola protíné v bodě K vodorovnou osu jako
klesající funkce. Z tohoto grafu je snadné poznat, že z jakéhokoliv nenulového
výchozího stavu se velikost populace po čase ustálí na hodnotě nosné kapacity
prostředí.

Pokud chceme sledovat časový vývoj, tedy třeba za jak dlouho se budeme od nosné
kapacity prostředí lišit o méně než deset procent, musíme najít řešení rovnice
jako funkci času. To zařídíme použitím numerické simulace. Knihovny pro řešení
diferenciálních rovnic jsou dostupné asi v každém skriptovacím jazyce a v
případech, jako je tento, zpravidla stačí vzít vzorový příklad z helpu a
modifikovat pro své potřeby. Křivky získané pro různé počáteční podmínky
potvrzují, že se velikost populace ustálí na hodnotě K. Třeba myši jsou takzvaní
r-stratégové, mají vysokou hodnotu konstanty r a k nosné kapacitě prostředí se
namnoží poměrně rychle.

Pro zvolenou počáteční podmínku můžeme sledovat postupný časový vývoj, můžeme
sledovat polohu odpovídajícího bodu ve fázovém diagramu anebo sledovat, jak se
postupně plní nosná kapacita prostředí. Obsazenost dosáhne sta procent. 

Pokud do modelu zapojíme i lov, parabola ve fázovém portrétu se posune směrem
dolů o hodnotu h. Pokud je h malé, zůstane kousek paraboly nad vodorovnou osou.
Nalevo se objeví červená část signalizující pokles, ale od určité hranice
rovnice předpovídá růst. Jsou zde dva kladné stacionární body, jeden nestabilní
a jeden stabilní. Po simulaci časového vývoje pro různé počáteční podmínky
vidíme, že pokud křivka nezačne moc nízko, populace se s lovem dokáže vyrovnat a
hodnoty se ustálí u stabilního stacionárního bodu. Ten je sice pod nosnou
kapacitou prostředí, ale populace nezanikne. Po simulaci s oranžovou křivkou
vidíme ustálení se na hodnotě okolo tří čtvrtin nosné kapacity prostředí. Pokud
by simulace začala nízko, pod nestabilním stacionárním bodem, populace vymře.

Třetí simulace je s intenzivním lovem. Konstanta h je tak velká, že posune celou
parabolu pod osu x a parabola je tedy celá záporná, celá červená. To je
ekologický průšvih. Velikost populace stále klesá a po čase populace s jistotou
vymře. V praxi naštěstí zpravidla k vymření nedojde, ale omezí se nebo zakáže
lov, což nás vrací k prvnímu případu.

Uvedený model je velice jednoduchý. V praxi totiž nebývají k dispozici konstanty
do uvažované rovnice. Také se nestává, že by populace žila v lokalitě sama. I
tak se však jedná o užitečnou rovnici, umožňujících definovat bezepečnou hranici
pro využívání přírodních zdrojů. V praxi se sice kvůli tomu používají o něco
složitější modely, než je model, který jsme si představili, ale snad u všech
modelů používaných v matematické biologii je logistická rovnice základnám
stavebním kamenem. Věřím, že teď už rozumíme tomu, proč se tato rovnice v
modelech biologických systémů vyskytuje, co vyjadřuje a jak se modely s touto
rovnicí chovají.

"""