LIBRARY  = '.../liblibE57Tools.0.1.0.dylib'
TESTFILE = u'.../Downloads/bunnyDouble.e57'

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
            if count > 0:
                for i in range(count):
                    x = xyz[i][info.cartesianX] 
                    y = xyz[i][info.cartesianY]
                    z = xyz[i][info.cartesianZ]  
                    self.pts.append(FreeCAD.Vector(x,y,z))
            pt=Points.Points(self.pts)
            Points.show(pt)

test = E57Tools(TESTFILE)
