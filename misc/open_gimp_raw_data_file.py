import struct
import math

rawFilePath = 'F:/HOUDINI_15_playground/maps/custom_raw.raw'
# f = open('F:/HOUDINI_15_playground/maps/erosion/2by2.data','rb')
f = open(rawFilePath,'rb')


data = f.read()
f.close()	


dataSize = len(data)
numPixels = dataSize/3/2
dimension = math.sqrt(numPixels) 
print dataSize, numPixels, dimension

f = open(rawFilePath,'rb')

myStruct = struct.Struct('I')
for i in range(numPixels):
	data = f.read(4)
	val = myStruct.unpack(data)
	print val


f.close()	