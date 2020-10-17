# Highest score = 563.6
from collections import defaultdict

class Author():
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
            
    def CalculateTotal(self):
        total = 0
        tempList = list(self.papers.keys())
        for key in tempList[0:4]:
            total += float(self.papers[key])
        self.top5Total = total

    def __init__(self, papersList, maxPapersPerAuthor):
        self.papers = {k: v for k, v in sorted(papersList.items(), key=lambda item: item[1],reverse= True)}
        self.maxPapersPerAuthor = maxPapersPerAuthor
        self.CalculateTotal()

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

def FindPapers(pAllList, numOfPapers):
    AuthorsDic = CreateAuthorsDic(pAllList)
    pAList = GetPapersAuthorsDic(pAllList)

    toBeSubmitted = []

    pScList = GetPapersScoresDic(pAllList)
    pScList = {k: v for k, v in sorted(pScList.items(), key=lambda item: item[1], reverse= True)}

    for x in pScList:
        tempListOfAuthors = []
        tempListOfAuthors = pAList[x]
        
        authorToPick = []
        count = 0
        foundAuthor = False
        while foundAuthor == False:
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

        if len(toBeSubmitted) == numOfPapers:
            break

    for n in AuthorsDic:
        if AuthorsDic[n].numOfSubmittedPapers == 0:
            for x in AuthorsDic[n].papers:
                if any(x in sublist for sublist in toBeSubmitted):
                    for sublist in toBeSubmitted:
                        if AuthorsDic[sublist[1]].numOfSubmittedPapers > 1 and sublist[0] == x:
                            index = toBeSubmitted.index(sublist)
                            AuthorsDic[sublist[1]].numOfSubmittedPapers -= 1
                            toBeSubmitted[index][1] = n
                            AuthorsDic[n].numOfSubmittedPapers += 1
                            break
                            break
                else:
                    for sublist in toBeSubmitted[::-1]: 
                        if AuthorsDic[sublist[1]].numOfSubmittedPapers > 1:
                            index = toBeSubmitted.index(sublist)
                            AuthorsDic[sublist[1]].numOfSubmittedPapers -= 1
                            AuthorsDic[n].numOfSubmittedPapers += 1
                            toBeSubmitted[index] = [x, n, pScList[x]]
                            break
                            break
        if AuthorsDic[n].numOfSubmittedPapers == 0:
            print(f"ERROR: Could not find a way to get author {n} into list of papers!")
                
    return toBeSubmitted