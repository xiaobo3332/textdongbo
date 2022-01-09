from LayerDefinitions import *   
from AlignmentMarker import AlignmentMarker

class AlignmentMarkerSet(i3.PCell):
        _name_prefix = "ALIGNMENT MARKER SET"  
        
        # Center of the structure
        position = i3.Coord2Property(default = (0.0, 0.0)) 
        
        # Orientation
        horizontal = i3.BoolProperty(default = True)
        
        # Spacing
        v_spacing = i3.PositiveNumberProperty(default = 320.0)
        h_spacing = i3.PositiveNumberProperty(default = 300.0)
        
        class Layout(i3.LayoutView):
        
                def _generate_elements(self, elems):
                        
                        # Center of the structure
                        (x0, y0) = self.position   
                        
                        if self.horizontal == True:
                                  
                                # ADD RELEASE
                                elems += i3.SRef(reference = AlignmentMarker(layer = lay_island, layer_text = "Release"), transformation = i3.Translation((x0 + 0.0*self.h_spacing, y0)))
                                elems += i3.SRef(reference = AlignmentMarker(layer = lay_release, complement = True), transformation = i3.Translation((x0 + 0.0*self.h_spacing, y0))) 
                                                               
                                # ADD TETHER
                                elems += i3.SRef(reference = AlignmentMarker(layer = lay_island, layer_text = "Tether"), transformation = i3.Translation((x0 + 1.0*self.h_spacing, y0)))
                                elems += i3.SRef(reference = AlignmentMarker(layer = lay_release, protection = True), transformation = i3.Translation((x0 + 1.0*self.h_spacing, y0)))
                                elems += i3.SRef(reference = AlignmentMarker(layer = lay_tether, complement = True), transformation = i3.Translation((x0 + 1.0*self.h_spacing, y0))) 
                        else:
                        
                                # ADD RELEASE
                                elems += i3.SRef(reference = AlignmentMarker(layer = lay_release, layer_text = "Marker"), transformation = i3.Translation((x0 + 0.0*self.h_spacing, y0)))
                                elems += i3.SRef(reference = AlignmentMarker(layer = lay_island, complement = True), transformation = i3.Translation((x0 + 0.0*self.h_spacing, y0)))
                        
                                # ADD TETHER
                                elems += i3.SRef(reference = AlignmentMarker(layer = lay_release, layer_text = "Back up"), transformation = i3.Translation((x0, y0 - 1.0*self.v_spacing)))
                                # elems += i3.SRef(reference = AlignmentMarker(layer = lay_island, protection = True), transformation = i3.Translation((x0, y0 - 1.0*self.v_spacing)))
                                # elems += i3.SRef(reference = AlignmentMarker(layer = lay_tether, complement = True), transformation = i3.Translation((x0, y0 - 1.0*self.v_spacing)))
                               
                        return elems
        
# GDS-file generation for debugging
# AlignmentMarkerSet(horizontal = True).Layout.view.write_gdsii("AlignmentMarkerSet.gds")
# print("Done writing AlignmentMarkerSet.gds!")