from manim import *
import numpy as np

animation_runtime = 15
config.max_files_cached = 400

# from https://favpng.com/png_view/wood-frame-wood-circle-png/Kts40pG2
wood_img = r"c:\Users\marik\Documents\GitHub\manim\wood"

class Eigenvectors(Scene):

    def construct(self):

        title = Title(r"Vlastní směry matice")
        autor = VGroup(Tex("Robert Mařík"),Tex("Mendel University")).arrange(DOWN).next_to(title,DOWN)
        self.play(GrowFromCenter(title))
        self.play(GrowFromCenter(autor[0]))
        self.play(GrowFromCenter(autor[1]))
        self.wait(10)
        self.play(FadeOut(title),FadeOut(autor))

        wood_obj = ImageMobject(wood_img)
        varianty = [
        [1,1,0.5,1],
        [1,1.5,0.5,-1.2],
        [1,0.3,-0.3,1],
        [1.2,0,0,1.2],
        [1.2,0,0,.5],
        [1.5 ,0.2,0.2,.5],
        ]

        komentar = [
            r"Obecná matice",
            r"Matice se zápornou vlastní hodnotou",
            r"Matice malých rotací",
            r"Násobek jednotkové matice",
            r"Diagonální matice",
            r"Symetrická matice"
            ]

        obrazky = Group(Mobject(),Mobject(),Mobject(),Mobject(),wood_obj.copy().scale_to_fit_width(3),wood_obj.copy().rotate(19*DEGREES).scale_to_fit_width(3))
        obrazky.to_corner(DR)    

        number_plane = NumberPlane()
        self.add(number_plane)
        # optimg=VGroup()
        # self.add(optimg)

        first = True
        for _komentar,_varianty,img in zip (komentar,varianty,obrazky):
            a11,a12,a21,a22 = _varianty
            matice = np.array([[a11,a12],[a21,a22]])
            matice_mobj_ = Matrix([[a11, a12], [a21, a22]])
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
            self.add(img)

            uhly_limit = 360*2
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
            if first:
                first = False
                self.wait(10)
            for i in range(len(uhly)-1):
                self.play(UHEL.animate.set_value(uhly[i+1]), run_time = animation_runtime*(uhly[i+1]-uhly[i])/uhly_limit, rate_func=linear)
                self.wait()
            self.remove(komentar_mobj,matice_mobj,img)


    def vzor_a_obraz(self,uhel,delka,matice):  
        vzor_souradnice = [delka*np.cos(uhel*DEGREES),delka*np.sin(uhel*DEGREES)]
        output = VGroup()
        vzor = Arrow(start=(0,0,0),end=(*vzor_souradnice,0),color= YELLOW,buff=0)
        obraz = Arrow(start=(0,0,0),end=[*np.matmul(matice,np.array(vzor.get_end())[:2]),0],color= RED,buff=0)
        output.add(vzor)
        output.add(obraz)
        # check that there are real eigenvales and matrix is multiple of identity matrix
        if ((matice[1,1]+matice[0,0])**2 >  4* (matice[0,0]*matice[1,1]- matice[1,0]*matice[0,1]) ) and ( matice[1,0] != 0 or matice[0,1] != 0 or matice[0,0] != matice[1,1]):
            vv = np.linalg.eig(matice)
            vv1 = [*vv[1].T[0]*5,0]
            vv2 = [*vv[1].T[1]*5,0]
            output.add(Line(start = [-i for i in vv1],end = vv1, color=GREEN) )
            output.add(Line(start = [-i for i in vv2], end = vv2, color=GREEN))
            # if np.abs(vv1[1]*vv2[1]+vv1[0]*vv2[0]) < 0.01:
            #     self.remove(optimg)
            #     if vv1[1]*vv2[1]==0:
            #         otoceni = 0
            #     else:
            #         otoceni = min (np.arctan(vv1[1]/vv1[0]),np.arctan(vv1[1]/vv1[0]))
            #     print(vv1,vv2,otoceni)
            #     wood_img = obrazek_obj.copy().rotate(otoceni*DEGREES).scale_to_fit_width(3).to_corner(DR)
            #     optimg = wood_img
            #     self.add(optimg)
                
        return output 
        