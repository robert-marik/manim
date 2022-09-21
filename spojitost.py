from manim import *
import numpy as np
import common_definitions

from manim_editor import PresentationSectionType
template = TexTemplate(preamble=r'\usepackage{url}\usepackage[czech]{babel}\usepackage{amsmath}\usepackage{amssymb}')

class Nadpis(Scene):
    def construct(self):
        self.next_section("Nadpis")        
        title = Title(r"Derivace, spojitost, limita")
        autor = VGroup(Tex("Robert Mařík"),Tex("Mendel University")).arrange(DOWN).next_to(title,DOWN)
        self.play(GrowFromCenter(title))
        self.play(GrowFromCenter(autor[0]))
        self.play(GrowFromCenter(autor[1]))
        aplikace = VGroup(*[Tex(_) for _ in [
            "okamžitá rychlost jako motivace pro zavedení limity", 
            "spojitost jako nástroj pro zavedení limity", 
            "limita jako prostředek pro měření rychlosti (derivace)"
            ]]).arrange(DOWN).next_to(autor,DOWN, buff=2)
        for i,c in enumerate([RED,BLUE,ORANGE]):
            aplikace[i].set_color(c)
        self.play(AnimationGroup(*[GrowFromCenter(_) for _ in aplikace], lag_ratio=0.95), run_time=5)

        self.wait()

class Rychlost(Scene):
    def construct(self):
        
        self.next_section("Nadpis")
        title = Title(r"Rychlost změny funkce")
        title.set_z_index(5).add_background_rectangle(buff=.3)
        self.play(GrowFromCenter(title))

        texty = VGroup (*[ Tex(_) for _ in [
            r"$f(x)$",
            r"$f(x+h)$",
            r"$f(x+h)-f(x)$",
            r"$$\frac{f(x+h)-f(x)}{h}$$",
            r"???"
        ]])

        komentare = VGroup(*[Tex(r"$\dots$ "+_).scale(.9) for _ in [
            r"funkční hodnota v obecném bodě $x$",
            r"funkční hodnota ve vedlejším bodě",
            r"změna funkční hodnoty na intervalu $[x,x+h]$",
            r"průměrná rychlost změny funkce na $[x,x+h]$",
            r"okamžitá rychlost změny funkce"
        ]])

        texty.arrange(DOWN, aligned_edge=RIGHT, buff=0.5)
        texty.to_corner(DL)
        
        for i,j in zip (texty,komentare):
            j.next_to(i,buff=0.3)
            j.set_color(BLUE)
        j[-1].set_color(YELLOW)

        for i,j in zip (texty,komentare):
            self.play(FadeIn(i), FadeIn(j))
        
        self.wait()

class Derivace(Scene):
    def construct(self):
        
        self.next_section("Nadpis")
        title = Title(r"Okamžitá rychlost změny funkce")
        title.set_z_index(5).add_background_rectangle(buff=.3)
        self.play(GrowFromCenter(title))

        texty = VGroup (*[ Tex(_) for _ in [
            r"$f(x)$",
            r"$f(x+h)$",
            r"$f(x+h)-f(x)$",
            r"$$\frac{f(x+h)-f(x)}{h}$$",
            r"???"
        ]])

        komentare = VGroup(*[Tex(r"$\dots$ "+_).scale(.9) for _ in [
            r"funkční hodnota v obecném bodě $x$",
            r"funkční hodnota v bodě o $h$ napravo",
            r"změna funkční hodnoty na intervalu $[x,x+h]$",
            r"průměrná rychlost změny funkce na $[x,x+h]$",
            r"okamžitá rychlost změny funkce"
        ]])

        texty.arrange(DOWN, aligned_edge=RIGHT, buff=0.5)
        texty.to_corner(DL)
        
        for i,j in zip (texty,komentare):
            j.next_to(i,buff=0.3)
            j.set_color(BLUE)
        j[-1].set_color(YELLOW)

        self.play(FadeIn(texty), FadeIn(komentare))
        
        self.wait()
        self.play(VGroup(texty,komentare).animate.shift(3.1*UP))

        self.play(FadeOut(texty[-1]),FadeOut(komentare[-1]))
       
        definice = VGroup(
           *[MathTex(_) for _ in [
            r"\displaystyle\frac{\mathrm df}{\mathrm dx}",
            r"=",
            r"\displaystyle\lim_{h\to 0}",
            r"\displaystyle\frac{f(x+h)-f(x)}h"
           ]]
        ).arrange().scale(1.5).shift(2*DOWN)
        definice.set_color(YELLOW)
        temp = texty[3].copy()
        self.play(temp.animate.move_to(definice[3]))
        self.play(TransformMatchingShapes(temp,definice[3]))
        self.play(FadeIn(definice[2]))

        nazev = Tex("Derivace").scale(1.5).set_color(YELLOW)
        self.play(Create(nazev),Create(definice[:2]))
        self.wait()

