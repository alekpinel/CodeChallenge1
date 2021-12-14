# coding=utf-8
'''
  13/12/2021
  Made by Alejandro Pinel Martínez
  Code Challenge
  Challenge 4 - Let’s build musical scales
'''

scale1 = ["A", "A#", "B",  "B#", "C#", "D", "D#", "E",  "E#", "F#", "G", "G#"]
scale2 = ["A", "Bb", "Cb", "C",  "Db", "D", "Eb", "Fb", "F",  "Gb", "G", "Ab"]

def noteIsInScale(scale, note):
    return note in ''.join(scale)

def generateScale(root, steps):
    scale = [root]
    initialPos = pos = scale1.index(root) if root in scale1 else scale2.index(root)
    for step in steps:
        if (step == 'T'):
            pos += 2
        elif (step == 's'):
            pos += 1
        else:
            raise ValueError('Only T or s allowed')
        
        pos = pos % len(scale1)
        # print(pos)
        
        if (pos == initialPos):
            scale.append(root)
        elif (not noteIsInScale(scale, scale1[pos][0])):
            scale.append(scale1[pos])
        elif (not noteIsInScale(scale, scale2[pos][0])):
            scale.append(scale2[pos])
        else:
            raise ValueError('No possible note was found')

        # print(scale)
        
    scaleIsCorrect(scale)
    return ''.join(scale)

def scaleIsCorrect(scale):
    if (scale[0] != scale[-1]):
        raise ValueError('The scale should start and finish in the same note')
    
    string = ''.join(scale[1:])
    toCheck = ["A", "B", "C", "D", "E", "F", "G"]
    for char in toCheck:
        if (string.count(char) != 1):
            raise ValueError('The scale is incorrect')

def processCase(case):
    # print (case)
    root = case['Root']
    steps = case['Scale']
    
    return generateScale(root, steps)


def readCase(file):
    root = file.readline().replace('\n', '')
    scale = file.readline().replace('\n', '')

    case = {'Root':root, 'Scale':scale}
    return case

#Get input
def readInput(inputfile, caseProcessor):
    f = open(inputfile + ".txt", "r")
    nlines = int(f.readline())
    lines = []
    for i in range(nlines):
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
