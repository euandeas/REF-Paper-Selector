import csv

def OpenPaperList(iFileName):
    with open(iFileName) as csv_file:
        csv_reader = csv.reader(csv_file, delimiter=',')
        line_count = 0
        paperList = []
        for row in csv_reader:
            if line_count == 0:
                line_count += 1
            else:
                paperList.append([row[0],row[1],row[2]])
                line_count += 1
    return paperList

def SavePaperList(mList, oFileName):
    with open(oFileName, 'w', newline='') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(["Paper","Author","Score"])
        for n in mList:
            writer.writerow(n)

def FindScore(mList):
    total = 0
    for n in mList:
        total += n[2]
    return total

def RoundScore(score):
    return (round(score * 5) / 5)