class Spojitost(Scene):

    def construct(self):

        self.next_section("Nadpis")
        title = Title(r"Spojitost a limita funkce (pro $x=0$) intuitivně")
        title.set_z_index(5).add_background_rectangle(buff=1)
        self.play(GrowFromCenter(title))
        domain = np.linspace(0,1,300)
        funkce = [
            [lambda x:x+1, r"Spojitá funkce."],
            [lambda x:1/x, r"Nespojitost v nule (diverguje do nekonečna)."],
            [lambda x:(x+np.abs(x))/x, r"Nespojitost v nule (konečný skok)."],
            [lambda x:(x**2+x)/(x), r"Ostranitelná nespojitost."],
        ]

        formulas = [
            r"f_1(x)=x+1",
            r"f_2(x)=\frac {1}x",
            r"f_3(x)=\frac {x+|x|}x",
            r"f_4(x)=\frac {x^2+x}{x}",
        ]

        axes = Axes(
            x_range=[-10.5,10.5,1],
            y_range=[-0.5,4.1,1],
            tips = False,
            y_length=5
            ).to_edge(DOWN, buff=.7)

        #self.remove(axes.get_y_axis())
        grafy = VGroup()
        komentar = VGroup()
        predchozi = None
        colors = [YELLOW,RED,GREEN,BLUE]
        ranges = [
            [[-2,0.1],[0,3]],
            [[-11,-0.05],[0.25,11]],
            [[-11,-0.05],[0.05,11]],
            [[-2,-0.05],[0.05,3]]
        ]        
        dots = [[],[],[0,2],[1]]

        texty = VGroup()
        for i,j in zip(formulas, colors):
            texty.add(MathTex(i).set_color(j))
        texty.arrange(DOWN, aligned_edge=LEFT)
        texty.next_to(title,DOWN, aligned_edge=LEFT)
        texty.shift(RIGHT*0.5+UP)
        texty.set_z_index(1000).add_background_rectangle()

        self.play(FadeIn(texty),FadeIn(axes))
        self.add(Tex(r"$x$").next_to(axes.get_x_axis(),DOWN, aligned_edge=RIGHT).set_z_index(10).add_background_rectangle())

        zapis_ = [
            r"$x+1$ je spojitá",
            r"$$\lim_{x\to 0^+}\frac 1x=\infty$$",
            r"$$\lim_{x\to 0^+}\frac{x+|x|}{x}=2$$",
            r"$$\lim_{x\to 0}\frac{x^2+x}{x}=1$$",
            ]

        zapis_ = [r"""\begin{minipage}{7cm}\raggedright Žlutá funkce je spojitá v~nule. 
           Ostatní funkce mají v~nule bod nespojitosti. 
           V~případě modré funkce jde funkci učinit spojitou 
           dodefinováním jedné funkční hodnoty. Jedná se 
           o~odstranitelnou nespojitost. 
           \par
           \end{minipage}
           """]
        
        zapis = VGroup(*[
            Tex(_).scale(0.95).set_color(c) for _,c in zip(zapis_, colors)
            ])
        zapis.arrange(DOWN, aligned_edge=LEFT)
        zapis.set_z_index(1000).set_color(WHITE).add_background_rectangle(color=GRAY_BROWN, buff=0.2) 
        zapis.to_corner(UR).shift(DOWN)

        #i_ = 0       
        for f,t,c,ranges,dot in [[*i,j,k,l] for i,j,k,l in zip(funkce,colors,ranges,dots)]:            
            self.remove(komentar)
            soucasny = VGroup()
            for range in ranges:
                soucasny.add(axes.plot(f,x_range=[*range,0.01]).set_color(c).set_stroke(width=10))

            #self.play(FadeIn(texty[i_]))
            #i_ = i_ + 1
            dot_ = VGroup()
            for _ in dot:
                dot_.add(Circle(radius=0.07).set_stroke(width=6).set_color(c).move_to(axes.c2p(0,_)))

            if predchozi is None:
                self.play(Create(soucasny),FadeIn(dot_))
            else:
                self.play(TransformFromCopy(predchozi, soucasny),FadeIn(dot_))
            
            predchozi = soucasny
            grafy.add(soucasny)
            self.wait()
            self.next_section()

        self.play(FadeIn(zapis))
        self.wait()   

