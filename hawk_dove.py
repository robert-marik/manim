from manim import *
from scipy.integrate import solve_ivp  # řešení diferenciálních rovnic
import colorsys
import random
import os
from manim_editor import PresentationSectionType
from common_definitions import *


from scipy.integrate import solve_ivp  # řešení diferenciálních rovnic

config.max_files_cached = 200
random.seed(10)

hawk = os.path.join("icons","hawk.png")
dove = os.path.join("icons","dove.png")

class Intro(Scene):

    def construct(self):

        self.next_section("Nadpis")

        title = Title(r"Model soupeření jedinců jestřábí a holubičí povahy")
        autor = VGroup(Tex("Robert Mařík"),Tex("Mendel University")).arrange(DOWN).next_to(title,DOWN)
        zdroj = Tex(r"Zpracováno podle knihy\\J. Kalas, Z. Pospíšil:\\Spojité modely v biologii,\\Masarykova univerzita (2001).").scale(0.75).next_to(autor,DOWN,buff=1)
        self.play(GrowFromCenter(title))
        self.play(GrowFromCenter(autor[0]))
        self.play(GrowFromCenter(autor[1]))
        self.play(GrowFromCenter(zdroj))
        self.wait()


def rhs(x,V,D):
    return (x*(1-x)*(V/2-x*D/2))

def mujTex(text):
    return Tex(r"$\bullet\quad $\begin{minipage}[t]{13cm} "+text+r" \end{minipage}").scale(0.7)


class Formulace(Scene):

    def construct(self):
        

        texty = VGroup(
            mujTex(r"Souboj dvou protikladných povah v jedné populaci. Povaha holubice a jestřába."),
            mujTex(r"Jedinci se snaží využít zdroj, který posílí jejich reprodukční schopnost (potrava nebo přístup k~hnízdění u živočichů, přístup ke světlu pro rostliny a podobně). Jejich povaha se projevuje v ochotě o tento zdroj bojovat."),
            mujTex(r"Holubičí povaha nebojuje o zdroje. Pokud se u zdroje sejdou dvě holubice, jenom jedna zdroj zkonzumuje."),
            mujTex(r"Jestřáb je bojovník. Sejde-li se u zdroje s jiným jestřábem, bojují spolu. Jenom vítěz získá zdroj."),
            mujTex(r"Sejde-li se u zdroje holubice a jestřáb, holubice ustoupí a zdroj zkonzumuje jestřáb."),
            mujTex(r"Šíření vzorce chování typu jestřáb či holubice dokážeme modelovat diferenciální rovnicí. Značí-li $x$ frekvenci jestřábů, $D$ náklady na boj a $V$ zisk ze zkonzumovaného zdroje (po vyhraném boji mezi dvěma jestřáby či bez boje v ostatních případech), je možné ukázat, že $x$ se řídí diferenciální rovnicí $$\frac{\mathrm dx}{\mathrm dt}=x(1-x)\left(\frac V2-\frac D2 x\right).$$")
        )
        texty.arrange(DOWN, aligned_edge=LEFT)
        for i in texty:
            self.play(FadeIn(i))
        self.wait()


