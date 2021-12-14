# coding=utf-8
'''
  13/12/2021
  Made by Alejandro Pinel Martínez
  Code Challenge
  Challenge 5 - Invictus
'''

def getDistance(numbers):
    distance = []
    for i in range(len(numbers) - 1):
        distance.append(numbers[i + 1] - numbers[i])
    return distance

def processCase(case):
    
    words = []
    newWord = True
    for value in case:
        if (value > int(127).to_bytes(1, 'big')):
            if (newWord):
                words.append([])
                newWord = False
            words[-1].append(value)
        else:
            newWord = True
    
    # print(words)
    numbers = []
    for word in words:
        if (len(word) != 4):
            print('NO 4 BYTES ')
        
        byteConcatenate = word[0] + word[1] + word[2] + word[3]
        intWord = int.from_bytes(byteConcatenate, byteorder='big')
        numbers.append(intWord)
    
    print (f'Code Numbers: {numbers}')
    
    mandela = ['M', 'A', 'N', 'D', 'E', 'L', 'A']
    mandelaBytes = [ord(i) for i in mandela]
    mandelaDistance = getDistance(mandelaBytes)
    
    print (f'Distance of MANDELA: {getDistance(mandelaBytes)}')
    
    for i in range(len(numbers) - 1):
        eureka = True
        for j in range(len(mandelaDistance) - 1):
            difference = numbers[i + j + 1] - numbers[i + j]
            if (difference != mandelaDistance[j]):
                eureka = False
                break
            
        if (eureka):
            print('EUREKA')
            key = ord(mandela[0]) - numbers[i]
            print(f'The Key is {key}')
    
    THE_CODE = ''
    for number in numbers:
        char = chr((number + key)%192)
        THE_CODE += char
    
    return THE_CODE


def readCase(file):
    chars = []
    while 1:
      byte_s = file.read(1)
      if not byte_s:
         break
      chars.append(byte_s)
      
    return chars

#Get input
def readInput(inputfile, caseProcessor):
    f = open(inputfile + ".txt", "rb")
    nCases = 1
    lines = []
    for i in range(nCases):
        lines.append(caseProcessor(f))
    f.close()
    return lines

#Write the output
class OutputWriter:
    def __init__(self, outputfile):
        self.outputfile = None if outputfile == None else open(outputfile + ".txt", "w");
        self.i = 0

    def __del__(self):
        if (self.outputfile != None):
            self.outputfile.close()

    def __call__(self, output):
        string = output
        self.i = self.i + 1
        print(string.replace("\n", ""))
        if (self.outputfile != None):
            self.outputfile.write(string)

def main():
    writeFile = True

    inputfile = "Invictus"
    outputfile = "Output"

    if (not writeFile):
        outputfile = None

    inputs1 = readInput(inputfile, readCase)

    outputWriter = OutputWriter(outputfile)
    for input in inputs1:
        output = processCase(input)
        outputWriter(output)

if __name__ == "__main__":
    main()
