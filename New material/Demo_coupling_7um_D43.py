





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
		#cladding_process = i3.TECH.PROCESS.WG
		cladding_process = i3.TECH.PROCESS.RWG
		core_purpose = i3.TECH.PURPOSE.DF_AREA
		cladding_purpose = i3.TECH.PURPOSE.LF.LINE
		#cladding_purpose = i3.TECH.PURPOSE.DF_AREA
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


########################################### DEFINITION OF CHIP EDGES ########################



class flowcellbox(i3.PCell):

	
	#widthchip = i3.PositiveNumberProperty(default=15000)
	#heightchip = i3.PositiveNumberProperty(default=20000)
	widthchip = i3.PositiveNumberProperty(default=15000)
	heightchip = i3.PositiveNumberProperty(default=20000)	
	
	

	class Layout(i3.LayoutView):
		layer = i3.LayerProperty(default=i3.TECH.TRACE.DEFAULT_LAYER)
		#layer_c = i3.LayerProperty(default=i3.TECH.TRACE.DEFAULT_LAYER)
		def _default_layer(self):
			layer=PPLayer(process=i3.TECH.PROCESS.WG,purpose=i3.TECH.PURPOSE.LF.LINE)
			return layer
		
		def _generate_elements(self, elems):
			elems += i3.Rectangle(layer=self.layer, box_size=(self.heightchip,self.widthchip))
						
			return elems

		
########################################### DEFINITION OF ALIGNING MARKS #########################################

class Square(PlaceComponents):

	size=i3.PositiveNumberProperty(default=20.0, doc="simension of the square of aligning mark")
	separation=i3.PositiveNumberProperty(default=2.0, doc="simension of the square of aligning mark")
	square = i3.ChildCellProperty(doc="grating with pitch 1", locked=True)
        tt_square = i3.TraceTemplateProperty(doc="Wide trace template used ")
	layName = i3.StringProperty(default = 'new')
	props = i3.DictProperty()
	
	def _default_props(self):
		return AssignProcess(self.layName)
	

	def _default_tt_square(self):
		tt_w = WireWaveguideTemplate()
		tt_w.Layout(core_width=(self.size),
                    cladding_width=(self.size),
		    **self.props
                    )
		print 'ttw in Square is ', tt_w
		
		return tt_w

	def _default_square(self):
		rect=i3.Waveguide(trace_template=self.tt_square)
		layout_rect = rect.Layout(shape=[(0.0, self.size/2.0),(self.size,self.size/2.0)])
		print 'The trace template of the hline of the cross ', rect.trace_template 
		return rect
       

	def _default_child_cells(self):
		child_cells={"S1" : self.square,
                           }        

		return child_cells



	class Layout(PlaceComponents.Layout):
		def _default_child_transformations(self):

			child_transformations={
			        "S1" : i3.Translation(translation=(-(self.size*0.5),(-self.size*0.5))),
                                   }

			return child_transformations	

