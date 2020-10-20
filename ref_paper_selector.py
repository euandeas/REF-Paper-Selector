import math
import argparse
from Algorithms import leastpotential_euandeas as lpe, nottingham_lembn as nlbn, abased_lembn as albn
import process_data as processor
import validate_output as validator

def GetFinalList(inList, n, runmode):
    if runmode == "leastpotential_euandeas":
        outList = lpe.FindPapers(inList, n)
    elif runmode == "nottingham_lembn":
        outList = nlbn.FindPapers(inList, n)
    elif runmode == "abased_lembn":
        outList = albn.FindPapers(inList, n)
    return outList

def Finalise(save, validateList, showScore, showRawScore, verbose, savePath, authorLim):
    if save == True:
        processor.SavePaperList(outList, savePath)
    if validateList == True:
        validator.Validate(inList, outList, authorLim, verbose)
    if showScore == True:
        print(f"\nScore: {processor.RoundScore(processor.FindScore(outList))}")
    if showRawScore == True:
        print(f"\nScore: {processor.FindScore(outList)}")

if __name__ == "__main__":
    try:
        epi = """
ALGORITHMS:
  leastpotential_euandeas
  nottingham_lembn
  abased_lembn

FOLLOW THE PROJECT: github.com/euandeas/REF-Paper-Selector

Created by:
  Euan Deas (github.com/euandeas)
  Lemuel Bodi-Ngwala (github.com/lembn)
  
v1.1.0"""

        parser = argparse.ArgumentParser(prog='REFSelector',
                                         allow_abbrev=False,
                                         formatter_class=argparse.RawTextHelpFormatter,
                                         description='Create a list of the highest scoring papers.',
                                         epilog=epi)

        parser.add_argument('-i', '--infile', metavar="[file]", action='store', help='input file name and location e.g. c:/user/REF/input.csv.')
        parser.add_argument('-n', '--N', action='store', type=int, help='number of papers to be selected.')
        parser.add_argument('-nm', '--nMax', action='store_true', help='create a list of maximum number of papers.')
        parser.add_argument('-r', '--runmode', metavar="[algorithm]", action='store', help='selection algorithm to use e.g. leastpotential_euandeas.')
        parser.add_argument('-o', '--output', action='store_true', help='save to output.csv saved in the same location as the input file.')
        parser.add_argument('-ot', '--outputTo', metavar="[file]", action='store', default=False, help='save ouput to custom filepath.')
        parser.add_argument('-va', '--validate', action='store_true', help='run validate_output.py on the final list to check the validity of the final list.')
        parser.add_argument('-val', '--validateLim', metavar="[x]", action='store', default=5, help='validate with a limit of x papers per author (default = 5).')
        parser.add_argument('-ve', '--verbose', action='store_true', help='run validate_output.py with verbose output. Only valid if --validate flag is passed.')
        parser.add_argument('-s', '--show', action='store_true', help='show score of produced list (rounded to the nearest 0.2).')
        parser.add_argument('-sr', '--showRaw', action='store_true', help='show score of produced list.')

        args = parser.parse_args()
        if args.outputTo == None:
            args.outputTo = "output.csv"
        if args.validateLim == None:
            args.validateLim = 5

        empty = []
        if args.infile == None:
            empty.append("infile (-i)")
        if args.N == None:
            empty.append("number of papers (-n)")
        if args.runmode == None:
            empty.append("runmode (-r)")
        if len(empty) > 0:
            print("ERROR")
            print(f"Missing arguments: {empty}")
            exit()     

        inList = processor.OpenPaperList(args.infile)
        numAuthors = len(validator.GetAuthorsList(inList))
        highestN = 2.5 * numAuthors
        if args.nMax == True:
            args.N = math.trunc(highestN)
        else:
            if args.N < numAuthors or args.N > highestN:
                print("ERROR")
                print("n must be less than (2.5 * number of authors) and greater than (number of authors - 1)")
                exit()

        outList = GetFinalList(inList, args.N, args.runmode)
        Finalise(args.output, args.validate, args.show, args.showRaw, args.verbose, args.outputTo, args.validateLim)
    except Exception as e:
        print('Something went wrong!')
        print(str(e))