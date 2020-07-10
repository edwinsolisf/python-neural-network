import random

def NumInLetters(number, englishMode = True):
    """Returns any number into its letter form"""

    num = str(number) 
    
    #list of units
    u_numbers = {"1":"one", "2":"two", "3":"three", "4":"four", "5":"five", "6":"six", "7":"seven", "8":"eight","9":"nine"}
    #list of tenths
    d_numbers = {"1":"ten", "2":"twenty", "3":"thirty", "4":"forty", "5":"fifty", "6":"sixty", "7":"seventy", "8":"eighty", "9":"ninty"}
    #list of cases 11 to 19
    t_numbers = {"1":"eleven", "2":"twelve", "3":"thirteen", "4":"fourteen", "5":"fifteen", "6":"sixteen", "7":"seventeen", "8":"eighteen", "9":"nineteen"}
    #list of size modifiers
    if(englishMode):
        powers = {3:"thousand", 6:"million", 9:"billion", 12:"trillion", 15:"quadrillion", 18:"quintillion", 21:"sixtillion", 24:"septillion", 27:"octillion", 30:"nonillion"}
    else:
        powers = {3:"thousand", 6:"million", 9:"thousand", 12:"billion", 15:"thousand", 18:"trillion", 21:"thousand", 24:"quadrillion", 27:"thousand", 30:"quintillion"}


    length = num.__len__()
    index = 0
    answer = ""
    i = int(length/3) + 1
    #Test for each sets of three digits
    while(i>0):
        #if number is greater than each 1000 step (eg. 1 000, 1 000 000, 1 000 000 000, etc)
        if((length - (3*i)) > index):
            #Hundreths digit placement
            if((length - (3*i+2)) > index):
                if(num[index]!="0"):
                    answer = answer + u_numbers.get(num[index])
                    answer = answer + " hundred "
                index = index + 1
            #Tenths digit placement
            if((length - (3*i+1)) > index):
                if(num[index]!="1" and num[index]!="0"):
                    answer = answer + d_numbers.get(num[index])
                    index = index + 1
                    #Units digit placement
                    if(num[index]!="0"):
                        answer = answer + " " + u_numbers.get(num[index])
                        index = index + 1
                    answer = answer + " " + powers.get(3*i) + " "  # <-------- Add modifier for the powers
                #Special case for digits from 10 to 19
                else:
                    if(num[index]!="0"):
                        index = index + 1
                        if(num[index]!="0"):
                            answer = answer + t_numbers.get(num[index])
                        else:
                            answer = answer + d_numbers.get("1")
                        answer = answer + " " + powers.get(3*i) + " " # <-------- Add modifier for the powers
                        index +=1
            else:
                answer = answer + u_numbers.get(num[index]) + " " + powers.get(3*i) + " " # <-------- Add modifier for the powers
                index = index + 1
        i = i - 1
    #For the final hundreds
    if((length - 2) > index):
            if(num[index]!="0"):
                answer = answer + u_numbers.get(num[index])
                answer = answer + " hundred "
            index = index + 1

    #For the final tenths
    if((length - 1) > index):
            if(num[index]!="1" and num[index]!="0"):
                answer = answer + d_numbers.get(num[index])
                index = index + 1
                if(num[index]!="0"):
                    answer = answer + " " + u_numbers.get(num[index])
                    index +=1

            else:
                if(num[index]!="0"):
                    index = index + 1
                    if(num[index]!="0"):
                        answer = answer + t_numbers.get(num[index])
                    else:
                        answer = answer + d_numbers.get("1")
                    index = index + 1

    return answer

def CollatzConjecture(input, doPrint = True):
    """Prints Collatz Analisis for the number"""
    if(doPrint):
        print(input)

    if(input % 2 == 1):
        if(input != 1):
            return CollatzConjecture(3 * input + 1)
        else:
            return 1
    else:
        return CollatzConjecture(int(input / 2))

def MergeSort(array):
    length = array.__len__()
    array1 = []
    array2 = []

    #Test for array of size 1
    if(length < 2):
        return array
    else:
        #Divide the array in half
        array1 = ArrayCopy(array, 0, int(length/2)-1)
        array2 = ArrayCopy(array, int(length/2), length - 1)
        
        #Sort those arrays
        array1 = MergeSort(array1)
        array2 = MergeSort(array2)

        #Merge them back 
        array = MergeArrays(array1, array2)

        return array

def MergeArrays(array1, array2):
    
    """Sorts arrays in ascending order"""
    length_1 = array1.__len__()
    pos_1 = 0
    length_2 = array2.__len__()
    pos_2 = 0
    total_length = length_1 + length_2
    new_array = []

    #Checking the first elements of each array
    for _i in range(0, total_length):
        #if it has arrived to the end of one array
        if((pos_1 >= length_1) or (pos_2 >= length_2)):
            if(pos_1 >= length_1):
                new_array.append(array2[pos_2])
                pos_2 += 1
            elif(pos_2 >= length_2):
                new_array.append(array1[pos_1])
                pos_1 += 1
        #For all normal cases compare the elements and put them back in the array
        else:
            if(array1[pos_1] < array2[pos_2]):
                new_array.append(array1[pos_1])
                pos_1 += 1
            else:
                new_array.append(array2[pos_2])
                pos_2 += 1

    return new_array
    
def BubbleSort(array):
    """Sorts a list in ascending order"""
    length = array.__len__()
    j = 0
    for j in range(1, length):
        for i in range(0, length - j):
            if(array[i] > array[i+1]):
                temp = array[i]
                array[i] = array[i+1]
                array[i+1] = temp
    return array

        

def RandomArrayNumberList(min, max, amount):
    """Creates a list of random integers"""
    i = 0
    array = []
    while(i < amount):
        array.append(random.randint(min, max))
        i += 1

    return array

def ArrayCopy(array, start = 0, end = 1):
    new_array = []
    for i in range(start, end + 1):
        new_array.append(array[i])
    return new_array 

def FibonnacciSequence(amount):
    array = [1]
    for i in range(0, amount - 1):
        if(amount < 2):
            return array
        else:
            if(i < 1):
                array.append(1)
            else:
                array.append(array[i]+array[i-1])
    return array