class Simulace(Scene):

    def construct(self):

        self.next_section("Model")        
        titulek = Tex(r"Model soupeření jestřábích a holubičích povah").scale(0.8).to_edge(UP)
        titulek.add_background_rectangle()
        titulek.set_z_index(10)
        self.add(titulek)

        ax = Axes(  
            x_range=[0, 1.2, 1],
            y_range=[-.13, .13, 2],
            tips=False,
            )

        tmax = 15
        ax2 = Axes(  
            x_range=[0, tmax, 1000],
            y_range=[0, 1, 2],
            tips=False,
            )
        V=1
        D=ValueTracker(2)

        t = np.linspace(0,tmax,500)
        def integralni_krivky():
            ttemp = VGroup()
            for i in np.linspace(0.01,0.99,20):
                sol = solve_ivp(lambda t, x: rhs(x,V,D.get_value()), [t[0], t[-1]], [i], t_eval=t)
                ttemp.add(ax2.plot_line_graph(sol.t, sol.y[0], add_vertex_dots=False))  # vykreslení řešení
            return ttemp

        hawk_mob = ImageMobject(hawk).scale_to_fit_width(1.5).set_color(RED)
        dove_mob = ImageMobject(dove).scale_to_fit_width(1.5).set_color(BLUE)
        #self.add(hawk_mob)
        #self.add(dove_mob)
        def ikony():
            return dove_mob.copy().scale_to_fit_width(
                    .7*max((D.get_value()-V),0)
                ).move_to(ax2.c2p(tmax*3/4,1,0)).set_z_index(3)
        def ikony_h():
            return hawk_mob.copy().scale_to_fit_width(
                    3*min(V/2/D.get_value(),.5)
                ).move_to(
                ax2.c2p(tmax*3/4,min(V/2/D.get_value(),0.5),0)
                ).set_z_index(3)


        legenda = VGroup(
            Tex(r"$x$\dots frekvence jestřábů"),
            Tex(r"$D$\dots náklady na boj"),
            Tex(r"$V$\dots zisk z vítězného boje")
        ).scale(0.8).arrange(DOWN, aligned_edge=LEFT)

        obr = always_redraw(lambda: 
            ax.plot(lambda x:rhs(x,V,D.get_value()), color=ORANGE)
            )
        obr2 = always_redraw(lambda: integralni_krivky())    
        obr3 = always_redraw(lambda: ikony()) 
        obr4 = always_redraw(lambda: ikony_h()) 
        self.add(obr3,obr4)   

        labels = ax.get_axis_labels(
            MathTex("x").scale(1.5), 
            MathTex(r"\frac{\mathrm dx}{\mathrm dt}=x(1-x)\left(\frac V2-\frac D2 x\right)").scale(1.5)
        )
        labels2 = ax2.get_axis_labels(
            MathTex("t").scale(1.5), 
            MathTex("x").scale(1.5)
        )        
        ax.add(MathTex("1").scale(1.5).next_to(ax.c2p(1,0,0),DOWN))
        ax.add(labels)
        ax2.add(labels2)
        ax.scale(0.5).to_corner(UL).shift(DOWN)
        ax2.scale(0.5).to_corner(UR).shift(DOWN)
        self.add(ax)
        self.add(ax2)
        self.add(obr,obr2)

        legenda.next_to(ax2,DOWN)
        self.add(legenda)

        kwds = {
                'value_max' : 2, 
                'values' : [0,1,2],
                }
        
        def budik():
            vystup = analog_indicator(V/D.get_value(),**kwds).scale(1.5)
            if V>=D.get_value():
                vystup.pointer.set_color(RED)
                vystup.dot.set_color(RED)
            else:
                vystup.pointer.set_color(BLUE)
                vystup.dot.set_color(BLUE)
            return vystup

        komentar = VGroup()
        komentar.add(
            Tex(r"Podíl $\displaystyle\frac VD$:"
            ).scale(0.8).next_to(ax,DOWN, aligned_edge=LEFT).shift(1*RIGHT))
        self.add(komentar[0])
        budik_image = always_redraw(lambda: budik().next_to(komentar[0],RIGHT,buff=1))
        self.add(budik_image)
        komentar.add(Tex(r"Uprostřed je $V=D$").scale(0.6).next_to(budik_image,DOWN))
        self.add(komentar[1])

        self.wait()

        self.next_section("Model, rust zisku")        
        self.play(D.animate.set_value(1), run_time=5, rate_func=linear)
        self.wait()

        self.next_section("Model, eliminace holubic")        
        self.play(D.animate.set_value(0.5), run_time=5, rate_func=linear)
        self.wait()

        self.next_section("Model, znovuobjeveni holubic")        
        self.play(D.animate.set_value(1), run_time=5, rate_func=linear)
        self.wait()

        self.next_section("Model, rust zastoupeni holubic")        
        self.play(D.animate.set_value(3), run_time=5, rate_func=linear)
        self.wait()

