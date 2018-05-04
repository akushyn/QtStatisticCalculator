from enum import Enum

class AkPatternType(Enum):
    POSITIVE = 1
    NEGATIVE = -1

class AkPattern(object):
    def __init__(self, degree):
        self._degree = degree
        self._list = self._set_list()
        self._type = self._set_type()

    def degree(self):
        '''Get degree of pattern.'''
        return self._degree

    def type(self):
        '''Get pattern type: return: AkPatternType.'''
        return self._type

    def length(self):
        '''Get length of pattern.'''
        return len(self._list)

    def list(self):
        '''Get pattern list.'''
        return self._list

    def _set_type(self):
        if (self._degree > 0):
            return AkPatternType.POSITIVE

        return AkPatternType.NEGATIVE

    def _set_list(self):
        s = []
        degree = self.degree()
        for i in range(1, abs(degree) + 1):
            if (degree < 0):
                s.append(-i)
            elif (degree > 0):
                s.append(i)
            else:
                raise Exception("Invalid power. Power can't be 0")
        return s


class AkSequence(object):
    def __init__(self, sequence=[]):
        self._list = sequence

    def sequence(self):
        '''Get sequence list.'''
        return self._list

    def patternIndexes(self, pattern):
        '''Get List of pattern indexes'''
        if (pattern.degree() == 0) or (pattern.degree() == -1) or (pattern.degree() == 1):
            return []

        matches = []
        for i in range(self.length() - pattern.length() + 1):
            if self._list[i] == pattern.list()[0] and self._list[i:i + len(pattern.list())] == pattern.list():
                if (self._valid_boundaries(i, pattern)):
                    matches.append(i)
        return matches

    def _valid_boundaries(self, idx, pattern):
        '''Check if pattern has valid boundaries.'''
        type = pattern.type()

        # exception when only right boundary
        if (idx == 0):
            if (type == AkPatternType.NEGATIVE) and (self._list[idx + pattern.length()] == 1):
                return True

            if (type == AkPatternType.POSITIVE) and (self._list[idx + pattern.length()] == -1):
                return True
        # exception when only left boundary
        elif (idx == self.length() - pattern.length()):
            if (type == AkPatternType.NEGATIVE) and (self._list[idx - 1] > 0):
                return True

            if (type == AkPatternType.POSITIVE) and (self._list[idx - 1] < 0):
                return True
        else:
            if (type == AkPatternType.NEGATIVE) and (self._list[idx-1] > 0) and (self._list[idx + pattern.length()] == 1):
                return True

            if (type == AkPatternType.POSITIVE) and (self._list[idx-1] < 0) and (self._list[idx + pattern.length()] == -1):
                return True

        return False

    def max(self):
        '''Get Max el of sequence.'''
        return max(self._list)

    def min(self):
        '''Get Min el of sequence.'''
        minValue = self._list[0]
        for i in range(self.length()):
            if (self._list[i] < minValue) and (abs(self._list[i]) > 1):
                minValue = self._list[i]
        return minValue

    def length(self):
        '''Get length of sequence.'''
        return len(self._list)

class AkSeriality(object):
    def __init__(self, ohlcData, parent=None):
        self._ohlcData = ohlcData


        if (parent is not None):
            self._name = parent.name()
        else:
            self._name = ''

    #----------------------------------------------------------------------
    # Get methods
    # ---------------------------------------------------------------------

    def getSerialityIndexesDictionary(self):
        sequence = AkSequence(self.getSerialitySequenceList())

        indexesDictionary = {}
        for degree in range(sequence.min(), sequence.max() + 1):
            pattern = AkPattern(degree)
            indexes = sequence.patternIndexes(pattern)
            if (indexes):
                indexesDictionary[degree] = indexes

        return indexesDictionary

    def getSerialitySequenceList(self):
        rowCount = len(self._ohlcData)
        sequence = []

        diff = self._open_close_diff(0)
        if (diff > 0):
            sequence.append(1)
        elif (diff < 0):
            sequence.append(-1)
        else:
            sequence.append(0)

        for i in range(1, rowCount):
            if (self._open_close_diff(i) > 0):
                if (sequence[i - 1] > 0):
                    sequence.append(sequence[i - 1] + 1)
                elif (sequence[i - 1] <= 0):
                    sequence.append(1)

            if (self._open_close_diff(i) < 0):
                if (sequence[i - 1] >= 0):
                    sequence.append(-1)
                elif (sequence[i - 1] < 0):
                    sequence.append(sequence[i - 1] - 1)

            if (self._open_close_diff(i) == 0):
                sequence.append(0)

        return sequence

    def getInstrumentName(self):
        return self._name

    def getSerialityOHLCDictionary(self):
        indexesDict = self.getSerialityIndexesDictionary()

        ohlcDict = {}
        for degree in indexesDict.keys():
            ohlc = []
            for idx in indexesDict[degree]:
                for i in range(abs(degree)):  # use abs! because degree cat be negative value
                    ohlc.append(self._ohlcData[idx + i])
            ohlcDict[degree] = ohlc

        return ohlcDict

    def getSerialityStartDatesDictionary(self):
        indexesDict = self.getSerialityIndexesDictionary()

        datesDict = {}
        for degree in indexesDict.keys():
            dates = []
            for idx in indexesDict[degree]:
                dates.append(self._ohlcData[idx][0])
            datesDict[degree] = dates

        return datesDict

    def getSerialityQuantitiesDictionary(self):
        indexesDict = self.getSerialityIndexesDictionary()
        quantitiesDict = {}
        for degree in indexesDict.keys():
            quantitiesDict[degree] = len(indexesDict[degree])

        return quantitiesDict


    def writeToFile(self, pathFileName):
        serialityIndexes = self.getSerialityIndexesDictionary()
        with open(pathFileName, "w") as text_file:
            print("Instrument:", self.getInstrumentName(), file=text_file)
            print("Sequence: ", self.getSerialitySequenceList(), file=text_file)
            print("Min: ", min(serialityIndexes.keys()), file=text_file)
            print("Max: ", max(serialityIndexes.keys()), file=text_file)

            print("Quantities: ", self.getSerialityQuantitiesDictionary(), file=text_file)
            print("Degrees: ", serialityIndexes.keys(), file=text_file)
            print("Indexes Matrix: ", serialityIndexes, file=text_file)

            ohlcDictionary = self.getSerialityOHLCDictionary()
            datesDictionary = self.getSerialityStartDatesDictionary()

            print("", file=text_file)
            print("--------------------------------------------------", file=text_file)
            for degree in ohlcDictionary.keys():
                print("Seriality:", degree, file=text_file)
                print("Quantity:", len(serialityIndexes[degree]), file=text_file)
                print("Events start dates:", datesDictionary[degree], file=text_file)

                ohlcList = ohlcDictionary[degree]
                for i in range(len(ohlcList)):
                    print(ohlcList[i], file=text_file)
                print("", file=text_file)

    #----------------------------------------------------------------------
    # Private methods
    # ---------------------------------------------------------------------

    def _open_close_diff(self, idx):
        return float(self._ohlcData[idx][4]) - float(self._ohlcData[idx][1])


    def _calc_ohlc_dict(self):

        return ohlcDict

    def _calc_dates_dict(self):

        return datesDict

    def _calc_quantities_dict(self):

        return quantitiesDict

if __name__ == '__main__':

    str = [1,-1,-2,-3,-4,1,-1,1,-1,-2,-3,1,-1,1,-1,-2,-3,-4,1,2,3,4,5,6,-1,1,2,3,-1,1,-1,-2,-3,1,2,3,-1,-2,-3,1]
