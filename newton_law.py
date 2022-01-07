from manim import *
from scipy.integrate import solve_ivp  # řešení diferenciálních rovnic
import colorsys
import random
from common_definitions import *
import os

config.max_files_cached = 400
random.seed(10)

AnimationRuntime = 1.5
WaitTime = 2
obrazek = os.path.join('icons', 'mug')

def value2hex(value):
    """
    The function converts value from the interval from 0 to 1 into a color.
    The colors are from red to green and to blue.
    """
    temp = 0.99*(1-value-0.1)*0.75
    if temp<0:
        temp = 0
    if temp>0.99:
        temp = 0.99
    return rgb2hex(colorsys.hsv_to_rgb(temp, 0.99, 0.99))
    
class Intro(Scene):

    def construct(self):
        title = Title(r"Derivace, konečné diference a Newtonův zákon ochlazování")
        autor = VGroup(Tex("Robert Mařík"),Tex("Mendel University")).arrange(DOWN).next_to(title,DOWN)
        self.play(GrowFromCenter(title))
        self.play(GrowFromCenter(autor[0]))
        self.play(GrowFromCenter(autor[1]))
        self.wait(1)

        func = lambda pos: (-(pos[1]))  * UP + RIGHT
        stream_lines = StreamLines(func, stroke_width=3, max_anchors_per_line=30, 
            y_range=[-1,1.6,.5],
            x_range=[-3,3,1], 
            padding=1,
            opacity=1).shift(DOWN)

        self.add(stream_lines)
        stream_lines.start_animation(warm_up=True, flow_speed=1.5)
        self.wait(stream_lines.virtual_time / stream_lines.flow_speed*15)

        stream_lines.add_to_back()
        self.wait(4*WaitTime)
        self.remove(stream_lines)
        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        )

