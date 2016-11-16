# clean "cow.csv" file
import csv


csvFile = open("cow.csv","r")


csvString = csvFile.read()




dialect = csv.Sniffer().sniff(csvString)
reader = csv.reader(csvFile,dialect)
csvFile.seek(0)


bigList = list(reader)



csvFile.close()
headers = bigList[0]

for i,item in enumerate(headers):
	print i," ---> ",item
prevInitials = ""
for i,line in enumerate(bigList):
	if i != 0 :
		initials = line[0]
		# print len(line)
		if initials != prevInitials:
			# print initials
			
			# print "new country : ", initials
			
			# print "\t coordinates : ", line[9]
			# print "\t elevation : ", line[11]
			# print "\t elevation low : ", line[12]
			# print "\t forest (%) : ", line[20]
			# print "\t population : ", line[29]
			# print "\t urban population : ", line[30]

			print "----------------------------------"
			print "new country : ", initials
			print "English name : ",bigList[i+1][70]
			# print "French name : ",bigList[i+4][71]
			print "----------------------------------"

			# if(initials == 'PS'):
			# 	print "found you !"
			# 	print "English name : ",bigList[i+1][70]
			# 	break
		prevInitials = initials
		# print initials