from technologies import silicon_photonics
from ipkiss3 import all as i3
from picazzo3.routing.place_route import PlaceAndAutoRoute
from picazzo3.routing.place_route import PlaceComponents
from picazzo3.wg.spirals import FixedLengthSpiralRounded
from picazzo3.traces.wire_wg import WireWaveguideTemplate
import joblib
import os
from spiral_wg_FBMS import SpiralWgLossEbeamFBMSMerged
from straight_wg import StraightWgLossEbeamFBMSMerged


wg_width = 0.5
lengths = [5000, 10000, 20000, 40000]
true_lengths = []
child_cells = dict()
child_cells["straight_ref_top"] = StraightWgLossEbeamFBMSMerged(name="Straight_ref_top", wg_width=wg_width)
child_cells["straight_ref_bottom"] = StraightWgLossEbeamFBMSMerged(name="Straight_ref_bottom", wg_width=wg_width)
for num,length in enumerate(lengths):
    a = SpiralWgLossEbeamFBMSMerged(name="Spiral_length_"+str(length), spiral_length=length, wg_width=wg_width)
    a_lo = a.Layout()
    child_cells["length"+str(length)] = a
    # true_lengths.append(a_lo.get_true_length())
    # print length, true_lengths[num]

child_transformations = dict()
child_transformations["length40000"] = (0,0)
# middle_x_plane = (a_lo.ports["in"].position.x+a_lo.ports["out"].position.x)/2.0
si = a_lo.size_info()
# middle_x_plane = (a_lo.west.position.x+a_lo.east.position.x)/2.0
middle_x_plane = (si.west+si.east)*0.5
child_transformations["length5000"] = i3.CMirror(mirror_center=(middle_x_plane,0)) + i3.Translation((0,600))
child_transformations["length10000"] = (0,700)
child_transformations["length20000"] = i3.CMirror(mirror_center=(middle_x_plane,0)) + i3.Translation((0,600+700))
child_transformations["straight_ref_top"] = (0,600+700+100)
child_transformations["straight_ref_bottom"] = (0,-100)

SpiralWg = PlaceAndAutoRoute(name="SpiralWgEbeam"+str(wg_width),child_cells=child_cells)
lo = SpiralWg.Layout(child_transformations=child_transformations)
gds_name = os.path.join(os.curdir, "spiral_wg_sweep_width"+str(wg_width)+".gds")
lo.write_gdsii(gds_name)