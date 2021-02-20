from technologies import silicon_photonics
from picazzo3.routing.place_route import PlaceAndAutoRoute

import ipkiss3.all as i3

from MMI22_V1 import v8
from MMI2112_V6 import v6

mmi1 = v8(name="P1")
mmi1_layout = mmi1.Layout(length=390)
mmi2 = v8(name="P2")
mmi2_layout = mmi2.Layout(length=398)
mmi3 = v8(name="P3")
mmi3_layout = mmi3.Layout(length=406)


mmmi1 = v6(name="PP1")
mmmi1_layout = mmmi1.Layout(length2=92)
mmmi2 = v6(name="PP2")
mmmi2_layout = mmmi2.Layout(length2=97)
mmmi3 = v6(name="PP3")
mmmi3_layout = mmmi3.Layout(length2=102)


pr = PlaceAndAutoRoute(
    child_cells={
        "1": mmi1,
        "2": mmi2,
        "3": mmi3,
        "cell_1": mmmi1,
        "cell_2": mmmi2,
        "cell_3": mmmi3
    }
)

pr_layout = pr.Layout(child_transformations={"1": (0, 0),
                                             "2": i3.HMirror(0.0) + i3.Translation((6000, 0)),
                                             "3": (6000, 0),
                                             "cell_1": i3.HMirror(0.0) + i3.Translation((3300, 0)) + i3.Translation((9000, 0.0)),
                                             "cell_2": i3.Translation((3300, 0)) + i3.Translation((9000, 0.0)),
                                             "cell_3": i3.HMirror(0.0) + i3.Translation((9900, 0)) + i3.Translation((9000, 0.0))
                                             })
# pr_layout.visualize()
pr_layout.write_gdsii("merge.gds")
#
# #layout.visualize(annotate=True)
#
# # # my_ring_layout.write_gdsii("my_ring.gds")
