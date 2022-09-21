# matice.py

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


class MatrixMultiplication(LinearTransformationScene):

    # def __init__(self):
    #     LinearTransformationScene.__init__(
    #         self,
    #         leave_ghost_vectors=True,
    #     )
    #def __init__(self):
    #    self.axis_config['']

    def construct(self):#, leave_ghost_vectors=True):

        self.next_section("Nadpis")
        title = Title(r"Matice a lineární transformace")
        autor = VGroup(Tex("Robert Mařík"),Tex("Mendel University")).arrange(DOWN).next_to(title,DOWN)
        title.add_background_rectangle()
        autor[0].add_background_rectangle()
        autor[1].add_background_rectangle()
        self.play(GrowFromCenter(title))
        self.play(GrowFromCenter(autor[0]))
        self.play(GrowFromCenter(autor[1]))
        self.setup()
        self.wait()


        i=1
        self.next_section("Transformace "+str(i))
        self.remove(autor[0],autor[1], title)
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
            self.apply_matrix(mtr)
            self.wait()
            self.remove(M)
            inverze = np.linalg.inv(np.array(mtr))
            self.next_section("Transformace "+str(i))
            self.moving_mobjects = []
            self.apply_matrix(inverze, run_time=0.4)
            #self.wait()


class TransformationCoordinates(LinearTransformationScene):

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

        self.next_section("Linearni kombinace")

        npv=np.array([[3,2]]).T
        v = Vector(npv.T[0]).set_color(YELLOW)
        znacka = MathTex(r"\vec{u}").next_to(v.get_end()).set_color(YELLOW)
        l = v.coordinate_label().set_color(BLUE).add_background_rectangle(buff=0.2)

        theta = 35*DEGREES
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
        self.next_section("Linearni kombinace po malem otoceni")

        self.remove(svorky_mobj)
        self.moving_mobjects = []
        self.apply_matrix(npMh)
        self.add(new_coor)

        svorky_mobj = svorky(poloha=npv1)
        self.add(svorky_mobj)
        self.wait()

        self.next_section("Linearni kombinace po vetsim otoceni")
        self.remove(new_coor, svorky_mobj)
        self.moving_mobjects = []
        self.apply_matrix(npMh)
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

