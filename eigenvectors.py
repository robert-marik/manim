from manim import *
import numpy as np
import os
import common_definitions

animation_runtime = 15
config.max_files_cached = 400
x_range = np.linspace(-4,4,500)
wait_time = 8
AnimationRuntime = 10

# from https://favpng.com/png_view/wood-frame-wood-circle-png/Kts40pG2
wood_img = os.path.join('icons', 'wood')

# images
wood_longitudal = os.path.join('icons', 'wood_L')
wood_perp = os.path.join('icons', 'wood_P')
wood_slanted = os.path.join('icons', 'wood_S')

# flipped images
wood_longitudal_f = os.path.join('icons', 'wood_L_f')
wood_perp_f = os.path.join('icons', 'wood_P_f')
wood_slanted_f = os.path.join('icons', 'wood_S_f')

class Eigenvectors(ThreeDScene):

    def construct(self):

        title = Title(r"Anatomické směry dřeva a vlastní směry matice")
        autor = VGroup(Tex("Robert Mařík"),Tex("Mendel University")).arrange(DOWN).next_to(title,DOWN)
        self.play(GrowFromCenter(title))
        self.play(GrowFromCenter(autor[0]))
        self.play(GrowFromCenter(autor[1]))
        self.wait(6)
        self.play(FadeOut(title),FadeOut(autor))

        self.next_section()

        matrix_u = Matrix([[2],[-1]])
        matrix_v_kov = Matrix([[10],[-5]])
        lambda_matrix = Matrix([[3,1],[1,2]])
        matrix_v_drevo = Matrix([[7],[0]])
        texty = VGroup(
            Tex(r"$\bullet$ $\vec v = \lambda \vec u$,\quad $\vec v$ je tok, $\vec u$ je spád teploty"),
            Tex(
                    r"$\bullet$ Materiál typu kov: $\lambda = 5$,", 
                    r"$\displaystyle\vec u=\begin{bmatrix} 2\\-1\end{bmatrix},$",
                    r"$\displaystyle\vec v=$",
                    r"$\displaystyle 5\begin{bmatrix} 2\\-1\end{bmatrix}$"
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                Tex(r"$\bullet$ Materiál typu dřevo: $\lambda = {}$"), 
                lambda_matrix,
                Tex(r"$, \vec u = {}$"), 
                matrix_u.copy()
            ).arrange(RIGHT, buff=0.2),
            VGroup(
                Tex(r"$\displaystyle\vec v={}$"),
                lambda_matrix.copy(),
                matrix_u.copy(),
                Tex(r"${}={}$"),
                matrix_v_drevo
            ).arrange(RIGHT, buff=0.2),
            Tex(r"Kov: $\vec v \parallel \vec u$\quad Dřevo: $\vec v \nparallel\vec u$",color=YELLOW),
        ).arrange(DOWN, aligned_edge=LEFT).to_corner(UL)

        m = texty[3]
        m.to_edge(RIGHT)
        tok_kov = Tex(r"$\displaystyle \begin{bmatrix} 10\\-5\end{bmatrix}$").move_to(texty[1][3])
        for _ in [texty[0],texty[1],texty[2],texty[3][0:4]]:
            self.play(FadeIn(_))
            self.wait()

        self.play(ReplacementTransform(texty[1][3],tok_kov))
        self.MatrixProduct(m[1],m[2],matrix_v_drevo)
        self.wait()
        texty[4].shift(RIGHT)
        self.play(FadeIn(texty[4]))
        self.wait(wait_time)
        self.play(*[FadeOut(_) for _ in self.mobjects])
        self.wait(wait_time)

        wood_obj = ImageMobject(wood_img).scale_to_fit_width(1)
        wood_longitudal_obj = ImageMobject(wood_longitudal).scale_to_fit_width(1)

        board_width = 6
        board_height = 2
        decline = 0.7
        board = {}
        board['rectangle'] = Rectangle(width=board_width, height=board_height).shift(0.6*board_height*UP)
        board['temperature'] = VGroup(
            Line(start=ORIGIN, end=[0,board_height,0], stroke_width=20).next_to(board['rectangle'],LEFT, buff=0.5).set_color(PURE_RED),
            Line(start=ORIGIN, end=[0,board_height,0], stroke_width=20).next_to(board['rectangle'],RIGHT, buff=0.5).set_color(PURE_BLUE),
        )
        board['img'] = ImageMobject(wood_longitudal).scale_to_fit_width(6).set_color(WHITE).move_to(board['rectangle'])
        board['img_perp'] = ImageMobject(wood_perp).scale_to_fit_width(6).set_color(WHITE).move_to(board['rectangle'])
        board['img_slanted'] = ImageMobject(wood_slanted).scale_to_fit_width(6).set_color(WHITE).move_to(board['rectangle'])
        board['arrow'] = Arrow(start = ORIGIN, end = 2*RIGHT, stroke_width=20, color=RED).move_to(board['rectangle'], aligned_edge=LEFT)
        board['arrow_declined'] = Arrow(start = ORIGIN, end = 2*RIGHT+decline*UP*.7, stroke_width=20, color=RED).move_to(board['rectangle'], aligned_edge=LEFT)
        board['arrow_short'] = Arrow(start = ORIGIN, end = RIGHT, stroke_width=20, color=RED, max_stroke_width_to_length_ratio=15, max_tip_length_to_length_ratio=0.5).move_to(board['rectangle'], aligned_edge=LEFT)
        board_copy = {}
        for _ in board.keys():
            board_copy[_]=board[_].copy()
        board['img'] = ImageMobject(wood_longitudal).scale_to_fit_width(6).set_color(WHITE).move_to(board['rectangle'])
        board['img_perp'] = ImageMobject(wood_perp).scale_to_fit_width(6).set_color(WHITE).move_to(board['rectangle'])
        board['img_slanted'] = ImageMobject(wood_slanted).scale_to_fit_width(6).set_color(WHITE).move_to(board['rectangle'])
        # Images for plane transformations
        obrazky = Group(Mobject(),Mobject(),Mobject(),Mobject(),
            board['img'].copy().scale_to_fit_width(10).set_z_index(20),
            board['img_slanted'].copy().scale_to_fit_width(10).set_z_index(20)
            ) 
        parts = ["arrow_declined","rectangle","temperature"]
        hidden_parts = ["arrow","arrow_short"]
        flip_parts = ["img_perp","img_slanted","img"]

        for _ in hidden_parts:
            board_copy[_].rotate_about_origin(180*DEGREES, RIGHT)

        self.play(AnimationGroup(
            *[FadeIn(_) for _ in [board['rectangle'],board['temperature'],board['img'],board['arrow_declined']]], 
            run_time=5, 
            lag_ratio=1
            ))
        self.add(*[board_copy[_] for _ in parts])

        self.wait()
        self.move_camera(
            phi=30 * DEGREES,
            theta=-50 * DEGREES
        )

        def update_drawing(d,dt):
            d.rotate_about_origin(dt, RIGHT)
        [_.add_updater(update_drawing) for  _ in board_copy.values()]        
        self.wait(PI)
        [_.remove_updater(update_drawing) for _ in board_copy.values()]

        board_copy['img'] = ImageMobject(wood_longitudal_f).scale_to_fit_width(6).set_color(WHITE).move_to(board_copy['rectangle'])
        board_copy['img_perp'] = ImageMobject(wood_perp_f).scale_to_fit_width(6).set_color(WHITE).move_to(board_copy['rectangle'])
        board_copy['img_slanted'] = ImageMobject(wood_slanted_f).scale_to_fit_width(6).set_color(WHITE).move_to(board_copy['rectangle'])
        self.play(FadeIn(board_copy['img']))
        self.move_camera(
            phi=0 * DEGREES,
            theta=-90 * DEGREES
        )
        frown = Text(r"☹", color=RED).scale(3).next_to(board['temperature'],UP)
        smile = Text(r"☺", color=GREEN).scale(3).next_to(board['temperature'],UP)
        self.add(frown)
        self.wait(wait_time)
        self.play(
            ReplacementTransform(board['arrow_declined'].copy(),board['arrow']),
            ReplacementTransform(board_copy['arrow_declined'].copy(),board_copy['arrow']),
            FadeOut(board['arrow_declined']),
            FadeOut(board_copy['arrow_declined']),
            ReplacementTransform(frown,smile)
        )
        self.wait(wait_time)
        self.play(
            ReplacementTransform(board['img'],board['img_perp']),
            ReplacementTransform(board_copy['img'],board_copy['img_perp']),
            ReplacementTransform(board['arrow'],board['arrow_short']),
            ReplacementTransform(board_copy['arrow'],board_copy['arrow_short']),
        )
        self.wait(wait_time)
        self.play(
            ReplacementTransform(board['arrow_short'],board['arrow_declined']),
            ReplacementTransform(board_copy['arrow_short'],board_copy['arrow_declined']),
            ReplacementTransform(board['img_perp'],board['img_slanted']),
            ReplacementTransform(board_copy['img_perp'],board_copy['img_slanted']),
        )
        self.wait(wait_time)

        self.next_section()
        self.play(*[FadeOut(_) for _ in self.mobjects])
        self.wait(wait_time)

        self.next_section()
        varianty = [
        [1,1,0.5,1],
        [1,1.5,0.5,-1.2],
        [1,0.3,-0.3,1],
        [1.2,0,0,1.2],
        [1.2,0,0,.5],
        [1.33, 0.37,0.37,0.67]
        ]
        komentar = [
            r"Obecná matice",
            r"Matice se zápornou vlastní hodnotou",
            r"Matice malých rotací",
            r"Násobek jednotkové matice",
            r"Diagonální matice",
            r"Symetrická matice"
            ]
        obrazky.to_corner(DR)    
        number_plane = NumberPlane()
        self.add(number_plane)

        first = True
        for _komentar,_varianty,img in zip (komentar,varianty,obrazky):
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
            self.add(img.set_color(WHITE))

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

            self.wait(wait_time)
            if first:
                first = False
                self.wait()
            for i in range(len(uhly)-1):
                self.play(UHEL.animate.set_value(uhly[i+1]), run_time = animation_runtime*(uhly[i+1]-uhly[i])/uhly_limit, rate_func=linear)
                self.wait()
            self.wait(wait_time)
            self.remove(komentar_mobj,matice_mobj,img)
            self.next_section()

        self.add(obrazky[-1])    


    def vzor_a_obraz(self,uhel,delka,matice):  
        vzor_souradnice = [delka*np.cos(uhel*DEGREES),delka*np.sin(uhel*DEGREES)]
        output = VGroup()
        vzor = Arrow(start=(0,0,0),end=(*vzor_souradnice,0),color= YELLOW,buff=0)
        obraz = Arrow(start=(0,0,0),end=[*np.matmul(matice,np.array(vzor.get_end())[:2]),0],color= RED,buff=0)
        output.add(vzor)
        output.add(obraz)
        # check that there are real eigenvales and matrix is not a multiple of identity matrix
        if ((matice[1,1]+matice[0,0])**2 >  4* (matice[0,0]*matice[1,1]- matice[1,0]*matice[0,1]) ) and ( matice[1,0] != 0 or matice[0,1] != 0 or matice[0,0] != matice[1,1]):
            vv = np.linalg.eig(matice)
            vv1 = [*vv[1].T[0]*5,0]
            vv2 = [*vv[1].T[1]*5,0]
            output.add(Line(start = [-i for i in vv1],end = vv1, color=GREEN) )
            output.add(Line(start = [-i for i in vv2], end = vv2, color=GREEN))                
        return output 

    def MatrixProduct(self,A,B,C,run_time=AnimationRuntime):
        """
        The function takes matrix 2x2 and 2x1 and animates the mutliplication using linear combination of columns.
        """
        a = A.copy()
        b = B.copy()
        c = C.copy()
        self.play(FadeIn(C.get_brackets()))
        cols_c = c.get_columns()
        for i in [0]:
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
    

