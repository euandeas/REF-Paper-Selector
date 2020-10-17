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

    #function to return the highest scoring unsubmitted paper of an author
    def GetHighestUnsubmittedPaper(self, finalPapers):
        score = 0
        highestPaper = None
        for paper in self.unsubmittedPapers:
            if paper.score > score and self in paper.validAuthors and paper not in finalPapers:
                highestPaper = paper
                score = paper.score
        return highestPaper

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