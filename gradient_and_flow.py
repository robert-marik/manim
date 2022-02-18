from typing_extensions import runtime
from manim import *
from manim.animation.animation import DEFAULT_ANIMATION_RUN_TIME
import numpy as np
from numpy.core.numeric import outer
import colorsys
from common_definitions import *
import os

from manim_editor import PresentationSectionType

animation_runtime = 15
wait_time = 5

# from https://favpng.com/png_view/wood-frame-wood-circle-png/Kts40pG2
wood_img = r"c:\Users\marik\Documents\GitHub\manim\wood"

a = 1/14
b = 7
A = 1/8
B = 2.5
wood_img = os.path.join("icons","wood")

def function(x,y):
    X = a*(x+b)
    Y = A*(y+B)
    return(-(Y**2 + X))

def contour_x(y,C):
    Y = A*(y+B)
    X = - (Y**2+C)
    x = X/a-b
    return x

def gradient(x,y,z=0):
    X = a*(x+b)
    Y = A*(y+B)
    return [a,2*Y*A]

def gradient_delka(x,y,z=0):
    X = a*(x+b)
    Y = A*(y+B)
    return np.sqrt(a**2 + (2*Y*A)**2)

d11,d12,d22 = 1,.9,1

def gradient_delka_D(x,y,z=0,d11=d11,d12=d12,d22=d22):
    X = a*(x+b)
    Y = A*(y+B)
    g1 = a
    g2 = 2*Y*A    
    return np.sqrt((d11*g1+d12*g2)**2 + (d12*g1+d22*g2)**2)    

