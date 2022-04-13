from manim import *
import numpy as np
import common_definitions
import random
random.seed(0)
np.random.seed(0)

from manim_editor import PresentationSectionType

config.max_files_cached = 300

wait_time = 2
a = 3
b = 3
alpha = 0.7
beta = 0.5
gamma = 0.4
delta = 0.8
def F(X):
    x = X[0]
    y = X[1]
    """ Return the vector field. """    
    result = np.sin(x) * RIGHT 
    return result

def F(X):
    x = X[0]
    y = X[1]
    """ Return the vector field. """    
    #return np.array([x*y-1/3*x**3,-x])
    #return np.array([x*(y+4)-6*np.sin(x),(x+7)/7])
    # x = x +7
    # y = y + 3.5
    # x = x/14
    # y = y/7
    #return np.array([a*x*(1-alpha*x-beta*y),b*y*(1-gamma*x-delta*y),0])
    result = np.sin(x + y) * RIGHT + np.sin(x*y / 3) * UP
    return result

# from https://github.com/3b1b/videos/blob/4716f5b75911af25c4ec24ad3e0d3dd83e28fabf/_2018/div_curl.py#L55
def divergence(vector_func, point, dt=1e-7):
    value = vector_func(point)
    point2 = np.array([point[0],point[1],0])
    return sum([
            (vector_func(point2 + dt * vect) - value)[i] / dt
            for i, vect in enumerate([RIGHT, UP, OUT])
        ])

def derivace(vector_func, point, dt=1e-7):
    value = vector_func(point)
    point2 = np.array([point[0],point[1],0])
    return np.array([
            (vector_func(point2 + dt * vect) - value)[i] / dt
            for i, vect in enumerate([RIGHT, UP, OUT])
        ])        

