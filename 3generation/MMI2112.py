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
            a = self.cell.mmi1_21.get_default_view(i3.LayoutView).ports['out'].x
            child_transformations = {"MMI1a": (a + 490, 0),
                                     "taper": (a, 0),
                                     "taper2": i3.HMirror(0.0) + i3.Translation((a + 490, 0))

                                     }
            return child_transformations

        # def _generate_elements(self, elems):
        #     elems += i3.PolygonText(layer=i3.TECH.PPLAYER.WG.TEXT,
        #                             text='Name={}_port_15'.format(
        #                                 self.cell.mmi1_21.get_default_view(i3.LayoutView).name),
        #                             coordinate=(200.0, 100.0),
        #                             alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
        #                             font=2,
        #                             height=20.0)
        #
        #     elems += i3.PolygonText(layer=i3.TECH.PPLAYER.WG.TEXT,
        #                             text='Name={}_port_15'.format(
        #                                 self.cell.mmi1_21.get_default_view(i3.LayoutView).name),
        #                             # coordinate=(-4000.0, -1650.0),
        #                             alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
        #                             font=2,
        #                             height=200.0,
        #                             transformation=i3.Rotation((0.0, 0.0), 90.0) + i3.Translation((-2050, -2000)))
        #
        #     return elems


# MMI2112().Layout.view.write_gdsii("MMI2112.gds")

