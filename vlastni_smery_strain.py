from manim import *
from manim_editor import PresentationSectionType
config.max_files_cached = 400
from numpy import sin, cos

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)

def angle_between(v1, v2):
    """ Returns the angle in radians between vectors 'v1' and 'v2'::

            >>> angle_between((1, 0, 0), (0, 1, 0))
            1.5707963267948966
            >>> angle_between((1, 0, 0), (1, 0, 0))
            0.0
            >>> angle_between((1, 0, 0), (-1, 0, 0))
            3.141592653589793
    """
    v1_u = unit_vector(v1)
    v2_u = unit_vector(v2)
    return np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0))


class MatrixMultiplication(Scene):

    # def __init__(self):
    #     LinearTransformationScene.__init__(
    #         self,
    #         leave_ghost_vectors=True,
    #     )
    #def __init__(self):
    #    self.axis_config['']

    def construct(self):#, leave_ghost_vectors=True):

        # self.next_section("Nadpis")
        # title = Title(r"Matice a lineární transformace")
        # autor = VGroup(Tex("Robert Mařík"),Tex("Mendel University")).arrange(DOWN).next_to(title,DOWN)
        # title.add_background_rectangle()
        # autor[0].add_background_rectangle()
        # autor[1].add_background_rectangle()
        # self.play(GrowFromCenter(title))
        # self.play(GrowFromCenter(autor[0]))
        # self.play(GrowFromCenter(autor[1]))
        # self.setup()
        # self.wait()


        i=1
        # self.next_section("Transformace "+str(i))
        # self.remove(autor[0],autor[1], title)
        for mtr in [
            [[5,2],[2,2]],
        ]:
            i = i+1
            # for i in self.mobjects:
            #     self.remove(i)
            kruh = Circle(radius=1.0, fill_color=RED, fill_opacity=1)
            ctverec = Rectangle(height=1, width=1, color=RED,fill_color=RED, fill_opacity=1
                ).shift(-0.25,-0.25)
            teleso = VGroup(kruh,ctverec).set_z_index(-5)
            self.add(teleso)
            M = Matrix(
                mtr,
                element_to_mobject=lambda x: MathTex(round(x,2)),
                h_buff=1.7,
                v_buff=1.2,
                ).to_corner(UL).add_background_rectangle(buff=0.2)
            n = NumberPlane(
                x_range=[-10,10,0.25],
                y_range=[-10,10,0.25],
                ).set_z_index(-1)
            n2 = NumberPlane(
                x_range=[-10,10,0.25],
                y_range=[-10,10,0.25],
                background_line_style={
                "stroke_color": TEAL,}).set_z_index(-1)
            self.add(M,n2)
            #self.moving_mobjects = []
            self.play(Rotate(n2,angle=np.arctan(0.5)))
            self.play(ApplyMatrix(mtr, teleso), 
              #ApplyMatrix(mtr, n),
              ApplyMatrix(mtr, n2)
              ,run_time=2)
            #self.apply_matrix(mtr)
            self.wait()
            self.remove(M)

            #self.wait()