class VektorovePole(MovingCameraScene):
    
    def construct(self):
        np.random.seed(0)
        random.seed(0)
        vectors = ArrowVectorField(lambda p:F(p)[0]*RIGHT+F(p)[1]*UP,
            x_range=[-7,7,.35],
            y_range=[-4,4,.35],
            colors = [GRAY,BLUE, YELLOW, ORANGE, RED,WHITE],
            #min_color_scheme_value=gradient_min, 
            #max_color_scheme_value=gradient_max, 
            length_func = lambda norm: min(norm, 0.4*sigmoid(norm)),
            stroke_width = 10,
        vector_config={"max_stroke_width_to_length_ratio":10, "max_tip_length_to_length_ratio":0.3}
        )
        
        a = [_ for _ in vectors]
        random.shuffle(a)

        self.next_section("Tok pomoci vektoru")        
        title = Title(r"Vektorové pole a jeho divergence").add_background_rectangle(buff=0.5).set_z_index(10)
        self.play(GrowFromCenter(title))
        self.play(AnimationGroup(*[FadeIn(_) for _ in a], lag_ratio=0.1),run_time=14)

        self.next_section("Tok pomoci proudnic")        
        self.play(FadeOut(title))

        draw_streamlines = False
        draw_streamlines = True
        np.random.seed(0)
        random.seed(0)
        if draw_streamlines:
            stream_lines = StreamLines(
                F,
                x_range=[-7,7,1],
                y_range=[-4,4,1], 
                stroke_width=2, 
                virtual_time=10,
                max_anchors_per_line=30)
            self.add(stream_lines)  
            stream_lines.start_animation(warm_up=True, flow_speed=1.5)
            self.wait(stream_lines.virtual_time / stream_lines.flow_speed)        
            self.play(stream_lines.end_animation())        
            self.wait()
            #self.remove(stream_lines)
        else:
            stream_lines = VGroup()

        np.random.seed(0)
        random.seed(0)
        stream_lines1 = StreamLines(
                F,
                x_range=[-7,7,.5],
                y_range=[-4,4,.5], 
                color=GRAY,
                noise_factor=0,
                max_anchors_per_line=30).set_stroke(width=0.5)
        np.random.seed(0)
        random.seed(0)
        stream_lines2 = StreamLines(
                lambda x:-F(x),
                x_range=[-7,7,.5],
                y_range=[-4,4,.5], 
                color=GRAY,
                noise_factor=0,
                max_anchors_per_line=30).set_stroke(width=0.5)

        self.play(
            FadeOut(*[i for i in self.mobjects]),
            FadeIn(stream_lines1),
            FadeIn(stream_lines2), 
            )            

        self.wait()
        #return False
        #self.add(NumberPlane())
        circles = {}
        streams = {}
        texts = {}
        arrows_all = {}
        all_comments = {}
        for i,point_and_text in enumerate([
                [-4.8,-2,0,[r"Převažuje tok ven z kruhu."]],
                [-2.6,-0.3,0,[r"Převažuje tok dovnitř do kruhu."]],
                [2,-1.5,0,[r"Mírná převaha toku ven z kruhu."]],
                [-4,-1,0,[r"Nejasná situace pro posouzení jenom podle obrázku.",r"Divergence bude numericky blízko k nule."]],
                [-1,1,0,[r"Převaha toku ven. Tok je pomalý (krátké vektory)."]],
                [0.5,3,0,[r"Tok dovnitř je vyšší než ven."]],
                [-3.5,2.3,0,[r"Převažuje tok ven.",r"Nehraje roli zda doleva nebo doprava."]],
                [-6,1.6,0,[r"Převaha toku ven,",r"na opačnou stranu než v předchozím případě."]],
                [-6,3.3,0,[r"Naprostá dominance toku dovnitř."]]
                ]):
            self.next_section("Detail")        
            circle = Circle(color=WHITE, radius=0.2).set_stroke(width=1)
            #circle.add(Dot(circle.get_center(), radius=0.02))
            point = point_and_text[:3]
            circle.move_to(point)            
            # self.play(Create(circle))
            # self.wait()

            self.camera.frame.save_state()
            detail_frame = SurroundingRectangle(circle, color=BLUE, buff=.3)
            detail_frame.set_stroke(width=1, opacity=0.5)
            self.play(AnimationGroup(
                Create(circle),
                Create(detail_frame),
                lag_ratio=0.05)
            )

            self.wait(0.5)
            self.play(self.camera.frame.animate.set(width=detail_frame.width*2).move_to(circle), run_time = 2)
            Delta = 0.3
            if draw_streamlines:
                np.random.seed(0)
                random.seed(0)
                stream_lines = StreamLines(F, stroke_width=2, max_anchors_per_line=10, 
                    x_range=[point[0]-Delta, point[0]+Delta, 0.1], 
                    y_range=[point[1]-Delta, point[1]+Delta, 0.1], 
                    padding=0.2, 
                    dt = 0.01,
                    ).set_z_index(-2).set_stroke(width=.75)
            else:
                stream_lines = VGroup()
            hodnota = MathTex(r"\nabla \cdot \vec{q} = "+str(round(divergence(F,point),2))).scale(0.75).next_to(circle)
            hodnota.add_background_rectangle(buff=0.1, opacity=0.5)
            arrows = VGroup()

            for i in range(12):
                uhel = i*2*PI/12
                smer = np.array([np.cos(uhel),np.sin(uhel),0])
                bod = np.array(point)+smer*0.2
                if np.dot(F(bod),smer)<0:
                    barva = RED
                else:
                    barva = BLUE
                arrows.add(Arrow(
                    start=bod, 
                    end=bod+F(bod)*0.25, # /np.linalg.norm(F(bod))
                    buff=0, 
                    max_stroke_width_to_length_ratio=10, 
                    max_tip_length_to_length_ratio = 0.2,
                    ).set_color(barva).set_stroke(width=1))

            comment = VGroup()
            if point_and_text[-1] != "":
                comment = VGroup(
                    *[Text(_) for _ in point_and_text[-1]]
                ).arrange(DOWN, aligned_edge=LEFT).scale(0.1).move_to(detail_frame,aligned_edge=UP).add_background_rectangle(buff=0.02, opacity=0.5)

            self.play(AnimationGroup(
                FadeIn(stream_lines),
                FadeIn(arrows),
                FadeIn(comment),
                lag_ratio=0.1))
            self.wait()

            self.next_section("Celkovy pohled")
            self.play(Restore(self.camera.frame),FadeOut(detail_frame), run_time = 2)   
            self.play(FadeIn(hodnota))
            self.wait()
            circles[i] = circle
            # streams[i] = stream_lines
            texts[i] = hodnota
            arrows_all[i] = arrows
            all_comments[i] = comment



        self.wait()            