class Flow(MovingCameraScene):

    def construct(self):

        self.next_section("Titulek")        
        title = Title(r"Gradient a tok ve dřevě (v ortotropním materiálu)")
        autor = VGroup(Tex("Robert Mařík"),Tex("Mendel University")).arrange(DOWN).next_to(title,DOWN)
        self.play(GrowFromCenter(title))
        self.play(GrowFromCenter(autor[0]))
        self.play(GrowFromCenter(autor[1]))
        self.wait(wait_time*2)


        number_plane = NumberPlane(
            axis_config={
                "stroke_color": BLUE_D,
                "stroke_width": 1, 
                "stroke_opacity": 0.1,}
            )

        self.next_section("Termosnimek")        

        self.play(FadeOut(VGroup(title,autor)))
        wood_obj = ImageMobject(wood_img)
        vertices=[[7,4],[7,-4],[-7,4],[-7,-4]]
        values = [function(x,y) for x,y in vertices]
        dolni_mez = np.min(values)
        horni_mez = np.max(values)

        gradienty = [gradient_delka(x,y) for x in np.linspace(-7,7,10) for y in np.linspace(-4,4,10)]
        gradient_max = np.max(gradienty)
        gradient_min = np.min(gradienty)

        number_of_contours = 20
        # Contours using implicit plot are more general but slower
        # contours = VGroup(*[
        #     ImplicitFunction(lambda x,y:function(x,y)-i)            
        #     .set_color(temperature_to_color(i, dolni_mez,horni_mez)) for i in np.linspace(dolni_mez + 0.05*(horni_mez-dolni_mez), horni_mez ,number_of_contours)
        #     ]
        # )
        contours = VGroup(
            *[
                ParametricFunction(lambda t : np.array([(-C-(A*(t+B))**2)/a -b ,t,0]), 
                   t_range = np.array([-4.3,4.3,0.1])).set_color(temperature_to_color(C, dolni_mez,horni_mez))
                   for C in 
                   np.linspace(dolni_mez + 0.05*(horni_mez-dolni_mez), horni_mez ,number_of_contours)
            ]
        )

        function_colors = VGroup(
            *[
              Square(side_length=0.1, fill_opacity=1).move_to((i,j,0)).set_color(temperature_to_color(function(i,j), dolni_mez,horni_mez))
              for i in np.linspace(-7,7,150) for j in np.linspace(-4,4,80)  
            ]
        )

        self.play(GrowFromEdge(function_colors, LEFT), run_time = 5)
        self.wait()

        self.next_section("Vrstevnice")        
        self.add(contours)
        self.play(AnimationGroup(
            FadeOut(function_colors),
        ), run_time=5)
        self.wait()

        self.next_section("Gradienty")        

        vectors_unscaled_opposite = ArrowVectorField(lambda p:-gradient(*p)[0]*RIGHT-gradient(*p)[1]*UP,
            x_range=[-7,7,1],
            y_range=[-4,4,1],
            color = WHITE,
            length_func = lambda n: 10*n,
        )

        vectors_unscaled = ArrowVectorField(lambda p:gradient(*p)[0]*RIGHT+gradient(*p)[1]*UP,
            x_range=[-7,7,1],
            y_range=[-4,4,1],
            color = WHITE,
            length_func = lambda n: 10*n,
        )

        vectors = ArrowVectorField(lambda p:gradient(*p)[0]*RIGHT+gradient(*p)[1]*UP,
            x_range=[-7,7,1],
            y_range=[-4,4,1],
            colors = [RED, YELLOW, BLUE, DARK_GRAY],
            min_color_scheme_value=gradient_min, 
            max_color_scheme_value=gradient_max, 
            length_func = lambda norm: 0.95 * sigmoid(norm),
            stroke_width = 10,
        vector_config={"max_stroke_width_to_length_ratio":10, "max_tip_length_to_length_ratio":0.4}
        )

        curves = StreamLines( 
            lambda p:gradient(*p)[0]*RIGHT+gradient(*p)[1]*UP,
            stroke_width=3,
            dt=0.5,
            virtual_time=3, opacity=0.75
            ).set_z_index(-1)

        funkce = VGroup(MathTex(r"f=20-y^2-x"),MathTex(r"-\nabla f = \begin{bmatrix} 1\\2y\end{bmatrix}"))
        funkce.arrange(DOWN,aligned_edge=LEFT).to_corner(UL).add_background_rectangle(opacity=0.9, buff=0.5).set_z_index(10)

        self.play(AnimationGroup(*[GrowArrow(_) for _ in vectors_unscaled_opposite], lag_ratio=0.05, run_time=2))
        self.wait()

        self.next_section("Zaporne vzate gradienty")        
        self.play(ReplacementTransform(vectors_unscaled_opposite,vectors_unscaled))
        self.wait()


        self.next_section("Vektorove pole")        
        self.play(ReplacementTransform(vectors_unscaled,vectors))
        self.wait()
        self.play(FadeIn(funkce))
        self.wait()

        self.next_section("Izotropni tok")        
        self.play(FadeOut(funkce), FadeIn(curves))
        self.wait()

        self.next_section("Ortotropni tok")        
        vlastni_vektory=VGroup(*[vectors[3+9*i] for i in range(14)])
        surroundingRectangle= SurroundingRectangle(vlastni_vektory[1:-1],color=YELLOW, buff=0.15)
        roh2 = vlastni_vektory[0].get_corner(UR)
        roh1 = vlastni_vektory[0].get_corner(DL)
        rozmery = roh2-roh1
        uhel = np.arctan(rozmery[1]/rozmery[0])/np.pi*180

        obrazek = wood_obj.copy().rotate(uhel*DEGREES).scale_to_fit_width(3)
        obrazek.to_edge(RIGHT).shift(.7*DOWN).set_z_index(-1)

        lambda1 = 3
        lambda2 = 1
        tempD = np.array([[lambda1,0],[0,lambda2]])
        C,S = np.cos(uhel*DEGREES),np.sin(uhel*DEGREES)
        R = np.array([[C,S],[-S,C]])
        D = np.matmul(np.linalg.inv(R),np.matmul(tempD,R))
        d11 = round(D[0,0],2)
        d12 = round(D[0,1],2)
        d22 = round(D[1,1],2)

        gradienty_D = [gradient_delka_D(x,y,d11=d11,d12=d12,d22=d22) for x in np.linspace(-7,7,10) for y in np.linspace(-4,4,10)]
        gradient_max_D = np.max(gradienty_D)
        gradient_min_D = np.min(gradienty_D)

        vectors_with_D = ArrowVectorField(
            lambda p:(d11*gradient(*p)[0]+d12*gradient(*p)[1])*RIGHT+(d12*gradient(*p)[0]+d22*gradient(*p)[1])*UP,
            x_range=[-7,7,1],
            y_range=[-4,4,1],
            colors = [RED, YELLOW, BLUE, DARK_GRAY],
            min_color_scheme_value=gradient_min_D, 
            max_color_scheme_value=gradient_max_D, 
            length_func = lambda norm: 0.95 * sigmoid(norm),
            stroke_width = 10,
            vector_config={"max_stroke_width_to_length_ratio":10, "max_tip_length_to_length_ratio":0.4}
        )

        curves_with_D = StreamLines( 
            lambda p:(d11*gradient(*p)[0]+d12*gradient(*p)[1])*RIGHT+(d12*gradient(*p)[0]+d22*gradient(*p)[1])*UP,
            stroke_width=3,
            dt=0.5,
            virtual_time=1.5, opacity=0.75
            ).set_z_index(-1)

        matice_D = VGroup(
            VGroup(MathTex("D={}"),Matrix([[d11,d12],[d12,d22]])).arrange(RIGHT),
            VGroup(MathTex(r"\lambda_1={}"+str(lambda1))),
            VGroup(MathTex(r"\lambda_2={}"+str(lambda2)))
            ).arrange(DOWN).to_corner(UL).add_background_rectangle(buff=0.5).set_z_index(10)


        self.play(FadeIn(matice_D), FadeOut(curves))
        self.wait()
        self.add(obrazek)
        self.wait()
        self.play(AnimationGroup(*[Wiggle(_) for _ in vlastni_vektory],Create(surroundingRectangle),lag_ratio=.05))
        self.wait()

        self.play(FadeIn(curves_with_D),ReplacementTransform(vectors.copy(),vectors_with_D),FadeToColor(vectors.set_opacity(.5),GRAY))
        komentar = VGroup(
            Tex(r"šedá ${}={}$ spád teploty"), 
            Tex(r"barevná ${}={}$ tok tepla")
            ).arrange(DOWN, aligned_edge=LEFT, buff=0.5).next_to(
                matice_D, DOWN).add_background_rectangle(
                    buff=0.5).set_z_index(10)
        self.play(FadeIn(komentar))
        self.wait()

        self.next_section("Detail ve vlastnim smeru")        
        first_time = True
        i=0
        # Moving camera from https://www.youtube.com/watch?v=QTlZp8tiql4
        for detail in [vectors_with_D[12*9+3], vectors_with_D[19] , vectors_with_D[60] ]:
            self.camera.frame.save_state()
            detail_frame = SurroundingRectangle(detail, color=PURE_RED, buff=.5)
            self.play(Create(detail_frame))
            self.wait()
            self.play(self.camera.frame.animate.set(width=detail_frame.width*2).move_to(detail), running_time = 2)
            if first_time:
                self.play(FadeOut(detail))
                self.wait(2)
                self.play(FadeIn(detail))
                first_time = False
            self.wait()
            i=i+1
            self.next_section("Detail "+str(i))        
            self.play(Restore(self.camera.frame),FadeOut(detail_frame), running_time = 2)   
            self.wait()     

        self.wait()

