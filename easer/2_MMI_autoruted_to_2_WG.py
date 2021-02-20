from technologies import silicon_photonics
from picazzo3.filters.mmi.cell import MMI1x2Tapered
from picazzo3.filters.mmi.cell import MMI2x1Tapered
from picazzo3.traces.wire_wg.trace import WireWaveguideTemplate
#from picazzo3.routing.place_route import PlaceComponents # To be able to place components
#from picazzo3.routing.place_route import ConnectComponents

#from picazzo3.routing.place_route import PlaceAndConnect
from picazzo3.routing.place_route import PlaceAndAutoRoute


import ipkiss3.all as i3

# Define Templates

wg_t1 = WireWaveguideTemplate()
wg_t1.Layout(core_width=5.0,
            cladding_width=20.0,
            core_process=i3.TECH.PROCESS.WG)

mmi_trace_template = WireWaveguideTemplate()
mmi_trace_template.Layout(core_width=50.0, cladding_width=54.0) #MMI_width

mmi_access_template = WireWaveguideTemplate()
mmi_access_template.Layout(core_width=5.0, cladding_width=9.0)

# Define components

WG1 = i3.Waveguide(trace_template=wg_t1)
layout_WG1 = WG1.Layout(shape=[(-50.0, 0.0),(50.0, 0.0)]
                        )

mmi1_12 = MMI1x2Tapered(mmi_trace_template=mmi_trace_template,
                    input_trace_template=mmi_access_template,
                    output_trace_template=mmi_access_template,
                    trace_template=i3.TECH.PCELLS.WG.DEFAULT,
                    )
layout_mmi1_12 = mmi1_12.Layout(transition_length=20.0, length=100.0, trace_spacing=20.0)

mmi1_21 = MMI2x1Tapered(mmi_trace_template=mmi_trace_template,
                        input_trace_template=mmi_access_template,
                        output_trace_template=mmi_access_template,
                        trace_template=i3.TECH.PCELLS.WG.DEFAULT,
                       )

layout_mmi1_21 = mmi1_21.Layout(transition_length=20.0, length=100.0, trace_spacing=20.0)


pr = PlaceAndAutoRoute(child_cells={"MMI1a": mmi1_12,
                                  "MMI1b": mmi1_21,
                                   "WGup": WG1,
                                   "WGdown": WG1},
                     links=[ ("MMI1a:out2", "WGup:in"),
                             ("MMI1a:out1", "WGdown:in"),
                             ("WGup:out", "MMI1b:in2"),
                             ("WGdown:out", "MMI1b:in1")]
                     )


layout = pr.Layout(child_transformations={"MMI1a": (-300, 0),
                                          "MMI1b": (200, 0),
                                          "WGup":(0,50),
                                          "WGdown":(0,-50)}

                   )

layout.visualize()

# my_ring_layout.write_gdsii("my_ring.gds")
layout.write_gdsii("2_MMI_autoruted_to_2_WG.gds")