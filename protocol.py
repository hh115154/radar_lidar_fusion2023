# env: python3.9
# -*- coding: utf-8 -*-
__author__ = 'Yang Hongxu'
# @Time     : 2022/6/25 15:03
import math
import struct
import presentationLayer
import numpy as np

# import CppApi


AR548_Detection_AzimuthAngle_Min = -3.14
AR548_Detection_AzimuthAngle_Max = 3.14
AR548_Detection_ElevationAngle_Min = AR548_Detection_AzimuthAngle_Min
AR548_Detection_ElevationAngle_Max = AR548_Detection_AzimuthAngle_Max
AR548_Detection_Range_Min = 0
AR548_Detection_Range_Max = 300


class ARS548_Detection:
    # init with a byte[44] as dtcnBuf
    def __init__(self, dtcnBuf):
        fmtDtcn = '>2fB6fbH3BHBH'
        stDtcn = struct.Struct(fmtDtcn)
        [self.f_AzimuthAngle,
         self.f_AzimuthAngleSTD,
         self.u_InvalidFlags,
         self.f_ElevationAngle,
         self.f_ElevationAngleSTD,
         self.f_Range,
         self.f_RangeSTD,
         self.f_RangeRate,
         self.f_RangeRateSTD,
         self.s_RCS,
         self.u_MeasurementID,
         self.u_PositivePredictiveValue,
         self.u_Classification,
         self.u_MultiTargetProbability,
         self.u_ObjectID,
         self.u_AmbiguityFlag,
         self.u_SortIndex] = stDtcn.unpack(dtcnBuf)

    def getPosn(self):
        x = -self.f_Range * math.sin(self.f_AzimuthAngle)
        y = self.f_Range * math.cos(self.f_ElevationAngle)
        z = self.f_Range * math.sin(self.f_ElevationAngle)
        return (x, y, z)

    def getPointColor(self):
        xp_r = [0, AR548_Detection_AzimuthAngle_Max / 2]
        xp_g = [AR548_Detection_AzimuthAngle_Min, AR548_Detection_AzimuthAngle_Max]
        xp_b = [AR548_Detection_Range_Min, AR548_Detection_Range_Max]
        fp_r = [0, 1.0]

        color_r = np.interp(self.f_AzimuthAngle, xp_r, fp_r)
        color_g = np.interp(self.f_ElevationAngle, xp_g, fp_r)
        color_b = np.interp(self.f_Range, xp_b, fp_r)
        return color_r, color_g, color_b, 1

    def __repr__(self):
        print("f_AzimuthAngle:", self.f_AzimuthAngle)
        print("f_AzimuthAngleSTD:", self.f_AzimuthAngleSTD)
        print("u_InvalidFlags:", self.u_InvalidFlags)
        print("f_ElevationAngle:", self.f_ElevationAngle)
        print("f_ElevationAngleSTD:", self.f_ElevationAngleSTD)
        print("f_Range:", self.f_Range)
        print("f_RangeSTD:", self.f_RangeSTD)
        print("f_RangeRate:", self.f_RangeRate)
        print("f_RangeRateSTD:", self.f_RangeRateSTD)
        print("s_RCS:", self.s_RCS)
        print("u_MeasurementID:", self.u_MeasurementID)
        print("u_PositivePredictiveValue:", self.u_PositivePredictiveValue)
        print("u_Classification:", self.u_Classification)
        print("u_MultiTargetProbability:", self.u_MultiTargetProbability)
        print("u_ObjectID:", self.u_ObjectID)
        print("u_AmbiguityFlag:", self.u_AmbiguityFlag)
        print("u_SortIndex:", self.u_SortIndex)
        return "finished!"


