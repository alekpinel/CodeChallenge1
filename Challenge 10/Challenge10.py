# coding=utf-8
'''
  21/12/2021
  Made by Alejandro Pinel Martínez
  Code Challenge
  Challenge 10 - Packets delivery
'''

import binascii

def processCase(case):
    case.sort(key=lambda x: (x['time']))
    word = ''
    for message, i in zip(case, range(len(case))):
        word += chr((int(message['id'], 16)))
    
    print(f'Hint: {word}')
    
    case.sort(key=lambda x: (x['seq']))
    dataHex = ''
    for message, i in zip(case, range(len(case))):
        dataHex += message['data']
    
    writeHex('secret.png', dataHex)
    
    # If we read the QR we obtain:
    print('The password is: KFXSMGTAJ9KT20')
    
    code = 'KFXSMGTAJ9KT20'
    
    return code
    
def readDataPacket(messages):
    file = open("packet.txt", "r", encoding="utf-8")

    for message in messages:
        line = file.readline()
        while ('Data (1 byte)' not in line):
            line = file.readline()
        line = file.readline()
        line = file.readline()
        message['data'] = line[6:8]
    file.close()
    
def readSeqAndIdPacket(messages):
    file = open("packet.csv", "r", encoding="utf-8")
    line = file.readline()
    for message, i in zip(messages, range(len(messages))):
        line = file.readline().replace('\"', '')
        info = line.split(',')
        extraInfo = info[6].split(' ')
        
        message['time'] = float(info[1])
        message['id'] = '0x' + info[6].split('=')[1][4:6]
        message['seq'] = int(info[7].split('=')[1].split('/')[0])
    file.close()

#Get input
def readInput():
    nMessages = 213
    messages = [{} for i in range(nMessages)]
    
    readDataPacket(messages)
    readSeqAndIdPacket(messages)
    
    return messages

def writeHex(hexFileName, hexNumbers):
    with open(hexFileName, 'wb') as f:
        f.write(binascii.unhexlify(hexNumbers))

def writeOutput(filename, output):
    f = open(filename + '.txt', "w")
    f.write(output)
    f.close()

def main():
    writeFile = True

    outputfile = "Output"

    if (not writeFile):
        outputfile = None

    inputs = readInput()
    
    output = processCase(inputs)

    writeOutput(outputfile, output)

if __name__ == "__main__":
    main()
