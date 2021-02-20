"""Example of creating a directional coupler using demolib technology.
"""

# First we load a PDK (demo PDK in this case)
import demolib.all as demo
import ipkiss3.all as i3

# Create a waveguide template (contains cross-sectional information)
wg_t = demo.SiWireWaveguideTemplate()
wg_t_lo = wg_t.Layout(core_width=0.5)


class DirectionalCoupler(i3.PCell):
    class Layout(i3.LayoutView):
        def _generate_instances(self, insts):
            # Define some parameters
            gap = 0.2
            core_width = wg_t_lo.core_width

            # Define a rounded waveguide
            wg = i3.RoundedWaveguide(name=self.name + '_wg1', trace_template=wg_t)
            wg.Layout(shape=[(-15, 3), (-10, 3), (-5, 0), (5, 0), (10, 3), (15, 3)])

            # Define instances
            insts += i3.SRef(name='wg_top', reference=wg, position=(0, 0.5 * (core_width + gap)))
            insts += i3.SRef(name='wg_bottom', reference=wg, position=(0, -0.5 * (core_width + gap)), transformation=i3.VMirror())

            return insts

        def _generate_ports(self, ports):
            return i3.expose_ports(self.instances,
                                   {'wg_bottom:in': 'in1',
                                    'wg_top:in': 'in2',
                                    'wg_bottom:out': 'out1',
                                    'wg_top:out': 'out2'})

dc = DirectionalCoupler()
dc_lay = dc.Layout()
dc_lay.write_gdsii('dircoup.gds')

# Visualize without displaying ports
dc_lay.visualize()

# Visualize, display ports
dc_lay.visualize(annotate=True)
