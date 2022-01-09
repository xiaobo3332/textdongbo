#from technologies import silicon_photonics
import ipkiss3. all as i3
from ipkiss3.pcell.gdscell import GDSCell


class mmi_slots_cell_test(GDSCell):

    def _default_filename(self):
        return 'MedPhab_CouponMask.gds'  # flatten the original gds file will cause crash issue!!

    def _default_cell_name(self):
        return 'PCELL_1990'

# mmi_slots_cell_test().Layout.view.write_gdsii("via_test.gds")

class Release(i3.PCell):
    _name_prefix = "RELEASE"

    # Layer
    lay_release = i3.Layer(number=1, name="release")
    layer = i3.LayerProperty(default=lay_release)

    # Mesa parameters
    length = i3.PositiveNumberProperty(default=40.0)
    width = i3.PositiveNumberProperty(default=8.0)

    class Layout(i3.LayoutView):

        def _generate_elements(self, elems):

            elems += i3.Rectangle(layer=self.layer, center=(0, 0),
                                  box_size=(self.length, self.width))
            return elems

# GDS-file generation for debugging
# Release().Layout.view.write_gdsii("Release.gds")
# print("Done writing Release.gds!")

class Coupon(i3.PCell):
        _name_prefix = "Coupon"

        # Center of the structure
        position = i3.Coord2Property(default=(0.0, 0.0))

        # Coupon parameters
        length = i3.PositiveNumberProperty(default=40.0)
        width = i3.PositiveNumberProperty(default=8.0)
        shrink = i3.NumberProperty(default=0.0)
        # nb = i3.PositiveIntProperty(default=8)
        space = i3.PositiveNumberProperty(default=1000.0)

        class Layout(i3.LayoutView):
            # _name_prefix = "length{}".format(str(self.length))
            def _generate_elements(self, elems):
                # Center of the structure
                (x0, y0) = self.position
                # RELEASE
                release = Release(length=self.length,
                                  width=self.width,
                                  )
                # release = i3.Rectangle(layer=i3.Layer(number=1, name="release"), center=(0, 0),
                #                         box_size=(self.length, self.width))
                # elems += i3.SRef(reference=release, position=self.position)  Error

                dx=918.125  # 800nm coupon
                for i in range (0,3,1):
                    elems += i3.ARef(n_o_periods=(3, 7), period=(159.5, 210), reference=release, origin=(640.5+i*dx, 468.4))
                    elems += i3.ARef(n_o_periods=(3, 7), period=(159.5, 210), reference=release, origin=(640.5+i*dx, 538.4))
                    elems += i3.ARefY(n_o_periods_1d=7, period_1d=210, reference=release, origin=(560.75+i*dx, 511.6))

                    dy=1725
                    elems += i3.ARef(n_o_periods=(3, 15), period=(159.5, 210), reference=release, origin=(640.5+i*dx, 468.4+dy))
                    elems += i3.ARef(n_o_periods=(3, 15), period=(159.5, 210), reference=release, origin=(640.5+i*dx, 538.4+dy))
                    elems += i3.ARefY(n_o_periods_1d=15, period_1d=210, reference=release, origin=(560.75+i*dx, 511.6+dy))

                    dy=5060
                    elems += i3.ARef(n_o_periods=(3, 15), period=(159.5, 210), reference=release,
                                     origin=(640.5+i*dx, 468.4 + dy))
                    elems += i3.ARef(n_o_periods=(3, 15), period=(159.5, 210), reference=release,
                                     origin=(640.5+i*dx, 538.4 + dy))
                    elems += i3.ARefY(n_o_periods_1d=15, period_1d=210, reference=release, origin=(560.75+i*dx, 511.6 + dy))

                    dy=8395
                    elems += i3.ARef(n_o_periods=(3, 8), period=(159.5, 210), reference=release, origin=(640.5+i*dx, 468.4+dy))
                    elems += i3.ARef(n_o_periods=(3, 7), period=(159.5, 210), reference=release, origin=(640.5+i*dx, 538.4+dy))
                    elems += i3.ARefY(n_o_periods_1d=7, period_1d=210, reference=release, origin=(560.75+i*dx, 511.6+dy))

                dx += 200   # 1000nm coupon
                for i in range (0,3,1):
                    elems += i3.ARef(n_o_periods=(4, 7), period=(167.6, 210), reference=release, origin=(3402.975+i*dx, 468.4))
                    elems += i3.ARef(n_o_periods=(4, 7), period=(167.6, 210), reference=release, origin=(3402.975+i*dx, 538.4))
                    elems += i3.ARefY(n_o_periods_1d=7, period_1d=210, reference=release, origin=(3319.175+i*dx, 511.6))

                    dy=1725
                    elems += i3.ARef(n_o_periods=(4, 15), period=(167.6, 210), reference=release, origin=(3402.975+i*dx, 468.4+dy))
                    elems += i3.ARef(n_o_periods=(4, 15), period=(167.6, 210), reference=release, origin=(3402.975+i*dx, 538.4+dy))
                    elems += i3.ARefY(n_o_periods_1d=15, period_1d=210, reference=release, origin=(3319.175+i*dx, 511.6+dy))

                    dy = 5060
                    elems += i3.ARef(n_o_periods=(4, 15), period=(167.6, 210), reference=release,
                                     origin=(3402.975 + i * dx, 468.4 + dy))
                    elems += i3.ARef(n_o_periods=(4, 15), period=(167.6, 210), reference=release,
                                     origin=(3402.975 + i * dx, 538.4 + dy))
                    elems += i3.ARefY(n_o_periods_1d=15, period_1d=210, reference=release,
                                      origin=(3319.175 + i * dx, 511.6 + dy))

                    dy = 8395
                    elems += i3.ARef(n_o_periods=(4, 8), period=(167.6, 210), reference=release,
                                     origin=(3402.975 + i * dx, 468.4 + dy))
                    elems += i3.ARef(n_o_periods=(4, 7), period=(167.6, 210), reference=release,
                                     origin=(3402.975 + i * dx, 538.4 + dy))
                    elems += i3.ARefY(n_o_periods_1d=7, period_1d=210, reference=release,
                                      origin=(3319.175 + i * dx, 511.6 + dy))

                dx += 200  # 1200nm coupon
                for i in range(0, 3, 1):
                    elems += i3.ARef(n_o_periods=(5, 7), period=(173, 210), reference=release,
                                     origin=(6762.75 + i * dx, 468.4))
                    elems += i3.ARef(n_o_periods=(5, 7), period=(173, 210), reference=release,
                                     origin=(6762.75 + i * dx, 538.4))
                    elems += i3.ARefY(n_o_periods_1d=7, period_1d=210, reference=release,
                                      origin=(6676.25 + i * dx, 511.6))

                    dy = 1725
                    elems += i3.ARef(n_o_periods=(5, 15), period=(173, 210), reference=release,
                                     origin=(6762.75 + i * dx, 468.4 + dy))
                    elems += i3.ARef(n_o_periods=(5, 15), period=(173, 210), reference=release,
                                     origin=(6762.75 + i * dx, 538.4 + dy))
                    elems += i3.ARefY(n_o_periods_1d=15, period_1d=210, reference=release,
                                      origin=(6676.25 + i * dx, 511.6 + dy))

                    dy = 5060
                    elems += i3.ARef(n_o_periods=(5, 15), period=(173, 210), reference=release,
                                     origin=(6762.75 + i * dx, 468.4 + dy))
                    elems += i3.ARef(n_o_periods=(5, 15), period=(173, 210), reference=release,
                                     origin=(6762.75 + i * dx, 538.4 + dy))
                    elems += i3.ARefY(n_o_periods_1d=15, period_1d=210, reference=release,
                                      origin=(6676.25 + i * dx, 511.6 + dy))

                    dy = 8395
                    elems += i3.ARef(n_o_periods=(5, 8), period=(173, 210), reference=release,
                                     origin=(6762.75 + i * dx, 468.4 + dy))
                    elems += i3.ARef(n_o_periods=(5, 7), period=(173, 210), reference=release,
                                     origin=(6762.75 + i * dx, 538.4 + dy))
                    elems += i3.ARefY(n_o_periods_1d=7, period_1d=210, reference=release,
                                      origin=(6676.25 + i * dx, 511.6 + dy))

                return elems


