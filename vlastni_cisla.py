import numpy as np

a11,a12,a21,a22=1,0.2,0.2,1
# a11,a12,a21,a22=1.2,0,0,1.2
# a11,a12,a21,a22=1,0.3,-0.3,1
matice = np.array([[a11,a12],[a21,a22]])

vv = np.linalg.eig(matice)
print(vv[1].T[1])
print(np.pi + np.arctan(-1))
uhly = [0,180]

for i in range(len(uhly)-1):
    print (i)