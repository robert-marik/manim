from curses.ascii import CR
from manim import *
from common_definitions import *

from manim_editor import PresentationSectionType
config.max_files_cached = 400

insect = os.path.join("icons","motyl.png")
bird = os.path.join("icons","ptacek.png")


class Intro(Scene):
    def construct(self):

        self.next_section("Nadpis")        
        title = Title(r"Periodické přemnožování obaleče")
        autor = VGroup(Tex("Robert Mařík"),Tex("Mendel University")).arrange(DOWN).next_to(title,DOWN)
        self.play(GrowFromCenter(title))
        self.play(GrowFromCenter(autor[0]))
        self.play(GrowFromCenter(autor[1]))
        self.wait()

class Popis(Scene):
    def construct(self):

        template = TexTemplate(preamble=r'\usepackage{url}\usepackage[czech]{babel}\usepackage{amsmath}\usepackage{amssymb}')
        texty = [
            r"""
            D. Ludwig, D. D. Jones, C. S. Holling: Qualitative Analysis of Insect Outbreak Systems: 
            The Spruce Budworm and Forest, \textit{The Journal of Animal Ecology}, Vol. 47, 
            No. 1. (Feb., 1978), pp. 315-332 (1978).
            """,
            r"""
            Model navržen pro vysvětlení periodického přemnožování obaleče (\textit{Choristoneura 
            fumiferana}) v kanadských lesích každých cca 30 až 40 let. Jeden
            z posledních od roku 2006 v Quebecu, do 2019 zasaženo cca 9.6 milionů
            hektarů (zdroj: \url{www.nrcan.gc.ca}, rozloha ČR je 7.8 milionů hektarů).
            """,
            r"""
            Dosavadní model obsahoval Canadian Forestry Service 30 654 proměnných
            a omezil se na popis, nedokázal podchytit příčinu.
            """,
            r"""
            Nový model sleduje populaci obaleče v prostředí s omezenou nosnou kapacitou. 
            V rostoucím lese roste nosná kapacita prostředí pro populaci obaleče roste 
            (větší les uživí více obaleče). Obsahuje působení predátorů (ptáků) a vysvětluje i příčiny 
            periodických přemnožení obaleče.
            """,
            r"""
            Model realisticky zachycuje, jak působení predátorů zpomaluje růst populace obaleče. 
            Pokud je obaleče málo, predátoři konzumují jinou potravu. Pokud je obaleče hodně, predátoři 
            konzumují jenom do své saturace.
            """,
            r"""Model předpokládá, že dynamika obaleče je rychlá ve srovnání s dynamikou lesa, protože les roste pomalu.""",
            r"""Dynamika predátorů je nezávislá na populaci obaleče, protože predátoři mají alternativní potravu.""",
            r"""
            V důsledku rychlé dynamiky populace obaleče v porovnání s dynamikou růstu lesa je velikost 
            populace obaleče v podstatě stále v rovnovážném stavu, který odpovídá podmínkám prostředí.
            """
        ]
        legenda = VGroup(*[Tex(r"$\bullet$ \begin{minipage}[t]{10cm}"+i+r"\end{minipage}", tex_template=template).scale(0.8) for i in texty])
        legenda.arrange(DOWN, aligned_edge=LEFT).to_edge(UP).set_color(BLACK)
        for i in range(len(texty)):
            self.next_section()        
            spodek = legenda[i].get_edge_center(DOWN)[1]
            if spodek < -2.5:
                self.play(legenda.animate.shift(UP*(-2.5-spodek)))
            self.play(FadeToColor(legenda[i],WHITE))
            self.wait()

