# matice.py

from manim import *
import light_theme

config.max_files_cached = 400
from numpy import sin, cos
from PIL import Image

from manim_slides import Slide, ThreeDSlide

def save_current_frame(self, path=None):
    if path is None:
        path = "frame"
    self.renderer.file_writer.output_image(
        Image.fromarray(self.renderer.get_frame()), 
        path, 
        ".png", 
        config["zero_pad"])

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



class MatrixMultiplication(LinearTransformationScene, Slide):

    # def __init__(self):
    #     LinearTransformationScene.__init__(
    #         self,
    #         leave_ghost_vectors=True,
    #     )
    #def __init__(self):
    #    self.axis_config['']

    def construct(self):#, leave_ghost_vectors=True):

        i=1
        for mtr in [
            [[2,0],[0,2]],
            [[3,0],[0,1]],
            [[1,.6],[0,1]],
            [[2.3,0],[0,0.7]],
            [[1,0.2],[-0.2,1]],
            [[1,0.2],[0.2,1]],
        ]:
            i = i+1
            # for i in self.mobjects:
            #     self.remove(i)
            M = Matrix(
                mtr,
                element_to_mobject=lambda x: MathTex(round(x,2)),
                h_buff=1.7,
                v_buff=1.2,
                ).to_corner(UL).add_background_rectangle(buff=0.2)
            self.add(M)
            self.moving_mobjects = []
            self.apply_matrix(mtr)
            self.wait(duration=0.01)
            save_current_frame(self, "example")
            self.next_slide()            
            self.remove(M)
            inverze = np.linalg.inv(np.array(mtr))
            self.next_section("Transformace "+str(i))
            self.moving_mobjects = []
            self.apply_matrix(inverze, run_time=0.2)


class TransformationCoordinates(LinearTransformationScene, Slide):

    # def __init__(self):
    #     LinearTransformationScene.__init__(
    #         self,
    #         leave_ghost_vectors=True,
    #     )

    def construct(self):

        def svorky(poloha):
            b1 = Brace(v,direction=RIGHT, buff=0.6).set_color(GRAY)
            b1.add(MathTex(round(poloha[1,0],2), color=GRAY).next_to(b1).add_background_rectangle(buff=0.2).set_z_index(2))            
            b2 = Brace(v,direction=DOWN, buff=0.3).set_color(GRAY)
            b2.add(MathTex(round(poloha[0,0],2), color=GRAY).next_to(b2,DOWN).add_background_rectangle(buff=0.2))
            return(VGroup(b1,b2))

        #self.setup()

        # self.next_section("Linearni kombinace")

        npv=np.array([[3,2]]).T
        v = Vector(npv.T[0]).set_color(YELLOW)
        znacka = MathTex(r"\vec{u}").next_to(v.get_end()).set_color(YELLOW)
        l = v.coordinate_label().set_color(BLUE).add_background_rectangle(buff=0.2)

        theta = 25*DEGREES
        npM = np.array([[cos(theta), -sin(theta)], [sin(theta), cos(theta)]])
        npMh = np.array([[cos(theta/2), -sin(theta/2)], [sin(theta/2), cos(theta/2)]])
        M = Matrix(
                npM,
                element_to_mobject=lambda x: MathTex(round(x,2)),
                h_buff=1.7,
                v_buff=1.2,
                ).to_corner(UL).add_background_rectangle(buff=0.2)
        M.set_column_colors(GREEN,RED)
        kombinace = MathTex(r"\vec u","=",r"3\cdot",r"\vec i","+",r"2\cdot",r"\vec j")
        kombinace[0].set_color(YELLOW)
        kombinace[3].set_color(GREEN)
        kombinace[-1].set_color(RED)
        kombinace.add_background_rectangle(buff=0.1)
        kombinace.to_corner(UR)

        popisky=VGroup(
            MathTex(r"\vec u").next_to(v.get_vector()).set_color(YELLOW),
            MathTex(r"\vec i").next_to(self.get_basis_vectors()[0]).set_color(GREEN),
            MathTex(r"\vec j").next_to(self.get_basis_vectors()[1],UP).set_color(RED)
        )

        for i in popisky:
            i.add_background_rectangle()

        vec_i = Vector([1,0]).set_color(GREEN)
        vec_j = Vector([0,1]).set_color(RED)
        self.add_transformable_mobject(vec_i,vec_j)
        
        self.add_vector(v)
        popisky[0].add_updater(lambda x: x.next_to(v.get_vector()))
        popisky[1].add_updater(lambda x: x.next_to(vec_i.get_vector()))
        popisky[2].add_updater(lambda x: x.next_to(vec_j.get_vector(),UP))
        self.add(popisky,kombinace)
        svorky_mobj = svorky(poloha=npv)
        self.add(svorky_mobj)

        original_coor = Matrix(npv, 
                element_to_mobject=lambda x: MathTex(round(x,2)))
        original_coor.set_color(BLUE).add_background_rectangle(buff=0.2)        
        npv1 = np.matmul(npMh,npv)
        npv2 = np.matmul(npM,npv)
        
        new_coor = Matrix(npv1, 
                element_to_mobject=lambda x: MathTex(round(x,2)))
        new_coor.to_corner(DL).set_color(GRAY)
        original_coor.next_to(new_coor,UP,buff=0.2, aligned_edge=LEFT)
        new_coor.add_background_rectangle()

        self.add(original_coor)
        self.wait()
        # self.next_section("Linearni kombinace po malem otoceni")

        # self.remove(svorky_mobj)
        # self.moving_mobjects = []
        # self.apply_matrix(npMh)
        # self.add(new_coor)

        # svorky_mobj = svorky(poloha=npv1)
        # self.add(svorky_mobj)
        # self.wait()

        self.next_section("Linearni kombinace po vetsim otoceni")
        self.remove(new_coor, svorky_mobj)
        self.moving_mobjects = []
        self.apply_matrix(npM)
        new_coor = Matrix(npv2, 
                element_to_mobject=lambda x: MathTex(round(x,2)))
        new_coor.next_to(original_coor,DOWN,aligned_edge=LEFT).set_color(GRAY)
        new_coor.add_background_rectangle()
        self.add(new_coor)
        self.wait()

        svorky_mobj = svorky(poloha=npv2)
        self.add(svorky_mobj)
        self.wait()

        self.next_section("Matice prechodu")
        self.add(M)

        self.next_section("Transformacni rovnice")
        self.wait()
        rovnitko = MathTex(r"=").next_to(new_coor)
        self.add(rovnitko)

        self.play(M.copy().animate().next_to(rovnitko))
        self.play(original_coor.copy().animate().next_to(rovnitko, buff=4))

        self.wait()
        #self.move_to()
