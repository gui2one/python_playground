
import struct
import binascii

dataIn = ''

for i in range(0,1000):
	values = (i*0.2,"test_sdfsdf_dsf_sdsf_sdf____aaaaaa_z")

	### get length of the string == size in bytes
	strByteSize = len(values[1]) 

	### create struct format
	s = struct.Struct('d %ss' % strByteSize)

	### pack data
	packedData = s.pack(*values)
	hexi = binascii.hexlify(packedData)
	dataIn += packedData
# print(s.unpack(hexi))

fileName = 'binary_filetest.g21'
f = open(fileName,'wb')

f.write(dataIn)

f.close()






### read data back

rFile = open(fileName,'rb')
data = rFile.read(44)
rFile.close()
print(s.unpack(data))
