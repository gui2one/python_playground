import astropy
from astropy import units as u
from astropy.coordinates import SkyCoord, CartesianRepresentation
from astropy.coordinates import Distance



csvFilePath = "F:/HOUDINI_14_playground/stars_data_base/hygdata_v3.csv"

f = open(csvFilePath, 'r')
dataLines = f.readlines()
f.close()


class myClass:
	def __init__(self, ra, dec, dist):
		# print 'myClass instance created'
		self.ra = float(ra)
		self.dec = float(dec)
		self.dist = float(dist)



print len(dataLines)

starList = []

for id, line in enumerate(dataLines):
	if id != 0 : #   and id < 500:
		values = line.split(",")
		o = myClass(values[7],values[8],values[9])
		starList.append(o)






newPoints = []

for id, star in enumerate(starList):

	if id%100 == 0 : print id
	c = SkyCoord(ra = star.ra * u.degree, dec = star.dec * u.degree, distance = star.dist * u.kpc )
	c.representation = CartesianRepresentation
	#spherical =  astropy.coordinates.cartesian_to_spherical(c.cartesian.x, c.cartesian.y, c.cartesian.z)

	#print (c.x.value)
	newPoints.append((c.cartesian.x, c.cartesian.y, c.cartesian.z))
	# newPoints.append((float(spherical[1].value), float(spherical[2].value)))


# print float(newPoints[50][0])

outF = open("3d_coords.csv","w")

for id, point in enumerate(newPoints):
	outF.write("%f,%f,%f\n" % (point[0].value, point[1].value, point[2].value))
outF.close()

# for line in dataLines:
