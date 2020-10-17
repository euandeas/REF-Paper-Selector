import refObject as ro

#function to get authors with more than one submission
def FindReplaceableAuthors(finalAuthors):
    replaceableAuthors = []
    for author in finalAuthors:
        if len(author.submittedPapers) > 1:
            replaceableAuthors.append(author)
    return ro.Sort(replaceableAuthors, "lowestSubmission.score") 

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

def FindPapers(inList, n):
    finalPapers = []
    finalAuthors = []
    papers, authors = ro.BuildObjects(inList)    

    for author in authors:
        author.CalculateValue()

    #begin selection process
    ranked_papers = ro.Sort(papers, "score", reverse=True)
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

            finalPapers, finalAuthors = Submit(author.GetHighestSubmittablePaper(finalPapers), author, finalPapers, finalAuthors)
        subCheck, unsubmittedAuthors = CheckSubmissions(authors, finalAuthors)

    return ro.BuildOutlist(finalPapers)