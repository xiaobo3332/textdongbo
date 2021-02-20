# 1.  Importing the technology file.
from technologies import silicon_photonics
from ipkiss3 import all as i3


# 2. Import other python libraries.
import numpy as np
import pylab as plt

# 3. Creating the trace template
from picazzo3.traces.wire_wg import WireWaveguideTemplate
socket_lentgh_def=50 #related to grating_spiral code
side1_r=3.        #cladd reel obtenue au Ebeam
side1=side1_r / 2
w_core1_r=0.35      #core reel obtenue au Ebeam
w_core_w1=w_core1_r+side1
w_clad_w1=2*side1+w_core_w1
wg_length=500

new_wg_template = WireWaveguideTemplate(name="my_wire")
WG_IT19 = new_wg_template.Layout(core_width=w_core_w1 ,cladding_width=w_clad_w1,)

# 4. Define the spirals

#---------SPIRAL IT19---------#

from picazzo3.wg.spirals import DoubleSpiralWithInCouplingRounded

n_o_loop_param=1,
inner_size_param=572.93,
spacing_param=5,
incoupling_length_param=300,

print n_o_loop_param[0]
# print n_o_loop_param[1]

my_spiral= DoubleSpiralWithInCouplingRounded(n_o_loops=n_o_loop_param[0], trace_template=WG_IT19,)
my_spiral_layout = my_spiral.Layout(angle_step=0.1, inner_size=(inner_size_param[0],205.001),
                     incoupling_length=incoupling_length_param[0],
                     bend_radius=50.0,
                     manhattan=False,
                     spacing=spacing_param[0])

print my_spiral_layout.trace_length()
my_spiral_layout.visualize()


Spiral_width=incoupling_length_param[0]+2*(n_o_loop_param[0]+1)*spacing_param[0]+inner_size_param[0]

print Spiral_width


from picazzo3.routing.place_route import PlaceAndAutoRoute

my_circuit = PlaceAndAutoRoute(trace_template=WG_IT19, child_cells={
                                            "spiral_c1" : my_spiral,
                                           },
                                   )


field_Ebeamx=500
field_Ebeamy=25+25*50



taper_length=200

my_circuit_layout2 = my_circuit.Layout(bend_radius=50, child_transformations={"spiral_c1": (field_Ebeamx/2+taper_length+socket_lentgh_def+wg_length/2-Spiral_width/2-incoupling_length_param [0]/2, field_Ebeamy),
                                                              })

# my_circuit_layout2.visualize()

my_circuit_layout2.write_gdsii("spiral.gds")