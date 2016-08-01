import numpy
import random
import math

random.seed()
total = 0.0
for i in range(10000):
	pos1 = numpy.array([random.random(), random.random()])
	pos2 = numpy.array([random.random(), random.random()])

	total += numpy.linalg.norm(pos1-pos2)

print total
print total/10000.0

