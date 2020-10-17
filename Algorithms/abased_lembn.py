import refObject as ro

def FindPapers(inList, n):
    finalPapers = []
    _, authors = ro.BuildObjects(inList)

    for author in authors:
        author.SetHSPs(finalPapers, papersIsEmpty=True)

    #rank authors by HSS DESC
    authors = ro.Sort(authors, "HSPScore", reverse=True)

    while n > 0:
        for author in authors:
            if n <= 0:
                break
            if len(author.submittedPapers) < 5:
                author.SetHSPs(finalPapers)
                if len(author.HSPs) == 1:
                    paper = author.HSPs[0]
                    finalPapers.append(paper)
                    paper.submittedAuthor = author
                    author.HSPs = [ro.Paper(None, None, 0)]
                    author.submittedPapers.append(paper)       
                    author.unsubmittedPapers.remove(paper)
                    author.SetHSPs(finalPapers)
                    n -= 1
                else:
                    print()
                    for paper in author.HSPs:
                        print(f"Index [{author.HSPs.index(paper)}]: {paper.paperID} by {paper.GetAuthorIDs()}")
                    print("The paper(s) above are all considerable for submission")
                    index = -1
                    while index < 0 or index > len(author.HSPs) - 1:
                        index = input("Enter the index of the paper which should be submitted: ")
                        try: 
                            index = int(index)
                        except ValueError:
                            index = -1

                    paper = author.HSPs[index]
                    finalPapers.append(paper)
                    paper.submittedAuthor = author
                    author.HSPs = [ro.Paper(None, None, 0)]
                    author.submittedPapers.append(paper)       
                    author.unsubmittedPapers.remove(paper)
                    author.SetHSPs(finalPapers)
                    n -= 1
        authors = ro.Sort(authors, "HSPScore", reverse=True)

    return ro.BuildOutlist(finalPapers)