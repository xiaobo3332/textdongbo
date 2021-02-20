from technologies import silicon_photonics
from picazzo3.filters.ring import RingRectSymm180DropFilter
from picazzo3.traces.wire_wg.trace import WireWaveguideTemplate

from picazzo3.traces.wire_wg import WireWaveguideTransitionLinear

from picazzo3.routing.place_route import PlaceAndAutoRoute
from picazzo3.container.transition_ports import AutoTransitionPorts

import ipkiss3.all as i3
import numpy as np


class MMI2112(PlaceAndAutoRoute):
    # wg_sm = i3.WaveguideTemplateProperty()
    # wg_t1 = i3.WaveguideTemplateProperty()
    # mmi_trace_template = i3.WaveguideTemplateProperty()
    # mmi_access_template = i3.WaveguideTemplateProperty()
    start_id = i3.PositiveNumberProperty(doc="name", default=1)
    gap = i3.PositiveNumberProperty(doc="gap", default=1.0)

    # def __init__(self, gap2):
    #     self.gap = gap2

    ring1 = i3.ChildCellProperty()
    ring2 = i3.ChildCellProperty()

    # WG1 = i3.ChildCellProperty()
    # WG2 = i3.ChildCellProperty()

    def _default_links(self):
        links = [
            # ("MMI1a:out2", "WGuptaper2:out"),
            # ("MMI1a:out1", "WGdowntaper2:out"),
            ("MMI1b:in1", "MMI1a:out2"),
            # ("WGuptaper:out", "MMI1b:in2"),
            # ("WGdowntaper:out", "MMI1b:in1")
        ]
        return links

    def _default_child_cells(self):
        child_cells = {
            "MMI1a": self.ring1,
            "MMI1b": self.ring2}
        return child_cells

    def _default_trace_template(self):
        wg_sm = WireWaveguideTemplate(name="sm_connection")
        wg_sm.Layout(core_width=3.8,
                     cladding_width=3.8 + 16.0)
        return wg_sm

    def _default_ring1(self):
        ring1 = RingRectSymm180DropFilter(name="my_rectsymm180dropring{}".format(str(self.start_id)),
                                          ring_trace_template=self.trace_template)

        return ring1

    def _default_ring2(self):
        ring2 = RingRectSymm180DropFilter(name="my_rectsymm180dropring2{}".format(str(self.start_id)),
                                          ring_trace_template=self.trace_template)

        return ring2

    class Layout(PlaceAndAutoRoute.Layout):
        radius = i3.PositiveNumberProperty(doc="radius", default=200.0)

        length = i3.PositiveNumberProperty(doc="coupler_length", default=60.0)

        # def _default_mmi1_12(self):
        #     layout_mmi1_12 = self.cell.mmi1_12.get_default_view(i3.LayoutView)
        #     layout_mmi1_12.set(transition_length=200.0, length=self.length, trace_spacing=11.0)
        #     return layout_mmi1_12

        def _default_ring1(self):
            layout_ring1 = self.cell.ring1.get_default_view(i3.LayoutView)
            layout_ring1.set(bend_radius=self.radius,
                             coupler_lengths=[self.length, self.length],
                             coupler_radii=[300.0, 300.0],
                             coupler_angles=[90.0, 90.0],
                             coupler_spacings=[3.8 + self.cell.gap, 3.8 + self.cell.gap],
                             straights=(self.length, 0.0),
                             # manhattan=True,
                             )
            return layout_ring1

        def _default_ring2(self):
            layout_ring1 = self.cell.ring2.get_default_view(i3.LayoutView)
            layout_ring1.set(bend_radius=self.radius + 20,
                             coupler_lengths=[self.length, self.length],
                             coupler_radii=[300.0, 300.0],
                             coupler_angles=[90.0, 90.0],
                             coupler_spacings=[3.8 + self.cell.gap, 3.8 + self.cell.gap],
                             straights=(self.length, 0.0),
                             # manhattan=True,
                             )
            return layout_ring1

        def _default_child_transformations(self):
            # print self.cell.mmi1_12.get_default_view(i3.LayoutView).length
            # print self.cell.mmi1_21.get_default_view(i3.LayoutView).ports['in1'].x
            # print self.cell.mmi1_21.get_default_view(i3.LayoutView).ports['out'].x
            # a = self.cell.mmi1_21.get_default_view(i3.LayoutView).ports['out'].x - \
            #     self.cell.mmi1_21.get_default_view(i3.LayoutView).ports['in1'].x
            child_transformations = {"MMI1a": (0, -2000),
                                     "MMI1b": (0, 2500)}
            return child_transformations

        def _default_bend_radius(self):
            bend_radius = 300
            return bend_radius


mmi1 = MMI2112(gap=0.8)
mmi1_layout = mmi1.Layout(length=100)
mmi1_layout.visualize(annotate=True)
# print mmi1_layout.ports
mmi1_layout.write_gdsii("ring_test.gds")

# mmi2 = v8()
# mmi2_layout = mmi2.Layout(length=398)
# mmi3 = v8()
# mmi3_layout = mmi3.Layout(length=406)
# #
# pr = PlaceAndAutoRoute(
#     child_cells={
#         "1": mmi1,
#         "2": mmi2,
#         "3": mmi3
#     }
# )
# pr_layout = pr.Layout(
#     child_transformations={
#         "1": (0, 0),
#         "2": i3.HMirror() + i3.Translation((6000, 0)),
#         "3": (6000, 0)
#     }
# )
# pr_layout.visualize()
# pr_layout.write_gdsii("MMI22_V1.gds")
# #
# # #layout.visualize(annotate=True)
# #
# # # # my_ring_layout.write_gdsii("my_ring.gds")