class Diference(MovingCameraScene):
    def construct(self):
        title = Title(r"Rychlost růstu a konečné diference").to_edge(UP)
        self.play(GrowFromCenter(title))        
        self.wait(.5)

        x = np.linspace(0,2,100) # husty definicni obor, pro spojitou funkci
        a = 3 # parametry pro funkci
        b = 7
        y = 1000-np.exp(-a*x + b) # "spojita" funkce, tj. s hustym definicnim oborem
        dy = np.gradient(y,x) # derivace spojite funkce

        X = x[::10] # diskretni definicni obor (ridky, obsahuje desetinu bodu v porovnani s hustym)
        Y = y[::10] # funkcni hodnoty diskretni funkce
        X = X[1:]
        Y = Y[1:]
        h = X[1]-X[0]

        
        derivace = dy[::10][4] # deriavace diskretni funkce
        # primka se smernici rovnou dopredne diferenci
        dopredna = (x-X[4])*(Y[5]-Y[4])/(X[5]-X[4])+Y[4]
        # primka se smernici rovnou zpetne diferenci
        zpetna = (x-X[4])*(Y[4]-Y[3])/(X[4]-X[3])+Y[4]
        # primka se smernici rovnou centralni diferenci
        centralni = (x-X[5])*(Y[5]-Y[3])/(X[5]-X[3])+Y[5]
        # primka se smernici danou derivaci, tj. tecna ke grafu
        tecna = (x-X[4])*derivace+Y[4]

        print ("min",np.min(x),np.min(y))
        print ("max",np.max(x),np.max(y))
        ax = Axes(y_range=[np.min(y),1.1*np.max(y),1e10], x_range=[np.min(x),np.max(x),1e10],y_length=5,tips=False)
        graf = ax.plot_line_graph(x,y,add_vertex_dots=False).set_color(BLUE)
        dots = VGroup(*[Dot().set_color(WHITE).move_to(ax.c2p(*bod)) for bod in zip(X,Y)])

        reddot = 2
        dots[reddot].set_color(RED)

        def primka(x):
            return((Y[-1]-Y[0])/(X[-1]-X[0])*(x-X[0])+Y[0])

        gr_primka = ax.plot(primka, color=BLUE)

        poloha = ValueTracker(1)
        self.add(poloha)

        slopes = always_redraw(lambda : ax.get_secant_slope_group(
            x=poloha.get_value(),
            graph=gr_primka,
            dx=.5,
            dx_label=Tex(r"$\Delta x = 1$"),
            dy_label=Tex(r"$k$"),
            dx_line_color=YELLOW,
            dy_line_color=RED,
            secant_line_length=4,
            secant_line_color=BLUE,
        ))

        popis = r"""
            \begin{minipage}{10cm}Směrnice (rychlost růstu) přímky je nárůst 
            na jednotkovou změnu nezávislé veličiny, 
            tj. v obrázku označeno jako $k$.\end{minipage}
            """
        komentar = Tex(popis).scale(.9).to_edge(DOWN).add_background_rectangle()

        for i in [ax,gr_primka]:
            self.play(FadeIn(i))
            
        self.wait(WaitTime)
        for i in [slopes,komentar]:
            self.play(FadeIn(i))

        self.wait(WaitTime)

        self.play(poloha.animate.set_value(0), run_time=5, rate_func=linear)
        self.play(poloha.animate.set_value(0.5), run_time=5, rate_func=linear)
        self.wait(3*WaitTime)


        delka_dx = ValueTracker(0.5)
        slopes2 = always_redraw(lambda : ax.get_secant_slope_group(
            x=poloha.get_value(),
            graph=gr_primka,
            dx=delka_dx.get_value(),
            dx_label=Tex(r"$\Delta x$"),
            dy_label=Tex(r"$\Delta y$"),
            dx_line_color=YELLOW,
            dy_line_color=RED,
            secant_line_length=4,
            secant_line_color=BLUE,
        ))

        komentar2 = Tex(r"\begin{minipage}{10cm}Obecněji a pro libovolnou vodorovnou odvěsnu je směrnice podílem svislé a vodorovné vzdálenosti, tj. zde \(\displaystyle\frac{\Delta y}{\Delta x}\).\end{minipage}").scale(.9).to_edge(DOWN).add_background_rectangle()

        self.add(delka_dx)
        self.play(AnimationGroup(FadeOut(slopes),FadeOut(komentar),FadeIn(slopes2),FadeIn(komentar2)))
        self.play(delka_dx.animate.set_value(1.5), run_time=5, rate_func=linear)
        self.play(delka_dx.animate.set_value(0.5), run_time=5, rate_func=linear)
        self.wait(4*WaitTime)
        self.remove(slopes2,delka_dx,komentar2,gr_primka)
        self.add(graf)
        self.wait(3*WaitTime)
        poloha = ValueTracker(1)
        tangent = always_redraw(lambda:
            ax.plot(lambda x: a*np.exp(-a*(poloha.get_value())+b)*(x-poloha.get_value())+1000-np.exp(-a*(poloha.get_value()) + b),
                x_range = [poloha.get_value()-2*h, poloha.get_value()+2*h, h/10]).set_color(ORANGE)
        )

        popis = r"rychlost růstu je derivace $\displaystyle\frac{\mathrm dy}{\mathrm dx}$"
        komentar = Tex(popis).move_to(ax,aligned_edge=DR).add_background_rectangle()
        self.play(AnimationGroup(FadeIn(tangent),FadeIn(komentar),lag_ratio=1), run_time=2)
        self.wait(6*WaitTime)
        self.play(poloha.animate.set_value(2), run_time=1, rate_func=linear)
        self.play(poloha.animate.set_value(0), run_time=3, rate_func=linear)
        self.play(poloha.animate.set_value(1), run_time=2, rate_func=linear)
        self.play(poloha.animate.set_value(X[reddot]), run_time=2, rate_func=linear)

    ########################################################################
    #######################################
        self.play(FadeIn(dots[2]))
        self.wait(5*WaitTime)

        dopredna = ax.plot(lambda x:(Y[reddot+1]-Y[reddot])/(X[reddot+1]-X[reddot])*(x-X[reddot])+Y[reddot], 
            x_range=[X[reddot]-2*h,X[reddot]+2*h,h/10]).set_color(GREEN)
        zpetna = ax.plot(lambda x:(Y[reddot-1]-Y[reddot])/(X[reddot-1]-X[reddot])*(x-X[reddot])+Y[reddot], 
            x_range=[X[reddot]-2*h,X[reddot]+2*h,h/10]).set_color(WHITE)
        centralni = ax.plot(lambda x:(Y[reddot-1]-Y[reddot+1])/(X[reddot-1]-X[reddot+1])*(x-X[reddot-1])+Y[reddot-1], 
            x_range=[X[reddot]-2*h,X[reddot]+2*h,h/10]).set_color(PINK)

        self.play(AnimationGroup(*[FadeIn(_) for _ in dots], lag_ratio=.6, run_time=5))
        self.wait(WaitTime)

        distanc_1 = VGroup(*[DoubleArrow(start=ax.c2p(X[_],0,0),end=ax.c2p(X[_+1],0,0),buff=0,color=YELLOW,tip_length=0.2).shift(0.2*UP) for _ in range(len(dots)-1)])
        distanc_2 = VGroup(*[Tex(r"$h$").set_color(YELLOW).next_to(_,UP) for _ in distanc_1])
        distanc_all = VGroup(*[VGroup(_,__) for _,__ in zip(distanc_1,distanc_2)])
        distanc = VGroup(distanc_all[1],distanc_all[2])

        vlines_all = VGroup(*[ax.get_vertical_line(ax.coords_to_point(*point), line_config={"dashed_ratio": 0.5, "dash_length":.1}) for point in zip(X,Y)])
        vlines = VGroup(*[vlines_all[_] for _ in [reddot-1,reddot,reddot+1]])

        hlines = VGroup(*[ax.get_horizontal_line(ax.coords_to_point(*point), line_config={"dashed_ratio": 0.5, "dash_length":.1}) for point in zip(X[reddot-1:reddot+2],Y[reddot-1:reddot+2])])

        vlines_labels=VGroup()
        for co,kde in zip(["-h","","+h"],vlines):
            vlines_labels.add(Tex(r"$x"+co+"$").scale(0.7).next_to(kde,DOWN))

        hlines_labels=VGroup()
        for co,kde in zip(["-h","","+h"],hlines):
            hlines_labels.add(Tex(r"$f(x"+co+")$").scale(0.7).next_to(kde,LEFT))

        self.play(AnimationGroup(*[Create(_) for _ in vlines_all],*[Create(_) for _ in distanc_all], lag_ratio=0.2))
        self.add(dots)
        self.wait(WaitTime)
        self.play(AnimationGroup(*[FadeOut(_) for _ in distanc_all],*[FadeOut(_) for _ in vlines_all], lag_ratio=0.2))
        

        self.play(FadeOut(komentar))
        self.wait(5*WaitTime)
        def cycle_lines(delka=4):
            self.play(AnimationGroup(
                FadeIn(tangent),                
            ))
            self.wait(delka)
            self.play(AnimationGroup(
                FadeOut(tangent),                
                FadeIn(dopredna)
            ))
            self.wait(delka)
            self.play(AnimationGroup(
                FadeOut(dopredna),
                FadeIn(zpetna)
            ))
            self.wait(delka)
            self.play(AnimationGroup(
                FadeOut(zpetna),
                FadeIn(centralni)
            ))
            self.wait(delka)
            self.play(FadeOut(centralni))

        cycle_lines()
        detail=VGroup(dots[reddot],dots[reddot-1],dots[reddot+1])

        # Moving camera from https://www.youtube.com/watch?v=QTlZp8tiql4
        self.camera.frame.save_state()
        self.play(self.camera.frame.animate.set(width=detail.width*2).move_to(detail))
        self.wait(3*WaitTime)
        cycle_lines(3)
        self.wait(WaitTime)
        self.play(Restore(self.camera.frame))

        self.wait(WaitTime)

        vsechno = VGroup(ax,graf,*dots,tangent)
        vsechno.generate_target()
        vsechno.target.shift(RIGHT*7)
        self.play(MoveToTarget(vsechno))
        VGroup(distanc,vlines,hlines,hlines_labels,vlines_labels).shift(RIGHT*7)

        dopredna = ax.plot(lambda x:(Y[reddot+1]-Y[reddot])/(X[reddot+1]-X[reddot])*(x-X[reddot])+Y[reddot], 
            x_range=[X[reddot]-2*h,X[reddot]+2*h,h/10]).set_color(GREEN)
        zpetna = ax.plot(lambda x:(Y[reddot-1]-Y[reddot])/(X[reddot-1]-X[reddot])*(x-X[reddot])+Y[reddot], 
            x_range=[X[reddot]-2*h,X[reddot]+2*h,h/10]).set_color(WHITE)
        centralni = ax.plot(lambda x:(Y[reddot-1]-Y[reddot+1])/(X[reddot-1]-X[reddot+1])*(x-X[reddot-1])+Y[reddot-1], 
            x_range=[X[reddot]-2*h,X[reddot]+2*h,h/10]).set_color(PINK)

        self.wait(3*WaitTime)

        temp = DoubleArrow(start = ax.c2p(X[reddot-1],0,0), end = ax.c2p(X[reddot+1],0,0), color=YELLOW, buff=0, tip_length=0.2).shift(1.5*UP)
        distanc.add(VGroup(temp,Tex(r"$2h$").set_color(YELLOW).next_to(temp,UP)))

        i = reddot
        vdistanc = VGroup(
            *[DoubleArrow(start = ax.c2p(0,Y[_],0,0), end = ax.c2p(0,Y[__],0,0), color=YELLOW, buff=0, tip_length=0.2).shift(RIGHT) for _,__ in [[i,i+1],[i,i-1],[i-1,i+1]] ]
        )

        self.add(hlines,hlines_labels,vlines,vlines_labels,dots)

        diference = VGroup(
            Tex(r"$\bullet$ Dopředná"),
            Tex(r"$\displaystyle \frac{f(x+h)-f(x)}{h}$"),
            Tex(r"$\bullet$ Zpětná"),
            Tex(r"$\displaystyle \frac{f(x)-f(x-h)}{h}$"),
            Tex(r"$\bullet$ Centrální"),
            Tex(r"$\displaystyle \frac{f(x+h)-f(x-h)}{2h}$")
        ).scale(0.8).arrange(DOWN,aligned_edge=LEFT).next_to(title,DOWN).to_edge(LEFT, buff=1)
        for i in [1,3,5]:
            diference[i].shift(RIGHT)

        def predstav(jmeno,vzorec,hd,vd,primka):
            self.play(AnimationGroup(FadeIn(jmeno),FadeIn(primka),FadeIn(vd),FadeIn(hd),FadeIn(vzorec),ApplyWave(vzorec),lag_ratio=0.5), run_time=5)
            self.wait(5*WaitTime)
            self.play(AnimationGroup(*[FadeOut(_) for _ in [primka,vd,hd]], lag_ratio=.5))

        self.wait(8*WaitTime)
        predstav(diference[0],diference[1],distanc[1],vdistanc[0],dopredna)
        predstav(diference[2],diference[3],distanc[0],vdistanc[1],zpetna)
        predstav(diference[4],diference[5],distanc[2],vdistanc[2],centralni)
        # self.wait(WaitTime)        

        self.wait(25*WaitTime)
        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        )

