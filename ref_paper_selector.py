import sys
import getopt
import math
from Algorithms import leastpotential_euandeas as lpe, nottingham_lembn as nlbn, abased_lembn as albn
import process_data as processor
import validate_output as validator

def RepresentsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False

def HelpText():
    print("\n====================================================================================\n")
    print("-i [filepath]            input file name and location e.g. c:/user/REF/input.csv\n")

    print("-r [algorithm_name]      selection algorithm to use e.g. leastpotential_euandeas")
    print("ALGORITHMS:")
    print("leastpotential_euandeas")
    print("nottingham_lembn")
    print("abased_lembn\n")

    print("-n [x]                   select x papers")
    print("OPTIONS:")
    print("-n max                   set n to the highest possible value with the given dataset\n")

    print("-o true                  save to output.csv saved in the same location as the input file")
    print("OPTIONS:")
    print("-o [filepath]            custom filepath or filename.\n")

    print("-v true                  run validate_output.py on the final list to check the validity of the final list") 
    print("OPTIONS:")
    print("-v [x]                   validate with a limit of x papers per author (default = 5)")
    print("-v v                     run validate_output.py in verbose mode\n")  
    
    print("-s true                  show score of produced list (rounded down to the nearest 0.2)")
    print("OPTIONS:")
    print("-s raw                   show the raw value of the score")
    print("\n====================================================================================\n")

def GetFinalList(inList, n, runmode):
    if runmode == "leastpotential_euandeas":
        outList = lpe.FindPapers(inList, n)
    elif runmode == "nottingham_lembn":
        outList = nlbn.FindPapers(inList, n)
    elif runmode == "abased_lembn":
        outList = albn.FindPapers(inList, n)

    return outList

def Finalise():
    if save == True:
        processor.SavePaperList(outList, savePath)

    if validateList == True:
        validator.Validate(inList, outList, authorLim, verbose)

    if showScore == True:
        print(f"\nScore: {processor.RoundScore(processor.FindScore(outList))}")
    elif showRawScore == True:
        print(f"\nScore: {processor.FindScore(outList)}")

if __name__ == "__main__":
    argv = sys.argv[1:]
    try:
        infile = "infile (-i)"
        n = "number of papers (-n)"
        runmode = "runmode(-r)"
        requiredArgs = {infile: None, n: None, runmode: None}

        maxN = False
        save = False
        savePath = "output.csv"
        validateList = False
        authorLim = 5
        verbose = False        
        showScore = False
        showRawScore = False

        opts, _ = getopt.getopt(argv, 'i:o:n:r:h:v:s:')
        if len(opts) == 0:
            HelpText()
            exit()
        for opt, arg in opts:
            if opt == "-h":
                HelpText()
                exit()
            else:
                if opt == "-i":
                    requiredArgs[infile] = arg
                elif opt == "-r":
                    requiredArgs[runmode] = arg
                elif opt == "-n":
                    if arg == "max":
                        maxN = True
                    elif RepresentsInt(arg) == True:
                        requiredArgs[n] = int(arg)
                elif opt == "-o":
                    if arg == "true":
                        save = True
                    else:
                        save = True
                        savePath = arg
                elif opt == "-v":
                    if arg == "true":
                        validteList = True
                    elif RepresentsInt(arg) == True:
                        authorLim == int(arg)
                        validteList = True
                    elif arg == "v":
                        validateList = True
                        verbose = True
                elif opt == "-s":
                    if arg == "true":
                        showScore = True
                    if arg == "raw":
                        showRawScore = True
                        showScore = False

        empty = []
        for arg in requiredArgs:
            if requiredArgs[arg] == None:
                empty.append(arg)
        if len(empty) > 0:
            print("ERROR")
            print(f"Missing arguments: {empty}")
            exit()        

        inList = processor.OpenPaperList(requiredArgs[infile])
        numAuthors = len(validator.GetAuthorsList(inList))
        highestN = 2.5 * numAuthors
        if maxN == True:
            requiredArgs[n] = math.trunc(highestN)
        else:
            if requiredArgs[n] < numAuthors or requiredArgs[n] > highestN:
                print("ERROR")
                print("n must be less than (2.5 * number of authors) and greater than (number of authors - 1)")
                exit()

        outList = GetFinalList(inList, requiredArgs[n], requiredArgs[runmode])
        Finalise()
    except Exception as e:
        print('Something went wrong!')
        print(str(e))
