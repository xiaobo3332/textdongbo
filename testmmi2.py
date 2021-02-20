from technologies import silicon_photonics

from picazzo3.traces.wire_wg.trace import WireWaveguideTemplate

from picazzo3.routing.place_route import PlaceAndAutoRoute

import ipkiss3.all as i3

# Define Templates

wg_t1 = WireWaveguideTemplate()
wg_t1.Layout(core_width=15.0,
             cladding_width=15.0+16.0,
             )

# Define components

WG1 = i3.Waveguide(trace_template=wg_t1)

layout_WG1 = WG1.Layout(shape=[(0.0, 0.0), (50.0, 0.0)]
                        )

pr = PlaceAndAutoRoute(trace_template=wg_t1,
                       child_cells={
                                    "WGup": WG1,
                                    "WGdown": WG1},
                       links=[
                              ("WGup:in", "WGdown:out"),
                              ]
                       )

layout = pr.Layout(child_transformations={
                                          "WGup": (400, 0),
                                          "WGdown": (-4000, 0)},
                                    )

#layout.visualize(annotate=True)

layout.write_gdsii("testmmi2.gds")