class ARS548_DetectionList:
    def __init__(self, data_buffer):
        data_buffer1 = data_buffer[0:85]
        data_buffer2 = data_buffer[85:35200 + 85]  # 35200 = 800*352/8
        data_buffer3 = data_buffer[35285:]  # 35286 = 85 + 35200 ; 20 = 4*5

        format1 = '>Q5IBIBH12fB'
        struct1 = struct.Struct(format1)
        [self.CRC,
         self.Length,
         self.SQC,
         self.DataID,
         self.Timestamp_Nanoseconds,
         self.Timestamp_Seconds,
         self.Timestamp_SyncStatus,
         self.EventDataQualifier,
         self.ExtendedQualifier,
         self.Origin_InvalidFlags,
         self.Origin_Xpos,
         self.Origin_Xstd,
         self.Origin_Ypos,
         self.Origin_Ystd,
         self.Origin_Zpos,
         self.Origin_Zstd,
         self.Origin_Roll,
         self.Origin_Rollstd,
         self.Origin_Pitch,
         self.Origin_Pitchstd,
         self.Origin_Yaw,
         self.Origin_Yawstd,
         self.List_InvalidFlags] = struct1.unpack(data_buffer1)

        format2 = '>2fI2f'
        struct2 = struct.Struct(format2)
        [self.List_RadVelDomain_Min,
         self.List_RadVelDomain_Max,
         self.List_NumOfDetections,
         self.Aln_AzimuthCorrection,
         self.Aln_ElevationCorrection] = struct2.unpack(data_buffer3)

        # 800*detection
        self.List_Detections = []
        dtcn_len = 44
        for i in range(self.List_NumOfDetections):
            data_buf = data_buffer2[i * dtcn_len:(i + 1) * dtcn_len]
            dtctn = ARS548_Detection(data_buf)
            self.List_Detections.append(dtctn)

    def get_road_lane(self, xs, ys, zs, rcs):
        pass
        # lane = CppApi.RoadLane(xs, ys, zs, rcs,self.List_NumOfDetections)
        # return lane

    def __repr__(self):
        print('-------------start print detection list-------------------')
        print('CRC', self.CRC)
        print('Length', self.Length)
        print('SQC', self.SQC)
        print('DataID', self.DataID)
        print('Timestamp_Nanoseconds', self.Timestamp_Nanoseconds)
        print('Timestamp_Seconds', self.Timestamp_Seconds)
        print('Timestamp_SyncStatus', self.Timestamp_SyncStatus)
        print('EventDataQualifier', self.EventDataQualifier)
        print('ExtendedQualifier', self.ExtendedQualifier)
        print('Origin_InvalidFlags', self.Origin_InvalidFlags)
        print('Origin_Xpos', self.Origin_Xpos)
        print('Origin_Xstd', self.Origin_Xstd)
        print('Origin_Ypos', self.Origin_Ypos)
        print('Origin_Ystd', self.Origin_Ystd)
        print('Origin_Zpos', self.Origin_Zpos)
        print('Origin_Zstd', self.Origin_Zstd)
        print('Origin_Roll', self.Origin_Roll)
        print('Origin_Rollstd', self.Origin_Rollstd)
        print('Origin_Pitch', self.Origin_Pitch)
        print('Origin_Pitchstd', self.Origin_Pitchstd)
        print('Origin_Yaw', self.Origin_Yaw)
        print('Origin_Yawstd', self.Origin_Yawstd)
        print('List_InvalidFlags', self.List_InvalidFlags)

        for i in range(self.List_NumOfDetections):
            print(self.List_Detections[i])

        print('List_RadVelDomain_Min', self.List_RadVelDomain_Min)
        print('List_RadVelDomain_Max', self.List_RadVelDomain_Max)
        print('List_NumOfDetections', self.List_NumOfDetections)
        print('Aln_AzimuthCorrection', self.Aln_AzimuthCorrection)
        print('Aln_ElevationCorrection', self.Aln_ElevationCorrection)

        print('-----------------detection list print finished!--------------------------')
        return 'finished!'

    def getTimeStamp_s(self):
      return  self.Timestamp_Seconds + self.Timestamp_Nanoseconds/1000000000


# get index of the list max vale
def getMaxIndex(list):
    max = 0
    maxIndex = 0
    for i in range(len(list)):
        if list[i] > max:
            max = list[i]
            maxIndex = i
    return maxIndex


