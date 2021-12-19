# coding=utf-8
'''
  19/12/2021
  Made by Alejandro Pinel Martínez
  Code Challenge
  Challenge 14 - SEND + MORE = MONEY
'''

class Word:
    def __init__(self, word):
        self.word = word
        if (word.isnumeric()):
            self.isNumber = True
            self.word = int(word)
        else:
            self.isNumber = False

    def decode(self, digitMap):
        if (self.isNumber):
            return self.word
        
        N = len(self.word)
        value = 0
        factor = 1
        for i in range(N):
            value += digitMap[self.word[N - i - 1]] * factor
            factor *= 10
        return value
    
    def __str__(self):
        return self.word
    
    def getLetters(self):
        result = set()
        if (self.isNumber):
            return result
        
        for letter in self.word:
          result.add(letter)
        return result
    
    def getFirstLetters(self):
        if (self.isNumber):
            return '$'
        return set(self.word[0])
    
    def getDecodedString(self, code):
        return str(self.decode(code))
    
    def decodePartially(self, digitMap):
        if (self.isNumber):
            return self.word, self.word
        
        N = len(self.word)
        min_value = 0
        max_value = 0
        factor = 1
        for i in range(N):
            if (digitMap[self.word[N - i - 1]] != None):
                min_value += digitMap[self.word[N - i - 1]] * factor
                max_value += digitMap[self.word[N - i - 1]] * factor
            else:
                min_value += 0 * factor
                max_value += 9 * factor
                
            factor *= 10
            
        if (min_value == 0):
            min_value = 1
            
        return min_value, max_value
    
    def letterImportance(self, importantMap):
        if (self.isNumber):
            return 
        
        N = len(self.word)
        factor = 1
        for i in range(N):
            importantMap[self.word[N - i - 1]] += factor
            factor *= 10

class Operation:
    def __init__(self, left, operator, right):
        self.left = left
        self.right = right
        self.operator = operator
        
    def decode(self, digitMap):
        left_value = self.left.decode(digitMap)
        right_value = self.right.decode(digitMap)
        if (self.operator == '+'):
            return left_value + right_value
        elif (self.operator == '-'):
            return left_value - right_value
        elif (self.operator == '*'):
            return left_value * right_value
        elif (self.operator == '/'):
            return left_value / right_value
        elif (self.operator == '='):
            return left_value == right_value

    def __str__(self):
        return str(self.left) + ' ' + self.operator + ' ' + str(self.right)
    
    def getLetters(self):
        return self.left.getLetters().union(self.right.getLetters())
    
    def getFirstLetters(self):
        return self.left.getFirstLetters().union(self.right.getFirstLetters())
    
    def getDecodedString(self, code):
        return f'{self.left.getDecodedString(code)} {self.operator} {self.right.getDecodedString(code)}'

    def decodePartially(self, digitMap):
        left_values = self.left.decodePartially(digitMap)
        right_values = self.right.decodePartially(digitMap)
        
        if (left_values[0] > left_values[1]):
            raise ValueError('error')
        if (right_values[0] > right_values[1]):
            raise ValueError('error')
        
        if (self.operator == '+'):
            return left_values[0] + right_values[0], left_values[1] + right_values[1]
        elif (self.operator == '-'):
            return left_values[0] - right_values[1], left_values[1] - right_values[0]
        elif (self.operator == '*'):
            return left_values[0] * right_values[0], left_values[1] * right_values[1]
        elif (self.operator == '/'):
            return left_values[0] / right_values[1], left_values[1] / right_values[0]
        elif (self.operator == '='):
            max_min = max(left_values[0], right_values[0])
            min_max = min(left_values[1], right_values[1])
            return max_min <= min_max

    def letterImportance(self, importantMap):
        self.left.letterImportance(importantMap)
        self.right.letterImportance(importantMap)


def processCase(equation):
    letterSet = equation.getLetters()
    firstletters = equation.getFirstLetters()
    
    code = {}
    letterImportance = {}
    for letter in letterSet:
        code[letter] = None
        letterImportance[letter] = 0
    keys = list(code.keys())
    
    equation.letterImportance(letterImportance)
    
    keys.sort(key=lambda x:letterImportance[x], reverse=True)

    results = []
    
    def getPossibleRange(letter, code):
        if (letter in firstletters):
            base = list(range(1, 10))
        else:
            base = list(range(0, 10))
        
        used_values = code.values()
        return filter(lambda pos: pos not in used_values, base)
        
    def checkIfCorrect(code):
        if (equation.decode(code)):
            # print(equation.getDecodedString(code))
            results.append(equation.getDecodedString(code))

    def selectNextCombination(code, i):
        # print(f'Entering {i}: {code}')
        for pos in getPossibleRange(keys[i], code):
            code[keys[i]] = pos
            if (equation.decodePartially(code)):
                if (i + 1 == len(keys)):
                    checkIfCorrect(code)
                else:
                        selectNextCombination(code, i + 1)
        code[keys[i]] = None
    
    
    selectNextCombination(code, 0)
    
    results.sort()
    
    if (len(results) == 0):
        return 'IMPOSSIBLE'
    
    resultString = ''
    for result in results:
        resultString += result +';'
    return resultString[:-1]


def readCase(file):
    def getEquationPart(words):
        words = list(filter(None, words))
        left = Word(words[0])
        
        for op_pos in range(1, len(words), 2):
            operator = words[op_pos]
            right = Word(words[op_pos + 1])
            left = Operation(left, operator, right)
            
        return left
    
    line = file.readline().replace('\n', '').split('=')
    left = getEquationPart(line[0].split(' '))
    right = getEquationPart(line[1].split(' '))
    
    return Operation(left, '=', right)

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
        
    def close(self):
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
    outputWriter.close()

if __name__ == "__main__":
    main()
