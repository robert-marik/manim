from manim import *
from manim_editor import PresentationSectionType

import numpy as np

AnimationRuntime = 1
WaitTime = 2

class Deformation(ThreeDScene):
    def construct(self):

        self.next_section("Tenzor deformace")        

        title = Title(r"Tenzor deformace a jeho transformace")
        autor = VGroup(Tex("Robert Mařík"),Tex("Mendel University")).arrange(DOWN).next_to(title,DOWN)
        self.play(AnimationGroup(GrowFromCenter(title),GrowFromCenter(autor[0]),GrowFromCenter(autor[1]),lag_ratio=0.2))
        self.wait(5)
        
        self.next_section("Popis ulohy")        

        self.play(FadeOut(title),FadeOut(autor))
        rct = Rectangle(color=GREEN, width=6, height=2, fill_opacity=0.5 ) 
        square = Square(color=BLUE, side_length=1, fill_opacity=1)
        squareL = square.copy().set_color(WHITE).shift(LEFT*2)
        squareR = square.copy().set_color(WHITE).shift(RIGHT*2)
        squareC = square.copy().set_color(RED).rotate(45 * DEGREES)
        tenzor1={}
        tenzor1['O'] = Matrix([[r'\varepsilon_{xx}', r'\varepsilon_{xy}'], [r'\varepsilon_{xy}',r'\varepsilon_{yy}']]).to_corner(UL)
        tenzor1['D'] = Matrix([[0.5, 0], [0,"-0.1"]]).to_corner(UL)
        tenzor1['N'] = Matrix([[0, 0], [0,0]]).to_corner(UL)

        zacatek = np.array([0,0,0])
        arrow_x = Arrow(start=zacatek, end=RIGHT, color=WHITE, buff=0)
        arrow_y = arrow_x.copy().rotate(90*DEGREES, about_point=zacatek)
        popisek_x = MathTex(r"x").next_to(arrow_x,RIGHT)
        popisek_y = MathTex(r"y").next_to(arrow_y,UP)
        osy = VGroup(arrow_x,arrow_y,popisek_x,popisek_y).next_to(tenzor1["O"],RIGHT,buff=1)

        tenzor2 = {}
        tenzor2['O'] = Matrix([[r"\varepsilon_{x'x'}", r"\varepsilon_{x'y'}"], [r"\varepsilon_{x'y'}",r"\varepsilon_{y'y'}"]]).to_edge(UR).set_color(RED)
        tenzor2['D'] = Matrix([["0.2", "-0.3"], ["-0.3","0.2"]]).to_edge(UR).set_color(RED)
        tenzor2['N'] = Matrix([["0", "0"], ["0","0"]]).to_edge(UR).set_color(RED)        
        tenzor=[tenzor1["O"],tenzor2["O"]]

        arrow_xr = Arrow(start=zacatek, end=RIGHT, color=RED, buff=0)
        arrow_yr = arrow_xr.copy().rotate(90*DEGREES, about_point=zacatek)
        popisek_xr = MathTex(r"x'", color=RED).rotate(-45*DEGREES).next_to(arrow_xr,RIGHT)
        popisek_yr = MathTex(r"y'", color=RED).rotate(-45*DEGREES).next_to(arrow_yr,UP)
        osyr = VGroup(arrow_xr,arrow_yr,popisek_xr,popisek_yr).rotate(45*DEGREES, about_point=zacatek).next_to(tenzor2["O"],LEFT,buff=1)
        
        vg = VGroup(rct)
        vg2 = rct.copy()
        vg1 = rct.copy()
        vg1.shift(LEFT*1.55)
        vg2.stretch(1.5,0)
        vg2.stretch(0.9,1) 

        tvg = vg.copy()
        tvg1 = vg1.copy()
        tvg2 = vg2.copy()

        title = Title(r"Deformace elastického pásu").to_edge(UP)
        self.play(FadeIn(title))

        popis = VGroup(
            Tex(r"$\bullet $ Pás natažením prodloužíme o polovinu délky"),
            Tex(r"$\bullet $ Pás se natažením zúží o desetinu")
        ).arrange(DOWN,aligned_edge=LEFT).next_to(title,DOWN)
        self.play(FadeIn(tvg),FadeIn(popis))
        self.play(ReplacementTransform(tvg, tvg1), run_time=3*AnimationRuntime)
        self.wait(WaitTime)
        self.play(ReplacementTransform(tvg1, tvg2), run_time=3*AnimationRuntime)
        self.wait(WaitTime)

        self.next_section("Zavedeni souradnic")        

        self.play(FadeOut(popis), FadeOut(title))

        temp = VGroup(osy)

        self.play(FadeIn(temp))
        self.wait(duration=WaitTime)


        self.play(FadeIn(osyr))
        self.wait(duration=WaitTime)


        self.play(ReplacementTransform(tvg2,rct))

        self.play(FadeIn(tenzor1["O"]))
        self.wait(duration=WaitTime)

        self.play(FadeIn(tenzor2["O"]))
        self.wait(duration=WaitTime)
        
        vg = VGroup()
        vg.add(rct,squareL, squareR, squareC)

        self.wait(WaitTime)
        self.play(FadeIn(square))
        self.wait(duration=WaitTime)

        self.play(
            ReplacementTransform(square, squareL),
            ReplacementTransform(square.copy(), squareR),
            ReplacementTransform(square.copy(), squareC)
        )
        self.wait(duration=WaitTime)

        self.next_section("Komponenty tenzoru 1")        

        b1 = VGroup(Brace(squareL, color=YELLOW),Brace(squareR, color=YELLOW))
        b2 = VGroup(Brace(squareL, direction=LEFT, color=YELLOW),Brace(squareR, direction=LEFT, color=YELLOW))
        b3 = Brace(squareC, direction=LEFT+DOWN, color=YELLOW)
        b4 = Brace(squareC, direction=RIGHT+DOWN, color=BLUE)

        angle1= VGroup(*[Arc(
                radius=0.3,
                start_angle=0*DEGREES,
                angle =90*DEGREES,
                color=YELLOW, stroke_width=8
            ).move_to(_,aligned_edge=DL) for _ in [squareL,squareR] ])
        angle2= Arc(
                radius=0.3,
                start_angle=45*DEGREES,
                angle =90*DEGREES,
                color=YELLOW, stroke_width=8
            ).shift(squareC.get_bottom()*UP)    
  
        def explain_element(tensor,element,marker=[], extracolor = None):
            temp1 = VGroup(*[SurroundingRectangle(tensor.get_entries()[_]) for _ in element],*marker)
            # temp2 = Text(text).scale(0.75).next_to(vg,DOWN).to_edge(LEFT)
            if extracolor is not None:
                temp1[0].set_color(extracolor)
            self.play(FadeIn(temp1))
            return(temp1)

        t = explain_element(tenzor1["O"],[0],marker=[b1])
        self.wait(duration=WaitTime)

        self.next_section("Komponenty tenzoru 2")        
        self.play(FadeOut(t))
        t = explain_element(tenzor1["O"],[3],marker=[b2])
        self.wait(duration=WaitTime)

        self.next_section("Komponenty tenzoru 3")        
        self.play(FadeOut(t))
        t = explain_element(tenzor1["O"],[1,2],marker=[angle1])
        self.wait(duration=WaitTime)

        self.next_section("Komponenty tenzoru 4")        
        # This rotates the 2D scene to 3D and back
        angle11= VGroup(*[angle1[0].copy().flip(RIGHT).set_color(BLUE).move_to(_,aligned_edge=UL) for _ in [squareL,squareR] ])
        self.play(FadeIn(angle11))
        self.wait(WaitTime)
        rotation_axis = DashedLine(start=[-4,0,0], end = [4,0,0], color=YELLOW)
        self.play(FadeIn(rotation_axis))
        self.wait(WaitTime)

        self.move_camera(
            phi=30 * DEGREES,
            theta=-50 * DEGREES
        )
        
        def update_drawing(d,dt):
            d.rotate_about_origin(dt, RIGHT)

        [_.add_updater(update_drawing) for _ in [*vg,angle11,angle1]]
        
        self.wait(PI)
        [_.remove_updater(update_drawing) for _ in [*vg,angle11,angle1]]

        self.move_camera(
            phi=0 * DEGREES,
            theta=-90 * DEGREES
        )
        self.wait(3*WaitTime)
        # end of 3D stuff

        self.next_section("Komponenty tenzoru 4b")        
        self.play(FadeOut(t), FadeOut(angle11), FadeOut(rotation_axis))

        t = explain_element(tenzor2["O"],[0,3],marker=[b3,b4], extracolor=BLUE)
        self.wait(duration=WaitTime)

        rotation_axis = DashedLine(start=[0,-2,0], end = [0,2,0], color=YELLOW)
        self.play(FadeIn(rotation_axis))
        self.wait(duration=WaitTime)
        
        # This rotates the 2D scene to 3D and back
        self.move_camera(
            phi=30 * DEGREES,
            theta=-50 * DEGREES
        )
        
        def update_drawing(d,dt):
            d.rotate_about_origin(dt, UP)

        [_.add_updater(update_drawing) for _ in [*vg,b3,b4]]
        
        self.wait(PI)
        [_.remove_updater(update_drawing) for _ in [*vg,b3,b4]]

        self.move_camera(
            phi=0 * DEGREES,
            theta=-90 * DEGREES
        )
        self.wait(WaitTime)
        # end of 3D stuff        

        self.next_section("Komponenty tenzoru 5")        

        self.play(FadeOut(t), FadeOut(rotation_axis))
        t = explain_element(tenzor2["O"],[1,2],marker=[angle2])
        self.wait(duration=WaitTime)

        self.next_section("Vlastni deformace")        
        self.play(FadeOut(t))

        vg2 = vg.copy()
        vg1 = vg.copy()
        vg1.shift(LEFT*1.55)
        vg2.stretch(1.5,0)
        vg2.stretch(0.9,1)

        self.play(
            ReplacementTransform(tenzor1["O"], tenzor1["N"]),
            ReplacementTransform(tenzor2["O"], tenzor2["N"]),
        )

        self.play(ReplacementTransform(vg, vg1))

        self.wait(WaitTime)

        self.play(ReplacementTransform(vg1,vg2), \
            ReplacementTransform(tenzor1["N"], tenzor1["D"]), \
            ReplacementTransform(tenzor2["N"], tenzor2["D"]), 
            run_time=AnimationRuntime)
        self.wait(WaitTime)    

        #self.clear()

