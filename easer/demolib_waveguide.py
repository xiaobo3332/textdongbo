# First we load a PDK (demolib in this case)
import demolib.all as demo
import ipkiss3.all as i3

wg_t = demo.SiWireWaveguideTemplate()
wg_t_lo = wg_t.Layout(core_width=0.5)

# Define a rounded waveguide
wg = i3.RoundedWaveguide(name='MyWaveguide', trace_template=wg_t)
wg_lo = wg.Layout(shape=[(-15, 3), (-10, 3), (-5, 0), (5, 0), (10, 3), (15, 3)])

wg_lo.visualize(annotate=True)