class BranchRotation(Scene):
    def construct(self):
        data = np.genfromtxt('branch.csv', delimiter=',')
        ax_length = 3.6
        axes = VGroup()
        bokorys = Axes(
            x_range=[0,1600*0.7,1e5], y_range=[0,1600,1e5],
            x_length=ax_length*0.7,y_length=ax_length,
            tips=False,
            ).to_corner(UR)
        narys = Axes(
            x_range=[0,1600,1e5], y_range=[0,1600,1e5],
            x_length=ax_length,y_length=ax_length,
            tips=False,
            ).next_to(bokorys,LEFT)
        pudorys = Axes(
            x_range=[0,1600,1e5], y_range=[0,1600*0.7,1e5],
            x_length=ax_length,y_length=ax_length*0.7,
            tips=False,
            ).next_to(narys,DOWN)
        axonometrie = Axes(
            x_range=[0,2000,1e5], y_range=[0,2000,1e5],
            x_length=ax_length*0.5,y_length=ax_length*0.5,
            tips=False,
            ).next_to(bokorys,DOWN).shift(1.3*RIGHT+DOWN*0.5)

        matice = np.array([
            [0.2,-0.8,0],[0.1,0.2,0.8]
        ])
        osy = np.matmul(matice,np.array([
            [1600,0,0],[0,1600,0],[0,0,1600]
        ])).T
        temp = VGroup(
            axonometrie.plot_line_graph([0,osy[0,0]], [0,osy[0,1]], add_vertex_dots=False).set_color(GRAY),
            axonometrie.plot_line_graph([0,osy[1,0]], [0,osy[1,1]], add_vertex_dots=False).set_color(GRAY),
            axonometrie.plot_line_graph([0,osy[2,0]], [0,osy[2,1]], add_vertex_dots=False).set_color(GRAY),
            MathTex("x").scale(0.5).next_to(axonometrie.c2p(osy[0,0],osy[0,1]),RIGHT),
            MathTex("y").scale(0.5).next_to(axonometrie.c2p(osy[1,0],osy[1,1]),LEFT),
            MathTex("z").scale(0.5).next_to(axonometrie.c2p(osy[2,0],osy[2,1],UP)),
        )

        data_3d = np.matmul(matice,data.T).T
        vetev=VGroup(
            # axes.plot_line_graph(data[:,0],data[:,1],data[:,2],add_vertex_dots=False),
            narys.plot_line_graph(data[:,0],data[:,2],add_vertex_dots=False),
            bokorys.plot_line_graph(data[:,1],data[:,2],add_vertex_dots=False),
            pudorys.plot_line_graph(data[:,0],data[:,1],add_vertex_dots=False),
            axonometrie.plot_line_graph(data_3d[:,0],data_3d[:,1],add_vertex_dots=False),
        )

        nadpisy = VGroup(
            *[Tex(i).scale(0.6).move_to(j,UP) for i,j in 
            [
                [r"Pohled zepředu",narys],
                ["Pohled z boku",bokorys],
                ["Pohled shora",pudorys],
                ]]
        )

        popisky = VGroup(
            MathTex("z").scale(0.5).next_to(narys.get_y_axis(),LEFT, aligned_edge=UP, buff=0.05),
            MathTex("z").scale(0.5).next_to(bokorys.get_y_axis(),LEFT, aligned_edge=UP, buff=0.05),
            MathTex("x").scale(0.5).next_to(narys.get_x_axis(),UP, aligned_edge=RIGHT, buff=0.05),
            MathTex("y").scale(0.5).next_to(bokorys.get_x_axis(),UP, aligned_edge=RIGHT, buff=0.05),
            MathTex("x").scale(0.5).next_to(pudorys.get_x_axis(),UP, aligned_edge=RIGHT, buff=0.05),
            MathTex("y").scale(0.5).next_to(pudorys.get_y_axis(),LEFT, aligned_edge=UP, buff=0.05),
        )
        self.play(*[FadeIn(i) for i in [popisky,axes,temp,vetev,narys,bokorys,pudorys,nadpisy]])

        idx = [3, 39]  # body, ktere pri rotaci maji zustat na miste
        A = data[idx[0],:]
        B = data[idx[1],:]
        B_target = [800, None, 850]
        B_target[1] = np.sqrt(np.linalg.norm(B)**2-B_target[0]**2-B_target[2]**2)
        k2 = np.cross(B,B_target)
        k2 = k2/np.linalg.norm(k2)
        theta2 = angle_between(B,B_target)

        def nakresli_transformovanou_vetev(theta_,theta2_):
            K2 = np.array([[0 , -k2[2], k2[1]],[k2[2], 0, -k2[0]],[-k2[1], k2[0], 0]])

            I = np.identity(3);
            R2 = I + np.sin(theta2_)*K2 + (1-np.cos(theta2_))*np.matmul(K2,K2)

            k=B-A
            k=k/np.linalg.norm(k)
            K = np.array([[0 , -k[2], k[1]],[k[2], 0, -k[0]],[-k[1], k[0], 0]]);
            I = np.identity(3);

            R = I + np.sin(theta_)*K + (1-np.cos(theta_))*(np.matmul(K,K))

            data2 = np.matmul(np.matmul(R2,R),data.T).T
            data2_3d = np.matmul(matice,data2.T).T
            vetev2=VGroup(
                # axes.plot_line_graph(data[:,0],data[:,1],data[:,2],add_vertex_dots=False),
                narys.plot_line_graph(data2[:,0],data2[:,2],add_vertex_dots=False),
                Dot(narys.c2p(data2[idx[0],0],data2[idx[0],2],0)),
                Dot(narys.c2p(data2[idx[1],0],data2[idx[1],2],0)),
                Dot(bokorys.c2p(data2[idx[0],1],data2[idx[0],2],0)),
                Dot(bokorys.c2p(data2[idx[1],1],data2[idx[1],2],0)),
                Dot(pudorys.c2p(data2[idx[0],0],data2[idx[0],1],0)),
                Dot(pudorys.c2p(data2[idx[1],0],data2[idx[1],1],0)),
                bokorys.plot_line_graph(data2[:,1],data2[:,2],add_vertex_dots=False),
                pudorys.plot_line_graph(data2[:,0],data2[:,1],add_vertex_dots=False),
                axonometrie.plot_line_graph(data2_3d[:,0],data2_3d[:,1],add_vertex_dots=False),
                )
            vetev2.set_color(RED)
            return(vetev2)

        popis = Tex(r"""\begin{minipage}{9cm} Po vykreslení dat ze skenu je větev prakticky v ro\-vi\-ně $zx$. Je potřeba ji
        otočit okolo své osy do správné polohy (jedno maticové násobení)
        a naklonit do polohy dle experimentu (další maticové násobení).
        \end{minipage}
        """).scale(0.5).to_corner(UL)

        self.play(FadeIn(popis))
        self.wait()
        self.next_section("")

        popis1 = VGroup(
            Tex(r"$D$ je matice dat z 3D skenování větve").set_color(YELLOW),
            Tex(r"$R_2$ je transformace definující sklon"),
            Tex(r"$R_1$ je pootočení skloněné větve okolo osy"),
            Tex(r"$R_1R_2D$ je větev v poloze při experimentu").set_color(RED),
        ).scale(0.5).arrange(DOWN, aligned_edge=LEFT)

        popis2 = Tex(r"""\begin{minipage}{9cm}
        Je-li $\theta$ úhel otočení a $\vec k=(k_x, k_y, k_z)$ vektor osy otáčení, je matice rotace
        $R$ ve 3D prostoru dána vzta\-hem (Euler–Rodrigues formula) $$ R=I+\sin(\theta)K+(1-\cos(\theta))K^2, $$
        kde $$ K = \begin{pmatrix}0 & -k_z & k_y\\ k_z & 0 &-k_x\\
            -k_y & k_x&0\end{pmatrix}.$$
        Maticový součin je použit i pro převedení 3D dat do roviny při kreslení axonometrického obrázku.
        \end{minipage} """).scale(0.5)
        popis1.next_to(popis,DOWN, aligned_edge=LEFT)
        popis2.next_to(popis1,DOWN, aligned_edge=LEFT)
        self.play(FadeIn(popis1),FadeIn(popis2))
        self.wait()
        self.next_section("")

        uhel_skloneni = ValueTracker(0)
        uhel_otoceni = ValueTracker(0)
        a = always_redraw (
            lambda : nakresli_transformovanou_vetev(
                uhel_otoceni.get_value(),
                uhel_skloneni.get_value()
                ))
        self.add(a)
        self.play(uhel_skloneni.animate.set_value(theta2),run_time=5)
        self.play(uhel_otoceni.animate.set_value(4),run_time=5)
        self.wait()


