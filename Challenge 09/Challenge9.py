# coding=utf-8
'''
  15/12/2021
  Made by Alejandro Pinel Martínez
  Code Challenge
  Challenge 9 - Collisions
'''

SPRITE_TEMPLATES = []
SPRITE_SIZE = []
SPRITE_POINTS = []

def spriteSize(spriteIndex):
    height = len(SPRITE_TEMPLATES[spriteIndex])
    width = len(SPRITE_TEMPLATES[spriteIndex][0])
    return height, width

def checkCollisions(sprite1, sprite2):
    height1, width1 = spriteSize(sprite1[0])
    height2, width2 = spriteSize(sprite2[0])
    
    if (height1 * width1 > height2 * width2):
        sprite1, sprite2 = sprite2, sprite1
        height1, height2 = height2, height1
        width1, width2 = width2, width1
    
    offset_x = sprite1[1] - sprite2[1]
    offset_y = sprite1[2] - sprite2[2]
    
    # printSprite(SPRITE_TEMPLATES[sprite1[0]])
    # printSprite(SPRITE_TEMPLATES[sprite2[0]])
    # print(f"sprite [{sprite1}, {sprite2}]")
    # print(f"size1 ({height1}, {width1})")
    # print(f"size2 ({height2}, {width2})")
    # print(f"offset ({offset_x}, {offset_y})")
    
    for i_1 in range(height1):
        i_2 = i_1 + offset_x
        
        if (i_2 >= 0 and i_2 < height2):
            
            for j_1 in range(width1):
                j_2 = j_1 + offset_y
                
                if (j_2 >= 0 and j_2 < width2):
                    # print(f"({i_1}, {j_1}) {SPRITE_TEMPLATES[sprite1[0]][i_1][j_1]} ({i_2}, {j_2}) {SPRITE_TEMPLATES[sprite2[0]][i_2][j_2]}")
                    
                    
                    if (SPRITE_TEMPLATES[sprite1[0]][i_1][j_1] == '1' and SPRITE_TEMPLATES[sprite2[0]][i_2][j_2] == '1'):
                        return True
    return False

def checkCollisionsPoints(sprite1, sprite2):
    if (len(SPRITE_POINTS[sprite1[0]]) > len(SPRITE_POINTS[sprite2[0]])):
        sprite1, sprite2 = sprite2, sprite1
        
    offset_x = sprite1[1] - sprite2[1]
    offset_y = sprite1[2] - sprite2[2]
    
    height2, width2 = spriteSize(sprite2[0])
    
    for point1 in SPRITE_POINTS[sprite1[0]]:
        point2 = (point1[0] + offset_x, point1[1] + offset_y)
        if (point2[0] >= 0 and point2[0] < height2 and point2[1] >= 0 and point2[1] < width2):
            if (SPRITE_TEMPLATES[sprite2[0]][point2[0]][point2[1]] == '1'):
                return True
    
    return False

def printSprite(sprite):
    for i in range(len(sprite)):
        print (sprite[i])
        
def checkCollisionsRectangle(sprite1, sprite2):
    min_1 = (sprite1[1], sprite1[2])
    max_1 = (sprite1[1] + SPRITE_SIZE[sprite1[0]][0], sprite1[2] + SPRITE_SIZE[sprite1[0]][1])
    
    min_2 = (sprite2[1], sprite2[2])
    max_2 = (sprite2[1] + SPRITE_SIZE[sprite2[0]][0], sprite2[2] + SPRITE_SIZE[sprite2[0]][1])
    
    return not (max_1[0] < min_2[0] or min_1[0] > max_2[0] or max_1[1] < min_2[1] or min_1[1] > max_2[1])

def naiveAlgorithm(sprites):
    # for sprite in SPRITE_TEMPLATES:
    #     printSprite(sprite)
    
    collisions = 0
    for i in range(len(sprites)):
        for j in range(i + 1, len(sprites)):
            # print(f'checking {i}-{j}')
            if (checkCollisions(sprites[i], sprites[j])):
                collisions += 1
                # print(f'COLLISION {i}-{j}')
               
    return collisions

