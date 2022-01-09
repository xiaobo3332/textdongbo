# from technologies import silicon_photonics
import ipkiss3. all as i3
# from picazzo3.routing.place_route import PlaceComponents

class Release(i3.PCell):
    _name_prefix = "RELEASE"

    # Layer
    lay_release = i3.Layer(number=4, name="release")
    layer = i3.LayerProperty(default=lay_release)

    # Mesa parameters
    length = i3.PositiveNumberProperty(default=1500.0)
    width = i3.PositiveNumberProperty(default=85.0)

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
        length = i3.PositiveNumberProperty(default=2750.0)
        width = i3.PositiveNumberProperty(default=85.0)
        shrink = i3.NumberProperty(default=0.0)
        nb = i3.PositiveIntProperty(default=8)
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
                # elems += i3.SRef(reference=release, position=self.position)
                elems += i3.ARef(n_o_periods=(3, self.nb), period=(self.length + 250, 210), reference=release, origin=(x0, y0))
                elems += i3.ARef(n_o_periods=(3, self.nb), period=(self.length + 250, 280), reference=release, origin=(x0, y0+210*self.nb-(210-self.width)+self.space))
                elems += i3.ARef(n_o_periods=(3, self.nb), period=(self.length + 250, 350), reference=release, origin=(x0, y0+210*self.nb-(210-self.width)+self.space+280*self.nb-(280-self.width)+self.space))
                elems += i3.ARef(n_o_periods=(3, self.nb), period=(self.length + 250, 420), reference=release, origin=(x0, y0+210*self.nb-(210-self.width)+self.space+280*self.nb-(280-self.width)+self.space+350*self.nb-(350-self.width)+self.space))

                elems += i3.ARef(n_o_periods=(2, self.nb), period=(self.length + 500, 210), reference=release,
                                 origin=(x0+9250-self.shrink*3, y0))
                elems += i3.ARef(n_o_periods=(2, self.nb), period=(self.length + 500, 280), reference=release,
                                 origin=(x0+9250-self.shrink*3, y0+210*self.nb-(210-self.width)+self.space))
                elems += i3.ARef(n_o_periods=(2, self.nb), period=(self.length + 500, 350), reference=release,
                                 origin=(x0+9250-self.shrink*3, y0+210*self.nb-(210-self.width)+self.space+280*self.nb-(280-self.width)+self.space))
                elems += i3.ARef(n_o_periods=(2, self.nb), period=(self.length + 500, 420), reference=release,
                                 origin=(x0+9250-self.shrink*3, y0+210*self.nb-(210-self.width)+self.space+280*self.nb-(280-self.width)+self.space+350*self.nb-(350-self.width)+self.space))

                elems += i3.ARef(n_o_periods=(2, self.nb), period=(self.length + 750, 210), reference=release,
                                 origin=(x0 + 8000*2-self.shrink*5, y0))
                elems += i3.ARef(n_o_periods=(2, self.nb), period=(self.length + 750, 280), reference=release,
                                 origin=(x0 + 8000*2-self.shrink*5, y0+210*self.nb-(210-self.width)+self.space))
                elems += i3.ARef(n_o_periods=(2, self.nb), period=(self.length + 750, 350), reference=release,
                                 origin=(x0 + 8000*2-self.shrink*5, y0+210*self.nb-(210-self.width)+self.space+280*self.nb-(280-self.width)+self.space))
                elems += i3.ARef(n_o_periods=(2, self.nb), period=(self.length + 750, 420), reference=release,
                                 origin=(x0 + 8000*2-self.shrink*5, y0+210*self.nb-(210-self.width)+self.space+280*self.nb-(280-self.width)+self.space+350*self.nb-(350-self.width)+self.space))

                elems += i3.ARef(n_o_periods=(2, self.nb), period=(self.length + 1000, 210), reference=release,
                                 origin=(x0 + 23250-self.shrink*7, y0))
                elems += i3.ARef(n_o_periods=(2, self.nb), period=(self.length + 1000, 280), reference=release,
                                 origin=(x0 + 23250-self.shrink*7, y0+210*self.nb-(210-self.width)+self.space))
                elems += i3.ARef(n_o_periods=(2, self.nb), period=(self.length + 1000, 350), reference=release,
                                 origin=(x0 + 23250-self.shrink*7, y0+210*self.nb-(210-self.width)+self.space+280*self.nb-(280-self.width)+self.space))
                elems += i3.ARef(n_o_periods=(2, self.nb), period=(self.length + 1000, 420), reference=release,
                                 origin=(x0 + 23250-self.shrink*7, y0+210*self.nb-(210-self.width)+self.space+280*self.nb-(280-self.width)+self.space+350*self.nb-(350-self.width)+self.space))

                elems += i3.ARef(n_o_periods=(2, self.nb), period=(self.length + 1500, 210), reference=release,
                                 origin=(x0 + 29750+1500-self.shrink*9, y0))
                elems += i3.ARef(n_o_periods=(2, self.nb), period=(self.length + 1500, 280), reference=release,
                                 origin=(x0 + 29750+1500-self.shrink*9, y0+210*self.nb-(210-self.width)+self.space))
                elems += i3.ARef(n_o_periods=(2, self.nb), period=(self.length + 1500, 350), reference=release,
                                 origin=(x0 + 29750+1500-self.shrink*9, y0+210*self.nb-(210-self.width)+self.space+280*self.nb-(280-self.width)+self.space))
                elems += i3.ARef(n_o_periods=(2, self.nb), period=(self.length + 1500, 420), reference=release,
                                 origin=(x0 + 29750+1500-self.shrink*9, y0+210*self.nb-(210-self.width)+self.space+280*self.nb-(280-self.width)+self.space+350*self.nb-(350-self.width)+self.space))

                elems += i3.ARef(n_o_periods=(2, self.nb), period=(self.length + 2000, 210), reference=release,
                                 origin=(x0 + 38250+2000-self.shrink*11, y0))
                elems += i3.ARef(n_o_periods=(2, self.nb), period=(self.length + 2000, 280), reference=release,
                                 origin=(x0 + 38250+2000-self.shrink*11, y0+210*self.nb-(210-self.width)+self.space))
                elems += i3.ARef(n_o_periods=(2, self.nb), period=(self.length + 2000, 350), reference=release,
                                 origin=(x0 + 38250+2000-self.shrink*11, y0+210*self.nb-(210-self.width)+self.space+280*self.nb-(280-self.width)+self.space))
                elems += i3.ARef(n_o_periods=(2, self.nb), period=(self.length + 2000, 420), reference=release,
                                 origin=(x0 + 38250+2000-self.shrink*11, y0+210*self.nb-(210-self.width)+self.space+280*self.nb-(280-self.width)+self.space+350*self.nb-(350-self.width)+self.space))

                elems += i3.ARef(n_o_periods=(2, self.nb), period=(self.length + 3000, 210), reference=release,
                                 origin=(x0 + 47750+3000-self.shrink*13, y0))
                elems += i3.ARef(n_o_periods=(2, self.nb), period=(self.length + 3000, 280), reference=release,
                                 origin=(x0 + 47750+3000-self.shrink*13, y0+210*self.nb-(210-self.width)+self.space))
                elems += i3.ARef(n_o_periods=(2, self.nb), period=(self.length + 3000, 350), reference=release,
                                 origin=(x0 + 47750+3000-self.shrink*13, y0+210*self.nb-(210-self.width)+self.space+280*self.nb-(280-self.width)+self.space))
                elems += i3.ARef(n_o_periods=(2, self.nb), period=(self.length + 3000, 420), reference=release,
                                 origin=(x0 + 47750+3000-self.shrink*13, y0+210*self.nb-(210-self.width)+self.space+280*self.nb-(280-self.width)+self.space+350*self.nb-(350-self.width)+self.space))

                # elems += i3.Circle(layer=i3.Layer(number = 5, name = "tether"),radius=50000)
                return elems


