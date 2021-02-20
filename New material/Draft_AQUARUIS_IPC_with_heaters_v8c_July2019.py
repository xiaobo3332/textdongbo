from technologies import silicon_photonics
#from isipp50g_my_version import technology # in this example here isipp50g is actually the new pdk for MIR01
#from isipp50g import technology
import ipkiss3.all as i3
TECH = i3.get_technology()
from picazzo3.filters.mmi.cell import MMI1x2Tapered 
from picazzo3.filters.mmi.cell import MMI2x2Tapered
from picazzo3.filters.mzi import MZIWaveguides
from picazzo3.traces.wire_wg.trace import WireWaveguideTemplate
from picazzo3.routing.place_route import PlaceAndAutoRoute
from picazzo3.routing.place_route import PlaceAndConnect
from ipkiss.geometry.shapes.spline import ShapeRoundAdiabaticSpline
from picazzo3.container.transition_ports import AutoTransitionPorts
from picazzo3.fibcoup.uniform import UniformLineGrating
from picazzo3.wg.spirals import FixedLengthSpiralRounded
from picazzo3.traces.wire_wg.trace import WireWaveguideTemplate
from picazzo3.wg.bend import WgBend90
#from picazzo3.fibcoup.uniform import UniformLineGrating
from picazzo3.routing.place_route import PlaceComponents
#from picazzo3.traces.wire_wg.trace import WireWaveguideTemplate
from picazzo3.filters.mzi import MZIWaveguideArm
from ipkiss.process import PPLayer
print i3.TECH.PROCESS
#import ipkiss3.all as i3
#import Heater_test2

########################################### DEFINITION OF LAYOUT #########################################


	  
         



def AssignProcess(layName):
	if layName == 'waveguide':
		core_process = i3.TECH.PROCESS.WG
		cladding_process = i3.TECH.PROCESS.WG
		core_purpose = i3.TECH.PURPOSE.DF_AREA
		cladding_purpose = i3.TECH.PURPOSE.DF_AREA
	elif layName == 'metal2':
		core_process = i3.TECH.PROCESS.SK
		cladding_process = i3.TECH.PROCESS.SK
		core_purpose = i3.TECH.PURPOSE.DF_AREA
		cladding_purpose = i3.TECH.PURPOSE.DF_AREA
		
	elif layName == 'metal':
		core_process = i3.TECH.PROCESS.RWG
		cladding_process = i3.TECH.PROCESS.RWG
		core_purpose = i3.TECH.PURPOSE.DF_AREA
		cladding_purpose = i3.TECH.PURPOSE.DF_AREA
		#core_process = i3.TECH.PROCESS.M1
		#cladding_process = i3.TECH.PROCESS.M1		
		#core_purpose = i3.TECH.PURPOSE.LF.LINE
		#cladding_purpose = i3.TECH.PURPOSE.LF.LINE		
		
	elif layName == 'flowcell':
		#core_process = i3.TECH.PROCESS.FC
		#cladding_process = i3.TECH.PROCESS.FC
		#core_purpose = i3.TECH.PURPOSE.DF_AREA
		#cladding_purpose = i3.TECH.PURPOSE.DF_AREA
		core_process = i3.TECH.PROCESS.WG
		cladding_process = i3.TECH.PROCESS.WG
		core_purpose = i3.TECH.PURPOSE.LF.LINE
		cladding_purpose = i3.TECH.PURPOSE.LF.LINE		
	else:
		raise Exception('not found process')

	
	kwargs_process = {
                    "core_process": core_process,
                    "core_purpose": core_purpose,
                    "cladding_process": cladding_process,
                    "cladding_purpose": cladding_purpose	          
            }		    
	
	return kwargs_process


def AssignProcessGrating(layName):
	if layName == 'waveguide':
		
		process = i3.TECH.PROCESS.WG
		purpose = i3.TECH.PURPOSE.DF_AREA
		
	elif layName == 'metal2':
				
		process = i3.TECH.PROCESS.SK		
		purpose = i3.TECH.PURPOSE.DF_AREA
		
	elif layName == 'metal':
					
		process = i3.TECH.PROCESS.RWG		
		purpose = i3.TECH.PURPOSE.DF_AREA
		
	#elif layName == 'flowcell':
						
		#process = i3.TECH.PROCESS.NONE		
		#purpose = i3.TECH.PURPOSE.DF_AREA		
				
	else:
		raise Exception('not found process')

	
	kwargs_processgrating = {
                    "process": process,
                    "purpose": purpose,
                              
            }		    
	
	return kwargs_processgrating


########################################### DEFINITION OF FLOW CELL ########################


class arc(PlaceAndAutoRoute):
	R=i3.PositiveNumberProperty(default=200, doc="Radius of curvature of the arc")
	#bend = i3.ChildCellProperty(doc="arc", locked=True)       
	bend90 = i3.ChildCellProperty(doc="arc", locked=True)	
	tt_n_arc = i3.TraceTemplateProperty(doc="Narrow trace template used") 
	tlarc=i3.PositiveNumberProperty(default=40, doc="transition length")
	vline_l=i3.NumberProperty(default=0, doc="core width")
	Vline = i3.ChildCellProperty(doc="to add extra length to the MZI")
	core=i3.PositiveNumberProperty(default=8, doc="core thickness")
	layName = i3.StringProperty(default = 'new')
	props = i3.DictProperty()

	def _default_props(self):
		return AssignProcess(self.layName)


	def _default_Vline(self):
		Vline=i3.Waveguide(trace_template=self.tt_n_arc)
		layout_Vline = Vline.Layout(shape=[(0.0, 0.0),(0.0,self.vline_l*0.5)])#.visualize(annotate=True)
		print 'Vline template: ', Vline.trace_template
		return Vline             

	def _default_bend90(self):
		bend90 = WgBend90(trace_template=self.tt_n_arc)
		layout_bend90= bend90.Layout(quadrant=-3,bend_radius = self.R, rounding_algorithm=ShapeRoundAdiabaticSpline)#.visualize(annotate=True)
		print 'the trace template of arc is', bend90.trace_template
		print 'The trace template of the 90bend of the mzi arc ', bend90.trace_template
		return bend90

	def _default_child_cells(self):

		child_cells={"arc1" : self.bend90,
	                     "arc2" : self.bend90,
	                     
	                     "connector1": self.Vline,
	                     "connector2": self.Vline,
	                     }        

		return child_cells

	def _default_trace_template(self):
		return self.tt_n_arc	

	class Layout(PlaceAndAutoRoute.Layout):
		def _default_child_transformations(self):

			arc_t =i3.Translation(translation=(self.R,0.0)) 

			child_transformations={"arc1":-arc_t + i3.Translation(translation=(0.0,self.vline_l*0.5)),
		                               "arc2":i3.HMirror()+arc_t+ i3.Translation(translation=(0.0,self.vline_l*0.5)),
		                               
		                               "connector1":i3.Translation(translation=(-self.R,0.0)),
		                               "connector2":i3.Translation(translation=(self.R,0.0)),

		                               }
			return child_transformations

	def _default_bend_radius(self):
		return 500	          


class FlowcellRing(PlaceAndAutoRoute):
	#tt_ring = i3.TraceTemplateProperty(doc="Wide trace template used for defining the width of the ring")
	arc = i3.ChildCellProperty(doc="arc", locked=True)
	R=i3.PositiveNumberProperty(default=5500, doc="Radius of curvature of the arc")
		      
	#bend90 = i3.ChildCellProperty(doc="arc", locked=True)	
	tt = i3.TraceTemplateProperty(doc="Narrow trace template used") 
	#tlarc=i3.PositiveNumberProperty(default=40, doc="transition length")
	vline_l=i3.NumberProperty(default=5000, doc="core width")
	#Vline = i3.ChildCellProperty(doc="to add extra length to the MZI")
	core=i3.PositiveNumberProperty(default=1250, doc="core thickness")
	layName = i3.StringProperty(default = 'flowcell')
	props = i3.DictProperty()
	
	def _default_tt(self):
		tt_w = WireWaveguideTemplate()
		tt_w.Layout(core_width=self.core,
	            cladding_width=self.core,
	            **self.props
	            )
		print 'ttw in MoireSquare is ', tt_w
		
		return tt_w	

	def _default_props(self):
		return AssignProcess(self.layName)	
	
	def _default_arc(self):
		cell=arc(R=self.R, vline_l=self.vline_l, core=self.core, layName = self.layName, tt_n_arc=self.tt)
		cell_layout=arc.Layout
		print 'The trace template of the flowcell arc ',cell.trace_template
		return cell	
		
	def _default_child_cells(self):
		child_cells={"arcup" : self.arc,
	                     "arcdown" : self.arc,
	           
	             }        

		return child_cells
	
	
	
	class Layout(PlaceAndAutoRoute.Layout):
		def _default_child_transformations(self):

			child_transformations={"arcup" : i3.Translation(translation=(0.0,0.0)),
		                   "arcdown" : i3.VMirror()+i3.Translation(translation=(0.0,0.0)),

		                   }

			return child_transformations
		
