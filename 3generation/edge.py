from technologies import silicon_photonics
from picazzo3.traces.wire_wg.trace import WireWaveguideTemplate
from picazzo3.traces.wire_wg import WireWaveguideTransitionLinear
from picazzo3.routing.place_route import PlaceAndAutoRoute
import ipkiss3.all as i3
from picazzo3.container.transition_ports import AutoTransitionPorts
from picazzo3.filters.mmi.cell import MMI1x2Tapered
from picazzo3.filters.mmi.cell import MMI2x1Tapered


class edge(PlaceAndAutoRoute):
    wg_sm = i3.WaveguideTemplateProperty()
    mmi_trace_template = i3.WaveguideTemplateProperty()
    mmi_access_template = i3.WaveguideTemplateProperty()


    WG2 = i3.ChildCellProperty()
    narro = i3.ChildCellProperty()

    # def _default_links(self):
    #     links = [("taper:out", "taper2:out")]
    #     return links

    def _default_child_cells(self):
        child_cells = dict()
        for counter in range(0, 48, 1):  # Routing dummy
            print counter
            child_cells['edge1' + str(counter)] = self.narro
            child_cells['edge2' + str(counter)] = self.WG2

        return child_cells

    def _default_trace_template(self):
        wg_sm2 = WireWaveguideTemplate()
        wg_sm2.Layout(core_width=15, cladding_width=15 + 24.0)
        return wg_sm2



    def _default_WG2(self):
        WG2 = i3.Waveguide(name="20", trace_template=self.wg_sm)
        return WG2

    def _default_narro(self):
        WGnarrow = i3.Waveguide(name="15", trace_template=self.trace_template)
        return WGnarrow

    def _default_wg_sm(self):
        wg_sm = WireWaveguideTemplate()
        wg_sm.Layout(core_width=20, cladding_width=20 + 24.0)
        return wg_sm

    def _default_mmi_trace_template(self):
        mmi_trace_template = WireWaveguideTemplate()
        mmi_trace_template.Layout(core_width=20.0, cladding_width=20.0 + 24.0)  # MMI_width
        return mmi_trace_template

    def _default_mmi_access_template(self):
        mmi_access_template = WireWaveguideTemplate()
        mmi_access_template.Layout(core_width=9.0, cladding_width=9.0 + 24.0)
        return mmi_access_template

    class Layout(PlaceAndAutoRoute.Layout):
        length = i3.PositiveNumberProperty(doc="MMI length", default=97)

        def _default_WG2(self):
            layout_WG2 = self.cell.WG2.get_default_view(i3.LayoutView)
            layout_WG2.set(shape=[(0.0, 0.0), (300.0, 0.0)])
            return layout_WG2

        def _default_narro(self):
            layout = self.cell.narro.get_default_view(i3.LayoutView)
            layout.set(shape=[(0.0, 0.0), (300.0, 0.0)])
            return layout



        def _default_child_transformations(self):
            trans = dict()
            for counter in range(0, 24, 1):
                trans['edge1' + str(counter)] = i3.Translation(translation=(-300,  counter * 150))
                trans['edge2' + str(counter)] = i3.Translation(translation=(-300, counter * 150+7500))
            for counter in range(24, 48,1):
                trans['edge1' + str(counter)] = i3.Translation(translation=(18600, counter * 150-2600))
                trans['edge2' + str(counter)] = i3.Translation(translation=(18600, counter * 150 + 7500-2600))

            return trans


# edge().Layout.view.visualize(annotate=True)
# edge().Layout.view.write_gdsii("edge.gds")
