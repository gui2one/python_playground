import sys
import struct
print " read BPHYS file"
# dataFile = open('F:/HOUDINI_15_playground/blendcache_particles_cache_test/test_000000_01.bphys', 'rb')
# dataFile = open('F:/HOUDINI_15_playground/geo/blender_cache/cache_000000_01.bphys', 'rb')

try:
	dataFile = open(sys.argv[1],'rb')
except:
	print 'needs a bphys file as first argument'
	sys.exit(0)

stringHeader = struct.unpack('8c',dataFile.read(8)) ### B,P,H,Y,S,I,C,S

dataType = struct.unpack('III',dataFile.read(12))

nParticles = dataType[1]
print(stringHeader, dataType[0], nParticles, "dataType[2] -->", dataType[2])

inc = 0
if dataType[2] == 64:
	
	for i in range(nParticles):
		try:
			lifeList = struct.unpack('fff',dataFile.read(12))
			print(lifeList)
			inc += 1
		except:

			print 'file finished ?!!!'
			print inc, " ENTRIES IN FILE"
			sys.exit(0)

		## outputs life range of every particles in the sim ( birth, death, lifetime)


elif dataType[2] == 31:

	for i in range(nParticles):
		##ID
		readId = struct.unpack('I',dataFile.read(4))[0]
		readPosition = struct.unpack('fff', dataFile.read(12))
		readRotation = struct.unpack('ffff', dataFile.read(16))
		readAvelocity = struct.unpack('fff', dataFile.read(12))
		readVelocity = struct.unpack('fff', dataFile.read(12))

		print 'readId -->' , readId
		print 'readPosition -->' , readPosition
		print 'readAvelocity -->' , readAvelocity
		print 'readVelocity -->' , readVelocity
		print '------------------------------------------------\n\n'


dataFile.close()


print "sys.argv[1]--- >", sys.argv[1]



