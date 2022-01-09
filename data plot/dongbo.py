import numpy as np
import matplotlib.pyplot as plt


data1 = np.loadtxt("displacement_mesa_4um_Ge_0.0um_0.55_0.74_0.80_1.0_50um_071021_1.txt", comments="#", delimiter=",", unpack=False)
data2 = np.loadtxt("displacement_mesa_4um_Ge_1.0um_0.55_0.74_0.80_1.0_50um_071021_1.txt", comments="#", delimiter=",", unpack=False)
data3 = np.loadtxt("displacement_mesa_4um_Ge_2.0um_0.55_0.74_0.80_1.0_50um_071021_1.txt", comments="#", delimiter=",", unpack=False)
data4 = np.loadtxt("displacement_mesa_4um_Ge_3.0um_0.55_0.74_0.80_1.0_50um_071021_1.txt", comments="#", delimiter=",", unpack=False)



plt.rcParams['font.size'] = '18'
plt.rcParams["figure.figsize"] = (12, 8)
#plt.rcParams["font.family"] = "Times New Roman"


x1 = data1[:, 0]*1e6
y1 = data1[:, 1]
x2 = data2[:, 0]*1e6
y2 = data2[:, 1]
x3 = data3[:, 0]*1e6
y3 = data3[:, 1]
x4 = data4[:, 0]*1e6
y4 = data4[:, 1]


plt.plot(x1, y1,linewidth=2,label='misalignment = 0um')
plt.plot(x2, y2,'--',linewidth=2,label='misalignment = 1um')
plt.plot(x3, y3,'*',linewidth=2,label='misalignment = 2um')
plt.plot(x4, y4,linewidth=2,label='misalignment = 3um')


plt.xlabel('Length of taper (um)')
plt.ylabel('Transmission (abs(T))')
plt.grid(True)
plt.xlim((0,1000))
plt.ylim((0.2,1.05))
plt.title('Impact of coupon misalignment_rib Ge')
plt.legend(loc='lower right')
plt.savefig('Impact of coupon misalignment_071021.png')
#plt.show()
plt.show()


