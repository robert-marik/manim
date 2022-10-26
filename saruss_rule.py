from manim import *
from manim_editor import PresentationSectionType


class Rule(Scene):
    def construct(self):

        title = Title(r"Sarussovo pravidlo")
        self.add(title)
        k = VGroup()
        for i in [0,1,2,0,1]:
            for j in [0,1,2]:
                k.add(MathTex("a_{"+str(i+1)+str(j+1)+"}"))
        A = MobjectMatrix([k[0:3],k[3:6],k[6:9]],left_bracket="|",right_bracket="|")
        A.to_corner(UL).shift(DOWN*2)
        B = MobjectMatrix([k[9:12],k[12:15]],left_bracket="|",right_bracket="|")
        B.set_color(GRAY).next_to(A,DOWN,buff=0)
        b = B.get_rows()[0:2]
        self.add(A)
        self.wait()
        self.play(FadeIn(b))
        self.wait()

        barvy = [
            RED, WHITE,WHITE,
            BLUE, RED, WHITE,
            GREEN, BLUE, RED,
            GRAY, GREEN, BLUE, 
            GRAY, GRAY, GREEN]
        self.play(
            *[FadeToColor (i,j)
            for i,j in zip(k,barvy)
            ]
        )

        kladne = MathTex("=","a_{11}a_{22}a_{33}","+","a_{13}a_{21}a_{32}","+","a_{12}a_{23}a_{31}")
        zaporne = MathTex("-","a_{13}a_{22}a_{31}","-","a_{11}a_{23}a_{32}","-","a_{12}a_{21}a_{33}")
        for i,j in zip([1,3,5],[RED,BLUE,GREEN]):
            kladne[i].set_color(j)
        for i,j in zip([1,3,5],[RED,BLUE,GREEN]):
            zaporne[i].set_color(j)
        kladne.next_to(A)
        zaporne.next_to(kladne,DOWN).shift(RIGHT+0.3*DOWN)

        zdroj = [
            VGroup(k[0],k[4],k[8]),
            VGroup(k[3],k[7],k[11]),
            VGroup(k[6],k[10],k[14])
            ]
        cil = [kladne[1],kladne[3],kladne[5]]

        self.play(
            AnimationGroup(
                *[TransformMatchingShapes(_.copy(),__)
                for _,__ in zip(zdroj,cil)], lag_ratio=0.5),
                run_time=3
        )
        self.wait()
        self.next_section("")        
        
        self.play(
            FadeToColor(k[:9],WHITE),
            FadeToColor(k[9:],GRAY))
        barvy = [
            WHITE, WHITE,RED,
            WHITE, RED, BLUE,
            RED, BLUE, GREEN,
            BLUE, GREEN, GRAY, 
            GREEN, GRAY, GRAY]
        self.play(
            *[FadeToColor (i,j)
            for i,j in zip(k,barvy)
            ]
        )

        zdroj = [
            VGroup(k[2],k[4],k[6]),
            VGroup(k[5],k[8],k[10]),
            VGroup(k[8],k[10],k[12])
            ]
        cil = [zaporne[1],zaporne[3],zaporne[5]]

        self.play(
            AnimationGroup(
                *[TransformMatchingShapes(_.copy(),__)
                for _,__ in zip(zdroj,cil)], lag_ratio=0.5),
                run_time=3
        )
        self.wait()
        self.next_section("")        

        self.add(kladne)
        self.add(zaporne)
        self.next_section("")        
        self.wait()
        
        self.play(
            FadeToColor(kladne,WHITE),
            FadeToColor(zaporne,WHITE),
            FadeToColor(A,WHITE),
            FadeOut(b),
            run_time=2
        )
        self.add(VGroup(title,kladne,zaporne,A).set_color(WHITE))
        self.wait(3)

