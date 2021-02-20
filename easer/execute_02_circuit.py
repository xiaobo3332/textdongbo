# 1.  Importing the technology file. 
from technologies import silicon_photonics
from ipkiss3 import all as i3

# 2. Import other python libraries.
import numpy as np
import pylab as plt

# 3. Creating the ring resonator 
from picazzo3.filters.ring import RingRect180DropFilter
my_ring = RingRect180DropFilter()
my_ring_layout = my_ring.Layout(bend_radius=10.0)

cp = dict(cross_coupling1=1j*0.3**0.5,
          straight_coupling1=0.7**0.5) #The coupling from bus to ring and back


my_ring_cm = my_ring.CircuitModel(ring_length=2 * np.pi * my_ring_layout.bend_radius, # we can manually specify the ring length, or take it from the layout
                                  coupler_parameters=[cp, cp]) # 2 couplers

# 4. Creating the grating coupler. 
from picazzo3.fibcoup.curved import FiberCouplerCurvedGrating
my_grating = FiberCouplerCurvedGrating()
my_grating_layout = my_grating.Layout(n_o_lines=24, period_x=0.65, box_width=15.5)
my_grating_cm = my_grating.CircuitModel(center_wavelength=1.55,
                                       bandwidth_3dB=0.06, 
                                       peak_transmission=0.60**0.5,
                                       reflection=0.05**0.5)

# 5. Create the place and auto-route. 
from picazzo3.routing.place_route import PlaceAndAutoRoute
my_circuit = PlaceAndAutoRoute(child_cells={"in_grating": my_grating,
                                            "pass_grating": my_grating,
                                            "add_grating" : my_grating, 
                                            "drop_grating" : my_grating,
                                            "ring" : my_ring},
                       
                                   links=[("in_grating:out", "ring:in1"),
                                          ("pass_grating:out", "ring:out1"),
                                          ("add_grating:out", "ring:in2"),
                                          ("drop_grating:out", "ring:out2")]
                                   )

distance_x = 100.0
distance_y = 30.0
my_circuit_layout = my_circuit.Layout(child_transformations={"ring": (0, 0),
                                                             "in_grating": i3.Rotation(rotation=0) + i3.Translation((-distance_x, -distance_y)),
                                                             "pass_grating": i3.Rotation(rotation=180) + i3.Translation((distance_x, -distance_y)),
                                                             "add_grating": i3.Rotation(rotation=180) + i3.Translation((distance_x, distance_y)),
                                                             "drop_grating": i3.Rotation(rotation=0) + i3.Translation((-distance_x, distance_y)),
                                                              })
my_circuit_layout.visualize()


# 6. Simulate
my_circuit_cm = my_circuit.CircuitModel()
wavelengths = np.linspace(1.50, 1.6, 2001)
S = my_circuit_cm.get_smatrix(wavelengths=wavelengths)

# 7. Plot
plt.plot(wavelengths, np.abs(S['in_grating_vertical_in', 'pass_grating_vertical_in'])**2, 'b', label="pass")
plt.plot(wavelengths, np.abs(S['in_grating_vertical_in', 'drop_grating_vertical_in'])**2, 'r', label="drop")
plt.plot(wavelengths, np.abs(S['in_grating_vertical_in', 'add_grating_vertical_in'])**2, 'g', label="add")
plt.plot(wavelengths, np.abs(S['in_grating_vertical_in', 'in_grating_vertical_in'])**2, 'k', label="reflection")
plt.legend()
plt.show() 
