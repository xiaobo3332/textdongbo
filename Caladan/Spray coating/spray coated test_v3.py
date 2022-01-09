from LayerDefinitions import *
from AlignmentMarkerSet import AlignmentMarkerSet
# from picazzo3.routing.place_route import PlaceComponents

class Release(i3.PCell):
    _name_prefix = "RELEASE"

    # Layer
    layer = i3.LayerProperty(default=lay_release)

    # Mesa parameters
    length = i3.PositiveNumberProperty(default=1500.0)
    width = i3.PositiveNumberProperty(default=85.0)

    class Layout(i3.LayoutView):

        def _generate_elements(self, elems):

            elems += i3.Rectangle(layer=self.layer, center=(0, 0),
                                  box_size=(self.length, self.width))
            return elems

# # GDS-file generation for debugging
# # Release().Layout.view.write_gdsii("Release.gds")
# # print("Done writing Release.gds!")

class Release_horizontal(i3.PCell):
    _name_prefix = "Horizontal"

    # Center of the structure
    position = i3.Coord2Property(default=(0.0, 0.0))

    # Layer
    layer = i3.LayerProperty(default=lay_release)

    # Mesa parameters
    length = i3.PositiveNumberProperty(default=1500.0)
    width = i3.PositiveNumberProperty(default=85.0)

    class Layout(i3.LayoutView):

        def _generate_elements(self, elems):

            # Center of the structure
            (x0, y0) = self.position

            elems += i3.Rectangle(layer=self.layer, center=(x0, y0),
                                  box_size=(self.length, self.width))
            x0+=self.length+3000
            elems += i3.Rectangle(layer=self.layer, center=(x0, y0),
                                  box_size=(self.length, self.width))
            x0 += self.length + 2000
            elems += i3.Rectangle(layer=self.layer, center=(x0, y0),
                                  box_size=(self.length, self.width))
            x0 += self.length + 1500
            elems += i3.Rectangle(layer=self.layer, center=(x0, y0),
                                  box_size=(self.length, self.width))
            x0 += self.length + 1000
            elems += i3.Rectangle(layer=self.layer, center=(x0, y0),
                                  box_size=(self.length, self.width))
            x0 += self.length + 750
            elems += i3.Rectangle(layer=self.layer, center=(x0, y0),
                                  box_size=(self.length, self.width))
            x0 += self.length + 500
            elems += i3.Rectangle(layer=self.layer, center=(x0, y0),
                                  box_size=(self.length, self.width))
            x0 += self.length + 250
            elems += i3.Rectangle(layer=self.layer, center=(x0, y0),
                                  box_size=(self.length, self.width))
            x0 += self.length + 130
            elems += i3.Rectangle(layer=self.layer, center=(x0, y0),
                                  box_size=(self.length, self.width))
            # x0 = 0
            # y0 += 420
            # elems += i3.Rectangle(layer=self.layer, center=(x0, y0),
            #                       box_size=(self.length, self.width))
            # y0 += 350
            # elems += i3.Rectangle(layer=self.layer, center=(x0, y0),
            #                       box_size=(self.length, self.width))
            # y0 += 280
            # elems += i3.Rectangle(layer=self.layer, center=(x0, y0),
            #                       box_size=(self.length, self.width))
            # y0 += 210
            # elems += i3.Rectangle(layer=self.layer, center=(x0, y0),
            #                       box_size=(self.length, self.width))
            # y0 += 140
            # elems += i3.Rectangle(layer=self.layer, center=(x0, y0),
            #                       box_size=(self.length, self.width))

            return elems

