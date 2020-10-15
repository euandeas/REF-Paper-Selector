import sys
import getopt
from Algorithms import leastpotential_euandeas as lpe, nottingham_lembn as lbn
from process_data import * 
from validate_output import *

def HelpText():
    print("-i    input file name and location e.g. c:/user/REF/input")
    print("-o    output file name (optional) - Default = output.csv saved in the same location as the input file.")
    print("-n    total number of unique papers to be selected")
    print("-r    selection algorithm to use e.g. leastpotential_euandeas")
    print("-v    run validate_output.py on the final list to check the validity of the final list")
    print("-vv    run validate_output.py on the final list to check the validity of the final list")

def GetFinalList(inList, n, runmode):
    if runmode == "leastpotential-euandeas":
        outList = lpe.FindPapers(inList)
    elif runmode == "nottingham-lembn":
        outList = lbn.FindPapers(inList, n)

    return outList

if __name__ == "__main__":
    argv = sys.argv[1:]
    try:
        params = ["infile", "outfile", "number of papers (n)", "runmode"]
        mainArgs = ["infile", "outfile", "number of papers (n)", "runmode"]

        opts, args = getopt.getopt(argv, 'i:o:n:r:h:v:')
        validateList = False
        verbose = False
        for opt, arg in opts:
            if opt == "-h":
                HelpText()
                exit()
            else:
                if opt == "-i":
                    mainArgs[0] = arg
                elif opt == "-o":
                    mainArgs[1] = arg
                elif opt == "-n":
                    mainArgs[2] = int(arg)
                elif opt == "-r":
                    mainArgs[3] = arg
                elif opt == "-v":
                    validteList = True
                elif opt == "-vv":
                    validateList = True
                    verbose = True

        #mainArgs = ["testpapers", "output", 50, "leastpotential-euandeas"]
        mainArgs = ["testpapers", "output", 50, "nottingham-lembn"]
        validateList = True
        verbose = True

        if mainArgs[1] == "outfile":
            mainArgs[1] = "output"

        empty = []
        for arg in mainArgs:
            if arg in params:
                empty.append(arg)
                
        if len(empty) > 0:
            print("Missing arguments: " + str(empty))
            exit()        

        inList = OpenPaperList(mainArgs[0])
        numAuthors = len(GetAuthorsList(inList))
        if mainArgs[2] < numAuthors or mainArgs[2] > 2.5 * numAuthors:
            print("n must be less than (2.5 * number of authors) and greater tham (number of authors - 1)")
            exit()
        outList = GetFinalList(inList, mainArgs[2], mainArgs[3])
        #SavePaperList(outList, mainArgs[1])
        print("Score: " + str(FindScore(outList)))
        if validateList == True:
            Validate(inList, outList, 5, verbose)

    except getopt.GetoptError:
        print('Something went wrong!')