from technologies import silicon_photonics
from picazzo3.traces.wire_wg.trace import WireWaveguideTemplate
from picazzo3.routing.place_route import PlaceAndAutoRoute
import ipkiss3.all as i3
from picazzo3.container.transition_ports import AutoTransitionPorts


class Lspiral(PlaceAndAutoRoute):
    rectV_list = i3.ChildCellListProperty(default=[])
    rectH_list = i3.ChildCellListProperty(default=[])
    gap_inc_vec = i3.ListProperty(default=[], doc="Length of MMI")
    gap_inc_vec2 = i3.ListProperty(default=[], doc="length of 12mmi")
    WG1 = i3.ChildCellProperty(doc="", locked=True)
    WG2 = i3.ChildCellProperty()
    wg_t1 = i3.WaveguideTemplateProperty(doc="board WG")
    wg_t2 = i3.WaveguideTemplateProperty(doc="change WG")
    # mmi_trace_template = i3.WaveguideTemplateProperty()
    # mmi_access_template = i3.WaveguideTemplateProperty()
    width = i3.PositiveNumberProperty(doc="width of ports", default=15)
    # cleave = i3.PositiveNumberProperty(doc="tolerance", default=150)
    offset = i3.NumberProperty(doc="count", default=0)

    def _default_wg_t1(self):
        wg_t1 = WireWaveguideTemplate(name="port20")
        wg_t1.Layout(core_width=20,
                     cladding_width=20 + 2 * 12.0,
                     )
        return wg_t1

    def _default_wg_t2(self):
        wg_t2 = WireWaveguideTemplate(name="port_{}_{}".format(str(self.width), str(self.offset)))
        wg_t2.Layout(core_width=self.width,
                     cladding_width=self.width + 2 * 12.0,
                     )
        return wg_t2

    def _default_trace_template(self):
        wg_sm = WireWaveguideTemplate(name="sm_template")
        wg_sm.Layout(core_width=3.8, cladding_width=3.8 + 2 * 12.0)
        return wg_sm

    def _default_WG1(self):
        WG1 = i3.Waveguide(name="straight{}".format(str(self.width)), trace_template=self.wg_t1)
        WG1.Layout(shape=[(-200.0, 0.0), (600.0, 0.0)])
        return WG1

    def _default_WG2(self):
        Port = AutoTransitionPorts(
            name="ports{}".format(str(self.width)),
            contents=self.WG1,
            port_labels=["out"],
            trace_template=self.wg_t2)
        Port.Layout(transition_length=300)  # .visualize(annotate=True)
        return Port

    # def _default_mmi_trace_template(self):
    #     mmi_trace_template = WireWaveguideTemplate(name="MMI_tt")
    #     mmi_trace_template.Layout(core_width=20.0, cladding_width=20.0 + 2 * 12)  # MMI_width
    #     return mmi_trace_template
    #
    # def _default_mmi_access_template(self):
    #     mmi_access_template = WireWaveguideTemplate(name="MMI_at")
    #     mmi_access_template.Layout(core_width=9.0, cladding_width=9.0 + 2 * 12)
    #     return mmi_access_template

    def _default_rectH_list(self):

        MMI22_list = []
        for l in range(0,5,1):

            cell = i3.Waveguide(name="rectH{}_{}".format(str(l),str(self.offset)),
                               trace_template=self.wg_t2)
            cell.Layout(shape=[(0.0, 0.0), (17000-4000*l, 0.0)])
            # cell = i3.Waveguide(name="rectV{}".format(str(l)),
            #                     trace_template=self.wg_t2)
            # cell.Layout(shape=[(18000 - 4000 * l, 0.0), (0.0, 0.0)])

            MMI22_list.append(cell)

        return MMI22_list

    def _default_rectV_list(self):
        print '____________ MMI 2x2 ______________'
        MMI22_list2 = []
        for l in range(0,5,1):

            # cell = i3.Waveguide(name="rectH{}".format(str(l)),
            #                    trace_template=self.wg_t2)
            # cell.Layout(shape=[(0.0, 0.0), (18000-4000*l, 0.0)])
            cell = i3.Waveguide(name="rectV{}_{}".format(str(l),str(self.offset)),
                                trace_template=self.wg_t2)
            cell.Layout(shape=[(0.0, 0.0), (0.0, -1000-4000*l)])

            MMI22_list2.append(cell)

        return MMI22_list2

    def _default_child_cells(self):
        child_cells = dict()
        for counter in range(0, 5, 1):
            print counter
            # child_cells['straight' + str(counter)] = self.WG1
            child_cells['taperH' + str(counter)] = self.WG2
            child_cells['taperV' + str(counter)] = self.WG2

        for counter, child in enumerate(self.rectH_list):
            print 'child number' + str(counter)
            child_cells['recH' + str(counter)] = child
            print 'child name ' + str(child.name)

        for counter, child in enumerate(self.rectV_list):
            print 'child number' + str(counter)
            child_cells['recV' + str(counter)] = child
            print 'child name ' + str(child.name)

        return child_cells

    def _default_links(self):
        links = [
            ("recH0:out", "recV4:out"),
            ("recH1:out", "recV3:out"),
            ("recH2:out", "recV2:out"),
            ("recH3:out", "recV1:out"),
            ("recH4:out", "recV0:out"),



        ]
        return links

    class Layout(PlaceAndAutoRoute.Layout):

        def _default_child_transformations(self):
            trans = dict()
            column = 4000
            # trans['ring0'] = (600, 0)
            # trans['ring1'] = (600, 1 * column)
            # trans['ring2'] = (600, 2 * column)
            # # trans['ring3'] = (1300, 8000 + 2 * column )

            for i in range(0,5,1):
                trans["taperH{}".format(i)]=(0,column*i+100*self.offset)
                trans["taperV{}".format(i)] = i3.Rotation(rotation=-90)+i3.Translation((4000+column * i-100*self.offset, 20000))
                trans["recH{}".format(i)] = (900, column * i+100*self.offset)
                trans["recV{}".format(i)] = (4000+column * i-100*self.offset, 20000-900)
            # trans["taper0"] = (0, 0)
            # trans["taper1"] = i3.HMirror(0) + i3.Translation((2500, -1500))
            # trans["taper2"] = i3.HMirror(0) + i3.Translation((2500, 1500))
            #
            # trans["taper3"] = (0, 1 * column)
            # trans["taper4"] = i3.HMirror(0) + i3.Translation((2500, -1500 + 1 * column))
            #
            # trans["taper5"] = i3.HMirror(0) + i3.Translation((2500, 1500 + 1 * column))
            #
            # trans["taper6"] = (0, 2 * column)
            # trans["taper7"] = i3.HMirror(0) + i3.Translation((2500, -1500 + 2 * column))
            # trans["taper8"] = i3.HMirror(0) + i3.Translation((2500, 1500 + 2 * column))
            #
            # trans["taper9"] = (0, 3800 + 2 * column)
            #
            # trans["taper10"] = i3.HMirror(0) + i3.Translation((2500, -1500 + 3 * column))
            # # trans["taper11"] = i3.HMirror(0) + i3.Translation((3000, 6500+ 2 * column))
            # # trans["taper12"] = i3.HMirror(0) + i3.Translation((3000, 9500+ 2 * column))

            return trans

        def _default_bend_radius(self):
            bend_radius = 500
            return bend_radius

        def _generate_elements(self, elems):


            for i in range(0, 5, 1):
                elems += i3.PolygonText(layer=i3.TECH.PPLAYER.WG.TEXT,
                                        text="WITDH={}_length={}*2_R=500".format(str(self.width), 17000-4000*i),
                                        coordinate=(900, 55+ 4000 * i+100*self.offset),
                                        font=2,
                                        height=20.0,
                                        )
                for j in range(0,13,1):
                    elems += i3.PolygonText(layer=i3.TECH.PPLAYER.WG.TEXT,
                                            text="{}_{}".format(str(i),str(j)),
                                            coordinate=(550, 63 + 4000 * i +100*j),
                                            font=2,
                                            height=30.0,
                                            )
                    elems += i3.PolygonText(layer=i3.TECH.PPLAYER.WG.TEXT,
                                            text="{}_{}".format(str(i), str(j)),
                                            # coordinate=(),
                                            font=2,
                                            height=30.0,
                                            transformation=i3.Rotation(rotation=-90)+i3.Translation((20000-4000 * i -100*j+63, 20000-550)),
                                            )
            for i in range (0,6,1):
                elems += i3.Rectangle(layer=i3.TECH.PPLAYER.WG.TEXT,
                                      center=(100, 4000 * i-1000+700),
                                      box_size=(100, 100))
                elems += i3.Rectangle(layer=i3.TECH.PPLAYER.WG.TEXT,
                                      center=(300, 4000 * i-1000+700),
                                      box_size=(100, 100))
                elems += i3.Rectangle(layer=i3.TECH.PPLAYER.WG.TEXT,
                                      center=(4000 * i +300,19700),
                                      box_size=(100, 100))
                elems += i3.Rectangle(layer=i3.TECH.PPLAYER.WG.TEXT,
                                      center=(4000 * i +300,19900),
                                      box_size=(100, 100))
            elems += i3.Rectangle(layer=i3.TECH.PPLAYER.WG.TEXT,
                                  center=(100, 19900),
                                  box_size=(100, 100))
            elems += i3.Rectangle(layer=i3.TECH.PPLAYER.WG.TEXT,
                                  center=(-100, 19900),
                                  box_size=(100, 100))
            elems += i3.Rectangle(layer=i3.TECH.PPLAYER.WG.TEXT,
                                  center=(500, 19900),
                                  box_size=(100, 100))
            elems += i3.Rectangle(layer=i3.TECH.PPLAYER.WG.TEXT,
                                  center=(100, 19500),
                                  box_size=(100, 100))
            elems += i3.Rectangle(layer=i3.TECH.PPLAYER.WG.TEXT,
                                  center=(100, 20100),
                                  box_size=(100, 100))
            elems += i3.Rectangle(layer=i3.TECH.PPLAYER.WG.TEXT,
                                  center=(-100, -500),
                                  box_size=(100, 100))
            elems += i3.Rectangle(layer=i3.TECH.PPLAYER.WG.TEXT,
                                  center=(100, -500),
                                  box_size=(100, 100))
            elems += i3.Rectangle(layer=i3.TECH.PPLAYER.WG.TEXT,
                                  center=(300, -500),
                                  box_size=(100, 100))
            elems += i3.Rectangle(layer=i3.TECH.PPLAYER.WG.TEXT,
                                  center=(500, -500),
                                  box_size=(100, 100))
            elems += i3.Rectangle(layer=i3.TECH.PPLAYER.WG.TEXT,
                                  center=(20500, 19500),
                                  box_size=(100, 100))
            elems += i3.Rectangle(layer=i3.TECH.PPLAYER.WG.TEXT,
                                  center=(20500, 19700),
                                  box_size=(100, 100))
            elems += i3.Rectangle(layer=i3.TECH.PPLAYER.WG.TEXT,
                                  center=(20500, 19900),
                                  box_size=(100, 100))
            elems += i3.Rectangle(layer=i3.TECH.PPLAYER.WG.TEXT,
                                  center=(20500, 20100),
                                  box_size=(100, 100))

            return elems