class Flowcell(PlaceAndAutoRoute):
	OutRing_w=i3.PositiveNumberProperty(default=1250, doc="core thickness")
	InRing_w=i3.PositiveNumberProperty(default=500, doc="core thickness")
	R_out=i3.PositiveNumberProperty(default=2750, doc="Radius of curvature of the arc")
	R_in=i3.PositiveNumberProperty(default=1500, doc="Radius of curvature of the arc")
	vline_l_out=i3.NumberProperty(default=6000, doc="core width")
	vline_l_in=i3.NumberProperty(default=6000, doc="core width")
	layName = i3.StringProperty(default = 'flowcell')
	props = i3.DictProperty()
	InRing = i3.ChildCellProperty(doc="Inner ring", locked=True)
	OutRing = i3.ChildCellProperty(doc="Outter ring", locked=True)
	
		
	
	def _default_props(self):
			return AssignProcess(self.layName)	
		
	def _default_InRing(self):
		cell=FlowcellRing(R=self.R_in-0.5*self.InRing_w, vline_l=self.vline_l_in, core=self.InRing_w, layName = self.layName)
		cell_layout=FlowcellRing.Layout
		
		return cell
	
	def _default_OutRing(self):
		cell=FlowcellRing(R=self.R_out-0.5*self.OutRing_w, vline_l=self.vline_l_out, core=self.OutRing_w, layName = self.layName)
		cell_layout=FlowcellRing.Layout
		
		return cell			
		
	def _default_child_cells(self):
			child_cells={"InRing" : self.InRing,
		                     "OutRing" : self.OutRing,
		           
		             }        
	
			return child_cells
	
	
	
	class Layout(PlaceAndAutoRoute.Layout):
		def _default_child_transformations(self):

			child_transformations={"InRing" : i3.Translation(translation=(0.0,0.0)),
		                   "OutRing" : i3.Translation(translation=(0.0,0.0)),

		                   }

			return child_transformations	

class flowcellbox(i3.PCell):
	width = i3.PositiveNumberProperty(default=35000)
	height = i3.PositiveNumberProperty(default=12000)
	circ_x = i3.PositiveNumberProperty(default=3000)
	circ_y = i3.PositiveNumberProperty(default=1000)
	R_s = i3.PositiveNumberProperty(default=2000)
	
	width2 = i3.PositiveNumberProperty(default=35000)
	height2 = i3.PositiveNumberProperty(default=24000)
	
	widthchip = i3.PositiveNumberProperty(default=15000)
	heightchip = i3.PositiveNumberProperty(default=20000)
	
	
	

	class Layout(i3.LayoutView):
		layer = i3.LayerProperty(default=i3.TECH.TRACE.DEFAULT_LAYER)
		layer_c = i3.LayerProperty(default=i3.TECH.TRACE.DEFAULT_LAYER)
		def _default_layer(self):
			layer=PPLayer(process=i3.TECH.PROCESS.WG,purpose=i3.TECH.PURPOSE.LF.LINE)
			return layer
		
		def _default_layer_c(self):
			layer=PPLayer(process=i3.TECH.PROCESS.SK,purpose=i3.TECH.PURPOSE.LF.LINE)
			return layer		

		def _generate_elements(self, elems):
			elems += i3.Rectangle(layer=self.layer, box_size=(self.width, self.height))
			elems += i3.Circle(layer=self.layer, center=(self.width*0.5-self.circ_x-self.R_s, 0.5*self.height-self.circ_y-self.R_s), radius=self.R_s)
			elems += i3.Circle(layer=self.layer, center=(self.width*0.5-self.circ_x-self.R_s, -(0.5*self.height-self.circ_y-self.R_s)), radius=self.R_s)
			elems += i3.Circle(layer=self.layer, center=(-(self.width*0.5-self.circ_x-self.R_s), 0.5*self.height-self.circ_y-self.R_s), radius=self.R_s)
			elems += i3.Circle(layer=self.layer, center=(-(self.width*0.5-self.circ_x-self.R_s), -(0.5*self.height-self.circ_y-self.R_s)), radius=self.R_s)
			
			#elems += i3.Rectangle(layer=self.layer, box_size=(self.width2, self.height2))
			shape=i3.Shape([(0.5*self.width2,-0.5*self.height2),
			                (0.5*self.width2,0.5*self.height2),
			                
			                (5000,0.5*self.height2),
			                (5000,0.5*self.height2-2000),
			                (-5000,0.5*self.height2-2000),
			                (-5000,0.5*self.height2),			                
			                
			                
			                (-0.5*self.width2,0.5*self.height2),
			                (-0.5*self.width2,-0.5*self.height2),
			                
			                (-5000,-0.5*self.height2),
			                (-5000,-0.5*self.height2+2000),
			                (5000,-0.5*self.height2+2000),
			                (5000,-0.5*self.height2),
			                
			        ])
			elems += i3.Boundary(layer=self.layer, shape=shape)		
			
			shape_c=i3.Shape([(0.5*self.widthchip,-0.5*self.heightchip),
			                (0.5*self.widthchip,0.5*self.heightchip),
			                (-0.5*self.widthchip,0.5*self.heightchip),
			                (-0.5*self.widthchip,-0.5*self.heightchip),

						        ])			
			#elems += i3.RectanglePath(layer=self.layer_c, box_size=(self.widthchip, self.heightchip))
			elems += i3.Boundary(layer=self.layer_c, shape=shape_c)	
			return elems

		
########################################### DEFINITION OF ALIGNING MARKS #########################################

class MoireSquare(PlaceComponents):

	#R=i3.PositiveNumberProperty(default=600, doc="Radius of curvature")	
	Pitch1=i3.PositiveNumberProperty(default=2.0, doc="pitch grating 1")	
	Pitch2=i3.PositiveNumberProperty(default=3.0, doc="pitch grating 2")

	dc=i3.PositiveNumberProperty(default=0.5, doc="duty cycle")
	size=i3.PositiveNumberProperty(default=250.0, doc="bigger dimension of aligning mark")


	Grating1 = i3.ChildCellProperty(doc="grating with pitch 1", locked=True)
	Grating2 = i3.ChildCellProperty(doc="grating with pitch 1", locked=True)
	#Grating_list = i3.ChildCellListProperty(default=[])


	tt_grating = i3.TraceTemplateProperty(doc="Wide trace template used ")
	
	layName = i3.StringProperty(default = 'new')
	props = i3.DictProperty()
	propsgrating = i3.DictProperty()
	
		
		
	
	def _default_props(self):
		return AssignProcess(self.layName)
	def _default_propsgrating(self):
		return AssignProcessGrating(self.layName)	


	def _default_Pitch1(self):

		return self.Pitch1    

	def _default_Pitch2(self):
		pitch2=self.Pitch1+0.05
		return pitch2



	def _default_tt_grating(self):
		tt_w = WireWaveguideTemplate()
		tt_w.Layout(core_width=(self.size-10.0)/6.0,
                    cladding_width=(self.size-10.0)/6.0,
		    **self.props
                    )
		print 'ttw in MoireSquare is ', tt_w
		
		return tt_w



	def _default_Grating1(self):
		print 'Pitch 1: ', self.Pitch1
		print 'I am in grating1 of aligning marks'

		FGC = UniformLineGrating(trace_template=self.tt_grating)
		FGC_layout = FGC.Layout(period=self.Pitch1,
                                line_width=self.Pitch1*self.dc,
                                line_length=(self.size-10.0)/6.0-1.0,
                                n_o_periods=int(((self.size-10.0)/6.0)/self.Pitch1),
                                socket_length=(self.size-10.0)/6.0, **self.propsgrating
		                )
		print 'origin G1: {}'.format(-0.5 * int(((self.size-10.0)/6.0)/self.Pitch1) * self.Pitch1)
		print 'The trace template of the aligning marks with grating1 is ', FGC.trace_template  
		return FGC    

	def _default_Grating2(self):
		print 'Pitch 2: ', self.Pitch2
		FGC = UniformLineGrating(trace_template=self.tt_grating)
		FGC_layout = FGC.Layout(period=self.Pitch2,
                                line_width=self.Pitch2*self.dc,
                                line_length=(self.size-10.0)/6.0-1,
                                n_o_periods=int(((self.size-10.0)/6.0)/self.Pitch2),
                                socket_length=(self.size-10.0)/6.0, **self.propsgrating)		
		print 'origin G2: {}'.format(-0.5 * int(((self.size-10.0)/6.0)/self.Pitch2) * self.Pitch2) 
		print 'The trace template of the aligning marks with grating2 is ', FGC.trace_template
		return FGC        

	def _default_child_cells(self):
		child_cells={"G1" : self.Grating1,
                     "G2" : self.Grating2,
                     "G3" : self.Grating2,
                     "G4" : self.Grating1,

                     }        

		return child_cells



	class Layout(PlaceComponents.Layout):
		def _default_child_transformations(self):

			child_transformations={"G1" : i3.Translation(translation=(-(self.size-10.0)/12.0,(self.size-10.0)/12.0)),
                                   "G2" : i3.Translation(translation=((self.size-10.0)/12.0,(self.size-10.0)/12.0)),
                                   "G3" : i3.Translation(translation=(-(self.size-10.0)/12.0,-(self.size-10.0)/12.0)), 
                                   "G4" : i3.Translation(translation=((self.size-10.0)/12.0,-(self.size-10.0)/12.0)),

                                   }

			return child_transformations	

