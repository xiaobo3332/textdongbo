from technologies import silicon_photonics
import ipkiss3.all as i3


class dicingMarker(i3.PCell):
    _name_prefix = "markers"

    # Center of the structure
    position = i3.Coord2Property(default=(0.0, 0.0))

    # Layer
    layer = i3.LayerProperty(default=i3.TECH.PPLAYER.HFW)

    # layer_bool = i3.LayerProperty(default=i3.TECH.PPLAYER.NONE.DOC)

    class Layout(i3.LayoutView):

        def _generate_elements(self, elems):
            # Center of the structure
            (x0, y0) = self.position
            elems += i3.Rectangle(layer=self.layer, center=(8900, 7100),
                                  box_size=(21000, 200))

            for i in range(0, 4, 1):
                for j in range(0, 3, 1):
                    elems += i3.Rectangle(layer=self.layer, center=(x0 + i * 6200 - 100, y0 + j * 8000 - 1000),
                                          box_size=(100, 100))
                    elems += i3.Rectangle(layer=self.layer, center=(x0 + 200 + i * 6200 - 100, y0 + j * 8000 - 1000),
                                          box_size=(100, 100))
                    elems += i3.Rectangle(layer=self.layer, center=(x0 + i * 6200 - 100, y0 + 200 + j * 8000 - 1000),
                                          box_size=(100, 100))
                    elems += i3.Rectangle(layer=self.layer,
                                          center=(x0 + i * 6200 + 200 - 100, y0 + 200 + j * 8000 - 1000),
                                          box_size=(100, 100))
                    elems += i3.Rectangle(layer=self.layer,
                                          center=(x0 + i * 6200 + 400 - 100, y0 + 200 + j * 8000 - 1000),
                                          box_size=(100, 100))
                    elems += i3.Rectangle(layer=self.layer,
                                          center=(x0 + i * 6200 - 200 - 100, y0 + 200 + j * 8000 - 1000),
                                          box_size=(100, 100))
                    for k in range(0, 20, 1):
                        if i == 2:
                            continue

                        elems += i3.Rectangle(layer=self.layer,
                                              center=(-1000 + 0 + i * 6200, 1000 + 10 * k + j * 7000 - 600),
                                              box_size=(500, 0.6 + 0.2 * k))
                        elems += i3.PolygonText(layer=self.layer,
                                                text="{}".format(str(k)),
                                                # coordinate=(1300.0, 100.0),
                                                # alignment=(i3.TEXT_ALIGN_LEFT, i3.TEXT_ALIGN_LEFT),
                                                font=2,
                                                height=7.0,
                                                transformation=i3.Translation(
                                                    (-1000 + 260 + i * 6200, 1000 + 3 + 10 * k + j * 7000 - 600))
                                                )
            elems += i3.Rectangle(layer=i3.TECH.PPLAYER.NONE.DOC, center=(8900, 7100),
                                  box_size=(21000, 16400))
            for i in range(0, 4, 1):
                for j in range(0, 2, 1):
                        elems += i3.Rectangle(layer=self.layer, center=(x0 + 6200*i, y0 + 7900*j +6300),
                                              box_size=(300, 1000))
            # elems += i3.Rectangle(layer=self.layer, center=(x0 + 200 + 6200 - 100, y0 + 8000 - 1000),
            #                       box_size=(300, 300))

            # elems += i3.Rectangle(layer=i3.TECH.PPLAYER.CONTACT.PILLAR, center=(8500, 7500),
            #                       box_size=(22000, 18000))

            return elems


# GDS-file generation for debugging
dicingMarker().Layout.view.write_gdsii("dicingmarkers.gds")
