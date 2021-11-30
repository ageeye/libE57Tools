LIBRARY  = '.../liblibE57Tools.0.1.0.dylib'
TESTFILE = u'.../Downloads/bunnyDouble.e57'

import ctypes, Points


class ToolsFileInfo(ctypes.Structure):
     _fields_ = [('channels', ctypes.c_int64),
                 ('cartesianX', ctypes.c_int64),
                 ('cartesianY', ctypes.c_int64),
                 ('cartesianZ', ctypes.c_int64),
                 ("cartesianInvalidState", ctypes.c_int64)]

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
        count = e57tools.recordCount(pname, info) 
        ok_channels = info.channels in range(3,5)
        okXYZ = info.cartesianX != info.cartesianY != info.cartesianZ
        
        # read data if all is ok
        if (count>0 & ok_channels & okXYZ):
            XYZ = ctypes.c_double * 3 * count
            ptrXYZ = ctypes.POINTER(XYZ)
            xyz = XYZ()
            STATE = ctypes.c_int64 * count
            ptrSTATE = ctypes.POINTER(STATE)
            state = STATE()

            imf = e57tools.importfile
            imf.argtypes = [ctypes.c_char_p, ptrXYZ, ptrSTATE]
            imf.restype = ctypes.c_int64

            count = e57tools.importfile(pname, xyz, state) 
            
            self.pts = []
            if count > 0:
                for i in range(count):
                    x = xyz[i][info.cartesianX] 
                    y = xyz[i][info.cartesianY]
                    z = xyz[i][info.cartesianZ]  
                    self.pts.append(FreeCAD.Vector(x,y,z))
            pt=Points.Points(self.pts)
            Points.show(pt)

test = E57Tools(TESTFILE)
