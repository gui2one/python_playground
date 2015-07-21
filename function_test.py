

def sqrt(x):
	ans = 0
	if x >= 0:
		while ans<x : 
			
		
			if ans*ans != x:
				print x, 'is not a perfect square'
				return None
			else: return ans

			ans = ans + 1
	else:
		print x, 'is a negative number'
		return None


print sqrt(33) 		
