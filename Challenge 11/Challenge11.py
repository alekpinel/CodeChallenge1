# coding=utf-8
'''
  17/12/2021
  Made by Alejandro Pinel Martínez
  Code Challenge
  Challenge 11 - ALOT Another library of tools
'''

def commonPrefixLengh(word1, word2):
    min_lenght = min(len(word1), len(word2))
    points = 0
    for i in range(min_lenght):
        if (word1[i] == word2[i]):
            points += 1
        else:
            break
    return points

def calculateDistances(words):
    N = len(words)
    distances = []
    for i in range(N):
        distances.append(commonPrefixLengh(words[i%N], words[(i + 1)%N]))
        
    return distances

def calculateMaxScore(distances, K):
    N = len(distances)
    if (N < K):
        return 0
    
    if (N == K):
        return min(distances[:K-1])
    
    min_distance = min(distances[:-1])
    
    min_index = distances.index(min_distance)
    left = distances[:min_index + 1]
    right = distances[min_index + 1:]
    
    n_groups = N//K
    left_groups = len(left) // K
    right_groups = len(right) // K
    groups_to_fit = n_groups - left_groups - right_groups
    
    if (groups_to_fit > 1):
        raise ValueError('More than 1 group to fit')
    
    score = groups_to_fit * min_distance
    
    score += calculateMaxScore(left, K)
    score += calculateMaxScore(right, K)
    
    return score
        
def countChars(words):
    score = 0
    for word in words:
        score += len(word)
    return score
    
def processCase(case):
    N = case['N']
    K = case['K']
    words = case['words']
    words.sort()
    
    minValue = commonPrefixLengh(words[0], words[-1])
    if (minValue > 0):
        raise ValueError('CASE NOT CONTEMPLED MIN VALUE > 0')
        
    if (K == 1):
        return countChars(words)
    
    distances = calculateDistances(words)
    
    return calculateMaxScore(distances, K)


def readCase(file):
    data = file.readline().replace('\n', '').split(' ')
    N = int(data[0])
    K = int(data[1])
    words = []
    for i in range(N):
        words.append(file.readline().replace('\n', ''))
    
    case = {'N':N, 'K':K, 'words':words}
    return case

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
    for input in inputs[0:]:
        output = processCase(input)
        outputWriter(output)

if __name__ == "__main__":
    main()
