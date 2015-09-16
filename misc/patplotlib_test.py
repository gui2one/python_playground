import random
import matplotlib.pyplot as plt
print plt


numArray = []

for i in range(50) :
	numArray.append(random.uniform(0.0,5.0))

plt.plot(numArray,'ro')
plt.plot(numArray)
plt.axis([0,50,0,10])
plt.show()