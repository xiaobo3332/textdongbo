from technologies import silicon_photonics
from picazzo3.traces.wire_wg.trace import WireWaveguideTemplate
# from picazzo3.routing.place_route import ConnectComponents
from picazzo3.traces.wire_wg import WireWaveguideTransitionLinear
# from picazzo3.routing.place_route import PlaceAndConnect
from picazzo3.routing.place_route import PlaceAndAutoRoute
import ipkiss3.all as i3
from picazzo3.container.transition_ports import AutoTransitionPorts
# from picazzo3.filters.ring import RingRectSymm180DropFilter
from picazzo3.wg.spirals import DoubleSpiralRounded


class my_dc(PlaceAndAutoRoute):
    # dc = i3.ChildCellProperty()
    # dc2 = i3.ChildCellProperty()

    DC_list = i3.ChildCellListProperty(default=[])
    gap_inc_vec = i3.ListProperty(default=[], doc="gap")
    # length = i3.PositiveNumberProperty(default=60.0, doc="Length of coupler")

    WG1 = i3.ChildCellProperty(doc="", locked=True)
    WG2 = i3.ChildCellProperty()
    wg_t1 = i3.WaveguideTemplateProperty()
    # wg_dc2 = i3.WaveguideTemplateProperty()
    width = i3.PositiveNumberProperty(doc="width of ports", default=15)
    sm_width = i3.PositiveNumberProperty(doc="width of waveguide", default=3.8)

    # start_id = i3.PositiveNumberProperty(doc="name_id", default=1)

    def _default_wg_t1(self):
        wg_t1 = WireWaveguideTemplate(name="port_{}".format(str(self.width)))
        wg_t1.Layout(core_width=self.width,
                     cladding_width=self.width + 16,
                     )
        return wg_t1

    def _default_trace_template(self):
        wg_sm = WireWaveguideTemplate(name="sm_template" + str(self.sm_width))
        wg_sm.Layout(core_width=self.sm_width, cladding_width=self.sm_width + 16.0)
        return wg_sm

    def _default_WG1(self):
        WG1 = i3.Waveguide(name="straight{}".format(str(self.width)), trace_template=self.wg_t1)
        WG1.Layout(shape=[(0.0, 0.0), (150.0, 0.0)])
        return WG1

    def _default_WG2(self):
        Port = AutoTransitionPorts(
            name="ports{}".format(str(self.sm_width)),
            contents=self.WG1,
            port_labels=["out"],
            trace_template=self.trace_template)
        Port.Layout(transition_length=300)  # .visualize(annotate=True)
        return Port

    def _default_DC_list(self):
        print '____________ MMI 2x2 ______________'
        MMI22_list = []

        for l, dl in enumerate(self.gap_inc_vec):
            # print 'length number ' + str(l)
            # print 'dl ' + str(dl)

            cell = DoubleSpiralRounded(name='R={}_width={}'.format(str(dl), str(self.sm_width)),
                                       trace_template=self.trace_template,
                                       n_o_loops=8, )
            layout = cell.Layout(angle_step=30, inner_size=[1400, 700],
                                 bend_radius=self.gap_inc_vec[l],
                                 manhattan=False,
                                 spacing=2 * 8 + self.sm_width + 5,
                                 stub_direction="V",
                                 )
            print "{}_length={}".format(str(cell.name), str(layout.trace_length()))
            # print cell.name
            # print layout.trace_length()

            MMI22_list.append(cell)

        return MMI22_list

    def _default_child_cells(self):
        child_cells = dict()
        for counter in range(0, 8, 1):
            # print counter
            # child_cells['straight' + str(counter)] = self.WG1
            child_cells['taper' + str(counter)] = self.WG2
        # child_cells["dircoup1"] = self.dc
        # child_cells["dircoup2"] = self.dc2
        # child_cells["straight"] = self.WG2

        for counter, child in enumerate(self.DC_list):
            # print 'child number' + str(counter)
            child_cells['ring' + str(counter)] = child
            # print 'child name ' + str(child.name)
            # print child
        return child_cells

    def _default_links(self):
        links = [
            ("taper0:out", "ring0:in"),
            ("taper1:out", "ring0:out"),
            ("taper2:out", "ring1:in"),
            ("taper3:out", "ring1:out"),

            ("taper4:out", "ring2:in"),
            ("taper5:out", "ring2:out"),
            ("taper6:out", "ring3:in"),
            ("taper7:out", "ring3:out"),

            # ("taper8:out", "ring2:out2"),
            # ("taper9:out", "ring2:in1"),
            # ("taper10:out", "ring2:in2"),
            # ("taper11:out", "ring2:out1"),
            # ("taper12:out", "ring3:out2"),
            # ("taper13:out", "ring3:in1"),
            # ("taper14:out", "ring3:in2"),
            # ("taper15:out", "ring3:out1"),

        ]
        return links

    class Layout(PlaceAndAutoRoute.Layout):

        def _default_child_transformations(self):
            trans = dict()
            column = 3500
            # trans["dircoup1"] = (1650, 0)
            # trans["dircoup2"] = (4950, 0)
            # trans['mzi_22_22_0'] = (0, 0)
            trans['ring0'] = (1300, -2400)
            # trans['ring1'] = i3.VMirror(0) + i3.Translation((1300, 2000))
            trans['ring1'] = (1300 + column, -2400)
            trans['ring2'] = (1300 + 2 * column, -2400)
            trans['ring3'] = (1300 + 3 * column, -2400)

            trans["taper0"] = (0, -4000)
            trans["taper1"] = i3.HMirror(0) + i3.Translation((column, -3500))
            trans["taper2"] = (0 + column, -3500)
            trans["taper3"] = i3.HMirror(0) + i3.Translation((2 * column, -4000))
            trans["taper4"] = (0 + 2 * column, -4000)
            trans["taper5"] = i3.HMirror(0) + i3.Translation((3 * column, -3500))
            trans["taper6"] = (0 + 3 * column, -3500)
            trans["taper7"] = i3.HMirror(0) + i3.Translation((4 * column, -4000))

            return trans

        def _default_bend_radius(self):
            bend_radius = 300
            return bend_radius

        # def _default_start_straight(self):
        #     end_straight = 10
        #     return end_straight

        def _generate_elements(self, elems):
            for counter, child in enumerate(self.DC_list):
                name = child.name
                # aa = child.layout.trace_length()

                elems += i3.PolygonText(layer=i3.TECH.PPLAYER.WG.TEXT,
                                        text="{}".format(name),
                                        # coordinate=(4650.0, 100.0),
                                        alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
                                        font=2,
                                        height=150.0,
                                        transformation=i3.Translation(
                                            (300 + 3500 * counter, -3200)))

                # elems += i3.Rectangle(layer=i3.TECH.PPLAYER.WG.TEXT,
                #                       center=(0, 0),
                #                       box_size=(500, 300))
            return elems
            # elems += i3.PolygonText(layer=i3.TECH.PPLAYER.WG.TEXT,
            #                         text='Name={}_{}'.format(self.cell.dc2.name, self.cell.wg_t1.name),
            #                         coordinate=(4650.0, 100.0),
            #                         alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
            #                         font=2,
            #                         height=20.0)

            # elems += i3.PolygonText(layer=i3.TECH.PPLAYER.WG.TEXT,
            #                         text='Name={}_R={}_delay={}'.format(name, self.R, self.delay_length),
            #
            #                         coordinate=(0.0, -counter * 5 * self.R - 2 * self.R + 50.0  # -100
            #                                     ),
            #                         alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
            #                         font=2,
            #                         height=20.0)

            # return elems


