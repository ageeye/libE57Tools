LIBRARY  = '.../liblibE57Tools.0.1.0.dylib'
TESTFILE = u'.../Downloads/bunnyDouble.e57'
MINDISTANCE = 0.03 # to disable set the value < 0

import ctypes, Points


class ToolsFileInfo(ctypes.Structure):
     _fields_ = [('channels', ctypes.c_int64),
                 ('cartesianX', ctypes.c_int64),
                 ('cartesianY', ctypes.c_int64),
                 ('cartesianZ', ctypes.c_int64),
                 ("cartesianInvalidState", ctypes.c_int64),
                 ('intensity', ctypes.c_int64),
                 ('colorRed', ctypes.c_int64),
                 ('colorGreen', ctypes.c_int64),
                 ('colorBlue', ctypes.c_int64),
                 ('columnIndex', ctypes.c_int64),
                 ('rowIndex', ctypes.c_int64),
                 ('BuffersFloatsCount', ctypes.c_int64),
                 ('BuffersIntsCount', ctypes.c_int64)]

class E57Tools:

    def __init__(self, fname):
        e57tools = ctypes.CDLL(LIBRARY)
        pname = ctypes.c_char_p(fname.encode('utf-8'))
 
        # get infos from file
        ptrToolsFileInfo = ctypes.POINTER(ToolsFileInfo)
        rct = e57tools.recordCount
        rct.argtypes = [ctypes.c_char_p, ptrToolsFileInfo]
        rct.restype = ctypes.c_int64
        info = ToolsFileInfo()
        info.colorRed   = -1
        info.colorGreen = -1
        info.colorBlue  = -1
        count = e57tools.recordCount(pname, info) 
        okXYZ = info.cartesianX != info.cartesianY != info.cartesianZ
        
        # read data if all is ok
        if (count>0 and okXYZ):
            XYZ = ctypes.c_double * info.BuffersFloatsCount * count
            ptrXYZ = ctypes.POINTER(XYZ)
            xyz = XYZ()
            OTHERS = ctypes.c_int64 * info.BuffersIntsCount * count
            ptrOTHERS = ctypes.POINTER(OTHERS)
            others = OTHERS()

            imf = e57tools.importfile
            imf.argtypes = [ctypes.c_char_p, ptrXYZ, ptrOTHERS]
            imf.restype = ctypes.c_int64

            count = e57tools.importfile(pname, xyz, others) 
            
            self.pts = []
            colormap = []
            last = None
            if count > 0:
                for i in range(count):
                    x = xyz[i][info.cartesianX] 
                    y = xyz[i][info.cartesianY]
                    z = xyz[i][info.cartesianZ]
                    current = FreeCAD.Vector(x,y,z)
                    if not last:
                        last = current
                    if i==0 or (last.distanceToPoint(current) > MINDISTANCE):
                        self.pts.append(current)
                        colormap.append(i)
                        last = current
                    
            pt=Points.Points(self.pts)
            Points.show(pt)
            self.points = App.ActiveDocument.ActiveObject
            if (info.colorRed > -1):
                self.points.addProperty(
                    'App::PropertyColorList', 
                    'ColorList', 
                    'Object Style', 
                    'The color of the points.')
                colors = []
                for i in colormap:
                    r = others[i][info.colorRed] / 255
                    g = others[i][info.colorGreen] / 255
                    b = others[i][info.colorBlue] / 255
                    colors.append((r,g,b))
                self.points.ColorList = colors
                self.points.ViewObject.DisplayMode = u'Color' 

test = E57Tools(TESTFILE)
