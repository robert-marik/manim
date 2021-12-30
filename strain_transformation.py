from manim import *
import numpy as np

AnimationRuntime = 1
WaitTime = 2

class Deformation(Scene):
    def construct(self):
        rct = Rectangle(color=GREEN, width=6, height=2, fill_opacity=0.5 ) 
        square = Square(color=BLUE, side_length=1, fill_opacity=1)
        square1 = square.copy()
        square2 = square.copy()
        squareL = Square(color=WHITE, side_length=1, fill_opacity=1).shift(LEFT*2)
        squareR = Square(color=WHITE, side_length=1, fill_opacity=1).shift(RIGHT*2)
        squareC = Square(color=RED, side_length=1, fill_opacity=1).rotate(45 * DEGREES)
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

        intro = Text("""
        Ve videu si ukážeme, proč jsou
        v rotovaných souřadnicích
        jiné komponenty tenzoru deformace.
        """).to_edge(UL)
        self.play(Create(intro),run_time=AnimationRuntime)
        self.wait(duration=4)
        self.remove(intro)

        tvg = vg.copy()
        tvg1 = vg1.copy()
        tvg2 = vg2.copy()

        popis = Text("""
        Budeme uvažovat elastický pás,
        který natáhneme o polovinu podélně.
        Pás se přitom zúží o deset procent.
        """).to_edge(UL)
        self.play(FadeIn(tvg),Create(popis))
        self.play(ReplacementTransform(tvg, tvg1), run_time=3*AnimationRuntime)
        self.wait(WaitTime)
        self.play(ReplacementTransform(tvg1, tvg2), run_time=3*AnimationRuntime)
        self.wait(WaitTime)
        self.remove(popis)

        temp = VGroup(osy)
        popis_os = Text("""
        Bílá souřadná soustava respektuje geometrii pásu
        a namáhání. Očekáváme prodloužení ve vodorovné
        ose, zkrácení ve svislé ose a zachování úhlu
        mezi vektory mířícími před deformací ve směru os.
        """).scale(0.75).next_to(vg,DOWN).to_edge(LEFT)
        self.play(FadeIn(temp), Create(popis_os),run_time=AnimationRuntime)
        self.wait(duration=10*WaitTime)
        self.remove(popis_os)

        popis_osr = Text("""
        Červená souřadná soustava má osy skloněné stejně
        vzhledem ke geometrii úlohy. Očekáváme proto 
        ve směru obou os stejnou reakci.
        Úhel mezi vektory ve směru os se deformuje.
        """).scale(0.75).next_to(vg,DOWN).to_edge(LEFT)
        self.play(FadeIn(osyr), Create(popis_osr),run_time=AnimationRuntime)
        self.wait(duration=10*WaitTime)
        self.remove(popis_osr)


        self.play(ReplacementTransform(tvg2,rct))
        popis_tenzor =Text("""
        Tenzor vlevo je v souřadné soustavě respektující 
        geometrii a namáhání materiálu.
        """).scale(0.75).next_to(vg,DOWN).to_edge(LEFT)
        self.play(FadeIn(tenzor1["O"]),Create(popis_tenzor),run_time=AnimationRuntime)
        self.wait(duration=5*WaitTime)
        self.remove(popis_tenzor)

        popis_tenzor2 = Text("""
        Tenzor vpravo je v souřadné soustavě otočené
        proti směru hodinových ručiček o 45 stupňů.
        """).scale(0.75).next_to(vg,DOWN).to_edge(LEFT)
        self.play(FadeIn(tenzor2["O"]),Create(popis_tenzor2),run_time=AnimationRuntime)
        self.wait(duration=5*WaitTime)
        self.remove(popis_tenzor2)

        vg = VGroup()
        vg.add(rct,squareL, squareR, squareC)

        self.wait(WaitTime)
        popis = Text("""
        Deformace se nejlépe studuje na reprezentativním
        elementu (RVE - representative volume element).
        Ve dvoudimenzionálním případě na čtverci.
        """).scale(0.75).next_to(vg,DOWN).to_edge(LEFT)
        self.play(Write(square),Create(popis),run_time=AnimationRuntime)
        self.wait(duration=4*WaitTime)
        self.remove(popis)

        popis = Text("""
        Pro potřeby našich souřadných soustav potřebujeme 
        elementy zarovnané s osami. Tedy bílé čtverce 
        v základní poloze pro bílou soustavu a červené 
        pootočené pro soustavu červenou.
        """).scale(0.75).next_to(vg,DOWN).to_edge(LEFT)
        self.play(
            ReplacementTransform(square, squareL),
            ReplacementTransform(square1, squareR),
            ReplacementTransform(square2, squareC),
            Create(popis)
        )
        self.wait(duration=4*WaitTime)
  

        b1 = VGroup(Brace(squareL, color=YELLOW),Brace(squareR, color=YELLOW))
        b2 = VGroup(Brace(squareL, direction=LEFT, color=YELLOW),Brace(squareR, direction=LEFT, color=YELLOW))
        b3 = Brace(squareC, direction=LEFT+DOWN, color=YELLOW)
        b4 = Brace(squareC, direction=RIGHT+DOWN, color=YELLOW)
        #self.add(b1,b2,b3,b4)
        self.remove(popis)

        angle1= VGroup(*[Arc(
                radius=0.5,
                start_angle=0*DEGREES,
                angle =90*DEGREES,
                color=YELLOW
            ).shift(_.get_left()*RIGHT, _.get_bottom()*UP) for _ in [squareL,squareR] ])

        angle2= Arc(
                radius=0.5,
                start_angle=45*DEGREES,
                angle =90*DEGREES,
                color=YELLOW
            ).shift(squareC.get_bottom()*UP)    

        def explain_element(tensor,element,text,marker=[]):
            temp1 = VGroup(*[SurroundingRectangle(tensor.get_entries()[_]) for _ in element],*marker)
            temp2 = Text(text).scale(0.75).next_to(vg,DOWN).to_edge(LEFT)
            self.play(Create(temp1),Create(temp2))
            self.wait(duration=6*WaitTime)
            self.remove(temp1,temp2,*marker)
            

        explain_element(tenzor1["O"],[0],"""
        Levý horní prvek tenzoru deformace vyjadřuje
        relativní prodloužení vodorovné strany 
        bílého čtverce. Protože se strana prodlužuje
        o polovinu, očekáváme hodnotu 0.5.
        """,marker=[b1])
        explain_element(tenzor1["O"],[3],"""
        Pravý dolní prvek tenzoru deformace vyjadřuje 
        relativní prodloužení svislé strany bílého čtverce. 
        Protože se strana zkracuje o deset procent, 
        očekáváme hodnotu −0.1. 
        """,marker=[b2])
        explain_element(tenzor1["O"],[1,2],"""
        Mimodiagonální prvky vyjařují polovinu úhlu,
        o který se při deformaci sevřou vektory 
        směřující původně ve směru os. Očekáváme
        nulovou hodnotu, pravý úhel se zachová.
        """,marker=angle1)
        explain_element(tenzor2["O"],[0,3],"""
        Diagonální prvky tenzoru deformace v otočené 
        soustavě vyjadřují relativní změnu délek stran
        červeného čtverce. Očkáváme obě hodnoty stejné,
        situace je symetrická.
        """,marker=[b3,b4])
        explain_element(tenzor2["O"],[1,2],"""
        Mimodiagonální prvky vyjadřují polovinu úhlu, 
        o který se sevřou vektory směřující před 
        deformací ve směru červených os. Očekáváme 
        zápornou hodnotu, vektory se rozevírají.
        """,marker=angle2)

        angle= VGroup(*[Arc(
                    radius=0.5,
                    start_angle=0*DEGREES,
                    angle =90*DEGREES,
                    color=YELLOW
            ).shift(_.get_left()*RIGHT, _.get_bottom()*UP) for _ in [squareL,squareR] ])

        vg2 = vg.copy()
        vg1 = vg.copy()
        vg1.shift(LEFT*1.55)
        vg2.stretch(1.5,0)
        vg2.stretch(0.9,1)

        self.play(
            ReplacementTransform(tenzor1["O"], tenzor1["N"]),
            ReplacementTransform(tenzor2["O"], tenzor2["N"]),
        )

        popis = Text("""
        Posun nesouvisí s deformací. 
        Oba tenzory zůstávají nulové.
        """).scale(0.75).next_to(vg,DOWN).to_edge(LEFT)
        self.play(ReplacementTransform(vg, vg1), Create(popis),run_time=AnimationRuntime)
        self.wait(duration=3*WaitTime)
        self.remove(popis)

        popis = Text("""
        Změna tvaru se již projeví na obou tenzorech. 
        Vidíme, že jsou splněna přirozená očekávání, 
        která jsme zformulovali před simulací. 
        """).scale(0.75).next_to(vg,DOWN).to_edge(LEFT)
        self.play(ReplacementTransform(vg1,vg2), \
            ReplacementTransform(tenzor1["N"], tenzor1["D"]), \
            ReplacementTransform(tenzor2["N"], tenzor2["D"]), 
            Create(popis),
            run_time=AnimationRuntime)
        self.wait(10*WaitTime)    

        self.clear()

