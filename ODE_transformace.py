from tkinter import CENTER
from turtle import fillcolor
from manim import *
from matplotlib.pyplot import title
from scipy.integrate import solve_ivp  # řešení diferenciálních rovnic
import colorsys
import random
import os
from manim_editor import PresentationSectionType
from common_definitions import *

template = TexTemplate(preamble=r'\usepackage{url}\usepackage[czech]{babel}\usepackage{amsmath}\usepackage{amssymb}')

class Intro(Scene):
    def construct(self):

        self.next_section("Nadpis")        
        title = Title(r"Transformace diferenciálních rovnic (změnou jednotek)")
        autor = VGroup(Tex("Robert Mařík"),Tex("Mendel University")).arrange(DOWN).next_to(title,DOWN)
        self.play(GrowFromCenter(title))
        self.play(GrowFromCenter(autor[0]))
        self.play(GrowFromCenter(autor[1]))
        self.wait()

class TransformaceJednotek(MovingCameraScene):
    def construct(self):
        
        def MujTex(text):
            return(Tex(r"$\bullet$ \quad \begin{minipage}[t]{10cm}"+text+"\end{minipage}", tex_template=template).scale(.9))


        self.next_section("Fyzikalni pristup k transformaci jednotek")        
        title = Title(r"Transformace jednotek a jejich vliv na číselnou hodnotu")
        self.add(title)

        text = VGroup(
            MujTex(r"Pokud zvětšíme jednotku veličiny, její numerická hodnota se zmenší stejným násobkem. Například $2400\,\mathrm m = 2{,}4\mathrm{km}.$"),
            MujTex(r"Pokud zvětšíme jednotku derivované veličiny, numerická hodnota derivace se zmenší stejným násobkem. Například $2400\,\mathrm m \,\mathrm{min}^{-1}= 2{,}4\,\mathrm{km}\,\mathrm{min}^{-1}.$"),
            MujTex(r"Pokud zmenšíme jednotku veličiny podle níž derivujeme, numerická hodnota derivace se zmenší stejným násobkem. Například $2400\,\mathrm m \,\mathrm{min}^{-1}= 40\,\mathrm{m}\,\mathrm{s}^{-1}.$"),
            MujTex(r"Změnou jednotek dokážeme měnit hodnoty veličin. Většinou chceme mít standardizované jednotky, aby se daly sdílet měřící přístroje a porovnávat hodnoty. Někdy se ale hodí mít jednotky vlastní související třeba jen s jedním konkrétním problémem.")
        ).arrange(DOWN, aligned_edge=LEFT).next_to(title,DOWN)

        for i in text:
            if i == text[-1]:
                self.play(self.camera.frame.animate.move_to(text[-1],aligned_edge=DOWN).shift(DOWN))
            self.play(FadeIn(i))
            self.wait()

        title.move_to