def F2(X):
    x = X[0]
    y = X[1]
    """ Return the vector field. """    
    #return np.array([x*y-1/3*x**3,-x])
    #return np.array([x*(y+4)-6*np.sin(x),(x+7)/7])
    # x = x +7
    # y = y + 3.5
    # x = x/14
    # y = y/7
    #return np.array([a*x*(1-alpha*x-beta*y),b*y*(1-gamma*x-delta*y),0])
    result = (sigmoid(x/2) +0.1)*(1-0.4*np.cos(y)) *RIGHT + np.exp(-y**2/6)*(1+0.4*np.sin(x)) * UP
    return result

class DivergenceKartezske(MovingCameraScene):
    def construct(self):
        scale = .3
        sipky = {}
        sipky['both'] = VGroup()
        sipky['x'] = VGroup()
        sipky['y'] = VGroup()
        body = []
        for x in np.linspace(-5,5,21):
            for y in np.linspace(-3,3,13):
                start = x*RIGHT+y*UP
                body = body + [[x,y]]
                sipky['both'].add(Arrow(start=start, end=start + scale * F2([x,y]), buff=0,max_stroke_width_to_length_ratio=10, max_tip_length_to_length_ratio = 0.3))
                sipky['x'].add(Arrow(start=start, end=start + scale * F2([x,y])[0]*RIGHT, buff=0,max_stroke_width_to_length_ratio=10, max_tip_length_to_length_ratio = 0.3))
                sipky['y'].add(Arrow(start=start, end=start + scale * F2([x,y])[1]*UP, buff=0,max_stroke_width_to_length_ratio=10, max_tip_length_to_length_ratio = 0.3))
        sipky['x'].set_color(GREEN)
        sipky['y'].set_color(GREEN)

        self.next_section("Kartezske souradnice")        
        title = Title(r"Divergence v kartézských souřadnicích")
        self.play(GrowFromCenter(title))

        a = [_ for _ in sipky["both"]]
        random.shuffle(a)
        self.play(AnimationGroup(*[FadeIn(_) for _ in a], lag_ratio=0.1),run_time=8)

        self.play(FadeOut(title))
        self.wait()

        i_center = 13*9+8
        i_left = i_center-13
        i_right = i_center+13
        i_left2 = i_center-13*2
        i_right2 = i_center+13*2
        i_up = i_center+1
        i_down = i_center-1
        i_up2 = i_center+2
        i_down2 = i_center-2
        self.wait()
        bod = [*body[i_center],0] 
        hodnota_derivace = derivace(F2,bod)
        hodnota_divergence = divergence(F2,bod)

        self.next_section("Kartezske souradnice detail")        
        stred = Circle(radius=0.75,color=YELLOW).move_to(bod).set_z_index(-1).set_stroke(width=10)
        self.play(FadeIn(stred))
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.set(width=3.5).move_to(bod), run_time = 2)        
        self.wait()    

        Delta = 1
        stream_lines = StreamLines(F2, stroke_width=2, max_anchors_per_line=10, 
            x_range=[bod[0]-Delta, bod[0]+Delta, .5], 
            y_range=[bod[1]-Delta, bod[1]+Delta, .5], 
            padding=0.2, 
            dt = 0.01,
            ).set_z_index(-2).set_stroke(width=.75)        
        arrows = VGroup()

        for i in range(24):
            uhel = i*2*PI/24
            smer = np.array([np.cos(uhel),np.sin(uhel),0])
            start = np.array(bod)+smer*0.75
            if np.dot(F2(start),smer)<0:
                barva = RED
            else:
                barva = BLUE
            arrows.add(Arrow(
                start=start, 
                end=start+F2(start)*0.25, # /np.linalg.norm(F(bod))
                buff=0, 
                max_stroke_width_to_length_ratio=10, 
                max_tip_length_to_length_ratio = 0.2,
                ).set_color(barva).set_stroke(width=2))


        self.play(FadeIn(stream_lines))
        self.wait()
        self.play(FadeIn(arrows))
        self.wait()

        self.next_section("Kartezske souradnice :(")        
        oci = VGroup(Dot(),Dot(0.6*RIGHT))        
        oci.set_color(YELLOW).move_to(stred).shift(0.25*UP).set_z_index(-5)
        uhel = PI/4
        usmev = Arc(start_angle=3/2*PI-uhel, angle=2*uhel, radius=0.5)
        usmev.set_stroke(width=10, color=YELLOW).move_to(stred).shift(-0.35*UP).set_z_index(-5)
        zamraceni = usmev.copy().rotate(PI).move_to(stred).shift(-0.3*UP).set_z_index(-5)

        popis = Tex(r"Jedna těžká dvoudimenzionální úloha.")
        popis2 = Tex(r"Dvě snadné jednodimenzionální úlohy.")
        for _ in [popis,popis2]:
            _.scale(0.2).add_background_rectangle(buff=0.05).set_z_index(15)
            _.move_to(stred, aligned_edge=UP)#.shift(LEFT+0.2*UP)

        self.play(FadeOut(arrows))    
        self.play(FadeIn(oci),FadeIn(zamraceni))
        self.play(FadeIn(popis))

        self.next_section("Kartezske souradnice :)")        
        self.wait()
        sipky["kopie1"] = sipky["both"].copy()    
        sipky["kopie2"] = sipky["both"].copy()    
        self.play(
            *[Transform(i,j) for i,j in zip (sipky['kopie1'], sipky["x"])],
            *[Transform(i,j) for i,j in zip (sipky['kopie2'], sipky["y"])]
            )
        self.wait()
        self.play(
            ReplacementTransform(zamraceni, usmev),
            ReplacementTransform(popis, popis2),
        )
        self.play(FadeOut(sipky['both']))
        self.wait()

        self.next_section("Kartezske souradnice unfocus")        
        self.play(Restore(self.camera.frame), run_time = 2)   
        self.wait()

        radky = VGroup(
            MathTex(r"\vec q = (P,Q)"),
            MathTex(r"P"),
            MathTex(r"Q"),
            MathTex(r"\nabla\cdot \vec q = \frac{\partial P}{\partial x}+\frac{\partial Q}{\partial y}=",
                str(round(hodnota_derivace[0],3)+round(hodnota_derivace[1],3)))
        ).arrange(DOWN, aligned_edge=LEFT)
        j,P,Q,div = radky
        j.to_corner(UL)#.background_rectangle(buff=0.3)
        P.next_to(j,DOWN,aligned_edge=LEFT,buff=1)#.background_rectangle(buff=0.3)
        Q.next_to(P,DOWN,aligned_edge=LEFT,buff=2.5)#.background_rectangle(buff=0.3)
        div.to_corner(UR)
        self.play(
            AnimationGroup(
            *[FadeIn(_) for _ in [j,P,Q]], 
            lag_ratio=0.5
            ))

        vodorovne_sipky=VGroup(*[sipky['x'][_] for _ in [i_left,i_center,i_right,i_left2,i_right2]])
        vodorovne_sipky.add_background_rectangle(buff=0.2)

        svisle_sipky=VGroup(*[sipky['y'][_] for _ in [i_down,i_center,i_up,i_down2,i_up2]])
        svisle_sipky.add_background_rectangle(buff=0.2)

        self.play(AnimationGroup(
            vodorovne_sipky.animate.scale(5).set_stroke(width=10).next_to(P),
            svisle_sipky.animate.rotate(-90*DEGREES).scale(5).set_stroke(width=10).next_to(Q),
            FadeOut(stred), 
            FadeOut(sipky["kopie1"]),
            FadeOut(sipky["kopie2"]),
            FadeOut(oci),
            FadeOut(usmev),
            FadeOut(stream_lines),
            FadeOut(popis2),
            ),
            run_time=10, 
            )   
        self.wait()

        self.next_section("Divergence pomoci derivace")        
        vypocet_derivaci = VGroup(
            MathTex(r"\frac{\partial P}{\partial x}="+str(round(hodnota_derivace[0],3))),
            MathTex(r"\frac{\partial Q}{\partial y}="+str(round(hodnota_derivace[1],3)))
        )

        vypocet_derivaci[0].next_to(P,DOWN,aligned_edge=LEFT)
        self.play(FadeIn(vypocet_derivaci[0]))     
        self.wait()

        vypocet_derivaci[1].next_to(Q,DOWN,aligned_edge=LEFT)
        self.play(FadeIn(vypocet_derivaci[1]))     
        self.wait()
        br = Brace(VGroup(P,Q,vypocet_derivaci), direction=RIGHT).shift(0.5*RIGHT)
        self.play(FadeIn(br))

        div.next_to(br, buff=1)
        self.play(Create(div))     
        self.wait()