class Transformace(Scene):


    def MatrixProduct(self,A,B,C,run_time=AnimationRuntime):
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
                ReplacementTransform(A.copy().get_brackets().copy(),lincomb[1].get_brackets()),
                *[ReplacementTransform(_,__) for _,__ in zip(A.get_columns().copy()[0],lincomb[1].get_columns()[0])],
                FadeIn(lincomb[2]),
                ReplacementTransform(B.copy().get_columns()[i][1],lincomb[3]),
                ReplacementTransform(A.copy().get_brackets(),lincomb[4].get_brackets()),
                *[ReplacementTransform(_,__) for _,__ in zip(A.get_columns().copy()[1],lincomb[4].get_columns()[0])],
                FadeIn(lincomb[5]),
                lag_ratio=0.6
            ))    
            self.wait()
            self.play(FadeIn(lincomb[6]))
            self.wait()
            self.play(AnimationGroup(*[ReplacementTransform(_,__) for _,__ in zip(lincomb.copy()[6].get_columns()[0],C.get_columns()[i])],lag_ratio=0.4))
            self.wait()
            self.play(
                FadeOut(lincomb),
                FadeToColor(A,WHITE),
                FadeToColor(B,WHITE)
                )
        #self.play(FadeIn(C))
    
    def construct(self):

        # Formalni odvozeni transformacni rovnice pro tenzory
        lines = VGroup(
            Text ("Transformace zobrazení nebo tenzoru"),
            MathTex("V = A U"),
            MathTex("RV' = A R U'"),
            MathTex(r"V' = R^{-1} A R U'"),
            MathTex(r"V' = ","(R^{-1} A R)",r"U'")
        )
        lines.arrange(DOWN)#, buff=LARGE_BUFF)
        self.add(lines[0])
        self.wait()
        self.play(FadeIn(lines[1]),run_time=AnimationRuntime)
        self.wait()
        for i in [1,2,3]:
            self.play(
            TransformMatchingShapes(lines[i].copy(), lines[i+1], path_arc=90 * DEGREES, run_time=AnimationRuntime)
            ),
            self.wait(WaitTime)           

        svorka = Brace(lines[-1][1], direction=DOWN)
        popisek = svorka.get_text("Tenzor v čárkované soustavě souřadnic")
        lines[-1][1].set_color(YELLOW)
        self.play(FadeIn(svorka), FadeIn(popisek), run_time=AnimationRuntime)
        self.wait(WaitTime*5)

        self.clear()

        # nalezeni matice transformace
        theta = 20

        number_plane = NumberPlane(
        x_range=[-2, 2, .5],
        y_range=[-2, 2, .5],
        )#.scale(0.5)
        zacatek = np.array([0,0,0])
        e1 = Arrow(start=zacatek, end=2*RIGHT, color=RED, buff=0)
        e2 = e1.copy()
        e2.rotate_about_origin(90*DEGREES)
        circ = Circle(radius=2.0,color=WHITE, stroke_width=1)
        e12 = VGroup(e1,e2)
        e12_r = e12.copy()
        e12_r.rotate_about_origin(theta*DEGREES)
        
        line1 = Line(start=[2*np.cos(theta*DEGREES),2*np.sin(theta*DEGREES),0],end=[2*np.cos(theta*DEGREES),0,0],color= YELLOW, stroke_width=6)
        line1r = line1.copy().rotate_about_origin(90*DEGREES)
        line2 = Line(start=[2*np.cos(theta*DEGREES),0,0],end=[0,0,0],color= GREEN,stroke_width=6)
        line2r = line2.copy().rotate_about_origin(90*DEGREES)
        VGroup(e12,e12_r,number_plane,circ,line1,line1r,line2,line2r).shift(3*DOWN,LEFT)

        #e1_coor=np.ndarray([np.cos(theta),np.sin(theta)])
        #e2_coor=np.ndarray([-np.sin(theta),np.cos(theta)])
        self.play(FadeIn(number_plane), run_time=AnimationRuntime)
        self.play(Create(e12), run_time=AnimationRuntime)
        self.play(Succession(
            Create(circ),
            ReplacementTransform(e12,e12_r),
            lag_ratio=1, run_time=AnimationRuntime))
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


        R_theta = Matrix([[r"\cos(\theta)", r"-\sin(\theta)"], 
            [r"\sin(\theta)",r"\cos(\theta)"]], h_buff=h_buf).to_edge(UL)
        R0 = Matrix([[r"\frac{\sqrt 2}{2}",r"-\frac{\sqrt 2}{2}"],[r"\frac{\sqrt 2}{2}",r"\frac{\sqrt 2}{2}"]],
            v_buff=v_buf).to_edge(UR)
        R = VGroup(MathTex(r"\frac{\sqrt 2}{2}"), Matrix([[r"1", r"-1"], [r"1",r"1"]]))
        R.arrange(RIGHT, buff=0.5).to_edge(UR)


        # #R_theta = MathTex(r"\begin{bmatrix} \cos(\theta)&-\sin(\theta)\\\sin(\theta)&\cos(\theta)\end{bmatrix}").to_edge(UL)
        # R0 =  MathTex(r"R=\begin{bmatrix} \frac{\sqrt 2}2&-\frac{\sqrt 2}2\\\frac{\sqrt 2}2&\frac{\sqrt 2}2\end{bmatrix}").next_to(R_theta,RIGHT, buff=1)
        # R = VGroup(MathTex(r"R=\frac{\sqrt 2}{2}"),Matrix([[r"1", r"-1"], [r"1",r"1"]]),).arrange(RIGHT).next_to(R_theta,RIGHT, buff=1)

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
        self.wait(4*WaitTime)
        
        self.clear()
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

        self.wait(4*WaitTime)
        
        self.play(*[ReplacementTransform(what.copy(),where) for what,where in zip(
            [R[0][0],R[0][1],R[0][2],elementy[0],elementy[3],R[1].get_brackets()],
            [Rinv[0][0],Rinv[0][1],Rinv[0][2],e[0],e[3],Rinv[1].get_brackets()]
            )],run_time=AnimationRuntime, path_arc=PI/2)

        self.play(*[ReplacementTransform(what.copy(),where) for what,where in zip(
            [elementy[1],elementy[2]],
            [e[2],e[1]]
            )],run_time=AnimationRuntime, path_arc=PI/2)            

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
                ], [*vypocet[0],*[vypocet[i] for i in [1,2,3]]])],run_time=5*AnimationRuntime
            ,lag_ratio=0.3))
        self.play(*[FadeOut(_) for _ in [R,Rinv,D]], run_time=AnimationRuntime) 
        #self.play(ReplacementTransform(vypocet,vypocet_cp)) 
        self.play(vypocet.animate.to_corner(UL),run_time=AnimationRuntime)

        self.play(AnimationGroup(
            *[ReplacementTransform(what.copy(),where) for what,where in zip(
                [vypocet[0][3],vypocet[0][4],vypocet[3]], 
                [*vypocet2[0],vypocet2[2]]
                )],run_time=AnimationRuntime
            ,lag_ratio=0.05))
        self.wait(WaitTime)    

        self.MatrixProduct(vypocet[1],vypocet[2],vypocet2[1])
        self.wait(WaitTime)
        self.play(FadeIn(vypocet2[3]))
        self.MatrixProduct(vypocet2[1],vypocet2[2],vypocet2[4])

        #vypocet2.next_to(vypocet,DOWN, aligned_edge=LEFT).shift(RIGHT)
        vypocet3.next_to(vypocet2,DOWN, aligned_edge=LEFT)
        self.wait()
        self.play(FadeIn(vypocet3))
        #self.add(vypocet2,vypocet3)

        self.wait(5*WaitTime)