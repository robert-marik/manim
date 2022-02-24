from curses.ascii import CR
from manim import *
from common_definitions import *

from manim_editor import PresentationSectionType
config.max_files_cached = 400

insect = os.path.join("icons","motyl.png")

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

        popisek_x = Tex(r"velikost populace škůdce").scale(0.7)
        popisek_x.next_to(axes.get_x_axis(), DOWN)

        popisek_y = Tex(r"dynamika populace škůdce").scale(0.7).rotate(PI/2)
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
            print (indexy_zmen)
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
            nadpis.scale(0.7).to_corner(UL).set_color(YELLOW)
            nadpis.add_background_rectangle(buff=0.2).set_z_index(10)
            self.play(GrowFromCenter(nadpis))
            self.wait()
            return nadpis 


        temp = komentar(r"Jeden kladný stacionární bod.")
        self.wait()
        self.remove(temp)

        zoomed_camera = self.zoomed_camera
        zoomed_display = self.zoomed_display
        frame = zoomed_camera.frame
        zoomed_display_frame = zoomed_display.display_frame
        frame.move_to(axes.c2p(0,0,0)).shift(2.75*RIGHT+3*UP)
        zoomed_display.to_corner(DR)

        self.play(K.animate.set_value(6.35), run_time=5)
        temp = komentar(r"Vznikají další\\stacionární body.")

        self.play(Create(frame))
        zd_rect = BackgroundRectangle(zoomed_display, fill_opacity=0, buff=MED_SMALL_BUFF)        
        self.activate_zooming()        
        unfold_camera = UpdateFromFunc(zd_rect, lambda rect: rect.replace(zoomed_display))
        self.play(self.get_zoomed_display_pop_out_animation(), unfold_camera)                
        self.wait()
        self.remove(temp)

        self.play(K.animate.set_value(7.5),frame.animate.shift(1 * DOWN + 1.4*LEFT), run_time=3)
        temp = komentar(r"Dva stacionární body\\brzy zaniknou.\\Zůstane stabilní hodnota,\\která je násobně větší.")
        self.wait()
        self.remove(temp)

        self.play(K.animate.set_value(9), run_time=3)
        temp = komentar(r"Zůstává jenom jeden\\stacionární bod odpovídající\\řádově větší populaci.")
        self.remove(temp)
        self.wait()

        self.play(FadeOut(frame), FadeOut(zoomed_display), FadeOut(zoomed_display_frame))
        self.play(K.animate.set_value(13), run_time=5)
        self.wait()


