from technologies import silicon_photonics
# from picazzo3.filters.mmi.cell import MMI1x2Tapered
# from picazzo3.filters.mmi.cell import MMI2x1Tapered
from picazzo3.filters.mmi.cell import MMI2x2Tapered
from picazzo3.traces.wire_wg.trace import WireWaveguideTemplate

from picazzo3.traces.wire_wg import WireWaveguideTransitionLinear

from picazzo3.routing.place_route import PlaceAndAutoRoute

import ipkiss3.all as i3

from MMI2112_V3 import MMI2112


class v9(PlaceAndAutoRoute):
    wg_t1 = i3.WaveguideTemplateProperty()
    wg_sm = i3.WaveguideTemplateProperty()
    mmi_trace_template = i3.WaveguideTemplateProperty()
    mmi_access_template = i3.WaveguideTemplateProperty()
    length2 = i3.PositiveNumberProperty(doc="MMI2 length", default=97)
    mmi22 = i3.ChildCellProperty()
    WG1 = i3.ChildCellProperty()
    WG2 = i3.ChildCellProperty()

    def _default_links(self):
        links = [
            ("MMI1b:MMI1a_out2", "WGuptaper2:out"),
            ("MMI1b:MMI1a_out1", "WGdowntaper2:out"),
            # ("MMI1b:out","MMI1a:in"),
            ("WGuptaper:out", "MMI1b:MMI1b_in2"),
            ("WGdowntaper:out", "MMI1b:MMI1b_in1")
        ]
        return links

    def _default_child_cells(self):
        child_cells = {
            "MMI1b": self.mmi22,
            "WGup": self.WG1,
            "WGdown": self.WG1,
            "WGup2": self.WG1,
            "WGdown2": self.WG1,
            "WGuptaper": self.WG2,
            "WGdowntaper": self.WG2,
            "WGuptaper2": self.WG2,
            "WGdowntaper2": self.WG2}
        return child_cells

    def _default_trace_template(self):
        trace_template = self.wg_sm
        return trace_template

    def _default_mmi22(self):
        mmi22 = MMI2112(length=self.length2)
        # mmi22 = MMI2112()
        return mmi22

    def _default_WG2(self):
        WG2 = WireWaveguideTransitionLinear(start_trace_template=self.wg_t1,
                                            end_trace_template=self.wg_sm)
        return WG2

    def _default_WG1(self):
        WG1 = i3.Waveguide(name="Dongbo", trace_template=self.wg_t1)
        return WG1

    def _default_wg_t1(self):
        wg_t1 = WireWaveguideTemplate()
        wg_t1.Layout(core_width=15.0,
                     cladding_width=15.0 + 16.0,
                     core_process=i3.TECH.PROCESS.WG)
        return wg_t1

    def _default_wg_sm(self):
        wg_sm = WireWaveguideTemplate()
        wg_sm.Layout(core_width=3.8, cladding_width=3.8 + 16.0)
        return wg_sm

    def _default_mmi_trace_template(self):
        mmi_trace_template = WireWaveguideTemplate()
        mmi_trace_template.Layout(core_width=20.0, cladding_width=20.0 + 16.0)  # MMI_width
        return mmi_trace_template

    def _default_mmi_access_template(self):
        mmi_access_template = WireWaveguideTemplate()
        mmi_access_template.Layout(core_width=9.0, cladding_width=9.0 + 16.0)
        return mmi_access_template

    class Layout(PlaceAndAutoRoute.Layout):

        # length2 = i3.PositiveNumberProperty(doc="MMI2 length", default=97)

        def _default_WG1(self):
            layout_WG1 = self.cell.WG1.get_default_view(i3.LayoutView)
            layout_WG1.set(shape=[(0.0, 0.0), (150.0, 0.0)])
            return layout_WG1

        def _default_WG2(self):
            layout_WG2 = self.cell.WG2.get_default_view(i3.LayoutView)
            layout_WG2.set(start_position=(150.0, 0.0), end_position=(450.0, 0.0))
            return layout_WG2

        # def _default_mmi22(self):
        #     # layout_mmi22 = self.cell.mmi22.get_default_view(i3.LayoutView)
        #     self.cell.mmi22.length = self.length2
        #     layout_mmi22 = self.cell.mmi22.get_default_view(i3.LayoutView)
        #     return layout_mmi22

        def _default_child_transformations(self):
            child_transformations = {"MMI1b": (1300, 0),
                                     "WGup": (0, 4000),
                                     "WGuptaper": (0, 4000),
                                     "WGdown": (0, -4000),
                                     "WGdowntaper": (0, -4000),
                                     "WGuptaper2": i3.HMirror() + i3.Translation((3300, 2000)),
                                     "WGdowntaper2": i3.HMirror() + i3.Translation((3300, -6000)),
                                     "WGup2": (3150, 2000),
                                     "WGdown2": (3150, -6000)}
            return child_transformations

        def _default_bend_radius(self):
            bend_radius = 300
            return bend_radius


mmmi1 = v9(name="PP1", length2=92)
# mmmi1.length2 = 92
# mmmi1._default_mmi22(92)

mmmi1_layout = mmmi1.get_default_view(i3.LayoutView)

# print mmmi1.length2
# print v9.length2
# mmmi1_layout.write_gdsii("MMI2112_V4_1.gds")

mmmi2 = v9(name="PP2", length2=97)
# mmmi2.length2 = 97

# print mmmi1.length2
# print v9.length2
# print mmmi2.length2
mmmi2_layout = mmmi2.get_default_view(i3.LayoutView)

# mmmi1_layout.write_gdsii("MMI2112_V4_2.gds")

mmmi3 = v9(name="PP3", length2=102)
# # mmmi3.length2 = 102
# mmmi3_layout = mmmi3.Layout()
#
# print mmmi1.length2
# print mmmi2.length2
# print mmmi3.length2
# mmmi1_layout.write_gdsii("MMI2112_V4_1.gds")
# mmmi1_layout.write_gdsii("MMI2112_V4_2.gds")



prr = PlaceAndAutoRoute(
    child_cells={
        "cell_1": mmmi1,
        "cell_2": mmmi2,
        "cell_3": mmmi3
    }
)

prr_layout = prr.Layout(
    child_transformations={
        # "cell_1": (0, 0),
        # "cell_2": (3300, 0),
        # "cell_3": (6600, 0)
        "cell_1": i3.HMirror(0.0)+i3.Translation((3300, 0)),
        "cell_2": i3.Translation((3300, 0)),
        "cell_3": i3.HMirror(0.0) + i3.Translation((9900, 0))
    }
)

# prr_layout.visualize()
prr_layout.write_gdsii("MMI2112_V4.gds")
