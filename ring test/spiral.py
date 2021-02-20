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

            cell = DoubleSpiralRounded(name='spiral' + str(dl) + str(self.sm_width),
                                       trace_template=self.trace_template,
                                       n_o_loops=8, )
            layout = cell.Layout(angle_step=30, inner_size=[700, 1400],
                                 bend_radius=self.gap_inc_vec[l],
                                 manhattan=False,
                                 spacing=2 * 8 + self.sm_width + 5,
                                 )
            print layout.trace_length()

            MMI22_list.append(cell)

        return MMI22_list

    def _default_child_cells(self):
        child_cells = dict()
        for counter in range(0, 4, 1):
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

            # ("taper4:out", "ring1:out2"),
            # ("taper5:out", "ring1:in1"),
            # ("taper6:out", "ring1:in2"),
            # ("taper7:out", "ring1:out1"),
            #
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
            column = 3000
            # trans["dircoup1"] = (1650, 0)
            # trans["dircoup2"] = (4950, 0)
            # trans['mzi_22_22_0'] = (0, 0)
            trans['ring0'] = (1300, -2000)
            # trans['ring1'] = i3.VMirror(0) + i3.Translation((1300, 2000))
            trans['ring1'] = (1300 + column, -2000)
            # trans['ring2'] = (1500, 0 + 2 * column)
            # trans['ring3'] = (1500, 0 + 3 * column)

            trans["taper0"] = (0, -4000)

            trans["taper1"] = i3.HMirror(0) + i3.Translation((3000, -3500))

            trans["taper2"] = (0 + column, -3500)

            trans["taper3"] = i3.HMirror(0) + i3.Translation((3000 + column, -4000))

            return trans

        def _default_bend_radius(self):
            bend_radius = 300
            return bend_radius

        def _generate_elements(self, elems):
            #
            # elems += i3.PolygonText(layer=i3.TECH.PPLAYER.WG.TEXT,
            #                         text='Name={}_{}'.format(self.cell.dc.name, self.cell.wg_t1.name),
            #                         coordinate=(1350.0, 100.0),
            #                         alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
            #                         font=2,
            #                         height=20.0)
            #
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

            return elems


spr1 = my_dc(gap_inc_vec=[300, 200], sm_width=2.8)
spr1_layout = spr1.Layout()
# spr1_layout.visualize(annotate=True)
# spr1_layout.write_gdsii("spiral.gds")
spr2 = my_dc(gap_inc_vec=[300, 200], sm_width=3.0)
spr2_layout = spr2.Layout()
spr3 = my_dc(gap_inc_vec=[300, 200], sm_width=3.2)
spr3_layout = spr3.Layout()
spr4 = my_dc(gap_inc_vec=[300, 200], sm_width=3.4)
spr4_layout = spr4.Layout()
spr5 = my_dc(gap_inc_vec=[300, 200], sm_width=3.6)
spr5_layout = spr5.Layout()
spr6 = my_dc(gap_inc_vec=[300, 200], sm_width=3.8)
spr6_layout = spr6.Layout()
spr7 = my_dc(gap_inc_vec=[300, 200], sm_width=4.0)
spr7_layout = spr7.Layout()
spr8 = my_dc(gap_inc_vec=[300, 200], sm_width=4.2)
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
pr_layout = pr.Layout(child_transformations={"dc1": (0, 0),
                                             "dc2": i3.VMirror(-2000) + i3.Translation((0, 4000)),
                                             "dc3": (0, 8500),
                                             "dc4": i3.VMirror(-2000) + i3.Translation((0, 12500)),
                                             "dc5": (0, 17000),
                                             "dc6": i3.VMirror(-2000) + i3.Translation((0, 21000)),
                                             "dc7": (0, 25500),
                                             "dc8": i3.VMirror(-2000) + i3.Translation((0, 29500))
                                             })
# pr_layout.visualize()
pr_layout.write_gdsii("spiral.gds")