class Teplota(MovingCameraScene):
    def construct(self):
        
        self.next_section("Transformace postupnymi zmenami")        

        self.camera.frame.shift(1.3*UP)

        title = Title(r"Změna jednotek v rovnici ochlazování").shift(1.3*UP)
        self.add(title)

        merak = VGroup()
        merak.add(Dot(
            radius=0.1,
            stroke_color=WHITE,
            stroke_width=4,
            fill_color=RED,
            fill_opacity=1
        ))
        merak.add(
            Line(
                start = (0,0,0), 
                end = 3*UP
                ).set_z_index(-1).set_stroke(width=10)
        )
        merak.add(
            Line(
                start = (0,0,0), 
                end = 2.6*UP, 
                color=RED
            ).set_stroke(width=6)
        )
        merak.shift(0.2*DOWN)

        carka = Line(start = RIGHT*0, end=LEFT*0.13, buff=0)
        carka_delsi = Line(start = RIGHT*0, end=LEFT*0.18, buff=0)
        stupnice = VGroup()
        for i in range(27):
            if (i-3)%10 == 0:
                carka_stupnice = carka_delsi
            else:
                carka_stupnice = carka
            stupnice.add(carka_stupnice.copy().shift(-0.1*RIGHT+i/10*UP) )
        stupnice[3].set_color(ORANGE)
        nova_stupnice=stupnice.copy()
        # nova_stupnice[-3].set_color(WHITE)
        # nova_stupnice[6].set_color(WHITE)
        stupnice[-3].set_color(YELLOW).set_stroke(width=7).add_tip(at_start=True, tip_length=0.08)
        stupnice[6].set_color(YELLOW).set_stroke(width=7).add_tip(at_start=True, tip_length=0.08)
        nova_stupnice.flip()
        nova_stupnice.shift(0.35*RIGHT)
        merak.add(
            MathTex("T/^{\circ} \mathrm C").scale(0.5).next_to(stupnice, UP, aligned_edge=RIGHT)
        )

        merak2 = VGroup(
            MathTex(r"\tau").scale(0.5).next_to(nova_stupnice, UP, aligned_edge=LEFT)
        )
        
        teplomer = VDict([("merak",merak),("stupnice",stupnice),("nova_stupnice",nova_stupnice),("merak2",merak2)])
        stupnice.add(Tex(r"$0$").scale(0.5).next_to(stupnice[3],LEFT, buff=0.1).set_color(ORANGE))
        stupnice.add(Tex(r"$T_0$").scale(0.5).next_to(stupnice[-4],LEFT, buff=0.1).set_color(YELLOW))
        stupnice.add(Tex(r"$T_\infty$").scale(0.5).next_to(stupnice[6],LEFT, buff=0.1).set_color(YELLOW))

        teplomer.scale(2)
        teplomer.to_corner(UL)
        nova_stupnice_popisek=VGroup(
            Tex(r"0").scale(1).next_to(nova_stupnice[3],RIGHT, buff=0.1).set_color(ORANGE)
            )

        uloha = VGroup(
            Tex("Základní model v jednotkách SI:"),
            MathTex(r"\frac{\mathrm dT}{\mathrm dt}=-k(T-T_\infty), \quad T(0)=T_0"),
            Tex("V nových jednotkách teploty,"),
            MathTex(r"{{\frac{\mathrm d\tau}{\mathrm dt}=}}{{-k}}{{(\tau-0),}} \quad \tau(0)={{\tau_0}}"),
            Tex(r"V nových jednotkách teploty a času, $\theta=kt$:"),
            MathTex(r"{{\frac{\mathrm d\tau}{\mathrm d\theta}=}}{{-}}{{\tau,}} \quad \tau(0)={{1}}"),
            Tex(r"Trojparametrická úloha je redukována na úlohu bez parametru.")
        ).arrange(DOWN, aligned_edge=LEFT).next_to(teplomer, aligned_edge=UP, buff=2)

        for i in [0,2,4]:
            uloha[i].shift(LEFT)

        self.play(FadeIn(uloha[0],uloha[1]))

        def MujTex(text):
            return(Tex(r"\begin{minipage}[t]{10cm}"+text+"\end{minipage}", tex_template=template).scale(.9))

        temp = MujTex(r"Rovnice modeluje ochlazování tělesa o počáteční teplotě $T_0$ v~prostředí s teplotou $T_\infty$ podle Newtonova zákona ochlazování, kdy rychlost změny teploty je úměrná teplotnímu rozdílu").set_color(BLUE).to_edge(DOWN, buff=3)
        self.play(FadeIn(temp))
        self.wait()

        self.next_section()        
        self.remove(temp)
        self.play(self.camera.frame.animate.shift(1.3*DOWN))
        self.play(*[Create(i) for i in 
            [teplomer['merak'], teplomer['stupnice'], teplomer['nova_stupnice'], nova_stupnice_popisek]])
        self.wait()

        self.next_section()        
        # stupnice.add(Tex(r"1").scale(0.5).next_to(nova_stupnice[22],RIGHT, buff=0.1).set_color(ORANGE))
        komentar = Tex(r"Posuneme stupnici. Bude začínat na teplotě okolí.").next_to(teplomer, aligned_edge=DOWN)
        self.play(FadeIn(komentar))
        self.play(VGroup(nova_stupnice,nova_stupnice_popisek).animate().shift(3/10*2*UP))
        self.play(FadeIn(teplomer["merak2"].add_background_rectangle()))
        temp = Tex(r"$\tau_0$").scale(1).next_to(nova_stupnice[21],RIGHT,buff=0.1)
        self.play(FadeIn(temp))
        prevod = Tex(r"$\tau = T - T_\infty$:").next_to(uloha[2],RIGHT)
        self.play(FadeIn(uloha[2],uloha[3],prevod))
        self.wait()
        self.play(Transform(uloha[3][2],MathTex(r"\tau,").next_to(uloha[3][1], aligned_edge=DOWN).shift(0.07*DOWN)))
        self.wait()


        self.next_section()        
        self.remove(komentar)
        komentar = Tex(r"Změníme dílek stupnice. Počáteční teplota bude 1.").next_to(teplomer, aligned_edge=DOWN)
        self.play(FadeIn(komentar))
        self.play(
            FadeOut(temp),
            *[FadeOut(nova_stupnice[i]) for i in range(len(nova_stupnice)) if (i!=3) and (i!= 4)]
            )
        self.play(nova_stupnice[4].animate().move_to(nova_stupnice[21]))
        zacatek = nova_stupnice[3].get_center()[1]
        konec = nova_stupnice[21].get_center()[1]
        print (str(zacatek)+" po "+str(konec))
        delta = (konec-zacatek)/10

        dilky = VGroup()
        for i in [1,2,3,4,5,6,7,8,9,-1,-2]:
            dilky.add(
                Line(start=RIGHT*0, end=RIGHT*0.2).set_stroke(width=2).move_to(
                    nova_stupnice[3], aligned_edge=LEFT).shift(delta*UP*i)
            )
        dilky[4].set_stroke(width=5)    

        self.play(Create(dilky), FadeIn(Tex(r"$1$").scale(1).next_to(nova_stupnice[21],RIGHT,buff=0.1)))
        self.play(Transform(uloha[3][-1],MathTex(r"1").next_to(uloha[3][-2])))
        self.play(Transform(prevod,Tex(r"$\tau = \frac{T - T_\infty}{T_0-T_\infty}$:").next_to(uloha[2],RIGHT)))
        self.wait()


        self.next_section()        
        self.remove(komentar)
        self.play(FadeIn(uloha[4],uloha[5]))
        self.play(FadeIn(uloha[6].scale(0.75).shift(3*LEFT).set_color(RED)))
        self.wait()

