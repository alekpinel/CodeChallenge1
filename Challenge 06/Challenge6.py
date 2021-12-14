# coding=utf-8
'''
  14/12/2021
  Made by Alejandro Pinel Martínez
  Code Challenge
  Challenge 6 - What day is it?
'''

translations = {
        'CA': ['dilluns', 'dimarts', 'dimecres', 'dijous', 'divendres', 'dissabte', 'diumenge'], 
        'CZ': ['pondělí', 'úterý', 'středa', 'čtvrtek', 'pátek', 'sobota', 'neděle'], 
        'DE': ['montag', 'dienstag', 'mittwoch', 'donnerstag', 'freitag', 'samstag', 'sonntag'], 
        'DK': ['mandag', 'tirsdag', 'onsdag', 'torsdag', 'fredag', 'lørdag', 'søndag'], 
        'EN': ['monday', 'tuesday', 'wednesday', 'thursday', 'friday', 'saturday', 'sunday'], 
        'ES': ['lunes', 'martes', 'miércoles', 'jueves', 'viernes', 'sábado', 'domingo'], 
        'FI': ['maanantai', 'tiistai', 'keskiviikko', 'torstai', 'perjantai', 'lauantai', 'sunnuntai'], 
        'FR': ['lundi', 'mardi', 'mercredi', 'jeudi', 'vendredi', 'samedi', 'dimanche'], 
        'IS': ['mánudagur', 'þriðjudagur', 'miðvikudagur', 'fimmtudagur', 'föstudagur', 'laugardagur', 'sunnudagur'], 
        'GR': ['δευτέρα', 'τρίτη', 'τετάρτη', 'πέμπτη', 'παρασκευή', 'σάββατο', 'κυριακή'], 
        'HU': ['hétfő', 'kedd', 'szerda', 'csütörtök', 'péntek', 'szombat', 'vasárnap'], 
        'IT': ['lunedì', 'martedì', 'mercoledì', 'giovedì', 'venerdì', 'sabato', 'domenica'], 
        'NL': ['maandag', 'dinsdag', 'woensdag', 'donderdag', 'vrijdag', 'zaterdag', 'zondag'], 
        'VI': ['thứ hai', 'thứ ba', 'thứ tư', 'thứ năm', 'thứ sáu', 'thứ bảy', 'chủ nhật'], 
        'PL': ['poniedziałek', 'wtorek', 'środa', 'czwartek', 'piątek', 'sobota', 'niedziela'], 
        'RO': ['luni', 'marţi', 'miercuri', 'joi', 'vineri', 'sâmbătă', 'duminică'], 
        'RU': ['понедельник', 'вторник', 'среда', 'четверг', 'пятница', 'суббота', 'воскресенье'], 
        'SE': ['måndag', 'tisdag', 'onsdag', 'torsdag', 'fredag', 'lördag', 'söndag'], 
        'SI': ['ponedeljek', 'torek', 'sreda', 'četrtek', 'petek', 'sobota', 'nedelja'], 
        'SK': ['pondelok', 'utorok', 'streda', 'štvrtok', 'piatok', 'sobota', 'nedeľa']
   }

wordsChecked = {}

import datetime

def dateIsCorrect(day, month, year):
    #Years
    if (year < 1970):
        raise ValueError('Year before 1970')
    
    if (month < 1 or month > 12):
        return False
    
    correctDate = None
    try:
        newDate = datetime.datetime(year, month, day)
    except ValueError:
        return False
    
    return True

def processCase(case):
    # print (case)
    language = case['Language']
    date = case['Date']
    day, month, year = date
    
    if (not language in translations):
        return 'INVALID_LANGUAGE'
    
    if (not dateIsCorrect(day, month, year)):
        return 'INVALID_DATE'
    
    weekDay = newDate = datetime.datetime(year, month, day).weekday()
    
    wordsChecked[language][weekDay] += 1
    
    return translations[language][weekDay]


def readCase(file):
    line = file.readline().replace('\n', '')
    
    language = line.split(':')[1]
    
    dateString = line.split(':')[0]
    dateList = dateString.split('-')
    
    if (dateString[2] == '-'):
        date = [int(dateList[0]),int(dateList[1]),int(dateList[2])]
    elif (dateString[4] == '-'):
        date = [int(dateList[2]),int(dateList[1]),int(dateList[0])]
    else:
        raise ValueError('Date in wrong format')

    case = {'Language':language, 'Date':date}
    return case

def getTranslationDictionary():
    f = open("translations.txt", "r", encoding="utf-8")
    line = f.readline().replace('\n', '')
    dict = {}
    while line:
        wordList = line.split(' ')
        newList = []
        for word in wordList[1:]:
            newList.append(word.replace('_', ' ').lower())
        dict[wordList[0]] = newList
        
        print (line)
        line = f.readline().replace('\n', '')
    print (dict)

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
    
    # translations = getTranslationDictionary()
    
    testType = 'submit'
    writeFile = True

    inputfile = testType + "Input"
    outputfile = testType + "Output"

    if (not writeFile):
        outputfile = None

    inputs = readInput(inputfile, readCase)
    
    # wordsChecked = {}
    for key in translations.keys():
        wordsChecked[key] = []
        for i in range(7):
            wordsChecked[key].append(0)

    outputWriter = OutputWriter(outputfile)
    for input in inputs:
        output = processCase(input)
        outputWriter(output)
    
    print (f'Words checked: {wordsChecked}')

if __name__ == "__main__":
    main()
