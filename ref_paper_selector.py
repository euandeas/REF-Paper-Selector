from Algorithms.leastpotential-euandeas import FindPapers
from process_data import * 

while True:
    uInput = input()
    if uInput[:2] == "-i":
        iFileName = uInput[3:]
    if uInput[:2] == "-n":
        print("")
        #needs to be implemented
    if uInput[:2] == "-o":
        oFileName = uInput[2:]
    if uInput[:2] == "-g":
        inList = OpenPaperList("papers")
        papersToSubmit = FindPapers(inList)
        SavePaperList(papersToSubmit, "output")
        print(FindScore(papersToSubmit))