class AligningMarks(PlaceComponents):

	tt_cross = i3.TraceTemplateProperty(doc="Wide trace template used for the contact pads")
	hline = i3.ChildCellProperty(doc="Horizontal line", locked=True)
	vline = i3.ChildCellProperty(doc="Vertical", locked=True)
	square = i3.ChildCellProperty(doc="Vertical", locked=True)
	size=i3.PositiveNumberProperty(default=250.0, doc="bigger dimension of aligning mark")
	Pitch1=i3.PositiveNumberProperty(default=2.0, doc="pitch grating 1")	
	separation=i3.NumberProperty(default=100.0, doc="separation between cross and gratings")

	dc=i3.PositiveNumberProperty(default=0.47, doc="duty cycle") 
	
	layName = i3.StringProperty(default = 'standard')
	props = i3.DictProperty()	
			
		
	def _default_props(self):
		return AssignProcess(self.layName)		

	def _default_tt_cross(self):
		tt_w = WireWaveguideTemplate()
		tt_w.Layout(core_width=(self.size-10.0)/3.0,
                    cladding_width=(self.size-10.0)/3.0,
		    **self.props
                        )

		return tt_w

	def _default_hline(self):
		rect=i3.Waveguide(trace_template=self.tt_cross)
		layout_rect = rect.Layout(shape=[(0.0, self.size/2.0),(self.size,self.size/2.0)])
		print 'The trace template of the hline of the cross ', rect.trace_template 
		return rect  

	def _default_vline(self):
		rect=i3.Waveguide(trace_template=self.tt_cross)
		layout_rect = rect.Layout(shape=[(self.size/2.0, 0.0),(self.size/2.0,self.size)])
		print 'The trace template of the vline of the cross ', rect.trace_template 
		                          
			
		return rect  

	def _default_square(self):
		square=MoireSquare(size=self.size, Pitch1=self.Pitch1, dc=self.dc, layName=self.layName)
		return square

	def _default_child_cells(self):
		child_cells={"S1" : self.square,
                     "S2" : self.square,
                     "S3" : self.square,
                     "S4" : self.square,
                     "V"  : self.vline,
                     "H"  : self.hline
                     }        

		return child_cells    

	class Layout(PlaceComponents.Layout):

		def _default_child_transformations(self):

			child_transformations={"S1" : i3.Translation(translation=(-(self.size-10.0)/3.0-10.0/2,(self.size-10.0)/3.0+10.0/2)),
                                   "S2" : i3.Rotation(rotation=(90.0))+i3.Translation(translation=((self.size-10.0)/3.0+10.0/2,(self.size-10.0)/3.0+10.0/2)),
                                   "S3" : i3.Rotation(rotation=(90.0))+i3.Translation(translation=(-(self.size-10.0)/3.0-10.0/2,-(self.size-10.0)/3.0-10.0/2)), 
                                   "S4" : i3.Translation(translation=((self.size-10.0)/3.0+10.0/2,-(self.size-10.0)/3.0-10.0/2)), 
                                   "V"  : i3.Translation(translation=(0.0, self.size+self.separation))+ i3.Translation(translation=(-(self.size)/2.0,-(self.size)/2.0)),
                                   "H"  : i3.Translation(translation=(0.0, self.size+self.separation))+ i3.Translation(translation=(-(self.size)/2.0,-(self.size)/2.0))	                       
                                   }   


			return child_transformations

	def _generate_elements(self, elems):

		elems += i3.PolygonText(layer= i3.TECH.PPLAYER.WG.TEXT, text='Pitch1={}_Pitch2={}_dc_{}'.format(self.Pitch1,
                                                                                                        self.square.Pitch2,
                                                                                                         self.dc
                                                                                                         ),

                                coordinate=(-250.0, -self.size*0.5-20.0),
                                alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
                                font = 2,
                                height=20.0)  

		return elems



#cell=AligningMarks(Pitch1=1.95, dc=0.5)

#lv = cell.Layout()
#lv.write_gdsii("AligningMarks_test2_P1_{}_dc_{}_P2_{}.gds".format(cell.Pitch1, cell.dc, cell.square.Pitch2))
#lv.visualize(annotate=True)


########################################### DEFINITION OF HEATERS #########################################


class harc(PlaceAndAutoRoute):

	R=i3.PositiveNumberProperty(default=200, doc="Radius of curvature of the arc")	
	#al=i3.PositiveNumberProperty(default=2005.0, doc="arc length")
	hl=i3.NumberProperty(default=1.0, doc="connection waveguide length")
	bend = i3.ChildCellProperty(doc="arc", locked=True)
	bend90 = i3.ChildCellProperty(doc="arc", locked=True)	
	tt_n_harc = i3.TraceTemplateProperty(doc="Narrow trace template used")
	tt_pads_harc = i3.TraceTemplateProperty(doc="Wide trace template used for the contact pads")
	hline = i3.ChildCellProperty(doc="Horizontal pad", locked=True)
	hPort = i3.ChildCellProperty(doc="Horizontal pad with port", locked=True)
	tlarc=i3.PositiveNumberProperty(default=40, doc="transition length")
	vline_l=i3.NumberProperty(default=0, doc="core width")
	width=i3.PositiveNumberProperty(default=7, doc="core width")
	pads_w=i3.PositiveNumberProperty(default=7, doc="cwidth of pads")
	r_heater=i3.PositiveNumberProperty(default=50, doc="radius of curvature of connexion of heater arc with pads")

	
	def _default_bend90(self):

		bend90 = WgBend90(trace_template=self.tt_n_harc)

		layout_bend90= bend90.Layout(quadrant=-3,bend_radius = self.R, rounding_algorithm=ShapeRoundAdiabaticSpline)#.visualize(annotate=True)
		print 'The trace template of the heater harc bend90 ', bend90.trace_template 
		return bend90


	def _default_bend(self):
		bend=AutoTransitionPorts(contents=self.bend90, 
                                         port_labels=["in"],
                                         trace_template=self.tt_pads_harc,
                                         )
		layout_bend =bend.Layout(transition_length=self.tlarc)#.visualize(annotate=True)
		print 'The trace template of the heater harc bend ', bend.trace_template 
		return bend


	def _default_hline(self):
		hline=i3.Waveguide(trace_template=self.tt_n_harc)
		layout_hline = hline.Layout(shape=[(0.0, 0.0),(self.hl,0.0)]
                                            )
		print 'The trace template of the hline of harc for heater ', hline.trace_template 
		return hline

	def _default_hPort(self):
		hPort=AutoTransitionPorts(contents=self.hline, 
                                          port_labels=["in"],
                                          trace_template=self.tt_pads_harc)
		layout_hPort = hPort.Layout(transition_length=self.tlarc)#.visualize(annotate=True)
		print 'The trace template of the hport of harc for heater ', hPort.trace_template 
		return hPort

	def _default_child_cells(self):

		child_cells={"arc1" : self.bend90,
                             "arc2" : self.bend90,
                             "h1"   : self.hPort,
                             "h2"   : self.hPort,


                             }        

		return child_cells

	def _default_links(self):
		links = [
                    ("h2:out", "arc2:in"),
                        ("h1:out", "arc1:in"),
                ]
		
		
		return links

	def _default_trace_template(self):
		return self.tt_n_harc	

	class Layout(PlaceAndAutoRoute.Layout):
		def _default_child_transformations(self):
			V_t = i3.Translation(translation=(5*self.R+self.tlarc,0.0))
			arc_t =i3.Translation(translation=(self.R,0.0)) 

			child_transformations={"arc1":-arc_t + i3.Translation(translation=(0.0,2*self.bend_radius)),
                                               "arc2":i3.HMirror()+arc_t+ i3.Translation(translation=(0.0,2*self.bend_radius)),
                                               "h2" : i3.HMirror()+i3.Translation(translation=(self.R+2*self.bend_radius,0.0)), 
                                               "h1" : i3.Translation(translation=(-(self.R+2*self.bend_radius),0.0)), 

                                               }




			return child_transformations

		def _default_bend_radius(self):
			return self.r_heater	  
			#return self.R

