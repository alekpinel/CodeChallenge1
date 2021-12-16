# coding=utf-8
'''
  16/12/2021
  Made by Alejandro Pinel Martínez
  Code Challenge
  Challenge 10 - Packets delivery
'''

def calculateChecksum(buffer):
        nleft = len(buffer)
        sum = 0
        pos = 0
        while nleft > 1:
            sum = ord(buffer[pos]) * 256 + (ord(buffer[pos + 1]) + sum)
            pos = pos + 2
            nleft = nleft - 2
        if nleft == 1:
            sum = sum + ord(buffer[pos]) * 256

        sum = (sum >> 16) + (sum & 0xFFFF)
        sum += (sum >> 16)
        sum = (~sum & 0xFFFF)

        return sum 

def processCase(case):
    # print (case)
    
    integers = []
    for hex in case:
        integers.append(int(hex, 16))
    
    # print (len(integers))
    
    chars = []
    for integer in integers:
        chars.append(chr(integer))
    
    chars = []
    for i in range(0, len(integers), 3):
        print(integers[i] + ord('R'))
        print(integers[i+1] + ord('F'))
        print(integers[i+2] + ord('C'))
        intValue = (integers[i] + integers[i+1] + integers[i+2])%255
        chars.append(chr(intValue))
    
    print(chars)
    
    # megaString = ''
    # for i in range(192):
    #     possible_word = ''
    #     for integer in integers:
    #         possible_word += chr((integer + i)%192)
    #     # print (possible_word)
    #     megaString += f'{possible_word}\n'
    
    # payload_body = '\x10'
    
    # msg_type = '\x08' # ICMP Echo Request
    # msg_code = '\x00' # must be zero
    # msg_checksum_padding = '\x00\x00' # "...with value 0 substituted for this field..."
    # rest_header = '\x00\x57\x00\x89' # from pcap
    # entire_message = msg_type + msg_code + msg_checksum_padding + rest_header + payload_body
    # entire_chk = calculateChecksum(entire_message)
    # print (entire_chk, '{:x}'.format(entire_chk), '(host byte order)')
    
    return None


def readCase(file):
    data = []
    for i in range(213):
        line = file.readline()
        while ('Data (1 byte)' not in line):
            line = file.readline()
        line = file.readline()
        line = file.readline()
        data.append(line[6:8])
    return data

#Get input
def readInput(inputfile, caseProcessor):
    f = open(inputfile + ".txt", "r", encoding="utf-8")
    nlines = 1
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
    writeFile = True

    inputfile = "packet"
    outputfile = "Output"

    if (not writeFile):
        outputfile = None

    inputs = readInput(inputfile, readCase)


    outputWriter = OutputWriter(outputfile)
    for input in inputs:
        output = processCase(input)
        outputWriter(output)

if __name__ == "__main__":
    main()