komentar = """

Dobrý den, v tomto videu si ukážeme souvislost anatomických směrů dřeva s pojmy
lineární algebry. Z fyziky je známo, že tok tepla určíme násobením součinitele
tepelné vodivosti se spádem teploty. Zatímco ale v kovech teplo teče přesně ve
směru klesající teploty, ve dřevě to je jinak. Tok se částečně stáčí do
podélného směru. Proto musí součinitel tepla mít maticový charakter a tok
vypočteme násobením této matice s vektorem definujícícm spád teploty. 

Někdy se však směr toku tepla a směr spádu teploty přece jenom shodují i u
dřeva. Například pokud teplota klesá v podélném směru. V tomto případě teplo
teče také v podélném směru. Opravdu. Představme si situaci s vedením tepla ve
dvourozměrném případě v kusu prkna. Vlevo je horký konec, vpravo studený. Prkno
je nařezáno podélně. Představme si, že teplo by teklo například doprava nahoru.
Překlopením okolo delší hrany dostaneme opět prkno s podélným směrem zleva
doprava, s horým koncem nalevo a studeným napravo. Tedy stejně jako před
překlopením. Je to tedy fyzikálně zcela stejná situace, ale tok tepla změnil
směr. To je absurdní, takto příroda nefunguje. Proto tok tepla v tomto případě
musí být v podélném směru. 

Podobnou argumentaci můžeme použít i pro prkno nařezané kolmo na podélný směr.
Jediný rozdíl je v tom, že stejný teplotní spád vyvolá menší tepelný tok,
protože tepelná vodivost v tomto směru je menší. 

Naše úvaha ale nefunguje pro prkno nařezané našikmo. V tomto případě nedostaneme
po přetočení stejnou orientaci vláken a nemáme fyzikálně stejnou situaci. V
tomto případě se tok tepla od směru spádu teploty odklonit může a skutečně se
odklání.

Z uvedeného vidíme, že ve dvou případech dřevo pošle teplo ve směru spádu
teploty. Pokud je tento spád podél nebo napříč. Toto je zjednodušený
dvoudimenzionální model, ve 3D bychom měli směry tři, podélný, radiální a
tangenciální. 

Vzhledem k tom, že přepočet spádu teploty na tok obstarává maticové zobrazení
násobení, znamená to, že u tohoto zobrazení je stejný směr vzoru a obrazu. V
aplikacích i v teoretické matematice je nezbytné umět identifikvat takovou
situaci a proto si vektory mající uvedenou vlastnost vysloužily název vlastní
vektory. Teď se na ně podíváme geometricky. 

Žlutý vektor na obrázku je vektor u. Jeho obrazem ve zobrazení představovaném
maticí na obrazovce je červený vektor v. Žlutým vektorem budeme otáčet v rovině
a budeme sledovat, kdy budou oba vektory rovnoběžné. Buď souhlasně rovnoběžné
nebo nesouhlasně rovnoběžné, tj. pokud míří přesně stejným nebo přesně opačným
směrem. V situaci, kdy toto nastane, animaci na chvíli zastavíme. Zastávky,
vlastní směry, jsou vyznačeny zeleně. Podíl délek vektorů opatřený případně
znaménkem minus pokud vektory míří na opačnou stranu se nazývá vlastní hodnota.
V prvním případě vidíme dva vlastní směry zleva dole směrem doprava nahoru a
poté zprava dole směrem doleva nahoru. V tomto případě míří při zastavení oba
vektory stejným směrem a obě vlastní hodnoty jsou kladné. Jiná matice má jednu
vlastní hodnotu kladnou a druhou zápornou. Toto je málo zajímavé z praktického
hlediska, protože situace, kdy teplo samovolně teče proti směru spádu teploty v
přírodě nenastává. 

Matice nemusí mít žádný vlastní směr. Například matice s jednotkami v hlavní
diagonále a opačnými čísly blízkými k nule ve vedlejší diagonále je matice
malých rotací a ta vektor jenom potočí. Obraz zaostává za vzorem o konstantní
úhel a vektory nikdy nemíří ani stejným ani opačným směrem. Ani takto materiály
v přírodě nefungují.

Matice může mít naopak každý směr vlastní. To jsou nejhezčí materiály z hlediska
popisu vlastností. Teplo teče směrem, kterým klesá teplota. Takto fungují
materiály, mající ve všech směrech stejné vlastnosti. Například kovy. Příslušná
matice je násobkem jednotkové matice.

Matice diagonální s různými hodnotami v diagonále už vyjadřuje komplikovanější
situaci. Vlastní směry jsou kolmé a ve směrech souřadných os. To je příjemné.
Vlastní čísla však nejsou stejná. Tedy ve dvou směrech teče teplo směrem spádu
teploty, ale jednou lépe a podruhé hůře. Přesně jako jsme měli u dřeva. V
případech mimo vlastní směry se tok od spádu teploty odklání ve prospěch směru s
vyšší vodivostí, což je zde vodorovně. Naše matice odpovídá chování dřeva s
podélným směrem zleva doprava. Diagonální matice jsou pořád pěkné a relativně
snadné na zpracovávání. Aby nám v modelech materiálové vlastnosti vedly na
diagonální matice, snažíme se při studiu dřevěného materiálu volit souřadné osy
v anatomických směrech dřeva.

Pokud taková volba není možná a osy jsou skloněné vůči anatomickým směrům dřeva,
není příslušná matice už diagonální. Je symetrická, například jako na obrázku.
Co zůstává je kolmost vlastních směrů. V animaci vidíme, že je opět v jednom
vlastním směru obraz delší než ve druhém. To odpovídá podélnému a příčnému směru
dřeva v tomto pořadí. Přesně jako na obrazovce.

Ve videu jsme si ukázali, jak se dá symetrie využít k tomu, že v některých
případech umíme ukázat, že podnět a odezva při materiálovém namá hání mají stejný
směr. Pro identifikaci takových situací matematika zavádí pojem vlastní směr.
Ukázali jsme si, jak vlastní směry souvisí s tvarem matice. Prakticky zajímavými
případy z hlediska materiálových vlastností jsou diagonální matice a symetrická
matice.

"""
        