class Transformace(Scene):


    def MatrixProduct(self,A,B,C,run_time=AnimationRuntime):
        """
        The function takes three matrices 2x2 as argument and animates the mutliplication using linear combination of columns.
        """
        a = A.copy()
        b = B.copy()
        c = C.copy()
        self.play(FadeIn(C.get_brackets()))
        cols_c = c.get_columns()
        for i in [0,1]:
            cols = a.copy().get_columns()
            for _,__ in zip(A.get_columns(),[YELLOW,RED]):
                _.set_color(__)
            print(cols)
            coefs = b.copy().get_columns()[i]

            opt_plus = MathTex("+")
            if float(str(coefs[1]).split("'")[1]) < 0:
                opt_plus = Text(".").set_color(BLACK)
            lincomb = VGroup(
                coefs[0].set_color(PINK),
                Matrix([[cols[0][0]],[cols[0][1]]],element_to_mobject=lambda x: x).set_color(YELLOW),
                opt_plus,
                coefs[1].set_color(PINK),
                Matrix([[cols[1][0]],[cols[1][1]]],element_to_mobject=lambda x: x).set_color(RED),
                MathTex("="),
                Matrix([[cols_c[i][0]],[cols_c[i][1]]],element_to_mobject=lambda x: x).set_color(BLUE)).arrange(RIGHT).to_corner(DL)
            B.get_columns()[i].set_color(PINK)
            self.play(AnimationGroup(
                ReplacementTransform(B.copy().get_columns()[i][0],lincomb[0]),
                AnimationGroup(ReplacementTransform(A.copy().get_brackets().copy(),lincomb[1].get_brackets()),
                ReplacementTransform(A.get_columns().copy()[0],lincomb[1].get_columns()[0])),
                FadeIn(lincomb[2]),
                ReplacementTransform(B.copy().get_columns()[i][1],lincomb[3]),
                AnimationGroup(ReplacementTransform(A.copy().get_brackets(),lincomb[4].get_brackets()),
                ReplacementTransform(A.get_columns().copy()[1],lincomb[4].get_columns()[0])),
                FadeIn(lincomb[5]),
                lag_ratio=0.6
            ))    
            self.wait()
            self.play(FadeIn(lincomb[6]))
            self.wait()
            temp = lincomb.copy()[6].get_columns()[0]
            self.play(ReplacementTransform(temp,C.get_columns()[i]))
            self.wait()
            self.play(
                FadeOut(lincomb),
                FadeToColor(A,WHITE),
                FadeToColor(B,WHITE)
                )
    
    def construct(self):

        self.next_section("Rovnice")        
        title = Title(r"Odvození rovnice pro transformaci tenzorů").to_edge(UP)
        self.play(FadeIn(title))
        self.wait(WaitTime)         
        lines = MathTex(
            r"{{V}} &= {{A}} {{U}}\\",
            r"{{RV'}} &= {{A}} {{R U'}}\\",
            r"{{V'}} &= {{ R^{-1} }} {{A}} {{R U'}}\\",
            r"{{V'}} &= {{(R^{-1} A R)}} {{U'}}"
        )
        print(len(lines))
        groups = [
            lines[:5],
            lines[5:11],
            lines[11:19],
            lines[19:]
            ]

        self.play(FadeIn(groups[0]))
        self.wait(WaitTime)
        for i in [0,1,2]:
            self.play(
            TransformMatchingShapes(
                groups[i].copy(), 
                groups[i+1], 
                path_arc=90 * DEGREES)
            ),
            self.wait(WaitTime)           

        self.wait(WaitTime)         

        svorka = Brace(lines[-3], direction=DOWN)
        popisek = svorka.get_text("Tenzor v čárkované soustavě souřadnic")
        lines[-3].set_color(YELLOW)
        self.play(FadeIn(svorka), FadeIn(popisek), run_time=AnimationRuntime)
        self.wait(WaitTime)

        self.next_section("Matice transformace")        
        self.clear()

        # nalezeni matice transformace
        theta = 20

        number_plane = NumberPlane(
        x_range=[-2, 2, .5],
        y_range=[-2, 2, .5],
        background_line_style={
                        "stroke_color": GREEN
                    }
        )#.scale(0.5)
        zacatek = np.array([0,0,0])
        e1 = Arrow(start=zacatek, end=2*RIGHT, color=RED, buff=0)
        e2 = e1.copy()
        e2.rotate_about_origin(90*DEGREES)
        circ = Circle(radius=2.0,color=WHITE, stroke_width=3)
        e12 = VGroup(e1,e2)
        e12_r = e12.copy()
        e12_r.rotate_about_origin(theta*DEGREES)
        
        line1 = Line(start=[2*np.cos(theta*DEGREES),2*np.sin(theta*DEGREES),0],end=[2*np.cos(theta*DEGREES),0,0],color= YELLOW, stroke_width=6)
        line1r = line1.copy().rotate_about_origin(90*DEGREES)
        line2 = Line(start=[2*np.cos(theta*DEGREES),0,0],end=[0,0,0],color= BLUE,stroke_width=6)
        line2r = line2.copy().rotate_about_origin(90*DEGREES)

        #e1_coor=np.ndarray([np.cos(theta),np.sin(theta)])
        #e2_coor=np.ndarray([-np.sin(theta),np.cos(theta)])
        self.play(FadeIn(number_plane), run_time=AnimationRuntime)
        self.play(Create(e12), run_time=AnimationRuntime)
        self.wait(WaitTime)
        self.play(AnimationGroup(
            Create(circ),
            ReplacementTransform(e12,e12_r),
            lag_ratio=0.4, run_time=AnimationRuntime))
        self.wait(WaitTime)

        h_buf = 2
        v_buf = 1.5
        e1r_text = Matrix([[r"\cos(\theta)",r"\sin(\theta)"]],h_buff=h_buf).next_to(e1.get_end(), RIGHT)
        e2r_text = Matrix([[r"-\sin(\theta)",r"\cos(\theta)"]],h_buff=h_buf).next_to(e2.get_end(), UP)

        self.play(FadeIn(e1r_text), run_time=AnimationRuntime)
        self.play(Create(line1), run_time=AnimationRuntime)
        self.play(Create(line2), run_time=AnimationRuntime)
        
        self.wait(WaitTime)
        self.play(ReplacementTransform(line1.copy(),line1r), run_time=AnimationRuntime)
        self.play(ReplacementTransform(line2.copy(),line2r), run_time=AnimationRuntime)
        self.play(FadeIn(e2r_text), run_time=AnimationRuntime)

        self.play(AnimationGroup(*[_.animate.shift(2*DOWN,LEFT) for _ in self.mobjects],lag_ratio=0.02))

        R_theta = Matrix([[r"\cos(\theta)", r"-\sin(\theta)"], 
            [r"\sin(\theta)",r"\cos(\theta)"]], h_buff=h_buf).to_edge(UL)
        R0 = Matrix([[r"\frac{\sqrt 2}{2}",r"-\frac{\sqrt 2}{2}"],[r"\frac{\sqrt 2}{2}",r"\frac{\sqrt 2}{2}"]],
            v_buff=v_buf).to_edge(UR)
        R = VGroup(MathTex(r"\frac{\sqrt 2}{2}"), Matrix([[r"1", r"-1"], [r"1",r"1"]]))
        R.arrange(RIGHT, buff=0.5).to_edge(UR)

        self.play(FadeIn(R_theta.get_brackets()))
        self.play(
            ReplacementTransform(e1r_text.get_entries()[0].copy(),R_theta.get_entries()[0]),
            ReplacementTransform(e1r_text.get_entries()[1].copy(),R_theta.get_entries()[2]), 
            run_time=3*AnimationRuntime
            )
        self.play(
            ReplacementTransform(e2r_text.get_entries()[0].copy(),R_theta.get_entries()[1]),
            ReplacementTransform(e2r_text.get_entries()[1].copy(),R_theta.get_entries()[3]), 
            run_time=3*AnimationRuntime
            )
        self.wait(WaitTime)
        self.play(ReplacementTransform(R_theta.copy(),R0), run_time=3*AnimationRuntime)
        self.wait(WaitTime)
        self.play(ReplacementTransform(R0,R), run_time=3*AnimationRuntime)
        self.wait(WaitTime)
        self.next_section("Nasobeni matic")        
        
        self.play(AnimationGroup(*[FadeOut(_) for _ in self.mobjects],lag_ratio=0.05))

        # Nasobeni matic

        R = VGroup(MathTex("R","=",r"\frac{\sqrt 2}{2}"), Matrix([[r"1", r"-1"], [r"1",r"1"]])).arrange(RIGHT).to_corner(UL)
        Rinv = VGroup(MathTex("R^{-1}","=",r"\frac{\sqrt 2}{2}"), Matrix([[r"1", r"1"], [r"-1",r"1"]])).arrange(RIGHT).next_to(R,RIGHT,buff=2)
        D = VGroup(MathTex("D","="), Matrix([[r"0.5", r"0"], [r"0",r"-0.1"]])).arrange(RIGHT).next_to(R,DOWN)

        vypocet = VGroup(MathTex("R^{-1}","D","R","=",r"\frac{\sqrt 2}{2}",r"\frac{\sqrt 2}{2}"),
            Matrix([[r"1", r"1"], [r"-1",r"1"]]),
            Matrix([[r"0.5", r"0"], [r"0",r"-0.1"]]),
            Matrix([[r"1", r"-1"], [r"1",r"1"]])
            ).arrange(RIGHT).next_to(D,DOWN,aligned_edge=LEFT)

        vypocet2 = VGroup(
            MathTex("=",r"\frac{1}{2}"),
            Matrix([[r"0.5", r"-0.1"], [r"-0.5",r"-0.1"]]),
            Matrix([[r"1", r"-1"], [r"1",r"1"]]),
            MathTex("=",r"\frac 12"),
            Matrix([[r"0.4", r"-0.6"], [r"-0.6",r"0.4"]])
            ).arrange(RIGHT)

        vypocet3 = VGroup(MathTex("="),
            Matrix([[r"0.2", r"-0.3"], [r"-0.3",r"0.2"]])
            ).arrange(RIGHT)

            
        for _ in [R,D]:
            self.play(Create(_),run_time=AnimationRuntime) 

        elementy = R[1].get_entries()
        e = Rinv[1].get_entries()

        self.wait()
        self.next_section("Nasobeni matic 2")        
        
        self.play(*[ReplacementTransform(what.copy(),where) for what,where in zip(
            [R[0][0],R[0][1],R[0][2],elementy[0],elementy[3],R[1].get_brackets()],
            [Rinv[0][0],Rinv[0][1],Rinv[0][2],e[0],e[3],Rinv[1].get_brackets()]
            )],run_time=2*AnimationRuntime, path_arc=PI/2)

        self.wait(WaitTime)

        sipky = VGroup(
            Arrow(start=elementy[1],end = e[2], buff=0.4, color=YELLOW),
            Arrow(start=elementy[2],end = e[1], buff=0.4, color=BLUE)
        )
        self.play(FadeIn(sipky))
        self.play(AnimationGroup(*[ReplacementTransform(what.copy(),where) for what,where in zip(
            [elementy[1],elementy[2]],
            [e[2],e[1]]
            )],run_time=3*AnimationRuntime, path_arc=PI/2,lag_ratio=.5))            
        self.play(FadeOut(sipky))

        self.wait(WaitTime)

        self.play(AnimationGroup(
            *[ReplacementTransform(what.copy(),where) for what,where in zip([
                Rinv[0][0],
                D[0][0],
                R[0][0],
                VGroup(R[0][1],Rinv[0][1],D[0][1]),
                R[0][2],
                Rinv[0][2],
                Rinv[1],
                D[1],
                R[1]
                ], [*vypocet[0],*[vypocet[i] for i in [1,2,3]]])],run_time=7*AnimationRuntime
            ,lag_ratio=0.3))
        self.play(*[FadeOut(_) for _ in [R,Rinv,D]], run_time=AnimationRuntime) 
        self.play(vypocet.animate.to_corner(UL),run_time=AnimationRuntime)

        self.play(AnimationGroup(
            *[ReplacementTransform(what.copy(),where) for what,where in zip(
                [vypocet[0][3],vypocet[0][4],vypocet[3]], 
                [*vypocet2[0],vypocet2[2]]
                )],run_time=AnimationRuntime
            ,lag_ratio=0.05))
        self.wait(WaitTime)    
        self.next_section("Nasobeni matic 3")        

        self.MatrixProduct(vypocet[1],vypocet[2],vypocet2[1])
        self.wait(WaitTime)

        self.next_section("Nasobeni matic 4")        
        self.play(FadeIn(vypocet2[3]))
        self.MatrixProduct(vypocet2[1],vypocet2[2],vypocet2[4])

        vypocet3.next_to(vypocet2,DOWN, aligned_edge=LEFT)
        self.wait()
        self.play(FadeIn(vypocet3))

        self.wait(10*WaitTime)

