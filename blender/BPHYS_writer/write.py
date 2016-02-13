import struct
import random

dataType = 1
nParticles = 100000
data = struct.pack("8c","B","P","H","Y","S","I","C","S")
data += struct.pack("III",dataType,nParticles,31)


for i in range(nParticles):
	data += struct.pack('I',i) #index


	data += struct.pack('fff',random.random(), random.random(), random.random()) #Location
	data += struct.pack('fff',random.random(), random.random(), random.random()) #Velocity
	data += struct.pack('ffff',0.0,1.0,0.0,0.5) #Rotation
	data += struct.pack('fff',10.0,0.0,5.0) #Avelocity


f = open("cache/cache_000001_00.bphys",'wb')

f.write(data)

f.close()
