from typing_extensions import runtime
from manim import *
from manim.animation.animation import DEFAULT_ANIMATION_RUN_TIME
import numpy as np
from numpy.core.numeric import outer
import colorsys
from common_definitions import *
import os

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

        title = Title(r"Gradient a tok ve dřevě (v ortotropním materiálu)")
        autor = VGroup(Tex("Robert Mařík"),Tex("Mendel University")).arrange(DOWN).next_to(title,DOWN)
        self.play(GrowFromCenter(title))
        self.play(GrowFromCenter(autor[0]))
        self.play(GrowFromCenter(autor[1]))
        self.wait(wait_time*2)


        number_plane = NumberPlane()
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

        self.add(function_colors)
        self.wait(wait_time*7)
        self.add(contours, number_plane)
        self.play(AnimationGroup(
            FadeOut(function_colors),
        ), run_time=5)
        self.wait(wait_time*7)

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
        self.wait(5*wait_time)
        self.play(ReplacementTransform(vectors_unscaled_opposite,vectors_unscaled))

        self.wait(3*wait_time)
        self.play(ReplacementTransform(vectors_unscaled,vectors))
        self.wait(wait_time)
        self.add(funkce)
        self.wait(wait_time)
        self.add(curves)
        self.wait(wait_time)

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

        self.remove(funkce)
        self.add(matice_D)
        self.wait(wait_time)
        self.add(obrazek)
        self.wait(wait_time)
        self.play(AnimationGroup(*[Wiggle(_) for _ in vlastni_vektory],Create(surroundingRectangle),lag_ratio=.05))

        self.wait(wait_time)
        self.play(ReplacementTransform(curves,curves_with_D),ReplacementTransform(vectors.copy(),vectors_with_D),FadeToColor(vectors.set_opacity(.5),GRAY))
        self.wait(wait_time)

        first_time = True
        # Moving camera from https://www.youtube.com/watch?v=QTlZp8tiql4
        for detail in [vectors_with_D[12*9+3], vectors_with_D[19] , vectors_with_D[60] ]:
            self.camera.frame.save_state()
            detail_frame = SurroundingRectangle(detail, color=PURE_RED, buff=.5)
            self.play(Create(detail_frame))
            self.wait(2*wait_time)
            self.play(self.camera.frame.animate.set(width=detail_frame.width*2).move_to(detail), running_time = 2)
            if first_time:
                self.play(FadeOut(detail))
                self.wait()
                self.play(FadeIn(detail))
                first_time = False
            self.wait(5*wait_time)
            self.play(Restore(self.camera.frame),FadeOut(detail_frame), running_time = 2)   
            self.wait(2*wait_time)     

        self.wait()

komentar = """

Dobrý den, v tomto videu si ukážeme, jak se přepočítává pomocí gradientu a
součinitele tepelné vodivosti teplotní spád na tok tepla. Ukážeme si některé
záludnosti na které narazíme, pokud budeme studovat materiál, mající v různých
směrech různé vlastnosti. Nejběžnějším představitelem takového materiálu je ten
nejhezčí a nejdostupnější, totiž dřevo.

Matematický popis je ale univerzální, stejně funguje spád koncentrace a difuzní
tok, spád vlhkosti a pohyb vody ve dřevě nebo spád hydraulické hladiny a pohyb
podzemní vody.

Budeme studovat dvourozměrný materiál s určitým rozložením teploty. Termosnímek
by mohl vypadat jako na obrazovce. Každé teplotě je přiřazena nějaká barva.
Toto rozložení teploty definuje podnět, na který příroda reaguje a snaží se
vyrovnat teploty tokem tepla. Výsledný tok tepla je souhra tohoto podnětu s
materiálovými vlastnostmi. Nejprve prozkoumejme tento podnět.

Na obrazovce je příliš mnoho informací. To není vždy ideální. Zkusíme si
vytáhnout jenom některé křivky podél nichž je teplota konstantní. Jedná se o
vrtevnice, nebo v kontextu teploty lépe o izotermy. Pomocí těchto izoterm
můžeme identifikovat gradient teploty. To je vektor udávající směr a intezitu
růstu teploty. Bílé šipky znázorňující gradient jsou kolmé k izotermám a jsou
delší tam, kde jsou izotermy nahusto.

Pro potřeby toku nepotřebujeme sledovat růst, ale pokles teploty. Vynásobíme
tedy gradient minus jedničkou a máme záporně vzatý gradient, ukazující směr
poklesu. Obrázek však není moc přehledný. Pro vylepšení můžeme všechny šipky
zkrátit na stejnou délku a informaci o délce gradientu zakódovat do barvy
šipek.

Všechny šipky jsou teď kolmé na izotermy a směřují do míst s menší teplotou.
Takto, ve směru šipek, by se dalo do pohybu teplo v materiálech, které mají ve
všech směrech stejné vlastnosti. Například v kovech. Stejně velký gradient
vyvolá stejně velký tok a ten je vždy ve směru poklesu.

V případě dřeva jsou v různých směrech různé vlasnosti a gradient podélným
směrem vyvolá větší tok než stejně velký gradient směrem napříč. Navíc, pokud
gradient není v anatomickém směru dřeva, tak se směr poklesu teploty a směr
toku tepla neshodují. Záporně vzatý gradient přepočítáváme na tok pomocí
maticového násobení a situace může vypadat například tak jako na plátně. Zde
máme matici se dvěma vlastníma hodnotama, kterým náleží dva vlastní směry. 


"""