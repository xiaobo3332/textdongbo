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
            x = 6200
            y = 8000
            Height = 300
            elems += i3.PolygonText(layer=self.layer,
                                    text="1N",
                                    # coordinate=(1300.0, 100.0),
                                    # alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
                                    font=2,
                                    height=Height,
                                    transformation=i3.Translation((x0, y0))
                                    )
            elems += i3.PolygonText(layer=self.layer,
                                    text="5J",
                                    # coordinate=(1300.0, 100.0),
                                    # alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
                                    font=2,
                                    height=Height,
                                    transformation=i3.Translation((x0 + 1 * x, y0 + 1 * y+700))
                                    )
            elems += i3.PolygonText(layer=self.layer,
                                    text="4W",
                                    # coordinate=(1300.0, 100.0),
                                    # alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
                                    font=2,
                                    height=Height,
                                    transformation=i3.Translation((x0 + 0 * x, y0 + 1 * y))
                                    )
            elems += i3.PolygonText(layer=self.layer,
                                    text="2E",
                                    # coordinate=(1300.0, 100.0),
                                    # alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
                                    font=2,
                                    height=Height,
                                    transformation=i3.Translation((x0 + 1 * x, y0 + 0 * y+1100))
                                    )
            elems += i3.PolygonText(layer=self.layer,
                                    text="3W",
                                    # coordinate=(1300.0, 100.0),
                                    # alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
                                    font=2,
                                    height=Height,
                                    transformation=i3.Translation((x0 + 2 * x, y0 + 0 * y))
                                    )
            elems += i3.PolygonText(layer=self.layer,
                                    text="6E",
                                    # coordinate=(1300.0, 100.0),
                                    # alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
                                    font=2,
                                    height=Height,
                                    transformation=i3.Translation((x0 + 2 * x, y0 + 1 * y))
                                    )

            return elems

# GDS-file generation for debugging
# label().Layout.view.write_gdsii("label.gds")
