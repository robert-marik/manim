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
        title = Title(r"Vektorov?? pole a jeho divergence").add_background_rectangle(buff=0.5).set_z_index(10)
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
                [-4.8,-2,0,[r"P??eva??uje tok ven z kruhu."]],
                [-2.6,-0.3,0,[r"P??eva??uje tok dovnit?? do kruhu."]],
                [2,-1.5,0,[r"M??rn?? p??evaha toku ven z kruhu."]],
                [-4,-1,0,[r"Nejasn?? situace pro posouzen?? jenom podle obr??zku.",r"Divergence bude numericky bl??zko k nule."]],
                [-1,1,0,[r"P??evaha toku ven. Tok je pomal?? (kr??tk?? vektory)."]],
                [0.5,3,0,[r"Tok dovnit?? je vy?????? ne?? ven."]],
                [-3.5,2.3,0,[r"P??eva??uje tok ven.",r"Nehraje roli zda doleva nebo doprava."]],
                [-6,1.6,0,[r"P??evaha toku ven,",r"na opa??nou stranu ne?? v p??edchoz??m p????pad??."]],
                [-6,3.3,0,[r"Naprost?? dominance toku dovnit??."]]
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
        title = Title(r"Divergence v kart??zsk??ch sou??adnic??ch")
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

        popis = Tex(r"Jedna t????k?? dvoudimenzion??ln?? ??loha.")
        popis2 = Tex(r"Dv?? snadn?? jednodimenzion??ln?? ??lohy.")
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
        autor = VGroup(Tex("Robert Ma????k"),Tex("Mendel University")).arrange(DOWN).next_to(title,DOWN)
        self.play(GrowFromCenter(title))
        self.play(GrowFromCenter(autor[0]))
        self.play(GrowFromCenter(autor[1]))
        self.wait()
        aplikace = VGroup(*[Tex(_) for _ in ["veden?? tepla", "difuze", "su??en?? d??eva",  "proud??n?? podzemn?? vody"]]).arrange(DOWN).next_to(autor,DOWN, buff=2)
        for i,c in enumerate([RED,BLUE,ORANGE,YELLOW]):
            aplikace[i].set_color(c)
        self.play(AnimationGroup(*[GrowFromCenter(_) for _ in aplikace], lag_ratio=0.95), run_time=5)

        self.wait()

class Motivace(Scene):
    def construct(self):

        bilance = VGroup(
            Tex(r"N??r??st mno??stv?? (prvn?? verze):"),
            Tex(r"Mno??stv?? vygenerovn?? zdroji"),
            Tex(r"Mno??stv?? spot??ebovan?? spot??ebi??i"),
            Tex(r"Mno??stv?? dodan?? tokem"),
            Tex(r"Mno??stv??, kter?? odteklo")
        ).arrange(DOWN, aligned_edge=LEFT).to_edge(UP)

        bilance2 = VGroup(
            Tex(r"N??r??st mno??stv?? (zkr??cen?? verze):"),
            Tex(r"P????sp??vek ze zdroj?? a spot??ebi????"),
            Tex(r"Celkov?? bilance toku")
        ).arrange(DOWN, aligned_edge=LEFT).next_to(bilance,DOWN, aligned_edge=LEFT)

        bilance3 = VGroup(
            Tex(r"N??r??st mno??stv?? (pomoc?? intenzity toku):"),
            Tex(r"P????sp??vek ze zdroj?? a spot??ebi????"),
            Tex(r"Sn????en?? intenzity toku")
        ).arrange(DOWN, aligned_edge=LEFT).next_to(bilance2,DOWN, aligned_edge=LEFT)

        bilance4 = VGroup(
            Tex(r"N??r??st mno??stv?? (pomoc?? n??r??stu toku):"),
            Tex(r"P????sp??vek ze zdroj?? a spot??ebi????"),
            Tex(r"Zes??len?? toku")
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
            Tex(r"??len $\nabla\cdot \vec q$ je divergence vektorov??ho pole $\vec q$."),
            Tex(r"Znak $\nabla$ je oper??tor nabla."),
        ).arrange(DOWN, aligned_edge=LEFT).next_to(rovnice,DOWN)

        self.play(*[FadeOut(_) for _ in [bilance,bilance2,bilance3]])
        self.play(FadeIn(rovnice[1]))
        self.play(ReplacementTransform(bilance4[0].copy(),rovnice[0]),run_time=4)
        self.play(ReplacementTransform(bilance4[1].copy(),rovnice[2]),run_time=4)
        self.play(ReplacementTransform(bilance4[2].copy(),VGroup(rovnice[3],rovnice[4])),run_time=4)

        self.play(FadeIn(cleny))
        self.wait()
        

