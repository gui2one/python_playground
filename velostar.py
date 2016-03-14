import urllib
from urllib import urlencode
import xml.dom.minidom as dom

key = 'WJM174VR6TEIZRQ'
cmd = 'getbikestations'

stationNum = 23 ### station velo rotonde
enc = urlencode({"cmd":cmd, "key":key, "version":2.0})
# print enc
url = 'http://data.keolis-rennes.com/xml/?'+enc+''

data = urllib.urlopen(url)
stationsData = data.read()
data.close()

stationsXmlData = dom.parseString(stationsData)




for element in stationsXmlData.getElementsByTagName('number'):
	## ROTONDE
	if element.firstChild.nodeValue == '23':
		stationRotondeNode = element.parentNode

	### canal / auberge de jeunesse
	elif element.firstChild.nodeValue == '37':
		stationCanalNode = element.parentNode



print 'Rotonde / Redon'
print '----------------------------------'
print 'Velos Libres : ', stationRotondeNode.getElementsByTagName('bikesavailable')[0].firstChild.nodeValue
print 'Emplacements Disponibles :', stationRotondeNode.getElementsByTagName('slotsavailable')[0].firstChild.nodeValue
print '----------------------------------\n'

print 'Canal / Auberge de Jeunesse'
print '----------------------------------'
print 'Velos Libres : ', stationCanalNode.getElementsByTagName('bikesavailable')[0].firstChild.nodeValue
print 'Emplacements Disponibles :', stationCanalNode.getElementsByTagName('slotsavailable')[0].firstChild.nodeValue
print '----------------------------------\n'