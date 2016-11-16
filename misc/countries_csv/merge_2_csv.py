import csv
import json






coordsFile = open("countries_latlon.csv","r")
coordsData = coordsFile.read()
coordsFile.close()

namesFile = open("countries_name.csv","r")
namesData = namesFile.read()
namesFile.close()

list1 = []

for i, line in enumerate(namesData.split('\n')):
	if i != 0 and len(line)> 0:
		data = {}
		lineData = line.split(",")
		# print lineData
		data["initials"] = lineData[0]
		data["english"] = lineData[1]
		data["french"] = lineData[2]
		list1.append(data)

dict2 = {}
for i, line in enumerate(coordsData.split('\n')):
	if i != 0 and len(line)> 0:
		data = {}
		lineData = line.split(",")
		# print lineData
		dict2[lineData[0]] = [lineData[1],lineData[2]]
		

outputCsvString = 'initials, english name, french name, lat, lng\n'

for country in list1:
	try:
		initials = country["initials"]
		english = country["english"]
		french = country["french"]
		coords = dict2[initials]
		# print initials, dict2[initials], english, french
		outputCsvString += "%s,%s,%s,%s,%s\n" % (initials, english, french,coords[0], coords[1])
	except: 
		print "file mismatch ... ignoring"





outputFile = open("merged_file.csv","w")

outputFile.write(outputCsvString)
outputFile.close()



