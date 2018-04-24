from enum import Enum

class AkPatternEnum(Enum):
    POSITIVE = 1
    NEGATIVE = -1

class AkPattern(object):
    def __init__(self, degree):
        self._degree = degree
        self._list = self._set_list()
        self._type = self._set_type()

    def degree(self):
        return self._degree

    def type(self):
        return self._type

    def length(self):
        return len(self._list)

    def list(self):
        return self._list

    def _set_type(self):
        if (self._degree > 0):
            return AkPatternEnum.POSITIVE

        return AkPatternEnum.NEGATIVE

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
        return self._list

    def patternIndexes(self, pattern):
        # skip seriality length < 2
        if (pattern.degree() == 0) or (pattern.degree() == -1) or (pattern.degree() == 1):
            return []

        matches = []
        for i in range(self.length() - pattern.length() + 1):
            if self._list[i] == pattern.list()[0] and self._list[i:i + len(pattern.list())] == pattern.list():
                if (self._valid_boundaries(i, pattern)):
                    matches.append(i)
        return matches

    def _valid_boundaries(self, idx, pattern):
        type = pattern.type()

        # exception when only right boundary
        if (idx == 0):
            if (type == AkPatternEnum.NEGATIVE) and (self._list[idx + pattern.length()] == 1):
                return True

            if (type == AkPatternEnum.POSITIVE) and (self._list[idx + pattern.length()] == -1):
                return True
        # exception when only left boundary
        elif (idx == self.length() - pattern.length()):
            if (type == AkPatternEnum.NEGATIVE) and (self._list[idx - 1] > 0):
                return True

            if (type == AkPatternEnum.POSITIVE) and (self._list[idx - 1] < 0 ):
                return True
        else:
            if (type == AkPatternEnum.NEGATIVE) and (self._list[idx-1] > 0) and (self._list[idx + pattern.length()] == 1):
                return True

            if (type == AkPatternEnum.POSITIVE) and (self._list[idx-1] < 0) and (self._list[idx + pattern.length()] == -1):
                return True

        return False

    def max(self):
        return max(self._list)

    def min(self):
        minValue = self._list[0]
        for i in range(self.length()):
            if (self._list[i] < minValue) and (abs(self._list[i]) > 1):
                minValue = self._list[i]
        return minValue

    def length(self):
        return len(self._list)

class AkSeriality(object):
    def __init__(self, degree, items):
        self._degree = degree
        self._items = items

    def degree(self):
        return self._degree

    def indexes(self):
        return self._items

    def quantity(self):
        return len(self._items)

class AkSerialityIndexes():
    def __init__(self, indexes={}):
        self._indexes = indexes

    def degrees(self):
        '''
        Get a list of serialities. Degree can be positive or negative.

        Negative means, that its a bearish sequence of bars.
        Positive means, that its a bulish sequence of bars.
        :return: list[]
        '''
        return self._indexes.keys()

    def values(self):
        return self._indexes.values()

    def quantity(self, degree):
        return len(self._indexes[degree])

    def indexes(self, degree):
        '''Gets list of indexes by degree. Returns: list[]'''
        return self._indexes[degree]

    def max(self):
        return max(self._indexes.keys())

    def min(self):
        return min(self._indexes.keys())

    def matrix(self):
        return self._indexes

class AkSerialityDates(object):
    def __init__(self, dates):
        self._dates = dates

    def degrees(self):
        return self._dates.keys()

    def values(self):
        return self._dates.values()

    def dates(self, degree):
        return self._dates[degree]

class AkSerialityOHLC(object):
    def __init__(self, ohlc):
        self._ohlc = ohlc

    def degrees(self):
        return self._ohlc.keys()

    def values(self):
        return self._ohlc.values()

    def ohlc(self, degree):
        return self._ohlc[degree]


class AkSerialityInfo(object):
    def __init__(self, ohlc = None):
        self._sequence = None
        self._indexesMatrix = None
        self._instrumentName = ''
        self._ohlc = None
        self._dates = None

    def setIndexes(self, indexesMatrix):
        self._indexesMatrix = indexesMatrix

    def getIndexes(self):
        return self._indexesMatrix

    def setSequence(self, sequence):
        self._sequence = sequence

    def getSequence(self):
        return self._sequence

    def setInstrumentName(self, instrumentName):
        self._instrumentName = instrumentName

    def getInstrumentName(self):
        return self._instrumentName

    def setOHLC(self, ohlc):
        self._ohlc = ohlc

    def getOHLC(self):
        return self._ohlc

    def setDates(self, dates):
        self._dates = dates

    def getDates(self):
        return self._dates

    def quantities(self):
        quantities = {}
        for degree in self.degrees():
            quantities[degree] = self._indexesMatrix.quantity(degree)


if __name__ == '__main__':


    str = [1,-1,-2,-3,-4,1,-1,1,-1,-2,-3,1,-1,1,-1,-2,-3,-4,1,2,3,4,5,6,-1,1,2,3,-1,1,-1,-2,-3,1,2,3,-1,-2,-3,1]
    sequence = AkSequence(str)

    print("Min: ", sequence.min())
    print("Max: ", sequence.max())

    matrix = sequence.serialityIndexes()
    print("Seriality Matrix:", matrix)