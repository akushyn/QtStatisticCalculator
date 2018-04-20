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


def getDistributionList():
    global highLow, highClose, openHigh, openLow, lowClose, data, distributions

    # D - [0]   O - [1]   H - [2]   L - [3]   C - [4]
    data = csv.csvData
    # print(DataFrame(data))

    for i in range(len(data)):
        if (i == 0):
            continue
        highLow.append(float(data[i][2]) - float(data[i][3]))
        highClose.append(float(data[i][2]) - float(data[i][4]))
        openHigh.append(float(data[i][2]) - float(data[i][1]))
        openLow.append(float(data[i][1]) - float(data[i][3]))
        lowClose.append(float(data[i][4]) - float(data[i][3]))

    # append data according to shortNames posistions
    distributions = []
    distributions.append(highLow)
    distributions.append(highClose)
    distributions.append(openHigh)
    distributions.append(openLow)
    distributions.append(lowClose)

    return distributions
