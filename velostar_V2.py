import urllib
from urllib import urlencode
import xml.dom.minidom as dom
import sys
import numpy as np
import time
from datetime import datetime

import json
from pprint import pprint

# testTime = time.struct_time(tm_year=2016, tm_month=3, tm_mday=15, tm_hour=17, tm_min=25,tm_sec=0, tm_wday=2, tm_yday=0,tm_isdst=1)

# # formattedTime = time.mktime(testTime)
# print formattedTime 
def infoTime(timeStamp):
	# timeStampString = '2016-03-15T17:43:09+01:00'
	timeStampString = timeStamp
	dateString = timeStampString.split('T')[0]
	timeString = timeStampString.split('T')[1]
	timeString = timeString.split('+')[0]
	timeString = timeString.split('-')[0]

	hours = int(timeString.split(':')[0])
	minutes = int(timeString.split(':')[1])
	seconds =int(timeString.split(':')[2])


	now = time.localtime(time.time())
	nowHours = now[3]
	nowMinutes = now[4]
	nowSeconds = now[5]

	minutesAgo = 0.0

	minutesAgo += (nowHours - hours)*60.0
	minutesAgo += (nowMinutes - minutes)

	stringOut = '%s minutes ago' % (minutesAgo)
	return stringOut

key = 'WJM174VR6TEIZRQ'
cmd = 'getbikestations'

stationNum = 23 ### station velo rotonde
enc = urlencode({"cmd":cmd, "key":key, "version":2.0})
# print enc
# http://data.explore.star.fr
#url = 'http://data.keolis-rennes.com/xml/?'+enc+''
url = 'http://data.explore.star.fr/api/records/1.0/search/?dataset=vls-stations-etat-tr&facet=nom&facet=etat&facet=nombreemplacementsactuels&facet=nombreemplacementsdisponibles&facet=nombrevelosdisponibles'

data = urllib.urlopen(url)



stationsData = data.read()

for entry in json.loads(stationsData) :
	pprint (entry)
data.close()

# stationsXmlData = dom.parseString(stationsData)

# answerCode = int(stationsXmlData.getElementsByTagName('status')[0].getAttribute('code'))
# answerMessage = stationsXmlData.getElementsByTagName('status')[0].getAttribute('message')

# if answerCode != 0: ### 0 is code for 'OK'
	

# 	if answerCode == 0:
# 		print 'good to go !'
# 	elif answerCode == 1:		
# 		print 'unvalid data error code :', answerCode, 'Invalid key'
# 		sys.exit()
# 	elif answerCode == 2:		
# 		print 'unvalid data error code :', answerCode, 'Invalid version'
# 		sys.exit()		
# 	elif answerCode == 3:		
# 		print 'unvalid data error code :', answerCode, 'Invalid Command'
# 		sys.exit()	
# 	elif answerCode == 4:		
# 		print 'unvalid data error code :', answerCode, 'Empty Key'
# 		sys.exit()			
# 	elif answerCode == 5:		
# 		print 'unvalid data error code :', answerCode, 'Empty Version'
# 		sys.exit()			
# 	elif answerCode == 6:		
# 		print 'unvalid data error code :', answerCode, 'Empty Command'
# 		sys.exit()			
# 	elif answerCode == 8:		
# 		print 'unvalid data error code :', answerCode, 'Usage limit reached'
# 		sys.exit()	
# 	elif answerCode == 98:		
# 		print 'unvalid data error code :', answerCode, 'API Disabled by an administrator'
# 		sys.exit()	
# 	elif answerCode == 99:		
# 		print 'unvalid data error code :', answerCode, 'Maintenance'
# 		sys.exit()		
# 	elif answerCode >= 100:
# 		print 'unvalid data error code :', answerCode, 'Specific Command error code'
# 		sys.exit() 


# print 'code',answerCode
# print 'message :',answerMessage


# for element in stationsXmlData.getElementsByTagName('number'):
# 	## ROTONDE
# 	if element.firstChild.nodeValue == '23':
# 		stationRotondeNode = element.parentNode

# 	### canal / auberge de jeunesse
# 	elif element.firstChild.nodeValue == '37':
# 		stationCanalNode = element.parentNode

# states = {}

# for element in stationsXmlData.getElementsByTagName('state'):
# 	parent = element.parentNode
# 	name = parent.getElementsByTagName("name")[0].firstChild.nodeValue
# 	state = parent.getElementsByTagName("state")[0].firstChild.nodeValue
	
# 	states[name] = state

# for item in states:
# 	print item, '--->', states[item]
	


# #rotondeLastUpdate = infoTime( stationRotondeNode.getElementsByTagName('lastupdate')[0].firstChild.nodeValue  )

# print 'Rotonde / Redon'
# print '----------------------------------'
# print 'Velos Libres : ', stationRotondeNode.getElementsByTagName('bikesavailable')[0].firstChild.nodeValue
# print 'Emplacements Disponibles :', stationRotondeNode.getElementsByTagName('slotsavailable')[0].firstChild.nodeValue
# #print rotondeLastUpdate
# print '----------------------------------\n'


# #canalLastUpdate = infoTime( stationCanalNode.getElementsByTagName('lastupdate')[0].firstChild.nodeValue  )
# print 'Canal / Auberge de Jeunesse'
# print '----------------------------------'
# print 'Velos Libres : ', stationCanalNode.getElementsByTagName('bikesavailable')[0].firstChild.nodeValue
# print 'Emplacements Disponibles :', stationCanalNode.getElementsByTagName('slotsavailable')[0].firstChild.nodeValue
# #print canalLastUpdate
# print '----------------------------------\n'