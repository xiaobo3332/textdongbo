from technologies import silicon_photonics
from picazzo3.filters.mmi.cell import MMI1x2Tapered
from picazzo3.filters.mmi.cell import MMI2x1Tapered
from picazzo3.traces.wire_wg.trace import WireWaveguideTemplate
from picazzo3.traces.wire_wg import WireWaveguideTransitionLinear
from picazzo3.routing.place_route import PlaceAndAutoRoute
from picazzo3.container.transition_ports import AutoTransitionPorts

import ipkiss3.all as i3


class MMI2112(PlaceAndAutoRoute):
    wg_sm = i3.WaveguideTemplateProperty()
    mmi_trace_template = i3.WaveguideTemplateProperty()
    mmi_access_template = i3.WaveguideTemplateProperty()

    mmi1_12 = i3.ChildCellProperty()
    mmi1_21 = i3.ChildCellProperty()
    WG2 = i3.ChildCellProperty()

    # def _default_external_port_names(self):
    #     ports = dict()
    #     ports["MMI1b:in1"] = "vertical_in"
    #     ports["MMI1b:in2"] = "out"
    #     return ports

    def _default_links(self):
        links = [("taper:out", "taper2:out")]
        return links

    def _default_child_cells(self):
        child_cells = {
            "MMI1a": self.mmi1_12,
            "MMI1b": self.mmi1_21,
            "taper": self.WG2,
            "taper2": self.WG2
        }
        return child_cells

    def _default_trace_template(self):
        wg_sm2 = WireWaveguideTemplate()
        wg_sm2.Layout(core_width=3.1, cladding_width=3.1 + 16.0)
        return wg_sm2

    def _default_mmi1_12(self):
        mmi12 = MMI1x2Tapered(mmi_trace_template=self.mmi_trace_template,
                              input_trace_template=self.mmi_access_template,
                              output_trace_template=self.mmi_access_template,
                              trace_template=self.wg_sm,
                              port_labels=["out1", "out2"],
                              )

        return mmi12

    def _default_mmi1_21(self):
        mmi21 = MMI2x1Tapered(mmi_trace_template=self.mmi_trace_template,
                              input_trace_template=self.mmi_access_template,
                              output_trace_template=self.mmi_access_template,
                              trace_template=self.wg_sm,
                              port_labels=["in1", "in2"],
                              )

        return mmi21

    def _default_WG2(self):
        WG2 = WireWaveguideTransitionLinear(start_trace_template=self.mmi_access_template,
                                            end_trace_template=self.trace_template)
        return WG2

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
        length = i3.PositiveNumberProperty(doc="MMI length", default=97)

        # def _default_WG1(self):
        #     layout_WG1 = self.cell.WG1.get_default_view(i3.LayoutView)
        #     layout_WG1.set(shape=[(0.0, 0.0), (150.0, 0.0)])
        #     return layout_WG1
        #
        def _default_WG2(self):
            layout_WG2 = self.cell.WG2.get_default_view(i3.LayoutView)
            layout_WG2.set(start_position=(0.0, 0.0), end_position=(200.0, 0.0))
            return layout_WG2

        def _default_mmi1_12(self):
            layout_mmi1_12 = self.cell.mmi1_12.get_default_view(i3.LayoutView)
            layout_mmi1_12.set(transition_length=200.0, length=self.length, trace_spacing=11.0)
            return layout_mmi1_12

        def _default_mmi1_21(self):
            layout_mmi1_21 = self.cell.mmi1_21.get_default_view(i3.LayoutView)
            layout_mmi1_21.set(transition_length=200.0, length=self.length, trace_spacing=11.0)
            # print layout_mmi1_21.ports['in1'].x
            return layout_mmi1_21

        def _default_child_transformations(self):
            # print self.cell.mmi1_12.get_default_view(i3.LayoutView).length
            # print self.cell.mmi1_21.get_default_view(i3.LayoutView).ports['in1'].x
            # print self.cell.mmi1_21.get_default_view(i3.LayoutView).ports['out'].x
            # a = self.cell.mmi1_21.get_default_view(i3.LayoutView).ports['out'].x - self.cell.mmi1_21.get_default_view(i3.LayoutView).ports['in1'].x
            a = self.cell.mmi1_21.get_default_view(i3.LayoutView).ports['out'].x
            child_transformations = {"MMI1a": (a + 490, 0),
                                     "taper": (a, 0),
                                     "taper2": i3.HMirror(0.0) + i3.Translation((a + 490, 0))
                                     # "WGup": (0, 4000),
                                     # "WGuptaper": (0, 4000),
                                     # "WGdown": (0, -4000),
                                     # "WGdowntaper": (0, -4000),
                                     # "WGuptaper2": i3.HMirror() + i3.Translation((3400, 4000)),
                                     # "WGdowntaper2": i3.HMirror() + i3.Translation((3400, -4000)),
                                     # "WGup2": (3250, 4000),
                                     # "WGdown2": (3250, -4000)
                                     }
            return child_transformations


# mmi1 = MMI2112()
# mmi1_layout = mmi1.Layout(length=120)
# mmi1_layout.visualize(annotate=True)
# print mmi1_layout.ports
# mmi1_layout.write_gdsii("MMI2112_V5.gds")