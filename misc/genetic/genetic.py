'''
starting dataPool 
'''
import random
import time








def createPopulation(poolSize):
	dataPool = []
	for i in range(poolSize):
		random.seed()

		### creates a list of (len(targetPhrase)) length .... VERY pythonic !
		word = [None] * len(targetPhrase)


		for j in range( len(targetPhrase)):
			# word += characters[ int(math.floor(random.random()* len(characters)))]
			word[j] = characters[ random.randint(0, len(characters)-1 )]
		dataPool.append(word)
	return dataPool




def fitness(item):
	inc = 0
	# print item
	for i, char in enumerate(item):
		if char == targetPhrase[i]:
			# print targetPhrase 
			inc += 1
		#print dataPool[i], "\r",
		# time.sleep(0.01)
		
	ratio = float(inc) / len(targetPhrase)

	return ratio





def killUnfit(dataPool, killRatio):

	sortedList = sorted(dataPool, key=lambda item: fitness, reverse=True)

	truncList =  sortedList[:int(len(sortedList)/1.2)]
	return truncList




def mutate(dataPool):
	for i,item in enumerate(dataPool):

		''' choses a character in the sequence at random and replaces it by a random 
			character of the alphabet'''
		random.seed()
		randIndex = random.randint(0, len(targetPhrase)-1)
		randIndex2 = random.randint(0, len(targetPhrase)-1)
		item[randIndex] = characters[randIndex2]

	return dataPool

		

def refillPool_Asexual(dataPool):
	for i in range(poolSize - len(dataPool)):
		random.seed()

		### creates a list of (len(targetPhrase)) length .... VERY pythonic !
		word = [None] * len(targetPhrase)


		for j in range( len(targetPhrase)):
			# word += characters[ int(math.floor(random.random()* len(characters)))]
			word[j] = characters[ random.randint(0, len(characters)-1 )]
		dataPool.append(word)	

	return dataPool




def evolve(generations, dataPool):

	_dataPool = dataPool
	print 'starting with  %s' % (len(_dataPool))
	for i in range(generations):
		# print dataPool
		# print len(_dataPool)
		data1 = killUnfit(_dataPool,0.2)
		# print(len(data1))
		data2 = mutate(data1)
		# print len(_dataPool)
		# print '-----------------\n'

		data3 = refillPool_Asexual(data2)
		_dataPool = data3

		print i,'\r',
		# print dataPool
	return _dataPool

characters = [' ','a','b','c','d','e','f','g','h','i','k','l','m','n','o','p','q','r','s','t','u','v','w','x','y','z']

targetPhrase = "hello"
SEED = 100
poolSize = 10
dataPool = createPopulation(poolSize)

evolvedData = evolve(20000,dataPool)

for item in evolvedData:
	print (''.join(item))

print '-----------------\n'	