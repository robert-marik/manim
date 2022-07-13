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

        varianty = [
        [1.33, 0.37,0.37,0.67],
        [1.33, 0.1,0.37,0.67]
        ]
        komentar = [
            r"Symetrická matice",
            r"Nesymetrická matice"
            ]
        number_plane = NumberPlane()
        self.add(number_plane)

        first = True
        for _komentar,_varianty in zip (komentar,varianty):
            # a11,a12,a21,a22 = _varianty
            # matice = np.array([[a11,a12],[a21,a22]])
            matice = np.reshape(_varianty,(2,2))
            matice_mobj_ = Matrix(matice, h_buff = 1.5).set_z_index(10)
            matice_mobj = VGroup(MathTex(r"{\vec v").set_color(RED),MathTex(r"{}={}"),matice_mobj_,MathTex(r"\vec u").set_color(YELLOW))
            matice_mobj.arrange(RIGHT).to_corner(UL).add_background_rectangle(opacity=0.5, buff=.5)
            komentar_mobj = Tex(_komentar).to_corner(UR).add_background_rectangle(opacity=0.5, buff=.5)

            self.add(matice_mobj)
            self.add(komentar_mobj)

            UHEL = ValueTracker(0)
            DELKA = ValueTracker(3)

            vzor = Arrow()
            obraz = Arrow()
            vectors = always_redraw(lambda : self.vzor_a_obraz(UHEL.get_value(),DELKA.get_value(),matice))
    
            self.add(vectors)

            uhly_limit = 270
            if ((matice[1,1]+matice[0,0])**2 >  4* (matice[0,0]*matice[1,1]- matice[1,0]*matice[0,1]) ) and ( matice[1,0] != 0 or matice[0,1] != 0 or matice[0,0] != matice[1,1]):
                vv = np.linalg.eig(matice)
                vv1 = [*vv[1].T[0]]
                vv2 = [*vv[1].T[1]]
                uhel1 = np.arctan2(vv1[1],vv1[0])/np.pi*180
                uhel2 = np.arctan2(vv2[1],vv2[0])/np.pi*180
                seznam = [uhel1+180*i for i in range(100)] + [uhel2+180*i for i in range(100)]
                uhly = [i for i in seznam if (i>=0) and (i<=uhly_limit)]
                uhly.sort()
                uhly = [0]+uhly[:-1]
            else: 
                uhly = [0,uhly_limit]   

            self.wait()
            # if first:
            #     first = False
            #     self.wait()
            for i in range(len(uhly)-1):
                self.play(UHEL.animate.set_value(uhly[i+1]), run_time = animation_runtime*(uhly[i+1]-uhly[i])/uhly_limit, rate_func=linear)
                self.wait()
            self.remove(vectors)
            self.wait()
            self.next_section("Vlastni smery")
            self.remove(komentar_mobj,matice_mobj)


    def vzor_a_obraz(self,uhel,delka,matice):  
        vzor_souradnice = [delka*np.cos(uhel*DEGREES),delka*np.sin(uhel*DEGREES)]
        vzor_souradnice_2 = [-delka*np.sin(uhel*DEGREES), delka*np.cos(uhel*DEGREES)]
        output = VGroup()
        vzor = Arrow(start=(0,0,0),end=(*vzor_souradnice,0),color= YELLOW,buff=0)
        obraz = Arrow(start=(0,0,0),end=[*np.matmul(matice,np.array(vzor.get_end())[:2]),0],color= RED,buff=0)
        vzor_2 = Arrow(start=(0,0,0),end=(*vzor_souradnice_2,0),color= YELLOW,buff=0)
        obraz_2 = Arrow(start=(0,0,0),end=[*np.matmul(matice,np.array(vzor_2.get_end())[:2]),0],color= RED,buff=0)
        output.add(vzor, vzor_2)
        output.add(obraz, obraz_2)
        # check that there are real eigenvales and matrix is not a multiple of identity matrix
        if ((matice[1,1]+matice[0,0])**2 >  4* (matice[0,0]*matice[1,1]- matice[1,0]*matice[0,1]) ) and ( matice[1,0] != 0 or matice[0,1] != 0 or matice[0,0] != matice[1,1]):
            vv = np.linalg.eig(matice)
            vv1 = [*vv[1].T[0]*5,0]
            vv2 = [*vv[1].T[1]*5,0]
            output.add(Line(start = [-i for i in vv1],end = vv1, color=GREEN) )
            output.add(Line(start = [-i for i in vv2], end = vv2, color=GREEN))                
        return output 


komentar = """

"""
        