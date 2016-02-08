

import struct
import binascii

dataType = 1

data = struct.pack("cccccccc","B","P","H","Y","S","I","C","S")
data += struct.pack("III",dataType,1,1)


data += struct.pack('I',1) #index
data += struct.pack('fff',1.0,0.0,0.0) #Location
data += struct.pack('fff',10.0,0.0,0.0) #Velocity
data += struct.pack('ffff',0.0,1.0,0.0,0.5) #Rotation
data += struct.pack('fff',10.0,0.0,5.0) #Avelocity
data += struct.pack('f',1.0) #pSize
data += struct.pack('fff',20.0,1.0,18) #pTimes
data += struct.pack('ffffhh',0.0,0.0,0.0,0.0,0.0,0.0)

f = open("cache/test_000000_00.bphys",'wb')

f.write(data)

f.close()

print data