import urllib
from urllib import urlencode
import xml.dom.minidom as dom

key = 'WJM174VR6TEIZRQ'


cmd = 'getbikestations'

stationNum = 23 ### station velo rotonde
enc = urlencode({"cmd":cmd,"param[station]":'number', "param[value]":stationNum, "key":key, "version":2.0})
# print enc
url = 'http://data.keolis-rennes.com/xml/?'+enc+''

data = urllib.urlopen(url)
rotondeData = data.read()
data.close()




stationNum = 37 ## station auberge de jeunesse
enc = urlencode({"cmd":cmd,"param[station]":'number', "param[value]":stationNum, "key":key, "version":2.0})
url = 'http://data.keolis-rennes.com/xml/?'+enc+''

data = urllib.urlopen(url)
canalData =  data.read()
data.close()


rotondeXmlData =  dom.parseString(rotondeData)
print 'Rotonde / Redon'
bikesAvailable = rotondeXmlData.getElementsByTagName('bikesavailable')[0].firstChild.nodeValue
slotsAvailable = rotondeXmlData.getElementsByTagName('slotsavailable')[0].firstChild.nodeValue
print 'Velos Libres :',bikesAvailable
print 'Emplacements Libres :',slotsAvailable
print '-------------------------------\n'



xmlData =  dom.parseString(canalData)
print 'Auberge de jeunesse / Canal'
bikesAvailable = xmlData.getElementsByTagName('bikesavailable')[0].firstChild.nodeValue
slotsAvailable = xmlData.getElementsByTagName('slotsavailable')[0].firstChild.nodeValue
print 'Velos Libres :',bikesAvailable
print 'Emplacements Libres :',slotsAvailable
print '-------------------------------\n'