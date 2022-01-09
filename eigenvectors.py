from manim import *
import numpy as np

animation_runtime = 15
config.max_files_cached = 400
x_range = np.linspace(-4,4,500)

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

        title = Title(r"Vlastní směry matice")
        autor = VGroup(Tex("Robert Mařík"),Tex("Mendel University")).arrange(DOWN).next_to(title,DOWN)
        self.play(GrowFromCenter(title))
        self.play(GrowFromCenter(autor[0]))
        self.play(GrowFromCenter(autor[1]))
        self.wait(10)
        self.play(FadeOut(title),FadeOut(autor))

        self.next_section()

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

        #board['img_rotated'] = wood_obj.copy().rotate(90*DEGREES).move_to(board['rectangle'])
        board['arrow'] = Arrow(start = ORIGIN, end = 2*RIGHT, stroke_width=20, color=RED).move_to(board['rectangle'], aligned_edge=LEFT)
        board['arrow_declined'] = Arrow(start = ORIGIN, end = 2*RIGHT+decline*UP*.7, stroke_width=20, color=RED).move_to(board['rectangle'], aligned_edge=LEFT)
        board['arrow_short'] = Arrow(start = ORIGIN, end = RIGHT, stroke_width=20, color=RED, max_stroke_width_to_length_ratio=15, max_tip_length_to_length_ratio=0.5).move_to(board['rectangle'], aligned_edge=LEFT)

        def update_drawing(d,dt):
            d.rotate_about_origin(dt, RIGHT)

        board_copy = {}
        for _ in board.keys():
            board_copy[_]=board[_].copy()

        board['img'] = ImageMobject(wood_longitudal).scale_to_fit_width(6).set_color(WHITE).move_to(board['rectangle'])
        board['img_perp'] = ImageMobject(wood_perp).scale_to_fit_width(6).set_color(WHITE).move_to(board['rectangle'])
        board['img_slanted'] = ImageMobject(wood_slanted).scale_to_fit_width(6).set_color(WHITE).move_to(board['rectangle'])

        # Images for plane transformations
        obrazky = Group(Mobject(),Mobject(),Mobject(),Mobject(),
            board['img'].copy().scale_to_fit_width(6),
            board['img_slanted'].copy().scale_to_fit_width(6)
            ) 

        parts = ["arrow_declined","rectangle","temperature"]
        hidden_parts = ["arrow","arrow_short"]
        flip_parts = ["img_perp","img_slanted","img"]

        for _ in hidden_parts:
            board_copy[_].rotate_about_origin(180*DEGREES, RIGHT)

        self.add(*[board[_] for _ in parts],board['img'])
        self.add(*[board_copy[_] for _ in parts])

        self.wait()
        self.move_camera(
            phi=30 * DEGREES,
            theta=-50 * DEGREES
        )

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

        self.wait()

        self.play(
            ReplacementTransform(board['arrow_declined'].copy(),board['arrow']),
            ReplacementTransform(board_copy['arrow_declined'].copy(),board_copy['arrow']),
            FadeOut(board['arrow_declined']),
            FadeOut(board_copy['arrow_declined'])
        )

        self.wait()

        self.play(
            ReplacementTransform(board['arrow'],board['arrow_short']),
            ReplacementTransform(board_copy['arrow'],board_copy['arrow_short']),
            ReplacementTransform(board['img'], board['img_perp']),
            ReplacementTransform(board_copy['img'], board_copy['img_perp']),
        )

        self.wait()

        self.play(
            ReplacementTransform(board['arrow_short'],board['arrow_declined']),
            ReplacementTransform(board_copy['arrow_short'],board_copy['arrow_declined']),
            ReplacementTransform(board['img_perp'], board['img_slanted']),
            ReplacementTransform(board_copy['img_perp'], board_copy['img_slanted']),
        )

        self.wait()

        self.next_section()
        self.play(*[FadeOut(_) for _ in self.mobjects])
        self.wait()

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
            a11,a12,a21,a22 = _varianty
            matice = np.array([[a11,a12],[a21,a22]])
            matice_mobj_ = Matrix([[a11, a12], [a21, a22]], h_buff = 1.5).set_z_index(10)
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
            self.add(img.set_color(YELLOW).add_background_rectangle().set_z_index(10))

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
            self.next_section()

        self.add(obrazky[-1])    


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

