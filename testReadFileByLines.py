import protocol
import pandas as pd

csvFile = "pclData.csv"

fileName = "Record_2021-12-05_11-31-31.someip.ars540.hex"
lineNr = 0

mylines = []

file = open(fileName, "r")
while 1:
    lines = file.readlines(100000)
    if not lines:
        break
    for line in lines:
        mylines.append(line)


print(len(mylines))

ser=pd.Series(mylines)
print(mylines[0])
print(ser[0])










