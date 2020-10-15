###Sort all papers in desc order by score
###Add papers to final list as the program traverses though the list of papers
###If there is more than one author of a paper, submit the paper with the author with the lowest value
###Value represents the total amount of score an author could potentially add to the final score at any given time
###At the end, make a list of all authors with more than one submitted paper - order by score of their lowest scoring paper asc 
###Authors in this list will have their lowest scoring paper replaced by the highest scoring paper of unsubmitted authors

from operator import attrgetter

#class to represent authors
class Author:
    def __init__(self, authorID):
        self.authorID = authorID
        self.value = 0
        self.submittedPapers = []
        self.unsubmittedPapers = []
        self.lowestSubmission = None #(submitted paper with the lowest score)

    #function to calculate value of author
    #(total of top 5 scoring papers)
    def CalculateValue(self):
        if len(self.unsubmittedPapers) > 5:
            topPapers = self.unsubmittedPapers[:5]
        else:
            topPapers = self.unsubmittedPapers

        topScores = 0
        for paper in topPapers:
            topScores += paper.score
        self.value = topScores

    #function to calculate the lowest scoring submitted paper of an author
    def SetLowestSubmission(self):
        for paper in self.submittedPapers:
            if self.lowestSubmission == None:
                self.lowestSubmission = paper
            else:
                if paper.score < self.lowestSubmission.score:
                    self.lowestSubmission = paper

    #function to return the highest scoring unsubmitted paper of an author
    def GetHighestUnsubmittedPaper(self):
        highestPaper = Paper(0, 0, 0)
        for paper in self.unsubmittedPapers:
            if paper.score > highestPaper.score:
                highestPaper = paper
        return highestPaper

    #function to declare an author as invalid across the program
    def Invalidate(self):
        for paper in self.unsubmittedPapers:
            paper.validAuthors.remove(self)


#class to represent papers
class Paper:
    def __init__(self, paperID, author, score):
        self.paperID = paperID
        self.authors = []
        self.validAuthors = self.authors
        self.authors.append(author)
        self.score = float(score)
        self.submittedAuthor = None

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


#function to submit papers
def Submit(paper, author, finalPapers, finalAuthors):
    paper.submittedAuthor = author
    finalPapers.append(paper)
    author.submittedPapers.append(paper)
    author.unsubmittedPapers.remove(paper)
    author.SetLowestSubmission()
    if author not in finalAuthors:
        finalAuthors.append(author)
    if len(author.submittedPapers) == 5:
        author.Invalidate()
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
            author = Author(authorID)
            authors.append(author)

        paper = GetObjectByID(paperID, papers, "p")
        if paper == False:
            papers.append(Paper(paperID, author, paperScore))
        else:
            paper.authors.append(author)

    return papers, authors

def BuildOutlist(papers):
    outlist = []
    for paper in papers:
        outlist.append([paper.submittedAuthor.authorID, paper.paperID, paper.score])
    return outlist

def FindPapers(inList, n):
    finalPapers = []
    finalAuthors = []
    papers, authors = BuildObjects(inList)

    #order papers from highest to lowest (by score)
    ranked_papers = list(reversed(sorted(papers, key=attrgetter('score'))))

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

            if len(paper.authors) > 1:
                values = {}
                for author in paper.validAuthors:
                    values[paper.validAuthors.index(author)] = author.value
                authorIndex = min(values)

            if submittable == True:
                finalPapers, finalAuthors = Submit(paper, paper.validAuthors[authorIndex], finalPapers, finalAuthors)
                n -= 1

    #get authors with more than one submission
    replaceableAuthors = []
    for author in finalAuthors:
        if len(author.submittedPapers) > 1:
            replaceableAuthors.append(author)

    #order replaceable authors from lowest to highest (by lowestSubmission)
    submittedAuthors_lowestSub = sorted(replaceableAuthors, key=attrgetter('lowestSubmission.score'))

    #loop to make sure all authors have at least one submitted paper
    for author in authors:
        if author not in finalAuthors:
            #'replaceTarget' represents the author to be replaced
            replaceTarget = submittedAuthors_lowestSub[0]
            finalPapers.remove(replaceTarget.lowestSubmission)
            replaceTarget.submittedPapers.remove(replaceTarget.lowestSubmission)
            replaceTarget.unsubmittedPapers.append(replaceTarget.lowestSubmission)
            del submittedAuthors_lowestSub[0]
            finalPapers, finalAuthors = Submit(author.GetHighestUnsubmittedPaper(), author, finalPapers, finalAuthors)

    return BuildOutlist(finalPapers)