class Heater(PlaceAndAutoRoute):

	r=i3.PositiveNumberProperty(default=200, doc="Radius of curvature")
	tl=i3.NumberProperty(default=10.0, doc="transition length")
	increment=i3.PositiveNumberProperty(default=1.0, doc="increment for lateral separation")

	Hl=i3.PositiveNumberProperty(default=10.0, doc="length horizontal pad")
	Vline = i3.ChildCellProperty(doc="Vertical pad, defines the width of the heater", locked=True)
	Hline = i3.ChildCellProperty(doc="Horizontal pad, defines the heigth of the heater", locked=True)

	contact = i3.ChildCellProperty(doc="Horizontal pad", locked=True)
	ContactPort = i3.ChildCellProperty(doc="Horizontal pad with port", locked=True)
	contact_pos=i3.NumberProperty(default=5000, doc="position of contact pads with respect to chip edge")
	contact_height=i3.NumberProperty(default=4500, doc="position of contact pads with respect to chip edge")
	contact_w=i3.PositiveNumberProperty(default=1000, doc="core thickness")
	contact_l=i3.PositiveNumberProperty(default=1000, doc="length of the contact")

	tt_n_heater = i3.TraceTemplateProperty(doc="Narrow trace template used")
	tt_pads_heater = i3.TraceTemplateProperty(doc="Wide trace template used for the contact pads")
	tt_contact_heater = i3.TraceTemplateProperty(doc="Wide trace template used for the contacts")
	Arc = i3.ChildCellProperty(doc="arc")
	tlarc=i3.PositiveNumberProperty(default=40, doc="transition length")
	width=i3.PositiveNumberProperty(default=1, doc="width of heater narrow")
	pads_w=i3.PositiveNumberProperty(default=2.2, doc="width of pads")
	r_heater=i3.PositiveNumberProperty(default=50, doc="radius of curvature of connexion of heater arc with pads")
	layName = i3.StringProperty(default = 'new')
	props = i3.DictProperty()
	codearc = i3.PositiveNumberProperty(default=1, doc="transition length")


		
	def _default_props(self):
		
		return AssignProcess(self.layName)
	
	
	
	def _default_tl(self):
		tl =(self.contact_w-self.pads_w)*0.5
		return tl
	
	def _default_contact_l(self):
		contact_l =self.contact_height-(3*self.r-50+self.pads_w+self.tl)#-self.tl#+3*self.r+50+1.5*self.pads_w)
		#contact_l =-50-self.pads_w-self.tl+self.contact_height-2*self.r_heater
		#contact_l =self.contact_height-self.tl-(2*self.r_heater+2*self.pads_w+self.r+50)
		print 'The contact length is: ', contact_l
	
		return contact_l
	
	def _default_ContactPort(self):
		Hport=AutoTransitionPorts(contents=self.contact, 
	                                  port_labels=["in"],
	                                  trace_template=self.tt_pads_heater)
		layout_Hport = Hport.Layout(transition_length=self.tl)
		#layout_Hport.visualize(annotate=True)
		print 'The trace template of the Hport of theheater ', Hport.trace_template 
		return Hport	

	def _default_contact(self):
		contact=i3.Waveguide(trace_template=self.tt_contact_heater)
		layout_contact = contact.Layout(shape=[(0.0, 0.0),(0.0,self.contact_l)])
		#layout_contact.visualize(annotate=True)
		print 'The trace template of the heater contacts ', contact.trace_template 
		return contact		

	def _default_tt_n_heater(self):
		tt_n = WireWaveguideTemplate()
		tt_n.Layout(core_width=self.width,
                            cladding_width=self.width, **self.props
                            )
		return tt_n

	def _default_tt_pads_heater(self):
		tt_pads = WireWaveguideTemplate()
		tt_pads.Layout(core_width=self.pads_w,
                               cladding_width=self.pads_w, **self.props
                               )
		return tt_pads	

	def _default_tt_contact_heater(self):
		tt_contact = WireWaveguideTemplate()
		tt_contact.Layout(core_width=self.contact_w,
                                  cladding_width=self.contact_w, **self.props
                                  )
		return tt_contact	

	def _default_Arc(self):
		Arc=harc(R=self.r, tlarc=self.tlarc, width=self.width, tt_pads_harc=self.tt_pads_heater,
		         r_heater=self.r_heater, tt_n_harc = self.tt_n_heater)
		print 'the radius of the heater arc is ',self.r
		layout_Arc = Arc.Layout()#.visualize(annotate=True)
		print 'The trace template of the Arc of the heater ', Arc.trace_template 
		return Arc	  

	def _default_Vline(self):
		Vline=i3.Waveguide(trace_template=self.tt_pads_heater)
		layout_Vline = Vline.Layout(shape=[(0.0, 0.0),(0.0,self.Hl)])#.visualize(annotate=True)
		print 'The trace template of the Vline of theheater ', Vline.trace_template 
		return Vline

	def _default_Hline(self):
		Hline=i3.Waveguide(trace_template=self.tt_pads_heater)
		layout_Hline = Hline.Layout(shape=[(0.0, 0.0),(self.Hl,0.0)])
		print 'The trace template of the Hline of theheater ', Hline.trace_template 
		return Hline


	def _default_child_cells(self):
		child_cells={"V1"   : self.Vline,
                             "V2"   : self.Vline,
                             #"Arc"  : self.Arc
                             "H1"   : self.Hline,
                             "H2"   : self.Hline,
                             "c1"   : self.ContactPort,
                             "c2"   : self.ContactPort
                             }    
		if self.codearc==1:
			child_cells["Arc"]=self.Arc
		return child_cells

	def _default_links(self):
		links = [#("V1:in", "Arc:h1_in"),
                         #("V2:in", "Arc:h2_in"),
                         ("H1:out", "V1:out"),
                         ("H2:out", "V2:out"),
                         ("c1:in", "H1:in"),
                         ("c2:in", "H2:in"),
                         ]
		if self.codearc==1:
			links.append(("V1:in", "Arc:h1_in"))
			links.append(("V2:in", "Arc:h2_in"))
		return links

	def _default_trace_template(self):
		return self.tt_pads_heater

	
	class Layout(PlaceAndAutoRoute.Layout):


		def _default_child_transformations(self):
			V_t = i3.Translation(translation=(2*self.r+self.tlarc,0.0))

			child_transformations={"V1": - V_t +i3.Translation(translation=(0.0,2*self.r)),
                                                               "V2":  V_t +i3.Translation(translation=(0.0,2*self.r)),

                                                               "H1" : - V_t + i3.Translation(translation=(-500,3*self.r)), 

                                                               "H2" :- V_t + i3.Translation(translation=(-500,3*self.r+50+self.pads_w)),

                                                               "c1" : i3.Translation(translation=(-self.contact_pos-self.contact_w-200,self.tl+3*self.r+50+1.5*self.pads_w)),
                                                               "c2" : i3.Translation(translation=(-self.contact_pos,self.tl+3*self.r+50+1.5*self.pads_w)),
			                                       #"c1" : i3.Translation(translation=(-self.contact_pos-self.contact_w-200,-self.pads_w+self.tl+3*self.r+50+1*self.pads_w)),			                                       
			                                       
			                                       
			                                       #"c1" : i3.Translation(translation=(-self.contact_pos-self.contact_w-200,self.tl+2*(3*self.r_heater+50+self.pads_w)+2*self.r_heater+self.pads_w)),
			                                       #"c2" : i3.Translation(translation=(-self.contact_pos,self.tl+2*(3*self.r_heater+50+self.pads_w)+2*self.r_heater+self.pads_w)),			                                       

                                                               }
			print 'contact position ', self.contact_pos
			return child_transformations                

		def _default_bend_radius(self):
			return 5


########################################### DEFINITION OF MZI #########################################

