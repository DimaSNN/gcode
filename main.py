#!/usr/bin/python

import re
import sys



#constants
workSpeed = 'F396.000'
fastSpeed = 'F900.000'
workCode = 'M05'
stopWorkCode = 'M03'
stopCode = 'M00'


#Удалить из строк "A38.21071" и вставить "F396.000", где уже есть "F396.000" нужно только удалить "A38.21071"
def Condition1(inputLines):
    i = 0
    while i < len(inputLines):
        inputLines[i] = re.sub(r' A\d{1,3}\.\d{5}', '', inputLines[i])
        #print(inputLines[i])
        i += 1

    return inputLines


## Вставка М05 и М03
def Condition2(inputLines):
    currSpeed = None
    i = 0
    while i < len(inputLines):
        res = re.search(f"{fastSpeed}|{workSpeed}", inputLines[i])
        if res:
            # print(f"Было {inputLines[i]}")
            newSpeed = res.group(0)
            # если переход workSpeed -> fastSpeed
            if currSpeed == workSpeed and newSpeed == fastSpeed:
                inputLines.insert(i, workCode)
                # print(f"\tСтало {inputLines[i]}")
                # print(f"\tСтало {inputLines[i+1]}")
                i += 1

            # если переход fastSpeed -> workSpeed
            if currSpeed == fastSpeed and newSpeed == workSpeed:
                s = inputLines[i]
                inputLines[i] = s[:res.start()] + f"{stopWorkCode} " + s[res.start():]
                # print(f"\tСтало {inputLines[i]}")
            
            currSpeed = newSpeed

        i += 1

    return inputLines

## Вставка M00
def Condition3(inputLines):
    i = 0
    while i < len(inputLines):
        res = re.search("Z", inputLines[i])
        if res:
            inputLines.insert(i, stopCode)
            i +=1
        
        i += 1

    return inputLines

def main():
    print ("Start program")
    # print command line arguments
    print ('Number of arguments:', len(sys.argv), 'arguments.')
    print ('Argument List:', str(sys.argv))

    #default filenames
    inputFilename = "input.txt"
    outputFilename = "out.txt"
    if len(sys.argv) == 3:
        inputFilename = str(sys.argv[1])
        outputFilename = str(sys.argv[2])

    #Read input file
    lines = []
    f = open(inputFilename, 'r')
    lines = f.read().splitlines()
    f.close()

    print(str(len(lines)) + " lines were read!")
    if len(lines) == 0:
        print("file was not read!")
        exit(1)

    #print(lines[0])

    lines = Condition1(lines)
    lines = Condition2(lines)
    lines = Condition3(lines)


    #debug print
    # for el in lines:
    #     print(el)

    f = open(outputFilename, 'w')
    for el in lines:
        f.write(el + '\n')
    f.close()
    print(str(len(lines)) + " lines were written!")


#chouse main function
if __name__ == "__main__":
    main()
