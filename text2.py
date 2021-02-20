# 1.  Importing the technology file.

from technologies import silicon_photonics
from ipkiss3 import all as i3

# 2. Import other python libraries.
import numpy as np
import pylab as plt

# 3. Ring Resonator import the ring resonator
from picazzo3.filters.ring.cell import RingRect180DropFilter
my_ring = RingRect180DropFilter()
print my_ring

# # 4. Layout
# my_ring_layout = my_ring.Layout(bend_radius=10.0)
# my_ring_layout.visualize(annotate= "true")
#
#
# my_ring_layout.write_gdsii("my_ring.gds")
#
# # 5. CircuitModel: Parameters of the couplers.
# cp = dict(cross_coupling1=1j*0.3**0.5,
#           straight_coupling1=0.7**0.5) #The coupling from bus to ring and back
#
#
# my_ring_cm = my_ring.CircuitModel(coupler_parameters=[cp, cp])
#
# wavelengths = np.linspace(1.50, 1.6, 2001)
# S = my_ring_cm.get_smatrix(wavelengths=wavelengths)
#
# plt.plot(wavelengths, np.abs(S['in1', 'out1'])**2, 'b', label="pass")
# plt.plot(wavelengths, np.abs(S['in1', 'out2'])**2, 'r', label="drop")
# plt.plot(wavelengths, np.abs(S['in1', 'in2'])**2, 'g', label="add")
#
# plt.xlabel("Wavelength ($\mu m$)")
# plt.ylabel("Power transmission")
# plt.legend()
# plt.show()

# # 6. Curved grating
# from picazzo3.fibcoup.curved import FiberCouplerCurvedGrating
# my_grating = FiberCouplerCurvedGrating()
#
# # 7. Layout
# my_grating_layout = my_grating.Layout(n_o_lines=24, period_x=0.65, box_width=15.5)
# my_grating_layout.visualize()
#
# # 8. Setting the CircuitModel view from the grating coupler.
# my_grating_cm = my_grating.CircuitModel(center_wavelength=1.55, bandwidth_3dB=0.03, peak_transmission=0.60**0.5, reflection=0.05**0.5)
# S = my_grating_cm.get_smatrix(wavelengths=wavelengths)
# plt.plot(wavelengths, np.abs(S['vertical_in', 'out'])**2, 'b', label="pass")
# plt.legend()
# plt.show()

cp = dict(cross_coupling1=1j*0.3**0.5,
          straight_coupling1=0.7**0.5)
print cp

a=1j
print (a**2)