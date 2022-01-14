from manim import *
from common_definitions import *

class HeatTransfer(Scene):
    def construct(self):

        # th = thermometer(value = 50, )
        # self.add(th.dot, th.line, th.red_line, th.red_dot)
        # self.add(th)

        
        pocet = 5
        C = [100*2/n*(-1)**(n+1) for n in range(1,pocet+1)]
        C = [60,80,40]
        def teplota(x,t=0, C=C):
            temp = 0            
            for k,c in zip(range(len(C)),C):
                k = k+1
                temp += c*np.exp(-k*PI*t)*np.sin(k*PI*x)
            return -temp/PI + x*100
        
        ax2 = Axes(x_range=[0,1,2],y_range=[-1,1,2], y_length=1)
        ax3 = ax2.copy()
        ax4 = ax2.copy()

        n = 100
        nT = 11
        dxT = 0.1
        xmin, xmax = 0,1
        dx = (xmax-xmin)/n
        x_interval = np.linspace(xmin,xmax,n)
        def plot_rod(ax_,temperature, draw_thermometers=False):
            rod = VGroup()
            for i in x_interval:
                rod.add(Line(start = ax_.c2p(i,0,0),end=ax_.c2p(i+0.011,0,0), 
                color=temperature_to_color(temperature(i), min_temp=-50, max_temp=110)
                ))
            rod.set_stroke(width=20)
            for j in np.linspace(0,1,11):
                rod.add(Tex(round(temperature(j),1)).scale(.85).next_to(ax_.c2p(j,0,0),UP))    
            dTdx = np.gradient(np.array([temperature(i) for i in x_interval]))
            maximum = max(dTdx)
            minimum = min(dTdx)
            print(maximum, minimum)
            dTdx = dTdx/max(abs(maximum),abs(minimum))
            gradient = ax_.plot_line_graph(x_interval, -dTdx, add_vertex_dots=False)
            rod.add(gradient)
            #for j in np.linspace(0,1,11)[:-1]:
            #    rod.add(Tex(round(temperature(j+0.1)-temperature(j),1)).scale(.85).next_to(ax_.c2p(j+0.05,0,0),DOWN).set_color(BLUE))
            # if draw_thermometers:
            #     for j in np.linspace(0,1,11):
            #         rod.add((round(temperature(j),1)).scale(.85).next_to(ax_.c2p(j,0,0),UP))    

            return rod

        rod = plot_rod(ax2, lambda x:teplota(x,t=0,C=C))
        rod2 = plot_rod(ax3, lambda x:teplota(x,t=0.05,C=C))
        rod3 = plot_rod(ax4, lambda x:teplota(x,t=2,C=C))

        rod.set(alpha=0.5)
        rods = VGroup(rod,rod2, rod3)
        rods.arrange(DOWN).to_corner(UR)

        self.add(rod)
        
        ax = Axes(x_range = [0,1.05,1],y_range = [0,110,1000], x_length=4, y_length=2, tips=False)
        ax.to_corner(DL)
        self.add(ax)
        g1 = ax.plot(lambda x:teplota(x, C=C), x_range=[0,1,.01])
        g2 = ax.plot(lambda x:teplota(x, C=C, t=.1), x_range=[0,1,.01], color=RED)
        self.add(g1,g2)

        
        self.wait()


