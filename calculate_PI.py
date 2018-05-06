def factorial(num):
    inc = num
    for i in range(1, num):
        inc *= num-i
        # print(inc)
    return inc

print( factorial(5))
print(5**2)
def chudnovsky(k):

    result = (factorial(6*k)) * ((545140134 * k)+ 13591409)   
    return result


print(chudnovsky(0))