from technologies import silicon_photonics

from picazzo3.traces.wire_wg.trace import WireWaveguideTemplate

from picazzo3.traces.wire_wg import WireWaveguideTransitionLinear

from picazzo3.routing.place_route import PlaceAndAutoRoute

import ipkiss3.all as i3
from picazzo3.filters.mmi.cell import MMI1x2Tapered
from picazzo3.filters.mmi.cell import MMI2x1Tapered

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
            layout_mmi1_21.set(name="MMI2112_l_{}".format(str(self.length)), transition_length=200.0, length=self.length, trace_spacing=11.0)
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

        def _generate_elements(self, elems):

                elems += i3.PolygonText(layer=i3.TECH.PPLAYER.WG.TEXT,
                                        text='Name={}_port_15'.format(self.cell.mmi1_21.get_default_view(i3.LayoutView).name),
                                        coordinate=(200.0, 100.0),
                                        alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
                                        font=2,
                                        height=20.0)


                return elems


class v6(PlaceAndAutoRoute):
    wg_t1 = i3.WaveguideTemplateProperty()
    wg_sm = i3.WaveguideTemplateProperty()
    mmi22 = i3.ChildCellProperty()
    WG1 = i3.ChildCellProperty()
    WG2 = i3.ChildCellProperty()
    WGSM = i3.ChildCellProperty()

    def _default_links(self):
        links = [
            ("MMI1b:MMI1a_out2", "WGuptaper2:out"),
            ("MMI1b:MMI1a_out1", "WGdowntaper2:out"),
            # ("MMI1b:out","MMI1a:in"),
            ("WGuptaper:out", "MMI1b:MMI1b_in2"),
            ("WGdowntaper:out", "MMI1b:MMI1b_in1"),

            ("DWGuptaper:out", "DWGuptaper2:out"),
            ("DWGdowntaper:out", "dummy1:in"),
            ("DWGdowntaper2:out", "dummy1:out")
        ]
        return links

    def _default_child_cells(self):
        child_cells = {
            "dummy1": self.WGSM,
            "MMI1b": self.mmi22,
            "WGup": self.WG1,
            "WGdown": self.WG1,
            "WGup2": self.WG1,
            "WGdown2": self.WG1,
            "WGuptaper": self.WG2,
            "WGdowntaper": self.WG2,
            "WGuptaper2": self.WG2,
            "WGdowntaper2": self.WG2,

            "DWGup": self.WG1,
            "DWGdown": self.WG1,
            "DWGup2": self.WG1,
            "DWGdown2": self.WG1,
            "DWGuptaper": self.WG2,
            "DWGdowntaper": self.WG2,
            "DWGuptaper2": self.WG2,
            "DWGdowntaper2": self.WG2
        }
        return child_cells

    def _default_trace_template(self):
        trace_template = self.wg_sm
        return trace_template

    def _default_mmi22(self):
        mmi22 = MMI2112()
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

    def _default_WGSM(self):
        WGSM = i3.Waveguide(name="SM", trace_template=self.trace_template)

        return WGSM

    class Layout(PlaceAndAutoRoute.Layout):
        length2 = i3.PositiveNumberProperty(doc="MMI2 length", default=97)

        def _default_WG1(self):
            layout_WG1 = self.cell.WG1.get_default_view(i3.LayoutView)
            layout_WG1.set(shape=[(0.0, 0.0), (150.0, 0.0)])
            return layout_WG1

        def _default_WG2(self):
            layout_WG2 = self.cell.WG2.get_default_view(i3.LayoutView)
            layout_WG2.set(start_position=(150.0, 0.0), end_position=(450.0, 0.0))
            return layout_WG2

        def _default_WGSM(self):
            layout_WGSM = self.cell.WGSM.get_default_view(i3.LayoutView)
            layout_WGSM.set(shape=[(0.0, 0.0), (400.0, 0.0)])
            return layout_WGSM

        def _default_mmi22(self):
            # layout_mmi22 = self.cell.mmi22.get_default_view(i3.LayoutView)
            self.cell.mmi22.length = self.length2
            layout_mmi22 = self.cell.mmi22.get_default_view(i3.LayoutView)
            layout_mmi22.set(length=self.length2)
            return layout_mmi22

        def _default_child_transformations(self):
            child_transformations = {"MMI1b": (1300, 0),
                                     "WGup": (0, 4000),
                                     "WGuptaper": (0, 4000),
                                     "WGdown": (0, -4000),
                                     "WGdowntaper": (0, -4000),
                                     "WGuptaper2": i3.HMirror() + i3.Translation((3300, 2000)),
                                     "WGdowntaper2": i3.HMirror() + i3.Translation((3300, -6000)),
                                     "WGup2": (3150, 2000),
                                     "WGdown2": (3150, -6000),

                                     "dummy1": (1450, -300),
                                     "DWGup": (0, 20900),
                                     "DWGuptaper": (0, 20900),
                                     "DWGdown": (0, -4300),
                                     "DWGdowntaper": (0, -4300),
                                     "DWGuptaper2": i3.HMirror() + i3.Translation((3300, 20900)),
                                     "DWGdowntaper2": i3.HMirror() + i3.Translation((3300, -6300)),
                                     "DWGup2": (3150, 20900),
                                     "DWGdown2": (3150, -6300)

                                     }
            return child_transformations

        def _default_bend_radius(self):
            bend_radius = 300
            return bend_radius


mmmi1 = v6(name="PP1")
mmmi1_layout = mmmi1.Layout(length2=92)
mmmi2 = v6(name="PP2")
mmmi2_layout = mmmi2.Layout(length2=97)
mmmi3 = v6(name="PP3")
mmmi3_layout = mmmi3.Layout(length2=102)

prr = PlaceAndAutoRoute(
    child_cells={
        "cell_1": mmmi1,
        "cell_2": mmmi2,
        "cell_3": mmmi3
    }
)

prr_layout = prr.Layout(
    child_transformations={
        "cell_1": i3.HMirror(0.0)+i3.Translation((3300, 0)),
        "cell_2": i3.Translation((3300, 0)),
        "cell_3": i3.HMirror(0.0) + i3.Translation((9900, 0))
    }
)

prr_layout.visualize(annotate=True)
prr_layout.write_gdsii("2_2_MMI2112_V6.gds")