class marc(PlaceAndAutoRoute):
	R=i3.PositiveNumberProperty(default=200, doc="Radius of curvature of the arc")
	#bend = i3.ChildCellProperty(doc="arc", locked=True)       
	bend90 = i3.ChildCellProperty(doc="arc", locked=True)	
	tt_n_arc = i3.TraceTemplateProperty(doc="Narrow trace template used") 
	tlarc=i3.PositiveNumberProperty(default=40, doc="transition length")
	vline_l=i3.NumberProperty(default=0, doc="core width")
	Vline = i3.ChildCellProperty(doc="to add extra length to the MZI")
	core=i3.PositiveNumberProperty(default=8, doc="core thickness")
	layName = i3.StringProperty(default = 'new')
	props = i3.DictProperty()

	def _default_props(self):
		return AssignProcess(self.layName)


	def _default_Vline(self):
		Vline=i3.Waveguide(trace_template=self.tt_n_arc)
		layout_Vline = Vline.Layout(shape=[(0.0, 0.0),(0.0,self.vline_l)])#.visualize(annotate=True)
		print 'Vline template: ', Vline.trace_template
		return Vline             

	def _default_bend90(self):
		bend90 = WgBend90(trace_template=self.tt_n_arc)
		layout_bend90= bend90.Layout(quadrant=-3,bend_radius = self.R, rounding_algorithm=ShapeRoundAdiabaticSpline)#.visualize(annotate=True)
		print 'the trace template of arc is', bend90.trace_template
		print 'The trace template of the 90bend of the mzi arc ', bend90.trace_template
		return bend90

	def _default_child_cells(self):

		child_cells={"arc1" : self.bend90,
	                     "arc2" : self.bend90,
	                     "arc3"   : self.bend90,
	                     "arc4"   : self.bend90,
	                     "connector1": self.Vline,
	                     "connector2": self.Vline,
	                     }        

		return child_cells

	def _default_trace_template(self):
		return self.tt_n_arc	

	class Layout(PlaceAndAutoRoute.Layout):
		def _default_child_transformations(self):

			arc_t =i3.Translation(translation=(self.R,0.0)) 

			child_transformations={"arc1":-arc_t + i3.Translation(translation=(0.0,self.R+self.vline_l)),
		                               "arc2":i3.HMirror()+arc_t+ i3.Translation(translation=(0.0,self.R+self.vline_l)),
		                               "arc3" : i3.VMirror()+i3.Translation(translation=(self.R,self.R)), 
		                               "arc4" :i3.HMirror()+i3.VMirror()+i3.Translation(translation=(-(self.R),self.R)),
		                               "connector1":i3.Translation(translation=(-self.R,self.R)),
		                               "connector2":i3.Translation(translation=(self.R,self.R)),

		                               }
			return child_transformations

	def _default_bend_radius(self):
		return 500	          




class MZI(PlaceAndAutoRoute):
	mmi1_12 = i3.ChildCellProperty(doc="mmi1_12 used")
	mmi1_22 = i3.ChildCellProperty(doc="mmi1_22 used")
	arc = i3.ChildCellProperty(doc="mmi1_22 used")

	tt_n_mzi = i3.TraceTemplateProperty(doc="Narrow trace template used")
	#tt_wide = i3.TraceTemplateProperty(doc="Wide trace template used")
	#length_taper_wide=i3.PositiveNumberProperty(default=1000, doc="Length of taper for detection region")
	mzi_position=i3.PositiveNumberProperty(default=12000, doc="Position of mzi with respect to the center of the chip")
	mmi12_l=i3.PositiveNumberProperty(default=148.0, doc="lenght of mmi 1x2")
	mmi12_w=i3.PositiveNumberProperty(default=22.0, doc="width of mmi 1x2")
	mmi12_port=i3.PositiveNumberProperty(default=10.0, doc="width of port of mmi 1x2")
	mmi22_l=i3.PositiveNumberProperty(default=298.0, doc="lenght of mmi 2x2")
	mmi22_w=i3.PositiveNumberProperty(default=22.0, doc="width of mmi 2x2")
	mmi22_port=i3.PositiveNumberProperty(default=10.0, doc="width of port of mmi 1x2")
	length_taper_mmi12=i3.PositiveNumberProperty(default=100, doc="Length of taper for detection mmi ports")
	length_taper_mmi22=i3.PositiveNumberProperty(default=100, doc="Length of taper for detection region")
	R=i3.PositiveNumberProperty(default=200, doc="Radius of curvature of the arc")	        
	core=i3.PositiveNumberProperty(default=4, doc="core width")
	vline_l=i3.NumberProperty(default=2.2, doc="estra length for MZI")
	layName = i3.StringProperty(default = 'new')
	props = i3.DictProperty()		
	
	def _default_props(self):
		return AssignProcess(self.layName)	


	def _default_mmi1_12(self):
		mmi_trace_template = WireWaveguideTemplate()
		mmi_trace_template.Layout(core_width=self.mmi12_w, cladding_width=self.mmi12_w, **self.props)

		mmi_access_template = WireWaveguideTemplate()
		mmi_access_template.Layout(core_width=self.mmi12_port, cladding_width=self.mmi12_port, **self.props) 

		mmi1_12 = MMI1x2Tapered(mmi_trace_template=mmi_trace_template,
                                        input_trace_template=mmi_access_template,
                                        output_trace_template=mmi_access_template,
                                        trace_template=self.tt_n_mzi,
                                        )
		layout_mmi1_12 = mmi1_12.Layout(transition_length=self.length_taper_mmi12, length=self.mmi12_l, trace_spacing=self.mmi12_w-self.mmi12_port)  
		print 'mmi_trace_template 12 ', mmi_trace_template
		print 'mmi_access_template 12 ', mmi_access_template		
		return mmi1_12


	def _default_mmi1_22(self):


		mmi_trace_template = WireWaveguideTemplate()
		mmi_trace_template.Layout(core_width=self.mmi22_w, cladding_width=self.mmi22_w, **self.props)

		mmi_access_template = WireWaveguideTemplate()
		mmi_access_template.Layout(core_width=self.mmi22_port, cladding_width=self.mmi22_port, **self.props)    

		mmi1_22 = MMI2x2Tapered(mmi_trace_template=mmi_trace_template,
                                        input_trace_template=mmi_access_template,
                                        output_trace_template=mmi_access_template,
                                        trace_template=self.tt_n_mzi,
                                        )

		layout_mmi1_22 = mmi1_22.Layout(transition_length=self.length_taper_mmi22, length=self.mmi22_l, trace_spacing=self.mmi22_w-self.mmi22_port)  
		#print 'mmi1_22 done'
		print 'mmi_trace_template 22 ', mmi_trace_template
		print 'mmi_access_template 22 ', mmi_access_template		
		return mmi1_22

	def _default_arc(self):
		cell=marc(R=self.R, vline_l=self.vline_l, core=self.core, tt_n_arc = self.tt_n_mzi, layName = self.layName)
		cell_layout=arc.Layout
		print 'The trace template of the  mzi arc ',cell.trace_template
		return cell

	def _default_child_cells(self):

		child_cells={"mmi12" : self.mmi1_12,
                             "mmi22" : self.mmi1_22,
                             "arc_up"  : self.arc,
                             "arc_down"  : self.arc,
                             }        
		return child_cells 

	
	def _default_external_port_names(self):
		expn = dict()
		expn["mm12:in"] = "in"
		expn["mmi22:out1"] = "out1"
		expn["mmi22:out2"] = "out2"

		return expn        

	class Layout(PlaceAndAutoRoute.Layout):
		             
		def _default_child_transformations(self):
			child_transformations={
                            "arc_down":i3.VMirror() + i3.Translation(translation=(0.0,-(self.mmi12_w*0.5-self.mmi12_port*0.5))),
                        "arc_up": i3.Translation(translation=(0.0,self.mmi12_w*0.5-self.mmi12_port*0.5)),
                        "mmi12": i3.Translation(translation=(-(2*self.R+self.length_taper_mmi12+self.mmi12_l),0.0)),
                        "mmi22": i3.Translation(translation=((2*self.R+self.length_taper_mmi22),0.0)),

                        }
			return child_transformations       

		def _default_bend_radius(self):
			#return self.R
			return 20 
		
########################################### DEFINITION OF BRANCH OF CIRCUIT #########################################

