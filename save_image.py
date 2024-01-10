# matice.py

from manim import *
config.max_files_cached = 400
from numpy import sin, cos
from PIL import Image

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


class MatrixMultiplication(LinearTransformationScene):

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
            self.apply_matrix(mtr, run_time=0.01)
            self.wait(duration=0.01)
            save_current_frame(self, "example")
            self.remove(M)
            inverze = np.linalg.inv(np.array(mtr))
            self.next_section("Transformace "+str(i))
            self.moving_mobjects = []
            self.apply_matrix(inverze, run_time=0.01)

