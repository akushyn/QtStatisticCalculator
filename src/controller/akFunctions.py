import csv
import os

def loadCSV(fileName):
    data = []
    with open(fileName, "r") as fileInput:
        for row in csv.reader(fileInput):
            items = [field for field in row]
            data.append(items)

        # remove 'Volume' column
        for row in data:
            del row[5]

        # get 'Headers'
        headers = data.pop(0)
    return headers, data

def getShortName(pathFileName):
    return os.path.splitext(os.path.basename(pathFileName))[0]