class Branch(PlaceAndAutoRoute):

	core=i3.PositiveNumberProperty(default=2.2, doc="core width")	        
	tt_n_branch = i3.TraceTemplateProperty(doc="Narrow trace template used")
	tt_wide_branch = i3.TraceTemplateProperty(doc="Wide trace template used")
	delay_length = i3.PositiveNumberProperty(default=0, doc="Delay length used in the mzi")
	mzi = i3.ChildCellProperty(doc="Mzi used", locked=True)
	spiral = i3.ChildCellProperty(doc="spiral used")
	#sensor = i3.ChildCellProperty(doc="region in contact with analyte/reference used")
	R=i3.PositiveNumberProperty(default=200, doc="Radius of curvature")
	length_taper_wide=i3.PositiveNumberProperty(default=1000, doc="Length of taper for detection region")
	mzi_position=i3.PositiveNumberProperty(default=12000, doc="Position of mzi with respect to the center of the chip")
	mmi12_l=i3.PositiveNumberProperty(default=148.0, doc="lenght of mmi 1x2")
	mmi12_w=i3.PositiveNumberProperty(default=22.0, doc="width of mmi 1x2")
	mmi12_port=i3.PositiveNumberProperty(default=10.0, doc="width of port of mmi 1x2")
	mmi22_l=i3.PositiveNumberProperty(default=298.0, doc="lenght of mmi 2x2")
	mmi22_w=i3.PositiveNumberProperty(default=22.0, doc="width of mmi 2x2")
	mmi22_port=i3.PositiveNumberProperty(default=10.0, doc="width of port of mmi 1x2")
	length_taper_mmi12=i3.PositiveNumberProperty(default=100, doc="Length of taper for detection mmi ports")
	length_taper_mmi22=i3.PositiveNumberProperty(default=100, doc="Length of taper for detection region")
	vline_l=i3.NumberProperty(default=2.2, doc="estra length for MZI")
	wide_wg_l = i3.NumberProperty(default=2000, doc="Wide Waveguide")
	tipo =i3.NumberProperty(default=2, doc="1=spiral, 2=wide waveguide")
	refsig_d=i3.PositiveNumberProperty(default=2.2, doc="separation between reference and signal waveguides")
	coresensing=i3.PositiveNumberProperty(default=50, doc="separation between reference and signal waveguides")
	layName = i3.StringProperty(default = 'new')
	props = i3.DictProperty()	
	

	def _default_props(self):
		return AssignProcess(self.layName)	

	def _default_child_cells(self):

		child_cells={"mzi_1" : self.mzi,
                             "mzi_2" : self.mzi,
                             "Sup"  : self.spiral,
                             "Sdown": self.spiral}        

		return child_cells



#Define the child cells which act as splitter and combiner and how they are      
	def _default_links(self):
		links = [("mzi_1:out2", "Sup:in"),
                         ("mzi_1:out1", "Sdown:in"),
                         ("mzi_2:out2", "Sup:out"),
                         ("mzi_2:out1", "Sdown:out")]

		return links


	def _default_spiral(self):
		if self.tipo==1:
			spiral = FixedLengthSpiralRounded(name='spiral',total_length=13000, n_o_loops=1, trace_template=self.tt_wide_branch)
			spiral.Layout(incoupling_length=0.0,
                          bend_radius=self.R,
                      spacing=self.coresensing+10,
                      stub_direction="H",  # either H or V
                      growth_direction="H"  # either H or V
                      )
		if self.tipo==2:
			spiral = i3.Waveguide(trace_template=self.tt_wide_branch)
			spiral.Layout(shape=[(-self.wide_wg_l*0.5, 0.0),(self.wide_wg_l*0.5, 0.0)]) 		
		print 'The trace template of the  spiral ',spiral.trace_template
		taper_spiral = AutoTransitionPorts(contents=spiral, 
                                           #port_labels=["in","out"],
                                                   trace_template=self.tt_n_branch)
		layout=taper_spiral.Layout(transition_length=self.length_taper_wide)
		print 'The trace template of the tapered spiral ',spiral.trace_template
		#layout.visualize(annotate=True)
		return taper_spiral  

	 	

	def _default_tt_wide_branch(self):
		tt_w = WireWaveguideTemplate()
		tt_w.Layout(core_width=self.coresensing,
                            cladding_width=self.coresensing,
		            **self.props
                           )

		return tt_w

	def _default_tt_n_branch(self):
		tt_n = WireWaveguideTemplate()
		tt_n.Layout(core_width=self.core,
                            cladding_width=self.core,
		            **self.props
		        )
		return tt_n


	def _default_mzi(self):
		cell=MZI(R=self.R, vline_l=self.vline_l, core=self.core, mmi12_w=self.mmi12_w, 
		         mmi22_w=self.mmi22_w, mmi12_l=self.mmi12_l, mmi22_l=self.mmi22_l, 
		         mmi12_port=self.mmi12_port, mmi22_port=self.mmi22_port,
		         tt_n_mzi=self.tt_n_branch, layName = self.layName
		         )
		print 'The trace template of the  MZI',cell.trace_template	
		print 'The MZI radius is', self.R
		return cell      

	def _default_trace_template(self):
		return self.tt_n_branch

	class Layout(PlaceAndAutoRoute.Layout):
		def _generate_elements(self, elems):
			if self.tipo==1:
				#Sdown_t = (-0.5*lenght+self.length_taper_wide, -0.5*self.refsig_d-self.coresensing-50.0)
				#Sup_t=(-0.5*lenght+self.length_taper_wide, 0.5*self.refsig_d+self.coresensing+50.0)
			
				Sdown_t =(0.0, -0.5*self.refsig_d-self.coresensing-50.0#+2*self.R
				          )
				Sup_t=(0.0, 0.5*self.refsig_d+self.coresensing+50.0#-2*self.R
				       )	
				print Sdown_t
				print self.R
			if self.tipo==2:
				Sdown_t =(0.0, -0.5*self.refsig_d-self.coresensing-50.0)
				Sup_t=(0.0, 0.5*self.refsig_d+self.coresensing+50.0)				

			    #i3.TECH.PPLAYER.NONE.LOGOTXT   when using isipp50g
			elems += i3.PolygonText(layer= i3.TECH.PPLAYER.WG.TEXT, text='Width={}'.format(self.coresensing,
		                                                                                                     ),
		                            coordinate=Sup_t,
		                            alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
		                            font = 2,
		                            height=20.0)
			elems += i3.PolygonText(layer= i3.TECH.PPLAYER.WG.TEXT, text='Width={}'.format(self.coresensing,
						                                                                                             ),
						                    coordinate=Sup_t,
						                    alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
						                    font = 2,
						                    height=20.0)			
			return elems
		


		def _default_bend_radius(self):
			return self.R

		def _default_start_straight(self):

			ops=self.spiral.ports['out'].position
			ips=self.spiral.ports['in'].position
			print 'ips', ips
			pm=self.mzi.ports['out1'].position


			lenght_s=ops[0]-ips[0]
			print 'length_s is:', lenght_s
			lenght = self.mzi_position-2*self.R-self.mmi22_w-self.length_taper_mmi22-(0.5*lenght_s-self.length_taper_wide)
			print 'lenght is:', lenght			
			print 'end straigth'
			return 0 #lenght#2000.0      		

		
		def _default_child_transformations(self):

			print self.spiral.instances#['spiral'].inner_size 
			outport=self.spiral.ports['out'].position
			inport=self.spiral.ports['in'].position
			print 'inport:', inport, 'outport:', outport
			print self.spiral.ports
			lenght=outport[0]-inport[0]
			print lenght
			#width=outport[1]-inport[1]

			mzi_t1 =  i3.Translation((-(self.mzi_position), 0.0))
			mzi_t2 = i3.HMirror() -mzi_t1
			if self.tipo==1:
				Sdown_t = i3.VMirror() + i3.Translation((-0.5*lenght+self.length_taper_wide, -0.5*self.refsig_d+2*self.R+2*self.coresensing))
				Sup_t=i3.Translation((-0.5*lenght+self.length_taper_wide, 0.5*self.refsig_d-2*self.R-2*self.coresensing))
			if self.tipo==2:
				Sdown_t = i3.VMirror() + i3.Translation((0.0, -0.5*self.refsig_d))
				Sup_t=i3.Translation((0.0, 0.5*self.refsig_d))				


			child_transformations={"mzi_1": mzi_t1,
                                               "mzi_2": mzi_t2,
                                               "Sup": Sup_t,
                                               "Sdown":Sdown_t

                                               }

			return child_transformations                        

########################################### DEFINITION OF CPUPLER #########################################

