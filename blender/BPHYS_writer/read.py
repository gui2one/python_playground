import struct
print " read BPHYS file"
dataFile = open('F:/BLENDER_playground/blendcache_load_cache/cache_000000_08.bphys', 'rb')

stringHeader = struct.unpack('cccccccc',dataFile.read(8)) ### B,P,H,Y,S,I,C,S

dataType = struct.unpack('III',dataFile.read(12))

nParticles = dataType[1]
print(stringHeader, nParticles, "dataType[2] -->", dataType[2])

inc = 0
for i in range(nParticles):

	# print inc, "--->",(struct.unpack('8I', dataFile.read(32)))
	pIndex = struct.unpack('I',dataFile.read(4))
	print(pIndex)

	pLocation = struct.unpack('fff',dataFile.read(4*3))
	print "pLocation -->", pLocation

	pVelocity = struct.unpack('fff',dataFile.read(4*3))
	print "pVelocity -->", pVelocity

	pRotation = struct.unpack('ffff',dataFile.read(4*4))
	print "pRotation -->", pRotation

	pAvelocity = struct.unpack('fff',dataFile.read(4*3))
	print "pAvelocity -->", pAvelocity


dataFile.close()
