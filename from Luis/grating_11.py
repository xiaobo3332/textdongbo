from technologies import silicon_photonics
from ipkiss3 import all as i3
from picazzo3.traces.wire_wg import WireWaveguideTemplate
from picazzo3.fibcoup.uniform import UniformLineGrating

#Template garting waveguide

side1_r=3.        #cladd reel obtenue au Ebeam
side1=side1_r / 2
w_core1_r=10     #core reel obtenue au Ebeam
w_core_w1=w_core1_r+side1
w_clad_w1=2*side1+w_core_w1

wg_coupler = WireWaveguideTemplate()
wg_coupler.Layout(core_width=w_core_w1, cladding_width=w_clad_w1)

#Grating 1
socket_lentgh_def=50
periode=1.0
line_widthe=0.5*periode
FGC1 = UniformLineGrating(trace_template=wg_coupler)
FGC_layout1 = FGC1.Layout(period=periode,
                        line_width=line_widthe,
                        line_length=16.0,
                        n_o_periods=35,
                        origin=(0,0),
                        socket_length=socket_lentgh_def,)



from picazzo3.traces.wire_wg import WireWaveguideTransitionLinear

new_wg_template = WireWaveguideTemplate(name="my_wire_t1")
WG_T1 = wg_coupler
 
new_wg_template = WireWaveguideTemplate(name="my_wire_t2")

#cladding_width_def=3
#core_width_def=0.35


side2_r=3.        #cladd reel obtenue au Ebeam
side2=side2_r / 2
w_core2_r=0.35      #core reel obtenue au Ebeam
w_core_w2=w_core2_r+side2
w_clad_w2=2*side2+w_core_w2

WG_T2FBMS = new_wg_template.Layout(core_width=w_core_w2,cladding_width=w_clad_w2,)

my_taperG = WireWaveguideTransitionLinear(start_trace_template=WG_T1,
                                  end_trace_template=WG_T2FBMS)

field_Ebeamx=500
field_Ebeamy=25+0*50
wg_length=500 #real length is wg_length+100
overlap_wg=0

taper_length=200

my_taperG_lay = my_taperG.Layout(start_position=(0.0,0.0), end_position=(taper_length,0.0))

my_taperG_lay.visualize()

#FBMS waveguide

wg_left = i3.Waveguide(name="my_wire_t3",
                 trace_template=WG_T2FBMS)
layout = wg_left.Layout(shape=[(field_Ebeamx/2+taper_length+socket_lentgh_def, field_Ebeamy), (field_Ebeamx/2+taper_length+overlap_wg+socket_lentgh_def+wg_length/2, field_Ebeamy)])

wg_rigth = i3.Waveguide(name="my_wire_t4",
                 trace_template=WG_T2FBMS)
layout = wg_rigth.Layout(shape=[(-taper_length+field_Ebeamx/2+field_Ebeamx-overlap_wg+wg_length-socket_lentgh_def-wg_length/2, field_Ebeamy), (-taper_length+field_Ebeamx/2+field_Ebeamx+wg_length-socket_lentgh_def, field_Ebeamy)])


from picazzo3.routing.place_route import PlaceAndAutoRoute

my_circuit = PlaceAndAutoRoute(trace_template=WG_T1, child_cells={
                                            "grating1": FGC1,
                                            "taper_G_c1" : my_taperG,   
                                            "taper_G_c2" : my_taperG, 
                                            "grating2": FGC1,
                                            "my_wire_t3":wg_left,
                                            "my_wire_t4":wg_rigth,
                                            },
                                   )

my_circuit_layout1 = my_circuit.Layout(child_transformations={"grating1": i3.Translation((-socket_lentgh_def/2+field_Ebeamx/2+socket_lentgh_def, field_Ebeamy)),
                                                              "taper_G_c1": i3.Translation((field_Ebeamx/2+socket_lentgh_def, field_Ebeamy)), 
                                                              "taper_G_c2": i3.Rotation(rotation_center=(0.0,0.0), rotation=180.0, absolute_rotation=False)+i3.Translation((field_Ebeamx/2+field_Ebeamx+wg_length-socket_lentgh_def, field_Ebeamy)), 
                                                              "grating2": i3.Rotation(rotation_center=(0.0,0.0), rotation=180.0, absolute_rotation=False)+i3.Translation((socket_lentgh_def/2+field_Ebeamx/2+field_Ebeamx+wg_length-socket_lentgh_def, field_Ebeamy)),
                                                              })
                                                        
my_circuit_layout1.visualize()

my_circuit_layout1.write_gdsii("grating_11.gds")

