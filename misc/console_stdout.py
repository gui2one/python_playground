import sys
import time

def restart_line():
    sys.stdout.write('\r')
    sys.stdout.flush()

def drawBar(inc):
	string = ""
	for i in range(0,inc):
		string += "="

	return string

for i in range(0,51):
	# sys.stdout.write('some data')
	sys.stdout.flush()
	time.sleep(0.1) # wait 2 seconds...
	restart_line()
	outStr = 'other different data '+ str(i) 
	sys.stdout.write(str(i) + "-->" + drawBar(i))
	sys.stdout.flush()


print '\n'