class Odvozeni(Scene):

    def construct(self):

        title = Title(r"Newtonův zákon ochlazování").to_edge(UP)

        definice = VGroup(
            Tex(r"$\bullet$\quad  Teplotu označíme ",r"$T$",". ",r"Teplota okolí je ",r"$T_0$","."),
            Tex(r"$\bullet$\quad Rychlost ochlazování je úměrná\\rozdílu teploty tělesa a okolí."),
            Tex(r"Rychlost poklesu teploty"," je úměrná"," rozdílu teplot.").set_color(YELLOW)
            )

        definice.arrange(DOWN, aligned_edge = LEFT, buff=0.3).next_to(title,DOWN,aligned_edge=LEFT, buff=0.3)
        rovnice = definice[-1].shift(.5*DOWN)
        rovnice_clean = MathTex(r"-\frac{\mathrm dT}{\mathrm dt}","=k",r"(T-T_0)").move_to(rovnice)
        rovnice_final = MathTex(r"\frac{\mathrm dT}{\mathrm dt}=-k(T-T_0)").next_to(rovnice,DOWN,buff=1)

        mug= ImageMobject(obrazek).scale_to_fit_width(3).set_color(RED).to_corner(DR)

        self.play(GrowFromCenter(title)) 
        self.play(FadeIn(mug))
        self.wait(6*WaitTime)

        for i in definice:
            self.play(FadeIn(i))
            self.wait(3*WaitTime)

        # rovnice.set_color(YELLOW)
        a1 = Tex(r"$\displaystyle-\frac{\mathrm dT}{\mathrm dt}$").move_to(rovnice[0])
        a2 = Tex(r"$(T-T_0)$").move_to(rovnice[2])
        a3 = Tex(r"${}=k$").move_to(rovnice[1])
        
        for i in [
             ReplacementTransform(VGroup(definice[0][1].copy(),rovnice[0]),a1),
             ReplacementTransform(VGroup(definice[0][1].copy(),definice[0][4].copy(),rovnice[2]),a2),
             ReplacementTransform(VGroup(rovnice[1]),a3),
             AnimationGroup(*[ReplacementTransform(_,__) for _,__ in zip([a1,a3,a2],rovnice_clean)],lag_ratio=0.5),
             TransformMatchingShapes(rovnice_clean.copy(),rovnice_final)
        ]:
            self.play(i, run_time = 3) 
            self.wait(2*WaitTime)

        self.wait(6*WaitTime)

        self.play(*[FadeOut(_) for _ in [title,rovnice_clean,definice]])

        title = Title(r"Transformace pro numerický model").to_edge(UP)
        self.play(FadeIn(title))
        self.wait(4*WaitTime)

        odvozeni = VGroup(
            MathTex(r"\displaystyle \frac {\mathrm dT}{\mathrm dt}=-k(T-T_0)"),
            MathTex(r"{T(t+h)-T(t) \over h}",r"{}=-k(T(t)-T_0)"),
            MathTex(r"T(t+h)-T(t)=-k(T(t)-T_0)h"),
            MathTex(r"T(t+h)","{}={}","T(t)","{}-{}","k(T(t)-T_0)h")
        ).arrange(DOWN).next_to(title,DOWN)

        self.play(ReplacementTransform(rovnice_final,odvozeni[0]))
        for i in [0,1,2]:
            self.play(TransformMatchingShapes(odvozeni[i].copy(),odvozeni[i+1]))
            if i==0:
                b = Brace(odvozeni[1][0], direction=DOWN, color=YELLOW)
                t = Tex(r"dopředná diference\\s krokem $h$").next_to(b,DOWN)
                self.play(GrowFromCenter(VGroup(b,t)))
                self.wait(3*WaitTime)
                self.play(FadeOut(VGroup(b,t)))
            self.wait(2*WaitTime)

        self.wait(3*WaitTime)
        r = VGroup(*[odvozeni[-1][_] for _ in [0,2,4]])
        b = VGroup(*[Brace(_, direction=DOWN, color=YELLOW) for _ in r])
        t = VGroup(Tex(r"teplota\\za okamžik $h$\\od současnosti"),Tex(r"současná\\teplota"),Tex(r"snížení teploty\\za čas $h$"))
        cs = [RED,BLUE,ORANGE]
        for _ in [1,2,0]:
            t[_].next_to(b[_],DOWN).scale(0.7).shift(0.3*UP).set_color(cs[_])
            self.play(GrowFromCenter(VGroup(t[_],b[_])),FadeToColor(r[_], color=cs[_]))
            self.wait(2*WaitTime)

        self.wait(6*WaitTime)
        self.play(
            *[FadeOut(mob)for mob in self.mobjects]
        )

