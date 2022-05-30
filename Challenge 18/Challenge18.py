# coding=utf-8
'''
  19/12/2021
  Made by Alejandro Pinel Martínez
  Code Challenge
  Challenge 18 - Bit Saver
  
  This one didn't pass the submit phase
'''

import math

def sumAssignations(assigned_bits, max_bit):
    result = 0
    for bits in assigned_bits.values():
        result += 2**(max_bit-bits)
    return result

def calculateResult(program_lines, assigned_bits):
    # Calculate lenght
    total = 0
    min_lenght = float('inf')
    max_lenght = float('-inf')
    for line in program_lines:
        total += assigned_bits[line[0]] + 2
        min_lenght = min(min_lenght, assigned_bits[line[0]])
        max_lenght = max(max_lenght, assigned_bits[line[0]])
    
    diff = max_lenght - min_lenght
    return (total, diff)

def getBestResult(results):
    return min(results, key=lambda x:x[0] * 1000 + x[1])

def processCase(program_lines):
    N = len(program_lines)
    
    word_list = []
    frecuencies = {}
    for word in program_lines:
        if (word[0] not in frecuencies):
            frecuencies[word[0]] = 0
            word_list.append(word[0])
            
        frecuencies[word[0]] += 1
    word_list.sort(key = lambda x: frecuencies[x], reverse=True)
    
    max_bits = max(math.ceil(math.log(len(word_list), 2)) + 1, 1)
    results = []
    assigned_bits = {}
    capacity = 2**max_bits
    
    
    def assign(i, min_bits_to_change):
        if (i == len(word_list)):
            results.append(calculateResult(program_lines, assigned_bits))
        else:
            word = word_list[i]
            for bits in range(min_bits_to_change, max_bits + 1):
                assigned_bits[word] = bits
                current_capacity = sumAssignations(assigned_bits, max_bits)
                if (current_capacity <= capacity):
                    assign(i + 1, bits)
            
    assign(0, 1)
    total, diff = getBestResult(results)
    
    return f'{total}, {diff}'


def readCase(file):
    lines = int(file.readline())
    words = []
    for i in range(lines):
        line = file.readline().replace('\n', '').split(' ')
        words.append([line[0], line[1]])
    return words

#Get input
def readInput(inputfile, caseProcessor):
    f = open(inputfile + ".txt", "r", encoding="utf-8")
    nlines = int(f.readline())
    lines = []
    for i in range(nlines):
        lines.append(caseProcessor(f))
    f.close()
    return lines

#Write the output
class OutputWriter:
    def __init__(self, outputfile):
        self.outputfile = None if outputfile == None else open(outputfile + ".txt", "w", encoding="utf-8");
        self.i = 0
        
    def __del__(self):
        if (self.outputfile != None):
            self.outputfile.close()

    def __call__(self, output):
        string = "Case #" + str(self.i + 1) + ": " + str(output) + "\n"
        self.i = self.i + 1
        print(string.replace("\n", ""))
        if (self.outputfile != None):
            self.outputfile.write(string)

def main():
    testType = 'test'
    writeFile = True

    inputfile = testType + "Input"
    outputfile = testType + "Output"

    if (not writeFile):
        outputfile = None

    inputs = readInput(inputfile, readCase)


    outputWriter = OutputWriter(outputfile)
    for input in inputs:
        output = processCase(input)
        outputWriter(output)

if __name__ == "__main__":
    main()
