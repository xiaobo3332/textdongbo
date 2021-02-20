from technologies import silicon_photonics
from picazzo3.traces.wire_wg.trace import WireWaveguideTemplate
# from picazzo3.routing.place_route import ConnectComponents
from picazzo3.traces.wire_wg import WireWaveguideTransitionLinear
# from picazzo3.routing.place_route import PlaceAndConnect
from picazzo3.routing.place_route import PlaceAndAutoRoute
import ipkiss3.all as i3
from picazzo3.container.transition_ports import AutoTransitionPorts
from picazzo3.filters.ring import RingRectSymm180DropFilter
from picazzo3.filters.ring import RingRectSymmNotchFilter


class my_dc(PlaceAndAutoRoute):
    # dc = i3.ChildCellProperty()
    # dc2 = i3.ChildCellProperty()

    DC_list = i3.ChildCellListProperty(default=[])
    gap_inc_vec = i3.ListProperty(default=[], doc="gap")
    length = i3.PositiveNumberProperty(default=80.0, doc="Length of coupler")

    WG1 = i3.ChildCellProperty(doc="", locked=True)
    WG2 = i3.ChildCellProperty()
    wg_t1 = i3.WaveguideTemplateProperty()
    # wg_dc2 = i3.WaveguideTemplateProperty()
    width = i3.PositiveNumberProperty(doc="width of ports", default=15)

    # start_id = i3.PositiveNumberProperty(doc="name_id", default=1)

    def _default_wg_t1(self):
        wg_t1 = WireWaveguideTemplate(name="port_{}".format(str(self.width)))
        wg_t1.Layout(core_width=self.width,
                     cladding_width=self.width + 16,
                     )
        return wg_t1

    def _default_trace_template(self):
        wg_sm = WireWaveguideTemplate(name="sm_template")
        wg_sm.Layout(core_width=3.8, cladding_width=3.8 + 16.0)
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

    def _default_DC_list(self):
        print '____________ MMI 2x2 ______________'
        MMI22_list = []

        for l, dl in enumerate(self.gap_inc_vec):
            print 'length number ' + str(l)
            print 'dl ' + str(dl)

            cell = RingRectSymm180DropFilter(name='SR_GAP={}_L={}'.format(str(dl), str(self.length)),
                                             ring_trace_template=self.trace_template)
            cell.Layout(bend_radius=200,
                        coupler_lengths=[self.length, self.length],
                        coupler_radii=[300.0, 300.0],
                        coupler_angles=[90.0, 90.0],
                        coupler_spacings=[3.8 + self.gap_inc_vec[l], 3.8 + self.gap_inc_vec[l]],
                        straights=(self.length, 0.0),
                        # manhattan=True,
                        )
            cell2 = RingRectSymmNotchFilter(name='ring_s' + str(dl) + str(self.length),
                                            ring_trace_template=self.trace_template)
            cell2.Layout(bend_radius=200,
                         coupler_lengths=[self.length, self.length],
                         coupler_radii=[300, 300],
                         coupler_angles=[90.0, 90],
                         coupler_spacings=[(3.8 + self.gap_inc_vec[l])],
                         straights=(self.length, 0.0),
                         # manhattan=True,
                         )

            MMI22_list.append(cell)
            MMI22_list.append(cell2)

            print 'cell name ' + str(cell.name)
            print '__________________________'

        return MMI22_list

    def _default_child_cells(self):
        child_cells = dict()
        for counter in range(0, 24, 1):
            print counter
            # child_cells['straight' + str(counter)] = self.WG1
            child_cells['taper' + str(counter)] = self.WG2
        # child_cells["dircoup1"] = self.dc
        # child_cells["dircoup2"] = self.dc2
        # child_cells["straight"] = self.WG2

        for counter, child in enumerate(self.DC_list):
            print 'child number' + str(counter)
            child_cells['ring' + str(counter)] = child
            print 'child name ' + str(child.name)
            print child
        return child_cells

    def _default_links(self):
        links = [
            ("taper0:out", "ring0:out2"),
            ("taper1:out", "ring0:in1"),
            ("taper2:out", "ring0:in2"),
            ("taper3:out", "ring0:out1"),
            ("taper4:out", "ring1:in"),
            ("taper5:out", "ring1:out"),

            ("taper6:out", "ring2:out2"),
            ("taper7:out", "ring2:in1"),
            ("taper8:out", "ring2:in2"),
            ("taper9:out", "ring2:out1"),
            ("taper10:out", "ring3:in"),
            ("taper11:out", "ring3:out"),
            ("taper12:out", "ring4:out2"),
            ("taper13:out", "ring4:in1"),
            ("taper14:out", "ring4:in2"),
            ("taper15:out", "ring4:out1"),
            ("taper16:out", "ring5:in"),
            ("taper17:out", "ring5:out"),
            ("taper18:out", "ring6:out2"),
            ("taper19:out", "ring6:in1"),
            ("taper20:out", "ring6:in2"),
            ("taper21:out", "ring6:out1"),
            ("taper22:out", "ring7:in"),
            ("taper23:out", "ring7:out"),
        ]
        return links

    class Layout(PlaceAndAutoRoute.Layout):

        def _default_child_transformations(self):
            trans = dict()
            column = 4500
            # trans["dircoup1"] = (1650, 0)
            # trans["dircoup2"] = (4950, 0)
            # trans['mzi_22_22_0'] = (0, 0)
            trans['ring0'] = (1500, -3000)
            trans['ring4'] = (1500, -3000 + 2 * column)
            trans['ring1'] = (1500, -300)
            trans['ring5'] = (1500, -300 + 2 * column)

            trans['ring2'] = (1500, -3000 + column)
            trans['ring6'] = (1500, -3000 + 3 * column)
            trans['ring3'] = (1500, -300 + column)
            trans['ring7'] = (1500, -300 + 3 * column)

            trans["taper0"] = (0, -2100)
            trans["taper1"] = (0, -3850)
            trans["taper2"] = i3.HMirror(0) + i3.Translation((3000, -1500))
            trans["taper3"] = i3.Translation((0, -4000))
            trans["taper4"] = (0, -1950)
            trans["taper5"] = i3.HMirror(0) + i3.Translation((3000, -1350))

            trans["taper6"] = (0, -2100 + column)
            trans["taper7"] = (0, -3850 + column)
            trans["taper8"] = i3.HMirror(0) + i3.Translation((3000, -1500 + column))
            trans["taper9"] = i3.Translation((0, -4000 + column))
            trans["taper10"] = (0, -1950 + column)
            trans["taper11"] = i3.HMirror(0) + i3.Translation((3000, -1350 + column))
            trans["taper12"] = (0, -2100 + 2 * column)
            trans["taper13"] = (0, -3850 + 2 * column)
            trans["taper14"] = i3.HMirror(0) + i3.Translation((3000, -1500 + 2 * column))
            trans["taper15"] = i3.Translation((0, -4000 + 2 * column))
            trans["taper16"] = (0, -1950 + 2 * column)
            trans["taper17"] = i3.HMirror(0) + i3.Translation((3000, -1350 + 2 * column))
            trans["taper18"] = (0, -2100 + 3 * column)
            trans["taper19"] = (0, -3850 + 3 * column)
            trans["taper20"] = i3.HMirror(0) + i3.Translation((3000, -1500 + 3 * column))
            trans["taper21"] = i3.Translation((0, -4000 + 3 * column))
            trans["taper22"] = (0, -1950 + 3 * column)
            trans["taper23"] = i3.HMirror(0) + i3.Translation((3000, -1350 + 3 * column))

            return trans

        def _default_bend_radius(self):
            bend_radius = 300
            return bend_radius

        def _generate_elements(self, elems):
            for counter, child in enumerate(self.DC_list):
                if (counter % 2 == 0):
                    name = child.name
                    elems += i3.PolygonText(layer=i3.TECH.PPLAYER.WG.TEXT,
                                            text="{}".format(name[0:10]),
                                            # coordinate=(4650.0, 100.0),
                                            alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
                                            font=2,
                                            height=200.0,
                                            transformation=i3.Rotation((0.0, 0.0), -90.0) + i3.Translation(
                                                (3000-450, -2000 + 4500 * counter/2)))
                else:
                    elems += i3.PolygonText(layer=i3.TECH.PPLAYER.WG.TEXT,
                                            text="R=200_L=80",
                                            alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
                                            font=2,
                                            height=80.0,
                                            transformation=i3.Rotation((0.0, 0.0), -90.0) + i3.Translation(
                                                (3000-450, -2700 + 4500 * counter/2)))

            # elems += i3.Rectangle(layer=i3.TECH.PPLAYER.WG.TEXT,
            #                       center=(0, 0),
            #                       box_size=(500, 300))
            return elems


