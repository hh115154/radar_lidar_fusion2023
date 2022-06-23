from ctypes import *
import ctypes
import time

# RoadLaneDll = CDLL('./cppdll/fit_1.dll')
# pcl_alg_dll = CDLL('./cppdll/pcl_alg_dll.dll')

ctype_af3 = ctypes.c_float * 3



class RoadLane:
    def __init__(self, x, y, z, rcs, ptNr):
        # floatArrType = ctypes.c_float * ptNr
        x1 = (ctypes.c_float * ptNr)(*x)
        y1 = (ctypes.c_float * ptNr)(*y)
        z1 = (ctypes.c_float * ptNr)(*z)
        rcs1 = (ctypes.c_float * ptNr)(*rcs)
        t0=time.time()
        RoadLaneDll.get_guardtral(x1, y1, z1, rcs1, ptNr)
        # pcl_alg_dll.obj_track(x1, y1, z1, rcs1, ptNr)
        # obj_num_outp = ctypes.c_ubyte.in_dll(pcl_alg_dll,"obj_num_outp")
        # print("obj_num_outp:",obj_num_outp.value)
        t1=time.time()
        print("*********************time:",t1-t0)
        print(len(x),len(y),len(z),len(rcs))
        le_coef = ctype_af3.in_dll(RoadLaneDll, "le_coef")
        ri_coef = ctype_af3.in_dll(RoadLaneDll, "ri_coef")

        self.le_coef = list(le_coef)
        self.ri_coef = list(ri_coef)
        print("le_coef:",self.le_coef)
        print("ri_coef:",self.ri_coef)



class Track_Object:
    def __init__(self, _id, typ,  x, y, z, vx, vy, vz, length, width, height, movement_state):
        self.id = _id
        self.typ = typ
        self.x = x
        self.y = y
        self.z = z
        self.vx = vx
        self.vy = vy
        self.vz = vz
        self.length = length
        self.width = width
        self.height = height
        self.movement_state = movement_state

arrLen = 80
ctype_af80 = ctypes.c_float * arrLen
ctype_au8_80 = ctypes.c_ubyte * arrLen
class Track_Object_List:
    def __init__(self, f_AzimuthAngle, f_ElevationAngle, f_Range, rcs,rel_spd):
        self.ptNr = len(f_AzimuthAngle)
        self.argType = ctypes.c_float * self.ptNr
        self.speed = 0
        self.yaw_rate = 0
        self.object_list = []
        # self.x = x
        # self.y = y
        # self.z = z
        self.rel_spd = rel_spd
        self.f_AzimuthAngle=f_AzimuthAngle
        self.f_ElevationAngle=f_ElevationAngle
        self.f_Range=f_Range
        self.rcs = rcs

        f_AzimuthAngle1 = self.argType(*self.f_AzimuthAngle)
        f_ElevationAngle1 = self.argType(*self.f_ElevationAngle)
        f_Range1 = self.argType(*self.f_Range)
        rcs1 = self.argType(*self.rcs)
        rel_spd = self.argType(*self.rel_spd)

        # run function
        # print("range=",f_Range)
        # print("elevation=",f_ElevationAngle)
        # print("azimuth=",f_AzimuthAngle)
        # print("rcs=",rcs)
        # print("rel_spd=",rel_spd)


        pcl_alg_dll.obj_track(f_Range1,f_ElevationAngle1,f_AzimuthAngle1 ,rel_spd, rcs1,0,0, self.ptNr)

        # read outputs
        obj_num_outp = ctypes.c_ubyte.in_dll(pcl_alg_dll,"obj_num_outp")
        obj_id_outp = ctype_au8_80.in_dll(pcl_alg_dll,"obj_id_outp")
        obj_typ_outp = ctype_au8_80.in_dll(pcl_alg_dll,"obj_typ_outp")
        obj_px_outp = ctype_af80.in_dll(pcl_alg_dll, "obj_px_outp")
        obj_py_outp = ctype_af80.in_dll(pcl_alg_dll, "obj_py_outp")
        obj_pz_outp = ctype_af80.in_dll(pcl_alg_dll, "obj_pz_outp")
        obj_vx_outp = ctype_af80.in_dll(pcl_alg_dll, "obj_vx_outp")
        obj_vy_outp = ctype_af80.in_dll(pcl_alg_dll, "obj_vy_outp")
        obj_vz_outp = ctype_af80.in_dll(pcl_alg_dll, "obj_vz_outp")
        obj_length_outp = ctype_af80.in_dll(pcl_alg_dll, "obj_length_outp")
        obj_width_outp = ctype_af80.in_dll(pcl_alg_dll, "obj_width_outp")
        obj_height_outp = ctype_af80.in_dll(pcl_alg_dll, "obj_heigth_outp")
        obj_motion_sts = ctype_au8_80.in_dll(pcl_alg_dll, "obj_motion_sts")

        obj_id_outp = list(obj_id_outp)
        obj_typ_outp = list(obj_typ_outp)
        obj_px_outp = list(obj_px_outp)
        obj_py_outp = list(obj_py_outp)
        obj_pz_outp = list(obj_pz_outp)
        obj_vx_outp = list(obj_vx_outp)
        obj_vy_outp = list(obj_vy_outp)
        obj_vz_outp = list(obj_vz_outp)
        obj_length_outp = list(obj_length_outp)
        obj_width_outp = list(obj_width_outp)
        obj_height_outp = list(obj_height_outp)
        obj_motion_sts = list(obj_motion_sts)

        # print("obj_px_outp=",obj_px_outp)
        # print("obj_py_outp=",obj_py_outp)
        # print("obj_pz_outp=",obj_pz_outp)
        # print("obj_vx_outp=",obj_vx_outp)
        # print("obj_vy_outp=",obj_vy_outp)
        # print("obj_vz_outp=",obj_vz_outp)
        # print("obj_length_outp=",obj_length_outp)
        # print("obj_width_outp=",obj_width_outp)
        # print("obj_height_outp=",obj_height_outp)
        # print("obj_motion_sts=",obj_motion_sts)


        for j in range(obj_num_outp.value):
            obj = Track_Object(_id=obj_id_outp[j],typ= obj_typ_outp[j],
                               x=obj_px_outp[j], y=obj_py_outp[j], z=obj_pz_outp[j],
                               vx=obj_vx_outp[j], vy=obj_vy_outp[j], vz=obj_vz_outp[j],
                               length=obj_length_outp[j], width=obj_width_outp[j], height=obj_height_outp[j],
                               movement_state=obj_motion_sts[j])
            self.object_list.append(obj)



#
#
#