class Release_vertical(i3.PCell):
    _name_prefix = "Vertical"

    # Center of the structure
    position = i3.Coord2Property(default=(0.0, 0.0))

    # Layer
    layer = i3.LayerProperty(default=lay_release)

    # Mesa parameters
    length = i3.PositiveNumberProperty(default=1500.0)
    width = i3.PositiveNumberProperty(default=85.0)

    class Layout(i3.LayoutView):

        def _generate_elements(self, elems):

            # Center of the structure
            (x0, y0) = self.position

            elems += i3.Rectangle(layer=self.layer, center=(x0, y0),
                                  box_size=(self.length, self.width))
            # x0+=1500+3000
            # elems += i3.Rectangle(layer=self.layer, center=(x0, y0),
            #                       box_size=(self.length, self.width))
            # x0 += 1500 + 2000
            # elems += i3.Rectangle(layer=self.layer, center=(x0, y0),
            #                       box_size=(self.length, self.width))
            # x0 += 1500 + 1500
            # elems += i3.Rectangle(layer=self.layer, center=(x0, y0),
            #                       box_size=(self.length, self.width))
            # x0 += 1500 + 1000
            # elems += i3.Rectangle(layer=self.layer, center=(x0, y0),
            #                       box_size=(self.length, self.width))
            # x0 += 1500 + 750
            # elems += i3.Rectangle(layer=self.layer, center=(x0, y0),
            #                       box_size=(self.length, self.width))
            # x0 += 1500 + 500
            # elems += i3.Rectangle(layer=self.layer, center=(x0, y0),
            #                       box_size=(self.length, self.width))
            # x0 += 1500 + 250
            # elems += i3.Rectangle(layer=self.layer, center=(x0, y0),
            #                       box_size=(self.length, self.width))
            # x0 += 1500 + 130
            # elems += i3.Rectangle(layer=self.layer, center=(x0, y0),
            #                       box_size=(self.length, self.width))
            # x0 = 0
            y0 += 490
            elems += i3.Rectangle(layer=self.layer, center=(x0, y0),
                                  box_size=(self.length, self.width))

            y0 += 420
            elems += i3.Rectangle(layer=self.layer, center=(x0, y0),
                                  box_size=(self.length, self.width))
            y0 += 350
            elems += i3.Rectangle(layer=self.layer, center=(x0, y0),
                                  box_size=(self.length, self.width))
            y0 += 280
            elems += i3.Rectangle(layer=self.layer, center=(x0, y0),
                                  box_size=(self.length, self.width))
            y0 += 210
            elems += i3.Rectangle(layer=self.layer, center=(x0, y0),
                                  box_size=(self.length, self.width))
            y0 += 140
            elems += i3.Rectangle(layer=self.layer, center=(x0, y0),
                                  box_size=(self.length, self.width))

            return elems