class PopisMat(MovingCameraScene):
    def construct(self):

        self.next_section()        
        rovnice = MathTex(r"{{\frac{\mathrm dx}{\mathrm dt}}} = {{f(x)}} - {{g(x)}}")
        rovnice.to_edge(UP)
        rovnice[0].set_color(YELLOW)
        rovnice[2].set_color(BLUE)
        rovnice[4].set_color(RED)
        self.play(Create(rovnice))

        komentar = [
            r"Rychlost růstu populace obaleče",
            r"Růst bez přítomnosti predátorů",
            r"Zpomalení růstu působením predátorů"]
        
        legenda1 = VGroup(*[VGroup(rovnice[i].copy()) for i in [0,2,4]]).arrange(DOWN, aligned_edge=RIGHT, buff=0.5)
        for i,j in enumerate(komentar):
            legenda1[i].add(Tex(j).next_to(legenda1[i], buff=2))

        legenda1.next_to(rovnice,DOWN,buff=1)
        self.play(Create(legenda1))
        self.wait()

        self.next_section()        
        self.remove(legenda1)
        insect_mob = ImageMobject(insect).scale_to_fit_width(1.5).set_color(BLUE)        
        bird_mob = ImageMobject(bird).scale_to_fit_width(2.5).set_color(RED)

        ax1 = Axes (x_range=[0,1.1,2], y_range=[0,0.5,1], tips=False)
        ax1.scale(0.4).to_edge(LEFT)

        popisky1 = VGroup(
            ax1.get_x_axis_label(
            label = Tex(r"velikost populace obaleče").scale(0.6),
            edge=DOWN, 
            direction=DOWN),
            Tex(r"""
            rychlost růstu populace obaleče\\bez přítomnosti predátorů\\{}
            """).scale(0.6).move_to(ax1, aligned_edge=UP).set_color(BLUE),
            VGroup()
            )
        ax1.add(popisky1)
        f1 = ax1.plot(lambda x:x*(1-x)).set_color(BLUE)

        texty = [r"""Populace obaleče roste podle logistické rovnice.""",
        r"""Je-li málo obaleče, predátoři konzumují jinou potravu.""",
        r"""Je-li obalečů víc, predátoři konzumují úměrně množství.""",
        r"""Predátoři konzumují jenom do svého nasyceni."""
        ]
        template = TexTemplate(preamble=r'\usepackage{url}\usepackage[czech]{babel}\usepackage{amsmath}\usepackage{amssymb}')
        legenda = VGroup(*[Tex(r"$\bullet$ \begin{minipage}[t]{10cm}"+i+r"\end{minipage}", tex_template=template).scale(0.8) for i in texty])
        legenda.arrange(DOWN, aligned_edge=LEFT, buff=0.05)
        legenda.to_edge(DOWN)        
        legenda.set_color(RED)
        legenda[0].set_color(BLUE)


        ax2 = Axes (x_range=[0,8,20], y_range=[0,1,6], tips=False)
        ax2.scale(0.4).to_edge(RIGHT)
        popisky2 = VGroup(
            ax2.get_x_axis_label(
            label = Tex(r"velikost populace obaleče").scale(0.6),
            edge=DOWN, 
            direction=DOWN),
            Tex(r"""
            rychlost s jakou predátoři\\likvidují populaci obaleče
            """).scale(0.6).move_to(ax2).set_color(RED)
            )
        ax2.add(popisky2)        
        f2s = VGroup(*[ax2.plot(lambda x:x**3/(1+x**3), x_range=[*i,0.01]) for i in [[0,0.4],[0.4,1],[1,8]]])
        f2s.set_color(RED)

        insect_mob.next_to(ax1,UP)
        bird_mob.next_to(ax2,UP)

        self.play(FadeIn(insect_mob))
        self.play(Create(ax1),Create(f1),FadeIn(legenda[0]))
        self.wait()

        self.next_section("Predation 1/3")        
        self.play(FadeIn(bird_mob))
        self.play(Create(ax2),Create(f2s[0]),FadeIn(legenda[1]))

        detail = f2s[0]
        self.camera.frame.save_state()
        detail_frame = SurroundingRectangle(detail, color=GRAY, buff=.2)
        self.play(self.camera.frame.animate.set(width=detail_frame.width*2).move_to(detail), FadeIn(detail_frame), running_time = 2)
        self.wait()

        self.next_section("Predation 2/3")        
        self.play(Restore(self.camera.frame),FadeOut(detail_frame), running_time = 2)   
        self.play(Create(f2s[1]),FadeIn(legenda[2]))
        self.wait()

        self.next_section("Predation 3/3")        
        self.play(Create(f2s[2]),FadeIn(legenda[3]))
        self.wait()

