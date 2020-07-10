import Module1
import random
import time
import math
#num = str(input("Enter a number in digit form to transform to letter form\n"))
#print(Module1.NumInLetters(num,1))
array = Module1.RandomArrayNumberList(0,1000,100)
print(array)
print("*************************************************")
print(Module1.MergeSort(array))

Module1.CollatzConjecture(257)

for i in range(2003):
    if((2003-i)==(int(math.sqrt(2003-i))*int(math.sqrt(2003-i)))):
        print(math.sqrt(i), 2003-i)