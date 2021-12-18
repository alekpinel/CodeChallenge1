# coding=utf-8
'''
  18/12/2021
  Made by Alejandro Pinel Martínez
  Code Challenge
  Challenge 13 - Find the New Earth
'''

# To download the problem file, I needed a user and password. The hint was:
# "plyba:xvyy_nyy_uhznaf"

# Searching, I found a 2003 post with the word "plyba". It was about Battlestar Galactica
# https://chile.rec.cf.narkive.com/BUlCNqn4/galactica-2003
# So I discovered that they used rot13 to avoid spoilers
# I used an online tool to decode the hint
# https://rot13.com/
# "cylon:kill_all_humans"

# That was user and password so I could download the problem file.

# The file was the output of a file analyser, so recomposed the original file.

# Then, I used an online analyser to know the extension of the file
# https://asecuritysite.com/forensics/file

# It was gzip, so I knew how to read it


import binascii
import gzip
from crc64iso.crc64iso import crc64, crc64_pair

#################### RECREATE THE FILE ####################

def readOriginalBytes(inputfile):
    hexNumbers = ''
    with open(inputfile, "r") as file:
        for i in range(39):
            line = file.readline().split(' ')
            
            for j in range(8):
                hexNumbers += line[1 + j]
    
    return hexNumbers

def writeHex(hexFileName, hexNumbers):
    with open(hexFileName, 'wb') as f:
        f.write(binascii.unhexlify(hexNumbers))

def recreateOriginalFile(inputfile, newFile):
    hexNumbers = readOriginalBytes(inputfile)
    writeHex(newFile, hexNumbers)

#################### DECODING THE FILE ####################

def readGzip(gzipfilename):
    with gzip.open(gzipfilename + '', 'rb') as f:
        file_content = f.read()
        # print(file_content)
        # print(file_content.decode("utf-8") )
    return file_content

def getCoordenates(filename):
    bytes = readGzip(filename)
    
    with open('originalFile', 'rb') as f:
        file_content = f.read()
        print(hex(binascii.crc32(file_content)))
    
    
    print(binascii.crc32(bytes))
    print(hex(binascii.crc32(bytes)))
    
    # print(crc64(bytes.decode("utf-8")))
    # print(int(crc64(bytes.decode("utf-8")), 16))
    
    # print(gzip.compress(bytes).decode("utf-8"))
    
    # print(bytes)
    
    cleanTest = b''
    
    words = []
    newWord = True
    for i in range(len(bytes)):
        # intValue = int.from_bytes(value, "big")
        value = bytes[i:i+1]
        if (value > int(127).to_bytes(1, 'big')):
            if (newWord):
                words.append(bytes[i:i+3])
                newWord = False
        else:
            newWord = True
            cleanTest += value
    
    strangeWordsCount = {}
    for word in words:
        if word not in strangeWordsCount:
            strangeWordsCount[word] = 0
        strangeWordsCount[word] += 1
    print(strangeWordsCount)
    
    
    print(len(words))
    print(words)
    badBytes = b''
    numbers = []
    hexString = ''
    for word in words:
        number = int.from_bytes(word, byteorder='big')
        numbers.append(number)
        # code += chr((number)%192)
        hexString += word.hex()
        badBytes += word
        
    
    # print(numbers)
    # print(badBytes)
    # print(gzip.compress(badBytes))
    

def main():
    inputfile = "here-is-the-position"
    newFile = "originalFile"
    
    # Recreate the original file
    recreateOriginalFile(inputfile, newFile)
    getCoordenates(newFile)


if __name__ == "__main__":
    main()