komentar = """

Dobr?? den, v??tejte u videa, ve kter??m se sezn??m??me s pojmem divergence a
vyu??ijeme jej p??i sestaven?? rovnice kontinuity. Mo??nou aplikac?? je popis
libovoln??ho transportn??ho d??je, jako nap????klad veden?? tepla, difuze, su??en??
d??eva nebo proud??n?? podzemn?? vody.

P??edstavme si cokoliv co proud?? a m????e se kumulovat. V tomto kontextu se obvykle
mluv?? o hustot?? stavov?? veli??iny v dan??m bod?? a jej??m toku t??mto bodem, ale
p??edstavujte si klidn?? vodu v jeze??e. Jezero m????e m??t pramen a m????e z n??j b??t
voda odeb??r??na k zavla??ov??n??. Tedy m????e zde b??t zdroj a spot??ebi??. Obvykle m??
jezero n??jak?? p????tok a n??jak?? odtok. Do celkov?? bilance tedy vstupuj?? ??ty??i
faktory. Dva p??sob?? kladn?? a dva ??erven?? z??porn??. Toto m????eme je??t??
zjednodu??it, pokud budeme dva a dva faktory uva??ovat spole??n??. Spot??ebi??e
budeme br??t jako zdroje se z??porn??m ????inkem a odtok jako z??porn?? p????tok nebo
naopak. T??m se situace zjednodu???? ze ??ty?? ??len?? na dva ??leny.

Prvn?? souvis?? se zdroji a spot??ebi??i a druh?? s tokem. P??esn??ji, n??r??st veli??iny
v dan??m m??st?? je roven mno??stv?? o kolik je odtok men???? ne?? p????tok. Tedy
mno??st??, o kolik je tok zeslaben. Aby koncept l??pe zapadl do obvykl??ho postupu,
kdy p??irozen?? sledujeme r??st veli??in, budeme m??sto se zeslaben??m toku pracovat
se zes??len??m toku a zapo????t??vat ho z??porn??.

A u?? n??m nic nebr??n?? sestavit z??kladn?? rovnici pou????vanou pro popis
transportn??ch d??j??. Proto??e tok vztahujeme k jednotce ??asu, vzt??hneme k
jednotce ??asu celou bilanci. N??r??st sledovan?? veli??iny za jednotku ??asu je
derivace podle ??asu. To dob??e zn??me, proto??e to je slovn?? interpretace
parci??ln?? derivace. P????r??stek ze spole??n??ho p??soben?? zdroj?? a spot??ebi???? mus??
b??t sou????st?? formulace ??lohy. Ozna????me jej sigma, to je druh?? ??len do na????
bilance. Chyb?? u?? jenom t??et?? ??len, kter??m kvantifikujeme zesilov??n?? toku.

Tok q p??en????ej??c?? stavovou veli??inu m?? velikost a sm??r. Je to tedy vektorov??
funkce nebo t???? vektorov?? pole. Zavedeme speci??ln?? oper??tor ud??vaj??c?? n??r??st
tohoto toku. Tento oper??tor se naz??v?? divergence, ozna??uje symbolem nabla,
zapisujeme jako troj??heln??k vrcholem dol??.

Tak??e jak divergence funguje, jak ji naj??t a co vyjad??uje?

Uva??ujme vektorov?? pole jako na obr??zku. Pro p??ehlednost jsou v n??m v??echny
p????li?? dlouh?? vektory zkr??ceny na stejnou d??lku a p??vodn?? d??lka je zak??dov??na v
barv??. P??edstavme si tyto vektory jako rychlostn?? pole a d??vejme se na
trajektorie objekt??, kter?? se podle n??j budou pohybovat. Jedn?? se o takzvan??
integr??ln?? k??ivky. Na prvn?? pohled se zd??, ??e pohyb je nefyzik??ln??, proto??e
n??kde se integr??ln?? k??ivky sb??haj?? a jinde rozb??haj??. Pokud bychom uva??ovali
nestla??itelnou tekutinu bez zdroj?? a spot??ebi????, byla by to i pravda. Ale
uv??domme si, ??e pokud je p??en????enou veli??inou nap????klad vlhkost ve d??ev??, tak
se tato veli??ina m????e kumulovat tak, ??e d??evo v dan??m m??st?? prost?? zvy??uje
svoji vlhkost. P??i proud??n?? tepla zase m????e r??st nebo klesat teplota. A r??st
vlhkosti nebo teploty jsou v??echno p??irozen?? jevy doprov??zej??c?? p??enos l??tky
nebo energie.

Pokud v n??jak??m bod?? pot??ebujeme posoudit, zda tok sl??bne nebo zesiluje,
nakresl??me si okolo tohoto bodu malou oblast. Kru??nici, ??tvere??ek nebo cokoliv
vhodn??ho. Na tuto oblast se zam??????me a studiem toku pod??l hranice vyhodnot??me,
jestli do oblasti v??ce p??it??k?? ne?? odt??k?? nebo naopak. P??i vyhodnocen?? toku je
d??le??it?? si uv??domit, ??e v??t???? p????sp??vek k celkov??mu toku nastane tam, kde je
vy?????? rychlost a sm??r v??ce kolm?? k hranici mno??iny. Je to jako plachta co
nab??r?? v??tr. Nejv??t???? ????inek pozorujeme, pokud je v??tr siln?? a plachta je kolmo
na jeho sm??r. Abychom mohli situaci co nejl??pe vyhodnotit, budeme pracovat i s
d??lkou vektoru a barevn?? odli????me vektory sm????uj??c?? dovnit?? a ven. V tomto
prvn??m p????pad?? vid??me opticky jasnou p??evahu toku ven. To znamen??, ??e v dan??m
m??st?? tok zesiluje. V takov??m p????pad?? je divergence kladn??. Numericky je rovna
celkov??mu zes??len?? toku d??len??mu obsahem sledovan?? oblasti. Pro p??esnou
definici je nutn?? st??hnout rozm??ry oblasti k nule tak jak to d??l??me p??i
limitn??m p??echodu v definici derivace. To je v??ak nad r??mec tohoto videa. Te??
se spokoj??me s pod??lem jako s numerickou aproximac?? divergence.

D??vejte se na chov??n?? toku v jednotliv??ch bodech a p????padn?? si zastavujte a
vracejte video pro bli?????? prozkoum??n?? situace. N??kdy je bilance toku jasn??, ale
n??kdy p????li?? z??eteln?? zda p??eva??uje tok dovnit?? ??i ven nen??. Pochopiteln?? se
nemus??me spol??hat na odhad podle obr??zku. Um??me tok vypo????tat i p??esn??. To se
nau????me v kapitole s k??ivkov??m integr??lem. Byla by to te?? v??ak zbyte??n?? siln??
zbra??. Te?? posuzujme tok pouze opticky a v dal???? ????sti tohoto videa si uk????eme,
??e k m????en?? toho, zda tok s??l?? a jak moc, n??m sta???? parci??ln?? derivace a jeden
zaj??mav?? trik.

Prohl????ejte si r??zn?? situace, v????mejte si, ??e divergence je kladn?? v m??st??, kde
tok s??l?? a z??porn?? tam kde sl??bne. ??e divergence je numericky velk?? tam, kde je
naprost?? p??evaha toku ven nebo dovnit??. V????mejte si tak??, ??e nez??le???? v??bec na
tom, zda tok te??e doleva ??i doprava. Ve v??ech p????padech sledujeme, zda se pod??l
toku jeho intenzita zvy??uje. Pokud ano, je divergence kladn??. Pokud se tok
zvy??uje hodn??, je divergence hodn?? kladn?? a podobn?? situace je i v dal????ch
p????padech.

Z??st??v?? ot??zka, co s p????pady, kdy je rozd??l mezi p????tokem a odtokem m??lo
v??razn?? a tak?? ot??zka, jak vy????slit divergenci numericky. Uk????eme si to na
dal????m vektorov??m poli, tentokr??t s m??n?? v??razn??mi zm??nami ne?? v p??edchoz??m.
Vid??me p??evahu toku dovnit??, ale nen?? nijak v??razn?? a r??di bychom ji vy????slili.

Z??kladn?? taktika, kterou pou??ijeme, je v matematice obl??ben?? p??eveden?? ??lohy na
jinou ??lohu, kterou u?? um??me vy??e??it. A pro proud??n?? um??me ??e??it
jednodimenzion??ln?? ??lohu. V takov??m p????pad?? se proud??n?? odehr??v?? v jednom
sm??ru. N??r??st toku v tomto sm??ru je derivace toku podle prostorov?? prom??nn??.
Proto rozlo????me jedno proud??n?? ve dvou dimenz??ch na dv?? jednodimenzion??ln??
proud??n??. K tomu pot??ebujeme kart??zsk?? sou??adnice. Osu x budeme orientovat jak
je obvykl??, vodorovn?? doprava. Osu y orientujeme svisle nahoru. Tok rozd??l??me
na komponenty ve sm??ru t??chto os. T??m m??me v ka??d??m bod?? dv?? nez??visl??
jednodimenzion??ln?? ??lohy. Ka??dou jednodimenzion??ln?? ??lohu zpracujeme samostatn??
a se??teme jejich v??sledky. Ozna????me-li komponentu proud??n?? ve sm??ru vodorovn??
osy P a komponentu ve sm??ru svisl?? osy Q, sta???? pro n??r??st toku ur??it derivace
podle prostorov??ch prom??nn??ch. Komponenta P te??e pod??l osy x a proto jej??
n??r??st odhal??me pomoc?? derivace podle x. Komponenta Q te??e pod??l osy y a jej??
n??r??st ur????me derivov??n??m podle prom??nn?? y. V detailu vid??me, ??e veli??ina P
roste, ??ipky se prodlu??uj??. Proto je derivace P podle x kladn?? a tok zesiluje.
Naopak, veli??ina Q sl??bne a to v??razn??ji ne?? P, poto??e mezi ??ipkami jsou v??t????
rozd??ly. Proto je derivace Q podle y z??porn?? a v absolutn?? hodnot?? numericky
vet???? ne?? derivace P podle x. Konkr??tn?? hodnoty pro funkci pou??itou v animaci
vid??me na obrazovce. Divergence je pot?? sou??tem obou derivac?? a proto??e
p??eva??uje z??porn?? hodnota, tok jako celek sl??bne a m?? z??pornou divergenci.

T??m je na??e mise u c??le. Uk??zali jsme si rovnici kontinuity, z??kladn?? rovnici
pro studium transportn??ch d??j??. Sou????st?? t??to rovnice je oper??tor divergence.
Ten popisuje intenzitu s jakou vektorov?? pole zesiluje. Uk??zali jsme si
interpretaci divergence a tak?? metodu v??po??tu pomoc?? parci??ln??ch derivac??.

"""