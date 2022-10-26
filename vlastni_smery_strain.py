from manim import *
from manim_editor import PresentationSectionType
config.max_files_cached = 400

class PumpkinTransform(Scene):

    def construct(self):#, leave_ghost_vectors=True):

        self.next_section("")

        A = VGroup(
                Tex("Afinní zobrazení dýně"),
                Tex("Popis v \"přirozené\" soustavě souřadnic"),
                Tex("Popis v soustavě souřadnic respektující vlastnosti zobrazení")
        )
        A[1].set_color(RED)
        A[2].set_color(YELLOW)
        for i in A:
            i.add_background_rectangle().to_edge(UP)

        i=1
        # self.next_section("Transformace "+str(i))
        # self.remove(autor[0],autor[1], title)
        for mtr in [
            [[5,2],[2,2]],
        ]:
            i = i+1
            # for i in self.mobjects:
            #     self.remove(i)
            k = Circle(radius=1.0, fill_color=RED, fill_opacity=1)
            kruh = VGroup(k.copy(),k.copy()).arrange(buff=-1.5)
            kruh = k
                
            ctverec = Rectangle(height=1, width=1, color=RED,fill_color=RED, fill_opacity=1
                ).shift(-0.25,-0.25)
            kruh.set_color(ORANGE)
            oci = VGroup(Triangle(),Triangle()).arrange(buff=2).set_color(YELLOW).set_fill(YELLOW, opacity=1)
            pusa = VGroup(*[Triangle().rotate(PI) for i in range(6)]).arrange(buff=-.8).set_color(YELLOW).set_fill(YELLOW, opacity=1)
            oci.scale(.2).shift(0.4*UP)
            pusa.scale(.2).shift(0.4*DOWN)
            teleso = VGroup(kruh,oci,pusa).set_z_index(-5)
            
            teleso2 = teleso.copy()#.set_color(YELLOW)
            M = Matrix(
                mtr,
                element_to_mobject=lambda x: MathTex(round(x,2)),
                h_buff=1.7,
                v_buff=1.2,
                ).set_color(RED).to_corner(UL).shift(DOWN).add_background_rectangle(buff=0.2)
            M2 =  Matrix(
                [[3,0],[0,1]],
                element_to_mobject=lambda x: MathTex(round(x,2)),
                h_buff=1.7,
                v_buff=1.2,
                ).set_color(YELLOW).next_to(M,DOWN).add_background_rectangle(buff=0.2)   
            n = NumberPlane(
                x_range=[-10,10,0.25],
                y_range=[-10,10,0.25],
                background_line_style={
                "stroke_color": WHITE,
                "stroke_opacity":0.5}
                ).set_z_index(-1)
            n2 = NumberPlane(
                x_range=[-10,10,0.25],
                y_range=[-10,10,0.25],
                background_line_style={
                "stroke_color": TEAL,}).set_z_index(-1)

            teleso0 = teleso.copy()

            self.add(A[0])
            self.play(FadeIn(teleso0))
            self.wait()
            self.next_section("")
            #return False
            self.play(ApplyMatrix(mtr, teleso0), 
              run_time=2)
            self.wait()

            self.next_section("")
            self.play(
                FadeOut(teleso0),
                FadeIn(teleso), FadeIn(M), FadeIn(n))  
            
            self.play(Transform(A[0],A[1]))
            self.play(ApplyMatrix(mtr, teleso), 
              #ApplyMatrix(mtr, n),
              ApplyMatrix(mtr, n)
              ,run_time=2)
            #self.moving_mobjects = []
            self.wait()
            self.next_section("")

            self.play(FadeOut(n))

            self.play(teleso.animate.set_fill(GRAY, opacity=1).set_stroke(color=GRAY, opacity=1))

            self.play(Transform(A[1],A[2]))

            self.add(n2,teleso2)

            self.play(Rotate(n2,angle=np.arctan(0.5)))
            self.play(ApplyMatrix(mtr, teleso2), 
              #ApplyMatrix(mtr, n),
              ApplyMatrix(mtr, n2)
              ,run_time=2)
            #self.apply_matrix(mtr)
            self.play(FadeIn(M2))
            self.wait()
