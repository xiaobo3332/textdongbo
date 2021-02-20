# This program creates a MZI from 

from technologies import silicon_photonics
from picazzo3.filters.mmi.cell import MMI1x2Tapered 
from picazzo3.filters.mmi.cell import MMI2x1Tapered
from picazzo3.filters.mzi import MZIWaveguides
from picazzo3.traces.wire_wg.trace import WireWaveguideTemplate



import ipkiss3.all as i3

# ############ Define Templates################################################################
# Define waveguide-like templates. They will be used to build in the MMI and the MZI arms.
#
#          wg_t1 --> Waveguide template to define the core and cladding widths for the MZI arms 
#          (and eventually the connexions between the componets)
#          mmi_trace_template --> Waveguide template for the MMI 'trace', i.e. the multi-mode part of the MMI
#          mmi_access_template --> Waveguide template for the MMI 'access', i.e., the ports of the MMI
#
# layout: core_width --> width of the core 
#         cladding_width --> width of the cladding 
# ##############################################################################################

wg_t1 = WireWaveguideTemplate()
wg_t1.Layout(core_width=5.0,
            cladding_width=9.0,
            core_process=i3.TECH.PROCESS.WG)

mmi_trace_template = WireWaveguideTemplate()
mmi_trace_template.Layout(core_width=50.0, cladding_width=54.0)

mmi_access_template = WireWaveguideTemplate()
mmi_access_template.Layout(core_width=8.0, cladding_width=12.0)

# ########### Define components #############################################################

# ###########################################################################################
# Define 1x2 and 2x1 MMI's: mmi_trace_template --> Defines the wide, MM part.
#                 input_trace_template --> Defines the MMI input channels.
#                 output_trace_template --> Defines the MMI output channels.
#                 trace_template --> Defines the final dimmensions of the input and output waveguides.
# Layout:         transition_length --> length of the inputs and ouput channels
#                 length --> Length of the MM part of the MMI.
#                 trace_spacing --> Spacing between the input (or output) channels.
# ###########################################################################################

mmi1_12 = MMI1x2Tapered(mmi_trace_template=mmi_trace_template,
                    input_trace_template=mmi_access_template,
                    output_trace_template=mmi_access_template,
                    trace_template=wg_t1,
                    )
layout_mmi1_12 = mmi1_12.Layout(transition_length=20.0, length=100.0, trace_spacing=20.0)
layout_mmi1_12.visualize(annotate="true")

mmi1_21 = MMI2x1Tapered(mmi_trace_template=mmi_trace_template,
                        input_trace_template=mmi_access_template,
                        output_trace_template=mmi_access_template,
                        trace_template=wg_t1,
                       )

layout_mmi1_21 = mmi1_21.Layout(transition_length=20.0, length=100.0, trace_spacing=20.0) 

# ###########################################################################################
# Define MZIWaveguides: mzi (defines a MZI)
#                 splitter --> Defines the MZI splitting element, in this case will be a 1x2 MMI.
#                 combiner --> Defines the MZI combiner element, in this case will be a 2x1 MMI 
#                 trace_template --> The dimmensions of the MZI arms.
#                 splitter_port_names --> Identifies the ports of the splitter element that will be connected to 
#                                      the input ports of the MZI arms.
#                 combiner_port_names -->  Identifies the ports of the scombiner element that will be connected to 
#                                      the output ports of the MZI arms.

# Layout:         delay_length --> Definces a delay between the two arms of the MZI (a positive value makes 
#                                  longer the tbottom arm, a negative the top arm)
# ###########################################################################################

mzi = MZIWaveguides(name="my_mzi_waveguides_1",
                    trace_template=wg_t1,
                    splitter=mmi1_12,
                    combiner=mmi1_21,
                    splitter_port_names=['out1','out2'],
                    combiner_port_names=['in1','in2'])

layout = mzi.Layout(delay_length=-100.0) 

# ########### Visualize the layout

layout.visualize(annotate="true")
layout.write_gdsii("2_MMI_autoruted_MZI _arms.gds")