from technologies import silicon_photonics
from picazzo3.traces.wire_wg.trace import WireWaveguideTemplate
# from picazzo3.routing.place_route import ConnectComponents
from picazzo3.traces.wire_wg import WireWaveguideTransitionLinear
# from picazzo3.routing.place_route import PlaceAndConnect
from picazzo3.routing.place_route import PlaceAndAutoRoute
import ipkiss3.all as i3
from picazzo3.wg.dircoup import BendDirectionalCoupler


class my_dc(PlaceAndAutoRoute):
    dc = i3.ChildCellProperty()
    dc2 = i3.ChildCellProperty()
    WG1 = i3.ChildCellProperty()
    WG2 = i3.ChildCellProperty()
    WGSM = i3.ChildCellProperty()
    wg_t1 = i3.WaveguideTemplateProperty()
    wg_dc2 = i3.WaveguideTemplateProperty()
    width = i3.PositiveNumberProperty(doc="width of ports", default=15)
    # start_id = i3.PositiveNumberProperty(doc="name_id", default=1)

    def _default_wg_t1(self):
        wg_t1 = WireWaveguideTemplate(name="port_{}".format(str(self.width)))
        wg_t1.Layout(core_width=self.width,
                     cladding_width=self.width + 16,
                     core_process=i3.TECH.PROCESS.WG)
        return wg_t1

    def _default_trace_template(self):
        wg_sm = WireWaveguideTemplate(name="sm_template")
        wg_sm.Layout(core_width=3.8, cladding_width=3.8 + 16.0)
        return wg_sm

    def _default_wg_dc2(self):
        wg_dc2 = WireWaveguideTemplate(name="dc2_template")
        wg_dc2.Layout(core_width=2.8, cladding_width=2.8 + 16.0)
        return wg_dc2

    def _default_WG1(self):
        WG1 = i3.Waveguide(name="straight{}".format(str(self.width)), trace_template=self.wg_t1)
        return WG1

    def _default_WG2(self):
        WG2 = WireWaveguideTransitionLinear(name="taper{}".format(str(self.width)),
                                            start_trace_template=self.wg_t1,
                                            end_trace_template=self.trace_template)
        return WG2

    def _default_WGSM(self):
        WGSM = i3.Waveguide(name="SM", trace_template=self.trace_template)

        return WGSM

    def _default_dc(self):
        dc = BendDirectionalCoupler(name="DC_gap_1.5_l_923",
                                    trace_template1=self.trace_template,
                                    coupler_length=923.0)
        dc.Layout(coupler_spacing=1.5 + 3.8,
                  bend_radius=300.0,
                  # manhattan=True,
                  # straight_after_bend=600.0,
                  bend_angle=90.0)
        return dc

    def _default_dc2(self):
        dc2 = BendDirectionalCoupler(name="DC_gap_2_l_888",
                                     trace_template1=self.wg_dc2,
                                     coupler_length=888.0)
        dc2.Layout(coupler_spacing=2 + 2.8,
                   bend_radius=300.0,
                   # manhattan=True,
                   bend_angle=90.0)
        return dc2

    def _default_child_cells(self):
        child_cells = dict()
        for counter in range(0, 16, 1):
            print counter
            child_cells['straight' + str(counter)] = self.WG1
            child_cells['taper' + str(counter)] = self.WG2
        child_cells["dircoup1"] = self.dc
        child_cells["dircoup2"] = self.dc2
        child_cells["dummy1"] = self.WGSM
        child_cells["dummy2"] = self.WGSM
        return child_cells

    def _default_links(self):
        links = [
            ("taper0:out", "dircoup1:in2"),
            ("taper1:out", "dircoup1:in1"),
            ("taper2:out", "dircoup1:out2"),
            ("taper3:out", "dircoup1:out1"),
            ("taper4:out", "dircoup2:in2"),
            ("taper5:out", "dircoup2:in1"),
            ("taper6:out", "dircoup2:out2"),
            ("taper7:out", "dircoup2:out1"),
            ("taper8:out", "taper10:out"),
            ("taper12:out", "taper14:out"),
            ("taper9:out", "dummy1:in"),
            ("taper11:out", "dummy1:out"),
            ("taper13:out", "dummy2:in"),
            ("taper15:out", "dummy2:out")
        ]
        return links

    class Layout(PlaceAndAutoRoute.Layout):

        def _default_WG1(self):
            layout_WG1 = self.cell.WG1.get_default_view(i3.LayoutView)
            layout_WG1.set(shape=[(0.0, 0.0), (150.0, 0.0)])
            return layout_WG1

        def _default_WG2(self):
            layout_WG2 = self.cell.WG2.get_default_view(i3.LayoutView)
            layout_WG2.set(start_position=(0.0, 0.0), end_position=(300.0, 0.0))
            return layout_WG2

        def _default_WGSM(self):
            layout_WGSM = self.cell.WGSM.get_default_view(i3.LayoutView)
            layout_WGSM.set(shape=[(0.0, 0.0), (400.0, 0.0)])
            return layout_WGSM

        # def _default_dc(self):
        #     layout_dc = self.cell.dc.get_default_view(i3.LayoutView)
        #     layout_dc.set(coupler_spacing=2.5 + 3.8,
        #                   bend_radius=300.0,
        #                   manhattan=True,
        #                   # straight_after_bend=6.0,
        #                   bend_angle=90.0)
        #     return layout_dc

        def _default_child_transformations(self):
            trans = dict()
            trans["dircoup1"] = (1650, 0)
            trans["dircoup2"] = (4950, 0)
            trans["dummy1"] = (1450, -300)
            trans["dummy2"] = (4750, -300)
            # for counter in range(0, 8, 1):
            #     print counter
            #     trans['straight' + str(counter)] = (2000 * (counter + 1), 0)
            #     trans["taper" + str(counter)] = (0, 2000 * (counter + 1))
            trans["straight0"] = (0, 4000)
            trans["straight1"] = (0, -4000)
            trans["straight2"] = (3150, 2000)
            trans["straight3"] = (3150, -6000)
            trans["straight4"] = (3300, 2000)
            trans["straight5"] = (3300, -6000)
            trans["straight6"] = (6450, 4000)
            trans["straight7"] = (6450, -4000)
            trans["taper0"] = (150, 4000)
            trans["taper1"] = (150, -4000)
            trans["taper2"] = i3.HMirror(150) + i3.Translation((2850, 2000))
            trans["taper3"] = i3.HMirror(150) + i3.Translation((2850, -6000))
            trans["taper4"] = (3450, 2000)
            trans["taper5"] = (3450, -6000)
            trans["taper6"] = i3.HMirror(150) + i3.Translation((6150, 4000))
            trans["taper7"] = i3.HMirror(150) + i3.Translation((6150, -4000))

            trans["straight8"] = (0, 20900)
            trans["straight9"] = (0, -4150)
            trans["straight10"] = (3150, 20900)
            trans["straight11"] = (3150, -6150)
            trans["straight12"] = (3300, 20900)
            trans["straight13"] = (3300, -6150)
            trans["straight14"] = (6450, 20900)
            trans["straight15"] = (6450, -4150)
            trans["taper8"] = (150, 20900)
            trans["taper9"] = (150, -4150)
            trans["taper10"] = i3.HMirror(150) + i3.Translation((2850, 20900))
            trans["taper11"] = i3.HMirror(150) + i3.Translation((2850, -6150))
            trans["taper12"] = (3450, 20900)
            trans["taper13"] = (3450, -6150)
            trans["taper14"] = i3.HMirror(150) + i3.Translation((6150, 20900))
            trans["taper15"] = i3.HMirror(150) + i3.Translation((6150, -4150))

            return trans

        def _default_bend_radius(self):
            bend_radius = 300
            return bend_radius

        # def _default_start_straight(self):
        #     start_straight = 100.0
        #     return start_straight

        def _generate_elements(self, elems):

                elems += i3.PolygonText(layer=i3.TECH.PPLAYER.WG.TEXT,
                                        text='Name={}_{}'.format(self.cell.dc.name, self.cell.wg_t1.name),
                                        coordinate=(1350.0, 100.0),
                                        alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
                                        font=2,
                                        height=20.0)

                elems += i3.PolygonText(layer=i3.TECH.PPLAYER.WG.TEXT,
                                        text='Name={}_{}'.format(self.cell.dc2.name, self.cell.wg_t1.name),
                                        coordinate=(4650.0, 100.0),
                                        alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
                                        font=2,
                                        height=20.0)

                # elems += i3.PolygonText(layer=i3.TECH.PPLAYER.WG.TEXT,
                #                         text='Name={}_R={}_delay={}'.format(name, self.R, self.delay_length),
                #
                #                         coordinate=(0.0, -counter * 5 * self.R - 2 * self.R + 50.0  # -100
                #                                     ),
                #                         alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
                #                         font=2,
                #                         height=20.0)

                return elems


dc_10 = my_dc(width=10)
dc_10_layout = dc_10.Layout()
dc_10_layout.visualize(annotate=True)
dc_10_layout.write_gdsii("3_DC_V3.gds")


# dc_10 = my_dc(width=10)
# dc_15 = my_dc(width=15)
# dc_20 = my_dc(width=20)
# pr = PlaceAndAutoRoute(
#     child_cells={
#         "dc1": dc_10,
#         "dc2": dc_15,
#         "dc3": dc_20
#     }
# )
# pr_layout = pr.Layout(child_transformations={"dc1": (0, 0),
#                                              "dc2": (0, 8300),
#                                              "dc3": (0, 16600)
#                                              })
# # pr_layout.visualize()
# pr_layout.write_gdsii("3_DC_V3.gds")
