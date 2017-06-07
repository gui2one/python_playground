#### CODE  from https://en.wikipedia.org/wiki/Linear_congruential_generator

def lcg(seed):

	modulus = 10000
	a = 2558
	c = 5000
	if seed != None:
		lcg.previous = seed

		random_number = (lcg.previous * a + c) % modulus
		lcg.previous = random_number
		return random_number

# lcg.previous = 5557

numbers = []
for i in range(5000):
	randValue = lcg((i+123)*3)/10000
	if randValue not in numbers:
		numbers.append(randValue)

print(numbers)
print (len(numbers))