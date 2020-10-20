from operator import attrgetter

#class to represent authors
class Author:
    def __init__(self, authorID):
        self.authorID = authorID
        self.value = 0
        self.submittedPapers = []
        self.unsubmittedPapers = []
        self.lowestSubmission = None #(submitted paper with the lowest score)
        self.HSPs = [Paper(None, None, 0)] #Highest Submittable Papers
        self.HSPScore = 0 #Highest Scoring Paper Score

    ###INTERNAL METHODS

    #function to assign papers to the authors who wrote them
    def PopulateUnsubmittedPapers(self, papers):
        for paper in papers:
            for author in paper.authors:
                if author.authorID == self.authorID:
                    self.unsubmittedPapers.append(paper)

    ###GENERAL METHODS

    #function to return the highest scoring unsubmitted paper of an author
    def GetHighestSubmittablePaper(self, finalPapers):
        score = 0
        highestPaper = None
        for paper in self.unsubmittedPapers:
            if paper.score > score and self in paper.validAuthors and paper not in finalPapers:
                highestPaper = paper
                score = paper.score
        return highestPaper

    ###NOTTINGHAM METHODS

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
    def SetLowestSubmission(self, finalPapers):
        if len(self.submittedPapers) == 1:
            self.lowestSubmission = self.submittedPapers[0]
        else:
            for paper in self.submittedPapers:
                if self.lowestSubmission == None or self.lowestSubmission not in finalPapers:
                    self.lowestSubmission = paper
                else:
                    if paper.score < self.lowestSubmission.score:
                        self.lowestSubmission = paper

    #function to declare an author as invalid across the program
    def CalculateValidity(self):
        if len(self.submittedPapers) >= 5:
            for paper in self.unsubmittedPapers:
                if self in paper.validAuthors:
                    paper.validAuthors.remove(self)
                    paper.invalidAuthors.append(self)
        else:
            for paper in self.unsubmittedPapers:
                if self not in paper.validAuthors:
                    paper.validAuthors.append(self)
                    paper.invalidAuthors.remove(self)

    #ABASED METHODS

    #function to set the hss of an author
    def SetHSPs(self, papers, papersIsEmpty=False):
        self.HSPs = [Paper(None, None, 0)]
        unsubmittable = 0
        if papersIsEmpty == False:
            for paper in self.unsubmittedPapers:
                if paper not in papers:
                    if paper.score > self.HSPs[0].score:
                        self.HSPs.clear()
                        self.HSPs.append(paper)
                    elif paper not in self.HSPs and paper.score == self.HSPs[0].score:
                        self.HSPs.append(paper)
                else:
                    self.unsubmittedPapers.remove(paper)
                    unsubmittable += 1
        else:
            for paper in self.unsubmittedPapers:
                if paper.score > self.HSPs[0].score:
                    self.HSPs.clear()
                    self.HSPs.append(paper)
                elif paper not in self.HSPs and paper.score == self.HSPs[0].score:
                    self.HSPs.append(paper)

        if unsubmittable == len(self.unsubmittedPapers):
            self.submittedPapers = [Paper(None, None, 0), Paper(None, None, 0), Paper(None, None, 0), Paper(None, None, 0), Paper(None, None, 0)]

        self.HSPScore = self.HSPs[0].score

#class to represent papers
class Paper:
    def __init__(self, paperID, author, score):
        self.paperID = paperID
        self.authors = []
        self.validAuthors = self.authors
        self.invalidAuthors = []
        self.authors.append(author)
        self.score = float(score)
        self.submittedAuthor = None

    #ABASED METHODS

    def GetAuthorIDs(self):
        IDs = []
        for author in self.authors:
            IDs.append(author.authorID)
        return IDs


#function to sort lists by 'key'
def Sort(arr, key, reverse=False):
    if reverse == False:
        return sorted(arr, key=attrgetter(key))
    else:
        return list(reversed(sorted(arr, key=attrgetter(key))))

#function to return an object from a list using its ID. Returns False if not in list
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

#function to create objects from in list
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

    #order papers from highest to lowest (by score)   
    #assing papers from the ranked list so authors.unsubmittedPapers will be ordered DESC
    ranked_papers = Sort(papers, "score", reverse=True)
    for author in authors:
        author.PopulateUnsubmittedPapers(ranked_papers)

    return papers, authors

#function to create final list of papers in desired format
def BuildOutlist(papers):
    outlist = []
    for paper in papers:
        outlist.append([paper.paperID, paper.submittedAuthor.authorID, paper.score])
    return outlist