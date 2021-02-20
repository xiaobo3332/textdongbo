# Example: Definition of a PCell with Properties

from ipkiss import all as ia
from ipkiss3 import all as i3

# We will define a Ring Resonator PCell which consists of
# a ring waveguide with evanescent coupling to a bus waveguide

class RingResonator(i3.PCell):

    """A generic ring resonator class.

    It is defined by a circular waveguide evanescently coupled to a straight bus waveguide.
    """
    _name_prefix = "RINGRES"  # a prefix added to the unique identifier

    ring_radius = i3.PositiveNumberProperty(doc="radius of the ring in micrometers")
    ring_wg_width = i3.PositiveNumberProperty(default=0.5, doc="width of the ring waveguide in micrometers")
    bus_wg_width = i3.PositiveNumberProperty(default=0.5, doc="width of the bus waveguide in micrometers")
    coupler_spacing = i3.PositiveNumberProperty(doc="spacing between centerline of bus waveguide and ring waveguide")
    
    def _default_coupler_spacing(self):
        return self.ring_wg_width + self.bus_wg_width + 1.0

    def validate_properties(self):
        """Check whether the combination of properties is valid."""
        if self.coupler_spacing <= 0.5 * (self.ring_wg_width + self.bus_wg_width):
            raise i3.PropertyValidationError(self, "coupler_spacing too small: waveguides will touch",
                                             {"coupler_spacing": self.coupler_spacing,
                                              "ring_wg_width": self.ring_wg_width,
                                              "bus.wg_width": self.bus_wg_width
                                              })

        if self.ring_radius < self.ring_wg_width:
            raise i3.PropertyValidationError(self, "ring_radius too small for given waveguide definition",
                                             {"ring_radius": self.ring_radius,
                                              "ring_wg_width": self.ring_wg_width
                                              })
        return True


if __name__ == "__main__":
    # The code here is only executed if this python file is run directly.
    # As this is only contains a library component, we should call it from
    # another file. In this case, it is 'execute.py'

    print "This is not the main file. Run 'execute.py' in the same folder\n"