class Limita(Scene):
    def construct(self):
        self.next_section("Nadpis")
        title = Title(r"Limita a odstranitelná nespojitost")
        title.set_z_index(5).add_background_rectangle(buff=.1)
        self.play(GrowFromCenter(title))            
        #self.wait()


        axes = Axes(
            x_range=[-8.5,8.5,1],
            y_range=[-0.1,1.1,1],
            tips = False,
            y_length=2,
            x_length=8
            ).to_corner(DR, buff=0.7)        

        axes2 = axes.copy()
        axes2.next_to(axes,UP, buff=1)

        limity = [r"1",r"1",r"{\displaystyle \frac 12}"]
        limity_num = [1,1,0.5]
        predpisy = [
            r"{\displaystyle \frac{\sin x}{x}}",
            r"{\displaystyle \frac{e^x-1}{x}}",
            r"{\displaystyle \frac{1-\cos x}{x^2}}"
        ]

        funkce = [
            lambda x:np.sin(x)/x, 
            lambda x:(np.exp(x)-1)/x, 
            lambda x:(1-np.cos(x))/x**2, 
            ]

        for i in range(3):

            def f(x):
                return funkce[i](x)
            limita = limity[i]
            limita_num = limity_num[i]
            predpis = predpisy[i]

            c = RED
            c2 = BLUE
            graf = axes.plot(f,x_range=[-8,8,0.03]).set_color(c)
            graf2 = VGroup()
            graf2.add(axes2.plot(f,x_range=[-8,-0.1,0.01]).set_color(c2))
            graf2.add(Circle(radius=0.05).set_stroke(width=3).move_to(axes2.c2p(0,limita_num)).set_color(c2))
            graf2.add(axes2.plot(f,x_range=[0.1,8,0.01]).set_color(c2))


            popisek2 = VGroup()
            popisek2.add(Tex(r"$$y="+predpis+r"$$"))
            popisek2.add(Tex(r"$$\lim_{x\to 0}"+predpis+r"="+limita+r"$$"))
            popisek2.set_color(c2).arrange(DOWN, aligned_edge=LEFT).next_to(axes2, LEFT).to_edge(LEFT)

            popisek = VGroup(
                Tex(r"$$y=\begin{cases}"+limita+r"&\text{pro $x=0$}\\[6pt]"+predpis+r" & \text{jinak} \end{cases}$$").set_color(c),
            ).arrange(DOWN, aligned_edge=LEFT).add_background_rectangle().next_to(axes, LEFT).to_edge(LEFT)

            self.play(FadeIn(popisek2[0]))
            self.add(axes2)
            self.play(Create(graf2[0]))
            self.add(graf2[1])
            self.play(Create(graf2[2]))
            self.play(FadeIn(popisek2[1]))

            self.next_section()
            self.wait()

            self.play(FadeIn(popisek))
            self.add(axes)
            self.play(Create(graf))

            self.next_section()
            self.wait()

            self.play(FadeOut(axes,axes2,graf,graf2,popisek,popisek2))


