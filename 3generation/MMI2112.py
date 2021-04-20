from technologies import silicon_photonics
from picazzo3.traces.wire_wg.trace import WireWaveguideTemplate
from picazzo3.traces.wire_wg import WireWaveguideTransitionLinear
from picazzo3.routing.place_route import PlaceAndAutoRoute
import ipkiss3.all as i3
from picazzo3.container.transition_ports import AutoTransitionPorts
from picazzo3.filters.mmi.cell import MMI1x2Tapered
from picazzo3.filters.mmi.cell import MMI2x1Tapered


class MMI2112(PlaceAndAutoRoute):
    wg_sm = i3.WaveguideTemplateProperty()
    mmi_trace_template = i3.WaveguideTemplateProperty()
    mmi_access_template = i3.WaveguideTemplateProperty()

    mmi1_12 = i3.ChildCellProperty()
    mmi1_21 = i3.ChildCellProperty()
    WG2 = i3.ChildCellProperty()
    narrow = i3.ChildCellProperty()

    # def _default_links(self):
    #     links = [("taper:out", "taper2:out")]
    #     return links

    def _default_child_cells(self):
        child_cells = {
            "MMI1a": self.mmi1_12,
            # "MMI1b": self.mmi1_21,
            # "taper": self.WG2,
            "taper2": self.WG2,
            "narrow": self.narrow
        }
        return child_cells

    def _default_trace_template(self):
        wg_sm2 = WireWaveguideTemplate()
        wg_sm2.Layout(core_width=3.1, cladding_width=3.1 + 24.0)
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

    def _default_narrow(self):
        WGnarrow = i3.Waveguide(name="narrow", trace_template=self.trace_template)
        return WGnarrow

    def _default_wg_sm(self):
        wg_sm = WireWaveguideTemplate()
        wg_sm.Layout(core_width=3.8, cladding_width=3.8 + 24.0)
        return wg_sm

    def _default_mmi_trace_template(self):
        mmi_trace_template = WireWaveguideTemplate()
        mmi_trace_template.Layout(core_width=20.0, cladding_width=20.0 + 24.0)  # MMI_width
        return mmi_trace_template

    def _default_mmi_access_template(self):
        mmi_access_template = WireWaveguideTemplate()
        mmi_access_template.Layout(core_width=9.0, cladding_width=9.0 + 24.0)
        return mmi_access_template

    class Layout(PlaceAndAutoRoute.Layout):
        length = i3.PositiveNumberProperty(doc="MMI length", default=97)

        def _default_WG2(self):
            layout_WG2 = self.cell.WG2.get_default_view(i3.LayoutView)
            layout_WG2.set(start_position=(0.0, 0.0), end_position=(200.0, 0.0))
            return layout_WG2

        def _default_narrow(self):
            layout = self.cell.narrow.get_default_view(i3.LayoutView)
            layout.set(shape=[(0.0, 0.0), (90.0, 0.0)])
            return layout

        def _default_mmi1_12(self):
            layout_mmi1_12 = self.cell.mmi1_12.get_default_view(i3.LayoutView)
            layout_mmi1_12.set(transition_length=200.0, length=self.length, trace_spacing=11.0)
            return layout_mmi1_12

        def _default_mmi1_21(self):
            layout_mmi1_21 = self.cell.mmi1_21.get_default_view(i3.LayoutView)
            layout_mmi1_21.set(name="MMI2112_l_{}".format(str(self.length)), transition_length=200.0,
                               length=self.length, trace_spacing=11.0)
            # print layout_mmi1_21.ports['in1'].x
            return layout_mmi1_21

        def _default_child_transformations(self):
            # a = self.cell.mmi1_21.get_default_view(i3.LayoutView).ports['out'].x
            child_transformations = {
                "MMI1a": (290, 0),
                # "taper": (a, 0),
                "taper2": i3.HMirror(0.0) + i3.Translation((290, 0))

            }
            return child_transformations


# MMI2112().Layout.view.visualize(annotate=True)
# MMI2112().Layout.view.write_gdsii("MMI2112.gds")