class my_MMI2112(PlaceAndAutoRoute):
    DC_list = i3.ChildCellListProperty(default=[])
    gap_inc_vec = i3.ListProperty(default=[], doc="Length of MMI")
    WG1 = i3.ChildCellProperty(doc="", locked=True)
    WG2 = i3.ChildCellProperty()
    wg_t1 = i3.WaveguideTemplateProperty(doc="board WG")
    mmi_trace_template = i3.WaveguideTemplateProperty()
    mmi_access_template = i3.WaveguideTemplateProperty()
    width = i3.PositiveNumberProperty(doc="width of ports", default=15)

    def _default_wg_t1(self):
        wg_t1 = WireWaveguideTemplate(name="port_{}".format(str(self.width)))
        wg_t1.Layout(core_width=self.width,
                     cladding_width=self.width + 2 * 12.0,
                     )
        return wg_t1

    def _default_trace_template(self):
        wg_sm = WireWaveguideTemplate(name="sm_template")
        wg_sm.Layout(core_width=3.8, cladding_width=3.8 + 2 * 12.0)
        return wg_sm

    def _default_WG1(self):
        WG1 = i3.Waveguide(name="straight{}".format(str(self.width)), trace_template=self.wg_t1)
        WG1.Layout(shape=[(0.0, 0.0), (150.0, 0.0)])
        return WG1

    def _default_WG2(self):
        Port = AutoTransitionPorts(
            name="ports{}".format(str(self.width)),
            contents=self.WG1,
            port_labels=["out"],
            trace_template=self.trace_template)
        Port.Layout(transition_length=300)  # .visualize(annotate=True)
        return Port

    def _default_mmi_trace_template(self):
        mmi_trace_template = WireWaveguideTemplate(name="MMI_tt")
        mmi_trace_template.Layout(core_width=20.0, cladding_width=20.0 + 2 * 12)  # MMI_width
        return mmi_trace_template

    def _default_mmi_access_template(self):
        mmi_access_template = WireWaveguideTemplate(name="MMI_at")
        mmi_access_template.Layout(core_width=9.0, cladding_width=9.0 + 2 * 12)
        return mmi_access_template

    def _default_DC_list(self):
        print '____________ MMI 2x2 ______________'
        MMI22_list = []

        for l, dl in enumerate(self.gap_inc_vec):
            print 'length number ' + str(l)
            print 'dl ' + str(dl)

            cell = MMI2112()

            cell.Layout(name="MMI2112_l_{}".format(str(self.gap_inc_vec[l])),
                        length=self.gap_inc_vec[l]
                        )

            # cell = RingRectSymm180DropFilter(name='ring' + str(dl) + str(self.length),
            #                                  ring_trace_template=self.trace_template)
            # cell.Layout(bend_radius=200,
            #             coupler_lengths=[self.length, self.length],
            #             coupler_radii=[300.0, 300.0],
            #             coupler_angles=[90.0, 90.0],
            #             coupler_spacings=[3.8 + self.gap_inc_vec[l], 3.8 + self.gap_inc_vec[l]],
            #             straights=(self.length, 0.0),
            #             # manhattan=True,
            #             )

            MMI22_list.append(cell)

            print 'cell name ' + str(cell.name)
            print '__________________________'

        return MMI22_list

    def _default_child_cells(self):
        child_cells = dict()
        for counter in range(0, 12, 1):
            print counter
            # child_cells['straight' + str(counter)] = self.WG1
            child_cells['taper' + str(counter)] = self.WG2

        for counter, child in enumerate(self.DC_list):
            print 'child number' + str(counter)
            child_cells['ring' + str(counter)] = child
            print 'child name ' + str(child.name)
            print child
        return child_cells

    def _default_links(self):
        links = [
            ("taper0:out", "ring0:MMI1b_in2"),
            ("taper1:out", "ring0:MMI1b_in1"),
            ("taper2:out", "ring0:MMI1a_out2"),
            ("taper3:out", "ring0:MMI1a_out1"),

            ("taper4:out", "ring1:MMI1b_in2"),
            ("taper5:out", "ring1:MMI1b_in1"),
            ("taper6:out", "ring1:MMI1a_out2"),
            ("taper7:out", "ring1:MMI1a_out1"),

            ("taper8:out", "ring2:MMI1b_in2"),
            ("taper9:out", "ring2:MMI1b_in1"),
            ("taper10:out", "ring2:MMI1a_out2"),
            ("taper11:out", "ring2:MMI1a_out1"),

        ]
        return links

    class Layout(PlaceAndAutoRoute.Layout):

        def _default_child_transformations(self):
            trans = dict()
            column = 10000
            # trans["dircoup1"] = (1650, 0)
            # trans["dircoup2"] = (4950, 0)
            # trans['mzi_22_22_0'] = (0, 0)
            trans['ring0'] = (2500, 0)
            trans['ring1'] = (2500, 0 + column)
            trans['ring2'] = (2500, 0 + 2 * column)
            # trans['ring3'] = (1500, 0 + 3 * column)

            trans["taper0"] = (0, 4000)
            trans["taper1"] = (0, -4000)
            trans["taper2"] = i3.HMirror(0) + i3.Translation((5000, 2500))
            trans["taper3"] = i3.HMirror(0) + i3.Translation((5000, -2500))

            trans["taper4"] = (0, 4000 + column)
            trans["taper5"] = (0, -4000 + column)
            trans["taper6"] = i3.HMirror(0) + i3.Translation((5000, 2500 + column))
            trans["taper7"] = i3.HMirror(0) + i3.Translation((5000, -2500 + column))

            trans["taper8"] = (0, 4000 + 2 * column)
            trans["taper9"] = (0, -4000 + 2 * column)
            trans["taper10"] = i3.HMirror(0) + i3.Translation((5000, 2500 + 2 * column))
            trans["taper11"] = i3.HMirror(0) + i3.Translation((5000, -2500 + 2 * column))

            return trans

        def _default_bend_radius(self):
            bend_radius = 300
            return bend_radius

        # def _generate_elements(self, elems):
        #     for counter, child in enumerate(self.DC_list):
        #         name = child.name
        #
        #         elems += i3.PolygonText(layer=i3.TECH.PPLAYER.WG.TEXT,
        #                                 text="{}_{}".format(name, self.cell.wg_t1.name),
        #                                 # coordinate=(1300.0, 100.0),
        #                                 alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
        #                                 font=2,
        #                                 height=20.0,
        #                                 transformation=i3.Translation((2500, 100 + 10000 * counter))
        #                                 )
        #
        #         elems += i3.PolygonText(layer=i3.TECH.PPLAYER.WG.TEXT,
        #                                 text="{}_{}".format(name, self.cell.wg_t1.name),
        #                                 # coordinate=(-2000, -150),
        #                                 alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
        #                                 font=2,
        #                                 height=200.0,
        #                                 transformation=i3.Rotation((0.0, 0.0), 90.0)
        #                                             + i3.Translation((450, -2000 + 10000 * counter))
        #                                 )

        #     return elems


# my_MMI2112(gap_inc_vec=[92, 97, 102], name="MMI2112").Layout.view.write_gdsii("MMI2112.gds")
# my_MMI2112(gap_inc_vec=[390, 398, 406], name="MMI2112").Layout.view.visualize(annotate=True)