class PlaceMyComponents(i3.PCell):
    _name_prefix = "place"

    # Center of the structure
    position = i3.Coord2Property(default=(0.0, 0.0))

    # # Coupon parameters
    # length = i3.PositiveNumberProperty(default=2750.0)
    # width = i3.PositiveNumberProperty(default=85.0)

    class Layout(i3.LayoutView):

        def _generate_elements(self, elems):
            # # Center of the structure
            # (x0, y0) = self.position
            # # RELEASE

            c1 = Coupon(length=40) #2750 label A no need for shrink
            elems += i3.SRef(reference=c1, transformation=i3.Translation((0, 0)))

            Medphab = mmi_slots_cell_test()
            elems += i3.SRef(reference=Medphab)
            return elems

# GDS-file generation for debugging
# Coupon2().Layout.view.write_gdsii("Coupon.gds")
PlaceMyComponents().Layout.view.write_gdsii("via.gds")
print("Done writing Coupon.gds!")

# # mmi_slots = Coupon2()
# mmi_ribs = mmi_slots_cell_test()
#
# from picazzo3.routing.place_route import PlaceComponents
# #from picazzo3.routing.place_route import PlaceAndAutoRoute
# pr = PlaceComponents(child_cells = {#"mmi1":mmi_slots,
#                                       "mmi2":mmi_ribs,},
#                     )
#
# layout = pr.Layout(child_transformations={#"mmi1":(0.,-50.),
#                                           "mmi2":(0.,300.),
#                                           }
#                    )
#
# #layout.visualize()
# layout.write_gdsii("final.gds")


# c1 = Coupon(name="haha1", length=2750, nb=16)
# c2 = Coupon(name="haha2", length=2250, shrink=500, nb=16)
# c3 = Coupon(name="haha3", length=1500, shrink=1250, nb=16)
#
# pr = PlaceComponents(
#     child_cells={
#         "com1": c1,
#         "com2": c2,
#         "com3": c3,
#     }
# )
# pr_layout = pr.Layout(child_transformations={"com1": (0, 0),
#                                              "com2": (0, 23240),
#                                              "com3": (0, 46480),
#                                              })
# pr_layout.write_gdsii("cou.gds")    #AttributeError: 'Layer' object has no attribute 'process'