komentar = """
Dobrý den. Pokud přemýšlíte, jestli jsou nutné neustálé šarvátky a plýtvání energií na soupeření, ať již na úrovni států nebo jedinců, následující video přiblíží tuto problematiku z hlediska evoluce. Budeme v populaci jednoho druhu sledovat vývoj dvou vzorců chování. Ukážeme si, že určité procento agresivního vzorce chování bude vždy přítomno a za určitých okolností to dokonce bude jediný vzorec chování. 

Uvažujme jednotlivce jednoho druhu se dvěma vzorci chování. Nebojovné chování budeme nazývat holubičí povahou a jejich nositele budeme označovat jako holubice. Tito jedinci nebojují o zdroje k přežití. Těmito zdroji může být například prostor k hnízdění nebo přístup k potravě. Holubičí povahy se vyhýbají konfliktu a místo boje raději hledají jiné zdroje. Kromě toho budou v populaci i takzvaní jestřábi, což jsou jedinci s bojovnou povahou. Sejde-li se u jednoho zdroje jestřáb a holubice, holubice ustoupí. Pokud se však u zdroje sejdou dva jestřábi, potom o tento zdroj bojují. Boj vyžaduje nějaké úsilí a to oslabí reprodukční zdatnost jedinců, kteří bojovali. 

Je možné ukázat, že rozumné předpoklady o vývoji populace vedou k tomu, že procentuální zastoupení jestřábího chování v populaci je možné popsat diferenciální rovnicí, která je na obrazovce. V této rovnici figuruje procentuální zastoupení jestřábů x, náklady na boj mezi dvěma jestřáby vyjádřený parametrem D a zisk z konzumace zdroje označený parametrem V.

Rovnice má tři stacionární body, nula, jedna a V/D. Je-li V/D mezi nulou a jedničkou, může být situace jako na obrázku. Rovnice má nestabilní stacionární body 0 a 1. Nestabilita těchto bodů znamená, že v populaci nebude dominovat žádný druh chování stoprocentně. Kromě toho má rovnice stabilní stacionární bod V/D. Na tomto procentu se usadí procentuální zastoupení jestřábů.

Toto nastává, pokud jsou náklady na boj větší než velikost zdroje. Malý zisk z vítězného boje znamená, že se může vyplatit chovat se jako holubice a vyhýbat se boji. Samé holubice však v populaci být také nemohou, protože nula je také nestabilní stacionární bod. Opravdu, pokud do populace holubičích povah pronikne jedna jestřábí povaha, má tento jestřáb k dispozici veškeré zdroje, protože mu všichni ustupují. To znamená, že se jeho geny a jeho vzorec chování bode šířit rychleji než vzorec holubičího chování.

Zkusme snižovat náklady na boj. Podíl V/D tedy bude růst. Vidíme, že stacionární bod se posunuje k větší frekvenci jestřábů a pro V=D bude stacionární bod roven jedné. To znamená, že populace bude složena jenom z jestřábů. Ani další snižování nákladů na boj situaci nemění. Jenom bude systém rychleji konvergovat do stacionárního bodu. 

Jsou-li náklady na boj malé ve srovnání se ziskem při konzumaci zdroje, budou v populaci jenom samí jestřábi. To je případ například stromů v lese. Zdroj je sluneční svit a náklady na boj spočívají ve vybudování delšího kmene. Náklady na boj jsou relativně malé a proto jsou všechny stromy v lese vysoké. 

Pokud ovšem náklady na boj budou růst a podíl V/D klesat pod jedničku, objeví se opět stacionární bod vyjadřující rovnováhu mezi holubičími a jestřábími povahami. Nikdy však populace jestřábů neklesne na nulu. Jak už bylo řešeno, pokud je jestřábů velmi málo, tak mají bez poje k dispozici všechny zdroje, u kterých se objeví, protože je nízká pravděpodobnost, že se u zdroje setkají s dalším jestřábem. 

Je to špatná zpráva pro všechny mírumilovné povahy, ale když se nad tím zamyslíme, chodí to tak nějak i v lidské společnosti. Ať už na úrovni malých kolektivů, nebo na úrovni celých národů. Zkuste si sami rozmyslet, jestli znáte nějaký vhodný příklad. 

"""