import sys
import getopt
import ast
import json
from Algorithms import leastpotential_euandeas as lpe, nottingham_lembn as lbn
from process_data import * 
from validate_output import *

testmode = True

class TestDataObject:
    def __init__(self):
        with open('testmode_data.json') as dataFile:
            data = json.load(dataFile)
            self.requiredArgs = ast.literal_eval(data['requiredArgs'])
            self.requiredArgs[n] = int(self.requiredArgs[n])
            self.save = data['save']
            self.savePath = data['savePath']
            self.validateList = data['validateList']
            self.authorLim = int(data['authorLim'])
            self.verbose = data['verbose']
            self.showScore = data['showScore']
            self.showRawScore = data['showRawScore']

    def GetData(self):
        return self.requiredArgs, self.save, self.savePath, self.validateList, self.authorLim, self.verbose, self.showScore, self.showRawScore

def HelpText():
    print("-i              input file name and location e.g. c:/user/REF/input.csv")
    print("-n              total number of papers to be selected")
    print("-r              selection algorithm to use e.g. leastpotential_euandeas")
    print("\n==========================================================================\n")

    print("-o              save to output.csv saved in the same location as the input file.")
    print("OPTIONS:")
    print("-o [filepath]   custom filepath or filename.\n")

    print("-v              run validate_output.py on the final list to check the validity of the final list") 
    print("OPTIONS:")
    print("-v n            validate with a limit of n papers per author (default = 5)")
    print("-v true         run validate_output.py in verbose mode\n")    
    
    print("-s              show score of produced list (rounded down to the nearest 0.2)")
    print("OPTIONS:")
    print("-s raw          show the raw value of the score")

def GetFinalList(inList, n, runmode):
    if runmode == "leastpotential_euandeas":
        outList = lpe.FindPapers(inList, n)
    elif runmode == "nottingham_lembn":
        outList = lbn.FindPapers(inList, n)

    return outList

def Finalise():
    if save == True:
        SavePaperList(outList, savePath)

    if validateList == True:
        Validate(inList, outList, authorLim, verbose)

    if showScore == True:
        print(f"\nScore: {RoundScore(FindScore(outList))}")
    elif showRawScore == True:
        print(f"\nScore: {FindScore(outList)}")

if __name__ == "__main__":
    argv = sys.argv[1:]
    try:
        infile = "infile (-i)"
        n = "number of papers (-n)"
        runmode = "runmode(-r)"
        requiredArgs = {infile: None, n: None, runmode: None}

        save = False
        savePath = "output.csv"
        validateList = False
        authorLim = 5
        verbose = False        
        showScore = False
        showRawScore = False

        opts, args = getopt.getopt(argv, 'i:o:n:r:h:v:s:')
        for opt, arg in opts:
            if opt == "-h":
                HelpText()
                exit()
            else:
                if opt == "-i":
                    requiredArgs[infile] = arg
                elif opt == "-n":
                    requiredArgs[n] = int(arg)
                elif opt == "-r":
                    requiredArgs[runmode] = arg
                elif opt == "-o":
                    save = True
                    if arg == True:
                        savePath = arg
                elif opt == "-v":
                    validteList = True
                    if arg == "true":
                        verbose = True
                elif opt == "-s":
                    showScore = True
                    if arg == "raw":
                        showRawScore = True
                        showScore = False                

        if testmode == True:
            dataObj = TestDataObject()
            requiredArgs, save, savePath, validateList, authorLim, verbose, showScore, showRawScore = dataObj.GetData()

        empty = []
        for arg in requiredArgs:
            if requiredArgs[arg] == None:
                empty.append(arg)
        if len(empty) > 0:
            print("ERROR")
            print(f"Missing arguments: {empty}")
            exit()        

        inList = OpenPaperList(requiredArgs[infile])
        numAuthors = len(GetAuthorsList(inList))
        if requiredArgs[n] < numAuthors or requiredArgs[n] > 2.5 * numAuthors:
            print("ERROR")
            print("n must be less than (2.5 * number of authors) and greater than (number of authors - 1)")
            exit()

        outList = GetFinalList(inList, requiredArgs[n], requiredArgs[runmode])
        Finalise()
    except Exception as e:
        print('Something went wrong!')
        print(str(e))