class Curl(Scene):
    def construct(self):

        title = Title(r"Rotace vektorového pole $\vec F=Pi+Qj+Rk$")
        self.add(title)
        komponenty = [
            r"i",
            r"j",
            r"k",
            r"\frac{\partial}{\partial x}",
            r"\frac{\partial}{\partial y}",
            r"\frac{\partial}{\partial z}",
            r"P",
            r"Q",
            r"R",
            r"i",
            r"j",
            r"k",
            r"\frac{\partial}{\partial x}",
            r"\frac{\partial}{\partial y}",
            r"\frac{\partial}{\partial z}"
        ]
        k = VGroup()
        for i in komponenty:
            k.add(MathTex(i))
        curl = MathTex(r"\nabla \times \vec F =")
        A = MobjectMatrix([k[0:3],k[3:6],k[6:9]],left_bracket="|",right_bracket="|")
        A.to_corner(UL).shift(1.5*DOWN+2.5*RIGHT)
        curl.next_to(A,LEFT)
        B = MobjectMatrix([k[9:12],k[12:15]],left_bracket="|",right_bracket="|")
        B.set_color(GRAY).next_to(A,DOWN,buff=0)
        b1 = B.get_rows()[0].shift(0.2*LEFT+0.01*UP)
        b2 = B.get_rows()[1].shift(0.4*DOWN)
        A.get_rows()[0].shift(.2*UP+0.2*LEFT)
        A.get_rows()[1].shift(.3*DOWN)
        A.get_rows()[2].shift(.2*DOWN)
        k[4].shift(0.1*DOWN)
        k[-2].shift(0.1*DOWN)
        self.add(curl,A)
        self.wait()
        self.play(FadeIn(b1),FadeIn(b2))

        vysledek = VGroup(MathTex(
            r"=",
            r"\left(",
            r"\frac{\partial R}{\partial y}",
            r"-",
            r"\frac{\partial Q}{\partial z}",
            r"\right)",
            r"i",
            ),
            MathTex(
                r"+\left(",
                r"\frac{\partial P}{\partial z}",
                r"-",
                r"\frac{\partial R}{\partial x}",
                r"\right)",
                r"j",
            ),
            MathTex(
                r"+\left(",
                r"\frac{\partial Q}{\partial x}",
                r"-",
                r"\frac{\partial P}{\partial y}",
                r"\right)",
                r"k",
            ),
        )
        vysledek[0].set_color(RED)
        vysledek[1].set_color(GREEN)
        vysledek[2].set_color(BLUE)

        vysledek[0].next_to(A)
        vysledek[1].next_to(vysledek[0],DOWN).shift(RIGHT)
        vysledek[2].next_to(vysledek[1],DOWN)

        self.play(
            *[FadeIn(vysledek[0][i]) for i in [0,1,5,6]],
            *[FadeIn(vysledek[1][i]) for i in [0,4,5]],
            *[FadeIn(vysledek[2][i]) for i in [0,4,5]],
            )
        
        factors = [0,4,8,3,7,11,6,10,14]
        barvy = [
            RED, RED, RED,
            BLUE, BLUE, BLUE,
            GREEN, GREEN, GREEN]
        self.play(
            AnimationGroup(
            *[FadeToColor(k[i],j)
            for i,j in zip(factors,barvy)               
            ],lag_ratio=0.4)
        )

        self.wait()

        zdroj = [
            VGroup(k[0],k[4],k[8]),
            VGroup(k[3],k[7],k[11]),
            VGroup(k[6],k[10],k[14])
            ]
        cil = [
            VGroup(vysledek[0][2],vysledek[0][-1]),
            VGroup(vysledek[2][1],vysledek[1][-1]),
            VGroup(vysledek[1][1],vysledek[1][-1])
        ] 

        temp = [None,None,None,None,None,None,]
        temp[0::2] = [Wiggle(_)
                for _ in zdroj
            ]
        temp[1::2] = [
            TransformMatchingShapes(_.copy(),__)
                for _,__ in zip(zdroj,cil)
            ]
        self.play(
            AnimationGroup(
            *temp,lag_ratio=1),run_time=8
        )
        self.wait()
        self.next_section("")        
        
        barvy = [
            WHITE, WHITE,WHITE,
            WHITE, WHITE,WHITE,
            WHITE, WHITE,WHITE,
            GRAY, GRAY, GRAY, 
            GRAY, GRAY, GRAY]
        self.play(
            FadeIn(vysledek[0][3]),
            FadeIn(vysledek[1][2]),
            FadeIn(vysledek[2][2]),*[FadeToColor (i,j)
            for i,j in zip(k,barvy)
            ]
        )
        factors = [2,4,6,5,7,9,8,10,12]
        barvy = [
            BLUE, BLUE, BLUE, 
            RED, RED, RED, 
            GREEN, GREEN, GREEN,
            ]
        self.play(
            AnimationGroup(
            *[FadeToColor (k[i],j)
            for i,j in zip(factors,barvy)               
            ],lag_ratio=0.4)
        )

        zdroj = [
            VGroup(k[2],k[4],k[6]),
            VGroup(k[5],k[7],k[9]),
            VGroup(k[12],k[8],k[10]),
            ]

        cil = [
            VGroup(vysledek[2][3],vysledek[2][-1]),
            VGroup(vysledek[0][4],vysledek[0][-1]),
            VGroup(vysledek[1][3],vysledek[1][-1]),
        ] 

        temp = [None,None,None,None,None,None,]
        temp[0::2] = [Wiggle(_)
                for _ in zdroj
            ]
        temp[1::2] = [
            TransformMatchingShapes(_.copy(),__)
                for _,__ in zip(zdroj,cil)
            ]
        self.play(
            AnimationGroup(
            *temp,lag_ratio=1),run_time=8
        )
        self.wait()        
        self.next_section("")        
        
        self.play(
            FadeOut(b1,b2),
            FadeToColor(k[:9],WHITE),
            FadeToColor(vysledek,WHITE),
            run_time = 3
            )
        #self.add(VGroup(title,A,vysledek,curl).set_color(WHITE))
        self.wait(4)