class Intro(Scene):
    def construct(self):

        self.next_section("Nadpis")        
        title = Title(r"Divergence a rovnice kontinuity")
        autor = VGroup(Tex("Robert Mařík"),Tex("Mendel University")).arrange(DOWN).next_to(title,DOWN)
        self.play(GrowFromCenter(title))
        self.play(GrowFromCenter(autor[0]))
        self.play(GrowFromCenter(autor[1]))
        self.wait()
        aplikace = VGroup(*[Tex(_) for _ in ["vedení tepla", "difuze", "sušení dřeva",  "proudění podzemní vody"]]).arrange(DOWN).next_to(autor,DOWN, buff=2)
        for i,c in enumerate([RED,BLUE,ORANGE,YELLOW]):
            aplikace[i].set_color(c)
        self.play(AnimationGroup(*[GrowFromCenter(_) for _ in aplikace], lag_ratio=0.95), run_time=5)

        self.wait()

class Motivace(Scene):
    def construct(self):

        bilance = VGroup(
            Tex(r"Nárůst množství (první verze):"),
            Tex(r"Množství vygenerovné zdroji"),
            Tex(r"Množství spotřebované spotřebiči"),
            Tex(r"Množství dodané tokem"),
            Tex(r"Množství, které odteklo")
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(UP)

        bilance2 = VGroup(
            Tex(r"Nárůst množství (zkrácená verze):"),
            Tex(r"Příspěvek ze zdrojů a spotřebičů"),
            Tex(r"Celková bilance toku")
        ).arrange(DOWN, aligned_edge=LEFT).next_to(bilance,DOWN, aligned_edge=LEFT)

        bilance3 = VGroup(
            Tex(r"Nárůst množství (pomocí intenzity toku):"),
            Tex(r"Příspěvek ze zdrojů a spotřebičů"),
            Tex(r"Snížení intenzity toku")
        ).arrange(DOWN, aligned_edge=LEFT).next_to(bilance2,DOWN, aligned_edge=LEFT)

        bilance4 = VGroup(
            Tex(r"Nárůst množství (pomocí nárůstu toku):"),
            Tex(r"Příspěvek ze zdrojů a spotřebičů"),
            Tex(r"Zesílení toku")
        ).arrange(DOWN, aligned_edge=LEFT).next_to(bilance3,DOWN, aligned_edge=LEFT)
 
        self.next_section("Bilance 1")        
        bilance[0].shift(LEFT)
        bilance[2].set_color(RED)
        bilance[4].set_color(RED)
        self.play(AnimationGroup(*[FadeIn(_) for _ in bilance],lag_ratio=0.8), run_time=6)
        self.wait()

        self.next_section("Bilance 2")        
        bilance2[0].shift(LEFT)
        self.play(FadeIn(bilance2[0]))
        self.play(ReplacementTransform(
            VGroup(bilance[1].copy(),bilance[2].copy()), bilance2[1]))
        self.play(ReplacementTransform(
            VGroup(bilance[3].copy(),bilance[4].copy()), bilance2[2]))
        self.wait()   

        self.next_section("Bilance 3")        
        bilance3[0].shift(LEFT)
        self.play(FadeIn(bilance3[0]))
        self.play(ReplacementTransform(
            bilance2[1].copy(), bilance3[1]))        
        self.play(ReplacementTransform(
            bilance2[2].copy(), bilance3[2]))        
        self.wait()   

        self.next_section("Bilance 4")        
        self.play(
            VGroup(
                bilance,bilance2,bilance3
            ).animate.shift(3*UP))  
        bilance4.shift(3*UP)
        bilance4[0].shift(LEFT)
        bilance4[2].set_color(RED)
        self.play(FadeIn(bilance4[0]))
        self.play(ReplacementTransform(
            bilance3[1].copy(), bilance4[1]))        
        self.play(ReplacementTransform(
            bilance3[2].copy(), bilance4[2]))          
        self.wait()         

        rovnice = MathTex(r"\frac{\partial u}{\partial t}","=",
        r"\sigma","-",r"\nabla\cdot\vec q").scale(1.5).to_edge(UP)

        cleny = VGroup(
            Tex(r"Člen $\nabla\cdot \vec q$ je divergence vektorového pole $\vec q$."),
            Tex(r"Znak $\nabla$ je operátor nabla."),
        ).arrange(DOWN, aligned_edge=LEFT).next_to(rovnice,DOWN)

        self.play(*[FadeOut(_) for _ in [bilance,bilance2,bilance3]])
        self.play(FadeIn(rovnice[1]))
        self.play(ReplacementTransform(bilance4[0].copy(),rovnice[0]),run_time=4)
        self.play(ReplacementTransform(bilance4[1].copy(),rovnice[2]),run_time=4)
        self.play(ReplacementTransform(bilance4[2].copy(),VGroup(rovnice[3],rovnice[4])),run_time=4)

        self.play(FadeIn(cleny))
        self.wait()
        

komentar = """

Dobrý den, vítejte u videa, ve kterém se seznámíme s pojmem divergence a
využijeme jej při sestavení rovnice kontinuity. Možnou aplikací je popis
libovolného transportního děje, jako například vedení tepla, difuze, sušení
dřeva nebo proudění podzemní vody.

Představme si cokoliv co proudí a může se kumulovat. V tomto kontextu se obvykle
mluví o hustotě stavové veličiny v daném bodě a jejím toku tímto bodem, ale
představujte si klidně vodu v jezeře. Jezero může mít pramen a může z něj být
voda odebírána k zavlažování. Tedy může zde být zdroj a spotřebič. Obvykle má
jezero nějaký přítok a nějaký odtok. Do celkové bilance tedy vstupují čtyři
faktory. Dva působí kladně a dva červené záporně. Toto můžeme ještě
zjednodušit, pokud budeme dva a dva faktory uvažovat společně. Spotřebiče
budeme brát jako zdroje se záporným účinkem a odtok jako záporný přítok nebo
naopak. Tím se situace zjednoduší ze čtyř členů na dva členy.

První souvisí se zdroji a spotřebiči a druhý s tokem. Přesněji, nárůst veličiny
v daném místě je roven množství o kolik je odtok menší než přítok. Tedy
množstí, o kolik je tok zeslaben. Aby koncept lépe zapadl do obvyklého postupu,
kdy přirozeně sledujeme růst veličin, budeme místo se zeslabením toku pracovat
se zesílením toku a započítávat ho záporně.

A už nám nic nebrání sestavit základní rovnici používanou pro popis
transportních dějů. Protože tok vztahujeme k jednotce času, vztáhneme k
jednotce času celou bilanci. Nárůst sledované veličiny za jednotku času je
derivace podle času. To dobře známe, protože to je slovní interpretace
parciální derivace. Přírůstek ze společného působení zdrojů a spotřebičů musí
být součástí formulace úlohy. Označíme jej sigma, to je druhý člen do naší
bilance. Chybí už jenom třetí člen, kterým kvantifikujeme zesilování toku.

Tok q přenášející stavovou veličinu má velikost a směr. Je to tedy vektorová
funkce nebo též vektorové pole. Zavedeme speciální operátor udávající nárůst
tohoto toku. Tento operátor se nazývá divergence, označuje symbolem nabla,
zapisujeme jako trojúhelník vrcholem dolů.

Takže jak divergence funguje, jak ji najít a co vyjadřuje?

Uvažujme vektorové pole jako na obrázku. Pro přehlednost jsou v něm všechny
příliš dlouhé vektory zkráceny na stejnou délku a původní délka je zakódována v
barvě. Představme si tyto vektory jako rychlostní pole a dívejme se na
trajektorie objektů, které se podle něj budou pohybovat. Jedná se o takzvané
integrální křivky. Na první pohled se zdá, že pohyb je nefyzikální, protože
někde se integrální křivky sbíhají a jinde rozbíhají. Pokud bychom uvažovali
nestlačitelnou tekutinu bez zdrojů a spotřebičů, byla by to i pravda. Ale
uvědomme si, že pokud je přenášenou veličinou například vlhkost ve dřevě, tak
se tato veličina může kumulovat tak, že dřevo v daném místě prostě zvyšuje
svoji vlhkost. Při proudění tepla zase může růst nebo klesat teplota. A růst
vlhkosti nebo teploty jsou všechno přirozené jevy doprovázející přenos látky
nebo energie.

Pokud v nějakém bodě potřebujeme posoudit, zda tok slábne nebo zesiluje,
nakreslíme si okolo tohoto bodu malou oblast. Kružnici, čtvereček nebo cokoliv
vhodného. Na tuto oblast se zaměříme a studiem toku podél hranice vyhodnotíme,
jestli do oblasti více přitéká než odtéká nebo naopak. Při vyhodnocení toku je
důležité si uvědomit, že větší příspěvek k celkovému toku nastane tam, kde je
vyšší rychlost a směr více kolmý k hranici množiny. Je to jako plachta co
nabírá vítr. Největší účinek pozorujeme, pokud je vítr silný a plachta je kolmo
na jeho směr. Abychom mohli situaci co nejlépe vyhodnotit, budeme pracovat i s
délkou vektoru a barevně odlišíme vektory směřující dovnitř a ven. V tomto
prvním případě vidíme opticky jasnou převahu toku ven. To znamená, že v daném
místě tok zesiluje. V takovém případě je divergence kladná. Numericky je rovna
celkovému zesílení toku dělenému obsahem sledované oblasti. Pro přesnou
definici je nutné stáhnout rozměry oblasti k nule tak jak to děláme při
limitním přechodu v definici derivace. To je však nad rámec tohoto videa. Teď
se spokojíme s podílem jako s numerickou aproximací divergence.

Dívejte se na chování toku v jednotlivých bodech a případně si zastavujte a
vracejte video pro bližší prozkoumání situace. Někdy je bilance toku jasná, ale
někdy příliš zřetelné zda převažuje tok dovnitř či ven není. Pochopitelně se
nemusíme spoléhat na odhad podle obrázku. Umíme tok vypočítat i přesně. To se
naučíme v kapitole s křivkovým integrálem. Byla by to teď však zbytečně silná
zbraň. Teď posuzujme tok pouze opticky a v další části tohoto videa si ukážeme,
že k měření toho, zda tok sílí a jak moc, nám stačí parciální derivace a jeden
zajímavý trik.

Prohlížejte si různé situace, všímejte si, že divergence je kladná v místě, kde
tok sílí a záporná tam kde slábne. Že divergence je numericky velká tam, kde je
naprostá převaha toku ven nebo dovnitř. Všímejte si také, že nezáleží vůbec na
tom, zda tok teče doleva či doprava. Ve všech případech sledujeme, zda se podél
toku jeho intenzita zvyšuje. Pokud ano, je divergence kladná. Pokud se tok
zvyšuje hodně, je divergence hodně kladná a podobná situace je i v dalších
případech.

Zůstává otázka, co s případy, kdy je rozdíl mezi přítokem a odtokem málo
výrazný a také otázka, jak vyčíslit divergenci numericky. Ukážeme si to na
dalším vektorovém poli, tentokrát s méně výraznými změnami než v předchozím.
Vidíme převahu toku dovnitř, ale není nijak výrazná a rádi bychom ji vyčíslili.

Základní taktika, kterou použijeme, je v matematice oblíbené převedení úlohy na
jinou úlohu, kterou už umíme vyřešit. A pro proudění umíme řešit
jednodimenzionální úlohu. V takovém případě se proudění odehrává v jednom
směru. Nárůst toku v tomto směru je derivace toku podle prostorové proměnné.
Proto rozložíme jedno proudění ve dvou dimenzích na dvě jednodimenzionální
proudění. K tomu potřebujeme kartézské souřadnice. Osu x budeme orientovat jak
je obvyklé, vodorovně doprava. Osu y orientujeme svisle nahoru. Tok rozdělíme
na komponenty ve směru těchto os. Tím máme v každém bodě dvě nezávislé
jednodimenzionální úlohy. Každou jednodimenzionální úlohu zpracujeme samostatně
a sečteme jejich výsledky. Označíme-li komponentu proudění ve směru vodorovné
osy P a komponentu ve směru svislé osy Q, stačí pro nárůst toku určit derivace
podle prostorových proměnných. Komponenta P teče podél osy x a proto její
nárůst odhalíme pomocí derivace podle x. Komponenta Q teče podél osy y a její
nárůst určíme derivováním podle proměnné y. V detailu vidíme, že veličina P
roste, šipky se prodlužují. Proto je derivace P podle x kladná a tok zesiluje.
Naopak, veličina Q slábne a to výrazněji než P, potože mezi šipkami jsou větší
rozdíly. Proto je derivace Q podle y záporná a v absolutní hodnotě numericky
vetší než derivace P podle x. Konkrétní hodnoty pro funkci použitou v animaci
vidíme na obrazovce. Divergence je poté součtem obou derivací a protože
převažuje záporná hodnota, tok jako celek slábne a má zápornou divergenci.

Tím je naše mise u cíle. Ukázali jsme si rovnici kontinuity, základní rovnici
pro studium transportních dějů. Součástí této rovnice je operátor divergence.
Ten popisuje intenzitu s jakou vektorové pole zesiluje. Ukázali jsme si
interpretaci divergence a také metodu výpočtu pomocí parciálních derivací.

"""