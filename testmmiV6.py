from technologies import silicon_photonics
from picazzo3.filters.mmi.cell import MMI1x2Tapered
from picazzo3.filters.mmi.cell import MMI2x1Tapered
from picazzo3.filters.mmi.cell import MMI2x2Tapered
from picazzo3.traces.wire_wg.trace import WireWaveguideTemplate
# from picazzo3.routing.place_route import PlaceComponents # To be able to place components
# from picazzo3.routing.place_route import ConnectComponents
from picazzo3.traces.wire_wg import WireWaveguideTransitionLinear

# from picazzo3.routing.place_route import PlaceAndConnect
from picazzo3.routing.place_route import PlaceAndAutoRoute

import ipkiss3.all as i3

# Define Templates

wg_t1 = WireWaveguideTemplate()
wg_t1.Layout(core_width=15.0,
             cladding_width=15.0+16.0,
             core_process=i3.TECH.PROCESS.WG)

wg_sm = WireWaveguideTemplate()
wg_sm.Layout(core_width=3.8, cladding_width=3.8+16.0)



mmi_trace_template = WireWaveguideTemplate()
mmi_trace_template.Layout(core_width=20.0, cladding_width=20.0+16.0)  # MMI_width

mmi_access_template = WireWaveguideTemplate()
mmi_access_template.Layout(core_width=9.0, cladding_width=9.0+16.0)

# Define components

WG1 = i3.Waveguide(name="Dongbo",trace_template=wg_t1)
layout_WG1 = WG1.Layout(shape=[(0.0, 0.0), (50.0, 0.0)]
                        )

WG2 = WireWaveguideTransitionLinear(start_trace_template=wg_t1,
                             end_trace_template=wg_sm)
layout_WG2 = WG2.Layout(start_position=(50.0,0.0), end_position=(350.0,0.0))

#layout_WG2.visualize()

WG3 = WireWaveguideTransitionLinear(start_trace_template=wg_sm,
                             end_trace_template=wg_t1)
layout_WG3 = WG3.Layout(start_position=(50.0,0.0), end_position=(350.0,0.0))



mmi1_12 = MMI1x2Tapered(mmi_trace_template=mmi_trace_template,
                        input_trace_template=mmi_access_template,
                        output_trace_template=mmi_access_template,
                        trace_template=wg_sm,
                        )

layout_mmi1_12 = mmi1_12.Layout(transition_length=200.0, length=97.0, trace_spacing=11.0)



mmi22 = MMI2x2Tapered(mmi_trace_template=mmi_trace_template,
                        input_trace_template=mmi_access_template,
                        output_trace_template=mmi_access_template,
                        trace_template=wg_sm,
                        )

layout_mmi22 = mmi22.Layout(transition_length=200.0, length=398.0, trace_spacing=11.0)

# layout_mmi1_21.visualize(annotate="true")

pr = PlaceAndAutoRoute( trace_template=wg_sm,
                        child_cells={
                                    "MMI1a": mmi22,
                                    "MMI1b": mmi22,
                                    "WGup": WG1,"WGup3": WG1,
                                    "WGdown": WG1, "WGdown3": WG1,
                                    "WGup2": WG1,
                                    "WGdown2": WG1,
                                     "WGuptaper":WG2,
                                     "WGdowntaper":WG2,
                                     "WGuptaper2":WG3,
                                     "WGdowntaper2":WG3},
                       links=[
                              ("MMI1b:out2", "WGuptaper2:in"),
                              ("MMI1b:out1", "WGdowntaper2:in"),
                             ("MMI1a:in1","WGdown2:out"),("MMI1a:in2","WGup2:out"),
                           ("MMI1a:out1","WGdown3:in"),("MMI1a:out2","WGup3:in"),
                              ("WGuptaper:out", "MMI1b:in2"),
                              ("WGdowntaper:out", "MMI1b:in1")
                       ]
                       )

layout = pr.Layout(child_transformations={"MMI1b": (1200, 0),
                                            "MMI1a": (1200+3600, 0),
                                          "WGup": (0, 4000),
                                          "WGuptaper":(0,4000),
                                          "WGdown": (0, -4000),
                                          "WGdowntaper":(0,-4000),
                                          "WGuptaper2":(2700,2000),
                                          "WGdowntaper2":(2700,-6000),
                                          "WGup2": (3050, 2000),"WGup3": (7050, 4000),"WGdown3": (7050, -4000),
                                          "WGdown2": (3050, -6000)},
                    bend_radius=300

                   )

#layout.visualize(annotate=True)

# my_ring_layout.write_gdsii("my_ring.gds")
layout.write_gdsii("testmmiV6.gds")