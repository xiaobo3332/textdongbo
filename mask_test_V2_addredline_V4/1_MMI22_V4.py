from technologies import silicon_photonics
# from picazzo3.filters.mmi.cell import MMI1x2Tapered
# from picazzo3.filters.mmi.cell import MMI2x1Tapered
from picazzo3.filters.mmi.cell import MMI2x2Tapered
from picazzo3.traces.wire_wg.trace import WireWaveguideTemplate

from picazzo3.traces.wire_wg import WireWaveguideTransitionLinear

from picazzo3.routing.place_route import PlaceAndAutoRoute

import ipkiss3.all as i3

# import numpy as np


class v8(PlaceAndAutoRoute):
    wg_t1 = i3.WaveguideTemplateProperty()
    wg_sm = i3.WaveguideTemplateProperty()
    mmi_trace_template = i3.WaveguideTemplateProperty()
    mmi_access_template = i3.WaveguideTemplateProperty()
    WGSM = i3.ChildCellProperty()
    widtha = i3.PositiveNumberProperty(doc="width of ports", default=15)

    mmi22 = i3.ChildCellProperty()
    WG1 = i3.ChildCellProperty()
    WG2 = i3.ChildCellProperty()
    #
    # start_id = None
    start_id = i3.PositiveNumberProperty(doc="name", default=1)
    # start_id = current_id
    param_num = 5

    def _default_links(self):
        links = [
            ("MMI1b:out2", "WGuptaper2:out"),
            ("MMI1b:out1", "WGdowntaper2:out"),
            # ("MMI1b:out","MMI1a:in"),
            ("WGuptaper:out", "MMI1b:in2"),
            ("WGdowntaper:out", "MMI1b:in1"),

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
        mmi22 = MMI2x2Tapered(mmi_trace_template=self.mmi_trace_template,
                              input_trace_template=self.mmi_access_template,
                              output_trace_template=self.mmi_access_template,
                              trace_template=self.wg_sm,
                              )
        return mmi22

    def _default_WG2(self):
        WG2 = WireWaveguideTransitionLinear(name="Dongbo{}".format(str(self.start_id)),
                                            start_trace_template=self.wg_t1,
                                            end_trace_template=self.wg_sm,
                                            )
        return WG2

    def _default_WG1(self):
        WG1 = i3.Waveguide(name="Dongbo{}".format(str(self.start_id + 1)), trace_template=self.wg_t1)
        return WG1

    def _default_wg_t1(self):
        wg_t1 = WireWaveguideTemplate(name="port_{}".format(str(self.widtha)))
        wg_t1.Layout(core_width=self.widtha,
                     cladding_width=self.widtha + 16.0,
                     core_process=i3.TECH.PROCESS.WG)
        return wg_t1

    def _default_wg_sm(self):
        wg_sm = WireWaveguideTemplate(name="dongbo{}".format(str(self.start_id + 3)))
        wg_sm.Layout(core_width=3.8, cladding_width=3.8 + 16.0)
        return wg_sm

    def _default_WGSM(self):
        WGSM = i3.Waveguide(name="SM", trace_template=self.trace_template)

        return WGSM

    def _default_mmi_trace_template(self):
        mmi_trace_template = WireWaveguideTemplate(name="dongbo{}".format(str(self.start_id + 4)))
        mmi_trace_template.Layout(core_width=20.0, cladding_width=20.0 + 16.0)  # MMI_width
        return mmi_trace_template

    def _default_mmi_access_template(self):
        mmi_access_template = WireWaveguideTemplate(name="dongbo{}".format(str(self.start_id + 5)))
        mmi_access_template.Layout(core_width=9.0, cladding_width=9.0 + 16.0)
        return mmi_access_template

    class Layout(PlaceAndAutoRoute.Layout):
        length = i3.PositiveNumberProperty(doc="MMI length", default=398)

        # width = i3.PositiveNumberProperty(doc="width of ports", default=15)

        # def _default_wg_t1(self):
        #     layout_wg_t1 = self.cell.wg_t1.get_default_view(i3.LayoutView)
        #     layout_wg_t1.set(core_width=self.width,
        #                      cladding_width=self.width + 16.0,
        #                      core_process=i3.TECH.PROCESS.WG)
        #     return layout_wg_t1

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
            layout_mmi22 = self.cell.mmi22.get_default_view(i3.LayoutView)
            layout_mmi22.set(name="MMI22_l_{}".format(str(self.length)), transition_length=200.0, length=self.length, trace_spacing=11.0)
            return layout_mmi22

        def _default_child_transformations(self):
            child_transformations = {"MMI1b": (1300, 0),
                                     "WGup": (0, 4000),
                                     "WGuptaper": (0, 4000),
                                     "WGdown": (0, -4000),
                                     "WGdowntaper": (0, -4000),
                                     "WGuptaper2": i3.HMirror() + i3.Translation((3000, 2000)),
                                     "WGdowntaper2": i3.HMirror() + i3.Translation((3000, -6000)),
                                     "WGup2": (2850, 2000),
                                     "WGdown2": (2850, -6000),

                                     "dummy1": (1300, -300),
                                     "DWGup": (0, 4150),
                                     "DWGuptaper": (0, 4150),
                                     "DWGdown": (0, -4150),
                                     "DWGdowntaper": (0, -4150),
                                     "DWGuptaper2": i3.HMirror() + i3.Translation((3000, 4150)),
                                     "DWGdowntaper2": i3.HMirror() + i3.Translation((3000, -6150)),
                                     "DWGup2": (2850, 4150),
                                     "DWGdown2": (2850, -6150)
                                     }
            return child_transformations

        def _default_bend_radius(self):
            bend_radius = 300
            return bend_radius

        def _generate_elements(self, elems):

                elems += i3.PolygonText(layer=i3.TECH.PPLAYER.WG.TEXT,
                                        text='Name={}_{}'.format(self.cell.mmi22.get_default_view(i3.LayoutView).name, self.cell.wg_t1.name),
                                        coordinate=(1300.0, 100.0),
                                        alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
                                        font=2,
                                        height=20.0)

                elems += i3.PolygonText(layer=i3.TECH.PPLAYER.WG.TEXT,
                                        text='Name={}_{}'.format(self.cell.mmi22.get_default_view(i3.LayoutView).name,
                                                                 self.cell.wg_t1.name),
                                        coordinate=(-2000.0, -150.0),
                                        alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
                                        font=2,
                                        height=200.0,
                                        transformation=i3.Rotation((0.0, 0.0), 90.0))


                return elems


#
current_id = 1
mmi1 = v8(name="P1", widtha=10, start_id=current_id)
current_id += mmi1.param_num
mmi1_layout = mmi1.Layout(length=390)
# from copy import deepcopy
# mmi1.wg_t1 = deepcopy(mmi1.wg_t1 )
mmi2 = v8(name="P2", widtha=10, start_id=current_id)
current_id += mmi2.param_num
mmi2_layout = mmi2.Layout(length=398)
mmi3 = v8(name="P3", widtha=10, start_id=current_id)
current_id += mmi3.param_num
mmi3_layout = mmi3.Layout(length=406)
mmi4 = v8(name="P4", widtha=15, start_id=current_id)
current_id += mmi4.param_num
mmi4_layout = mmi4.Layout(length=390)
mmi5 = v8(name="P5", widtha=15, start_id=current_id)
current_id += mmi5.param_num
mmi5_layout = mmi5.Layout(length=398)
mmi6 = v8(name="P6", widtha=15, start_id=current_id)
current_id += mmi6.param_num
mmi6_layout = mmi6.Layout(length=406)
mmi7 = v8(name="P7", widtha=20, start_id=current_id)
current_id += mmi7.param_num
mmi7_layout = mmi7.Layout(length=390)
mmi8 = v8(name="P8", widtha=20, start_id=current_id)
current_id += mmi8.param_num
mmi8_layout = mmi8.Layout(length=398)
mmi9 = v8(name="P9", widtha=20, start_id=current_id)
current_id += mmi9.param_num
mmi9_layout = mmi9.Layout(length=406)

mmi10 = v8(name="P10", widtha=10, start_id=current_id)
current_id += mmi10.param_num
mmi10_layout = mmi10.Layout(length=382)
mmi11 = v8(name="P11", widtha=10, start_id=current_id)
current_id += mmi11.param_num
mmi11_layout = mmi11.Layout(length=414)
mmi12 = v8(name="P12", widtha=15, start_id=current_id)
current_id += mmi12.param_num
mmi12_layout = mmi12.Layout(length=382)

mmi13 = v8(name="P13", widtha=15, start_id=current_id)
current_id += mmi13.param_num
mmi13_layout = mmi13.Layout(length=414)
mmi14 = v8(name="P14", widtha=20, start_id=current_id)
current_id += mmi14.param_num
mmi14_layout = mmi14.Layout(length=382)
mmi15 = v8(name="P15", widtha=20, start_id=current_id)
current_id += mmi15.param_num
mmi15_layout = mmi15.Layout(length=414)

# mmi1.set(width=10)
# mmi1_layout.write_gdsii("MMI22_V2.gds")
# mmi2 = v8(name="P2", width=20)
# mmi2.set(width=20)
# mmi2_layout = mmi2.Layout()
# mmi3 = v8(name="P3", widtha=20)
# mmi2.set(width=20)


# print mmi1.width
# mmi1_layout.write_gdsii("MMI22_V2_1.gds")
# mmi2_layout.write_gdsii("MMI22_V2_2.gds")
# mmi3_layout.write_gdsii("MMI22_V2_3.gds")

pr = PlaceAndAutoRoute(
    child_cells={
        "1": mmi1,
        "2": mmi2,
        "3": mmi3,
        "4": mmi4,
        "5": mmi5,
        "6": mmi6,
        "7": mmi7,
        "8": mmi8,
        "9": mmi9,
        "10": mmi10,
        "11": mmi11,
        "12": mmi12,
        "13": mmi13,
        "14": mmi14,
        "15": mmi15
    }
)

pr_layout = pr.Layout(child_transformations={"10": (0, 0),
                                             "1": i3.HMirror(0.0) + i3.Translation((6000, 0)),
                                             "2": (6000, 0),

                                             "12": (0, 10700),
                                             "4": i3.HMirror(0.0) + i3.Translation((6000, 10700)),
                                             "5": (6000, 10700),

                                             "14": (0, 21400),
                                             "7": i3.HMirror(0.0) + i3.Translation((6000, 21400)),
                                             "8": (6000, 21400),

                                             "3": i3.HMirror(0.0) + i3.Translation((12000, 0)),
                                             "11": (12000, 0),

                                             "6": i3.HMirror(0.0) + i3.Translation((12000, 10700)),
                                             "13": (12000, 10700),

                                             "9": i3.HMirror(0.0) + i3.Translation((12000, 21400)),
                                             "15": (12000, 21400)
                                             })
pr_layout.visualize(annotate=True)
pr_layout.write_gdsii("1_MMI22_V4.gds")