class AligningMarks(PlaceComponents):

	tt_cross = i3.TraceTemplateProperty(doc="Wide trace template used for the contact pads")
	hline = i3.ChildCellProperty(doc="Horizontal line", locked=True)
	vline = i3.ChildCellProperty(doc="Vertical", locked=True)
	square = i3.ChildCellProperty(doc="Vertical", locked=True)
	size=i3.PositiveNumberProperty(default=250.0, doc="bigger dimension of aligning mark")
	width=i3.PositiveNumberProperty(default=20.0, doc="smaller dimension of aligning mark")
	#Pitch1=i3.PositiveNumberProperty(default=2.0, doc="pitch grating 1")	
	separation=i3.NumberProperty(default=100.0, doc="separation between cross and gratings")

	#dc=i3.PositiveNumberProperty(default=0.47, doc="duty cycle") 
	
	layName = i3.StringProperty(default = 'metal2')
	props = i3.DictProperty()	
			
		
	def _default_props(self):
		return AssignProcess(self.layName)		

	def _default_tt_cross(self):
		tt_w = WireWaveguideTemplate()
		tt_w.Layout(core_width=(self.width),
                    cladding_width=(self.width),
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
		#square=Square(size=self.width, layName=self.layName)
		square=Square(size=self.width, layName='metal')
		#square.Layout().visualize()
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

			child_transformations={"S1" : i3.Translation(translation=(-(self.width+5.0),(self.width+5.0))),
			                       "S2" : i3.Translation(translation=((self.width+5.0),(self.width+5.0))),
			                       "S3" : i3.Translation(translation=(-(self.width+5.0),-(self.width+5.0))), 
			                       "S4" : i3.Translation(translation=((self.width+5.0),-(self.width+5.0))), 
			                       "V"  : i3.Translation(translation=(0.0, 0.0))+ i3.Translation(translation=(-(self.size)/2.0,-(self.size)/2.0)),
			                       "H"  : i3.Translation(translation=(0.0, 0.0))+ i3.Translation(translation=(-(self.size)/2.0,-(self.size)/2.0))				           
                                 }   


			return child_transformations

	

class Lens(i3.PCell):

	Diameter = i3.PositiveNumberProperty(default=250)
	
	
	class Layout(i3.LayoutView):
		#layer = i3.LayerProperty(default=i3.TECH.TRACE.DEFAULT_LAYER)
		layer_c = i3.LayerProperty(default=i3.TECH.TRACE.DEFAULT_LAYER)
		#def _default_layer(self):
			#layer=PPLayer(process=i3.TECH.PROCESS.WG,purpose=i3.TECH.PURPOSE.LF.LINE)
			#return layer
		
		def _default_layer_c(self):
			layer=PPLayer(process=i3.TECH.PROCESS.SK,purpose=i3.TECH.PURPOSE.DF_AREA)
			return layer		

		def _generate_elements(self, elems):
			#elems += i3.Rectangle(layer=self.layer, box_size=(self.width, self.height))
			elems += i3.Circle(layer=self.layer_c, center=(0.0, 0.0), radius=self.Diameter*0.5)
			
			return elems

########################################### DEFINITION OF waveguides #########################################

                      

class GratingCoupler1Band(PlaceComponents):
	core=i3.PositiveNumberProperty(default=3.3, doc="core width")
	period=i3.PositiveNumberProperty(default=2.566, doc="core width")
	duty=i3.PositiveNumberProperty(default=0.403, doc="core width")
	nperiods=i3.PositiveNumberProperty(default=7, doc="core width")
	wg_coupler= i3.TraceTemplateProperty(doc="Wide trace template used")
	#FGC= i3.ChildCellProperty(doc="grating used")
	ctipo=i3.PositiveNumberProperty(default=1, doc="type of coupler used ctipo=1 for grating and ctipo=2 for taper")	
	coupling_l=i3.PositiveNumberProperty(default=5000, doc="length of coupling WG")	
	coupler_template= i3.TraceTemplateProperty(doc="Wide trace template used for coupler tipo2")
	waveguide_template= i3.TraceTemplateProperty(doc="Wide trace template used on routing")
	coupling_w = i3.PositiveNumberProperty(default=20, doc="width of the coupling WG")
	transition_length_coupler=i3.PositiveNumberProperty(default=300, doc="transition length of the coupler")
	Grating_list = i3.ChildCellListProperty(doc="List containing the non etched parts of gratings")
	inPort = i3.ChildCellProperty( doc="Used for ports")
	outPort = i3.ChildCellProperty( doc="Used for ports")
	incouplingWG = i3.ChildCellProperty( doc="Used for ports")
	outcouplingWG = i3.ChildCellProperty( doc="Used for ports")
	chirp=i3.NumberProperty(default=1, doc="1=chirped")
	socket_length=i3.PositiveNumberProperty(default=2.2, doc="length of coupling WG")

	layName = i3.StringProperty(default = 'waveguide')
	layNameg = i3.StringProperty(default = 'metal')
	print 'the name of the layer is', layName
	props = i3.DictProperty()	
	
	def _default_props(self):
		return AssignProcess(self.layName)

	propsg = i3.DictProperty()	
		
	def _default_propsg(self):
		return AssignProcess(self.layNameg)	 
		
	
	Lo = i3.ListProperty(default=[]) #Non etched part, illuminated during e-beam
	Le = i3.ListProperty(default=[]) #Etched part
	Loc = i3.ListProperty(default=[]) #Non etched part, illuminated during e-beam
	Lec = i3.ListProperty(default=[]) #Etched part	

	
	#def _default_transition_length(self):
		#return self.transition_length_coupler
	
	def _default_socket_length(self):
		a=sum(self.Lo)+sum(self.Le)
		#if self.chirp==1:
			#A=a=self.period * int(self.nperiods)+sum(self.Loc))
		return a
	def _default_Loc(self):
		
		#Loc=[2.175,2.122,2.07,2.016,1.963,1.908,1.854,1.798,1.743,1.687,1.63,1.573,
			    #1.515,1.457,1.398,1.339,1.279,1.219,1.158,1.096]
		Loc=self.Loc
		Loc.reverse()
		return Loc
	
	def _default_Lec(self):
			
		#Lec=[0.242,0.301,0.361,0.421,0.482,0.543,0.605,0.667,0.73,0.794,0.858,0.922, 
	             #0.988,1.054,1.12,1.187,1.255,1.323,1.392,1.462]
		Lec=self.Lec
		Lec.reverse()
		return Lec	
	
	def _default_Lo(self):
		A=[None] * int(self.nperiods)
		if self.chirp==1:
			A=[None] * int(self.nperiods+len(self.Loc))
		
		for x in range(0,int(self.nperiods)):
			A[x]=self.period*self.duty
			if self.chirp==1:
				for x in range(0,int(len(self.Loc))):
					print x
					print len(self.Loc)
					A[int(self.nperiods)+x]=self.Loc[x]
			
			print 'Lo: ',A
			
		return A	
	
	
	def _default_Le(self):
		Le=[None] * int(self.nperiods)
		if self.chirp==1:
			Le=[None] * int(self.nperiods+len(self.Loc))		
		for x in range(0,int(self.nperiods)):
			Le[x]=self.period*(1-self.duty)
			if self.chirp==1:
				for x in range(0,int(len(self.Loc))):
					Le[int(self.nperiods)+x]=self.Lec[x]			
			print 'Le: ',Le
			
		return Le	
	
	def _default_Grating_list(self):
		Grating_list = [] 
		for x in range(0,int(len(self.Lo))):
			#rect=i3.Waveguide(trace_template=self.wg_coupler)
			rect=i3.Waveguide(trace_template=self.coupler_template)
			
			#layout_rect = rect.Layout(shape=[(0.0, 0.0),(self.Lo[x],0.0)])#.visualize(annotate=True)
			layout_rect = rect.Layout(shape=[(0.0, 0.0),(self.Lo[x],0.0)])#.visualize(annotate=True)
			                          
		 		
			Grating_list.append(rect)
		return Grating_list
	
	def _default_incouplingWG(self):
		rect=i3.Waveguide(trace_template=self.wg_coupler)
		layout_rect = rect.Layout(shape=[(0.0, 0.0),(self.coupling_l,0.0)]
			                  )
		return rect	

	def _default_outcouplingWG(self):
		rect=i3.Waveguide(trace_template=self.wg_coupler)
		layout_rect = rect.Layout(shape=[(0.0, 0.0),(50+self.socket_length,0.0)]
	                                  )
		return rect	
	
	def _default_inPort(self):
		Port=AutoTransitionPorts(contents=self.incouplingWG,
			                 port_labels=["in"],
			                     trace_template=self.waveguide_template)
		layout_Port = Port.Layout(transition_length=self.transition_length_coupler)#.visualize(annotate=True)
		return Port
	
	def _default_outPort(self):
		Port=AutoTransitionPorts(contents=self.outcouplingWG,
	                                 port_labels=["in"],
	                                     trace_template=self.wg_coupler)
		layout_Port = Port.Layout(transition_length=10)#.visualize(annotate=True)
		return Port	
	
	def _default_child_cells(self):
		child_cells = {}          # First we define the property "child_cells" as  an empty dictionary
	
		for counter, pillar  in enumerate(self.Grating_list):
			child_cells['pillar{}'.format(counter)] = pillar
			
			print pillar
			print 'name of pillar:', pillar.name
			
		child_cells['InPort'] = self.inPort
		child_cells['OutPort']= self.outPort
		print 'child_cells:', child_cells
		return child_cells	
	
	def _default_props(self):
		return AssignProcess(self.layName)	

	def _default_wg_coupler(self):
		wg_coupler = WireWaveguideTemplate()
		wg_coupler.Layout(core_width=self.coupling_w, cladding_width=self.coupling_w+2*8, **self.props)
		return wg_coupler
	
	def _default_waveguide_template(self):
		wg_t = WireWaveguideTemplate()
		wg_t_layout=wg_t.Layout(core_width=self.core, cladding_width=self.core+2*8, **self.props)
				
		return wg_t

	def _default_coupler_template(self):
		wg_t = WireWaveguideTemplate()
		wg_t_layout=wg_t.Layout(core_width=self.coupling_w, cladding_width=self.coupling_w, **self.propsg)

		return wg_t	

	def _default_trace_template(self):
		return self.waveguide_template  	


	def _default_contents(self):
		return self.FGC

	def _default_port_labels(self):
		return ["out"]

	


	class Layout(PlaceComponents.Layout):

		#def _default_transition_length(self):
			#return self.transition_length_coupler
		
		def _default_child_transformations(self):
			d={}
			position=0
			for counter, child  in enumerate(self.Grating_list):
				
				d['pillar{}'.format(counter)] = i3.Translation(translation=(position, 0.0))
				position=position+self.Lo[counter]+self.Le[counter]
				print 'pillar position: ', position
				print 'counter= ', counter
				print 'Lo: ', self.Lo[counter]
				print 'Le: ', self.Le[counter]
				
			#d['InPort'] = i3.HMirror()+ i3.Translation(translation=(position+10,0))
			d['InPort'] = i3.HMirror()+ i3.Translation(translation=(self.coupling_l+self.socket_length,0))
			d['OutPort'] = i3.Translation(translation=(-50,0.0))
												   
			return d			
		
		
		
########################################### DEFINITION OF FULL CIRCUIT #########################################

class CombinedCircuit(PlaceAndAutoRoute):
	L1=i3.PositiveNumberProperty(default=100,doc="radius or curvature of circuit")

	incoupler = i3.ChildCellProperty(doc="coupler used", locked=True)
	outcoupler = i3.ChildCellProperty(doc="coupler used", locked=True)

	aligningmark=i3.ChildCellProperty(doc="aligning mark")
	lens=i3.ChildCellProperty(doc="flowcellbox")
	flowcellbox=i3.ChildCellProperty(doc="lens")
	aligningmark_h=i3.ChildCellProperty(doc="aligning mark for heater")
	coupling_l=i3.PositiveNumberProperty(default=5+2*270, doc="length of coupling WG")	
	coupling_win = i3.PositiveNumberProperty(default=15, doc="width of the coupling WG")
	coupling_wout = i3.PositiveNumberProperty(default=15, doc="width of the coupling WG")	
	chip_length=i3.PositiveNumberProperty(default=20000,doc="length of the chip")
	
	radius=i3.PositiveNumberProperty(default=100,doc="radius or curvature of circuit")

	core=i3.PositiveNumberProperty(default=3.3, doc="core width")	        
	width=i3.PositiveNumberProperty(default=3.3, doc="narrow width of heaters")
	tipo =i3.NumberProperty(default=2, doc="1=spiral, 2=wide waveguide")
	
	
	wide_wg_l = i3.NumberProperty(default=20, doc="Wide Waveguide")
	coupler_p=i3.NumberProperty(default=20, doc="position of the grating coupler with respect to the edge")
	ctipoin=i3.PositiveNumberProperty(default=2, doc="type of coupler used ctipo=1 for grating and ctipo=2 for taper")
	ctipoout=i3.PositiveNumberProperty(default=1, doc="type of coupler used ctipo=1 for grating and ctipo=2 for taper")
	transition_length_couplerin=i3.PositiveNumberProperty(default=500, doc="transition length of the coupler")
	transition_length_couplerout=i3.PositiveNumberProperty(default=500, doc="transition length of the coupler")
	aligningmark=i3.ChildCellProperty(doc="aligning mark for circuit used")
	
	increment=i3.NumberProperty(default=0, doc="core width")
	
	periodin=i3.PositiveNumberProperty(default=1.73, doc="core width")
	dutyin=i3.PositiveNumberProperty(default=0.5, doc="core width")
	nperiodsin=i3.PositiveNumberProperty(default=8, doc="core width")
	
	periodout=i3.PositiveNumberProperty(default=2.566, doc="core width")
	dutyout=i3.PositiveNumberProperty(default=0.403, doc="core width")
	nperiodsout=i3.PositiveNumberProperty(default=20, doc="core width")	
	
	Loc = i3.ListProperty(default=[]) #Non etched part, illuminated during e-beam
	Lec = i3.ListProperty(default=[]) #Etched part	
	
	
	layName_h = i3.StringProperty(default = 'standard', doc = 'options: standard, new')
	layName_h2 = i3.StringProperty(default = 'standard', doc = 'options: standard, new')
	layName_c = i3.StringProperty(default = 'standard', doc = 'options: standard, new')
	layName_f = i3.StringProperty(default = 'standard', doc = 'options: standard, new')
	separation=i3.NumberProperty(default=100.0, doc="separation between cross and gratings")
	size=i3.NumberProperty(default=250.0, doc="Size of the cross of aligning marks")
	
	print 'core width',core
	print 'heater width', width

	def _default_trace_template(self):
		return self.incoupler.inPort.trace_template
	
	
	def _default_Lec(self):
			
		#Loc=[2.175,2.122,2.07,2.016,1.963,1.908,1.854,1.798,1.743,1.687,1.63,1.573,
			    #1.515,1.457,1.398,1.339,1.279,1.219,1.158,1.096] #version A
		Loc=[2.043,1.643] #1um etch for 2um GOS
		#Loc=[1,1,1,1,1,1,1]
		Loc.reverse()
		return Loc
		
	def _default_Loc(self):
			
		#Lec=[0.242,0.301,0.361,0.421,0.482,0.543,0.605,0.667,0.73,0.794,0.858,0.922, 
		     #0.988,1.054,1.12,1.187,1.255,1.323,1.392,1.462] #version A
		Lec=[0.511,0.949] #1um etch for 2um GOS
		#Lec=[0.4,0.5,0.6,0.7,0.8,0.9,1]
		Lec.reverse()
		return Lec	

	def _default_child_cells(self):

		child_cells={
                             "incoupling1" : self.incoupler,
                             "outcoupling1" : self.outcoupler,
		             
		             
		             
                           #  "am1"     : self.aligningmark,
		           #  "am2"     : self.aligningmark,
		           #  "am3"     : self.aligningmark,
		           #  "am4"     : self.aligningmark,
		             
		           #  "inlens1" : self.lens,
		            # "outlens1" : self.lens,
		            	             
		            # "chip" : self.flowcellbox
		             	            
                     }
		return child_cells

	def _default_links(self):
		links = [( "incoupling1:InPort_in","outcoupling1:InPort_in"),
		        
                         
                         ]
	
		return links
	
	

	def _default_aligningmark(self):
		am=AligningMarks(layName='metal2', separation=self.separation, size=self.size)
		return am
	
	def _default_aligningmark_h(self):
		am=AligningMarks(layName=self.layName_h, separation=self.separation, size=self.size)
		return am	
	
	def _default_aligningmark_h2(self):
		am=AligningMarks(layName=self.layName_h2, separation=self.separation, size=self.size)
		return am


	def _default_outcoupler(self):
		print 'I am in the coupler'
		coupler = GratingCoupler1Band(coupling_l=self.coupling_l+self.increment, chirp=self.ctipoout, coupling_w=self.coupling_wout,core=self.core, 
		                              layName = self.layName_c, period=self.periodout, duty=self.dutyout, nperiods=self.nperiodsout,
						Loc=self.Loc,
		                                Lec=self.Lec,
		                                transition_length_coupler=self.transition_length_couplerout,
		                                )		
		#layout_coupler=coupler.Layout(transition_length_coupler=self.transition_length_couplerout,
		                              #)#.visualize(annotate=True)
		
		return coupler
	
	def _default_incoupler(self):
		print 'I am in the coupler'
		coupler = GratingCoupler1Band(coupling_l=self.coupling_l, chirp=self.ctipoin, coupling_w=self.coupling_win,core=self.core, 
	                                      layName = self.layName_c, period=self.periodin, duty=self.dutyin, nperiods=self.nperiodsin,
	                                        Loc=self.Loc,
	                                        Lec=self.Lec,
		                                transition_length_coupler=self.transition_length_couplerin,
	                                        )		
		##layout_coupler=coupler.Layout(transition_length_coupler=self.transition_length_couplerin,
	                                      #)#.visualize(annotate=True)
		
		return coupler	

	def _default_lens(self):
		lens=Lens()
		return lens	
	def _default_flowcellbox(self):
		fl=flowcellbox()
		return fl	


	class Layout(PlaceAndAutoRoute.Layout):
		def _default_child_transformations(self):
			
			incoupler_t =fc_t1 = i3.Rotation(rotation=00.0) #+ i3.Translation(translation=(-(self.chip_length*0.5-self.coupler_p),0.0))
			outcoupler_t = i3.Rotation(rotation=180.0) #+ i3.Translation(translation=(self.chip_length*0.5-self.coupler_p,0.0))
			
			L1=self.L1
			
			#s=270
			s=0
			#z=2500
			z=0
			#socket_length=2*self.period*int(self.nperiods)+2*10
			socket_lengthout=2*(sum(self.Lec)+sum(self.Loc))+2*self.periodout*int(self.nperiodsout)+1*10
			socket_lengthin=2*self.periodin*int(self.nperiodsin)+0*10
			xin=0.75*self.periodin*int(self.nperiodsin)
			xout=0.75*(self.periodout*int(self.nperiodsout)+sum(self.Lec)+sum(self.Loc))
			print "socket_lengthout: ", socket_lengthout
			print "socket_lengthin: ", socket_lengthin
			#print self.child_cells['incoupling1'].FGC.Layout.socket_length
			child_transformations={                                   
                                               
			                        
			                        #"incoupling1"     :   i3.Rotation(rotation=00.0) +i3.Translation(translation=(-z-socket_lengthin#-50.0#-self.transition_length_couplerin
			                                                                                                      #,-s)),
			                        #"outcoupling1"     :   i3.Rotation(rotation=180.0) +i3.Translation(translation=(L1#+50.0#+self.transition_length_couplerout+self.increment-z
			                                                                                                        #,-s)),
			                        "incoupling1"     :   i3.Rotation(rotation=00.0) +i3.Translation(translation=(-z#-socket_lengthin#-50.0#-self.transition_length_couplerin
			                                                                                                                                                              ,-s)),
			                        "outcoupling1"     :   i3.Rotation(rotation=180.0) +i3.Translation(translation=(L1+socket_lengthout-100#+50.0#+self.transition_length_couplerout+self.increment-z
			                                                                                                                                                                ,-s)),

 
			                        # "inlens1"     :   i3.Rotation(rotation=00.0) +i3.Translation(translation=(-z-self.transition_length_couplerin-socket_lengthin+xin,-s)),
			                         #"outlens1"     :   i3.Rotation(rotation=180.0) +i3.Translation(translation=(L1+self.transition_length_couplerin+self.increment-z-xin,-s)),
			                         
			                       #  "am1"     :   i3.Translation(translation=(self.chip_length*0.5-1000,0.0)),
			                       #  "am2"     :   i3.Translation(translation=(-self.chip_length*0.5+1000,0.0)),
			                       #  "am3"     :   i3.Translation(translation=(-self.chip_length*0.5+5000,0.0)),
			                       #  "am4"     :   i3.Translation(translation=(self.chip_length*0.5-5000,0.0)) ,			                       

                                    }                        


			return child_transformations
		def _generate_elements(self, elems):
		
			elems += i3.PolygonText(layer= i3.TECH.PPLAYER.WG.TEXT, text='period={}_duty={}_n={}_width={}'.format(self.periodin,
		                                                                                                      self.dutyin,
			                                                                                              self.nperiodsin,
		                                                                                                      self.core),
		                                #coordinate=(-(op[0]-ip[0])/2-1000.0, -(self.n+0.5)*counter*sx-50.0),
		                                #alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
		                                #font = 2,
		                                #height=20.0)


		                                coordinate=(0.0, -20),
		                                alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
		                                font = 2,
		                                height=20.0)                
			return elems



		def _default_bend_radius(self):
			return self.radius+self.core*0.5


########################################### PARAMETERS INPUT #########################################
#mmi12_port=6.75 for ebeam


# N0 in F out
#cell=CombinedCircuit(chip_length=20000,  radius=200, core=3.5,layName_h='metal',
                     #layName_c='waveguide', layName_h2='metal2',layName_f='flowcell',
                     ##dutyout=0.4656, periodout= 2.6310, nperiodsout=38,
		     #dutyout=0.4656, periodout= 2.6310, nperiodsout=38,		     
                     #dutyin=0.5, periodin=1.83, nperiodsin=8, L1=4500, increment=-2*270, ctipoout=1,
                                          
                     #)
# 1)L1=10000, increment=8000 -->  3928 WG  ~4mm
# 2)L1=15000, increment=3000 -->  8928 WG  ~9mm
# 3)L1=18000, increment=0 --> 11927  WG    ~12mm
# 4)L1=12000, increment=6000 --> 5927  WG  ~6mm
# 5)L1=10000-3923, increment=8000+3923 -->  4.745 WG ~0
# 2)L1=14000, increment=4000 -->  8928 WG  ~9mm  *************

## N0 in N0 out
#cell=CombinedCircuit(chip_length=20000,  radius=200, core=3.5,layName_h='metal',
                     #layName_c='waveguide', layName_h2='metal2',layName_f='flowcell',
                     ##dutyout=0.5, periodout= 1.87, nperiodsout=7,
                     ##dutyin=0.5, periodin=1.87, nperiodsin=7, L1=6000, increment=0, ctipoout=2,
                     #dutyin=0.5, periodin=1.91, nperiodsin=8, L1=16000, increment=0, ctipoout=2,coupling_l=0.5,
                      #dutyout=0.5, periodout= 1.91, nperiodsout=8,
                      #coupling_wout=15.0, coupling_win=15,  
                     
                                          
                     #)

#N0 in F0 out
cell=CombinedCircuit(chip_length=20000,  radius=200, core=3.3,layName_h='metal',
                     layName_c='waveguide', layName_h2='metal2',layName_f='flowcell',
                     #dutyout=0.5, periodout= 1.87, nperiodsout=7,
                     #dutyin=0.5, periodin=1.87, nperiodsin=7, L1=6000, increment=0, ctipoout=2,
                     dutyin=0.5, periodin=1.91, nperiodsin=8, L1=16000, increment=0, ctipoout=1,coupling_l=0.5,
                      dutyout=0.4656, periodout= 2.6310, nperiodsout=38,
                      coupling_wout=15.0, coupling_win=15,  
                     
                                          
                     )
		     
	#F0 in F0 out
#cell=CombinedCircuit(chip_length=20000,  radius=200, core=3.5,layName_h='metal',
                #layName_c='waveguide', layName_h2='metal2',layName_f='flowcell',
                ##dutyout=0.5, periodout= 1.87, nperiodsout=7,
                ##dutyin=0.5, periodin=1.87, nperiodsin=7, L1=6000, increment=0, ctipoout=2,
                #dutyin=0.4656, periodin=2.6310, nperiodsin=38, L1=16000, increment=0, ctipoout=1,coupling_l=0.5,
                 #dutyout=0.4656, periodout= 2.6310, nperiodsout=38, ctipoin=1,
                 #coupling_wout=15.0, coupling_win=15,  
                
                                     
                #)		     


########################################### VISUALIZATION AND GDSII #########################################
#GratingCoupler1Band().Layout().visualize(annotate=True)  
lv = cell.Layout()
lv.write_gdsii("NF_trenches_3c3WG.gds")
#lv.write_gdsii("test.gds")
lv.visualize()
#lv.visualize(annotate=True)    








