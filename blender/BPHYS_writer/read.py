import struct


print " read BPHYS file"



dataFile = open('F:/BLENDER_playground/blendcache_load_cache/cache_000003_08.bphys', 'rb')


unpacked = struct.unpack('cccccccc',dataFile.read(8)) ### B,P,H,Y,S,I,C,S

dataType = struct.unpack('III',dataFile.read(12))

print(unpacked, dataType)

inc = 0
while True:

	# print inc, "--->",(struct.unpack('8I', dataFile.read(32)))
	pIndex = struct.unpack('I',dataFile.read(4))
	print inc," index -->", pIndex	
	if pIndex == '':
		break	

	pLocation = struct.unpack('fff',dataFile.read(4*3))
	# print "pLocation -->", pLocation

	pVelocity = struct.unpack('fff',dataFile.read(4*3))
	# print "pVelocity -->", pVelocity

	pRotation = struct.unpack('ffff',dataFile.read(4*4))
	# print "pRotation -->", pRotation

	pAvelocity = struct.unpack('fff',dataFile.read(4*3))
	# print "pAvelocity -->", pAvelocity

	pSize = struct.unpack('f',dataFile.read(struct.calcsize('f')))
	# print "pSize -->", pSize

	pTimes = struct.unpack('fff',dataFile.read(4*3))
	# print "pTimes -->", pTimes

	# pBoids = struct.unpack('ffffhh',dataFile.read(4*5))
	dataFile.read(40)

	inc += 1
	


'''
times
pSize
Avelocity
pRotation
velocity
location
'''


	
	
	
	
	
	


	# print struct.unpack('f', f.read(4))


f.close()
