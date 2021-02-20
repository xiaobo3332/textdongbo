class MyOuter:  #github test
    age=18
    def __init__(self,name):
        self.name=name
    @classmethod
    def outer_class_method(cls):
        print('outer method')

    class MyInner:
        def __init__(self,inner_name):
            self.inner_name=inner_name
        def inner_method(self):
            print('inner method')
            MyOuter.outer_class_method()
            print(MyOuter.age)

out=MyOuter('lqz')
inner=out.MyInner('lqz_inner')
inner.inner_method()
# w_ebeam =1.5
# w_core = 10
# w_clad = 3
#
# print 1000.0+w_core
# # w_core = w_core+w_ebeam
# # w_clad = w_core-2*w_ebeam+2*w_clad
# # print   w_core,w_clad
# print 4//3
# w_core = w_core+w_ebeam
# w_clad = w_core+2*w_ebeam
# print   w_core,w_clad

# # print ("hello")
# # str1=123  # type: int
# # print (str1)
# #
# # str=[1,2,3]
# # print (str)
# for counter in range(0, 8, 1):
#     print counter

#
# from technologies import silicon_photonics
# # from ipkiss3 import all as i3
#
# # 2. Import other python libraries.
# # import numpy as np
# # import pylab as plt
#
# from picazzo3.filters.mmi.cell import MMI1x2Tapered
# from picazzo3.container.transition_ports import AutoTransitionPorts
# # from picazzo3.filters.mmi.cell import MMI2x1Tapered
# # from picazzo3.filters.mmi.cell import MMI2x2Tapered
# # from picazzo3.filters.mzi import MZIWaveguides
# from picazzo3.traces.wire_wg.trace import WireWaveguideTemplate
# # from ipkiss.geometry.shapes.spline import ShapeRoundAdiabaticSpline
# # from picazzo3.container.transition_ports import AutoTransitionPorts
# #
# # # MMI12 = i3.ChildCellProperty(default=[])
# # # 	MMI21_list = i3.ChildCellListProperty(default=[])
# # #
# # # MI12 = i3.ChildCellProperty(default=[])
# #
# wg_sm2 = WireWaveguideTemplate()
# wg_sm2.Layout(core_width=3.1, cladding_width=3.1+16.0)
#
# port_label=["in"]
# MMI12 = MMI1x2Tapered(port_labels=port_label)
# MMI12_layout = MMI12.Layout()
#
# mmi1_21_taper = AutoTransitionPorts(contents = MMI12,
#                                            port_labels = ['out1',"out2"],
#                                            trace_template = wg_sm2)
# #MMI12_layout.visualize(annotate=True)
# layout= mmi1_21_taper.Layout()
# layout.visualize(annotate=True)
# #MMI12_layout.write_gdsii("my_mmi test.gds")
#
