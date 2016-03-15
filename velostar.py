import urllib
from urllib import urlencode
import xml.dom.minidom as dom
import sys

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

answerCode = int(stationsXmlData.getElementsByTagName('status')[0].getAttribute('code'))
answerMessage = stationsXmlData.getElementsByTagName('status')[0].getAttribute('message')

if answerCode != 0: ### 0 is code for 'OK'
	

	if answerCode == 0:
		print 'good to go !'
	elif answerCode == 1:		
		print 'unvalid data error code :', answerCode, 'Invalid key'
		sys.exit()
	elif answerCode == 2:		
		print 'unvalid data error code :', answerCode, 'Invalid version'
		sys.exit()		
	elif answerCode == 3:		
		print 'unvalid data error code :', answerCode, 'Invalid Command'
		sys.exit()	
	elif answerCode == 4:		
		print 'unvalid data error code :', answerCode, 'Empty Key'
		sys.exit()			
	elif answerCode == 5:		
		print 'unvalid data error code :', answerCode, 'Empty Version'
		sys.exit()			
	elif answerCode == 6:		
		print 'unvalid data error code :', answerCode, 'Empty Command'
		sys.exit()			
	elif answerCode == 8:		
		print 'unvalid data error code :', answerCode, 'Usage limit reached'
		sys.exit()	
	elif answerCode == 98:		
		print 'unvalid data error code :', answerCode, 'API Disabled by an administrator'
		sys.exit()	
	elif answerCode == 99:		
		print 'unvalid data error code :', answerCode, 'Maintenance'
		sys.exit()		
	elif answerCode >= 100:
		print 'unvalid data error code :', answerCode, 'Specific Command error code'
		sys.exit() 


print 'code',answerCode
print 'message :',answerMessage


for element in stationsXmlData.getElementsByTagName('number'):
	## ROTONDE
	if element.firstChild.nodeValue == '23':
		stationRotondeNode = element.parentNode

	### canal / auberge de jeunesse
	elif element.firstChild.nodeValue == '37':
		stationCanalNode = element.parentNode

states = {}

for element in stationsXmlData.getElementsByTagName('state'):
	parent = element.parentNode
	name = parent.getElementsByTagName("name")[0].firstChild.nodeValue
	state = parent.getElementsByTagName("state")[0].firstChild.nodeValue
	states[name] = state

# for item in states:
# 	print item, '--->', states[item]
	




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