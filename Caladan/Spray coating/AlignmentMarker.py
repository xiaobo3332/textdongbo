from LayerDefinitions import *   

class AlignmentMarker(i3.PCell):
        _name_prefix = "ALIGNMENT MARKER"  
        
        # Center of the structure
        position = i3.Coord2Property(default = (0.0, 0.0)) 
        
        # Layer
        layer = i3.LayerProperty(required = True)
        
        # Complement
        complement = i3.BoolProperty(default = False)
        
        # Protection 
        protection = i3.BoolProperty(default = False)
        
        # Marker parameters
        cross_length = i3.PositiveNumberProperty(default = 150.0)  
        cross_width = i3.PositiveNumberProperty(default = 16.0) 
        cross_margin = i3.PositiveNumberProperty(default = 4.0) 
        
        vernier_length = i3.PositiveNumberProperty(default = 30.0)  
        vernier_width = i3.PositiveNumberProperty(default = 8.0) 
        vernier_period = i3.PositiveNumberProperty(default = 20.25) 
        vernier_left_center = i3.Coord2Property(default = (-121.0, 24.0)) 
        vernier_top_center = i3.Coord2Property(default = (-6.0, 119.0))
        
        vernier_complement_length = i3.PositiveNumberProperty(default = 18.0)  
        vernier_complement_long_length = i3.PositiveNumberProperty(default = 28.0) 
        vernier_complement_width = i3.PositiveNumberProperty(default = 10.0)    
        vernier_complement_shift = i3.PositiveNumberProperty(default = 9.0) 
        vernier_complement_period = i3.PositiveNumberProperty(default = 20) 
        
        protection_length = i3.PositiveNumberProperty(default = 300.0)  
        protection_width = i3.PositiveNumberProperty(default = 320.0)
        
        # Layer text
        layer_text = i3.StringProperty(default = "Mesa")  
        
        class Layout(i3.LayoutView):
        
                def _generate_elements(self, elems):
                        
                        # Center of the structure
                        (x0, y0) = self.position   
                        
                        shift = 0.5*self.cross_width + self.cross_margin
                        square_length = 0.5*self.cross_length - shift
                        
                        if (self.complement == False and self.protection == False):
                                
                                # Add cross
                                elems += i3.Rectangle(layer = self.layer, center = (x0, y0), box_size = (self.cross_length, self.cross_width))                     
                                elems += i3.Rectangle(layer = self.layer, center = (x0, y0), box_size = (self.cross_width, self.cross_length))
                                
                                # Add rectangles left VERNIER
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_left_center[0], self.vernier_left_center[1]) , box_size = (self.vernier_length, self.vernier_width))  
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_left_center[0], self.vernier_left_center[1] + self.vernier_period) , box_size = (self.vernier_length, self.vernier_width)) 
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_left_center[0], self.vernier_left_center[1] + 2.0*self.vernier_period) , box_size = (self.vernier_length, self.vernier_width)) 
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_left_center[0], self.vernier_left_center[1] + 3.0*self.vernier_period) , box_size = (self.vernier_length, self.vernier_width)) 
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_left_center[0], self.vernier_left_center[1] + 4.0*self.vernier_period) , box_size = (self.vernier_length, self.vernier_width)) 
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_left_center[0], self.vernier_left_center[1] - self.vernier_period) , box_size = (self.vernier_length, self.vernier_width)) 
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_left_center[0], self.vernier_left_center[1] - 2.0*self.vernier_period) , box_size = (self.vernier_length, self.vernier_width)) 
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_left_center[0], self.vernier_left_center[1] - 3.0*self.vernier_period) , box_size = (self.vernier_length, self.vernier_width)) 
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_left_center[0], self.vernier_left_center[1] - 4.0*self.vernier_period) , box_size = (self.vernier_length, self.vernier_width))
                                
                                # Add rectangles top VERNIER
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_top_center[0], self.vernier_top_center[1]) , box_size = (self.vernier_width, self.vernier_length))  
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_top_center[0] + self.vernier_period, self.vernier_top_center[1]) , box_size = (self.vernier_width, self.vernier_length)) 
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_top_center[0] + 2.0*self.vernier_period, self.vernier_top_center[1]) , box_size = (self.vernier_width, self.vernier_length)) 
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_top_center[0] + 3.0*self.vernier_period, self.vernier_top_center[1]) , box_size = (self.vernier_width, self.vernier_length)) 
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_top_center[0] + 4.0*self.vernier_period, self.vernier_top_center[1]) , box_size = (self.vernier_width, self.vernier_length)) 
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_top_center[0] - self.vernier_period, self.vernier_top_center[1]) , box_size = (self.vernier_width, self.vernier_length)) 
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_top_center[0] - 2.0*self.vernier_period, self.vernier_top_center[1]) , box_size = (self.vernier_width, self.vernier_length)) 
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_top_center[0] - 3.0*self.vernier_period, self.vernier_top_center[1]) , box_size = (self.vernier_width, self.vernier_length)) 
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_top_center[0] - 4.0*self.vernier_period, self.vernier_top_center[1]) , box_size = (self.vernier_width, self.vernier_length))
                                
                                # Add TEXT
                                elems += i3.PolygonText(layer = self.layer, coordinate = (x0, y0 - 100.0), text = self.layer_text, height = 35.0)                  

                        elif (self.complement == True and self.protection == False):
                        
                                # Add squares
                                elems += i3.Rectangle(layer = self.layer, center = (x0 - 0.25*self.cross_length - 0.5*shift, y0 + 0.25*self.cross_length + 0.5*shift), box_size = (square_length, square_length))                     
                                elems += i3.Rectangle(layer = self.layer, center = (x0 + 0.25*self.cross_length + 0.5*shift, y0 + 0.25*self.cross_length + 0.5*shift), box_size = (square_length, square_length))  
                                elems += i3.Rectangle(layer = self.layer, center = (x0 - 0.25*self.cross_length - 0.5*shift, y0 - 0.25*self.cross_length - 0.5*shift), box_size = (square_length, square_length))  
                                elems += i3.Rectangle(layer = self.layer, center = (x0 + 0.25*self.cross_length + 0.5*shift, y0 - 0.25*self.cross_length - 0.5*shift), box_size = (square_length, square_length))  
                               
                                # Add rectangles left VERNIER
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_left_center[0] - self.vernier_complement_shift - 0.5*self.vernier_complement_long_length, self.vernier_left_center[1]), box_size = (self.vernier_complement_long_length, self.vernier_complement_width))  
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_left_center[0] + self.vernier_complement_shift + 0.5*self.vernier_complement_long_length, self.vernier_left_center[1]), box_size = (self.vernier_complement_long_length, self.vernier_complement_width))                     
                               
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_left_center[0] - self.vernier_complement_shift - 0.5*self.vernier_complement_length, self.vernier_left_center[1] + self.vernier_complement_period), box_size = (self.vernier_complement_length, self.vernier_complement_width))  
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_left_center[0] + self.vernier_complement_shift + 0.5*self.vernier_complement_length, self.vernier_left_center[1] + self.vernier_complement_period), box_size = (self.vernier_complement_length, self.vernier_complement_width))                     
                               
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_left_center[0] - self.vernier_complement_shift - 0.5*self.vernier_complement_length, self.vernier_left_center[1] + 2.0*self.vernier_complement_period), box_size = (self.vernier_complement_length, self.vernier_complement_width))  
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_left_center[0] + self.vernier_complement_shift + 0.5*self.vernier_complement_length, self.vernier_left_center[1] + 2.0*self.vernier_complement_period), box_size = (self.vernier_complement_length, self.vernier_complement_width))                     
                               
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_left_center[0] - self.vernier_complement_shift - 0.5*self.vernier_complement_length, self.vernier_left_center[1] + 3.0*self.vernier_complement_period), box_size = (self.vernier_complement_length, self.vernier_complement_width))  
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_left_center[0] + self.vernier_complement_shift + 0.5*self.vernier_complement_length, self.vernier_left_center[1] + 3.0*self.vernier_complement_period), box_size = (self.vernier_complement_length, self.vernier_complement_width))                     
                               
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_left_center[0] - self.vernier_complement_shift - 0.5*self.vernier_complement_length, self.vernier_left_center[1] + 4.0*self.vernier_complement_period), box_size = (self.vernier_complement_length, self.vernier_complement_width))  
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_left_center[0] + self.vernier_complement_shift + 0.5*self.vernier_complement_length, self.vernier_left_center[1] + 4.0*self.vernier_complement_period), box_size = (self.vernier_complement_length, self.vernier_complement_width))                     
                               
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_left_center[0] - self.vernier_complement_shift - 0.5*self.vernier_complement_length, self.vernier_left_center[1] - self.vernier_complement_period), box_size = (self.vernier_complement_length, self.vernier_complement_width))  
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_left_center[0] + self.vernier_complement_shift + 0.5*self.vernier_complement_length, self.vernier_left_center[1] - self.vernier_complement_period), box_size = (self.vernier_complement_length, self.vernier_complement_width))                     
                        
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_left_center[0] - self.vernier_complement_shift - 0.5*self.vernier_complement_length, self.vernier_left_center[1] - 2.0*self.vernier_complement_period), box_size = (self.vernier_complement_length, self.vernier_complement_width))  
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_left_center[0] + self.vernier_complement_shift + 0.5*self.vernier_complement_length, self.vernier_left_center[1] - 2.0*self.vernier_complement_period), box_size = (self.vernier_complement_length, self.vernier_complement_width))                     
                        
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_left_center[0] - self.vernier_complement_shift - 0.5*self.vernier_complement_length, self.vernier_left_center[1] - 3.0*self.vernier_complement_period), box_size = (self.vernier_complement_length, self.vernier_complement_width))  
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_left_center[0] + self.vernier_complement_shift + 0.5*self.vernier_complement_length, self.vernier_left_center[1] - 3.0*self.vernier_complement_period), box_size = (self.vernier_complement_length, self.vernier_complement_width))                     
                        
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_left_center[0] - self.vernier_complement_shift - 0.5*self.vernier_complement_length, self.vernier_left_center[1] - 4.0*self.vernier_complement_period), box_size = (self.vernier_complement_length, self.vernier_complement_width))  
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_left_center[0] + self.vernier_complement_shift + 0.5*self.vernier_complement_length, self.vernier_left_center[1] - 4.0*self.vernier_complement_period), box_size = (self.vernier_complement_length, self.vernier_complement_width))                     
                       
                                # Add rectangles top VERNIER
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_top_center[0], self.vernier_top_center[1] - self.vernier_complement_shift - 0.5*self.vernier_complement_long_length), box_size = (self.vernier_complement_width, self.vernier_complement_long_length))  
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_top_center[0], self.vernier_top_center[1] + self.vernier_complement_shift + 0.5*self.vernier_complement_long_length), box_size = (self.vernier_complement_width, self.vernier_complement_long_length))                     
                               
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_top_center[0] + self.vernier_complement_period, self.vernier_top_center[1] - self.vernier_complement_shift - 0.5*self.vernier_complement_length), box_size = (self.vernier_complement_width, self.vernier_complement_length))  
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_top_center[0] + self.vernier_complement_period, self.vernier_top_center[1] + self.vernier_complement_shift + 0.5*self.vernier_complement_length), box_size = (self.vernier_complement_width, self.vernier_complement_length))                     
                               
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_top_center[0] + 2.0*self.vernier_complement_period, self.vernier_top_center[1] - self.vernier_complement_shift - 0.5*self.vernier_complement_length), box_size = (self.vernier_complement_width, self.vernier_complement_length))  
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_top_center[0] + 2.0*self.vernier_complement_period, self.vernier_top_center[1] + self.vernier_complement_shift + 0.5*self.vernier_complement_length), box_size = (self.vernier_complement_width, self.vernier_complement_length))                     
                               
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_top_center[0] + 3.0*self.vernier_complement_period, self.vernier_top_center[1] - self.vernier_complement_shift - 0.5*self.vernier_complement_length), box_size = (self.vernier_complement_width, self.vernier_complement_length))  
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_top_center[0] + 3.0*self.vernier_complement_period, self.vernier_top_center[1] + self.vernier_complement_shift + 0.5*self.vernier_complement_length), box_size = (self.vernier_complement_width, self.vernier_complement_length))                     
                               
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_top_center[0] + 4.0*self.vernier_complement_period, self.vernier_top_center[1] - self.vernier_complement_shift - 0.5*self.vernier_complement_length), box_size = (self.vernier_complement_width, self.vernier_complement_length))  
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_top_center[0] + 4.0*self.vernier_complement_period, self.vernier_top_center[1] + self.vernier_complement_shift + 0.5*self.vernier_complement_length), box_size = (self.vernier_complement_width, self.vernier_complement_length))                     
                               
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_top_center[0] - self.vernier_complement_period, self.vernier_top_center[1] - self.vernier_complement_shift - 0.5*self.vernier_complement_length), box_size = (self.vernier_complement_width, self.vernier_complement_length))  
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_top_center[0] - self.vernier_complement_period, self.vernier_top_center[1] + self.vernier_complement_shift + 0.5*self.vernier_complement_length), box_size = (self.vernier_complement_width, self.vernier_complement_length))                     
                                
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_top_center[0] - 2.0*self.vernier_complement_period, self.vernier_top_center[1] - self.vernier_complement_shift - 0.5*self.vernier_complement_length), box_size = (self.vernier_complement_width, self.vernier_complement_length))  
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_top_center[0] - 2.0*self.vernier_complement_period, self.vernier_top_center[1] + self.vernier_complement_shift + 0.5*self.vernier_complement_length), box_size = (self.vernier_complement_width, self.vernier_complement_length))                     
                                
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_top_center[0] - 3.0*self.vernier_complement_period, self.vernier_top_center[1] - self.vernier_complement_shift - 0.5*self.vernier_complement_length), box_size = (self.vernier_complement_width, self.vernier_complement_length))  
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_top_center[0] - 3.0*self.vernier_complement_period, self.vernier_top_center[1] + self.vernier_complement_shift + 0.5*self.vernier_complement_length), box_size = (self.vernier_complement_width, self.vernier_complement_length))                     
                                
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_top_center[0] - 4.0*self.vernier_complement_period, self.vernier_top_center[1] - self.vernier_complement_shift - 0.5*self.vernier_complement_length), box_size = (self.vernier_complement_width, self.vernier_complement_length))  
                                elems += i3.Rectangle(layer = self.layer, center = (self.vernier_top_center[0] - 4.0*self.vernier_complement_period, self.vernier_top_center[1] + self.vernier_complement_shift + 0.5*self.vernier_complement_length), box_size = (self.vernier_complement_width, self.vernier_complement_length))                     
                               
                        else:
                                elems += i3.Rectangle(layer = self.layer, center = (x0 -43.5, y0 + 11.5) , box_size = (self.protection_length, self.protection_width))  
                               
                        return elems
        
# GDS-file generation for debugging
# AlignmentMarker(layer = lay_mesa).Layout.view.write_gdsii("AlignmentMarker.gds")
# print("Done writing AlignmentMarker.gds!")