class GratingCoupler1Band(AutoTransitionPorts):
	core=i3.PositiveNumberProperty(default=2.2, doc="core width")	
	wg_coupler= i3.TraceTemplateProperty(doc="Wide trace template used")
	FGC= i3.ChildCellProperty(doc="grating used")
	ctipo=i3.PositiveNumberProperty(default=1, doc="type of coupler used ctipo=1 for grating and ctipo=2 for taper")	
	coupling_l=i3.PositiveNumberProperty(default=2.2, doc="length of coupling WG")	
	coupler_template= i3.TraceTemplateProperty(doc="Wide trace template used for coupler tipo2")
	waveguide_template= i3.TraceTemplateProperty(doc="Wide trace template used on routing")
	coupling_w = i3.PositiveNumberProperty(default=2.2, doc="width of the coupling WG")
	transition_length_coupler=i3.PositiveNumberProperty(default=100, doc="transition length of the coupler")	

	layName = i3.StringProperty(default = 'new')
	props = i3.DictProperty()	
	
	def _default_props(self):
		return AssignProcess(self.layName)	

	def _default_wg_coupler(self):
		wg_coupler = WireWaveguideTemplate()
		wg_coupler.Layout(core_width=25.0, cladding_width=25.0, **self.props)
		return wg_coupler
	
	def _default_waveguide_template(self):
		wg_t = WireWaveguideTemplate()
		wg_t_layout=wg_t.Layout(core_width=self.core, cladding_width=self.core, **self.props)

		return wg_t

	def _default_coupler_template(self):
		wg_t = WireWaveguideTemplate()
		wg_t_layout=wg_t.Layout(core_width=self.coupling_w, cladding_width=self.coupling_w, **self.props)

		return wg_t	

	def _default_trace_template(self):
		return self.waveguide_template  	


	def _default_contents(self):
		return self.FGC

	def _default_port_labels(self):
		return ["in","out"]

	def _default_FGC(self):
		if self.ctipo==1:
			FGC = UniformLineGrating(trace_template=self.wg_coupler)
			FGC_layout = FGC.Layout(period=1.89,
                                    line_width=1.89*0.47,
                                line_length=25.0,
                                n_o_periods=5,
                                socket_length=1.89*5,
			        )
		if self.ctipo==2:
			FGC=i3.Waveguide(trace_template=self.coupler_template)
			FGC.Layout(shape=[(-self.coupling_l*0.5, 0.0),(self.coupling_l*0.5, 0.0)])
		print 'The trace template of the coupler ',FGC.trace_template	
		return FGC #Tapered_FCG 


	class Layout(AutoTransitionPorts.Layout):

		def _default_transition_length(self):
			return self.transition_length_coupler

########################################### DEFINITION OF FULL CIRCUIT #########################################

