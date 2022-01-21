from manim import *
from scipy.interpolate import interp1d
from scipy.signal import argrelmin
from scipy.signal import argrelmax



class RollingBall(Scene):
    def construct(self):
        ball_radius=0.5

        xmin = -7 
        xmax = 7
        dx = 0.3
        a=4.6

        x = np.linspace(xmin,xmax,1000)
        y = 2.5  + np.cos(x/a*PI-PI/8)
        dy = np.gradient(y,x)

        mins = argrelmin(y)[0]
        maxs = argrelmax(y)[0]
        
        print(mins)
        print(maxs)
        st_points = [mins[0],maxs[0],mins[1]]
        x_s = [ x[:mins[0]+1], x[mins[0]:maxs[0]+1],  x[maxs[0]:mins[1]+1], x[mins[1]:] ]
        y_s = [ y[:mins[0]+1], y[mins[0]:maxs[0]+1],  y[maxs[0]:mins[1]+1], y[mins[1]:] ]
        
        radius = 0.2    
        zvetseni = 1
        ax = Axes(axis_config={'color':'BLUE'}).scale(zvetseni)
        func_graphs = [ ax.plot_line_graph(i,j,add_vertex_dots=False) for i,j in zip(x_s,y_s) ]
        full_curve = ax.plot_line_graph(x,y,add_vertex_dots=False)

        p=np.array([np.array([x_,y_])+radius*1.5/zvetseni*np.array([-dy_,1])/np.sqrt(1+dy_**2) for x_,y_,dy_ in zip (x,y,dy)])
        ball_graph = ax.plot_line_graph(p[:,0],p[:,1],add_vertex_dots=False)
        f1 = interp1d(p[:,0], p[:,1], kind='quadratic', fill_value='extrapolate', assume_sorted=True)

        pozice = ValueTracker(-0.2)
        ball=Dot(radius=radius).move_to(ax.c2p(pozice.get_value(),f1(pozice.get_value()),0))
        def posun():
            return ball.move_to(ax.c2p(pozice.get_value(),f1(pozice.get_value()),0))

        self.play(AnimationGroup(Create(full_curve), GrowFromCenter(ball), lag_ratio=1))
        kulicka = always_redraw(posun)
        self.add(kulicka)
        self.play(pozice.animate.set_value(x[mins[0]]), rate_func=rate_functions.linear)
        self.wait()
        self.play(FadeOut(kulicka))
        
        pozice.set_value(x[maxs[0]])
        posun()
        self.wait(0.1)
        self.play(FadeIn(kulicka))
        self.wait()  
        self.play(AnimationGroup(
            *[ApplyWave(i, ripples=4, amplitude=.02) for i in [full_curve]],
            lag_ratio=0)
        )
        self.play(pozice.animate.set_value(x[mins[1]]), rate_func=rate_functions.linear)
        self.wait()

        ball.generate_target()

        for dx in [0.5,-1,0.7,-0.3]:
            pozice.set_value(x[mins[1]]+dx)
            ball.target.move_to(ax.c2p(pozice.get_value(),f1(pozice.get_value()),0))
            self.play(AnimationGroup(
                *[ApplyWave(i, ripples=4, amplitude=.02) for i in [full_curve]],
                MoveToTarget(ball), 
                lag_ratio=0.5, rate_func=rate_functions.ease_out_bounce)
            )
            self.play(pozice.animate.set_value(x[mins[1]]), rate_func=rate_functions.linear)
        self.wait()

        # pozice.set_value(-2)  
        # self.play(pozice.animate.set_value(x[mins[0]]), rate_func=rate_functions.linear)


        colors = [BLUE,RED,BLUE,RED,BLUE]
        for i,j in zip(func_graphs,colors):
            self.play(FadeToColor(i,j))

     


        self.wait()

