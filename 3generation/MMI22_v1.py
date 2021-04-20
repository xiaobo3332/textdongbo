from technologies import silicon_photonics
from picazzo3.traces.wire_wg.trace import WireWaveguideTemplate
from picazzo3.routing.place_route import PlaceAndAutoRoute
from picazzo3.routing.place_route import PlaceComponents
import ipkiss3.all as i3
from picazzo3.container.transition_ports import AutoTransitionPorts
from picazzo3.filters.mmi.cell import MMI2x2Tapered
from MMI2112 import MMI2112
from picazzo3.wg.dircoup import SBendDirectionalCoupler

from dicingmarkers import dicingMarker
from label import label
from edge import edge


class my_dc(PlaceAndAutoRoute):
    DC_list = i3.ChildCellListProperty(default=[])
    MMI_list = i3.ChildCellListProperty(default=[])
    gap_inc_vec = i3.ListProperty(default=[], doc="Length of MMI")
    length_inc_vec = i3.ListProperty(default=[], doc="length of MMI2112")
    WG1 = i3.ChildCellProperty(doc="", locked=True)
    WG2 = i3.ChildCellProperty()
    WG3 = i3.ChildCellProperty(doc="dummy SM waveguide")  # define this to guide route
    wg_t1 = i3.WaveguideTemplateProperty(doc="board WG")
    wg_dc = i3.WaveguideTemplateProperty(doc="dc WG")
    wg_dc2 = i3.WaveguideTemplateProperty(doc="dc WG2")
    wg_dc3 = i3.WaveguideTemplateProperty(doc="dc WG3")
    mmi_trace_template = i3.WaveguideTemplateProperty()
    mmi_access_template = i3.WaveguideTemplateProperty()
    width = i3.PositiveNumberProperty(doc="width of ports", default=15)
    dc_length = i3.PositiveNumberProperty(doc="length of DC", default=888)

    def _default_wg_t1(self):
        wg_t1 = WireWaveguideTemplate(name="port_{}".format(str(self.width)))
        wg_t1.Layout(core_width=self.width,
                     cladding_width=self.width + 2 * 12.0,
                     )
        return wg_t1

    def _default_wg_dc(self):
        wg_t1 = WireWaveguideTemplate(name="dca")
        wg_t1.Layout(core_width=2.8,
                     cladding_width=2.8 + 2 * 12.0,
                     )
        return wg_t1

    def _default_wg_dc2(self):
        wg_t1 = WireWaveguideTemplate(name="dcb")
        wg_t1.Layout(core_width=2.5,
                     cladding_width=2.5 + 2 * 12.0,
                     )
        return wg_t1

    def _default_wg_dc3(self):
        wg_t1 = WireWaveguideTemplate(name="dcc")
        wg_t1.Layout(core_width=2.2,
                     cladding_width=2.2 + 2 * 12.0,
                     )
        return wg_t1

    def _default_trace_template(self):
        wg_sm = WireWaveguideTemplate(name="sm_template")
        wg_sm.Layout(core_width=3.8, cladding_width=3.8 + 2 * 12.0)
        return wg_sm

    def _default_WG1(self):
        wg1 = i3.Waveguide(name="straight{}".format(str(self.width)), trace_template=self.wg_t1)
        wg1.Layout(shape=[(0.0, 0.0), (300.0, 0.0)])
        return wg1

    def _default_WG3(self):
        wg3 = i3.Waveguide(name="route", trace_template=self.trace_template)
        wg3.Layout(shape=[(0.0, 0.0), (1.0, 0.0)])
        return wg3

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

            cell = MMI2x2Tapered(mmi_trace_template=self.mmi_trace_template,
                                 input_trace_template=self.mmi_access_template,
                                 output_trace_template=self.mmi_access_template,
                                 trace_template=self.trace_template,
                                 )

            cell.Layout(name="MMI22_l_{}".format(str(self.gap_inc_vec[l])), transition_length=200.0,
                        length=self.gap_inc_vec[l], trace_spacing=11.0
                        )

            MMI22_list.append(cell)

            print 'cell name ' + str(cell.name)
            print '__________________________'

        return MMI22_list

    def _default_MMI_list(self):
        print '____________ MMI 2112 ______________'
        MMI2112_list = []

        for l, dl in enumerate(self.length_inc_vec):
            print 'length number ' + str(l)
            print 'dl ' + str(dl)

            cell = MMI2112()

            cell.Layout(name="MMI2112_l_{}".format(str(self.length_inc_vec[l])),
                        length=self.length_inc_vec[l]
                        )

            MMI2112_list.append(cell)
            print 'cell name ' + str(cell.name)

        return MMI2112_list

    def _default_child_cells(self):
        child_cells = dict()
        for counter in range(0, 22, 1):  # Routing dummy
            print counter
            child_cells['straight1' + str(counter)] = self.WG3

        for counter in range(0, 24, 1):
            child_cells['taper_in' + str(counter)] = self.WG2

        for counter in range(0, 24, 1):
            # child_cells['straight2' + str(counter)] = self.WG3
            child_cells['taper_out' + str(counter)] = self.WG2

        for counter in range(0, 22, 1):  # Routing dummy
            child_cells['straight2' + str(counter)] = self.WG3

        for counter, child in enumerate(self.DC_list):
            print 'child number' + str(counter)
            child_cells['ring' + str(counter)] = child
            print 'child name ' + str(child.name)
            print child

        for counter, child in enumerate(self.MMI_list):
            print 'child number' + str(counter)
            child_cells['mmi' + str(counter)] = child
            print 'child name ' + str(child.name)
            print child

        child = SBendDirectionalCoupler(name="dc3", trace_template1=self.wg_dc3,
                                        coupler_length=self.dc_length)
        child.Layout(coupler_spacing=2 + 2.2,
                     straight_after_bend=50,
                     # bend_angle=30.0,
                     bend_angles1=(20, 20),
                     bend_angles2=(40, 40),
                     bend_radius=100
                     )
        child_cells['dc3'] = child

        child = SBendDirectionalCoupler(name="dc2", trace_template1=self.wg_dc2,
                                        coupler_length=self.dc_length)
        child.Layout(coupler_spacing=2 + 2.5,
                     straight_after_bend=50,
                     # bend_angle=30.0,
                     bend_angles1=(20, 20),
                     bend_angles2=(40, 40),
                     bend_radius=100,
                     # manhattan=True,
                     )
        child_cells['dc2'] = child

        child = SBendDirectionalCoupler(name="dc1", trace_template1=self.wg_dc,
                                        coupler_length=self.dc_length)
        child.Layout(coupler_spacing=2 + 2.8,
                     straight_after_bend=50,
                     # bend_angle=30.0,
                     bend_angles1=(20, 20),
                     bend_angles2=(40, 40),
                     bend_radius=100,
                     # manhattan=True,
                     )
        child_cells['dc1'] = child

        child = SBendDirectionalCoupler(name="dc4", trace_template1=self.trace_template,
                                        coupler_length=923)
        child.Layout(coupler_spacing=100 + 3.8,
                     straight_after_bend=1150,
                     # bend_angle=30.0,
                     bend_angles1=(1, 1),
                     bend_angles2=(40, 40),
                     bend_radius=100
                     )
        child_cells['dc4'] = child

        return child_cells

    def _default_links(self):
        links = []
        for counter in range(0, 10, 1):
            # in_port = "Spiral{}:in".format(counter)
            in_port = "taper_in{}:out".format(counter)
            # links.append((in_port, out_port))
            # in_port = "Spiral{}:out".format(counter)
            out_port = "straight1{}:in".format(counter)
            links.append((in_port, out_port))

            in_port = "taper_out{}:out".format(counter)
            # links.append((in_port, out_port))
            # in_port = "Spiral{}:out".format(counter)
            out_port = "straight2{}:out".format(counter)
            links.append((in_port, out_port))

            # for counter in range(0, 11, 1):
            if counter % 2 == 0:
                i_port = "straight1{}:out".format(counter)
                o_port = "ring{}:in1".format(counter // 2)
                links.append((i_port, o_port))
                i_port = "straight2{}:in".format(counter)
                o_port = "ring{}:out1".format(counter // 2)
                links.append((i_port, o_port))
            else:
                ii_port = "straight1{}:out".format(counter)
                oo_port = "ring{}:in2".format(counter // 2)
                links.append((ii_port, oo_port))

                ii_port = "straight2{}:in".format(counter)
                oo_port = "ring{}:out2".format(counter // 2)
                links.append((ii_port, oo_port))

        for counter in range(10, 16, 1):
            # in_port = "Spiral{}:in".format(counter)
            in_port = "taper_in{}:out".format(counter)
            # links.append((in_port, out_port))
            # in_port = "Spiral{}:out".format(counter)
            out_port = "straight1{}:in".format(counter)
            links.append((in_port, out_port))

            in_port = "taper_out{}:out".format(counter)
            # links.append((in_port, out_port))
            # in_port = "Spiral{}:out".format(counter)
            out_port = "straight2{}:out".format(counter)
            links.append((in_port, out_port))

            if counter % 2 == 0:
                i_port = "straight1{}:out".format(counter)
                o_port = "mmi{}:narrow_in".format((counter - 10) // 2)
                links.append((i_port, o_port))
                i_port = "straight2{}:in".format(counter)
                o_port = "mmi{}:MMI1a_out1".format((counter - 10) // 2)
                links.append((i_port, o_port))
            else:
                # ii_port = "straight1{}:out".format(counter)
                # oo_port = "mmi{}:MMI1b_in2".format((counter - 10) // 2)
                # links.append((ii_port, oo_port))

                ii_port = "straight2{}:in".format(counter)
                oo_port = "mmi{}:MMI1a_out2".format((counter - 10) // 2)
                links.append((ii_port, oo_port))

        for counter in range(16, 22, 1):
            # in_port = "Spiral{}:in".format(counter)
            in_port = "taper_in{}:out".format(counter)
            # links.append((in_port, out_port))
            # in_port = "Spiral{}:out".format(counter)
            out_port = "straight1{}:in".format(counter)
            links.append((in_port, out_port))

            in_port = "taper_out{}:out".format(counter)
            # links.append((in_port, out_port))
            # in_port = "Spiral{}:out".format(counter)
            out_port = "straight2{}:out".format(counter)
            links.append((in_port, out_port))

            if counter % 2 == 0:
                i_port = "straight1{}:out".format(counter)
                o_port = "dc{}:in1".format((counter - 16) // 2 + 1)
                links.append((i_port, o_port))
                i_port = "straight2{}:in".format(counter)
                o_port = "dc{}:out1".format((counter - 16) // 2 + 1)
                links.append((i_port, o_port))
            else:
                ii_port = "straight1{}:out".format(counter)
                oo_port = "dc{}:in2".format((counter - 16) // 2 + 1)
                links.append((ii_port, oo_port))

                ii_port = "straight2{}:in".format(counter)
                oo_port = "dc{}:out2".format((counter - 16) // 2 + 1)
                links.append((ii_port, oo_port))

        # links.append(("taper_in16:out", "dc1:in1")),
        # links.append(("taper_in17:out", "dc1:in2")),
        # links.append(("taper_out16:out", "dc1:out1")),
        # links.append(("taper_out17:out", "dc1:out2")),
        # links.append(("taper_in18:out", "dc2:in1")),
        # links.append(("taper_in19:out", "dc2:in2")),
        # links.append(("taper_out18:out", "dc2:out1")),
        # links.append(("taper_out19:out", "dc2:out2")),
        # links.append(("taper_in20:out", "dc3:in1")),
        # links.append(("taper_in21:out", "dc3:in2")),
        # links.append(("taper_out20:out", "dc3:out1")),
        # links.append(("taper_out21:out", "dc3:out2")),
        links.append(("taper_in22:out", "dc4:in1")),
        links.append(("taper_in23:out", "dc4:in2")),
        links.append(("taper_out22:out", "dc4:out1")),
        links.append(("taper_out23:out", "dc4:out2")),
        # links.append(
        #     ("taper_in0:out", "ring0:in2"),
        #     ("taper_in1:out", "ring0:in1"),
        #     # ("taper_in2:out", "ring0:out2"),
        #     # ("taper_in3:out", "ring0:out1"),
        #
        #     ("taper_in2:out", "ring1:in2"),
        #     ("taper_in3:out", "ring1:in1"),
        #     # ("taper6:out", "ring1:out2"),
        #     # ("taper7:out", "ring1:out1"),
        #     #
        #     ("taper_in4:out", "ring2:in2"),
        #     ("taper_in5:out", "ring2:in1"),
        #     # ("taper10:out", "ring2:out2"),
        #     # ("taper11:out", "ring2:out1"),
        #     ("taper_in6:out", "ring3:in2"),
        #     ("taper_in7:out", "ring3:in1"),
        #     ("taper_in8:out", "ring4:in2"),
        #     ("taper_in9:out", "ring4:in1"),
        #
        # )
        return links

    class Layout(PlaceAndAutoRoute.Layout):

        def _default_child_transformations(self):
            trans = dict()
            column = 150
            # a = self.cell.mmi1_21.get_default_view(i3.LayoutView).ports['out'].x
            for counter in range(0, 24, 1):
                trans['taper_in' + str(counter)] = i3.Translation(
                    translation=(0, counter * column))
                trans['taper_out' + str(counter)] = i3.HMirror(0) + i3.Translation(
                    translation=(6200, 1000 + counter * column))
                # trans['straight1' + str(counter)] = i3.Translation(
                #     translation=(1490 - counter * 30, 1670 + counter * 150), rotation=90)
                # trans['straight2']

            # trans["dircoup1"] = (1650, 0)
            # trans["dircoup2"] = (4950, 0)
            # trans['mzi_22_22_0'] = (0, 0)
            for counter in range(0, 5, 1):
                trans['ring' + str(counter)] = i3.Translation(translation=(3000, 5000 + counter * column / 1.5))

            for counter in range(0, 3, 1):
                trans['mmi' + str(counter)] = i3.Translation(translation=(3000, 5500 + counter * column / 1.5))

            trans['dc1'] = i3.Translation((3000 + 200, 5800))
            trans['dc2'] = i3.Translation((3000 + 200, 5950))
            trans['dc3'] = i3.Translation((3000 + 200, 6100))
            trans['dc4'] = i3.Translation((3000 + 200, 6300))

            for counter, child in enumerate(self.DC_list):
                a = (child.ports['in1'].x, child.ports['in1'].y)
                b = (child.ports['in2'].x, child.ports['in2'].y)
                c = (child.ports['out1'].x, child.ports['out1'].y)
                d = (child.ports['out2'].x, child.ports['out2'].y)
                n = counter * 2
                m = counter * 2 + 1
                trans['straight1' + str(n)] = i3.Translation(translation=a) + i3.Translation(
                    translation=(3000, 5000 + counter * column / 1.5)) + i3.Translation((-2 - 50 * n, 0))
                trans['straight1' + str(m)] = i3.Translation(translation=b) + i3.Translation(
                    translation=(3000, 5000 + counter * column / 1.5)) + i3.Translation((-2 - 50 * m, 0))
                trans['straight2' + str(n)] = i3.Translation(translation=c) + i3.Translation(
                    translation=(3000, 5000 + counter * column / 1.5)) + i3.Translation((2 + 50 * n, 0))
                trans['straight2' + str(m)] = i3.Translation(translation=d) + i3.Translation(
                    translation=(3000, 5000 + counter * column / 1.5)) + i3.Translation((2 + 50 * m, 0))
                print a, b

            for counter, child in enumerate(self.MMI_list):
                # a = (child.ports['MMI1b_in1'].x, child.ports['MMI1b_in1'].y)
                a = (child.ports['narrow_in'].x, child.ports['narrow_in'].y)
                # b = (child.ports['MMI1b_in2'].x, child.ports['MMI1b_in2'].y)
                c = (child.ports['MMI1a_out1'].x, child.ports['MMI1a_out1'].y)
                d = (child.ports['MMI1a_out2'].x, child.ports['MMI1a_out2'].y)
                n = 10 + counter * 2
                m = 10 + counter * 2 + 1
                trans['straight1' + str(n)] = i3.Translation(translation=a) + i3.Translation(
                    translation=(3000, 5500 + counter * column / 1.5)) + i3.Translation((-2 - 50 * n - 250, 0))
                trans['straight1' + str(m)] = i3.Translation(translation=a) + i3.Translation(
                    translation=(3000, 5500 + counter * column / 1.5)) + i3.Translation((-2 - 50 * m - 250, 20))
                trans['straight2' + str(n)] = i3.Translation(translation=c) + i3.Translation(
                    translation=(3000, 5500 + counter * column / 1.5)) + i3.Translation((2 + 50 * n + 50, 0))
                trans['straight2' + str(m)] = i3.Translation(translation=d) + i3.Translation(
                    translation=(3000, 5500 + counter * column / 1.5)) + i3.Translation((2 + 50 * m + 50, 0))
                # print a, b

            for counter in range(16, 18, 1):
                a = (self.child_cells['dc1'].get_default_view(i3.LayoutView).ports['in1'].x,
                     self.child_cells['dc1'].get_default_view(i3.LayoutView).ports['in1'].y)
                # a = (self.child_cells['dc1'].ports['in1'].x, self.child_cells['dc1'].ports['in1'].y)

                b = (self.child_cells['dc1'].get_default_view(i3.LayoutView).ports['in2'].x,
                     self.child_cells['dc1'].get_default_view(i3.LayoutView).ports['in2'].y)
                c = (self.child_cells['dc1'].get_default_view(i3.LayoutView).ports['out1'].x,
                     self.child_cells['dc1'].get_default_view(i3.LayoutView).ports['out1'].y)
                d = (self.child_cells['dc1'].get_default_view(i3.LayoutView).ports['out2'].x,
                     self.child_cells['dc1'].get_default_view(i3.LayoutView).ports['out2'].y)
                # print a, b
                nb = int(counter / 2 - 8)
                # n = 10 + counter * 2
                # m = 10 + counter * 2 + 1
                if counter % 2 == 0:
                    trans['straight1' + str(counter)] = i3.Translation(translation=a) + i3.Translation(
                        translation=(3200, 5800 + 150 * nb)) + i3.Translation((-2 - 100 * nb - 700, 0))
                    trans['straight2' + str(counter)] = i3.Translation(translation=c) + i3.Translation(
                        translation=(3200, 5800 + 150 * nb)) + i3.Translation((2 + 100 * nb + 700, 0))
                else:
                    trans['straight1' + str(counter)] = i3.Translation(translation=b) + i3.Translation(
                        translation=(3200, 5800 + 150 * nb)) + i3.Translation((-2 - 100 * nb - 700, 0))

                    trans['straight2' + str(counter)] = i3.Translation(translation=d) + i3.Translation(
                        translation=(3200, 5800 + 150 * nb)) + i3.Translation((2 + 100 * nb + 700, 0))

            # return trans

            for counter in range(18, 20, 1):
                a = (self.child_cells['dc2'].get_default_view(i3.LayoutView).ports['in1'].x,
                     self.child_cells['dc2'].get_default_view(i3.LayoutView).ports['in1'].y)
                # a = (self.child_cells['dc1'].ports['in1'].x, self.child_cells['dc1'].ports['in1'].y)

                b = (self.child_cells['dc2'].get_default_view(i3.LayoutView).ports['in2'].x,
                     self.child_cells['dc2'].get_default_view(i3.LayoutView).ports['in2'].y)
                c = (self.child_cells['dc2'].get_default_view(i3.LayoutView).ports['out1'].x,
                     self.child_cells['dc2'].get_default_view(i3.LayoutView).ports['out1'].y)
                d = (self.child_cells['dc2'].get_default_view(i3.LayoutView).ports['out2'].x,
                     self.child_cells['dc2'].get_default_view(i3.LayoutView).ports['out2'].y)
                # print a, b
                nb = int(counter / 2 - 8)
                # n = 10 + counter * 2
                # m = 10 + counter * 2 + 1
                if counter % 2 == 0:
                    trans['straight1' + str(counter)] = i3.Translation(translation=a) + i3.Translation(
                        translation=(3200, 5800 + 150 * nb)) + i3.Translation((-2 - 100 * nb - 700, 0))
                    trans['straight2' + str(counter)] = i3.Translation(translation=c) + i3.Translation(
                        translation=(3200, 5800 + 150 * nb)) + i3.Translation((2 + 100 * nb + 700, 0))
                else:
                    trans['straight1' + str(counter)] = i3.Translation(translation=b) + i3.Translation(
                        translation=(3200, 5800 + 150 * nb)) + i3.Translation((-2 - 100 * nb - 700, 0))

                    trans['straight2' + str(counter)] = i3.Translation(translation=d) + i3.Translation(
                        translation=(3200, 5800 + 150 * nb)) + i3.Translation((2 + 100 * nb + 700, 0))

            # return trans

            for counter in range(20, 22, 1):
                a = (self.child_cells['dc3'].get_default_view(i3.LayoutView).ports['in1'].x,
                     self.child_cells['dc3'].get_default_view(i3.LayoutView).ports['in1'].y)
                # a = (self.child_cells['dc1'].ports['in1'].x, self.child_cells['dc1'].ports['in1'].y)

                b = (self.child_cells['dc3'].get_default_view(i3.LayoutView).ports['in2'].x,
                     self.child_cells['dc3'].get_default_view(i3.LayoutView).ports['in2'].y)
                c = (self.child_cells['dc3'].get_default_view(i3.LayoutView).ports['out1'].x,
                     self.child_cells['dc3'].get_default_view(i3.LayoutView).ports['out1'].y)
                d = (self.child_cells['dc3'].get_default_view(i3.LayoutView).ports['out2'].x,
                     self.child_cells['dc3'].get_default_view(i3.LayoutView).ports['out2'].y)
                # print a, b
                nb = int(counter / 2 - 8)
                # n = 10 + counter * 2
                # m = 10 + counter * 2 + 1
                if counter % 2 == 0:
                    trans['straight1' + str(counter)] = i3.Translation(translation=a) + i3.Translation(
                        translation=(3200, 5800 + 150 * nb)) + i3.Translation((-2 - 100 * nb - 700, 0))
                    trans['straight2' + str(counter)] = i3.Translation(translation=c) + i3.Translation(
                        translation=(3200, 5800 + 150 * nb)) + i3.Translation((2 + 100 * nb + 700, 0))
                else:
                    trans['straight1' + str(counter)] = i3.Translation(translation=b) + i3.Translation(
                        translation=(3200, 5800 + 150 * nb)) + i3.Translation((-2 - 100 * nb - 700, 0))

                    trans['straight2' + str(counter)] = i3.Translation(translation=d) + i3.Translation(
                        translation=(3200, 5800 + 150 * nb)) + i3.Translation((2 + 100 * nb + 700, 0))

            return trans

        def _default_bend_radius(self):
            bend_radius = 300
            return bend_radius

        def _generate_elements(self, elems):
            for counter in range(0, 24, 1):

                elems += i3.PolygonText(layer=i3.TECH.PPLAYER.WG.TEXT,
                                        text="{}".format(str(counter)),
                                        # coordinate=(1300.0, 100.0),
                                        # alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
                                        font=2,
                                        height=70.0,
                                        transformation=i3.Translation((5700, 1100 + 150 * counter))
                                        )
                if counter == 11 or counter == 13 or counter == 15:
                    continue
                elems += i3.PolygonText(layer=i3.TECH.PPLAYER.WG.TEXT,
                                        text="{}".format(str(counter)),
                                        # coordinate=(1300.0, 100.0),
                                        # alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
                                        font=2,
                                        height=70.0,
                                        transformation=i3.Translation((400, 100 + 150 * counter))
                                        )

            return elems


dc_10 = my_dc(gap_inc_vec=[382.0, 390.0, 398.0, 406.0, 414.0], length_inc_vec=[92, 97, 102], name="ring1", width=15.0,
              dc_length=888)
dc_10_layout = dc_10.Layout()
# dc_10_layout.visualize(annotate=True)
# dc_10_layout.write_gdsii("MMI22_v1.gds")

dc_15 = my_dc(gap_inc_vec=[420.0, 430.0, 440.0, 450.0, 460.0], length_inc_vec=[110, 120, 130], name="ring2", width=15.0,
              dc_length=908)
dc_15_layout = dc_15.Layout()
dc_20 = my_dc(gap_inc_vec=[378.0, 388.0, 398.0, 408.0, 418.0], length_inc_vec=[87, 97, 107], name="ring3", width=15.0,
              dc_length=928)
dc_20_layout = dc_20.Layout()

dcc_10 = my_dc(gap_inc_vec=[378.0, 388.0, 398.0, 408.0, 418.0], length_inc_vec=[87, 97, 107], name="ring4", width=20.0,
               dc_length=948)
dcc_10_layout = dcc_10.Layout()
dcc_15 = my_dc(gap_inc_vec=[470.0, 480.0, 490.0, 500.0, 505.0], length_inc_vec=[140, 150, 160], name="ring5",
               width=20.0, dc_length=968)
dcc_15_layout = dcc_15.Layout()
dcc_20 = my_dc(gap_inc_vec=[420.0, 430.0, 440.0, 450.0, 460.0], length_inc_vec=[110, 120, 130], name="ring6",
               width=20.0, dc_length=988)
dcc_20_layout = dcc_20.Layout()

marker = dicingMarker()
marker_layout = marker.Layout()

marker2 = label()
marker2_layout = marker2.Layout()

marker3 = edge()
marker3_layout = marker3.Layout()

pr = PlaceComponents(
    child_cells={
        "comp1": dc_10,
        "comp2": dc_15,
        "comp3": dc_20,
        "comp4": dcc_10,
        "comp5": dcc_15,
        "comp6": dcc_20,
        "marker1": marker,
        "marker2": marker2,
        "marker3": marker3,

    }
)
pr_layout = pr.Layout(child_transformations={"comp1": (0, 0),
                                             # "comp2": (6000, 0),
                                             "comp2": i3.HMirror() + i3.Translation((12400, 0)),
                                             "comp3": (12400, 0),
                                             "comp4": (0, 7500),
                                             "comp5": i3.HMirror() + i3.Translation((12400, 7500)),
                                             "comp6": (12400, 7500),
                                             "marker1": (0, 0),
                                             "marker2": (650, 3900),
                                             "marker3": (0,0),

                                             })
# pr_layout.visualize()
pr_layout.write_gdsii("MMI22_v5.gds")
