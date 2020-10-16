import json
import ast

class TestDataObject:
    def __init__(self):
        with open('testmode_data.json') as dataFile:
            data = json.load(dataFile)
            self.requiredArgs = ast.literal_eval(data['requiredArgs'])
            self.maxN = data['maxN']
            self.save = data['save']
            self.savePath = data['savePath']
            self.validateList = data['validateList']
            self.authorLim = int(data['authorLim'])
            self.verbose = data['verbose']
            self.showScore = data['showScore']
            self.showRawScore = data['showRawScore']

    def GetData(self):
        return self.requiredArgs, self.maxN, self.save, self.savePath, self.validateList, self.authorLim, self.verbose, self.showScore, self.showRawScore