# coding=utf-8
'''
  30/05/2022
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

# It was gzip, so I knew how to read it. I extract the content using gzip library

# Then, I have to examinate the file. It contains a fragment from 'Lord of the Rings'
# But if we look closely enough, we can see some strange symbols
# [b'\xe2\x80\x8b', b'\xe2\x80\x8c', b'\xe2\x80\x99']
# The two firsts are blank spaces and the last one is a quote

# I didn't know how to continue from here, so I have to wait until the contest was over
# and I read the solutions from https://rsilnav.github.io/posts/challenge-13/. Credits to Rafael Sillero!

# With that info, we can go to https://330k.github.io/misc_tools/unicode_steganography.html and copy and paste
# the fragment with the special character in the 'Binary in Text Steganography Sample' and 
# We should select only the characters U+200B and U+200C
# We can download the hidden data and if we read it as a text file we have 424815162342666. Nice!

import binascii
import gzip
import re

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
    writeHex(newFile + '.txt.gz', hexNumbers)

#################### EXTRACTING THE FILE ####################

def readGzip(gzipfilename):
    with gzip.open(gzipfilename, 'rb') as f:
        file_content = f.read()
        # print(file_content)
        print(file_content.decode("utf-8") )
    return file_content

def extractFile(gzip_filename, text_filename):
    bytes = readGzip(gzip_filename)
    f = open(text_filename, "wb")
    f.write(bytes)
    f.close()
    string_file = bytes.decode("utf-8")
    return string_file

#################### EXAMINATE BYTES ####################

def analyzeBytes(filename):
    with open(filename, 'rb') as f:
        file_content = f.read()
    
    words = b''
    unique_words = []
    new_word = None
    for i in range(len(file_content)):
        value = file_content[i:i+1]
        if (value > int(127).to_bytes(1, 'big')):
            if (new_word == None):
                new_word = file_content[i:i+1]
            else:
                new_word += file_content[i:i+1]
        else:
            if (new_word is not None):
                if (new_word not in unique_words):
                    unique_words.append(new_word)
                words += new_word
                new_word = None
    print('Unique symbols')
    print(unique_words)

def main():
    inputfile = "here-is-the-position"
    newFile_gzip = "originalFile.txt.gz"
    newFile_txt = "originalFile.txt"
    
    # Recreate the original file
    recreateOriginalFile(inputfile, newFile_gzip)
    # Extract the file of the gzip
    extractFile(newFile_gzip, newFile_txt)
    # Check the special characters
    analyzeBytes(newFile_txt)


if __name__ == "__main__":
    main()