komentar = """

Dobrý den, v tomto videu se zaměříme na souvislost gradientu a toku. Například
gradientu teploty a toku tepla. Ukážeme si některé záludnosti na které
narazíme, pokud budeme studovat materiál, mající v různých směrech různé
vlastnosti. Nejběžnějším představitelem takového materiálu je ten nejhezčí a
nejdostupnější, totiž dřevo.

Matematický popis je univerzální, stejně funguje spád koncentrace a difuzní
tok, spád vlhkosti a pohyb vody ve dřevě nebo spád hydraulické hladiny a pohyb
podzemní vody.

Budeme studovat dvourozměrný materiál s určitým rozložením teploty. Termosnímek
by mohl vypadat jako na obrazovce. Každé teplotě je přiřazena nějaká barva. Toto
rozložení teploty definuje podnět, na který příroda reaguje a snaží se vyrovnat
teploty tokem tepla. Výsledný tok tepla je souhra tohoto podnětu s materiálovými
vlastnostmi. Nejprve prozkoumejme tento podnět.

Na obrazovce je příliš mnoho informací. To není vždy ideální. Zkusíme si
vytáhnout jenom některé křivky, podél nichž je teplota konstantní. Jedná se o
vrtevnice, nebo v kontextu teploty lépe o izotermy. Pomocí těchto izoterm můžeme
identifikovat gradient teploty. To je vektor udávající směr a intezitu růstu
teploty. Bílé šipky znázorňující gradient jsou kolmé k izotermám a jsou delší
tam, kde jsou izotermy nahusto.

Pro potřeby toku nepotřebujeme sledovat růst teploty, ale pokles. Vynásobíme
tedy gradient minus jedničkou na záporně vzatý gradient. Ten ukazuje směr
poklesu. Obrázek ještě není moc přehledný. Pro vylepšení můžeme všechny šipky
zkrátit na stejnou délku a informaci o délce zakódovat do barvy šipek.

Ve skutečnosti je na obrazovce termosnímek definovaný kvadratickou funkcí, kde
záporně vzatý gradient snadno spočítáme. Ten nezávisí na x, tedy všechny šipky
v jedné vodorovné řadě vypadají stejně. První komponenta je konstantní a druhá
roste s y. Tedy čím výše jsme na obrazovce, tím více se záporně vzatý gradient
přiklání ke svislému směru.

Všechny šipky jsou teď kolmé na izotermy a směřují do míst s menší teplotou.
Takto, ve směru šipek, by se dalo do pohybu teplo v materiálech, které mají ve
všech směrech stejné vlastnosti. Například v kovech. Stejně velký gradient
vyvolá stejně velký tok a ten je vždy ve směru poklesu.

V případě dřeva jsou v různých směrech různé vlasnosti a gradient podélným
směrem vyvolá větší tok než stejně velký gradient směrem napříč. Navíc, pokud
gradient není v anatomickém směru dřeva, tak se směr poklesu teploty a směr
toku tepla neshodují. Záporně vzatý gradient přepočítáváme na tok pomocí
maticového násobení a příslušná matice může vypadat například tak jako na
plátně.

Zde máme symetrickou matici mající dvě různé vlastní hodnoty. Těm náleží dva na
sebe kolmé vlastní směry. Jedna vlastní hodnota je třikrát větší. Ta dominuje a
strhává tok do svého vlastního směru. To by odpovídalo podélnému směru ve
dřevě. Po výpočtu vlastních vektorů a umístění dřeva podle výsledku by situace
mohla vypadat tak jako je na obrazovce. Abychom moc nerušili grafiku, zobrazíme
si z celé roviny jenom malý kousíček dřeva u kraje. Vektory mířící v podélném
směru dřeva jsou vlastními vektory matice D. Ty si dáme do rámečku.

Nyní pro všechny vektory vypočteme maticový součin s maticí D a tím najdeme
tok. Původní vektory, záporně vzatý gradient, necháme jako duchy jenom žašedlou
poloprůheldnou barvou a tok bude označen barevnými šipkami. 

Vektory mířící v podélném směru dřeva, tedy ve směru vlastníoh vektoru, po
násobení s maticí D nemění směr, protože to jsou vlastní vektory. V tomto
případě teplo teče kolmo na izotermy a směr toku splývá se směrem spádu
teploty.

Pojďme se podívat jinam. Třeba dolů. Tady nejsme ve vlastním směru a proto šedá
šipka se spádem teploty způsobila tok mířící malinko odlišným směrem. Barevná
šipka se přiklonila k podélnému směru dřeva.

Analogická situace nastane, pokud se podíváme nahoru. Opět spád teploty není ve
vlastním směru dřeva a proto je výsledný tok daný barevnou šipkou jakýmsi
kompromisem mezi spádem teploty a vlastním směrem dřeva. Tento kompromis je
popsán maticovým násobením spádu teploty s maticí D.

Takto umíme díky maticím a znalosti gradientu teploty počítat tok tepla. Postup
je plně přenositelný na jakoukoliv skalární stavovou veličinu, jako je
například koncentrace látky, obsah vody ve dřevě nebo hladina podzemní vody v
krajině.

"""