class CombinedCircuit(PlaceAndAutoRoute):
	branch = i3.ChildCellProperty(doc="Branch used")
	coupler = i3.ChildCellProperty(doc="coupler used", locked=True)
	heater= i3.ChildCellProperty(doc="heater used")
	heater2= i3.ChildCellProperty(doc="second layer of heater used")
	aligningmark=i3.ChildCellProperty(doc="aligning mark")
	aligningmark_h=i3.ChildCellProperty(doc="aligning mark for heater")
	aligningmark_h2=i3.ChildCellProperty(doc="aligning mark for second layer of heater")
	flowcell=i3.ChildCellProperty(doc="aligning mark for second layer of heater")
	flowcellbox=i3.ChildCellProperty(doc="aligning mark for second layer of heater")
	
	chip_length=i3.PositiveNumberProperty(default=20000,doc="length of the chip")
	mzi_pos=i3.PositiveNumberProperty(default=5000,doc="position of mzi with respect to chip edge")
	radius=i3.PositiveNumberProperty(default=100,doc="radius or curvature of circuit")
	d=i3.NumberProperty(default=5,doc="distance mzi-heater")
	core=i3.PositiveNumberProperty(default=2.2, doc="core width")	        
	width=i3.PositiveNumberProperty(default=2.2, doc="narrow width of heaters")
	vline_l=i3.NumberProperty(default=2.2, doc="estra length for MZI")
	pads_w=i3.PositiveNumberProperty(default=2.2, doc=" width of heaters' pads")
	mmi12_port=i3.PositiveNumberProperty(default=15, doc=" width of MMI1x2 ports")
	mmi22_port=i3.PositiveNumberProperty(default=15, doc=" width of MMI1x2 ports")
	mmi12_w=i3.PositiveNumberProperty(default=15, doc=" width of MMI1x2")
	mmi22_w=i3.PositiveNumberProperty(default=15, doc=" width of MMI2x2")
	mmi12_l=i3.PositiveNumberProperty(default=15, doc=" lenght of MMI 1x2")
	mmi22_l=i3.PositiveNumberProperty(default=15, doc=" lenght of MMI 2x2")
	length_taper_mmi12=i3.PositiveNumberProperty(default=300, doc=" lenght of  taper of MMI 1x2")
	length_taper_mmi22=i3.PositiveNumberProperty(default=300, doc=" lenght of  taper of MMI 2x2")
	r_heater=i3.PositiveNumberProperty(default=50, doc="radius of curvature of connexion of heater arc with pads")
	tipo =i3.NumberProperty(default=2, doc="1=spiral, 2=wide waveguide")
	#tl=i3.PositiveNumberProperty(default=2.2, doc="transition length for the heaters")
	wide_wg_l = i3.NumberProperty(default=20, doc="Wide Waveguide")
	coupler_p=i3.NumberProperty(default=20, doc="position of the grating coupler with respect to the edge")
	ctipo=i3.PositiveNumberProperty(default=2.2, doc="type of coupler used ctipo=1 for grating and ctipo=2 for taper")	
	coupling_l=i3.PositiveNumberProperty(default=2.2, doc="length of coupling WG")
	coupling_w=i3.PositiveNumberProperty(default=2.2, doc="length of coupling WG")
	refsig_d=i3.PositiveNumberProperty(default=2.2, doc="separation between reference and signal waveguides")
	coresensing=i3.PositiveNumberProperty(default=50, doc="separation between reference and signal waveguides")
	contact_w=i3.PositiveNumberProperty(default=1000, doc="core thickness")
	length_taper_wide=i3.PositiveNumberProperty(default=1000, doc="Length of taper for detection region")
	transition_length_coupler=i3.PositiveNumberProperty(default=500, doc="transition length of the coupler")
	#aligningmark=i3.ChildCellProperty(doc="aligning mark for circuit used")
	
	#aligningmark_2=i3.ChildCellProperty(doc="second aligning mark for circuit")
	
	
	
	layName_h = i3.StringProperty(default = 'standard', doc = 'options: standard, new')
	layName_h2 = i3.StringProperty(default = 'standard', doc = 'options: standard, new')
	layName_c = i3.StringProperty(default = 'standard', doc = 'options: standard, new')
	layName_f = i3.StringProperty(default = 'standard', doc = 'options: standard, new')
	separation=i3.NumberProperty(default=100.0, doc="separation between cross and gratings")
	size=i3.NumberProperty(default=100.0, doc="Size of the cross of aligning marks")
	
	OutRing_w=i3.PositiveNumberProperty(default=1250, doc="core thickness")
	InRing_w=i3.PositiveNumberProperty(default=500, doc="core thickness")
	R_out=i3.PositiveNumberProperty(default=2750, doc="Radius of curvature of the arc")
	R_in=i3.PositiveNumberProperty(default=1500, doc="Radius of curvature of the arc")	
	#Layers=i3.process.layer_map.GenericGdsiiPPLayerInputMap()

	#def _default_gdsiilayer_map(self):
		#return (1,2)

	print 'core width',core
	print 'heater width', width

	def _default_trace_template(self):
		return self.branch.trace_template


	def _default_child_cells(self):

		child_cells={"branch_1" : self.branch,
                             #"branch_2" : self.branch,
                             "incoupling" : self.coupler,
                             "outcoupling" : self.coupler,
                             "heater1" : self.heater,
                             "heater2" : self.heater,
		             
		             "heater3" : self.heater2, 
		             "heater4" : self.heater2,		             
		             
                             "am1"     : self.aligningmark,
		             "am2"     : self.aligningmark,
		             "am3"     : self.aligningmark,
		             "am4"     : self.aligningmark,
		             
		             "am5"     : self.aligningmark_h,
		             "am6"     : self.aligningmark_h,
		             "am7"     : self.aligningmark_h,
		             "am8"     : self.aligningmark_h,
		             
		             "am9"     : self.aligningmark_h2,
		             "am10"     : self.aligningmark_h2,
		             "am11"     : self.aligningmark_h2,
		             "am12"     : self.aligningmark_h2,	
		             
		             "am13"     : self.aligningmark,
		             "am14"     : self.aligningmark,
		             "am15"     : self.aligningmark,
		             "am16"     : self.aligningmark,
		             
		             "flowcell_up"     : self.flowcell,
		             "flowcell_down"     : self.flowcell,
		             "flowcellbox" : self.flowcellbox,
                     }
		return child_cells

	def _default_links(self):
		links = [("branch_1:mzi_1_mmi12_in", "incoupling:out"),
                         ("branch_1:mzi_2_mmi12_in","outcoupling:out"),
                         #("branch_2:in", "incoupling:in"),
                         #("branch_2:out","outcoupling:out")
                         ]
	# To be added: links to in and out-coupling gratings  
		return links
	
	def _default_flowcellbox(self):
		fc=flowcellbox()
		return fc	
	
	def _default_flowcell(self):
		fc=Flowcell(layName=self.layName_f, OutRing_w=self.OutRing_w, InRing_w=self.InRing_w, R_out=self.R_out, R_in=self.R_in)
		return fc	

	def _default_aligningmark(self):
		am=AligningMarks(layName=self.layName_c, separation=self.separation, size=self.size)
		return am
	
	def _default_aligningmark_h(self):
		am=AligningMarks(layName=self.layName_h, separation=self.separation, size=self.size)
		return am	
	
	def _default_aligningmark_h2(self):
		am=AligningMarks(layName=self.layName_h2, separation=self.separation, size=self.size)
		return am

	def _default_branch(self):
		i=0
		print 'mzi position in Combined Circuit:', self.chip_length*0.5-self.mzi_pos
		branch = Branch(mzi_position=self.chip_length*0.5-self.mzi_pos, name='circuit', 
                                R=self.radius, vline_l=self.vline_l, core=self.core, mmi12_port=self.mmi12_port,
                                mmi22_port=self.mmi22_port, mmi12_l=self.mmi12_l, mmi22_l=self.mmi22_l, 
                                length_taper_mmi22=self.length_taper_mmi22, length_taper_mmi12=self.length_taper_mmi12,
                                mmi12_w=self.mmi12_w, mmi22_w=self.mmi22_w, tipo=self.tipo,wide_wg_l=self.wide_wg_l,
                                refsig_d=self.refsig_d, coresensing=self.coresensing, length_taper_wide=self.length_taper_wide,
		                layName=self.layName_c,
                        )     

		print 'the trace template of branch is', branch.trace_template                
		
		i=i+1
		print i
		return branch 

	def _default_heater(self):
		heater = Heater(contact_pos=self.mzi_pos-2000, r=self.radius+self.d+0.5*self.width+self.core*0.5#+self.core*0.5+self.width*0.5
                                , width=self.width, pads_w=self.pads_w,r_heater=self.r_heater, contact_w=self.contact_w, 
		                layName = self.layName_h) 
		layout_heater = heater.Layout(bend_radius=20.0)
		print 'the trace template of the heater is', heater.trace_template 
		  

		return heater 
	
	def _default_heater2(self):
		heater = Heater(contact_pos=self.mzi_pos-2000, r=self.radius+self.d+0.5*self.width+self.core*0.5#+self.core*0.5+self.width*0.5
                                , width=self.width, pads_w=self.pads_w,r_heater=self.r_heater, contact_w=self.contact_w, 
		                layName = self.layName_h2) 
		layout_heater = heater.Layout(bend_radius=20.0)
		print 'the trace template of the heater is', heater.trace_template 
		  

		return heater 	

	def _default_coupler(self):
		print 'I am in the coupler'
		coupler = GratingCoupler1Band(coupling_l=self.coupling_l, ctipo=self.ctipo, coupling_w=self.coupling_w, layName = self.layName_c)
		layout_coupler=coupler.Layout(transition_length_coupler=self.transition_length_coupler,
		                              )
		print 'The trace template of the coupler is ', coupler.trace_template
		return coupler

	def _default_vline_l(self):
		return self.r_heater       

	class Layout(PlaceAndAutoRoute.Layout):
		def _default_child_transformations(self):
			
			incoupler_t =fc_t1 = i3.Rotation(rotation=00.0) + i3.Translation(translation=(-(self.chip_length*0.5-self.coupler_p),0.0))
			outcoupler_t = i3.Rotation(rotation=180.0) + i3.Translation(translation=(self.chip_length*0.5-self.coupler_p,0.0))
			mziport_t= i3.Translation(translation=(0.0,0.5*self.mmi12_w-0.5*self.mmi12_port))
			mziarc_t=i3.Translation(translation=(0.0,self.radius+self.vline_l-2*self.r_heater))
			pads_t=i3.Translation(translation=(0.0,-0.5*self.pads_w))
			

			child_transformations={"branch_1": (0, 0),

                                               "incoupling":incoupler_t,
                                                "outcoupling":outcoupler_t,
                                                "heater1" : i3.Translation(translation=(-(self.chip_length*0.5-self.mzi_pos),0.0))+mziport_t+mziarc_t,
                                                "heater3" :  i3.HMirror() + i3.Translation(translation=(self.chip_length*0.5-self.mzi_pos,0.0))+mziport_t+mziarc_t,
			                        "heater4" : i3.Translation(translation=(-(self.chip_length*0.5-self.mzi_pos),0.0))+mziport_t+mziarc_t,
			                                                                        "heater2" :  i3.HMirror() + i3.Translation(translation=(self.chip_length*0.5-self.mzi_pos,0.0))+mziport_t+mziarc_t,			                        
			                        
                                                "am1"     :   i3.Translation(translation=(self.chip_length*0.5-1000,6000)),
			                        "am2"     :   i3.Translation(translation=(-self.chip_length*0.5+1000,6000)),
			                        "am3"     :   i3.Translation(translation=(-self.chip_length*0.5+1000,-6000)),
			                        "am4"     :   i3.Translation(translation=(self.chip_length*0.5-1000,-6000)) ,
			                        
			                        "am5"     :  i3.VMirror() + i3.Translation(translation=(self.chip_length*0.5-1000,6000 + self.separation +self.size)),
			                        "am6"     :  i3.VMirror() +i3.Translation(translation=(-self.chip_length*0.5+1000,6000 + self.separation +self.size)),
			                        "am7"     :  i3.VMirror() +i3.Translation(translation=(-self.chip_length*0.5+1000,-6000 + self.separation +self.size)),
			                        "am8"     :  i3.VMirror() +i3.Translation(translation=(self.chip_length*0.5-1000,-6000 + self.separation +self.size)),			                        
			                        
			                        "am9"     :  i3.VMirror() + i3.Translation(translation=(self.chip_length*0.5-1500,5500 + self.separation +self.size)),
			                        "am10"     :  i3.VMirror() +i3.Translation(translation=(-self.chip_length*0.5+1500,5500 + self.separation +self.size)),
			                        "am11"     :  i3.VMirror() +i3.Translation(translation=(-self.chip_length*0.5+1500,-5500 + self.separation +self.size)),
			                        "am12"     :  i3.VMirror() +i3.Translation(translation=(self.chip_length*0.5-1500,-5500 + self.separation +self.size)),
			                        
			                        "am13"     :   i3.Translation(translation=(self.chip_length*0.5-1500,5500)),
			                        "am14"     :   i3.Translation(translation=(-self.chip_length*0.5+1500,5500)),
			                        "am15"     :   i3.Translation(translation=(-self.chip_length*0.5+1500,-5500)),
			                        "am16"     :   i3.Translation(translation=(self.chip_length*0.5-1500,-5500)) ,	
			                        
			                        "flowcell_up"     :  i3.Rotation(rotation=90.0)+ i3.Translation(translation=(0.0,self.R_out+250)) ,
			                        "flowcell_down"     :  i3.Rotation(rotation=90.0)+ i3.Translation(translation=(0.0,-(self.R_out+250)) ),
			                        "flowcellbox"      :  i3.Rotation(rotation=90.0)+ i3.Translation(translation=(0.0,0.0 )),
			                        
                                    }                        


			return child_transformations     


		def _default_bend_radius(self):
			return self.radius+self.core*0.5


########################################### PARAMETERS INPUT #########################################
#mmi12_port=6.75 for ebeam
# tipo=1 --> Spirals, tipo=2 --> waveguide
#cell=CombinedCircuit(chip_length=20000, mzi_pos=5000, radius=200, core=2, width=3, d=5, vline_l=10, pads_w=20, mmi12_port=10, mmi22_port=10, mmi12_w=22, mmi22_w=22, r_heater=10)
cell=CombinedCircuit(tipo=1,chip_length=20000, mzi_pos=3000, radius=200+0.5*2, core=3.3, width=2, d=3, pads_w=75,
                     mmi12_port=8.75, mmi22_port=8.75, mmi12_w=20, mmi22_w=20, 
                     length_taper_mmi12=200,length_taper_mmi22=200, mmi12_l=110, mmi22_l=435,
                     r_heater=10, wide_wg_l=6000, coupler_p=0, coupling_l=3000, ctipo=2, 
                     coupling_w=15, refsig_d=6000, coresensing=50, contact_w=500, 
                     length_taper_wide=3000, transition_length_coupler=500, 
                     layName_h='metal', layName_c='waveguide', layName_h2='metal2',layName_f='flowcell',
                     separation=100, size=250)

########################################### VISUALIZATION AND GDSII #########################################

lv = cell.Layout()
lv.write_gdsii("Heaters for R200.gds")
lv.visualize()
#lv.visualize(annotate=True)    







