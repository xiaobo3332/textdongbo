from technologies import silicon_photonics
from ipkiss3 import all as i3
from picazzo3.routing.place_route import PlaceAndAutoRoute
from picazzo3.routing.place_route import PlaceComponents
from picazzo3.wg.spirals import FixedLengthSpiralRounded
from picazzo3.traces.wire_wg import WireWaveguideTemplate
import joblib
import os
from merge_path import merge_path

class PathTraceWindow(i3.PathTraceWindow):
    def get_elements_from_shape(self, shape, termination_offsets = [], **kwargs):
        elems = super(PathTraceWindow, self).get_elements_from_shape(shape, termination_offsets=termination_offsets, **kwargs)

        elems = i3.ElementList([
            i3.Path(layer=el.layer, shape=el.centerline_shape,  line_width=el.path_line_width)
            if el.path_line_width == 0 else el
            for el in elems
        ])

        # print([(el.layer, getattr(el, 'line_width', None), type(el)) for el in elems])
        return elems

class LinearWindowWaveguideTransition(i3.LinearWindowWaveguideTransition):
    class Layout(i3.LinearWindowWaveguideTransition.Layout):
        def _generate_elements(self, elems):
            elems = super(LinearWindowWaveguideTransition.Layout, self)._generate_elements(elems)
            # shape_shift = ShapeOffset(original_shape=elems.shape, offset=self.offset)
            fbms_line = i3.ElementList()
            for el in elems:
                if el.layer==i3.TECH.PPLAYER.WG.CLADDING:
                    el_shape = el.shape
                    el_shape.open()
                    fbms_line += [i3.Path(layer=el.layer, shape=el_shape, line_width=0.0)]
            return elems+fbms_line

