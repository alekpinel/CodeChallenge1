# coding=utf-8
'''
  13/12/2021
  Made by Alejandro Pinel Martínez
  Code Challenge
  Challenge 2 - Catch them all
'''

def processCase(case):
    # print (case)
    pokemons = case['Pokemons']
    map = case['Map']

    pokemonsToDuplicate = [i for i in pokemons]
    for pokemon in pokemonsToDuplicate:
        pokemons.append(pokemon[::-1])

    while len(pokemons) > 0:
        pokemonsToSearch = [i for i in pokemons]
        for pokemon in pokemonsToSearch:
            if (pokemon in map):
                # print (pokemon + ' is in ' + map)
                map = map.replace(pokemon, '')
                pokemons.remove(pokemon)
                pokemons.remove(pokemon[::-1])
                # print ('Nuevo map ' + map)
    return map

def readCase(file):
    P, R, C = [int(i) for i in file.readline().split(" ")]
    pokemons = []
    for i in range(P):
        pokemons.append(file.readline().replace('\n', ''))

    map = ''
    for i in range(R):
        for char in file.readline().replace('\n', '').split(" "):
            map = map + char

    case = {'Pokemons':pokemons, 'Map':map}

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
    isSubmit = True
    writeFile = True

    if (isSubmit):
        inputfile = "submitInput"
        outputfile = "submitOutput"
    else:
        inputfile = "testInput"
        outputfile = "testOutput"

    if (not writeFile):
        outputfile = None

    inputs = readInput(inputfile, readCase)

    outputWriter = OutputWriter(outputfile)
    for input in inputs:
        output = processCase(input)
        outputWriter(output)

if __name__ == "__main__":
    main();
