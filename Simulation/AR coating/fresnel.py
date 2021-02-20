# -*- coding: utf-8 -*-
"""
Created on Mon Feb 18 16:27:14 2019

@author: evissers
"""

import numpy as np
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt
import scipy.fftpack as fftp

#pl.close('all')

class interface:
    def __init__(self, ni, nj):
        self.ni = ni
        self.nj = nj
        self.rij = (ni-nj)/(ni+nj)
        self.tij = 1+self.rij
        self.M = np.array([[1/self.tij, self.rij/self.tij],[self.rij/self.tij, 1/self.tij]], dtype=np.complex128)

class propagation: # distances in nm
    def __init__(self, n, d, WL, t=1):
        self.n = n
        self.d = d
        self.phi = ((2*np.pi*self.n*d)/WL)
        # print self.phi
        hierZeros = np.zeros_like(self.phi)
        self.M = np.array([[np.exp(1j*self.phi),hierZeros],[hierZeros,np.exp(-1j*self.phi)]], dtype=np.complex128)
        self.M = np.moveaxis(self.M, 2, 0)
        self.M[:,0,0] = self.M[:,0,0]/t
        self.M[:, 1, 1] = self.M[:, 1, 1]*t

class mirror:
    def __init__(self, R):
        self.rij = R
        self.tij = 1+self.rij
        self.M = np.array([[1/self.tij, self.rij/self.tij],[self.rij/self.tij, 1/self.tij]])

WLstart = 600 # nm
WLend = 1500 # nm

invcm_start = 1e-7/WLstart
invcm_end = 1e-7/WLend

#WL = np.linspace(WLstart, WLend, 50000)
invcm = np.linspace(invcm_end, invcm_start, 2**14)

WLs = 1e-7/invcm

# d1 = 100 # nm
# d2 = 100 # nm
# d3 = 1500 # nm
n_gain = 3.3347
n_sin = 1.724

class singleStack:
    def __init__(self, d1, d2, d3, t=1):
        a = interface(n_gain, 1.83698)
        b = propagation(1.83698, 10, WLs)
        c = interface(1.83698, 1.65887)
        d = propagation(1.65887, 15, WLs)
        e = interface(1.65887, 1.6637)
        f = propagation(1.6637, d1, WLs)
        g = interface(1.6637, 2.37166)
        h = propagation(2.37166, d2, WLs)
        i = interface(2.37166, 1)
        j = propagation(1, d3, WLs, t=0.707)
        k = interface(1, n_sin)

        matrices = [a, b, c, d, e, f, g, h, i, j, k]
        test = np.matmul(matrices[-2].M, matrices[-1].M)
        for M in reversed(matrices[:-2]):
            test = np.matmul(M.M, test)

        T_total = test

        self.r = (T_total[:,1,0]/(T_total[:,0,0]))
        self.t = (1/(T_total[:,0,0]))
        self.R = np.abs(self.r)**2
        self.T = (n_sin/n_gain)*np.abs(self.t)**2

    def get_T_R(self, WL):
        idx = np.abs(WLs - WL).argmin()
        T = self.T[idx]
        R = self.R[idx]
        return T, R

resx = 30
resy = 30

d1s = np.linspace(5, 100, resx)
d1bot = d1s[0] - 0.5*(d1s[1]-d1s[0])
d1top = d1s[-1] + 0.5*(d1s[1]-d1s[0])
print d1bot
print d1top
d2s = np.linspace(5, 100, resy)
d2bot = d2s[0] - 0.5*(d2s[1]-d2s[0])
d2top = d2s[-1] + 0.5*(d2s[1]-d2s[0])
print d2bot
print d2top

D1S, D2S = np.meshgrid(d1s, d2s)
D1S = np.reshape(D1S, -1)
D2S = np.reshape(D2S, -1)
stacks = []
Ts = []
Rs = []

i=1

for d1H, d2H in zip(D1S, D2S):
    #print d1H, d2H
    stacks.append(singleStack(d1H, d2H, 1500-d1H-d2H, t=0.707))
    T, R = stacks[-1].get_T_R(1100)
    Ts.append(T)
    Rs.append(R)
stacks, Ts, Rs = np.array(stacks), np.array(Ts), np.array(Rs)

D1S = D1S.reshape([resy, resx])
D2S = D2S.reshape([resy, resx])
stacks = stacks.reshape([resy, resx])
Ts = Ts.reshape([resy, resx])
Rs = Rs.reshape([resy, resx])

plt.figure()
plt.imshow(Ts, extent=[d1bot, d1top, d2bot, d2top], origin='lower')
plt.xlabel('d1 [nm]')
plt.ylabel('d2 [nm]')
plt.title('Transmission vs layer thickness')
plt.colorbar()

plt.figure()
plt.imshow(Rs, extent=[d1bot, d1top, d2bot, d2top], origin='lower')
plt.xlabel('d1 [nm]')
plt.ylabel('d2 [nm]')
plt.title('Reflection vs layer thickness')
plt.colorbar()

chosen_one = singleStack(92, 22, 1500-92-22, t=0.707)
plt.figure()
plt.plot(WLs, chosen_one.T, label='Transmission')
plt.plot(WLs, chosen_one.R, label='Reflection')
plt.xlabel('Wavelength [nm]')
plt.ylim([0, 1])
plt.title('1500 nm gap')
plt.legend()

chosen_one = singleStack(92, 22, 500-92-22, t=0.75)
plt.figure()
plt.plot(WLs, chosen_one.T, label='Transmission')
plt.plot(WLs, chosen_one.R, label='Reflection')
plt.xlabel('Wavelength [nm]')
plt.ylim([0, 1])
plt.title('500 nm gap')
plt.legend()



fig = plt.figure()
ax = fig.gca(projection='3d')
surf = ax.plot_surface(D1S, D2S, Ts, linewidth=0, antialiased=False)
plt.show()

# plt.figure()
# plt.plot(WLs, A.R, label="R 10")
# plt.plot(WLs, B.R, label="R 50")
# plt.plot(WLs, C.R, label="R 100")
# plt.plot(WLs, A.T, '.', label="T 10")
# plt.plot(WLs, B.T, '.', label="T 50")
# plt.plot(WLs, C.T, '.', label="T 100")
# plt.xlim([WLstart, WLend])
# plt.xlabel('Wavelength [nm]')
# plt.legend()
# plt.show()
#
# test = np.array([['11', '12'], ['21', '22']])
# print test[0, 0]
# print test[1, 0]
#
# print A.get_T_R(1100)