komentar = """

Dobrý den, v tomto videu si ukážeme graficky vztah mezi vzorem a obrazem při
zobrazení reprezentovaném maticovým násobením. Toto je důležité znát při studiu
materiálů, které mají v různých směrech různé vlastnosti, což je celá řada
přírodních materiálů. Typicky dřevo. Zde může být vzorem při zobrazení
například spád teploty, obrazem tok tepla. Zobrazení spádu teploty na tok tepla
je reprezentováno násobením součinitele tepelné vodivosti v maticovém tvaru s
vektorem definujícím spád teploty. A například zatímco v kovech teče teplo ve
směru spádu teploty, ve dřevě se tok stáčí do podélného směru, ve kterém je
tepelná vodivost největší. Výsledný tok tepla je tedy jakýmsi kompromisem mezi
směrem, kterým klesá teplota a směrem, ve kterém má materiál nejlepší tepelnou
vodivost.

Co je však jistota je to, že pokud u dřeva máme podnět v podélném směru, teplo
teče také v tomto směru. Opravdu. Představme si situaci s vedením tepla. Podnět
je zleva doprava, vlevo je horký konec, vpravo studený. Prkno je nařezáno
podélně. To znamená, že překlopením okolo delší hrany dostaneme opět prkno s
podélným směrem zleva doprava. Stejně jako před překlopením. Je to tedy
fyzikálně zcela stejná situace. Předpoklad, že tok tepla znázorněný červenoým
vektorem je odkloněný nahoru nebo dolů, by spolu s otočením vedl k tomu, že
máme dvě fyzikálně identické situace, ale pokaždé s jiným výsledkem. Ve stejné
úloze jednou teče teplo doprava nahoru a jednou doprava dolů. To je absurdní,
takto příroda nefunguje. Proto tok tepla v tomto případě musí být v podélném
směru. Podobnou argumentaci můžeme použít i pro prkno nařezané kolmo na podélný
směr. Jediný rozdíl je v tom, že stejný tepelný spád vyvolá menší tepelný tok,
protože tepelné vodivost v tomto směru je menší. Naše úvaha ale nefunguje pro
prkno nařezané našikmo. V tomto případě nedostaneme po přetočení stejnou
orientaci vláken a nemáme fyzikálně stejnou situaci. V tomto případě se tok
tepla může odklonit od směru spádu teploty.

Z uvedeného vidíme, že ve dvou případech dřevo pošle teplo ve směru spádu
teploty. Pokud tento spád je podél nebo napříč. Toto je zjednodušený
dvoudimenzionální model, ve 3D bychom měli podélný, radiální a tangenciální
směr. Výše uvedené znamená, že u maticového zobrazení je stejný směr vzoru a
obrazu. V aplikacích i v teporetické matematice je nezbytné umět iudentifikvat
takovou situaci a proto si vektory mající uvedenou vlastnost vysloužily název
vlastní vektory. Teď se na ně podíváme geometricky. 

Žlutý vektor na obrázku je vektor u. Jeho obrazem ve zobrazení představovaném
maticí v na obrazovce je červený vektor. Žlutým vektorem budeme otáčet v rovině
a budeme sledovat, kdy oba vektory jsou rovnoběžné. Buď souhlasně nebo
nesouhlasně, tj. pokud míří přesně stejným nebo přesně opačným směrem. V
situaci, kdy toto nastane animaci na chvíli zastavíme. Tyto směry jsou
vyznačeny zeleně a jedná se o vlastní směry. Podíl délek vektorů opatřený
znaménkem minus, pokud vektory míří na opačnou stranu, se nazývá vlastní
hodnota. V prvním případě vidíme dva vlastní směry zleva dole směrem vpravo
nahoře a poté zprava dole směrem doleva nahoru. V tomto případě miří při
zastavení oba vektory stejným směrem a obě vlastní hodnoty jsou kladné. Jiná
matice má jednu vlastní hodnotu kladnou a druhou zápornou. Toto je málo
zajímavé z praktického hlediska, protože situace, kdy teplo samovolně teče
proti směru spádu tepla v přírodě nenastává. 

Matice nemusí mít žádný vlastní směr. Například matice s jednotkami v hlavní
diagonále a opačnými čísly blízkými k nule ve vedlejší diagonále je matice
malých rotací a ta vektor jenom potočí. Obraz zaostává za vzorem o konstantní
úhel a vektory nikdy nemíří ani stejným ani opačným směrem. Ani takto materiály
v přírodě nefungují.

Nejhezčí materiály bez výhrad poslouchají spád teploty. Například kovy. V nich
je každý směr vlastním směrem a teplo teče ve směru spádu teploty. Tyto
materiály jsou izotropní, mají ve všech směrech stejné vlastnosti a příslušná
matice je násobkem jednotkové matice.

Matice diagonální už vyjadřuje komplikovanější situaci. Vlastní směry jsou ve
směrech souřadných os. Vlastní čísla nejsou stejná. Ve vodorovném směru je
obraz delší a ve svislém kratší. V ostatních případech se obraz od vzoru
odklání ve prospěch vodorovného směru. To v přírodě odpovídá chování dřeva s
podélným směrem zleva doprava. Při studiu dřevěného materiálu volíme souřadné
osy v anatomických směrech dřeva právě proto, aby v matematickém popisu hrála
roli diagonální matice.

Pokud taková volba není možná a anatomické směry dřeva jsou skloněné vůči osám,
je příslušná matice symetrická. Například jako na obrázku. Opět je v jednom
vlastním směru obraz delší než ve druhém. To odpovídá podélnému a příčnému
směru dřeva v tomto pořadí. Přesně jako na obrazovce.

Ve videu jsme si ukázali, jak se dá symetrie využít k tomu, že v některých
případech umíme ukázat, že podnět a směr při materiálovém namáhání mají stejný
směr. Pro identifikaci takových situací matematika zavádí pojem vlastní směr.
Ukázali jsme si, jak vlastní směry souvisí s tvarem matice. Prakticky
zajímavými případy z hlediska materiálových vlastností jsou diagonální matice a
symetrická matice.


"""
        