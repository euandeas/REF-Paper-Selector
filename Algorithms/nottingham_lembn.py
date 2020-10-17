from operator import attrgetter
import refObject as ro

#function to return a paper from 'papers'. Returns False if not in list
def GetObjectByID(target, arr, runmode):
    if runmode == "p":
        for paper in arr:
            if paper.paperID == target:
                return paper
        return False
    elif runmode == "a":
        for author in arr:
            if author.authorID == target:
                return author
        return False

#function to sort lists by 'key'
def Sort(arr, key, reverse=False):
    if reverse == False:
        return sorted(arr, key=attrgetter(key))
    else:
        return list(reversed(sorted(arr, key=attrgetter(key))))

#function to get authors with more than one submission
def FindReplaceableAuthors(finalAuthors):
    replaceableAuthors = []
    for author in finalAuthors:
        if len(author.submittedPapers) > 1:
            replaceableAuthors.append(author)
    return Sort(replaceableAuthors, "lowestSubmission.score") 

def CheckSubmissions(fullList, selection):
    leftOut = []
    for author in fullList:
        if author not in selection:
            leftOut.append(author)
    if len(leftOut) == 0:
        return True, []
    else:
        return False, leftOut

#function to submit papers
def Submit(paper, author, finalPapers, finalAuthors):
    paper.submittedAuthor = author
    finalPapers.append(paper)
    author.submittedPapers.append(paper)
    author.unsubmittedPapers.remove(paper)
    author.SetLowestSubmission(finalPapers)
    if author not in finalAuthors:
        finalAuthors.append(author)
    author.CalculateValidity()
    author.CalculateValue()

    return finalPapers, finalAuthors

#statment to parse data from csv
def BuildObjects(inList):
    papers = []
    authors = []

    for row in inList:
        authorID = row[0]
        paperID = row[1]        
        paperScore = row[2]

        author = GetObjectByID(authorID, authors, "a")
        if author == False:
            author = ro.Author(authorID)
            authors.append(author)

        paper = GetObjectByID(paperID, papers, "p")
        if paper == False:
            papers.append(ro.Paper(paperID, author, paperScore))
        else:
            paper.authors.append(author)

    return papers, authors

def BuildOutlist(papers):
    outlist = []
    for paper in papers:
        outlist.append([paper.paperID, paper.submittedAuthor.authorID, paper.score])
    return outlist

def FindPapers(inList, n):
    finalPapers = []
    finalAuthors = []
    papers, authors = BuildObjects(inList)

    #order papers from highest to lowest (by score)
    ranked_papers = Sort(papers, "score", reverse=True)

    #assign papers to the authors who wrote them
    #assing from the ranked list so authors.unsubmittedPapers will be ordered DESC
    for paper in ranked_papers:
        for author in paper.authors:
            author.unsubmittedPapers.append(paper)

    for author in authors:
        author.CalculateValue()

    #begin selection process
    for paper in ranked_papers:
        if n > 0:
            authorIndex = 0
            submittable = True

            if len(paper.validAuthors) == 0:
                submittable = False
            elif len(paper.validAuthors) > 1:
                values = {}
                for author in paper.validAuthors:
                    values[paper.validAuthors.index(author)] = author.value
                authorIndex = min(values)

            if submittable == True:
                finalPapers, finalAuthors = Submit(paper, paper.validAuthors[authorIndex], finalPapers, finalAuthors)
                n -= 1

    submittedAuthors_lowestSub = FindReplaceableAuthors(finalAuthors)
    subCheck, unsubmittedAuthors = CheckSubmissions(authors, finalAuthors)
    #loop to make sure all authors have at least one submitted paper
    while subCheck == False:
        for author in unsubmittedAuthors:
            #'replaceTarget' represents the author to be replaced
            replaceTarget = submittedAuthors_lowestSub[0]
            finalPapers.remove(replaceTarget.lowestSubmission)
            replaceTarget.submittedPapers.remove(replaceTarget.lowestSubmission)
            replaceTarget.unsubmittedPapers.append(replaceTarget.lowestSubmission)

            if len(replaceTarget.submittedPapers) == 0:
                finalAuthors.remove(replaceTarget)

            replaceTarget.SetLowestSubmission(finalPapers)
            replaceTarget.CalculateValidity()
            submittedAuthors_lowestSub = FindReplaceableAuthors(finalAuthors)

            finalPapers, finalAuthors = Submit(author.GetHighestUnsubmittedPaper(finalPapers), author, finalPapers, finalAuthors)
        subCheck, unsubmittedAuthors = CheckSubmissions(authors, finalAuthors)

    return BuildOutlist(finalPapers)