def lessNaiveAlgorithm(sprites):
    # for sprite in SPRITE_TEMPLATES:
    #     printSprite(sprite)
    
    collisions = 0
    for i in range(len(sprites)):
        min_x = sprites[i][1]
        min_y = sprites[i][2]
        max_x = min_x + SPRITE_SIZE[sprites[i][0]][0]
        max_y = min_y + SPRITE_SIZE[sprites[i][0]][1]
        for j in range(i + 1, len(sprites)):
            if (checkCollisionsRectangle(sprites[i], sprites[j])):
                # print(f'checking {i}-{j}')
                if (checkCollisionsPoints(sprites[i], sprites[j])):
                    collisions += 1
                    # print(f'COLLISION {i}-{j}')
               
    return collisions

def tableAlgorithm(sprites):
    # min_x = float("Inf")
    # min_y = float("Inf")
    # max_x = float("-Inf")
    # max_y = float("-Inf")
    # for sprite in sprites:
    #     min_x = min(min_x, sprite[1])
    #     min_y = min(min_x, sprite[2])
    #     max_x = max(max_x, sprite[1] + SPRITE_SIZE[sprite[0]][0])
    #     max_y = max(max_y, sprite[2] + SPRITE_SIZE[sprite[0]][1])
    
    # print (f"Min ({min_x}, {min_y})")
    # print (f"Min ({max_x}, {max_y})")
    
    map = dict()
    collisions = set()
    
    for spriteIndex in range(len(sprites)):
        sprite = sprites[spriteIndex]
        height, width = SPRITE_SIZE[sprite[0]]
        for i in range(height):
            for j in range(width):
                if (SPRITE_TEMPLATES[sprite[0]][i][j]  == '1'):
                    key = (i + sprite[1], j + sprite[2]) 
                    if key not in map:
                        map[key] = set()
                    for otherSprite in map[key]:
                        collisions.add((otherSprite, spriteIndex))
                    map[key].add(spriteIndex)
                
    # print(map)
    # print(collisions)
    
    return len(collisions)

def processCase(sprites):
    # print(f"N Sprites: {len(sprites)}")
    return lessNaiveAlgorithm(sprites)


def readCase(file):
    nSprites = int(file.readline())
    
    sprites = []
    for i in range(nSprites):
        line = file.readline().split(' ')
        sprites.append((int(line[0]), int(line[2]), int(line[1])))
    
    return sprites

def readSprite(file):
    dimensions = file.readline().split(' ')
    width = int(dimensions[0])
    height = int(dimensions[1])
    
    spriteTemplate = [[0 for x in range(width)] for y in range(height)]
    for i in range(height):
        line = file.readline()
        for j in range(width):
            spriteTemplate[i][j] = line[j]
    
    return spriteTemplate

#Get input
def readInput(inputfile, caseProcessor):
    f = open(inputfile + ".txt", "r", encoding="utf-8")
    
    nlines = int(f.readline())
    nSprites = int(f.readline())
    
    for i in range(nSprites):
        SPRITE_TEMPLATES.append(readSprite(f))
        SPRITE_SIZE.append((len(SPRITE_TEMPLATES[-1]), len(SPRITE_TEMPLATES[-1][0])))
    
    for spriteIndex in range(nSprites):
        sprite = SPRITE_TEMPLATES[spriteIndex]
        height, width = SPRITE_SIZE[spriteIndex]
        SPRITE_POINTS.append([])
        for i in range(height):
            for j in range(width):
                if (sprite[i][j]  == '1'):
                    pos = (i, j)
                    SPRITE_POINTS[spriteIndex].append(pos)
        # print (f'Sprite {spriteIndex}: {len(SPRITE_POINTS[spriteIndex])}')
    
    
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
    writeFile = False

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
