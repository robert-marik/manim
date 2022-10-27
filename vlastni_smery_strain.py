from manim import *
from manim_editor import PresentationSectionType
config.max_files_cached = 400

class PumpkinTransform(Scene):

    def construct(self):#, leave_ghost_vectors=True):

        self.next_section("")

        A = VGroup(
                Tex("Afinní zobrazení dýně"),
                Tex("Popis v \"obvyklé\" soustavě souřadnic"),
                Tex("Popis v soustavě souřadnic respektující vlastnosti zobrazení")
        )
        A[1].set_color(RED)
        A[2].set_color(YELLOW)
        for i in A:
            i.add_background_rectangle().to_edge(UP)

        for mtr in [
            [[5,2],[2,2]],
        ]:
            k = Circle(radius=1.0, fill_color=RED, fill_opacity=1)
            #kruh = VGroup(k.copy(),k.copy()).arrange(buff=-1.5)
            kruh = k
                
            ctverec = Rectangle(height=1, width=1, color=RED,fill_color=RED, fill_opacity=1
                ).shift(-0.25,-0.25)
            kruh.set_color(ORANGE)
            oci = VGroup(Triangle(),Triangle()).arrange(buff=2).set_color(YELLOW).set_fill(YELLOW, opacity=1)
            pusa = VGroup(*[Triangle().rotate(PI) for i in range(6)]).arrange(buff=-.8).set_color(YELLOW).set_fill(YELLOW, opacity=1)
            oci.scale(.2).shift(0.4*UP)
            pusa.scale(.2).shift(0.4*DOWN)
            teleso = VGroup(kruh,oci,pusa).set_z_index(-5)
            
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

            self.add(A[0], teleso)
            self.wait()
            self.next_section("")
            self.play(ApplyMatrix(mtr, teleso), 
              run_time=2)
            self.wait()

            self.next_section("")

            inverze = np.linalg.inv(np.array(mtr))
            self.next_section("")
            self.moving_mobjects = []
            self.play(ApplyMatrix(inverze, teleso), run_time=0.5)
            self.play(FadeIn(M), FadeIn(n),Transform(A[0],A[1]))
            self.play(ApplyMatrix(mtr, teleso), 
              ApplyMatrix(mtr, n)
              ,run_time=2)
            self.moving_mobjects=[]
            self.wait()

            self.next_section("")
            phantom = teleso.copy().set_fill(GRAY, opacity=1).set_stroke(color=GRAY, opacity=1)
            phantom.set_z_index(-15)
            self.add(phantom)
            self.play(ApplyMatrix(inverze, teleso), 
              ApplyMatrix(inverze, n),run_time=2)
 
            
            self.play(
                Rotate(n,angle=np.arctan(0.5), run_time=2)
            )
            self.wait(0.1)
            self.play(
                FadeToColor(n,YELLOW),
                Transform(A[1],A[2])
                )
            self.play(ApplyMatrix(mtr, teleso), 
              ApplyMatrix(mtr, n)
              ,run_time=2)
            self.play(FadeIn(M2))

            vysledek = VGroup(
                Tex(r"\textbf{Výhody:}"),
                Tex("Diagonální matice transformace"),
                Tex("Elementy zůstávají obdélníkové"),
            ).arrange(DOWN, aligned_edge=LEFT).add_background_rectangle()
            vysledek.to_corner(DR)
            self.play(FadeIn(vysledek))


            self.wait()