class StraightWgLossEbeam(PlaceAndAutoRoute):
    taper = i3.ChildCellProperty()
    wg = i3.ChildCellProperty()
    wg_right = i3.ChildCellProperty()
    expanded_wg = i3.ChildCellProperty()
    trace_template = i3.WaveguideTemplateProperty()
    expanded_wg_template = i3.WaveguideTemplateProperty()
    gc_taper = i3.ChildCellProperty()
    gc_slab = i3.ChildCellProperty()
    gc_slab_template = i3.WaveguideTemplateProperty()
    wg_SM_template = i3.WaveguideTemplateProperty()
    wg_SM = i3.ChildCellProperty()
    taper_expanded_wg2wg_SM = i3.ChildCellProperty()

    wg_width = i3.PositiveNumberProperty(default=2.0)
    trench_width = i3.PositiveNumberProperty(default=3.0)
    _wg_width_indesign = i3.PositiveNumberProperty()
    expanded_wg_width = i3.PositiveNumberProperty(default=3.0)
    _expanded_wg_width_indesign = i3.PositiveNumberProperty()
    gc_slab_width = i3.PositiveNumberProperty(default=10.0)
    wg_SM_width = i3.PositiveNumberProperty(default=0.5)

    def _default__wg_width_indesign(self):
        return self.wg_width

    def _default__expanded_wg_width_indesign(self):
        return self.expanded_wg_width

    def _default_trace_template(self):
        wstart1 = PathTraceWindow(layer=i3.TECH.PPLAYER.WG.CORE, start_offset=-self.wg_width*0.5, end_offset=self.wg_width*0.5)
        wstart2 = PathTraceWindow(layer=i3.TECH.PPLAYER.WG.CLADDING, start_offset=-(self.wg_width+self.trench_width)*0.5, end_offset=-(self.wg_width+self.trench_width)*0.5, line_width=0)
        wstart3 = PathTraceWindow(layer=i3.TECH.PPLAYER.WG.CLADDING, start_offset=(self.wg_width+self.trench_width)*0.5, end_offset=(self.wg_width+self.trench_width)*0.5, line_width=0)
        wg_t = i3.WindowWaveguideTemplate()
        wg_t.Layout(windows=[wstart1, wstart2, wstart3])
        return wg_t

    def _default_expanded_wg_template(self):
        wstart1 = PathTraceWindow(layer=i3.TECH.PPLAYER.WG.CORE, start_offset=-self.expanded_wg_width*0.5, end_offset=self.expanded_wg_width*0.5)
        wstart2 = PathTraceWindow(layer=i3.TECH.PPLAYER.WG.CLADDING, start_offset=-(self.expanded_wg_width+self.trench_width)*0.5, end_offset=-(self.expanded_wg_width+self.trench_width)*0.5, line_width=0)
        wstart3 = PathTraceWindow(layer=i3.TECH.PPLAYER.WG.CLADDING, start_offset=(self.expanded_wg_width+self.trench_width)*0.5, end_offset=(self.expanded_wg_width+self.trench_width)*0.5, line_width=0)
        expanded_wg_template = i3.WindowWaveguideTemplate()
        expanded_wg_template.Layout(windows=[wstart1, wstart2, wstart3])
        return expanded_wg_template

    def _default_wg(self):
        wg = i3.RoundedWaveguide(trace_template=self.trace_template)
        return wg

    def _default_wg_right(self):
        wg_right = i3.RoundedWaveguide(trace_template=self.trace_template)
        return wg_right

    def _default_expanded_wg(self):
        expanded_wg = i3.RoundedWaveguide(trace_template=self.expanded_wg_template)
        return expanded_wg

    def _default_taper(self):
        taper = i3.LinearWindowWaveguideTransition(start_trace_template=self.trace_template, end_trace_template=self.expanded_wg_template)
        return taper

    def _default_gc_slab_template(self):
        wstart1 = PathTraceWindow(layer=i3.TECH.PPLAYER.WG.CORE, start_offset=-self.gc_slab_width*0.5, end_offset=self.gc_slab_width*0.5)
        wstart2 = PathTraceWindow(layer=i3.TECH.PPLAYER.WG.CLADDING, start_offset=-(self.gc_slab_width+self.trench_width)*0.5, end_offset=-(self.gc_slab_width+self.trench_width)*0.5, line_width=0)
        wstart3 = PathTraceWindow(layer=i3.TECH.PPLAYER.WG.CLADDING, start_offset=(self.gc_slab_width+self.trench_width)*0.5, end_offset=(self.gc_slab_width+self.trench_width)*0.5, line_width=0)
        wg_t = i3.WindowWaveguideTemplate()
        wg_t.Layout(windows=[wstart1, wstart2, wstart3])
        return wg_t

    def _default_gc_taper(self):
        taper = i3.LinearWindowWaveguideTransition(start_trace_template=self.wg_SM_template, end_trace_template=self.gc_slab_template)
        return taper

    def _default_gc_slab(self):
        slab = i3.RoundedWaveguide(trace_template=self.gc_slab_template)
        return slab

    def _default_wg_SM_template(self):
        wstart1 = PathTraceWindow(layer=i3.TECH.PPLAYER.WG.CORE, start_offset=-self.wg_SM_width*0.5, end_offset=self.wg_SM_width*0.5)
        wstart2 = PathTraceWindow(layer=i3.TECH.PPLAYER.WG.CLADDING, start_offset=-(self.wg_SM_width+self.trench_width)*0.5, end_offset=-(self.wg_SM_width+self.trench_width)*0.5, line_width=0)
        wstart3 = PathTraceWindow(layer=i3.TECH.PPLAYER.WG.CLADDING, start_offset=(self.wg_SM_width+self.trench_width)*0.5, end_offset=(self.wg_SM_width+self.trench_width)*0.5, line_width=0)
        wg_t = i3.WindowWaveguideTemplate()
        wg_t.Layout(windows=[wstart1, wstart2, wstart3])
        return wg_t

    def _default_wg_SM(self):
        wg = i3.RoundedWaveguide(trace_template=self.wg_SM_template)
        return wg

    def _default_taper_expanded_wg2wg_SM(self):
        taper = i3.LinearWindowWaveguideTransition(start_trace_template=self.expanded_wg_template, end_trace_template=self.wg_SM_template)
        return taper

    def _default_child_cells(self):
        child_cells = dict()
        child_cells["taper_left"] = self.taper
        child_cells["taper_right"] = self.taper
        child_cells["wg_left"] = self.wg
        child_cells["wg_right"] = self.wg_right
        child_cells["expanded_wg_left"] = self.expanded_wg
        child_cells["expanded_wg_right"] = self.expanded_wg
        child_cells["taper_expanded_wg2wg_SM_left"] = self.taper_expanded_wg2wg_SM
        child_cells["wg_SM_left"] = self.wg_SM
        child_cells["wg_SM_right"] = self.wg_SM
        child_cells["taper_expanded_wg2wg_SM_right"] = self.taper_expanded_wg2wg_SM
        child_cells["gc_taper_left"] = self.gc_taper
        child_cells["gc_taper_right"] = self.gc_taper
        child_cells["gc_slab_left"] = self.gc_slab
        child_cells["gc_slab_right"] = self.gc_slab
        return child_cells

    def _default_external_port_names(self):
        ports = dict()
        ports["expanded_wg_right:out"] = "in"
        ports["expanded_wg_left:out"] = "out"
        return ports


    class Layout(PlaceAndAutoRoute.Layout):
        spiral_width = i3.PositiveNumberProperty(doc="total width of spiral structure",default=6000.0)
        right_wg_length = i3.PositiveNumberProperty(doc="length of narrow wg on the right side of spiral", default=500.0)
        expanded_wg_length = i3.PositiveNumberProperty(default=1000.0)
        taper_length = i3.PositiveNumberProperty(default=100.0)
        bend_radius = i3.PositiveNumberProperty(default=100.0)
        gc_taper_length = i3.PositiveNumberProperty(default=300.0)
        gc_slab_length = i3.PositiveNumberProperty(default=50.0)
        wg_SM_length = i3.PositiveNumberProperty(default=50.0)

        def _default_wg(self):
            wg_lo = self.cell.wg.get_default_view(i3.LayoutView)
            wg_lo.set(shape=[(0.0,0.0), (self.spiral_width,0)])
            return wg_lo

        def _default_wg_right(self):
            wg_right_lo = self.cell.wg_right.get_default_view(i3.LayoutView)
            wg_right_lo.set(shape=[(0.0,0.0), (self.right_wg_length, 0)])
            return wg_right_lo

        def _default_taper(self):
            taper_lo = self.cell.taper.get_default_view(i3.LayoutView)
            taper_lo.set(start_position=(0.0,0.0), end_position=(self.taper_length,0.0))
            return taper_lo

        def _default_expanded_wg(self):
            expanded_wg_lo = self.cell.expanded_wg.get_default_view(i3.LayoutView)
            expanded_wg_lo.set(shape=[(0.0,0.0), (self.expanded_wg_length,0.0)])
            return expanded_wg_lo

        def _default_gc_taper(self):
            gc_taper_lo = self.cell.gc_taper.get_default_view(i3.LayoutView)
            gc_taper_lo.set(start_position=(0.0,0.0), end_position=(self.gc_taper_length,0.0))
            return gc_taper_lo

        def _default_gc_slab(self):
            slab_lo = self.cell.gc_slab.get_default_view(i3.LayoutView)
            slab_lo.set(shape=[(0.0,0.0), (self.gc_slab_length,0.0)])
            return slab_lo

        def _default_wg_SM(self):
            wg_lo = self.cell.wg_SM.get_default_view(i3.LayoutView)
            wg_lo.set(shape=[(0.0,0.0), (self.wg_SM_length,0)])
            return wg_lo

        def _default_taper_expanded_wg2wg_SM(self):
            taper_lo = self.cell.taper_expanded_wg2wg_SM.get_default_view(i3.LayoutView)
            taper_lo.set(start_position=(0.0,0.0), end_position=(self.taper_length,0.0))
            return taper_lo

        def _default_child_transformations(self):
            trans = dict()
            trans["wg_right"] = (0.0, 0.0)
            trans["taper_right"] = i3.Translation((self.right_wg_length,0))

            start_x_expanded_wg_right = self.right_wg_length+self.taper_length
            trans["expanded_wg_right"] = i3.Translation((start_x_expanded_wg_right,0))

            start_x_taper_wg_SM2expanded_wg_right = start_x_expanded_wg_right+self.expanded_wg_length
            trans["taper_expanded_wg2wg_SM_right"] = i3.Translation((start_x_taper_wg_SM2expanded_wg_right,0.0))

            start_x_wg_SM_right = start_x_taper_wg_SM2expanded_wg_right+self.taper_length
            trans["wg_SM_right"] = i3.Translation((start_x_wg_SM_right, 0.0))

            start_x_gc_taper_right = start_x_wg_SM_right + self.wg_SM_length
            trans["gc_taper_right"] = i3.Translation((start_x_gc_taper_right,0))

            start_x_gc_slab_right = start_x_gc_taper_right + self.gc_taper_length
            trans["gc_slab_right"] = i3.Translation((start_x_gc_slab_right,0))

            trans["wg_left"] = i3.HMirror(mirror_plane_x=0.0)
            trans["taper_left"] = i3.HMirror(mirror_plane_x=0.0) + i3.Translation((-self.spiral_width,0))

            start_x_expanded_wg_left = -self.spiral_width-self.taper_length
            trans["expanded_wg_left"] = i3.HMirror(mirror_plane_x=0.0) + i3.Translation((start_x_expanded_wg_left,0))

            start_x_taper_expanded_wg2wg_SM_left = start_x_expanded_wg_left-self.expanded_wg_length
            trans["taper_expanded_wg2wg_SM_left"] = i3.HMirror(mirror_plane_x=0.0) + i3.Translation((start_x_taper_expanded_wg2wg_SM_left,0))

            start_x_wg_SM_left = start_x_taper_expanded_wg2wg_SM_left - self.taper_length
            trans["wg_SM_left"] = i3.HMirror(mirror_plane_x=0.0) + i3.Translation((start_x_wg_SM_left,0))

            start_x_gc_taper_left = start_x_wg_SM_left - self.wg_SM_length
            trans["gc_taper_left"] = i3.HMirror(mirror_plane_x=0.0) + i3.Translation((start_x_gc_taper_left,0))

            start_x_gc_slab_left = start_x_gc_taper_left - self.gc_taper_length
            trans["gc_slab_left"] = i3.HMirror(mirror_plane_x=0.0) + i3.Translation((start_x_gc_slab_left,0))

            return trans

        def get_true_length(self):
            return self.spiral_width+self.right_wg_length


class StraightWgLossEbeamFBMSMerged(i3.PCell):
    ## merge FBMS paths combined with Class:SpiralWgLossEbeam2
    wg_width = i3.PositiveNumberProperty(default=3.0)

    class Layout(i3.LayoutView):

        def _generate_elements(self, elems):
            SpiralWg = StraightWgLossEbeam(wg_width=self.wg_width)
            lo = SpiralWg.Layout()
            shapes = lo.layout.flat_copy()
            paths = []
            for shape in shapes:
                if shape.layer == i3.TECH.PPLAYER.WG.CLADDING:
                    paths.append(shape)
                    # print shape_absolute.shape.points
            merged_paths = merge_path(paths)
            elems += merged_paths
            elems += shapes
            print "straight length", lo.get_true_length()
            return elems


SpiralWg = StraightWgLossEbeamFBMSMerged(wg_width=0.5)
lo = SpiralWg.Layout()
gds_name = os.path.join(os.curdir, "straight_wg.gds")
lo.write_gdsii(gds_name)
# print(lo.get_true_length())

