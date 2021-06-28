
################################
# tipo=1 --> Straigth WG
# tipo=2 --> Bend WG
################################

from technologies import silicon_photonics
import ipkiss3.all as i3

#from isipp50g import technology
#import ipkiss3.all as i3
#TECH = i3.get_technology()

from picazzo3.traces.wire_wg.trace import WireWaveguideTemplate
from picazzo3.routing.place_route import PlaceAndAutoRoute
from picazzo3.routing.place_route import PlaceComponents
# from picazzo3.wg.spirals import FixedLengthSpiralRounded
from picazzo3.container.transition_ports import AutoTransitionPorts

class Spirals(PlaceAndAutoRoute):

    _name_prefix = 'LSpiral'

    tipo = i3.PositiveNumberProperty(doc="Number loops", default = 1)

    waveguide_template = i3.DefinitionProperty(doc="Trace template used")
    R=i3.PositiveNumberProperty(default=500, doc="Radius of curvature")
    spacing =i3.PositiveNumberProperty(default=100, doc="Radius of curvature")
    n_loops = i3.IntProperty(doc="Number loops", default = 2)
    n_loops_vec = i3.ListProperty(default=[4,8])
    s_length_vec = i3.ListProperty(default=[0.0])
    #Spiral_list = i3.ChildCellListProperty(doc="List containing the 90 degree angle child cells")
    #chip_length = i3.PositiveNumberProperty(default=12000.0, doc="")
    chip_length = i3.PositiveNumberProperty(default=13000.0, doc="")
    Port = i3.ChildCellProperty( doc="Used for ports")
    tlport = i3.PositiveNumberProperty(default=2000.0, doc="Transition legth to ports")
    couplingWG = i3.ChildCellProperty(doc="", locked=True)
    couplingWG_l=i3.PositiveNumberProperty(default=5000.0, doc="Length of the coupling WG ")
    tt_port = i3.TraceTemplateProperty(doc="Wide trace template used for the contacts")



    #width_vec = i3.ListProperty(default=[1])
    n=i3.PositiveNumberProperty(default=1, doc="")
    width=i3.PositiveNumberProperty(default=1, doc="")
    lengths=i3.PositiveNumberProperty(default=1, doc="")



    def _default_lengths(self):
        for counter, cell in enumerate(self.s_length_vec):
            numero=counter+1
        return numero


    #template for Autorute
    def _default_trace_template(self):
        return self.waveguide_template

    def _default_tt(self):
        return self.waveguide_template


    def _default_tt_port(self):
        tt_port = WireWaveguideTemplate()
        tt_port_layout=tt_port.Layout(core_width=15.0, cladding_width=15.0+2*8.0)
        return tt_port


    def _default_couplingWG(self):
        rect=i3.Waveguide(trace_template=self.tt_port)
        layout_rect = rect.Layout(shape=[(0.0, 0.0),(self.couplingWG_l,0.0)]
                                  )
        return rect

    def _default_Port(self):
        Port=AutoTransitionPorts(contents=self.couplingWG,
                                 port_labels=["in"],
                                     trace_template=self.waveguide_template)
        layout_Port = Port.Layout(transition_length=self.tlport)#.visualize(annotate=True)
        return Port


    def _default_child_cells(self):
        child_cells = {}          # First we define the property "child_cells" as  an empty dictionary

        for counter, length in enumerate(self.s_length_vec):  # the iteration starts in the first element of the list and follows element by element to the last element.

            #child_cells['Spiral{}'.format(counter)] = spiral
            #print spiral
            #print 'name of spiral:', spiral.name
            child_cells['InPort' + str(counter)] = self.Port
            child_cells['OutPort' + str(counter)]= self.Port

            print 'child_cells:', child_cells
        return child_cells


    def _default_links(self):
        links = []
        for counter, spiral  in enumerate(self.s_length_vec):
            print counter
            #in_port = "Spiral{}:in".format(counter)
            in_port = "InPort{}:in".format(counter)
            #links.append((in_port, out_port))
            #in_port = "Spiral{}:out".format(counter)
            out_port = "OutPort{}:in".format(counter)
            links.append((in_port, out_port))

        return links

    class Layout(PlaceAndAutoRoute.Layout):
        #tipo=1

        def _default_bend_radius(self):
            return self.R


        def _default_child_transformations(self):
            d={}
            for counter, child  in enumerate(self.s_length_vec):
                #ip= child.ports["in"].position
                #print self.child_cells['InPort' + str(counter)].ports["out"].position
                #print self.child_cells['OutPort' + str(counter)].ports.position
                print '----------------'

                #print 'spiral length:', child.total_length
                print 'counter: ', counter
                print 'self.n = ',self.n
                print 'self.width: ', self.width
                #print 'sx: ', sx

                if self.tipo==1:
                    sx=70
                    a=0.5
                    print 2*(22362*0.5-self.couplingWG_l)
                    print 'tipo = ', self.tipo

                    #d['Spiral' + str(counter)] = i3.Translation(translation=(-(op[0]-ip[0])/2, self.n*counter*sx))
                    #d['InPort' + str(counter)] = i3.HMirror()+ i3.Translation(translation=(-self.chip_length*0.5, (self.n+a)*counter*sx))
                    #d['OutPort' + str(counter)] = i3.Translation(translation=(self.chip_length*0.5, (self.n+a)*counter*sx))

                    d['InPort' + str(counter)] = i3.HMirror()+ i3.Translation(translation=(-22362*0.5+self.couplingWG_l, (self.n+a)*counter*sx))
                    d['OutPort' + str(counter)] = i3.Translation(translation=(22362*0.5-self.couplingWG_l, (self.n+a)*counter*sx))

                #if self.tipo==2:
                    #d['Spiral' + str(counter)] = i3.Translation(translation=(-(op[0]-ip[0])/2, -(self.n+0.5)*counter*sx))
                    #d['InPort' + str(counter)] = i3.HMirror()+ i3.Translation(translation=(-self.chip_length*(3/4)-self.couplingWG_l, -(self.n+0.5)*counter*sx))
                    #d['OutPort' + str(counter)] = i3.Rotation(rotation=90) + i3.Translation(translation=((op[0]-ip[0])/2+2*self.R+(((self.n+0.5)*counter+self.width)*sx/4), self.chip_length*(3/4)+(self.width+counter-(((counter+1)-1.0)%self.lengths))*sx))
                if self.tipo==2:
                    sx=100
                    #d['Spiral' + str(counter)] = i3.Translation(translation=(-(op[0]-ip[0])/2, -(self.n+1)*counter*sx))
                    a=7.0
                    print 'increment of length between waveguides of same width: ', (self.n+a)*1*sx     +      ((self.n+a)*1+0)*sx
                    print 'increment of length between waveguides of same length group: ', (self.n+a)*0*sx     +      ((self.n+a)*0+self.width)*sx

                    d['InPort' + str(counter)] = i3.HMirror()+ i3.Translation(translation=(0.0-self.chip_length*0.5
                                                                                           , -(self.n+a)*counter*sx))
                    d['OutPort' + str(counter)] = i3.Rotation(rotation=90) + i3.Translation(translation=((((self.n+a)*counter+self.width)*sx),
                                                                                                         self.chip_length*0.5+(self.width+counter-(((counter+1)-1.0)%self.lengths))*sx))

            return d
        # Fabio's addition
        # def _generate_elements(self, elems):
        #     # We calculate the lengths of the 2 spirals in this pcell.
        #     # Note that we assume that there are exactly 2 spirals in this list.
        #     #assert len(self.Spiral_list) == 2
        #     lengths = get_lengths(self)[0]
        #     print lengths
        #     Link = get_lengths(self)[1]
        #     print Link
        #     if self.tipo==1:
        #
        #         sx=70
        #         for counter, (child, length)  in enumerate(zip(self.s_length_vec, lengths)):
        #             #ip= child.ports["in"].position
        #             #op= child.ports["out"].position
        #
        #             width=Link.trace_template.core_width
        #             #print 'child.ports["in"].trace_template.core_width: ', child.ports["in"].trace_template.core_width
        #             a=0.5
        #         #i3.TECH.PPLAYER.NONE.LOGOTXT   when using isipp50g
        #             elems += i3.PolygonText(layer= i3.TECH.PPLAYER.WG.TEXT, text='Width={}'.format(width,
        #                                                                                                           ),
        #
        #                                 coordinate=(-self.chip_length*0.5+2*self.tlport, (self.n+a)*counter*sx-15.0),
        #                                 alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
        #                                 font = 2,
        #                                 height=20.0)
        #
        #             elems += i3.PolygonText(layer= i3.TECH.PPLAYER.WG.TEXT, text='Width={}'.format(width,
        #                                                                                                             ),
        #
        #                                 coordinate=(0.0, (self.n+a)*counter*sx-15.0),
        #                                 alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
        #                                 font = 2,
        #                                 height=20.0)
        #
        #             elems += i3.PolygonText(layer= i3.TECH.PPLAYER.WG.TEXT, text='Width={}'.format(width,
        #                                                                                                                               ),
        #
        #                                                     coordinate=(self.chip_length*0.5-2*self.tlport, (self.n+a)*counter*sx-15.0),
        #                                                     alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
        #                                                     font = 2,
        #                                                     height=20.0)
        #
        #
        #     if self.tipo==2:
        #         sx=100
        #         for counter, (child, length)  in enumerate(zip(self.s_length_vec, lengths)):
        #             #ip= child.ports["in"].position
        #             #op= child.ports["out"].position
        #
        #             width=Link.trace_template.core_width
        #             #print 'child.ports["in"].trace_template.core_width: ', child.ports["in"].trace_template.core_width
        #             a=7.0
        #         #i3.TECH.PPLAYER.NONE.LOGOTXT   when using isipp50g
        #             elems += i3.PolygonText(layer= i3.TECH.PPLAYER.WG.TEXT, text='Width={}_Length={}_R={}'.format(width,
        #                                                                                                           length,
        #                                                                                                      self.R),
        #
        #                                 coordinate=(-1500, -(self.n+a)*counter*sx-55.0),
        #                                 alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
        #                                 font = 2,
        #                                 height=20.0)
        #     return elems