class ARS548_Object:
    def __init__(self, data_buffer):
        data_format = '>HIH2BHB9fB2f11B5fB5fB5fB5fB2fIB2fIB2f'
        struct_data = struct.Struct(data_format)
        [self.u_StatusSensor,
         self.u_ID,
         self.u_Age,
         self.u_StatusMeasurement,
         self.u_StatusMovement,
         self.u_Position_InvalidFlags,
         self.u_Position_Reference,
         self.u_Position_X,
         self.u_Position_X_STD,
         self.u_Position_Y,
         self.u_Position_Y_STD,
         self.u_Position_Z,
         self.u_Position_Z_STD,
         self.u_Position_CovarianceXY,
         self.u_Position_Orientation,
         self.u_Position_Orientation_STD,
         self.u_Existence_InvalidFlags,
         self.u_Existence_Probability,
         self.u_Existence_PPV,
         self.u_Classification_Car,
         self.u_Classification_Truck,
         self.u_Classification_Motorcycle,
         self.u_Classification_Bicycle,
         self.u_Classification_Pedestrian,
         self.u_Classification_Animal,
         self.u_Classification_Hazard,
         self.u_Classification_Unknown,
         self.u_Classification_Overdrivable,
         self.u_Classification_Underdrivable,
         self.u_Dynamics_AbsVel_InvalidFlags,
         self.f_Dynamics_AbsVel_X,
         self.f_Dynamics_AbsVel_X_STD,
         self.f_Dynamics_AbsVel_Y,
         self.f_Dynamics_AbsVel_Y_STD,
         self.f_Dynamics_AbsVel_CovarianceXY,
         self.u_Dynamics_RelVel_InvalidFlags,
         self.f_Dynamics_RelVel_X,
         self.f_Dynamics_RelVel_X_STD,
         self.f_Dynamics_RelVel_Y,
         self.f_Dynamics_RelVel_Y_STD,
         self.f_Dynamics_RelVel_CovarianceXY,
         self.u_Dynamics_AbsAccel_InvalidFlags,
         self.f_Dynamics_AbsAccel_X,
         self.f_Dynamics_AbsAccel_X_STD,
         self.f_Dynamics_AbsAccel_Y,
         self.f_Dynamics_AbsAccel_Y_STD,
         self.f_Dynamics_AbsAccel_CovarianceXY,
         self.u_Dynamics_RelAccel_InvalidFlags,
         self.f_Dynamics_RelAccel_X,
         self.f_Dynamics_RelAccel_X_STD,
         self.f_Dynamics_RelAccel_Y,
         self.f_Dynamics_RelAccel_Y_STD,
         self.f_Dynamics_RelAccel_CovarianceXY,
         self.u_Dynamics_Orientation_InvalidFlags,
         self.u_Dynamics_Orientation_Rate_Mean,
         self.u_Dynamics_Orientation_Rate_STD,
         self.u_Shape_Length_Status,
         self.u_Shape_Length_Edge_InvalidFlags,
         self.u_Shape_Length_Edge_Mean,
         self.u_Shape_Length_Edge_STD,
         self.u_Shape_Width_Status,
         self.u_Shape_Width_Edge_InvalidFlags,
         self.u_Shape_Width_Edge_Mean,
         self.u_Shape_Width_Edge_STD] = struct_data.unpack(data_buffer)

    def get_classic_type(self):
        types = [self.u_Classification_Car,
                 self.u_Classification_Truck,
                 self.u_Classification_Motorcycle,
                 self.u_Classification_Bicycle,
                 self.u_Classification_Pedestrian,
                 self.u_Classification_Animal,
                 self.u_Classification_Hazard,
                 self.u_Classification_Unknown,
                 self.u_Classification_Overdrivable,
                 self.u_Classification_Underdrivable]
        index = getMaxIndex(types)
        return index

    def get_object_draw_info(self):
        obj_draw_info = presentationLayer.MyCuboid(width=self.u_Shape_Width_Edge_Mean,
                                                   length=self.u_Shape_Length_Edge_Mean,
                                                   x=self.u_Position_X,
                                                   y=self.u_Position_Y,
                                                   z=self.u_Position_Z,
                                                   _type=self.get_classic_type(),
                                                   _id=self.u_ID,
                                                   _stMovement=self.u_StatusMovement,
                                                   _probability=self.u_Existence_Probability,
                                                   _absV_x=self.f_Dynamics_AbsVel_X,
                                                   _absV_y=self.f_Dynamics_AbsVel_Y)
        return obj_draw_info

    def __repr__(self):
        print('-------------start print a object-------------------')
        print('u_StatusSensor', self.u_StatusSensor)
        print('u_ID', self.u_ID)
        print('u_Age', self.u_Age)
        print('u_StatusMeasurement', self.u_StatusMeasurement)
        print('u_StatusMovement', self.u_StatusMovement)
        print('u_Position_InvalidFlags', self.u_Position_InvalidFlags)
        print('u_Position_Reference', self.u_Position_Reference)
        print('u_Position_X', self.u_Position_X)
        print('u_Position_X_STD', self.u_Position_X_STD)
        print('u_Position_Y', self.u_Position_Y)
        print('u_Position_Y_STD', self.u_Position_Y_STD)
        print('u_Position_Z', self.u_Position_Z)
        print('u_Position_Z_STD', self.u_Position_Z_STD)
        print('u_Position_CovarianceXY', self.u_Position_CovarianceXY)
        print('u_Position_Orientation', self.u_Position_Orientation)
        print('u_Position_Orientation_STD', self.u_Position_Orientation_STD)
        print('u_Existence_InvalidFlags', self.u_Existence_InvalidFlags)
        print('u_Existence_Probability', self.u_Existence_Probability)
        print('u_Existence_PPV', self.u_Existence_PPV)
        print('u_Classification_Car', self.u_Classification_Car)
        print('u_Classification_Truck', self.u_Classification_Truck)
        print('u_Classification_Motorcycle', self.u_Classification_Motorcycle)
        print('u_Classification_Bicycle', self.u_Classification_Bicycle)
        print('u_Classification_Pedestrian', self.u_Classification_Pedestrian)
        print('u_Classification_Animal', self.u_Classification_Animal)
        print('u_Classification_Hazard', self.u_Classification_Hazard)
        print('u_Classification_Unknown', self.u_Classification_Unknown)
        print('u_Classification_Overdrivable', self.u_Classification_Overdrivable)
        print('u_Classification_Underdrivable', self.u_Classification_Underdrivable)
        print('u_Dynamics_AbsVel_InvalidFlags', self.u_Dynamics_AbsVel_InvalidFlags)
        print('f_Dynamics_AbsVel_X', self.f_Dynamics_AbsVel_X)
        print('f_Dynamics_AbsVel_X_STD', self.f_Dynamics_AbsVel_X_STD)
        print('f_Dynamics_AbsVel_Y', self.f_Dynamics_AbsVel_Y)
        print('f_Dynamics_AbsVel_Y_STD', self.f_Dynamics_AbsVel_Y_STD)
        print('f_Dynamics_AbsVel_CovarianceXY', self.f_Dynamics_AbsVel_CovarianceXY)
        print('u_Dynamics_RelVel_InvalidFlags', self.u_Dynamics_RelVel_InvalidFlags)
        print('f_Dynamics_RelVel_X', self.f_Dynamics_RelVel_X)
        print('f_Dynamics_RelVel_X_STD', self.f_Dynamics_RelVel_X_STD)
        print('f_Dynamics_RelVel_Y', self.f_Dynamics_RelVel_Y)
        print('f_Dynamics_RelVel_Y_STD', self.f_Dynamics_RelVel_Y_STD)
        print('f_Dynamics_RelVel_CovarianceXY', self.f_Dynamics_RelVel_CovarianceXY)
        print('u_Dynamics_AbsAccel_InvalidFlags', self.u_Dynamics_AbsAccel_InvalidFlags)
        print('f_Dynamics_AbsAccel_X', self.f_Dynamics_AbsAccel_X)
        print('f_Dynamics_AbsAccel_X_STD', self.f_Dynamics_AbsAccel_X_STD)
        print('f_Dynamics_AbsAccel_Y', self.f_Dynamics_AbsAccel_Y)
        print('f_Dynamics_AbsAccel_Y_STD', self.f_Dynamics_AbsAccel_Y_STD)
        print('f_Dynamics_AbsAccel_CovarianceXY', self.f_Dynamics_AbsAccel_CovarianceXY)
        print('u_Dynamics_RelAccel_InvalidFlags', self.u_Dynamics_RelAccel_InvalidFlags)
        print('f_Dynamics_RelAccel_X', self.f_Dynamics_RelAccel_X)
        print('f_Dynamics_RelAccel_X_STD', self.f_Dynamics_RelAccel_X_STD)
        print('f_Dynamics_RelAccel_Y', self.f_Dynamics_RelAccel_Y)
        print('f_Dynamics_RelAccel_Y_STD', self.f_Dynamics_RelAccel_Y_STD)
        print('f_Dynamics_RelAccel_CovarianceXY', self.f_Dynamics_RelAccel_CovarianceXY)
        print('u_Dynamics_Orientation_InvalidFlags', self.u_Dynamics_Orientation_InvalidFlags)
        print('u_Dynamics_Orientation_Rate_Mean', self.u_Dynamics_Orientation_Rate_Mean)
        print('u_Dynamics_Orientation_Rate_STD', self.u_Dynamics_Orientation_Rate_STD)
        print('u_Shape_Length_Status', self.u_Shape_Length_Status)
        print('u_Shape_Length_Edge_InvalidFlags', self.u_Shape_Length_Edge_InvalidFlags)
        print('u_Shape_Length_Edge_Mean', self.u_Shape_Length_Edge_Mean)
        print('u_Shape_Length_Edge_STD', self.u_Shape_Length_Edge_STD)
        print('u_Shape_Width_Status', self.u_Shape_Width_Status)
        print('u_Shape_Width_Edge_InvalidFlags', self.u_Shape_Width_Edge_InvalidFlags)
        print('u_Shape_Width_Edge_Mean', self.u_Shape_Width_Edge_Mean)
        print('u_Shape_Width_Edge_STD', self.u_Shape_Width_Edge_STD)
        print('-------------finish print detection list-------------------')
        return "obj print finished!"