komentar = """
V tomto povídání si řekněme, jak měřit okamžitou rychlost, s jakou se mění nějaká veličina. Tím se seznámíme s velice důležitým pojmem, derivace funkce. Nesmírně užitečný pojem, protože téměř každý fyzikální zákon mluví o rychlosti. Derivace je poté operací, umožňující napsat pro takový fyzikální zákon matematický model. Tím se vymaníme z poněkud omezeného světa středoškolské fyziky věnované dějům probíhajícím konstantními rychlostmi a kde se rychlost dá určovat podílem. Vstupujeme do opravdového světa dějů probíhajících libovolnými rychlostmi a získáváme nástroj pro popis a pochopení těchto dějů.

Pro korektní definici derivace budeme potřebovat další pojem, limita. Limitu si zavedeme pomocí spojitosti, kterou budeme chápat prozatím intuitivně. 

Zajímejme se o veličinu f, která je dána hodnotami jiné veličiny x. Pokud se veličina x mění, mění se i f a chceme vědět, jak rychle. Pro jednoduchost si pod veličinou x představujeme čas a f je veličina měnící se v čase. Zajímá nás, jak rychle. Uvažujeme-li dva časové okamžiky vzdálené od sebe h časových jednotek, tedy x a x+h, potom rozdíl funkčních hodnot udává, jak se veličina f v tomto časovém intervalu změní. Po vydělení délkou časového intervalu dostáváme změnu veličiny f za jednotku času, tedy rychlost. Přesněji, průměrnou rychlost, s jakou se f mění na intervalu od x do x+h. Tuto rychlost bychom rádi pozměnili z průměrné rychlosti na intervalu na okažitou rychlost v bodě x. Tedy bychom potřebovali časový interval stáhnout prakticky do jediného okamžiku. Jinými slovy, potřebovali bychom za hodnotu h dosadit nulu. 

Vzhledem k tomu, že h je ve jmenovateli, nebude toto dosazení realizovatelné běžnými aritmetickými prostředky. I když se to ale zdá nemožné, dá se tato operace provést. Budeme potřebovat koncept opírající se o pojmy spojistost a limita. Jak bylo řečeno, spojitost budeme chápat intuitivně. Například žlutá funkce je krásná lineární funckce jejímž grafem je přímka. Tato funkce je spojitá. Červená funkce má x ve jmenovateli a tedy problém pro x rovno nule. A opravdu, graf ukazuje, že v nule je bod nespojitosti. Jmenovatel zlomku teď necháme být,  to znamená že pořád bude problém v nule, ale budeme měnit čitatel. U zelené funkce vidíme mírné vylepšení oproti funkci červené. Je tam stále bod nespojitosti, ale nyní je již tento bod nespojitosti alespoň konečné výšky. Zajímavá situace nastane pro modrou funkci. Až na jeden jediný problematický bod nám modrá funkce splyne se spojitou žlutou funkcí. 

V tomto případě je možné funkci dodefinovat tak, aby se stala spojitou. Proto se takovému bodu nespojitosti říká odstranitelná nespojitost. Funkční hodnota, která odstraní odstranitelnou nespojitost v daném bodě se nazývá limita funkce v tomto bodě. Funkce (x^2+x)/x vypadá poněkud uměle, protože zlomek je možno upravit a tím se nespojitosti také zbavíme. Abychom se podívali i na méně umělé případy odstranitelné nespojitosti, můžeme uvažovat nepříklad funkci sin(x)/x, která není definovaná v nule. Pokud doplníme definici funkce tak, že funkční hodnota v nule je rovna jedné, dostaneme spojitou červenou funkci. V takovém případě říkáme, že funkce sin(x)/x má v nule limitu rovnu jedné. Podobná situace nastává u funkce (exp(x)-1)/x. Funkci je možno doplnit na spojitou, pokud funkční hodnotu v nule položíme rovnu jedné a proto limita teéto funkce v nule je rovna jedné. Z funkcí, majících limitu v nule různou od jedné, můžeme vzpomenout například funkci (1-cos(x))/x^2. Ta má limitu rovnu jedné polovině a situaci vidíme na obrázku. 

Limita funkce v bodě, ve kterém je odstranitelná nespojitost, je tedy jakási nejlepší rozumná náhrada funkční hodnoty. Taková, že výsledná funkce je v uvažovaném bodě spojitá. Situace je poměrně názorná, pokud pojem spojitost chápeme intuitivně. Což jsme si říkali, že pro potřeby tohoto našeho videa bude stačit. 

Vraťme se ke vzorečku s průměrnou rychlostí. Říkali jsme, že bychom rádi položili h rovno nule, ale nemůžeme, aby se nula neobjevila ve jmenovateli. Pokud však zlomek má pro h rovno nule odstranitelnou nespojitost, můžeme použít nejlepší rozumnou náhradu funkční hodnoty, limitu. A to je přesně ten okamžik, kdy se z průměrné rychlosti stane rychlost okamžitá. Nazývá se derivace funkce f podle proměnné x a značí buď f s čárkou, nebo zápisem připomínajícím zlomek a čteným jako df podle dx.

"""            