wg_t = WireWaveguideTemplate()
wg_t.Layout(core_width=3,cladding_width=3+2*8.0,)
test = Spirals(s_length_vec=[7600.0, 7600.0, 7600.0,7600.0,7600.0], waveguide_template= wg_t, R=1000, tipo=2, tlport=500)
layout = test.Layout()
layout.write_gdsii("LossWG.gds")
#
# class Spirals_w(PlaceComponents):
#     Spirals_w_list = i3.ChildCellListProperty(doc="List containing the different routed masks")
#     width_vec = i3.ListProperty(default=[10000.0,20000.0])
#     s_length_vec=i3.ListProperty(default=[50000.0])
#     n=i3.PositiveNumberProperty(default=1, doc="Radius of curvature")
#     tipo=i3.PositiveNumberProperty(default=1, doc="Radius of curvature")
#     R=i3.PositiveNumberProperty(default=500, doc="Radius of curvature")
#     tlport=i3.PositiveNumberProperty(default=300, doc="Radius of curvature")
#
#
#     def _default_n(self):
#         for counter, cell in enumerate(self.width_vec):
#             numero=counter+1
#                 #print 'number of legths: ', self.n
#         return numero
#
#     def _default_Spirals_w_list(self):
#         Spirals_w_list = []
#
#         for w, width in enumerate(self.width_vec):
#             print 'The core width is: ', width
#             wg_t = WireWaveguideTemplate()
#             wg_t.Layout(core_width=width,
#                         cladding_width=width+2*8.0,
#                             )
#             Spirals_w_list.append(Spirals(s_length_vec=self.s_length_vec, waveguide_template=wg_t, tipo=self.tipo, width=w+1, n=self.n, R=self.R, tlport=self.tlport,
#                                           name = 'Spirals_w_'+ str(width))#.Layout(local_mbend_radius = radius)
#                                   )
#         return Spirals_w_list
#
#
#
#     def _default_child_cells(self):
#         child_cells = {}
#
#         for counter, width  in enumerate(self.Spirals_w_list):
#
#             child_cells['Spirals{}'.format(counter)] = width
#
#
#             print 'child_cells:', child_cells
#         return child_cells
#
#
#     class Layout(PlaceComponents.Layout):
#
#
#         def _default_child_transformations(self):
#             d={}
#             for counter, child  in enumerate(self.child_cells):
#                 # We get the layoutview of the childcell
#                 spiral = self.child_cells[child].get_default_view(self)
#                # isz_0 = spiral.instances['Spiral0'].reference.inner_size
#                 #sx=isz_0[1]+200
#
#                 #print 'sx = ',sx
#                 #print("inner_size = {}".format(isz_0, isz_1))
#
#                 number=self.n
#                 if self.tipo==1:
#                     sx=200
#                     d['Spirals' + str(counter)] = i3.Translation(translation=(0.0, (counter)*sx))#+i3.i3.HMirror()
#                 if self.tipo==2:
#                     sx=100
#                     d['Spirals' + str(counter)] = i3.Translation(translation=(0.0, -(counter)*sx))#+i3.i3.HMirror()
#
#
#             return d
# ### Code to calculate the full lenghts.
#
# def get_length_connector(connector):
#     start_transition = connector.instances['start_transition'].reference
#     #print 'start_transition', start_transition
#     end_transition = connector.instances['end_transition'].reference
#     #print 'end_transition', end_transition
#     trace = connector.instances['trace'].reference
#     total_length = (
#         start_transition.length +
#         trace.trace_length() +
#         end_transition.length
#     )
#     #print 'start_transition.length: ', start_transition.length
#     #print 'end_transition.length', end_transition.length
#     #print 'The length of the connector is: ', total_length
#     return total_length
#
#
# def get_length_spiral(spiral):
#     length = spiral.total_length
#     'The length of the spiral is: ', length
#     return length
#
#
# def get_length_transition(transition):
#     return transition.transition_length
#
#
# def get_lengths(spirals):
#     length_total_v=[]
#     insts = spirals.instances
#     for counter, length in enumerate(spirals.instances):
#         print '------------counter: ', counter
#         if 'Spiral{}'.format(counter) in spirals.instances:
#             spiral = insts['Spiral{}'.format(counter)].reference
#         if 'OutPort{}'.format(counter) in spirals.instances:
#             transition_out = insts['OutPort{}'.format(counter)].reference
#         if 'InPort{}'.format(counter+1) in spirals.instances:
#             transition_in = insts['InPort{}'.format(counter)].reference
#         if 'link{}'.format(counter+1) in spirals.instances:
#             link1 = insts['link{}'.format(counter+1)].reference
#             #link2 = insts['link{}'.format(counter*2+2)].reference
#             print 'link{}'.format(counter)
#             print link1.ports["in"].position
#             print link1.ports["out"].position
#             print link1.ports["out"].position[0]-link1.ports["in"].position[0]
#        # print 'link2=link{}'.format(counter*2+2)
#        # print link2.ports["in"].position
#         #print link2.ports["out"].position
#             print 'R = ', link1.trace.bend_radius
#             print (link1.ports["out"].position[0]-link1.ports["in"].position[0])+(link1.ports["out"].position[1]-link1.ports["in"].position[1])+link1.trace.bend_radius*(3.14159/2-2)
#     #  For the calculation of the total leght we can include or not the lenght of the transitions,
#     # which are the wide waveguides to be cleaved.
#
#             length_total = (
#                 #get_length_transition(transition_in) +
#                 get_length_connector(link1)
#                 #+get_length_spiral(spiral) +
#                 #get_length_connector(link2)
#                 #+ get_length_transition(transition_out)
#                 )
#
#             #print 'length_transition_in: ', get_length_transition(transition_in)
#             print 'length_connector(link1): ', get_length_connector(link1)
#            # print 'length_spiral(spiral): ',get_length_spiral(spiral)
#             #print 'legth_connector(link2): ',get_length_connector(link2)
#             #print 'length_transition_out: ', get_length_transition(transition_out)
#             print 'length_total: ', length_total
#
#             length_total_v.append(length_total)
#     return length_total_v, link1
#
# #cell=Spirals_w(s_length_vec=[7600.0, 7600.0, 7600.0,7600.0,7600.0],width_vec=[3.2,3.4,3.6,3.8,4.0], tipo=2)
# #cell=Spirals_w(s_length_vec=[7600.0],width_vec=[4,5,6,7], R=600, tipo=1)
# #cell=Spirals_w(s_length_vec=[7600.0, 7600.0],width_vec=[2.2,2.7,3.3,3.6,5,10,15], R=600, tipo=2)
# cell=Spirals_w(s_length_vec=[7600.0, 7600.0, 7600.0,7600.0,7600.0],width_vec=[2.1,2.2,2.3,3.0,3.2,3.3,3.5,3.7,3.9,4.1,5,10,15], R=1000, tipo=2, tlport=500)
#
# #cell=Spirals_w(s_length_vec=[7600.0, 7600.0, 7600.0,7600.0,7600.0],width_vec=[5.4,5.6,5.8,6.0,10.0], tipo=2)
# #cell=Spirals_w(s_length_vec=[7600.0],width_vec=[5.4,5.6,5.8,6.0,10.0], tipo=1)
#
# lv = cell.Layout()
# lv.visualize(annotate=True)
# #lv.write_gdsii("LossWG_tipo1_Sept_200um_Delpjines mask.gds")
# lv.write_gdsii("dongbo.gds")





