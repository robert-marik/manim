from typing_extensions import runtime
from manim import *
import colorsys
import random

from numpy import array
from common_definitions import *
import os
from scipy.integrate import solve_ivp  # řešení diferenciálních rovnic


a = 1.
b = 0.1
c = 1.5
d = 0.75*b
def dX_dt(X, t=0, a=a):
    """ Return the growth rate of fox and rabbit populations. """
    return np.array([ a*X[0] -   b*X[0]*X[1] ,
                  -c*X[1] + d*X[0]*X[1] ])

X_f0 = np.array([     0. ,  0.])
X_f1 = np.array([ c/(d), a/b])

tmin = 0
tmax = 16.6 # maximum for time on graph
ymax = 60 # maximum on y axis´for graphs in time
tnumber = 1000
max_step_IC = tmax/tnumber*2
t = np.linspace(tmin, tmax,  tnumber)              # time

curves = {}
curves_higher_a = {}
number_of_curves = 9
for i in range(1,number_of_curves):
    X0 = np.array([60+i/number_of_curves*(-60+c/(d)), a/b])
    curves[i] = solve_ivp(
        lambda t, X: dX_dt(X,t), 
        [tmin,tmax], [*X0], t_eval=t, max_step=max_step_IC 
    )

X = curves.pop(4)

print(X.y)