class Model(ZoomedScene):

    def __init__(self, **kwargs):
        ZoomedScene.__init__(
            self,
            zoom_factor=0.3,
            zoomed_display_height=5,
            zoomed_display_width=5,
            image_frame_stroke_width=20,
            zoomed_camera_config={
                "default_frame_stroke_width": 3,
                },
            **kwargs
        )

    def construct(self):
        
        tmax = 12.5
        r = 0.57
        K = ValueTracker(2)

        axes = Axes(
            x_range=[0,tmax,1e6], 
            y_range=[0,1.75,1e6],
            tips = False)

        popisek_x = Tex(r"velikost populace obaleče").scale(0.7)
        popisek_x.next_to(axes.get_x_axis(), DOWN)

        popisek_y = Tex(r"dynamika populace obaleče").scale(0.7).rotate(PI/2)
        popisek_y.next_to(axes.get_y_axis(), LEFT)

        t = np.linspace(0,12.5,5000)
        predatori = t**2/(1+t**2)
        c_predatori = axes.plot_line_graph(x_values=t,y_values=predatori, add_vertex_dots=False, line_color=RED)

        def kresli_parabolu():
            t_pos = np.linspace(0,K.get_value(),500) 
            logisticky_rust = r*t_pos*(1-t_pos/K.get_value()) 
            vystup = VGroup()
            vystup.add(axes.plot_line_graph(x_values=t_pos,y_values=logisticky_rust, add_vertex_dots=False, line_color=BLUE))
            return vystup
        c_logisticky_rust =  always_redraw(lambda : kresli_parabolu())

        self.next_section("Simulace rustu")
        self.play(Create(axes))
        self.play(FadeIn(popisek_x,popisek_y))
        self.play(Create(c_logisticky_rust))
        self.play(Create(c_predatori))

        insect_mob = ImageMobject(insect).scale_to_fit_width(1.5).set_color(BLUE)
        def draw_for_animation():
            eq_rhs = r*t*(1-t/K.get_value()) - t**2/(1+t**2)
            equilibrium = np.argmax(eq_rhs<0)
            kwds = {
                    'value_max' : tmax, 
                    'values' : np.array(range(5))/4*tmax,
                    }
            vystup = VGroup()
            vystup.add(analog_indicator(t[equilibrium],**kwds).to_corner(UR))
            vystup.add(Line(start=axes.c2p(t[equilibrium],0,0),
                end=axes.c2p(t[equilibrium],t[equilibrium]**2/(1+t[equilibrium]**2),0)
                ).set_color(YELLOW).set_stroke(width=2))
            zmeny_znamenka = np.diff(eq_rhs<0)
            indexy_zmen = [i for i,j in enumerate(zmeny_znamenka) if j]
            for i in indexy_zmen:
                vystup.add(Circle(radius=0.1).move_to(axes.c2p(t[i],t[i]**2/(1+t[i]**2),0)).set_color(YELLOW).set_stroke(width=2))
            vystup.set_z_index(12)
            return vystup

        _hodiny = draw_for_animation()
        #self.add(hodiny)
        insect_mob.next_to(_hodiny[0],DOWN)
        self.add(insect_mob)
        hodiny = always_redraw(lambda : draw_for_animation() )
        self.add(hodiny)

        def komentar(text):
            nadpis = Tex(text)
            nadpis.scale(0.7).to_corner(UL).set_color(BLACK)
            nadpis.add_background_rectangle(buff=0.2, color=YELLOW).set_z_index(10)
            self.play(GrowFromCenter(nadpis))
            self.wait()
            return nadpis 


        temp = komentar(r"Jeden kladný stacionární bod pro malý les.")
        self.wait()


        self.next_section("Simulace rustu 2")
        self.remove(temp)
        zoomed_camera = self.zoomed_camera
        zoomed_display = self.zoomed_display
        frame = zoomed_camera.frame
        zoomed_display_frame = zoomed_display.display_frame
        frame.move_to(axes.c2p(0,0,0)).shift(2.75*RIGHT+3*UP)
        zoomed_display.to_corner(DR)

        self.play(K.animate.set_value(6.35), run_time=5)
        temp = komentar(r"""
        Jak les roste, roste jeho nosná kapacita a vznikají další stacionární body.\\
        Stabilní stacionární bod vpravo je oddělen nestabilním stacionárním bodem.\\
        Proto nás v tuto chvíli nemusí zajímat. Velikost populace je (zatím) malá.
        """)

        self.play(Create(frame))
        zd_rect = BackgroundRectangle(zoomed_display, fill_opacity=0, buff=MED_SMALL_BUFF)        
        self.activate_zooming()        
        unfold_camera = UpdateFromFunc(zd_rect, lambda rect: rect.replace(zoomed_display))
        self.play(self.get_zoomed_display_pop_out_animation(), unfold_camera)                
        self.wait()

        self.next_section("Simulace rustu 3")
        self.remove(temp)
        self.play(K.animate.set_value(8.5),frame.animate.shift(1 * DOWN + 1.4*LEFT), run_time=3)
        temp = komentar(r"""
        Dva stacionární body brzy zaniknou.\\
        Zůstane jediný stabilní stacionární bod.\\
        V něm je velikost populace násobek předchozího.""")
        self.wait()

        self.next_section("Simulace rustu 4")
        self.remove(temp)
        self.play(K.animate.set_value(9), run_time=3)
        temp = komentar(r"""
        V levé části grafu už průsečíky nejsou. Zůstává jenom jeden\\
        stacionární bod vpravo odpovídající řádově větší populaci.\\
        Řešení doroste do stacionárního stavu odpovídajícího přemnožení.""")
        self.wait()

        self.next_section("Simulace rustu 4")
        self.remove(temp)
        self.play(FadeOut(frame), FadeOut(zoomed_display), FadeOut(zoomed_display_frame))
        self.play(K.animate.set_value(13), run_time=5)
        temp = komentar(r"""
        Zůstal jeden stacionární bod zucela vpravo. \\
        Populace obaleče je přemnožená a zdecimuje les.
        """)
        self.wait()