class Simulace(Scene):

    def construct(self):

        tmin = 0
        tmax = 10
        ymin = 0
        ymax = 110
        T0=20
        r=0.5
        t = np.linspace(tmin,tmax,200)
        IC = 100
        max_step_IC = 0.1
        solIC = solve_ivp(lambda t, T: -r*(T-T0), [tmin,tmax], [IC], t_eval=t, max_step=max_step_IC )
        s = solIC
        x = s.t
        y = s.y[0]

        x=np.insert(x,0,x[0])
        y=np.insert(y,0,y[0])

        title = Title(r"Numerická simulace")
        self.play(GrowFromCenter(title))        

        poloha = ValueTracker(1)
        print(y[0])
        mug = always_redraw(lambda:ImageMobject(obrazek).set_color(value2hex(y[int(np.round(poloha.get_value()))]/IC)).scale_to_fit_width(3).to_corner(DR))
        
        self.play(FadeIn(mug))

        text_teplota = MathTex("T={}").scale(.7).move_to(mug).shift(.7*LEFT).set_color(BLACK)
        text_cas = MathTex("t={}").scale(.7).move_to(mug).shift(.7*LEFT).shift(.6*DOWN).set_color(BLACK)
        self.add(text_teplota, text_cas)

        value_teplota = always_redraw(
            lambda: DecimalNumber(num_decimal_places=1)
            .set_value(y[int(np.round(poloha.get_value()))]).scale(.7).set_color(BLACK)
            .next_to(text_teplota, RIGHT, buff=0.05)
        )
        value_cas = always_redraw(
            lambda: DecimalNumber(num_decimal_places=1)
            .set_value(x[int(np.round(poloha.get_value()))]).scale(0.7).set_color(BLACK)
            .next_to(text_cas, RIGHT, buff=0.05)
        )

        self.add(value_teplota,value_cas)


        self.wait(WaitTime)
        def cTex(text):
            return Tex(r"\texttt{"+text+"}")
        model = VGroup(
            MathTex(r"\frac{\mathrm dT}{\mathrm dt}=-k(T-T_0)"),
            MathTex(r"T(t+h)","{}={}","T(t)","{}-{}","k(T(t)-T_0)h"),
        ).arrange(DOWN, aligned_edge=LEFT).next_to(title,DOWN).to_edge(LEFT)

        simulace = VGroup(
            cTex(r"nastav T=100,t=0,h,T0,k"),
            cTex(r"opakuj v cyklu:"),
            cTex(r"vypočítej změnu teploty: dT=h*k*(T-T0)"),
            cTex(r"posuň čas: t=t+h"),
            cTex(r"oprav teplotu: T=T+dT"),
            cTex(r"ulož T,t"),
            cTex(r"zpracuj T,t")
        ).scale(0.8).arrange(DOWN,aligned_edge=LEFT).next_to(model,DOWN).set_color(YELLOW).shift(2*RIGHT)

        for i in simulace[2:-1]:
            i.shift(RIGHT)


        self.play(AnimationGroup(
            *[FadeIn(_) for _ in model],lag_ratio=1
            ))

        self.wait(WaitTime)
        
        self.play(AnimationGroup(
            *[FadeIn(_) for _ in simulace], lag_ratio=.2
            ),run_time=3)

        self.play(FadeToColor(simulace[0],RED))
        self.wait(5*WaitTime)

        curr = 0
        prev = 3
        for i in range(100):
            runtime = 2
            if i>6:
                runtime = 0.5
            if i>10:
                runtime = 0.2
            if i>20:
                runtime = 0.05
            if i==99:
                curr = 6                        
            self.play(AnimationGroup(FadeToColor(simulace[curr],RED),FadeToColor(simulace[prev],YELLOW),run_time=runtime))
            prev = curr
            curr = curr+1
            if curr == 6:
                curr = 2

        self.wait(WaitTime)

        self.play(simulace.animate.scale(0.7).next_to(title,DOWN).to_edge(RIGHT))
        self.wait(WaitTime)


        ax = Axes(                    
            x_range=[tmin, tmax, 1000],
            y_range=[ymin, ymax, 1000],                    
            tips=False,
            y_length=5,                    
            axis_config={"include_numbers": False},
            ).scale(0.75)
        
        text = Tex(r"Časový vývoj").scale(0.8)
        axt = VGroup(text,ax)
        labels = VGroup(MathTex(r"t"),MathTex(r"T"))
        axt[1].move_to(axt[0], aligned_edge=UP)
        axt[0].move_to(axt[1])
        axt.to_corner(DL, buff=0.5).shift(0.5*RIGHT)
        
        labels = ax.get_axis_labels(
            MathTex("t").scale(0.7), MathTex("T").scale(0.7)
        )
        self.add(axt,labels)

        skala = VGroup()
        for i in range(1,98):
            skala.add(ax.plot_line_graph([-.1,-.1],[i-1,i+2],add_vertex_dots=False,stroke_width=10).set_color(value2hex(i/100)))
        self.add(skala)

        sp = ax.plot_line_graph([tmin,tmax],[T0,T0],add_vertex_dots=False).set_color(WHITE)
        spt = MathTex(r"T_0").scale(0.7).next_to(sp,LEFT)

        self.add(sp,spt)
        self.wait(WaitTime)

        sol = always_redraw(lambda : ax.plot_line_graph(x[:int(poloha.get_value())],y[:int(poloha.get_value())],
                    add_vertex_dots=False).set_color(YELLOW))
        self.add(sol)

        analog = always_redraw(
            lambda : VGroup(
                analog_indicator(y[int(np.round(poloha.get_value()))],
                    value_max=100,
                    values=[25*i for i in range(5)], 
                    label_min="0", 
                    label_max="100", 
                    title=r"$T/{}^\circ\mathrm C$")
        ).to_edge(RIGHT))
        self.add(analog)

        stop_index = np.argwhere(np.array(y)<51)[0][0]
        self.play(poloha.animate.set_value(stop_index), run_time=10, rate_func=linear)

        self.wait(5*WaitTime)        
        self.play(poloha.animate.set_value(len(x)-1), run_time=10, rate_func=linear)

        self.wait(10*WaitTime)

        axRIGHT,axUP,_ = ax.c2p(1,1) - ax.c2p(0,0)
        scaling = 1
        func = lambda pos: -r*(ax.p2c(pos)[1]-T0)*axUP*UP*scaling + axRIGHT*RIGHT*scaling
        stream_lines = StreamLines(func, stroke_width=2, max_anchors_per_line=10, 
            y_range=[ax.c2p(0,0)[1],ax.c2p(0,110)[1],.5],
            x_range=[ax.c2p(0,0)[0],ax.c2p(10,0)[0],1], 
            padding=.1,
            opacity=.7
            )

        self.add(stream_lines)
        self.wait(2*WaitTime)
        stream_lines.start_animation(warm_up=True, flow_speed=1.5)
        self.wait(4*WaitTime)
        stream_lines.end_animation()
        self.wait(5*WaitTime)

