import ctypes
from ctypes import*
import os

def test_dll():
    so = CDLL('./fit_1.dll')
    # so = CDLL('./Dll3.dll')

    floatArrType = ctypes.c_float*10
    resType = ctypes.c_float*6

    # x = floatArrType()
    # y = floatArrType()
    # z = floatArrType()
    # rcs = floatArrType()
    # for i in range(10):
    #     x[i] = i
    #     y[i] = i
    #     z[i] = i
    #     rcs[i] = i

    x = []
    y=[]
    z=[]
    rcs = []
    var = []


    y= [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
    x= [21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35]
    z = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    rcs = [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]


    # for i in range(10):
    #     x.append(i+1)
    #     y.append(x[i]*x[i])
    #     z.append(i)
    #     rcs.append(i)
    lent=15
    x = (ctypes.c_float*lent)(*x)
    y = (ctypes.c_float*lent)(*y)
    z = (ctypes.c_float*lent)(*z)
    rcs = (ctypes.c_float*lent)(*rcs)

    so.get_guardtral(x,y,z,rcs,lent)


    var = (ctypes.c_float*6)(*var)

    # ctypes.cast(var, ctypes.c_float).value
    # print("head")
    # print(leRes)
    # print(ctypes.cast(var, ctypes.py_object).value)
    var = resType.in_dll(so, "le_coef")
    print(var[0])
    print(var[1])
    print(var[2])
    # print("tail")

    # so.myTestI(x,y,z,rcs,10)

    # var2 = resType.in_dll(so, "ri_coef")
    # print("head")
    # print(var1[0])
    # print(var1[1])
    # print(var1[2])
    # print(var2[0])
    # print(var2[1])
    # print(var2[2])
    # print("tail")

    # dll = CDLL('./binlog.dll')

    # GENERIC_READ = 0x80000000
    # GENERIC_WRITE = 0x40000000
    # GENERIC_EXECUTE = 0x20000000
    # GENERIC_ALL = 0x10000000
    #
    #
    # pFileName = 'pyTest.blf'
    # hFile = c_void_p()
    # hFile = dll.BLCreateFile(pFileName, GENERIC_WRITE)
    #
    # print(hFile)

# def test_so():
#     so = cdll.LoadLibrary(os.getcwd() + '/libguardtral_fit.so')
#     print(so.le_coe)
#     print(so.ri_coef)
#     x = [1,2,3,4,5,6,7,8,9,10]
#     y = [1,2,3,4,5,6,7,8,9,10]
#     z = [1,2,3,4,5,6,7,8,9,10]
#     rcs = [1,2,3,4,5,6,7,8,9,10]
#     so.get_guardtral(x,y,z,rcs)
#     print(so.le_coe)
#     print(so.ri_coe)



test_dll()