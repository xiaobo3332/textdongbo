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
    wg_t1 = i3.WaveguideTemplateProperty()
    wg_dc2 = i3.WaveguideTemplateProperty()
    width = i3.PositiveNumberProperty(doc="width of ports", default=15)
    start_id = i3.PositiveNumberProperty(doc="name_id", default=1)

    def _default_wg_t1(self):
        wg_t1 = WireWaveguideTemplate(name="port_template{}".format(str(self.start_id + 1)))
        wg_t1.Layout(core_width=self.width,
                     cladding_width=self.width + 16.0,
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
        WG1 = i3.Waveguide(name="straight{}".format(str(self.start_id + 2)), trace_template=self.wg_t1)
        return WG1

    def _default_WG2(self):
        WG2 = WireWaveguideTransitionLinear(name="taper{}".format(str(self.start_id + 3)),
                                            start_trace_template=self.wg_t1,
                                            end_trace_template=self.trace_template)
        return WG2

    def _default_dc(self):
        dc = BendDirectionalCoupler(name="my_dircoup_1",
                                    trace_template1=self.trace_template,
                                    coupler_length=923.0)
        dc.Layout(coupler_spacing=1.5 + 3.8,
                  bend_radius=300.0,
                  # manhattan=True,
                  # straight_after_bend=600.0,
                  bend_angle=90.0)
        return dc

    def _default_dc2(self):
        dc2 = BendDirectionalCoupler(name="my_dircoup_2",
                                     trace_template1=self.wg_dc2,
                                     coupler_length=888.0)
        dc2.Layout(coupler_spacing=2 + 2.8,
                   bend_radius=300.0,
                   # manhattan=True,
                   bend_angle=90.0)
        return dc2

    def _default_child_cells(self):
        child_cells = dict()
        for counter in range(0, 8, 1):
            print counter
            child_cells['straight' + str(counter)] = self.WG1
            child_cells['taper' + str(counter)] = self.WG2
        child_cells["dircoup1"] = self.dc
        child_cells["dircoup2"] = self.dc2
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
            ("taper7:out", "dircoup2:out1")
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
            return trans

        def _default_bend_radius(self):
            bend_radius = 300
            return bend_radius

        # def _default_start_straight(self):
        #     start_straight = 100.0
        #     return start_straight


current_id = 1
para_num = 3
dc_10 = my_dc(width=10, start_id=current_id)
current_id += para_num
dc_15 = my_dc(width=15, start_id=current_id)
current_id += para_num
dc_20 = my_dc(width=20, start_id=current_id)
current_id += para_num


# dc_10_layout = dc_10.Layout()
# dc_10_layout.visualize(annotate=True)
# dc_10_layout.write_gdsii("DC_V2.gds")

pr = PlaceAndAutoRoute(
    child_cells={
        "dc1": dc_10,
        "dc2": dc_15,
        "dc3": dc_20
    }
)
pr_layout = pr.Layout(child_transformations={"dc1": (0, 0),
                                             "dc2": (0, 8300),
                                             "dc3": (0, 16600)
                                             })
# pr_layout.visualize()
pr_layout.write_gdsii("DC_V2.gds")
