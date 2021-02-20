from elements import *

wgw = 3.8  # waveguide width
tl = 300  # taper length
gwgw = 10  # width of the waveguide for the grating
gsl = 78  # grating socket length
gp = 2.3  # grating period
gdc = 0.8  # grating duty cycle

s = 15.8 + 5  # spacing
il = 1000  # incoupling length

cc = {}
cl = {}

# spirals 2 um
i_s = (700, 1400)  # inner size (x, y)
nl = 8  # Number of loops in the spiral
s1 = spiralcircuit(wgw, nl, i_s, s, il, tl, gwgw, gsl, gp, gdc)
cc.update({'s1': s1})
cl.update({'s1': i3.Rotation(rotation_center=(2468, 255),
                             rotation=180, absolute_rotation=False) +
                 i3.Translation((1000, 200))})

s2 = spiralcircuit(wgw, nl, i_s, s, il, tl, gwgw, gsl, gp, gdc)
cc.update({'s2': s2})
cl.update({'s2': i3.Translation((0, 1280))})

# straight waveguides
wgw = 3
wgl = 4500
wg_spacing = 30
for i in range(17):
    wgw = 3 + i * 0.0625
    wg_A = FBMSwaveguidecircuit(wgl, wgw, tl, gwgw, gsl, gp, gdc)
    cc.update({'wg_A_' + str(i): wg_A})
    cl.update({'wg_A_' + str(i):
                   i3.Translation((0, 740 + i * wg_spacing))})
# for i in range(16):
# 	wgw = 1.8+i*0.025
# 	wg_B = FBMSwaveguidecircuit(wgl, wgw, tl, gwgw, gsl, gp, gdc)
# 	cc.update({'wg_B_'+str(i) : wg_B})
# 	cl.update({'wg_B_'+str(i) :
# 		   i3.Translation((700, 920+i*wg_spacing))})
# for i in range(16):
# 	wgw = 1.8+i*0.025
# 	wg_C = FBMSwaveguidecircuit(wgl, wgw, tl, gwgw, gsl, gp, gdc)
# 	cc.update({'wg_C_'+str(i) : wg_C})
# 	cl.update({'wg_C_'+str(i) :
# 		   i3.Translation((700, 1100+i*wg_spacing))})

circuit = PlaceAndAutoRoute(child_cells=cc)
circuit_layout = circuit.Layout(child_transformations=cl)


# circuit_layout.visualize()
circuit_layout.write_gdsii("shg_1.gds")