komentar = """ 

Dobrý den, v tomto videu si ukážeme metody, díky kterým matematika dokáže
pracovat s rychlostí změn funkcí. To je velmi užitečná dovednost, protože nám
zpřístupňuje možnost modelovat přírodní zákony. Díky tomu můžeme provádět
experimenty na počítači a předpovídat budoucí vývoj studovaných systémů. Jako
příklad budeme modelovat ochlazování hrnku s kávou.

====================================

Rychlost růstu je nejsnazší zavést pro lineární funkce. Stačí uvažovat
trojúhelník jako na obrázku s vodorovnou odvěsnou jednotkové délky. Svislá
odvěsna v takovém trojúhelníku je mírou rychlosti růstu a nazývá se směrnice.
Není to nic neobvyklého. V běžném životě takto definujeme stoupání, například u
silnice. Jasně vidíme, že nezáleží na konkrétní poloze nakresleného
trojúhleníka.

Pokud nechceme pracovat s odvěsnou jednotkové délky, můžeme pracovat s
trojúhelníkem libovolných rozměrů a směrnici najít podílem svislé a vodorovné
vzdálenosti bodů.

Pro nelineární funkce je situace komplikovanější. Aby bylo vůbec mozné rychlost
růstu zavést, musíme pracovat s lineární aproximací, tedy s tečnou ke grafu.
Místo směrnice máme derivaci. Aproximace tečnou je však jenom lokální. Podél
křivky se tečna naklání a v různých bodech funkce roste různou rychlostí.

Zajímejme se o rychlost růstu v bodě vyznačeném na obrázku. Při numerických
simulacích bohužel nemáme k dispozici celou křivku, jako na obrázku, ale jenom
funkční hodnoty v určitých bodech. Ideálně v bodech rovnoměrně rozmístěných
podél osy x. Na obrázku to je se vzdáleností bodů trošku přehnané, ale
představme si, že rychlost růstu v oranžovém bodě musíme zjistit jenom z teček
na grafu.

První možností je použít k získání informace o rychlosti růstu nejbliží tečku
vpravo. Takto definovaná rychlost růstu se nazývá dopředná diference. 

Další možností, je použít tečku vlevo a zpětnou diferenci. 

Ještě je možnost použít obě sousední tečky a toto vede na centrální diferenci.

Ještě jednou se podívejme na detail. Nejprve tečna. Ta přesně zachycuje směr
růstu a její směrnici bychom rádi zjistili z teček na grafu. Dopředná diference
použije následovníka, zpětná diference použije předchůdce a centrální diference
použije oba, následovníka i předchůdce.

Pro numerickou simulaci musíme geometrickou představu transformovat do přesných
vzorců. Funkci si označme f, bod našeho zájmu x, krok mezi body na grafu h.
Sousedé bodu x budou tedy x+h a x-h.

Dopředná diference používá funkční hodnoty v bodech x a x+h. Vodorovná
vzdálenost bodů na grafu je h a svislá vzdálenost je rozdíl funkčních hodnot.
To nám za použití podílu dává vzorec pro dopřednou diferenci.

Zpětná diference používá funkční hodnoty v bodech x a x-h. Vodorovná vzdálenost
je opět h a svislá opět rozdíl funkčních hodnot. Tím máme vzorec pro zpětnou
diferenci.

Centrální diference používá funkční hodnoty v bodech x+h a x-h. Vodorovná
vzdálenost bodů je 2h a svislá opět rozdíl funkčních hodnot.

Máme tedy vzorce pro všechny tři diference a k tomu derivaci. Kdy kterou
použít? Při formulaci přírodních zákonů použijeme derivaci, protože takto
příroda a svět okolo nás fungují. Pro simulaci vývoje v čase dopředu použijeme
dopřednou diferenci. To si za chviličku ukážeme.

=========================================================

Budeme modelovat časový vývoj teploty hrnku s kávou. Na začátku je hrnek horký a
z fyziky, z Newtonova zákona tepelné výměny, víme, že rychlost poklesu teploty
je dána teplotním rozdílem kávy a okolí. Přesněji, obě veličiny jsou úměrné.
Pro převedení tohoto přírodního zákona do podoby umožňující numerickou simulaci
si označíme potřebné veličiny. Dále si ujasníme vztah mezi rychlostí změny
teploty a parametry systému. Tento vztah je nutné matematizovat. Rychlost
poklesu teploty je záporně vzatá rychlost růstu a tedy záporně vzatá derivace
teploty podle času. Rozdíl teplot zapíšeme snadno, prostým odečtením potřebných
veličin. Úměrnost je slovní obrat pro násobení konstantnou. Pro pohodlí ještě
osamostatnníme derivaci převedením znaménka minus na opačnou stranu. Tím
dostaneme matematický model uvažovaného děje. Tento model je dále nutné převést
do podoby pro numerickou simulaci.

Derivaci nahradíme dopřednou diferencí s krokem délky h. V získaném vztahu
vyjádříme teplotu v časovém okamžiku t+h pomocí teploty v časovém okamžiku t,
pomocí kroku h numerické aproximace a pomocí parametrů systému jako jsou
konstanta úměrnosti k a teplota okolí T0.

Výsledkem je vzorec, který udává, jak se teplota v čase t dá použít pro
nalezení teploty v čase t+h. V matematice se tento postup nazývá Eulerova
metoda a je to základní metoda řešení diferneciálních rovnic. Ačkoliv se v
praxi reálných inženýrských aplikací používají vyspělejší metody, za chvíli
uvidíme, že i jednoduchá Eulerova metoda je pro numerickou simulaci použitelná.

==============================================================

Máme tedy matematický model ochlazování ve formě rovnice s derivací. Dále máme
numerické schema pro simulaci. Toto schema je snadné implementovat v libovolném
programu na numerické výpočty nebo i v tabulkovém procesoru. V pseudokódu na
obrazovce vidíme, že nejprve je nutné nastavit hodnoty parametrů a počáteční
stav. Simulaci zahájíme v čase nula a počáteční teplota je sto stupňů. Teplota
okolí T0 a konstanta k jsou parametry systému a zjistíme je například měřením.
Volba kroku h je v naší moci, souvisí s přesností simulace a s délkou výpočtu.
Začátečníci ji mohou zvolit nějak rozumně a vyzkoušet, jestli změna kroku má
vliv na chování simulace.

Po nastavení parametrů v cyklu vypočítáme změnu teploty, posuneme čas, opravíme
teplotu a uložíme data. Výpočetní výkon stačí malý a není problém nechat cyklus
proběhnout kolikát je potřeba. Konec cyklu plánujeme nejčastěji při dosažení
cílové hodnoty teploty nebo času. Například pokud nám káva chutná nejvíce při
padesáti stupních, bude toto hodnota pro zastavení výpočtu. Vizalizaci je možné
provést dle potřeby například grafem teploty jako funkce času, výpisem hodnot
nebo jednodušeji zelenou barvou ikony hrníčku signalizující zelenou ke
konzumaci. Naše simlace byla provedena pro čas od nuly do deseti a proto je
možné pokračovat ve vizualizaci.

S využitím hrubé výpočetní síly není těžké nasimulovat průběh pro celou řadu
výchozích teplot a máme tak chování kávy v hrníčku při různých výchozích
teplotách. Rovnice funguje dokonce i pro teploty menší než je teplota T0 a
umožňuje simulovat postupné ohřívání ledové kávy.

Ve videu jsme si ukázali, jak měříme rychlost změny funkcí, jak tuto rychlost
můžeme využít při matematické formulaci přírodního děje, jak tuto matematickou
formulaci můžeme upravit do formy vhodné pro numerické simulace a jak se
takové numerické simulace dají realizovat.

"""