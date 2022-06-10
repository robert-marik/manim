
from manim import *
from manim_editor import PresentationSectionType
config.max_files_cached = 400
from numpy import sin, cos

import matplotlib.pyplot as plt

def unit_vector(vector):
    """ Returns the unit vector of the vector.  """
    return vector / np.linalg.norm(vector)



class SmerovePole(Scene):


    def construct(self):

        jednotka = 1
        xmin,xmax = 0,12
        ymin,ymax = 0,6
        ax = Axes(
            x_range=[xmin,xmax,100],
            x_length=(xmax-xmin)*jednotka, 
            y_range=[ymin,ymax,100], 
            y_length=(ymax-xmin)*jednotka, 
            tips=False
            )

        def rhs(x,y):
            #return np.sin(x)+0.5*y
            return 1/2*x-y
            #return 4-y
            #return 0.31*y*(5-y)-1.5

        # pro funkci 0.31*y*(5-y)-1.5 na commons wikimedia
        stabilni = [3.688]
        nestabilni = [1.312]

        Y, X = np.mgrid[ymin:ymax:100j, xmin:xmax:100j]

        def plot_streams():
            U = X*0+1
            V = rhs(X,Y)
            speed = np.sqrt(U*U + V*V)
            stream_img = plt.streamplot(
                X, Y, U, V,
                #maxlength = 1,
                #density = 0.6
                )
            sgm = stream_img.lines.get_segments()
            krivky = []
            lastpoint = sgm[0]
            aktualni_krivka = [lastpoint[1,:]]
            n = 0
            for i in sgm[1:]:
                n = n+1
                #print("Bod "+str(n)+" \n"+str(i))
                if all(i[0,:] == lastpoint[1,:]):
                    aktualni_krivka = aktualni_krivka + [i[0,:],i[1,:]]
                    #print ("            Pridavam k predchozi vetvi, delka je "+str(len(aktualni_krivka)))
                else:
                    krivky = krivky + [aktualni_krivka]
                    aktualni_krivka = [i[0,:],i[1,:]]
                    #print ("Zakladam novou vetev")
                lastpoint = i
            krivky = krivky + aktualni_krivka
            ciste_krivky = [np.array(i) for i in krivky if len(i)>3]
            #streams = VGroup()
            #for t in ciste_krivky:
            #    streams.add(axes.plot_line_graph(t[:,0],t[:,1], add_vertex_dots=False))
            #return(streams)
            return ([
                ax.plot_line_graph(
                    t[:,0],t[:,1], add_vertex_dots=False
                    ).set_stroke(width=2).set_z_index(-5).set_color(WHITE) 
                    for t in ciste_krivky
            ])


        slope_field = VGroup()
        imax,jmax = 20,10
        for i in range(imax):
            xcoor = xmin + i*(xmax-xmin)/imax
            for j in range(jmax):
                ycoor = ymin + j*(ymax-ymin)/jmax
                smernice = rhs(xcoor,ycoor)
                delka = 0.3
                dX = 1/np.sqrt(1+smernice**2)*delka
                dY = smernice/np.sqrt(1+smernice**2)*delka
                slope_field.add(
                    Line(
                        start = ax.c2p(xcoor,ycoor,0), 
                        end = ax.c2p(xcoor+dX,ycoor+dY))
                        )
        slope_field.set_color(YELLOW).set_stroke(width=6)
        slope_field2 = VGroup(
            slope_field[125].copy(),
            slope_field[102].copy(),
            slope_field[12].copy(),
            slope_field[48].copy(),
        )

        # nestabilni_IK = VGroup()
        # nestabilni_IK.add(
        #     Line(
        #         start=ax.c2p(xmin,nestabilni[0]),
        #         end=ax.c2p(xmax,nestabilni[0]),
        #         ).set_color(RED)
        # )

        # stabilni_IK = VGroup()
        # stabilni_IK.add(
        #     Line(
        #         start=ax.c2p(xmin,stabilni[0]),
        #         end=ax.c2p(xmax,stabilni[0]),
        #         ).set_color(BLUE)
        # )

        axes = VGroup(ax)
        axes.add(MathTex("t").next_to(ax.get_x_axis()))
        axes.add(MathTex("x").next_to(ax.get_y_axis(),UP))
        slope_field2.shuffle_submobjects()

        rovnice = MathTex(r"\frac{\mathrm dx}{\mathrm dt}=\varphi(x,t)")
        rovnice.next_to(ax,UP).shift(DOWN*0.9)
        rovnice.set_z_index(10).add_background_rectangle(buff=0.5)
        axes.add(rovnice)

        self.add(axes)

        for i in slope_field2:
            svorky = VGroup()
            start = np.array(ax.p2c(i.get_start()))
            end = np.array(ax.p2c(i.get_end()))
            zmena = end-start
            smernice = zmena[1]/zmena[0]
            print("zmena"+str(zmena)+str(smernice))
            A = start
            B = A + np.array([1,0])
            C = start + np.array([1,zmena[1]/zmena[0]])
            print ("souradnice "+str(A)+str(B)+str(end))
            smer = Line(start=ax.c2p(A[0],A[1],0), end=ax.c2p(C[0],C[1],0))
            svorky.add(
                Brace(smer,np.sign(smernice)*DOWN, buff=0)
            )
            svorky.add(
                Brace(smer,RIGHT, buff=0)
            )
            svorky.add(MathTex("1").next_to(svorky[0],DOWN*np.sign(smernice),buff=0.2))
            smerniceR = round(smernice,3)
            svorky.add(MathTex(r"\varphi(x,t)="+str(smerniceR)).next_to(svorky[1],RIGHT))
            svorky.set_color(GRAY)
            bod = Dot(ax.c2p(A[0],A[1],0))
            self.play(FadeIn(bod))
            self.play(FadeIn(svorky))
            self.next_section()

            self.play(Create(smer),Uncreate(bod))
            self.play(FadeIn(i),FadeOut(svorky),Uncreate(smer))
            self.wait(0.2)
            self.next_section()

        #self.wait()
        self.play(AnimationGroup(
            *[FadeIn(i) for i in slope_field],
            ), run_time=1)
        self.wait()
        self.next_section()

        #return False
        krivky = plot_streams()#.shuffle_submobjects()
        
        self.play(*[Create(i) for i in krivky],run_time=1)            
        # self.add(nestabilni_IK)
        # self.add(stabilni_IK)

        self.wait()