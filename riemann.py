from manim import *
from manim_editor import PresentationSectionType

class UrcityIntegral(Scene):
    def construct(self):
        ax = Axes(
            x_range=[-0.1,2.4,10],
            y_range=[-0.5,6,100],
            tips = False,
            x_length=7.5,
            y_length=5.5
            ).to_corner(UR)

        funkce = [
            ax.plot(lambda x: 4, x_range = [0,2,0.1]),
            ax.plot(
                lambda x: np.piecewise(x,[x<1, x>=1],[2,6]),
                x_range = [0,2,0.01],
                use_smoothing=False, discontinuities=[1]              
            ),
            ax.plot(
                lambda x: np.piecewise(x,[x<0.5,x>=0.5, x>=1, x>=1.5],
                [2,3,5,6]),
                x_range = [0,2,0.01],
                use_smoothing=False, discontinuities=[0.5,1,1.5]              
            ),
            ax.plot(
                lambda x: 4-2*np.cos(x/2*3.14), 
                x_range = [0,2,0.01],
                use_smoothing=False              
            )
        ]
        for i in funkce:
            i.set_color(RED)

        # the rectangles are constructed from their top right corner.
        # passing an iterable to `color` produces a gradient
        rects=[None,None,None, None]
        rects[0] = ax.get_riemann_rectangles(
            funkce[0],
            x_range=[0, 2],
            dx=2,
            color=(TEAL, BLUE_B, DARK_BLUE),
            input_sample_type="left",
            stroke_width = 0
        ).set_z_index(-1)

        rects[1] = ax.get_riemann_rectangles(
            funkce[1],
            x_range=[0, 2],
            dx=1,
            color=(TEAL, BLUE_B, DARK_BLUE),
            input_sample_type="left",
            stroke_width = 0
        ).set_z_index(-1)

        rects[2] = ax.get_riemann_rectangles(
            funkce[2],
            x_range=[0, 2],
            dx=0.5,
            color=(TEAL, BLUE_B, DARK_BLUE),
            input_sample_type="left",
            stroke_width = 0
        ).set_z_index(-1)

        rects[3] = ax.get_riemann_rectangles(
            funkce[3],
            x_range=[0, 2],
            dx=0.5,
            color=(TEAL, BLUE_B, DARK_BLUE),
            input_sample_type="center",
            stroke_width = 0
        ).set_z_index(-1)

        def popisky(rects, vlabel = False):
            cislo = 1
            popisek = VGroup()
            for i in rects:
                popisek.add(MathTex("\Delta s_"+str(cislo)).move_to(i).set_color(YELLOW ))
                br = Brace(i,DOWN,buff=1)
                br.add(MathTex("\Delta t_"+str(cislo)).next_to(br,DOWN).set_color(YELLOW))
                popisek.add(br)
                if vlabel:
                    br = Brace(i,LEFT)
                    br.add(MathTex("v_"+str(cislo)).next_to(br,LEFT).set_color(YELLOW))
                    popisek.add(br)
                cislo = cislo + 1
            return(popisek)                

        vlabels = [False for i in rects]
        vlabels[1] = True
        labels = [popisky(i,v) for i,v in zip(rects,vlabels)]

        texty = VGroup(
            Tex(r"Konstrukce určitého integrálu (Riemannova)"),
            MathTex(r"s=vt"),
            MathTex(r"\Delta s=v \Delta t"),
            MathTex(r"\Delta s=v_1 \Delta t_1+v_2\Delta t_2"),
            MathTex(r"\Delta s=v_1 \Delta t_1+\cdots +v_4 \Delta t_4"),
            MathTex(r"\Delta s\approx\sum v_i \Delta t_i"),
            MathTex(r"\Delta s=\int_a^b v(t) \mathrm dt"),
        ).arrange(DOWN,aligned_edge=LEFT,buff=0.5).to_corner(UL)

        self.add(
            ax, 
            funkce[0], 
            rects[0],             
            texty[:2]
        )

        popisky = VGroup(
            MathTex("t").next_to(ax.c2p(2,0,0),DOWN),
            MathTex("v").next_to(ax.c2p(0,4,0),LEFT),
            MathTex("s").set_color(YELLOW).move_to(rects[0])
        )

        self.add(popisky)
        self.wait()
        self.next_section("")


        br = Brace(rects[0],DOWN,buff=1)
        br.add(MathTex("\Delta t").next_to(br,DOWN))
        br_ = Brace(rects[0],LEFT)
        br_.add(MathTex("v").next_to(br_,LEFT))
        popisky_n = VGroup(            
            MathTex("\Delta s").set_color(YELLOW).move_to(rects[0]),
            br,
            br_ 
        )

        popisky_ab = VGroup(            
            MathTex("a").next_to(ax.c2p(0,0,0),DOWN),
            MathTex("b").next_to(ax.c2p(2,0,0),DOWN),
            MathTex("t").next_to(ax.get_x_axis(),UP, aligned_edge = RIGHT),
        )

        final_int = MathTex(r"\Delta s = \int_a^b v(t)\mathrm dt").move_to(rects[0]).set_color(YELLOW).shift(0.5*DOWN)

        self.play(FadeOut(ax.get_y_axis(),popisky),FadeIn(popisky_n, popisky_ab, texty[2]))
        self.wait()

        self.next_section("")
        self.play(FadeOut(popisky_n))
        for i in range(3):
            self.play(
                #ReplacementTransform(rects[i],rects[i+1]),
                #ReplacementTransform(funkce[i],funkce[i+1]),
                #ReplacementTransform(labels[i],labels[i+1]),
                FadeOut(rects[i],funkce[i],labels[i]),
                FadeIn(rects[i+1],funkce[i+1],labels[i+1]),
                FadeIn(texty[3+i])
            )
            self.wait()
            self.next_section("")

        self.play(FadeOut(labels[-1]))

        distances = [0.5,0.4,0.3,0.2,0.1,0.05,0.001]
        rcts = [ax.get_riemann_rectangles(
            funkce[3],
            x_range=[0, 2],
            dx=i,
            color=(TEAL, BLUE_B, DARK_BLUE),
            input_sample_type="center",
            stroke_width = 0
        ).set_z_index(-1) for i in distances]


        self.play(ReplacementTransform(rects[-1],rcts[0]))
        for i in range(len(rcts)-1):
                self.play(ReplacementTransform(rcts[i],rcts[i+1]))
                self.wait(0.5)

        self.play(FadeIn(texty[-1]),FadeIn(final_int))                
        self.wait()            
        self.next_section("")

        self.play(FadeToColor(texty[1],YELLOW))
        self.wait()            
        self.play(ReplacementTransform(texty[1].copy(),texty[5]),FadeToColor(texty[5],YELLOW))
        self.wait()            
        self.play(
            ReplacementTransform(texty[5].copy(),texty[6]),FadeToColor(texty[6],YELLOW),
            ReplacementTransform(texty[5].copy(),final_int)
            )
        self.wait()            

