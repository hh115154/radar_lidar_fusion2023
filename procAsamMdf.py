# env: python3.9
# -*- coding: utf-8 -*-
__author__ = 'Yang Hongxu'
# @Time     : 2022/6/25 15:03
from asammdf import MDF, Signal
import numpy as np


class MdfFile:
	def __init__(self, obj=None):
		self.timeStamp = []
		self.signals = []
		self.table = {}

	def appendNewTimeStampData(self, obj, timestamp=0.0):
		if self.table:
			pass
		else:
			print("mdf file object table is null!")
		self.timeStamp.append(timestamp)
		i = int(0)
		#struct to list
		for name, value in vars(obj).items():
			if name not in self.table.keys():
				self.table[name] = []
			self.table[name].append(value)

	def export2file(self, file_name):
		for key in self.table:
			sig = Signal(
				samples=np.array(self.table[key], type(self.table[key][0])),
				timestamps=np.array(self.timeStamp, dtype=np.float64),
				name=key,
				unit=''
			)
			self.signals.append(sig)

		with MDF(version='4.10') as mdf4:
			mdf4.append(self.signals, comment='Creat by yanghongxu')
			mdf4.save(file_name, overwrite=True)

	def import_from_file(self, file_name):
		self.__init__()
		# with MDF(name=file_name, version='4.10') as mdf:
		# 	for sig in mdf.signals:
		# 		self.table[sig.name] = sig.samples.tolist()
		# 		self.timeStamp = sig.timestamps.tolist()

	def clearSignalBuffer(self):
		self.signals.clear()

#
# class Person:
# 	def __init__(self, _name="", _age=int(0)):
# 		self.name = _name
# 		self.age = _age
# 		self.sex = 1
#
if __name__ =='__main__':
	mdf = MdfFile()
	mdf.import_from_file("1649733765.9224124.mf4")
	print(mdf.signals)
# 	a = Person(float(1.1), int(20))
# 	b = Person(float(2.2), int(30))
# 	c = Person(float(3.3), int(40))
#
# 	mySig = MdfFile(a)
# 	mySig.appendNewTimeStampData(a, 0.0)
# 	mySig.appendNewTimeStampData(b, 0.1)
# 	mySig.appendNewTimeStampData(c, 0.2)
# 	mySig.export2file('my_first_mdf_file.mf4')