komentar = """

Dobrý den, v tomto videu si ukážeme, proč je potřeba mít transformační rovnice
pro vyjadřování deformace tělesa v různých souřadných soustavách. Ukážeme si,
že transformační rovnice vyplývají snadno z lineární algebry a maticového
počtu. Budeme používat tenzor deformace z mechaniky tuhého tělesa a
transformaci souřadnic z analytické geometrie. Pokud se během videa ve výkladu
ztratíte, zmíněné dvě partie si můžete zopakovat pro lepší pochopení.

Budeme studovat elastický pás, který natáhneme o polovinu. Tímto natažením se
pás zúží, například o deset procent. To je poměrně realistická představa
chování elastického materiálu. 

Změnu tvaru budeme popisovat ve dvou soustavách. Jedna soustava, bílá, bude
respektovat geometrii pásu. Její souřadné osy budou ve směru pásu a tím i ve
směru namáhání. Druhá soustava, červená, bude mít osy pootočené. Například o 45
stupňů, aby situace byla symetrická a obě osy byly vzhledem k pásu stejně
skloněny.

V bílé soustavě budeme mít bílý tenzor deformace, v červené soustavě červený. 

Deformaci nejlépe sledujeme na reprezentativním elementu materiálu, což je ve
dvou dimenzích čtverec. Přesněji, čtverec se stranami ve směru os. Použijeme
bílý element pro bílou soustavu a červený pro červenou.

Připomeňme si, jaké veličiny vidíme v tenzorech deformace. Vlevo nahoře v bílém
tenzoru vidíme relativní prodloužení vodorovné strany bílého čtverce.
Prodlužujeme podélně o polovinu délky, proto zde bude jedna polovina.

V pravém dolním rohu vidíme relativní prodloužení svislé strany čtverce. To
bude záporné, protože strana se zkracuje a hodnota bude minus jedna desetina.

Ve vedlejší diagonále bude číslo, které vyjařuje polovinu úhlu, o který se
zmenší úhel žlutě vyznačený na obrázku. Ten se ale nedeformuje nijak.
Abychom se o tom přesvědčili, stačí ukázat, že žlutý úhel bude pořád stejný
jako modrý úhel. To ukážeme snadno díky symetrii. Opravdu, pás ani materiál
pásu ani vejší podmínky se nemění při rotaci pásu okolo podélné osy o 180
stupňů. Tato rotace převede modře vyznačený úhel na žlutý. Protože před i po
otočení máme fyzikálně identickou situaci, musí být stejná i odezva materiálu.
Proto musí oba úhly být stejně velké. Pro jistotu si tuto transformaci ukažme
na animaci. Protože mají úhly nulovou deformaci, budou mimodiagonání prvky
tenzoru deformace nulové.

Komponenty v hlavní diagonále červeného tenzoru budou stejně velké, protože
odpovídají relativnímu prodloužení stran červeného čtverce. Odpovídající strany
čverce a komponenty tenzoru jsou vyznačeny stejnou barvou. Strany jsou stejně
skloněné k pásu a proto jejich deformace bude stejná. Pro pečlivé zdůvodnění
tohoto tvrzení by se zase dalo využít argumentu symetrie, tentokrát s překlopením
podél osy kolmé na osu pásu. Modrá značka se překlopí na žlutou a naopak, ale
jinak je situace naprosto identická jako před otočením. Proto musí být hodnoty
vyznačené v tenzoru žlutým a modrým rámečkem stejné.

Čísla ve vedlejší diagonále udávají polovinu zmenšení úhlu v červeném
čtverečku. Natažením pásu se úhel zvětší, proto tyto hodnoty budou záporné,
zvětšení je záporné zmenšení.

A teď zkusíme deformovat. Nejprve posuneme pás do vhodné polohy. Tato
transformace nemění tvar pásu a oba tenzory deformace jsou nulové. Po natažení
vidíme, že je do puntíku splněna naše předpověď. Bílý tenzor je diagonální s
čísly 0.5 a -0.1. Červený tenzor má v hlavní diagonále stejná čísla a ve
vedlješí záporná čísla. 

V dalším si ukážeme, jak vypočítat komponenty červeného tenzoru z komponent
tenzoru  bílého.

=====================================

Nejprve odvodíme rovnici pro transformaci komponent tenzoru mezi navzájem
pootočenými soustavami. Tenzory se transformují stejně jako zobrazení. Mějme
zobrazení vektoru U na vektor V reprezentované maticí A. V souřadnicích V=A*U.
Přejdeme do jiné soustavy souřadnic, v ní si souřadnice označíme například
čárkovaně. Mezi souřadnicemi v různých soustavách převádíme pomocí matice
přechodu R. Vynásobením zleva inverzní maticí R^{-1} osamostatníme vektor V' a
výraz, který zbyde před vektorem U' je vlastně matice převádějící vektor U' na
V'. Tedy to je matice našeho zobrazení v čárkované souřadné soustavě. Stejně se
transformuje i tenzor deformace.

Pro nalezení matice předchodu R musíme najít souřadnice jednotkových vektorů ve
směru os pootočené soustavy. To je záležitost definice funkcí sinus a kosinus na
jednotkové kružnici a použití shodných trojúhelníků. Získané souřadnice vytvoří
sloupce matice přechodu R. V našem konkrétním případě je úhel 45 stupňů a proto
můžeme goniometrické funkce vyčíslit numericky. Dokonce můžeme využít toho, že se
v matici opakuje stále stejná numerická hodnota a tuto hodnotu vytknout.

Máme tedy matici přechodu vyjařující rotaci souřadnic a tenzor deformace v
soustavě respektující geometrii úlohy. Nalezení inverzní matice je v případě
matice rotace triviální, inverze bude matice transponovaná.

Potom už stačí matice vynásobit ve správném pořadí, přičemž skalární násobky
můžeme shromáždit všechny vpředu.

Násobení matic není nic jiného než výpočet lineární kombinace sloupců první
matice při použití koeficientů ze sloupců druhé matice. Jako výsledky dostáváme
sloupce matice, která je součinem. Tuto operaci provedeme celkem dvakrát,
protože mezi třemi maticemi jsou dva maticové součiny. Na závěr vynásobíme
matici číslem stojícím před maticí a vidíme, že jsme našli tenzor deformace
přesně v tom tvaru, jako jsme měli v simulaci natahování pásu.

Ve videu jsme si připomněli, jak popisujeme deformaci elastických těles,
ujasnili jsme si, že tento popis souvisí s volbou souřadné soustavy a ukázali
jsme si, jak přejít od popisu v jedné souřadné soustavě do soustavy jiné.


"""
