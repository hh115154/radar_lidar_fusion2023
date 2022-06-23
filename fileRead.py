import protocol
import pandas as pd
import math


folderPath = 'C:\\Users\\yangh\\Desktop\\csvLogFile'


fileName = "Record_2022-06-23_17-14-36.someip.ars540.hex"
lineNr = 0
with open(fileName, 'r') as f:
	for line in f:
		bytes_data = bytes.fromhex(line)
		linelen = len(bytes_data)
		if linelen >10000:
			# pass
			# bufLen = linelen - 31
			buf = bytes_data[16:35321] # 有效数据的位置
			dList = protocol.ARS548_DetectionList(buf)
			f_AzimuthAngle = []
			f_ElevationAngle = []
			f_Range = []
			f_RangeRate = []
			s_RCS = []
			u_PositivePredictiveValue = []
			u_Classification = []
			u_MeasurementID = []
			x = []
			y = []
			z = []
			for i in range(len(dList.List_Detections)):

				x.append(dList.List_Detections[i].f_Range * math.cos(dList.List_Detections[i].f_ElevationAngle))
				y.append(dList.List_Detections[i].f_Range * math.sin(-dList.List_Detections[i].f_AzimuthAngle))
				z.append(dList.List_Detections[i].f_Range * math.sin(dList.List_Detections[i].f_ElevationAngle))

				# f_AzimuthAngle.append(dList.List_Detections[i].f_AzimuthAngle)
				# f_ElevationAngle.append(dList.List_Detections[i].f_ElevationAngle)
				# f_Range.append(dList.List_Detections[i].f_Range)
				# f_RangeRate.append(dList.List_Detections[i].f_RangeRate)
				s_RCS.append(dList.List_Detections[i].s_RCS)
				# u_PositivePredictiveValue.append(dList.List_Detections[i].u_PositivePredictiveValue)
				# u_Classification.append(dList.List_Detections[i].u_Classification)
				# u_MeasurementID.append(dList.List_Detections[i].u_MeasurementID)

			dataFram = pd.DataFrame({'x':x,
									 'y':y,
									 'z':z,
									 's_RCS':s_RCS})


			# dataFram = pd.DataFrame({'AzimuthAngle':f_AzimuthAngle,
			# 						 'ElevationAngle':f_ElevationAngle,
			# 						 'Range':f_Range,
			# 						 'RangeRate':f_RangeRate,
			# 						 'RCS':s_RCS,
			# 						 'PositivePredictiveValue':u_PositivePredictiveValue,
			# 						 'Classification':u_Classification,
			# 						 'u_MeasurementID':u_MeasurementID})
			csvfilename =folderPath +"\pclData"+str(lineNr)+".csv"
			dataFram.to_csv(csvfilename, index=False, sep=',')

			lineNr += 1
			# print(dList.Timestamp_Nanoseconds/1000000000+dList.Timestamp_Seconds)
		else:
			pass
			# buf = bytes_data[16:9385+16]
			# oList = protocol.ARS548_ObjectList(buf)
			#
			# u_ID = []
			# u_Position_X= []
			# u_Position_Y= []
			# u_Position_Z= []
			# u_Classification_Car= []
			# u_Classification_Truck= []
			# u_Classification_Motorcycle= []
			# u_Classification_Bicycle= []
			# u_Classification_Pedestrian= []
			# u_Classification_Animal= []
			# u_Classification_Overdrivable= []
			# u_Classification_Underdrivable= []
			# f_Dynamics_RelVel_X= []
			# f_Dynamics_RelVel_Y= []
			# u_Shape_Length_Status= []
			# u_Shape_Length_Edge_Mean= []
			# u_Shape_Width_Status= []
			# u_Shape_Width_Edge_Mean= []
			# u_Position_Orientation= []
			u_Existence_Probability= []
			# for i in range(oList.ObjectList_Objects.__len__()):
			# 	u_ID.append(oList.ObjectList_Objects[i].u_ID)
			# 	u_Position_X.append(oList.ObjectList_Objects[i].u_Position_X)
			# 	u_Position_Y.append(oList.ObjectList_Objects[i].u_Position_Y)
			# 	u_Position_Z.append(oList.ObjectList_Objects[i].u_Position_Z)
			# 	u_Classification_Car.append(oList.ObjectList_Objects[i].u_Classification_Car)
			# 	u_Classification_Truck.append(oList.ObjectList_Objects[i].u_Classification_Truck)
			# 	u_Classification_Motorcycle.append(oList.ObjectList_Objects[i].u_Classification_Motorcycle)
			# 	u_Classification_Bicycle.append(oList.ObjectList_Objects[i].u_Classification_Bicycle)
			# 	u_Classification_Pedestrian.append(oList.ObjectList_Objects[i].u_Classification_Pedestrian)
			# 	u_Classification_Animal.append(oList.ObjectList_Objects[i].u_Classification_Animal)
			# 	u_Classification_Overdrivable.append(oList.ObjectList_Objects[i].u_Classification_Overdrivable)
			# 	u_Classification_Underdrivable.append(oList.ObjectList_Objects[i].u_Classification_Underdrivable)
			# 	f_Dynamics_RelVel_X.append(oList.ObjectList_Objects[i].f_Dynamics_RelVel_X)
			# 	f_Dynamics_RelVel_Y.append(oList.ObjectList_Objects[i].f_Dynamics_RelVel_Y)
			# 	u_Shape_Length_Status.append(oList.ObjectList_Objects[i].u_Shape_Length_Status)
			# 	u_Shape_Length_Edge_Mean.append(oList.ObjectList_Objects[i].u_Shape_Length_Edge_Mean)
			# 	u_Shape_Width_Status.append(oList.ObjectList_Objects[i].u_Shape_Width_Status)
			# 	u_Shape_Width_Edge_Mean.append(oList.ObjectList_Objects[i].u_Shape_Width_Edge_Mean)
			# 	u_Position_Orientation.append(oList.ObjectList_Objects[i].u_Position_Orientation)
			# 	u_Existence_Probability.append(oList.ObjectList_Objects[i].u_Existence_Probability)
			#
			# dataFram = pd.DataFrame({
				# 'ID':u_ID,
				# 					 'Position_X':u_Position_X,
				# 					 'Position_Y':u_Position_Y,
				# 					 'Position_Z':u_Position_Z,
			# 						 'Classification_Car':u_Classification_Car,
			# 						 'Classification_Truck':u_Classification_Truck,
			# 						 'Classification_Motorcycle':u_Classification_Motorcycle,
			# 						 'Classification_Bicycle':u_Classification_Bicycle,
			# 						 'Classification_Pedestrian':u_Classification_Pedestrian,
			# 						 'Classification_Animal':u_Classification_Animal,
			# 						 'Classification_Overdrivable':u_Classification_Overdrivable,
			# 						 'Classification_Underdrivable':u_Classification_Underdrivable,
			# 						 'Dynamics_RelVel_X':f_Dynamics_RelVel_X,
			# 						 'Dynamics_RelVel_Y':f_Dynamics_RelVel_Y,
			# 						 'Shape_Length_Status':u_Shape_Length_Status,
			# 						 'Shape_Length_Edge_Mean':u_Shape_Length_Edge_Mean,
			# 						 'Shape_Width_Status':u_Shape_Width_Status,
			# 						 'Shape_Width_Edge_Mean':u_Shape_Width_Edge_Mean,
			# 						 'Position_Orientation':u_Position_Orientation,
			# 						 'Existence_Probability':u_Existence_Probability})
			#
			# csvfilename ="objData"+str(lineNr)+".csv"
			# dataFram.to_csv(csvfilename, index=False, sep=',')
			#
			# lineNr += 1

			# print(oList.Timestamp_Nanoseconds/1000000000+oList.Timestamp_Seconds)



print(lineNr)