import urllib
import MercatorProjection
import time
import random
"""
start value for centerLat = 46.5 increment by 0.08 maximum

"""
centerLat = 46.36

zoom = 13
mapWidth = 640
mapHeight = 640
while centerLat > 45.0:
# while centerLat > 46.1:
	centerLon = 5.6
	while centerLon < 8.0 :
	# while centerLon < 6.0 :
		centerPoint = MercatorProjection.G_LatLng(centerLat, centerLon)
		corners = MercatorProjection.getCorners(centerPoint, zoom, mapWidth, mapHeight)
		# >>> corners
		# {"E": -65.710988,
		# "N": 74.11120692972199,
		# "S": 0.333879313530149,
		# "W": -178.210988}

		print corners
		mapURL = "http://maps.googleapis.com/maps/api/staticmap?center=%f,%f&zoom=%d&size=%dx%d&scale=2&maptype=satellite&sensor=false"%(centerLat,centerLon,zoom,mapWidth,mapHeight)
		print mapURL
		# http://maps.googleapis.com/maps/api/staticmap?center=49.141404,-121.960988&zoom=10&size=640x640&scale=2&maptype=roadmap&sensor=false"
		fileName = "captures/"+str(centerLat) + "_" + str(centerLon)
		f = open(fileName +".png","wb")
		f.write(urllib.urlopen(mapURL).read())
		f.close()

		txtFile = open(fileName + ".txt","w")
		txtFile.write(str(corners))
		txtFile.close()

		centerLon += 0.1
		print("lat : %s -- lon :%s  ---> DONE" % (centerLat, centerLon))
		randVal = random.uniform(1.0,3.0)

		print("sleeping for %3.1f minutes " % randVal )
		time.sleep(60 * randVal)

	centerLat -= 0.07