import struct


print " read BPHYS file"



f = open('F:/BLENDER_playground/blendcache_cache_test/cache_000000_00.bphys', 'rb')


unpacked = struct.unpack('cccccccc',f.read(8)) ### B,P,H,Y,S,I,C,S

dataType = struct.unpack('I',f.read(4))[0]

print(unpacked, dataType)

while True:
	pIndex = struct.unpack('I',f.read(4))
	print "index -->", pIndex	
	if pIndex == '':
		break	

	pLocation = struct.unpack('fff',f.read(4*3))
	pVelocity = struct.unpack('fff',f.read(4*3))
	pRotation = struct.unpack('ffff',f.read(4*4))
	pAvelocity = struct.unpack('fff',f.read(4*3))
	pSize = struct.unpack('f',f.read(4))
	pTimes = struct.unpack('fff',f.read(4*3))
	pBoids = struct.unpack('ffffhh',f.read(4*5))




	print "pLocation -->", pLocation
	print "pVelocity -->", pVelocity
	print "pRotation -->", pRotation
	print "pAvelocity -->", pAvelocity
	print "pSize -->", pSize
	print "pTimes -->", pTimes


	# print struct.unpack('f', f.read(4))


f.close()