class TeplotaFormalne(MovingCameraScene):

    def construct(self):

        self.next_section()        
        title = Title(r"Formální transformace v rovnici ochlazování")
        self.add(title)

        eq = VGroup()
        eq.add(MathTex(r"{{\frac{\mathrm dT}{\mathrm dt} }} {{= - }} {{k}} {{(T-T_\infty)}}, \qquad {{T(0)=T_0}} "))   
        eq.add(MathTex(r"{{\frac{\mathrm d(T-T_\infty)}{\mathrm dt} }} {{= - }} {{k}} {{(T-T_\infty)}}, \qquad {{T(0)-T_\infty=T_0-T_\infty}} "))   
        eq.add(MathTex(r"{{\frac{1}{T_0-T_\infty}\frac{\mathrm d(T-T_\infty)}{\mathrm dt} }} {{= - }} {{k}} {{\frac{T-T_\infty}{T_0-T_\infty}}}, \qquad {{\frac{T(0)-T_\infty}{T_0-T_\infty}=1}} "))   
        eq.add(MathTex(r"{{\frac{\mathrm d\frac{T-T_\infty}{T_0-T_\infty} }{\mathrm dt} }} {{= - }} {{k}} {{\frac{T-T_\infty}{T_0-T_\infty}}}, \qquad {{\frac{T(0)-T_\infty}{T_0-T_\infty}=1}} "))   
        eq.add(MathTex(r"{{\frac 1k \frac{\mathrm d\frac{T-T_\infty}{T_0-T_\infty} }{\mathrm dt} }} {{= - }} {{}} {{\frac{T-T_\infty}{T_0-T_\infty}}}, \qquad {{\frac{T(0)-T_\infty}{T_0-T_\infty}=1}} "))   
        eq.add(MathTex(r"{{\frac{\mathrm d\frac{T-T_\infty}{T_0-T_\infty} }{\mathrm d(kt)} }} {{= - }} {{}} {{\frac{T-T_\infty}{T_0-T_\infty}}}, \qquad {{\frac{T(0)-T_\infty}{T_0-T_\infty}=1}} "))   
        eq.add(MathTex(r"{{\frac{\mathrm d\tau }{\mathrm d \theta} }} {{= - }} {{}} {{\tau}}, \qquad {{\tau(0)=1}} "))   

        eq.arrange(DOWN, buff=.5).next_to(title,DOWN, buff=.5)

        def MujTex(text):
            return(Tex(r"\begin{minipage}[t]{10cm}"+text+"\end{minipage}", tex_template=template).scale(.9))

        k = VGroup(
            MujTex(r"Základní rovnice pro ochlazování tělesa o počáteční teplotě $T_0$ v~prostředí o teplotě $T_\infty$ obsahuje tři parametry. Dva uvedené ($T_0$ a $T_\infty$) souvisí s teplotou. Třetí parametr, $k$, souvisí s intenzitou předávání tepla. Například s tím, jestli máme kafe v plechovém nebo polystyrenovém hrníčku."),
            MujTex(r"Posuneme teplotu o $T_\infty.$ Protože derivace konstanty je nulová a derivace rozdílu je rozdíl derivací, platí $$\frac{\mathrm d(T-T_\infty)}{\mathrm dt}=\frac{\mathrm dT}{\mathrm dt}-\frac{\mathrm dT_\infty}{\mathrm dt}=\frac{\mathrm dT}{\mathrm dt}.$$ U počáteční podmínky odečteme z obou stran konstantu $T_\infty$."),
            MujTex(r"Vydělíme rovnici i počáteční podmínku výrazem $T_0-T_\infty$."),
            MujTex(r"Začleníme násobení konstantou před zlomkem do derivované veličiny. Podle pravidla pro derivaci konstantního násobku platí $$k\frac{\mathrm dy}{\mathrm dx}=\frac{\mathrm d(ky)}{\mathrm dx}.$$"),
            MujTex(r"Vydělíme konstantou $k$."),
            MujTex(r"Začleníme konstantu před derivací do veličiny, podle které derivujeme. Podle pravidla pro derivaci složené funkce platí  $$\frac{\mathrm dy}{\mathrm dx} = \frac{\mathrm dy}{\mathrm d(kx)} \frac{\mathrm d(kx)}{\mathrm dx} = \frac{\mathrm dy}{\mathrm d(kx)}k\quad\text{ a odsud }\quad\frac 1k\frac{\mathrm dy}{\mathrm dx} = \frac{\mathrm dy}{\mathrm d(kx)}. $$"),
            MujTex(r"Zavedeme bezrozměrnou teplotu a bezrozměrný čas pomocí vztahů $\tau=\frac{T-T_\infty}{T_0-T_\infty}$, a $\theta = kt.$ Nová rovnice neobsahuje žádný parametr. Řešení bude vypadat pořád stejně. (Těleso vychladne na teplotu okolí.)"),
        )

        for i in k:
            i.set_color(BLUE)#  add_background_rectangle(buff=0.2, color=DARK_GRAY)

        k[0].next_to(eq[0],DOWN, buff=0.5)
        self.add(eq[0],k[0])
        self.wait()
        for i in range(len(eq)-1):
            self.next_section()        
            self.remove(*k)
            # temp = eq[i].copy()
            # next_to(eq[i],DOWN,buff=0.5)
            k[i+1].next_to(eq[i+1],DOWN, buff=0.5)
            self.play(self.camera.frame.animate.move_to(eq[i+1]).shift(DOWN))
            self.play(TransformMatchingTex(eq[i].copy(),eq[i+1]),FadeIn(k[i+1]))
            # self.play(eq.animate().shift(eq[i+1].get_center()[1]*DOWN))
            self.wait()

