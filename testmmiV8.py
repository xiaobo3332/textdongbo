from technologies import silicon_photonics
from picazzo3.filters.mmi.cell import MMI1x2Tapered
from picazzo3.filters.mmi.cell import MMI2x1Tapered
from picazzo3.filters.mmi.cell import MMI2x2Tapered
from picazzo3.traces.wire_wg.trace import WireWaveguideTemplate

from picazzo3.traces.wire_wg import WireWaveguideTransitionLinear

from picazzo3.routing.place_route import PlaceAndAutoRoute

import ipkiss3.all as i3

class ring(PlaceAndAutoRoute):
    wg_t1 = i3.WaveguideTemplateProperty()
    wg_sm = i3.WaveguideTemplateProperty()
    mmi_trace_template = i3.WaveguideTemplateProperty()
    mmi_access_template = i3.WaveguideTemplateProperty()

    mmi22 = i3.ChildCellProperty()
    WG1 = i3.ChildCellProperty()
    WG2 = i3.ChildCellProperty()

    def _default_links(self):
        links = [
            ("MMI1b:out2", "WGuptaper2:out"),
            ("MMI1b:out1", "WGdowntaper2:out"),
            # ("MMI1b:out","MMI1a:in"),
            ("WGuptaper:out", "MMI1b:in2"),
            ("WGdowntaper:out", "MMI1b:in1")
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
        mmi22 = MMI2x2Tapered(mmi_trace_template=self.mmi_trace_template,
                              input_trace_template=self.mmi_access_template,
                              output_trace_template=self.mmi_access_template,
                              trace_template=self.wg_sm,
                              )
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
        length = i3.PositiveNumberProperty(name="MMI length",default=200)

        def _default_WG1(self):
            layout_WG1 = self.cell.WG1.get_default_view(i3.LayoutView)
            layout_WG1.set(shape=[(0.0, 0.0), (50.0, 0.0)])
            return layout_WG1

        def _default_WG2(self):
            layout_WG2 = self.cell.WG2.get_default_view(i3.LayoutView)
            layout_WG2.set(start_position=(50.0, 0.0), end_position=(350.0, 0.0))
            return layout_WG2

        def _default_mmi22(self):
            layout_mmi22 = self.cell.mmi22.get_default_view(i3.LayoutView)
            layout_mmi22.set(transition_length=200.0, length=self.length, trace_spacing=11.0)
            return layout_mmi22

        def _default_child_transformations(self):
            child_transformations={"MMI1b": (1200, 0),
                                                   "WGup": (0, 4000),
                                                   "WGuptaper": (0, 4000),
                                                   "WGdown": (0, -4000),
                                                   "WGdowntaper": (0, -4000),
                                                   "WGuptaper2": i3.HMirror()+i3.Translation((3100, 4000)),
                                                   "WGdowntaper2": i3.HMirror()+i3.Translation((3100, -4000)),
                                                   "WGup2": (3050, 4000),
                                                   "WGdown2": (3050, -4000)}
            return child_transformations

        def _default_bend_radius(self):
             bend_radius=300
             return bend_radius




mmi1= v8()
mmi2= v8()
mmi1_layout = mmi1.Layout(length=300)
mmi2_layout = mmi2.Layout(length=400)

pr = PlaceAndAutoRoute(
                        child_cells={
                                    "1": mmi1,
                                    "2": mmi2,
                                     }
                        )
layout = pr.Layout(child_transformations={"1": (0, 0),
                                          "2": (4100, 0),


                                          }

                   )
layout.write_gdsii("testmmiV8.gds")

#layout.visualize(annotate=True)

# # my_ring_layout.write_gdsii("my_ring.gds")
# layout.write_gdsii("testmmiV7.gds")