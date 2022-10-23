
from manim import *
from manim_editor import PresentationSectionType
config.max_files_cached = 400
from numpy import sin, cos

import matplotlib.pyplot as plt

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)



class SmerovePole(Scene):


    def construct(self):

        jednotka = 1
        xmin,xmax = 0,12
        ymin,ymax = 0,6
        ax = Axes(
            x_range=[xmin,xmax,100],
            x_length=(xmax-xmin)*jednotka, 
            y_range=[ymin,ymax,100], 
            y_length=(ymax-xmin)*jednotka, 
            tips=False
            )

        def rhs(x,y):
            #return np.sin(x)+0.5*y
            return 1/2*x-y
            #return 4-y
            #return 0.31*y*(5-y)-1.5

        # pro funkci 0.31*y*(5-y)-1.5 na commons wikimedia
        stabilni = [3.688]
        nestabilni = [1.312]

        Y, X = np.mgrid[ymin:ymax:100j, xmin:xmax:100j]

        def plot_streams():
            U = X*0+1
            V = rhs(X,Y)
            speed = np.sqrt(U*U + V*V)
            stream_img = plt.streamplot(
                X, Y, U, V,
                #maxlength = 1,
                #density = 0.6
                )
            sgm = stream_img.lines.get_segments()
            krivky = []
            lastpoint = sgm[0]
            aktualni_krivka = [lastpoint[1,:]]
            n = 0
            for i in sgm[1:]:
                n = n+1
                #print("Bod "+str(n)+" \n"+str(i))
                if all(i[0,:] == lastpoint[1,:]):
                    aktualni_krivka = aktualni_krivka + [i[0,:],i[1,:]]
                    #print ("            Pridavam k predchozi vetvi, delka je "+str(len(aktualni_krivka)))
                else:
                    krivky = krivky + [aktualni_krivka]
                    aktualni_krivka = [i[0,:],i[1,:]]
                    #print ("Zakladam novou vetev")
                lastpoint = i
            krivky = krivky + aktualni_krivka
            ciste_krivky = [np.array(i) for i in krivky if len(i)>3]
            #streams = VGroup()
            #for t in ciste_krivky:
            #    streams.add(axes.plot_line_graph(t[:,0],t[:,1], add_vertex_dots=False))
            #return(streams)
            return ([
                ax.plot_line_graph(
                    t[:,0],t[:,1], add_vertex_dots=False
                    ).set_stroke(width=2).set_z_index(-5).set_color(WHITE) 
                    for t in ciste_krivky
            ])


        slope_field = VGroup()
        imax,jmax = 20,10
        for i in range(imax):
            xcoor = xmin + i*(xmax-xmin)/imax
            for j in range(jmax):
                ycoor = ymin + j*(ymax-ymin)/jmax
                smernice = rhs(xcoor,ycoor)
                delka = 0.3
                dX = 1/np.sqrt(1+smernice**2)*delka
                dY = smernice/np.sqrt(1+smernice**2)*delka
                slope_field.add(
                    Line(
                        start = ax.c2p(xcoor,ycoor,0), 
                        end = ax.c2p(xcoor+dX,ycoor+dY))
                        )
        slope_field.set_color(YELLOW).set_stroke(width=6)
        slope_field2 = VGroup(
            slope_field[125].copy(),
            slope_field[102].copy(),
            slope_field[12].copy(),
            slope_field[48].copy(),
        )

        # nestabilni_IK = VGroup()
        # nestabilni_IK.add(
        #     Line(
        #         start=ax.c2p(xmin,nestabilni[0]),
        #         end=ax.c2p(xmax,nestabilni[0]),
        #         ).set_color(RED)
        # )

        # stabilni_IK = VGroup()
        # stabilni_IK.add(
        #     Line(
        #         start=ax.c2p(xmin,stabilni[0]),
        #         end=ax.c2p(xmax,stabilni[0]),
        #         ).set_color(BLUE)
        # )

        axes = VGroup(ax)
        axes.add(MathTex("t").next_to(ax.get_x_axis()))
        axes.add(MathTex("x").next_to(ax.get_y_axis(),UP))
        slope_field2.shuffle_submobjects()

        rovnice = MathTex(r"\frac{\mathrm dx}{\mathrm dt}=\varphi(x,t)")
        rovnice.next_to(ax,UP).shift(DOWN*0.9)
        rovnice.set_z_index(10).add_background_rectangle(buff=0.5)
        axes.add(rovnice)

        self.add(axes)

        for i in slope_field2:
            svorky = VGroup()
            start = np.array(ax.p2c(i.get_start()))
            end = np.array(ax.p2c(i.get_end()))
            zmena = end-start
            smernice = zmena[1]/zmena[0]
            print("zmena"+str(zmena)+str(smernice))
            A = start
            B = A + np.array([1,0])
            C = start + np.array([1,zmena[1]/zmena[0]])
            print ("souradnice "+str(A)+str(B)+str(end))
            smer = Line(start=ax.c2p(A[0],A[1],0), end=ax.c2p(C[0],C[1],0))
            svorky.add(
                Brace(smer,np.sign(smernice)*DOWN, buff=0)
            )
            svorky.add(
                Brace(smer,RIGHT, buff=0)
            )
            svorky.add(MathTex("1").next_to(svorky[0],DOWN*np.sign(smernice),buff=0.2))
            smerniceR = round(smernice,3)
            svorky.add(MathTex(r"\varphi(x,t)="+str(smerniceR)).next_to(svorky[1],RIGHT))
            svorky.set_color(GRAY)
            bod = Dot(ax.c2p(A[0],A[1],0))
            self.play(FadeIn(bod))
            self.play(FadeIn(svorky))
            self.next_section()

            self.play(Create(smer),Uncreate(bod))
            self.play(FadeIn(i),FadeOut(svorky),Uncreate(smer))
            self.wait(0.2)
            self.next_section()

        #self.wait()
        self.play(AnimationGroup(
            *[FadeIn(i) for i in slope_field],
            ), run_time=1)
        self.wait()
        self.next_section()

        #return False
        krivky = plot_streams()#.shuffle_submobjects()
        
        self.play(*[Create(i) for i in krivky],run_time=1)            
        # self.add(nestabilni_IK)
        # self.add(stabilni_IK)

        self.wait()