class Logisticka(Scene):

    def construct(self):


        self.next_section()
        title = Title(r"Logistická rovnice s lovem")
        self.add(title)


        def MujTex(text):
            return(Tex(r"\begin{minipage}[t]{10cm}"+text+"\end{minipage}", tex_template=template).scale(.9))

        eq0 = MathTex(r"{{\frac{\mathrm dx}{\mathrm dt} }} {{=}} {{r}} {{x}} {{\left(1-\frac xK\right)}} {{-}} {{h}}")   
        eq1 = MathTex(r"{{\frac 1K\frac{\mathrm dx}{\mathrm dt} }} {{=}} {{r}} {{\frac xK}} {{\left(1-\frac xK\right)}} {{-}} {{\frac hK}}")   
        eq2 = MathTex(r"{{ \frac{1}{rK} \frac{\mathrm dx}{\mathrm dt} }} {{=}} {{}} {{ \frac{x}{K} }} {{\left(1-\frac xK\right)}} {{-}} {{ {h\over rK} }}")   
        eq3 = MathTex(r"{{\frac{\mathrm d \frac xK}{\mathrm d(rt)} }} {{=}} {{}} {{\frac xK}} {{\left(1-\frac xK\right)}} {{-}} {{\frac {h}{rK}}}")   
        eq4 = MathTex(r"{{\frac{\mathrm d X}{\mathrm dT} }} {{=}} {{}} {{X}} {{\left(1-X\right)}} {{-}} {{H}}")   

        eq = VGroup(eq0,eq1,eq2,eq3,eq4).arrange(DOWN).next_to(title,DOWN).to_edge(LEFT, buff=.5)

        k = VGroup(
            Tex(r"vydělit rovnici parametrem $K$"),
            Tex(r"vydělit rovnici parametrem $r$"),
            Tex(r"začlenit konstanty do derivace"),
            Tex(r"přeznačit proměnné"),
            Tex(r"$X=\frac xK$, $T=rt$, $H=\frac {h}{rK}$"),
        )

        self.add(eq[0])
        temp = MujTex(r"Logistická rovnice s lovem obsahuje tři parametry. Podle vzájemných relací mezi těmito parametry může a nemusí populace přežít. Vhodná volba jednotek (vhodná transformace rovnice) ukáže, že ve skutečnosti chování rovnice řídí jediný parametr, závisející na $r$, $K$ a $h$.")
        self.add(temp)
        self.wait()

        self.next_section()        
        self.remove(temp)
        for i in range(len(k)-1):
            k[i].next_to(eq[i],RIGHT, buff=0.5).to_edge(RIGHT)
            self.play(GrowFromCenter(k[i]))
            self.play(
                *[Transform(j.copy(),jj) for j,jj in zip(eq[i],eq[i+1])]
            )
            if i!=len(k)-2:
                self.wait()
                self.next_section()        

        k[-1].next_to(eq[-1],RIGHT, buff=1.5).to_edge(RIGHT)
        self.play(GrowFromCenter(k[-1]))
        self.wait()

        self.next_section()        
        self.remove(*[i for i in self.mobjects])
        self.add(eq,k,title)
        self.play(*[FadeOut(i) for i in [eq1,eq2,eq3,*k[:-1  ]]])
        self.play(eq4.animate().next_to(eq0).to_edge(RIGHT).set_color(YELLOW))
        self.play(k[4].animate().next_to(eq4,DOWN).to_edge(RIGHT))
        temp = MujTex(r"Logistická rovnice s lovem obsahuje tři parametry. Po transformaci zůstane jediný parametr $\displaystyle H=\frac h{rK}.$ Rovnice se tedy chová pořád stejně, pokud se lov $h$ i nosná kapacita $K$ zvětší stejným násobkem (například o stejné procento). Dokud vychází bezrozměrný parametr $H$ stále stejný, chová se rovnice stále stejně ve smyslu persistence populace.").to_edge(DOWN)
        self.add(temp)

        self.wait()

