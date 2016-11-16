import math

PI = math.pi

# for item in dir(math):
# 	print item

searchSpan = 50000
bestApprox = 0.0
oldDiff = 100000000.0
for i in range(1,searchSpan):
	for j in range(1,searchSpan):
		val = float(i)/float(j)
		diff = math.fabs(PI - val)
		if diff < 0.001 and diff < oldDiff :
			bestApprox = val
			oldDiff = diff
			print i,"/",j, " = ",bestApprox, " -- PI = ", PI