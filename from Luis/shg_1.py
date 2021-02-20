from elements import *

wgw = 2		# waveguide width
tl = 200	# taper length
gwgw = 10	# width of the waveguide for the grating
gsl = 28	# grating socket length
gp = 1.1	# grating period
gdc = 0.6	# grating duty cycle

s = 10		# spacing
il = 2500	# incoupling length

cc = {}
cl = {}

# spirals 2 um
wgw = 2
i_s = (150, 210.001)	# inner size (x, y)
nl = 8
s1 = spiralcircuit(wgw, nl, i_s, s, il, tl, gwgw, gsl, gp, gdc)
cc.update({'s1' : s1})
cl.update({'s1' : i3.Rotation(rotation_center=(2468,255),
			      rotation=180, absolute_rotation=False)+
	   i3.Translation((1000, 200))})

s2 = spiralcircuit(wgw, nl, i_s, s, il, tl, gwgw, gsl, gp, gdc)
cc.update({'s2' : s2})
cl.update({'s2' : i3.Translation((-100, 1280))})

# straight waveguides
wgl = 4500
wg_spacing = 10
for i in range(16):
	wgw = 1.8+i*0.025
	wg_A = FBMSwaveguidecircuit(wgl, wgw, tl, gwgw, gsl, gp, gdc)
	cc.update({'wg_A_'+str(i) : wg_A})
	cl.update({'wg_A_'+str(i) :
		   i3.Translation((700, 740+i*wg_spacing))})
for i in range(16):
	wgw = 1.8+i*0.025
	wg_B = FBMSwaveguidecircuit(wgl, wgw, tl, gwgw, gsl, gp, gdc)
	cc.update({'wg_B_'+str(i) : wg_B})
	cl.update({'wg_B_'+str(i) :
		   i3.Translation((700, 920+i*wg_spacing))})
for i in range(16):
	wgw = 1.8+i*0.025
	wg_C = FBMSwaveguidecircuit(wgl, wgw, tl, gwgw, gsl, gp, gdc)
	cc.update({'wg_C_'+str(i) : wg_C})
	cl.update({'wg_C_'+str(i) :
		   i3.Translation((700, 1100+i*wg_spacing))})

circuit = PlaceAndAutoRoute(child_cells=cc)
circuit_layout = circuit.Layout(child_transformations=cl)

#circuit_layout.visualize()
circuit_layout.write_gdsii("shg_1.gds")