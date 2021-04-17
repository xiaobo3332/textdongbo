from technologies import silicon_photonics
import ipkiss3.all as i3


class label(i3.PCell):
    _name_prefix = "label"

    # Center of the structure
    position = i3.Coord2Property(default=(0.0, 0.0))

    # Layer
    layer = i3.LayerProperty(default=i3.TECH.PPLAYER.HFW)

    # layer_bool = i3.LayerProperty(default=i3.TECH.PPLAYER.NONE.DOC)

    class Layout(i3.LayoutView):

        def _generate_elements(self, elems):
            # Center of the structure
            (x0, y0) = self.position
            x = 6000
            y = 7000
            Height = 180
            elems += i3.PolygonText(layer=self.layer,
                                    text="10_NO",
                                    # coordinate=(1300.0, 100.0),
                                    # alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
                                    font=2,
                                    height=Height,
                                    transformation=i3.Translation((x0, y0))
                                    )
            elems += i3.PolygonText(layer=self.layer,
                                    text="20_NO",
                                    # coordinate=(1300.0, 100.0),
                                    # alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
                                    font=2,
                                    height=Height,
                                    transformation=i3.Translation((x0 + 1 * x, y0 + 1 * y))
                                    )
            elems += i3.PolygonText(layer=self.layer,
                                    text="15_NOW",
                                    # coordinate=(1300.0, 100.0),
                                    # alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
                                    font=2,
                                    height=Height,
                                    transformation=i3.Translation((x0 + 0 * x, y0 + 1 * y))
                                    )
            elems += i3.PolygonText(layer=self.layer,
                                    text="15_NO",
                                    # coordinate=(1300.0, 100.0),
                                    # alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
                                    font=2,
                                    height=Height,
                                    transformation=i3.Translation((x0 + 1 * x, y0 + 0 * y))
                                    )
            elems += i3.PolygonText(layer=self.layer,
                                    text="10_NOW",
                                    # coordinate=(1300.0, 100.0),
                                    # alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
                                    font=2,
                                    height=Height,
                                    transformation=i3.Translation((x0 + 2 * x, y0 + 0 * y))
                                    )
            elems += i3.PolygonText(layer=self.layer,
                                    text="20_NOW",
                                    # coordinate=(1300.0, 100.0),
                                    # alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
                                    font=2,
                                    height=Height,
                                    transformation=i3.Translation((x0 + 2 * x, y0 + 1 * y))
                                    )

            return elems

# GDS-file generation for debugging
# label().Layout.view.write_gdsii("label.gds")
