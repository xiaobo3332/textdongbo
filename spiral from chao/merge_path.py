from technologies import silicon_photonics
from ipkiss3 import all as i3
import numpy as np

def merge_path(paths):

    ## firstly expand the transformation
    for path in paths:
        path.expand_transform()

    lines = []
    layer = i3.TECH.PPLAYER.NONE.DOC
    paths_in_loop = paths[:]

    for path0 in paths:
        if path0 not in paths_in_loop:
            pass

        else:

            finish_flag = 0
            line = path0.shape.points[:]
            rtol = 0
            atol = 2e-04

            while finish_flag==0:
                finish_flag = 1
                for path in paths:
                    if path not in paths_in_loop:
                        pass

                    elif np.array_equal(line, path.shape.points[:]):
                        # np.array_equal(line, path.shape.points):
                        # print "enter1"
                        # print path
                        paths_in_loop.remove(path)
                        finish_flag = 0

                    elif np.allclose(line[-1],path.shape.points[0],atol=atol,rtol=rtol):
                        # print "enter3"
                        # print line
                        line = np.concatenate((line,path.shape.points[1:]))
                        # print path.shape.points
                        # print line
                        paths_in_loop.remove(path)
                        finish_flag = 0

                    elif np.allclose(line[0],path.shape.points[-1],atol=atol,rtol=rtol):
                        # print "enter2"
                        # print line
                        line = np.concatenate((path.shape.points[:-1],line))
                        # print path.shape.points
                        # print line
                        paths_in_loop.remove(path)
                        finish_flag = 0

                    elif np.allclose(line[0],path.shape.points[0],atol=atol,rtol=rtol):
                        # print "enter4"
                        line = line[::-1]
                        # print path.shape.points
                        # print line
                        line = np.concatenate((line,path.shape.points[1:]))
                        # print line
                        paths_in_loop.remove(path)
                        finish_flag = 0

                    elif np.allclose(line[-1],path.shape.points[-1],atol=atol,rtol=rtol):
                        # print "enter5"
                        line = line[::-1]
                        # print path.shape.points
                        # print line
                        line = np.concatenate((path.shape.points[:-1],line))
                        # print line
                        paths_in_loop.remove(path)
                        finish_flag = 0

                    else:
                        pass


            lines.append(line)

    merged_path = i3.ElementList()
    for l in lines:
        merged_path += [i3.Path(layer=layer, line_width=0, shape=l)]

    return merged_path







