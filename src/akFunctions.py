import csv
import os
from dateutil import parser

from src.data.akEnums import AkSourceType, AkSelectionMethod


class AkFunctions:

    @classmethod
    def toFixed(cls, f, n=0):
        a, b = str(f).split('.')
        return '{}.{}{}'.format(a, b[:n], '0' * (n - len(b)))

    @classmethod
    def fold(cls, xData, method):

        d = xData[len(xData) - 1][0]
        h, _ = cls.max(xData)
        l, _ = cls.min(xData)

        # метод селекції Close[i] - Close[i-1]
        if (method == AkSelectionMethod.CC):
            o = xData[0][4]
            c = xData[len(xData) - 1][4]

        # метод селекції Close[i] - Open[i]
        elif (method == AkSelectionMethod.OC):
            o = xData[0][1]
            c = xData[len(xData) - 1][4]

        return [d, o, h, l, c]

    @classmethod
    def dataType(cls, date0, date1):
        """
        Метод повертає тип даних періоду по двум заданим датам.

        :param: date0. Дата першого елемента даних періоду.
        :param: date1. Дата другого елемента даних періоду.
        :return: AkSectionType().
        """

        # беремо перші два значення даних періоду
        dt0 = parser.parse(date0)
        dt1 = parser.parse(date1)

        dType = None

        # ідемо від найбільшого до найменшого значення по календарю.
        # якщо різниця дат у році, тип даних 'Year'
        if ((dt1.year - dt0.year) > 0):
            dType = AkSourceType.Y

        # якщо різниця дат у кварталі, то тип даних 'Quarter'
        elif ((AkFunctions.getQuarters(dt1) - AkFunctions.getQuarters(dt0)) > 0):
            dType = AkSourceType.Q

        # якщо різниця дат у місяці, то тип даних 'Month'
        elif ((dt1.month - dt0.month) > 0):
            dType = AkSourceType.M

        # якщо різниця дат у тижні, то тип даних 'Week'
        elif ((AkFunctions.getWeeks(dt1) - AkFunctions.getWeeks(dt0)) > 0):
            dType = AkSourceType.W

        # якщо різниця дат у дні, то тип даних 'Day'
        elif ((dt1.day - dt0.day) > 0):
            dType = AkSourceType.D

        return dType


    @classmethod
    def getQuarters(cls, dt):
        return (dt.month - 1) // 3 + 1

    @classmethod
    def getWeeks(cls, dt):
        return dt.isocalendar()[1]

    @classmethod
    def loadCSV(cls, fileName):
        data = []
        with open(fileName, "r") as fileInput:
            for row in csv.reader(fileInput):
                items = []
                for i in range(5):
                    items.append(row[i]) # = [field for field in row]
                data.append(items)

            headers = data.pop(0)
        return headers, data

    @classmethod
    def getShortName(cls, pathFileName):
        return os.path.splitext(os.path.basename(pathFileName))[0]

    @classmethod
    def max(cls, xData):
        '''Get maxValue & rowIndex of x_data.'''
        maxValue = xData[0][2] # High[0]
        rowIndex = 0
        for j in range(len(xData)):
            if (float(xData[j][2]) > float(maxValue)):
                maxValue = xData[j][2]
                rowIndex = j

        return maxValue, rowIndex

    @classmethod
    def min(cls, xData):
        '''Get minValue & rowIndex of x_data.'''
        minValue = xData[0][3] # High[0]
        rowIndex = 0
        for j in range(1, len(xData)):
            if (float(xData[j][3]) < float(minValue)):
                minValue = xData[j][3]
                rowIndex = j

        return minValue, rowIndex