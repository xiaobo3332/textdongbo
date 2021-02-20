from technologies import silicon_photonics
from ipkiss3 import all as i3
from picazzo3.fibcoup.uniform.cell import UniformLineGrating
from picazzo3.traces.wire_wg.trace import WireWaveguideTemplate
from picazzo3.container.transition_ports import AutoTransitionPorts
from picazzo3.routing.place_route import PlaceAndAutoRoute

class tapered_GratingCoupler_extension(PlaceAndAutoRoute):
    gc = i3.ChildCellProperty()
    tapered_gc = i3.ChildCellProperty()
    wg_socket = i3.WaveguideTemplateProperty()
    wg = i3.ChildCellProperty()

    def _default_trace_template(self):
        wg_t = WireWaveguideTemplate()
        wg_t.Layout(core_width=0.8, cladding_width=6.8)
        return wg_t

    def _default_wg(self):
        wg = i3.RoundedWaveguide(trace_template=self.trace_template)
        return wg


    def _default_wg_socket(self):
        wg_socket = WireWaveguideTemplate()
        wg_socket.Layout(core_width=12.0, cladding_width=18.0)
        return wg_socket

    def _default_gc(self):
        gc = UniformLineGrating(trace_template=self.wg_socket)
        return gc

    def _default_tapered_gc(self):
        tapered_gc = AutoTransitionPorts(contents=self.gc, trace_template=self.trace_template, port_labels=["out"])
        return tapered_gc

    def _default_child_cells(self):
        child_cells = dict()
        child_cells["tapered_gc"] = self.tapered_gc
        child_cells["wg"] = self.wg
        return child_cells

    def _default_links(self):
        links = [("tapered_gc:out", "wg:in")]
        return links

    def _default_external_port_names(self):
        ports = dict()
        ports["tapered_gc:vertical_in"] = "vertical_in"
        ports["wg:out"] = "out"
        return ports

    class Layout(PlaceAndAutoRoute.Layout):

        period = i3.PositiveNumberProperty(doc="period of grating", default=0.95)
        n_o_periods = i3.PositiveIntProperty(doc="number of periods of grating", default=16)
        line_width = i3.PositiveNumberProperty(doc="width of the grating")
        line_length = i3.PositiveNumberProperty(doc="length of the grating", default=13.0)
        socket_length = i3.PositiveNumberProperty(doc="length of socket")
        # transition_length = i3.PositiveNumberProperty(doc="length of the taper")
        transition_length = i3.PositiveNumberProperty(doc="taper length", default=100.0)
        extension_length = i3.PositiveNumberProperty(doc="extra straight length", default=100.0)

        def _default_line_width(self):
            return self.period * 0.5

        def _default_socket_length(self):
            return self.period * self.n_o_periods + 2.0

        def _default_gc(self):
            gc_lo = self.cell.gc.get_default_view(i3.LayoutView)
            gc_lo.set(period=self.period, n_o_periods=self.n_o_periods, line_width=self.line_width, line_length=self.line_length)
            return gc_lo

        def _default_tapered_gc(self):
            tapered_gc_lo = self.cell.tapered_gc.get_default_view(i3.LayoutView)
            tapered_gc_lo.set(transition_length=self.transition_length)
            return tapered_gc_lo

        def _default_wg(self):
            wg_lo = self.cell.wg.get_default_view(i3.LayoutView)
            wg_lo.set(shape=[(0.0, 0.0), (self.extension_length, 0.0)])
            return wg_lo

        def _default_child_transformations(self):
            trans = dict()
            trans["tapered_gc"] = (0, 0)
            trans["wg"] = i3.Translation(self.tapered_gc.ports["out"].position) + i3.Translation((10, 0))
            return trans


gc = tapered_GratingCoupler_extension()
gc_lo = gc.Layout(period=0.9, transition_length=300)
gc_lo.visualize(annotate=True)
gc_lo.write_gdsii('gc.gds')