komentar = """
V tomto videu si představíme silný nástroj pro zjednodušení práce s diferenciálními rovnicemi, a to transformaci proměnných.

Ukážeme si, že vhodnou volbou fyzikálních jednotek můžeme redukovat počet parametrů v matematickém modelu. Ukážeme si fyzikální pohled na věc a poté odvodíme formální matematické vztahy pro přechod k jiným veličinám. Ukážeme si tuto techniku na příkladě rovnice popisující tepelnou výměnu a na příkladě rovnice logistického růstu. Tato dovednost je zásadní pro matematické modelování, protože snížení počtu parametrů ovlivňujících úlohu značně redukuje složitost následné analýzy.

Nejprve malá rozcvička s převodem jednotek. Pokud zvětšíme jednotku ve které udáváme vzdálenost, zmenší se stejným násobkem numerická hodnota, například 2400 metrů je 2.4 kilometru.

Jednotka derivované veličiny je podílem jednotek veličin vstupujících do derivace. Změna jednotek se přirozeně promítne i do derivace. Pokud dopravní prostředek za minutu urazí 2400 metrů, tak urazí za minutu 2.4 kilometru a za sekundu 40 metrů. Změnou fyzikálních jednotek tedy dokážeme měnit a regulovat numerické hodnoty fyzikálních veličin.

Nyní se podívejme na klasický model tepelné výměny, kdy rychlost ochlazování tělesa o teplotě T je úměrná rozdílu teploty tělesa a okolí. Teplota okolí je T_nekonečno a počáteční teplota tělesa je T_0. 

Nyní pár fyzikálních triků. Při měření teploty nebudeme trvat na stupních celsia, ale stupnici si posuneme tak, aby v nové stupnici byla teplota okolí rovna nule. To můžeme, nulová hodnota na teplotní stupnici je stanovena úmluvou. Například pro Celsiovu stupnici jako rovnovážná teplota směsi vody a ledu. V naší nové stupnici bude nulová teplota dána teplotou okolí. Tím získá teplota okolí, původně označená T-nekonečno, nulovou hodnotu a v rozdílu se neuplatní. Teplota v nových jednotkách bude například tau. 

Domluvou je stanoven i jeden dílek stupnice teploty. Například pro Celsiovu stupnici je jeden dílek roven setině mezi teplotou tání ledu a varu vody. V naší nové stupnici nastavíme dílek na rozdíl mezi počáteční teplotou a teplotou okolí. Tím bude hodnota počáteční teploty rovna jedné. 

Konstanta úměrnosti k vyjadřuje rychlost s jakou klesá teplota pro tau rovno jedné, tj. na počátku. Vhodnou volbou jednotky času můžeme udělat tuto hodnotu rovnu jedné tak, aby se v součinu neuplatnila. Pokud bude na počátku například teplota klesat rychlostí pět jednotek teploty za jednotku času, odpovídá to jedné jednotce teploty za pětinu jednotky času. V takové situaci je šikovné měřit čas v pětinách minuty a konstanta úměrnosti bude rovna jedné. Čas v nových jednotkách označíme theta. 

Nyní vidíme, že se stalo něco fascinujícího. Namísto původní úlohy se třemi parametry, k, T0 a Tnekonečno, máme úlohu, kde žádný parametr nevystupuje. Takový model je rozhodně pohodlnější pro simulace a numerické výpočty. 

To byl fyzikální přístup, vyjádřený změnou jendotek. Matematik často takový postup odbude tvrzením, že bez újmy na obecnosti v modelu položíme Tnekonečno rovno nule, T0 rovno jedné a k také rovno jedné. Musí však být schopen ukázat, že taková volba opravdu není na újmu obecnosti. Jak bychom však argumentovali?

Využijeme základní vzorečky. Derivace součtu funkce a konstanty je stejná jako derivace této funkce. Podobně, derivace konstantního násobku funkce je konstantním násobkem derivace funkce. Analogicky se chová derivace podle veličiny, která je konstantním násobkem veličiny původní. 

Jak by dopadla aplikace těchto obratů na naši rovnici tepelné výměny? Rovnice obsahuje tři parametry. Teplotu okolí, počáteční teplotu a konstantu úměrnosti, která například v případě ochlazování kávy souvisí s materiálem hrníčku. 

První transformací bude odečtení teploty okolí od aktuální teploty. Poté rovnici i počáteční podmínku vydělíme teplotním rozdílem mezi počáteční teplotou a teplotou okolí. Konstantní násobek začleníme do derivované veličiny. Díky tomu nám vznikly sice strašné podíly obsahující rozdíl v čitateli i jmenovateli, ale všechny teploty figurují ve výrazu stejného typu a po zavedení nové proměnné se vše zjednoduší. 

Kromě uvedeného se ještě zbavíme konstanty k tak, že ji převedeme na opačnou stranu rovnice a použijeme ke změně jednotky času. 

Nyní máme všechno nachystáno na zavedení nových proměnných, teploty a času. Obě tyto veličiny budou vycházet fyzikálně bez jednotky, protože například teplota se měří v násobcích počátečního teplotního rozdílu. Proto se nové transformované veličiny nazývají bezrozměrná teplota a bezrozměrný čas. Nová úloha neobsahuje žádný parametr ani v rovnici ani v počáteční podmínce a proto bude proces probíhat stále stejně, tj. teplota tělesa se vyrovná s teplotou okolí. Ze zkušenosti z běžného života víme, že nic jiného ostatně v této úloze ani není možné očekávat. 

Jiný případ je rovnice popisující velikost populace v prostředí s omezenou nosnou kapacitou a vystavené lovu. Po vydělení rovnice nosnou kapacitou prostředí a invazním parametrem r můžeme rovnici převést na rovnici v transformovaných proměnných X a T a s jediným parametrem H. Původní počet parametrů v rovnici se tak snížil lze tří na jeden. V závislosti na velikosti tohoto parametru buď dojde k ustálení velikosti populace v stacionárním bodě, nebo populace vyhyne. Z rozboru vidíme, že to, která situace nastane, nezáleží na každém parametru samostatně, ale souvisí to s hodnotou výrazu h/(r*K). Za zmínku ještě stojí, že vydělení velikosti populace x nosnou kapacitou prostředí K znamená, je nová míra velikosti populace, X, se měří v násobcích nosné kapacity prostředí a nemá tedy žádnou jednotku. Jedná se opět o bezrozměrnou veličinu. Stejně bezrozměrnou veličinou je veličina H nebo T.

Na závěr si shrneme výhody práce s transformovanými diferenciálními rovnicemi. První výhodou je, že v rovnici redukujeme počet parametrů. To jsme viděli v obou předešlých příkladech.

Další výhodou je, že výsledné rovnice jsou pro veličiny bez fyzikálních jednotek a proto tyto jednotky nemusíme uvažovat v numerických simulacích. 

Další výhodou je, že získané bezrozměrné veličiny nemívají příliš velké ani příliš malé numerické  hodnoty. To je důsledek toho, že nové veličiny měříme v násobcích hodnot spojených s úlohou. To jsme opět viděli v obou uvedených příkladech. 

Ukázali jsme si, jak je možné transformovat diferenciální rovnice do jednoduššího tvaru, ukázali jsme si formální matematickou cestu i pohodlnější fyzikální cestu a uvedli jsme si několik důvodů, proč se tato činnost vyplatí. 
"""        