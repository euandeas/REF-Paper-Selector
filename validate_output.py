from collections import defaultdict

def GetAuthorsList(mList):
    finalDic = defaultdict(int)
    for x in mList:
        finalDic[x[0]] = 0  
    return finalDic

def validate(inList, outList, maxPerAuthor):
    authors = GetAuthorsList(inList)
    
    meetsReq = True
    numberOfAuthorsWithNoPapers = 0
    numberOfAuthorsWithToManyPapers = 0
    
    for x in outList:
        authors[x[1]] += 1

    for y in authors:
        if authors[y] == 0:
            meetsReq = False
            numberOfAuthorsWithNoPapers += 1
        if authors[y] > maxPerAuthor:
            meetsReq = False
            numberOfAuthorsWithToManyPapers += 1
    
    print(f"Valid results?: {meetsReq}")
    print(f"Total errors: {numberOfAuthorsWithNoPapers + numberOfAuthorsWithToManyPapers}")
    print(f"Total number of authors with no papers: {numberOfAuthorsWithNoPapers}")
    print(f"Total number of authors with to many papers: {numberOfAuthorsWithNoPapers}")