dc_20 = Lspiral(width=20, name="ring0",offset=0)
# dc_20_layout.visualize(annotate=True)
# dc_20_layout.write_gdsii("lspiral.gds")
dc_17 = Lspiral(width=17, name="ring1", offset=1)
dc_14 = Lspiral(width=14, name="ring2", offset=2)
dc_11 = Lspiral(width=11, name="ring3", offset=3)
dc_9 = Lspiral(width=9, name="ring4", offset=4)
dc_7 = Lspiral(width=7, name="ring5", offset=5)
dc_5 = Lspiral(width=5, name="ring6", offset=6)
dc_46 = Lspiral(width=4.6, name="ring7", offset=7)
dc_42 = Lspiral(width=4.2, name="ring8", offset=8)
dc_38 = Lspiral(width=3.8, name="ring9", offset=9)
dc_34 = Lspiral(width=3.4, name="ring10", offset=10)
dc_30 = Lspiral(width=3.0, name="ring11", offset=11)
dc_26 = Lspiral(width=2.6, name="ring12", offset=12)

pr = PlaceAndAutoRoute(
    child_cells={
        "dc0": dc_20,
        "dc1": dc_17,
        "dc2": dc_14,
        "dc3": dc_11,
        "dc4": dc_9,
        "dc5": dc_7,
        "dc6": dc_5,
        "dc7": dc_46,
        "dc8": dc_42,
        "dc9": dc_38,
        "dc10": dc_34,
        "dc11": dc_30,
        "dc12": dc_26,

    }


)
pr_layout = pr.Layout()
# pr_layout.visualize()
pr_layout.write_gdsii("lspiral.gds")