class Coupon2(i3.PCell):
    _name_prefix = "Coupon2"

    # Center of the structure
    position = i3.Coord2Property(default=(0.0, 0.0))

    # Coupon parameters
    length = i3.PositiveNumberProperty(default=2750.0)
    width = i3.PositiveNumberProperty(default=85.0)

    class Layout(i3.LayoutView):

        def _generate_elements(self, elems):
            # Center of the structure
            (x0, y0) = self.position
            # RELEASE

            c1 = Coupon(length=2750, nb=16) #2750 label A no need for shrink
            elems += i3.SRef(reference=c1, position=self.position, transformation=i3.Translation((0, 0))+i3.Translation((-16000,-25000)))
            elems += i3.PolygonText(layer=i3.Layer(number=4, name="release"),
                                    text="A16",
                                    font=2,
                                    height=1000.0,
                                    transformation=i3.Translation((45075, -12500)))
            c2 = Coupon(length=2250, shrink=500, nb=16)
            elems += i3.SRef(reference=c2, position=self.position,
                             transformation=i3.Translation((0, 23240)) + i3.Translation((-16000, -25000)))
            elems += i3.PolygonText(layer=i3.Layer(number=4, name="release"),
                                    text="B16",
                                    font=2,
                                    height=200.0,
                                    transformation=i3.Translation((35865, 20437.5)))

            c3 = Coupon(length=1500, shrink=1250, nb=16)
            elems += i3.SRef(reference=c3, position=self.position,
                             transformation=i3.Translation((0, 46480)) + i3.Translation((-16000, -25000)))
            elems += i3.PolygonText(layer=i3.Layer(number=4, name="release"),
                                    text="C16",
                                    font=2,
                                    height=1000.0,
                                    transformation=i3.Translation((-10000, 46677.5)))

            c4 = Coupon(length=2750, nb=8)
            elems += i3.SRef(reference=c4, position=self.position, transformation=i3.Translation((-28000, -38160)))
            elems += i3.PolygonText(layer=i3.Layer(number=4, name="release"),
                                    text="A8",
                                    font=2,
                                    height=1000.0,
                                    transformation=i3.Translation((32650, -30000)))
            c5 = Coupon(length=2250, shrink=500, nb=12)
            elems += i3.SRef(reference=c5, position=self.position, transformation=i3.Rotation(rotation=90)+i3.Translation((-18417.5, -23917.5)))
            elems += i3.PolygonText(layer=i3.Layer(number=4, name="release"),
                                    text="B12",
                                    font=2,
                                    height=1000.0,
                                    transformation=i3.Translation((-27695, 29707.5)))
            c6 = Coupon(length=1500, shrink=1250, nb=10)
            elems += i3.SRef(reference=c6, position=self.position, transformation=i3.Rotation(rotation=90)+i3.Translation((-36617.5, -23917.5)))
            elems += i3.PolygonText(layer=i3.Layer(number=4, name="release"),
                                    text="C10",
                                    font=2,
                                    height=1000.0,
                                    transformation=i3.Translation((-40000, 18832.5)))
            c7 = Coupon(length=1500, shrink=1250, nb=10)
            elems += i3.SRef(reference=c7, position=self.position, transformation=i3.Translation((-22000, -53840)))
            elems += i3.PolygonText(layer=i3.Layer(number=4, name="release"),
                                    text="C10",
                                    font=2,
                                    height=1000.0,
                                    transformation=i3.Translation((20950, -41500)))

            c8 = Coupon(length=2250, shrink=500, nb=14)
            elems += i3.SRef(reference=c8, position=self.position, transformation=i3.Translation((38750, -1760)))
            elems += i3.PolygonText(layer=i3.Layer(number=4, name="release"),
                                    text="B14",
                                    font=2,
                                    height=1000.0,
                                    transformation=i3.Translation((48000, -3802.5)))
            c9 = Coupon(length=1500, shrink=1250, nb=14)
            elems += i3.SRef(reference=c9, position=self.position, transformation=i3.Translation((27500, 21480)))
            elems += i3.PolygonText(layer=i3.Layer(number=4, name="release"),
                                    text="C14",
                                    font=2,
                                    height=200.0,
                                    transformation=i3.Translation((44000, 20437.5)))

            elems += i3.Circle(layer=i3.Layer(number=5, name="tether"), center=(0.0, 0.0), radius=50000)
            return elems

# GDS-file generation for debugging
#Coupon2(position=(-30000,-40000)).Layout.view.write_gdsii("Coupon.gds")
Coupon2().Layout.view.write_gdsii("Coupon.gds")
print("Done writing Coupon.gds!")





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