dc_10 = my_dc(gap_inc_vec=[0.6, 0.8, 1.0, 1.2], length=80, name="ring1")
dc_10_layout = dc_10.Layout()
dc_10_layout.visualize(annotate=True)
dc_10_layout.write_gdsii("ring_single_v2.gds")

# dc_15 = my_dc(gap_inc_vec=[0.6, 0.8, 1.0, 1.2], length=90, name="ring2")
# dc_15_layout = dc_15.Layout()
# # dc_20 = my_dc(gap_inc_vec=[0.6, 0.8, 1.0, 1.2], length=100, name="ring3")
# # dc_20_layout = dc_20.Layout()
# # dc_25 = my_dc(gap_inc_vec=[0.6, 0.8, 1.0, 1.2], length=120, name="ring4")
# # dc_25_layout = dc_25.Layout()
#
#
# pr = PlaceAndAutoRoute(
#     child_cells={
#         "dc1": dc_10,
#         "dc2": dc_15,
#         # "dc3": dc_20,
#         # "dc4": dc_25
#     }
# )
# pr_layout = pr.Layout(child_transformations={"dc1": (0, 0),
#                                              "dc2": i3.HMirror(1500) + i3.Translation((3000, 0)),
#                                              # "dc3": (6000, 0),
#                                              # "dc4": i3.HMirror(1500) + i3.Translation((9000, 0))
#                                              })
# # pr_layout.visualize()
# pr_layout.write_gdsii("ring_single.gds")
