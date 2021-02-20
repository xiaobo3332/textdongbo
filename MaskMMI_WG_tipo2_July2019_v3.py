from technologies import silicon_photonics

import ipkiss3.all as i3

from picazzo3.traces.wire_wg.trace import WireWaveguideTemplate
from picazzo3.routing.place_route import PlaceAndAutoRoute
from picazzo3.filters.mmi.cell import MMI1x2Tapered
from picazzo3.filters.mmi.cell import MMI2x1Tapered
from picazzo3.filters.mmi.cell import MMI2x2Tapered
from picazzo3.filters.mzi import MZIWaveguides
from picazzo3.traces.wire_wg.trace import WireWaveguideTemplate
from ipkiss.geometry.shapes.spline import ShapeRoundAdiabaticSpline
from picazzo3.container.transition_ports import AutoTransitionPorts


class MZI_12_21(PlaceAndAutoRoute):
    _name_prefix = 'MZIs'

    delay_length = i3.PositiveNumberProperty(default=132.0, doc="Delay length used in the mzi")
    R = i3.PositiveNumberProperty(default=200, doc="Radius of curvature")
    # MMI12_list = i3.ChildCellListProperty(default=[])
    MMI12 = i3.ChildCellProperty(default=[])
    MMI21_list = i3.ChildCellListProperty(default=[])
    MMI22_list = i3.ChildCellListProperty(default=[])
    # MZI_12_21_list = i3.ChildCellListProperty(default=[])
    MZI_12_22_list = i3.ChildCellListProperty(default=[])
    MZI_22_22_list = i3.ChildCellListProperty(default=[])
    # MMI22_list = i3.ChildCellListProperty()
    wg_t = i3.TraceTemplateProperty(doc="trace template used")
    wg_t_MM = i3.TraceTemplateProperty(doc="Trace template used in the MM part")
    wg_t_port = i3.TraceTemplateProperty(doc="Trace template used in the ports")
    width_inc_vec = i3.ListProperty(default=[])
    length_inc_vec = i3.ListProperty(default=[])

    l_taper = i3.PositiveNumberProperty(default=200.0, doc="Length of the tapers")
    width = i3.PositiveNumberProperty(default=20.0, doc="width of MM")
    length_12 = i3.PositiveNumberProperty(default=110.0, doc="Length of MMI 1x2")
    length_22 = i3.PositiveNumberProperty(default=435.0, doc="Length of MMI 2x2")
    ts_12 = i3.PositiveNumberProperty(default=11.25, doc="trace spacing")
    # ts for 12 is 7.0 --> MM=5   ()    L12=39.0   L22=158.0
    # ts for 20 is 11 -->MM=9      (ts=11.25, MM8.75) L12=110.0, L22=435.0
    # ts for 30 is 16 -->MM=14     (ts=16.25, MM=13.75) L12=245.0, L22=980.0
    chip_length = i3.PositiveNumberProperty(default=10000.0, doc="Radius of curvature")
    Port = i3.ChildCellProperty(doc="Used for ports")
    tlport = i3.PositiveNumberProperty(default=200.0, doc="Transition legth to ports")
    couplingWG = i3.ChildCellProperty(doc="", locked=True)
    couplingWG_l = i3.PositiveNumberProperty(default=3000.0, doc="Length of the coupling WG ")
    tt_port = i3.TraceTemplateProperty(doc="Wide trace template used for the contacts")

    tipo = i3.PositiveNumberProperty(default=1, doc="type of out-couplers tipo==1, straight, tipo==2, 90  degree bend")

    # template for Autorute
    def _default_trace_template(self):
        return self.wg_t

    def _default_wg_t_MM(self):
        tt_w = WireWaveguideTemplate()
        tt_w.Layout(core_width=self.width,
                    cladding_width=self.width + 2 * 8,
                    )
        return tt_w

    def _default_wg_t_port(self):
        tt_w = WireWaveguideTemplate()
        tt_w.Layout(core_width=8.75,
                    cladding_width=8.75 + 2 * 8,
                    )
        return tt_w

    def _default_wg_t(self):
        tt_n = WireWaveguideTemplate()
        tt_n.Layout(core_width=3.3,
                    cladding_width=3.3 + 2 * 8,
                    )
        return tt_n

    def _default_tt_port(self):
        tt_port = WireWaveguideTemplate()
        tt_port.Layout(core_width=15.0, cladding_width=15.0 + 2 * 8)
        return tt_port

    def _default_couplingWG(self):
        rect = i3.Waveguide(trace_template=self.tt_port)
        rect.Layout(shape=[(0.0, 0.0), (self.couplingWG_l, 0.0)])
        return rect

    def _default_Port(self):
        Port = AutoTransitionPorts(contents=self.couplingWG,
                                   port_labels=["in"],
                                   trace_template=self.wg_t)
        layout_Port = Port.Layout(transition_length=self.tlport)   .visualize(annotate=True)
        return Port

    def _default_MMI12(self):
        mmi12 = MMI1x2Tapered(mmi_trace_template=self.wg_t_MM,
                              input_trace_template=self.wg_t_port,
                              output_trace_template=self.wg_t_port,
                              trace_template=self.wg_t,
                              name='MMI12_w_{}_L_{}'.format(self.width, self.length_12), )
        mmi12.Layout(transition_length=self.l_taper, length=self.length_12,
                     trace_spacing=self.ts_12)  # .visualize(annotate=True)

        return mmi12

    #################################################################################

    def _default_MMI22_list(self):
        print '____________ MMI 2x2 ______________'
        MMI22_list = []

        for l, dl in enumerate(self.length_inc_vec):
            print 'length number ' + str(l)
            print 'dl ' + str(dl)
            print 'MM length ' + str(self.length_22 + dl)
            cell = MMI2x2Tapered(mmi_trace_template=self.wg_t_MM,
                                 input_trace_template=self.wg_t_port,
                                 output_trace_template=self.wg_t_port,
                                 trace_template=self.wg_t,
                                 name='MMI22_w_' + str(self.width) + '_l_' + str(self.length_22 + dl))
            cell.Layout(transition_length=self.l_taper, length=self.length_22 + dl, trace_spacing=self.ts_12)

            MMI22_list.append(cell)

            print 'cell name ' + str(cell.name)
            print '__________________________'

        for w, dw in enumerate(self.width_inc_vec):
            MM_w = self.width + dw
            print 'width number ' + str(w)
            print 'dw ' + str(dw)
            print 'MM width ' + str(MM_w)
            wg_t_MM_w = WireWaveguideTemplate()
            wg_t_MM_w.Layout(core_width=MM_w,
                             cladding_width=MM_w + 2 * 8,
                             )

            cell = MMI2x2Tapered(mmi_trace_template=wg_t_MM_w,
                                 input_trace_template=self.wg_t_port,
                                 output_trace_template=self.wg_t_port,
                                 trace_template=self.wg_t,
                                 name='MMI22_w_' + str(self.width + dw) + '_l_' + str(self.length_22))
            cell.Layout(transition_length=self.l_taper, length=self.length_22,
                        trace_spacing=self.ts_12 + dw)  # .visualize(annotate=True)
            print cell
            MMI22_list.append(cell)

            print 'cell name ' + str(cell.name)
            print '__________________________'

        print 'last MMI22 done'
        print '_ _ _ _ _ _ _ _ _ _ _ _ _ '
        return MMI22_list

    def _default_MZI_12_22_list(self):
        print '____________ MZI_1x2_2x2 ______________'
        MZI_12_22_list = []
        counter = 1
        print '____________ MZI_1x2_2x2 list ______________'
        for i, m in enumerate(self.MMI22_list):
            print 'MZI number ' + str(counter)
            cell = MZIWaveguides(name='MZI_12_22:' + str(self.MMI12.name) + str(m.name),
                                 trace_template=self.wg_t,
                                 splitter=self.MMI12,
                                 combiner=m,
                                 splitter_port_names=['out1', 'out2'],
                                 combiner_port_names=['in1', 'in2'])
            cell.Layout(bend_radius=self.R, delay_length=self.delay_length)  # .visualize(annotate=True)
            MZI_12_22_list.append(cell)
            counter = counter + 1

            print 'splitter ' + cell.splitter.name
            print 'combiner ' + cell.combiner.name

            print cell.name
            print '__________________________'

        print "Last MMI_12_22 done"
        print '_ _ _ _ _ _ _ _ _ _ _ _ _ '
        return MZI_12_22_list

    def _default_MZI_22_22_list(self):
        print '____________ MZI_2x2_2x2 ______________'
        MZI_22_22_list = []
        counter = 1
        print '____________ MZI_2x2_2x2 list ______________'
        for i, m in enumerate(self.MMI22_list):
            print 'MZI number ' + str(counter)
            cell = MZIWaveguides(name='MZI_22_22:' + str(m.name),
                                 trace_template=self.wg_t,
                                 splitter=m,
                                 combiner=m,
                                 splitter_port_names=['out1', 'out2'],
                                 combiner_port_names=['in1', 'in2'])
            cell.Layout(bend_radius=self.R, delay_length=self.delay_length)  # .visualize(annotate=True)
            MZI_22_22_list.append(cell)
            counter = counter + 1

            print 'splitter ' + cell.splitter.name
            print 'combiner ' + cell.combiner.name

            print cell.name
            print '__________________________'

        print "Last MMI_22_22 done"
        print '_ _ _ _ _ _ _ _ _ _ _ _ _ '
        return MZI_22_22_list

    #################################################################################

    def _default_child_cells(self):
        print '____________ Child cells ______________'
        child_cells = {}

        for counter, child in enumerate(self.MZI_22_22_list):
            print 'child number' + str(counter)

            child_cells['mzi_22_22_' + str(counter)] = child
            child_cells['InPort1_' + str(counter)] = self.Port
            child_cells['OutPort1_' + str(counter)] = self.Port
            child_cells['InPort2_' + str(counter)] = self.Port
            child_cells['OutPort2_' + str(counter)] = self.Port
            print 'child name ' + str(child.name)
            print child

        #################
        for counter2, child in enumerate(self.MZI_12_22_list):
            print 'child number' + str(counter + 1 + counter2)

            child_cells['mzi_12_22_' + str(counter + 1 + counter2)] = child
            child_cells['InPort_' + str(counter + 1 + counter2)] = self.Port
            child_cells['OutPort1_' + str(counter + 1 + counter2)] = self.Port
            child_cells['OutPort2_' + str(counter + 1 + counter2)] = self.Port
            print 'child name ' + str(child.name)
            print child
            ###################

            print '__________________________'
        child_cells['InPortWG1'] = self.Port
        child_cells['OutPortWG1'] = self.Port
        child_cells['InPortWG2'] = self.Port
        child_cells['OutPortWG2'] = self.Port
        child_cells['InPortWG3'] = self.Port
        child_cells['OutPortWG3'] = self.Port

        print "Last child cell done"
        print '_ _ _ _ _ _ _ _ _ _ _ _ _ '
        return child_cells

    def _default_links(self):
    	links = []
    	for counter, child  in enumerate(self.MZI_22_22_list):
    		print counter
    		in_port = "InPort1_{}:in".format(counter)
    		print 'in_port', in_port
    		out_port = 'mzi_22_22_{}:splitter_in1'.format(counter)
    		print 'out_port', in_port
    		links.append((in_port, out_port))

    		in_port = "InPort2_{}:in".format(counter)
    		print 'in_port', in_port
    		out_port = 'mzi_22_22_{}:splitter_in2'.format(counter)
    		links.append((in_port, out_port))

    		out_port = "OutPort1_{}:in".format(counter)
    		in_port = 'mzi_22_22_{}:combiner_out1'.format(counter)
    		print 'in_port', in_port
    		links.append((in_port, out_port))

    		out_port = "OutPort2_{}:in".format(counter)
    		in_port = 'mzi_22_22_{}:combiner_out2'.format(counter)
    		print 'in_port', in_port
    		links.append((in_port, out_port))


    	for counter2, child  in enumerate(self.MZI_12_22_list):
    		out_port = "InPort_{}:in".format(counter+1+counter2)
    		in_port = 'mzi_12_22_{}:splitter_in'.format(counter+1+counter2)
    		links.append((in_port, out_port))

    		in_port = "OutPort1_{}:in".format(counter+1+counter2)
    		out_port = 'mzi_12_22_{}:combiner_out1'.format(counter+1+counter2)
    		links.append((in_port, out_port))

    		in_port = "OutPort2_{}:in".format(counter+1+counter2)
    		out_port = 'mzi_12_22_{}:combiner_out2'.format(counter+1+counter2)
    		links.append((in_port, out_port))
    	links.append(("InPortWG1:in", "OutPortWG1:in"))
    	links.append(("InPortWG2:in", "OutPortWG2:in"))
    	links.append(("InPortWG3:in", "OutPortWG3:in"))
    	return links

    class Layout(PlaceAndAutoRoute.Layout):

        def _default_bend_radius(self):
            return self.R

        def _default_start_straight(self):
            return 1.0

        print '____________ Layout mask ______________'

        def _default_child_transformations(self):
            d = {}
            a = 2.2
            for counter, child in enumerate(self.MZI_22_22_list):
                if self.tipo == 1:
                    d['mzi_22_22_' + str(counter)] = i3.Translation(
                        translation=((-1) ** counter * 2 * self.R, counter * 5 * self.R))
                    d['InPort1_' + str(counter)] = i3.HMirror() + i3.Translation(
                        translation=(-self.chip_length * 0.5, counter * 5 * self.R - 2.2 * self.R))
                    d['OutPort1_' + str(counter)] = i3.Rotation(rotation=90.0) + i3.Translation(
                        translation=(self.chip_length * 0.5, counter * 5 * self.R - 2.2 * self.R))
                    d['InPort2_' + str(counter)] = i3.HMirror() + i3.Translation(
                        translation=(-self.chip_length * 0.5, counter * 5 * self.R + 2.2 * self.R))
                    d['OutPort2_' + str(counter)] = i3.Rotation(rotation=90.0) + i3.Translation(
                        translation=(self.chip_length * 0.5, counter * 5 * self.R + 2.2 * self.R))
                    print 'transformation ' + str(counter) + ' is ' + str(d)
                if self.tipo == 2:
                    # l_coupling=self.child_cells['Coupler'].l_coupling
                    # radius=self.child_cells['Coupler'].local_bend_radius
                    print 'R= ', self.R
                    # print 'translation port: '

                    # For w=20
                    d['mzi_22_22_' + str(counter)] = i3.Translation(
                        translation=(counter * 850 + 1200 + 1000 + 200, -counter * 5 * self.R))
                    d['InPort1_' + str(counter)] = i3.HMirror() + i3.Translation(
                        translation=(-self.chip_length * 0.1, -5 * self.R * counter - a * self.R))
                    d['OutPort1_' + str(counter)] = i3.Rotation(rotation=90.0) + i3.Translation(translation=(
                    self.chip_length * 0.5 + counter * 50 + counter * 4 * self.R + a * self.R - 100,
                    self.couplingWG_l + self.R * a))
                    d['InPort2_' + str(counter)] = i3.HMirror() + i3.Translation(
                        translation=(-self.chip_length * 0.1, -5 * self.R * counter + a * self.R))
                    d['OutPort2_' + str(counter)] = i3.Rotation(rotation=90.0) + i3.Translation(translation=(
                    self.chip_length * 0.5 + counter * 50 + counter * 4 * self.R - 100, self.couplingWG_l + self.R * a))

                d['InPortWG1'] = i3.HMirror() + i3.Translation(translation=(-self.chip_length * 0.1, 1000.0))
                d['OutPortWG1'] = i3.Rotation(rotation=90.0) + i3.Translation(
                    translation=(self.chip_length * 0.5 - 500, self.couplingWG_l + self.R * a))
                d['InPortWG2'] = i3.HMirror() + i3.Translation(translation=(-self.chip_length * 0.1, -3400 + 670))
                d['OutPortWG2'] = i3.Rotation(rotation=90.0) + i3.Translation(
                    translation=(self.chip_length * 0.5 + 2500, self.couplingWG_l + self.R * a))
                d['InPortWG3'] = i3.HMirror() + i3.Translation(translation=(-self.chip_length * 0.1, -6500))
                d['OutPortWG3'] = i3.Rotation(rotation=90.0) + i3.Translation(
                    translation=(self.chip_length * 0.5 + 5600, self.couplingWG_l + self.R * a))

            ###for w=30
            # d['mzi_22_22_' + str(counter)] = i3.Translation(translation=(counter*850+1200+1000+200,-counter*5*self.R))
            # d['InPort1_'+ str(counter)] = i3.HMirror()+i3.Translation(translation=(-self.chip_length*0.1, -5*self.R*counter-a*self.R))
            # d['OutPort1_'+ str(counter)]= i3.Rotation(rotation=90.0)+i3.Translation(translation=(self.chip_length*0.5+1100+counter*50+counter*4*self.R+a*self.R-100, self.couplingWG_l+self.R*a))
            # d['InPort2_'+ str(counter)] = i3.HMirror()+i3.Translation(translation=(-self.chip_length*0.1, -5*self.R*counter+a*self.R))
            # d['OutPort2_'+ str(counter)]= i3.Rotation(rotation=90.0)+i3.Translation(translation=(self.chip_length*0.5+1100+counter*50+counter*4*self.R-100, self.couplingWG_l+self.R*a))

            # d['InPortWG1'] = i3.HMirror()+i3.Translation(translation=(-self.chip_length*0.1, 1000.0))
            # d['OutPortWG1']= i3.Rotation(rotation=90.0)+i3.Translation(translation=(self.chip_length*0.5-500+1200, self.couplingWG_l+self.R*a))
            # d['InPortWG2'] = i3.HMirror()+i3.Translation(translation=(-self.chip_length*0.1, -3400+670))
            # d['OutPortWG2']= i3.Rotation(rotation=90.0)+i3.Translation(translation=(self.chip_length*0.5+2500+1100, self.couplingWG_l+self.R*a))
            # d['InPortWG3'] = i3.HMirror()+i3.Translation(translation=(-self.chip_length*0.1, -6500))
            # d['OutPortWG3']= i3.Rotation(rotation=90.0)+i3.Translation(translation=(self.chip_length*0.5+5600+1400, self.couplingWG_l+self.R*a))
            ################
            for counter2, child in enumerate(self.MZI_12_22_list):
                if self.tipo == 1:
                    d['mzi_12_22_' + str(counter + 1 + counter2)] = i3.Translation(translation=(
                    (-1) ** counter2 * 2 * self.R - self.length_22 + counter * 50 + counter * 4 * self.R,
                    (counter + 1 + counter2) * 5 * self.R))
                    d['InPort_' + str(counter + 1 + counter2)] = i3.HMirror() + i3.Translation(
                        translation=(-self.chip_length * 0.5, (counter + 1 + counter2) * 5 * self.R))
                    d['OutPort1_' + str(counter + 1 + counter2)] = i3.Translation(translation=(
                    self.chip_length * 0.5 - self.bend_radius * counter * 0.2 - a * self.R - 550,
                    (counter + 1 + counter2) * 5 * self.R - 2.2 * self.R))
                    d['OutPort2_' + str(counter + 1 + counter2)] = i3.Translation(translation=(
                    self.chip_length * 0.5 - self.bend_radius * counter * 0.2 - 550,
                    (counter + 1 + counter2) * 5 * self.R + 2.2 * self.R))
                if self.tipo == 2:
                    # l_coupling=self.child_cells['Coupler'].l_coupling
                    # radius=self.child_cells['Coupler'].local_bend_radius
                    print 'R= ', self.R
                    a = 2.2
                    b = 500
                    d['mzi_12_22_' + str(counter + 1 + counter2)] = i3.Translation(translation=(
                    (counter + 2 + counter2) * 850 + 1200 + 200 + 580 + 500,
                    -(counter + 1 + counter2) * 5 * self.R - b))
                    d['InPort_' + str(counter + 1 + counter2)] = i3.HMirror() + i3.Translation(
                        translation=(-self.chip_length * 0.1, -(5 * self.R) * (counter + 1 + counter2) - b))
                    d['OutPort1_' + str(counter + 1 + counter2)] = i3.Rotation(rotation=90.0) + i3.Translation(
                        translation=(self.chip_length * 0.5 + (counter + 1 + counter2) * 50 + a * self.R + (
                                    counter + 1 + counter2) * 4 * self.R + b, self.couplingWG_l + self.R * a))
                    d['OutPort2_' + str(counter + 1 + counter2)] = i3.Rotation(rotation=90.0) + i3.Translation(
                        translation=(self.chip_length * 0.5 + (counter + 1 + counter2) * 50 + (
                                    counter + 1 + counter2) * 4 * self.R + b, self.couplingWG_l + self.R * a))

                # d['mzi_12_22_'+ str(counter+1+counter2)] = i3.Translation(translation=((counter+2+counter2)*850+1200+200+580+1000,-(counter+1+counter2)*5*self.R-b))
                # d['InPort_'+ str(counter+1+counter2)] = i3.HMirror()+i3.Translation(translation=(-self.chip_length*0.1, -(5*self.R)*(counter+1+counter2)-b))
                # d['OutPort1_'+ str(counter+1+counter2)]= i3.Rotation(rotation=90.0)+i3.Translation(translation=(self.chip_length*0.5+1200+(counter+1+counter2)*50+a*self.R+(counter+1+counter2)*4*self.R+b, self.couplingWG_l+self.R*a))
                # d['OutPort2_'+ str(counter+1+counter2)]= i3.Rotation(rotation=90.0)+i3.Translation(translation=(self.chip_length*0.5+1200+(counter+1+counter2)*50+(counter+1+counter2)*4*self.R+b,self.couplingWG_l+self.R*a))
            #################
            print '__________________________'
            print "Last layout child cell done"
            print d
            print '_ _ _ _ _ _ _ _ _ _ _ _ _ '
            return d

        def _generate_elements(self, elems):
            for counter, child in enumerate(self.MZI_22_22_list):
                name = child.name

                print name
                elems += i3.PolygonText(layer=i3.TECH.PPLAYER.WG.TEXT,
                                        text='Name={}_R={}_delay={}'.format(name, self.R, self.delay_length),

                                        coordinate=(0.0, -counter * 5 * self.R + 2 * self.R - 50.0  # -100
													),
                                        alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
                                        font=2,
                                        height=20.0)

                elems += i3.PolygonText(layer=i3.TECH.PPLAYER.WG.TEXT,
                                        text='Name={}_R={}_delay={}'.format(name, self.R, self.delay_length),

                                        coordinate=(0.0, -counter * 5 * self.R - 2 * self.R + 50.0  # -100
													),
                                        alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
                                        font=2,
                                        height=20.0)
            for counter2, child in enumerate(self.MZI_12_22_list):
                name = child.name
                print name
                elems += i3.PolygonText(layer=i3.TECH.PPLAYER.WG.TEXT, text='Name={}'.format(name),

                                        coordinate=(0.0, -(counter + 1 + counter2) * 5 * self.R - 90.0 - 500  # -100
													),
                                        alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
                                        font=2,
                                        height=20.0)

            return elems


# cell=MZI_12_21(width_inc_vec=[-0.5,0,0.5], length_inc_vec=[-5,0,5], tipo=2)
cell = MZI_12_21(width_inc_vec=[], length_inc_vec=[-5, 0, 5], tipo=2)
lv = cell.Layout()
lv.write_gdsii("Ckeckwhicchversion.gds")
# lv.write_gdsii("MZIs_WG_test_v3.gds")
lv.visualize(annotate=True)