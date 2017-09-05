import sys
import timeit
sys.path.append(".")


t1 = timeit.Timer("fib(31)", setup="from tools import fib")

print t1.timeit(10)

