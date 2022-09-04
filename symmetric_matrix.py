from manim import *
import numpy as np
import os
import common_definitions
from manim_editor import PresentationSectionType

animation_runtime = 15
config.max_files_cached = 400
x_range = np.linspace(-4,4,500)
wait_time = 8
AnimationRuntime = 10

class Eigenvectors(ThreeDScene):

    def construct(self):

        self.next_section("Zobrazeni pomoci matice")
        self.remove(*[_ for _ in self.mobjects])

        komentar = [
            r"Symetrická matice",
            r"Nesymetrická matice"
            ]
        number_plane = [NumberPlane().scale(0.4) for i in range(4)]
        number_plane[0].to_corner(DL)
        number_plane[1].to_corner(DR)
        number_plane[2].to_corner(UL)
        number_plane[3].to_corner(UR)
        self.add(*number_plane)

        first = True
        #for _komentar,_varianty in zip (komentar,varianty):
            # a11,a12,a21,a22 = _varianty
            # matice = np.array([[a11,a12],[a21,a22]])
        matice = [np.reshape(i,(2,2))
                    for i in 
                        [
                            [1.3, 0.4,0.4,0.7] ,
                            [1.3, 0.4,0.1,0.7] ,
                            [1.3, 0,0,1.3] ,
                            [1.3, 0,0,0.7]
                        ]
                    ]

        komentar = [
            r"Symetrická matice",
            r"Obecná matice",
            r"Násobek jednotkové matice",
            r"Diagonální matice",
            ]

        # vv = np.linalg.eig(matice[0])
        # vv1 = [*vv[1].T[0]]
        # vv2 = [*vv[1].T[1]]
        
        matice_mobj = [VGroup(
             MathTex(r"{\vec v").set_color(RED),MathTex(r"{}={}"),
             Matrix(i, h_buff = 1.5),
             MathTex(r"\vec u").set_color(YELLOW)
             ).arrange(RIGHT)
            for i in matice
            ]


        for i,j in zip (matice_mobj,komentar):
            i.add(Tex(j).next_to(i,LEFT))

        for i,j in zip (matice_mobj,number_plane):
            i.scale(0.5).move_to(j, aligned_edge=UR)
            i.set_z_index(5)
            i.add_background_rectangle()

        self.add(*matice_mobj)

        UHEL = ValueTracker(-4*360)
        DELKA = ValueTracker(3)

        vzor = Arrow()
        obraz = Arrow()
        ifboth = False
        vectors = always_redraw(
            lambda : self.vzor_a_obraz_2(
                UHEL.get_value(),
                DELKA.get_value(),
                matice,
                number_plane, 
                ifboth)
            )

        self.add(vectors)

        self.play(
            UHEL.animate.increment_value(2*360), run_time = 8, rate_func=linear
            )
        self.wait()
        ifboth = True
        self.play(
            UHEL.animate.increment_value(2.1*360), run_time = 8, rate_func=linear
            )
        self.wait()

    def vzor_a_obraz_2(self,uhel,delka,matice,number_plane,both=True):  
        out = VGroup()
        for m_,n_ in zip(matice,number_plane):
            out.add(self.vzor_a_obraz(uhel,delka,m_,n_,both))
        return out


    def vzor_a_obraz(self,uhel,delka,matice,number_plane,both=True):  

        # check that there are real eigenvalues and matrix is not a multiple of identity matrix
        if ((matice[1,1]+matice[0,0])**2 >  4* (matice[0,0]*matice[1,1]- matice[1,0]*matice[0,1]) ) and ( matice[1,0] != 0 or matice[0,1] != 0 or matice[0,0] != matice[1,1]):
            if uhel > 0:
                vv = np.linalg.eig(matice)
                vv1 = [*vv[1].T[0]]
                uhel1 = np.arctan2(vv1[1],vv1[0])/np.pi*180
                uhel = min(uhel,uhel1)
        
        vzor_souradnice = [delka*np.cos(uhel*DEGREES),delka*np.sin(uhel*DEGREES)]
        vzor_souradnice_2 = [-delka*np.sin(uhel*DEGREES), delka*np.cos(uhel*DEGREES)]
        output = VGroup()
        vzor = Line(start=number_plane.c2p(0,0,0),end=number_plane.c2p(*vzor_souradnice,0),color= YELLOW,buff=0)
        obraz = Line(start=number_plane.c2p(0,0,0),end=number_plane.c2p(*np.matmul(matice,np.array(vzor_souradnice))),color= RED,buff=0)
        vzor_2 = Line(start=number_plane.c2p(0,0,0),end=number_plane.c2p(*vzor_souradnice_2,0),color= YELLOW,buff=0)
        obraz_2 = Line(start=number_plane.c2p(0,0,0),end=number_plane.c2p(*np.matmul(matice,np.array(vzor_souradnice_2))),color= RED,buff=0)
        for i in [vzor, vzor_2,obraz,obraz_2]:
            i.add_tip(tip_length=0.2)
        output.add(vzor, obraz)
        if both:
            output.add(vzor_2, obraz_2)
              
        return output 


komentar = """

"""
        