# GDS-file generation for debugging
# Release_single().Layout.view.write_gdsii("Release.gds")
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
                # release = i3.Rectangle(layer=lay_release, center=(0, 0), # directly using a rectrangle didn't work!!
                #                       box_size=(self.length, self.width))

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

                # elems += i3.Circle(layer=lay_p_contact,radius=50000)
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
            # # Center of the structure
            # (x0, y0) = self.position
            # RELEASE

            c1 = Coupon(length=2750, nb=16) #2750 label A no need for shrink
            elems += i3.SRef(reference=c1, position=self.position, transformation=i3.Translation((0, 0))+i3.Translation((-27000,-30000)))
            elems += i3.PolygonText(layer=lay_release,
                                    text="A16",
                                    font=2,
                                    height=1000.0,
                                    transformation=i3.Translation((34075, -7802.5)))
            c2 = Coupon(length=2250, shrink=500, nb=16)
            elems += i3.SRef(reference=c2, position=self.position,
                             transformation=i3.Translation((0, 23240)) + i3.Translation((-38000, -30000)))
            elems += i3.PolygonText(layer=lay_release,
                                    text="B16",
                                    font=2,
                                    height=1000.0,
                                    transformation=i3.Translation((-42325, 15437.5)))

            c3 = Coupon(length=1500, shrink=1250, nb=16)
            elems += i3.SRef(reference=c3, position=self.position,
                             transformation=i3.Translation((0, 46480)) + i3.Translation((-20000, -30000)))
            elems += i3.PolygonText(layer=lay_release,
                                    text="C16",
                                    font=2,
                                    height=1000.0,
                                    transformation=i3.Translation((22950, 38677.5)))

            c4 = Coupon(length=2750, nb=8)
            elems += i3.SRef(reference=c4, position=self.position, transformation=i3.Translation((-27000, -43160)))
            elems += i3.PolygonText(layer=lay_release,
                                    text="A8",
                                    font=2,
                                    height=1000.0,
                                    transformation=i3.Translation((33650, -31042.5)))
            # c5 = Coupon(length=2250, shrink=500, nb=12)
            # elems += i3.SRef(reference=c5, position=self.position, transformation=i3.Rotation(rotation=90)+i3.Translation((-18417.5, -23917.5)))
            # elems += i3.PolygonText(layer=i3.Layer(number=4, name="release"),
            #                         text="B12",
            #                         font=2,
            #                         height=1000.0,
            #                         transformation=i3.Translation((-27695, 29707.5)))
            # c6 = Coupon(length=1500, shrink=1250, nb=10)
            # elems += i3.SRef(reference=c6, position=self.position, transformation=i3.Rotation(rotation=90)+i3.Translation((-36617.5, -23917.5)))
            # elems += i3.PolygonText(layer=i3.Layer(number=4, name="release"),
            #                         text="C10",
            #                         font=2,
            #                         height=1000.0,
            #                         transformation=i3.Translation((-40000, 18832.5)))
            # c7 = Coupon(length=1500, shrink=1250, nb=10)
            # elems += i3.SRef(reference=c7, position=self.position, transformation=i3.Translation((-22000, -53840)))
            # elems += i3.PolygonText(layer=i3.Layer(number=4, name="release"),
            #                         text="C10",
            #                         font=2,
            #                         height=1000.0,
            #                         transformation=i3.Translation((20950, -41500)))
            #
            c8 = Coupon(length=2250, shrink=500, nb=12)
            elems += i3.SRef(reference=c8, position=self.position, transformation=i3.Translation((16750, -6760)))
            elems += i3.PolygonText(layer=lay_release,
                                    text="B12",
                                    font=2,
                                    height=1000.0,
                                    transformation=i3.Translation((46000, 12397.5)))
            # c9 = Coupon(length=1500, shrink=1250, nb=14)
            # elems += i3.SRef(reference=c9, position=self.position, transformation=i3.Translation((27500, 21480)))
            # elems += i3.PolygonText(layer=i3.Layer(number=4, name="release"),
            #                         text="C14",
            #                         font=2,
            #                         height=200.0,
            #                         transformation=i3.Translation((44000, 20437.5)))

            elems += i3.Circle(layer=lay_p_contact, center=(0.0, 0.0), radius=50000)
            elems += i3.RingSegment(layer=lay_tether, center=(0,0), angle_start=0.0, angle_end=360.0, inner_radius=45000,outer_radius=50000)

            ## ADD ALIGNMENT MARKER SET
            elems += i3.SRef(reference=AlignmentMarkerSet(horizontal=False),
                             transformation=i3.Translation((-34000.0, -24000.0)))
            elems += i3.SRef(reference=AlignmentMarkerSet(horizontal=False),
                             transformation=i3.Translation((-34000.0, 24000.0)))
            elems += i3.SRef(reference=AlignmentMarkerSet(horizontal=False),
                             transformation=i3.Translation((34000, -24000.0)))
            elems += i3.SRef(reference=AlignmentMarkerSet(horizontal=False),
                             transformation=i3.Translation((34000.0, 24000.0)))
            elems += i3.SRef(reference=AlignmentMarkerSet(horizontal=False),
                             transformation=i3.Translation((0.0, 44000.0)))

            # ADD release_single left down
            elems += i3.SRef(reference=Release_horizontal(),
                             transformation=i3.Translation((-50505.0, -7845.0)))
            elems += i3.SRef(reference=Release_horizontal(),
                             transformation=i3.Translation((-50505.0, -14145.0)))
            elems += i3.SRef(reference=Release_vertical(),
                             transformation=i3.Translation((-34755, -18000.0-120)))
            elems += i3.SRef(reference=Release_vertical(length=2250),
                             transformation=i3.Translation((-34755, -22000.0+405)))
            elems += i3.SRef(reference=Release_vertical(),
                             transformation=i3.Translation((-32755, -29000.0)))
            # ADD release_single left up
            elems += i3.SRef(reference=Release_horizontal(),
                             transformation=i3.Translation((-42880.0, 16480.0)))
            elems += i3.SRef(reference=Release_horizontal(),
                             transformation=i3.Translation((-42880.0, 16480.0+3150)))
            elems += i3.SRef(reference=Release_horizontal(),
                             transformation=i3.Translation((-42880.0, 16480.0+9520)))
            elems += i3.SRef(reference=Release_vertical(),
                             transformation=i3.Translation((-26755-375, 31000.0)))
            # ADD release_single top
            elems += i3.SRef(reference=Release_horizontal(),
                             transformation=i3.Translation((-15000, 40720.0)))
            elems += i3.SRef(reference=Release_horizontal(length=2250),
                             transformation=i3.Translation((-18000+1495+130-2000, 42720.0-110)))
            elems += i3.SRef(reference=Release_vertical(),
                             transformation=i3.Translation((12630, 40720.0)))
            # ADD release_single right up
            elems += i3.SRef(reference=Release_horizontal(length=2750),
                             transformation=(i3.HMirror()+i3.Translation((45750-490, 13440.0-565))))
            elems += i3.SRef(reference=Release_horizontal(),
                             transformation=(i3.HMirror()+i3.Translation((45500-870, 16480.0))))
            elems += i3.SRef(reference=Release_vertical(),
                             transformation=i3.Translation((27558+442, 23000.0-435)))
            elems += i3.SRef(reference=Release_vertical(length=2750),
                             transformation=i3.Translation((27558+442, 31000.0-460)))

            # ADD release_single right down
            elems += i3.SRef(reference=Release_horizontal(),
                             transformation=(i3.HMirror()+i3.Translation((34625+21130, -10440.0+75))))

            elems += i3.SRef(reference=Release_vertical(),
                             transformation=i3.Translation((34625, -17000-120)))
            elems += i3.SRef(reference=Release_vertical(),
                             transformation=i3.Translation((34625+2000, -21480-85)))

            return elems

# GDS-file generation for debugging
# Coupon2(position=(-30000,-40000)).Layout.view.write_gdsii("Coupon.gds")
Coupon2().Layout.view.write_gdsii("Coupon4.gds")
print("Done writing Coupon.gds!") #Final GDS





# c1 = Coupon(name="haha1", length=2750, nb=16)     didn't work!!
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