spr1 = my_dc(gap_inc_vec=[300, 250, 200, 150], sm_width=2.8)
spr1_layout = spr1.Layout()
# spr1_layout.visualize(annotate=True)
# spr1_layout.write_gdsii("spiral.gds")
spr2 = my_dc(gap_inc_vec=[300, 250, 200, 150], sm_width=3.0)
spr2_layout = spr2.Layout()
spr3 = my_dc(gap_inc_vec=[300, 250, 200, 150], sm_width=3.2)
spr3_layout = spr3.Layout()
spr4 = my_dc(gap_inc_vec=[300, 250, 200, 150], sm_width=3.4)
spr4_layout = spr4.Layout()
spr5 = my_dc(gap_inc_vec=[300, 250, 200, 150], sm_width=3.6)
spr5_layout = spr5.Layout()
spr6 = my_dc(gap_inc_vec=[300, 250, 200, 150], sm_width=3.8)
spr6_layout = spr6.Layout()
spr7 = my_dc(gap_inc_vec=[300, 250, 200, 150], sm_width=4.0)
spr7_layout = spr7.Layout()
spr8 = my_dc(gap_inc_vec=[300, 250, 200, 150], sm_width=4.2)
spr8_layout = spr8.Layout()

pr = PlaceAndAutoRoute(
    child_cells={
        "dc1": spr1,
        "dc2": spr2,
        "dc3": spr3,
        "dc4": spr4,
        "dc5": spr5,
        "dc6": spr6,
        "dc7": spr7,
        "dc8": spr8
    }
)
# pr_layout = pr.Layout(child_transformations={"dc1": (0, 0),
#                                              "dc2": i3.VMirror(-2000) + i3.Translation((0, 700)),
#                                              "dc3": (0, 5200),
#                                              "dc4": i3.VMirror(-2000) + i3.Translation((0, 5900)),
#                                              "dc5": (0, 10400),
#                                              "dc6": i3.VMirror(-2000) + i3.Translation((0, 11100)),
#                                              "dc7": (0, 15600),
#                                              "dc8": i3.VMirror(-2000) + i3.Translation((0, 16300))
#                                              })

pr_layout = pr.Layout(child_transformations={"dc1": (0, 0),
                                             "dc2": i3.Translation((0, 2350)),
                                             "dc3": (0, 2350*2),
                                             "dc4": i3.Translation((0, 2350*3)),
                                             "dc5": (0, 2350*4+500),
                                             "dc6": i3.Translation((0, 2350*5+500)),
                                             "dc7": (0, 2350*6+500),
                                             "dc8": i3.Translation((0, 2350*7+500))
                                             })
# pr_layout.visualize()
pr_layout.write_gdsii("spiral_v2.gds")
