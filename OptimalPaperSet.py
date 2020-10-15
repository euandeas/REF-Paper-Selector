import csv
from collections import defaultdict

# Total each authors top 5 scores
# What I need:
#   Object for each author with each paper they are related to and their scores
#   Dictionary of author objects
#   Ordered dictionary of papers with scores

iFileName = "default"
oFileName = "default"

class Author():
    topBoundScore = 0
    lowerBoundScore = 0 
    maxPapersPerAuthor = 0
    top5Total = 0
    numOfSubmittedPapers = 0
    
    def canPaperSubmit(self):
        if self.numOfSubmittedPapers == self.maxPapersPerAuthor:
            return False
        else:
            self.numOfSubmittedPapers += 1
            return True

    def removePaper(self, paperId):
        self.papers.pop(paperId)
        self.CalculateTotal()
        #self.topBoundScore += 1
        #self.lowerBoundScore += 1
            
    def CalculateTotal(self):
        total = 0
        tempList = list(self.papers.keys())
        for key in tempList[self.topBoundScore:self.lowerBoundScore-1]:
            total += float(self.papers[key])
        self.top5Total = total

    def __init__(self, papersList, maxPapersPerAuthor):
        self.papers = {k: v for k, v in sorted(papersList.items(), key=lambda item: item[1],reverse= True)}
        self.lowerBoundScore = maxPapersPerAuthor
        self.maxPapersPerAuthor = maxPapersPerAuthor
        self.CalculateTotal()

def OpenPaperList():
    with open(f'{iFileName}.csv') as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        paperList = []
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                paperList.append([row[0],row[1],row[2]])
                line_count += 1
            print(f'Processed {line_count} lines.')
    return paperList

def GetPapersScoresDic(mList):
    fDic = defaultdict(int)
    for x in mList:
        fDic[x[1]] = float(x[2]) 
    return fDic

def GetPapersAuthorsDic(mList):
    fDic = defaultdict(list)
    for x in mList:
        fDic[x[1]].append(x[0])    
    return fDic

def GetAuthorsList(mList):
    finalDic = defaultdict(int)
    for x in mList:
        finalDic[x[0]] = None  
    return finalDic

def GetAuthorsPapersDic(mList):
    fDic = defaultdict(list)
    for x in mList:
        fDic[x[0]].append(x[1])    
    return fDic

def CreateAuthorsDic(mList):
    finalDic = defaultdict(Author)
    AuthorPaperDic = GetAuthorsPapersDic(mList)
    papersScores = GetPapersScoresDic(mList)
    
    for x in mList:
        finalDic[x[0]] = None 

    for key in finalDic:
        papersDic = defaultdict(float)
        for value in AuthorPaperDic[key]:
            papersDic[value] = papersScores[value]
        finalDic[key] = Author(papersDic,5)

    return finalDic

def findStrongestSetOfPapers():
    pAllList = OpenPaperList()
    AuthorsDic = CreateAuthorsDic(pAllList)

    # Dic of {paper, [authors]}
    pAList = GetPapersAuthorsDic(pAllList)

    toBeSubmitted = []

    pScList = GetPapersScoresDic(pAllList)
    pScList = {k: v for k, v in sorted(pScList.items(), key=lambda item: item[1], reverse= True)}

    #x is key
    for x in pScList:
        tempListOfAuthors = []
        tempListOfAuthors = pAList[x]
        
        authorToPick = []
        count = 0
        foundAuthor = False
        while foundAuthor == False:
            print(tempListOfAuthors)
            print(authorToPick)
            for y in tempListOfAuthors:
                if count == 0:
                    authorToPick = [y,AuthorsDic[y].top5Total]
                    count += 1
                else:
                    if AuthorsDic[y].top5Total < authorToPick[1]:
                        authorToPick = [y,AuthorsDic[y].top5Total]
            
            if AuthorsDic[authorToPick[0]].canPaperSubmit() == True:
                toBeSubmitted.append([x, authorToPick[0], pScList[x]])
                foundAuthor = True
            else:
                try:
                    tempListOfAuthors.remove(y)
                except:
                    foundAuthor = True
        
        for y in tempListOfAuthors:
            AuthorsDic[y].removePaper(x)
        print("----")
        

    total = 0
    f = open(f'{oFileName}.csv', mode='w')
    writer = csv.writer(f)
    writer.writerow(["Paper","Author","Score"])
    for n in toBeSubmitted:
        writer.writerow(n)
        total += n[2]
    print(total)
    print("")

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
        findStrongestSetOfPapers()

#What needs to be done now?
#   Make it so you can set num of unique papers to be selected - this is tricky as we still have to make sure each author has at least one paper
#   Where an author has two or more papers eligible for selection, for example more than two papers with the same score for that author, then the script should take one of the following options??? - need more info