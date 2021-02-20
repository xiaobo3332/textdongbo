from elements import *

wgw = 2  # waveguide width
tl = 195  # taper length
gwgw = 10  # width of the waveguide for the grating
gsl = 28  # grating socket length
gp = 1.1  # grating period

nl = 3  # number of loops
s = 10  # spacing
il = 0  # incoupling length

cc = {}
cl = {}

# rings
gap = (0.2, 0.25, 0.3, 0.35, 0.4, 0.45, 0.5, 0.55, 0.6, 0.65, 0.7, 0.75,
       0.8, 0.9, 1, 1.2)
wgl = 40

gdc = 0.6
angle = 20
lx = 31.29
ly = 2.855
radius = 15
spacing = 41.666
for i in range(len(gap)):
    # gap = 0.3 + i * 0.1
    r50 = ringcircuit3(radius, gap[i], wgw,
                       wgw, angle, lx, ly, tl, gwgw, gsl, gp, gdc)
    cc.update({'ring50_' + str(i): r50})
    cl.update({'ring50_' + str(i):
                   i3.Translation((1901, 4.6 + i * spacing))})
    lx = lx + 0.089
    ly = ly + 0

angle = 40
lx = 51.288
ly = 9.334
radius = 15
spacing = 41.666
for i in range(len(gap)):
    r20 = ringcircuit3(radius, gap[i], wgw,
                       wgw, angle, lx, ly, tl, gwgw, gsl, gp, gdc)
    cc.update({'ring20_' + str(i): r20})
    cl.update({'ring20_' + str(i):
                   i3.Translation((3401, 1504.6 + i * spacing))})
    lx = lx + 0.16075
    ly = ly + 0

gdc = 0.7
angle = 20
lx = 31.29
ly = 2.759
radius = 15
spacing = 41.666
for i in range(len(gap)):
    r50x = ringcircuit3(radius, gap[i], wgw,
                        wgw, angle, lx, ly, tl, gwgw, gsl, gp, gdc)
    cc.update({'ring50x_' + str(i): r50x})
    cl.update({'ring50x_' + str(i):
                   i3.Translation((3401, 4.6 + i * spacing))})
    lx = lx + 0.089
    ly = ly + 0

angle = 40
lx = 51.288
ly = 0
radius = 15
spacing = 41.666
for i in range(len(gap)):
    r20x = ringcircuit3(radius, gap[i], wgw,
                        wgw, angle, lx, ly, tl, gwgw, gsl, gp, gdc)
    cc.update({'ring20x_' + str(i): r20x})
    cl.update({'ring20x_' + str(i):
                   i3.Translation((3901, 1504.6 + i * spacing))})
    lx = lx + 0.16075
    ly = ly + 0

circuit = PlaceAndAutoRoute(child_cells=cc)
circuit_layout = circuit.Layout(child_transformations=cl)

# circuit_layout.visualize()
circuit_layout.write_gdsii("shg_2.gds")
