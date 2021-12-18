# coding=utf-8
'''
  18/12/2021
  Made by Alejandro Pinel Martínez
  Code Challenge
  Challenge 8 - The crypto bubble
'''

import numpy as np
from numpy.linalg import matrix_power

def printMatrix(matrix):
    for i in matrix:
        print(i)

def extractNames(lines):
    names = {'BTC':0}
    
    def addToNames(name):
        if name not in names:
            names[name]= len(names)
    
    for line in lines:
        addToNames(line[0])
        addToNames(line[1])
        
    return names

def createMatrix(lines, names):
    N = len(names)
    matrix = np.zeros((N, N), dtype=int)
    
    for line in lines:
        matrix[names[line[1]], names[line[0]]] = max(matrix[names[line[1]], names[line[0]]], line[2])
    
    return matrix

def checkIfWinningLoop(matrices, row, column):
    mult = np.multiply(matrices[-1][row], matrices[0][:, column])
    # print(f'Revisamos con {len(matrices)}')
    # print (f'fila   : {matrices[-1][row]}')
    # print (f'column : {matrices[0][:, column]}')
    # print (f'mult   : {mult}')
    
    scores = []
    for i in range(len(mult)):
        if (mult[i] > 1):
            if (len(matrices) == 1):
                score = mult[i]
            else:
                score = checkIfWinningLoop(matrices[:-1], 0, i)
            scores.append(score)
    
    if (len(scores) > 0):
        return max(scores)
    
    return 1
    
    

def processCase(tradeLines):
    names = extractNames(tradeLines)
    matrix = createMatrix(tradeLines, names)
    N = len(names)
    
    # print(names)
    
    matrices = [matrix]
    
    if (matrix[0, 0] > 1):
        return matrix[0, 0]
    
    # print(f'Matriz original')
    # printMatrix(newmatrix)
    
    result = 1
    for i in range(2 * N):
        result = checkIfWinningLoop(matrices, 0, 0)
        
        if (result > 1):
            break
        
        # print(f'Matriz ^{i + 2}')
        newmatrix = np.matmul(matrices[-1], matrix)
        matrices.append(newmatrix)
        
        
        # printMatrix(newmatrix)
        # print(result)
        
    
    
    return result


def readCase(file):
    tradeLines = []
    n_websites = int(file.readline())
    for i in range(n_websites):
        line = file.readline().split(' ')
        website_name = line[0]
        n_trades = int(line[1])
        for j in range(n_trades):
            line = file.readline().replace('\n', '').split('-')
            tradeLines.append((line[0], line[2], int(line[1])))
    return tradeLines

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
    testType = 'submit'
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
