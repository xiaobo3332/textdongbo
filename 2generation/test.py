from technologies import silicon_photonics
from picazzo3.wg.dircoup import SBendDirectionalCoupler
from picazzo3.traces.wire_wg.trace import WireWaveguideTemplate
from ipkiss3.all import SplineRoundingAlgorithm
import ipkiss3.all as i3

wg_t = WireWaveguideTemplate(name="my_wg_template4")
wg_t.Layout(core_width=0.500,
            cladding_width=i3.TECH.WG.CLADDING_WIDTH,
            core_process=i3.TECH.PROCESS.WG)

wg_t2 = WireWaveguideTemplate(name="my_wg_template5")
wg_t2.Layout(core_width=0.600,
            cladding_width=i3.TECH.WG.CLADDING_WIDTH,
            core_process=i3.TECH.PROCESS.WG)

ra = SplineRoundingAlgorithm(adiabatic_angles=(30.0, 0)) #asymmetric

C = SBendDirectionalCoupler(name="my_sbenddircoup_4",
                            trace_template1=wg_t,
                            trace_template2=wg_t2,
                            coupler_length=6.0)

layout = C.Layout(coupler_spacing=10,
                bend_radius=5.0,
                manhattan=True,
                straight_after_bend=6.0,
                sbend_straight=1.0,
                # wg1b_shape=i3.Shape([(0,0),(3,0)], closed=False),
                # bend_angles1=(10,20),
                # bend_angles2=30.0,
                # rounding_algorithm=ra,
                  )
layout.visualize()