class ARS548_ObjectList:
    def __init__(self, data_buffer):
        buf1 = data_buffer[0:35]
        buf2 = data_buffer[35:]
        data_format = '>Q5IBI2B'
        struct_data = struct.Struct(data_format)
        [self.CRC,
         self.Length,
         self.SQC,
         self.DataID,
         self.Timestamp_Nanoseconds,
         self.Timestamp_Seconds,
         self.Timestamp_SyncStatus,
         self.EventDataQualifier,
         self.ExtendedQualifier,
         self.ObjectList_NumOfObjects] = struct_data.unpack(buf1)
        self.ObjectList_Objects = []
        obj_len = 187
        for i in range(self.ObjectList_NumOfObjects):
            data_buf = buf2[i * obj_len:(i + 1) * obj_len]
            obj = ARS548_Object(data_buf)
            self.ObjectList_Objects.append(obj)

    def getTimeStamp_s(self):
      return  self.Timestamp_Seconds + self.Timestamp_Nanoseconds/1000000000

    def __repr__(self):
        print('-------------start print obj list-------------------')

        print('CRC', self.CRC)
        print('Length', self.Length)
        print('SQC', self.SQC)
        print('DataID', self.DataID)
        print('Timestamp_Nanoseconds', self.Timestamp_Nanoseconds)
        print('Timestamp_Seconds', self.Timestamp_Seconds)
        print('Timestamp_SyncStatus', self.Timestamp_SyncStatus)
        print('EventDataQualifier', self.EventDataQualifier)
        print('ExtendedQualifier', self.ExtendedQualifier)
        print('ObjectList_NumOfObjects', self.ObjectList_NumOfObjects)

        for i in range(self.ObjectList_NumOfObjects):
            print(self.ObjectList_Objects[i])

        print('-------------end print obj list-------------------')
        return 'finished'