class TransformaceDerivace(MovingCameraScene):
    def construct(self):

        def MujTex(text):
            return(Tex(r"$\bullet$ \quad \begin{minipage}[t]{10cm}"+text+"\end{minipage}", tex_template=template).scale(.9))

        self.next_section()        
        title = Title(r"Transformace v derivaci")
        self.add(title)
        text = VGroup(
            MujTex(r"Derivace součtu je součet derivací a derivace konstanty je nula. Proto pro funkce vzniklá posunutím má stejnou derivaci jako původní funkce. Pro funkci $y(x)$ a konstantu $y_0$ platí $$\frac{\mathrm d(y+y_0)}{\mathrm dx}=\frac{\mathrm dy}{\mathrm dx}.$$" ),
            MujTex(r"Derivace konstantního násobku je násobek derivace, tedy pro funkci funkci $y(x)$ a konstantu $k$ platí $$\frac{\mathrm d(ky)}{\mathrm dx}=k\frac{\mathrm dy}{\mathrm dx}.$$"),
            MujTex(r"Podobně jako v předchozím, pokud derivujeme podle $k$-násobku původní proměnné, platí $$\frac{\mathrm dy}{\mathrm d(kx)}=\frac 1k \frac{\mathrm dy}{\mathrm dx}.$$")
            ).arrange(DOWN, aligned_edge=LEFT).next_to(title,DOWN)

        for i in text:
            if i == text[-1]:
                self.play(self.camera.frame.animate.move_to(text[-1],aligned_edge=DOWN).shift(DOWN))
            self.play(FadeIn(i))
            self.wait()
            self.next_section()        

class Cile(Scene):

    def construct(self):
        text = [
            r"Po transformaci obsahuje rovnice v nových veličinách menší množství parametrů.",
            r"Nové veličiny jsou bez fyzikální jednotky a tudíž vhodné pro numerické simulace, kdy se zpravidla o jednotky nestaráme.",
            r"Nové veličiny zpravidla nabývají hodnot řádově srovnatelných s~jedničkou. Nejedná se ani o tisíce ani o tisícíny."
            ]
        def MujTex(text):
            return(Tex(r"$\bullet$ \quad \begin{minipage}[t]{10cm}"+text+"\end{minipage}", tex_template=template).scale(.9))
        textTex = VGroup(
            *[MujTex(_) for _ in text]
        ).arrange(DOWN, buff=0.5)

        self.next_section()        
        title = Title(r"Výhody práce s transformovanými diferenciálními rovnicemi")
        self.add(title)
        textTex.next_to(title,DOWN, buff=1)
        for i in textTex:
            self.play(GrowFromCenter(i))
            self.wait()
            self.next_section()        



            
        

