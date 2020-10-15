from Algorithms import *
from process_data import OpenPaperList, SavePaperList, FindScore
import sys
import getopt



def HelpText():
    print("-i    input file name and location e.g. c:/user/REF/input.csv")
    print("-o    output file name (optional) - Default = output.csv saved in the same location as the input file.")
    print("-n    total number of unique papers to be selected")
    print("-r    selection algorithm to use e.g. leastpotential-euandeas")

def Main(infile, outfile, n, runmode):   
    try:
        inList = OpenPaperList(infile)
    except Exception as e:
        print(e)

    if runmode == "leastpotential_euandeas":
        outList = leastpotential_euandeas.FindPapers(inList)

    SavePaperList(outList, outfile)
    print("Score: " + FindScore(outList))


if __name__ == "__main__":
    argv = sys.argv[1:]
    try:
        params = ["infile", "outfile", "number of papers (n)", "runmode"]
        mainArgs = ["", "", "", ""]

        opts, args = getopt.getopt(argv, 'i:o:n:r:h:')
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
                    mainArgs[2] = arg
                elif opt == "-r":
                    mainArgs[3] = int(arg)

        empty = []
        for arg in mainArgs:
            if arg in params:
                empty.append(arg)
                
        if len(empty) > 0:
            print(f"Missing arguments : {empty}")
            exit()

        Main(mainArgs[0], mainArgs[1], mainArgs[2], mainArgs[3])
    except getopt.GetoptError:
        print('Something went wrong!')    
