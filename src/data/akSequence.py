from enum import Enum

class AkSequenceEnum(Enum):
    ZERO = 0
    PLUS = 1
    MINUS = -1


class AkPattern(object):
    def __init__(self, type, power):
        self._type = type
        self._power = power
        self._text = self._set_text()


    def length(self):
        return len(self._text)

    def _set_text(self):
        if (self._type == AkSequenceEnum.MINUS):
            s = ''
            for i in range(self._power):
                s = s + '-'
            return s
        elif (self._type == AkSequenceEnum.PLUS):
            s = ''
            for i in range(self._power):
                s = s + '+'
            return s

    def text(self):
        return self._text

    def validate(self):
        if (self._type == AkSequenceEnum.MINUS):
            return '+' + self._text + '+'
        elif (self._type == AkSequenceEnum.PLUS):
            return '-' + self._text + '-'


class AkSequence(object):
    def __init__(self, sequence=''):
        self._sequence = sequence
        self._transformed = self._transorm()

    def text(self):
        return self._sequence

    def serialityIndexMatrixes(self):

        plusMatrix = []
        for i in range(self.min(AkSequenceEnum.PLUS), self.max(AkSequenceEnum.PLUS) + 1):
            pattern = AkPattern(AkSequenceEnum.PLUS, i)
            indexes = self.patternIndexes(pattern)
            if (indexes):
                plusMatrix.append(indexes)

        minusMatrix = []
        for i in range(self.min(AkSequenceEnum.MINUS), self.max(AkSequenceEnum.MINUS) + 1):
            pattern = AkPattern(AkSequenceEnum.MINUS, i)
            indexes = self.patternIndexes(pattern)
            if (indexes):
                minusMatrix.append(indexes)

        return plusMatrix, minusMatrix

    # Get the list of indexes for the spicified pattern
    def patternIndexes(self, pattern):
        length = self.length()

        if (pattern.length() < 2):
            raise Exception('Invalid pattern length')

        if (length < 4):
            raise Exception('Invalid sequence length')

        indexes = []

        i = 0
        while(i < length):
            startIdx = self._sequence.find(pattern.validate(), i, length)
            if (startIdx == -1):
                break

            indexes.append(startIdx + 1)
            i = startIdx + pattern.length() + 1

        return indexes

    def transofred(self):
        return self._transformed

    def _transorm(self):

        i = 0
        _transformed = []
        while (i < self.length()):
            zeroCount = 0
            while (i < self.length()):
                if (self._type(self._sequence[i]) == AkSequenceEnum.ZERO):
                    zeroCount+=1
                    i+=1
                else:
                    break

            plusCount = 0
            while (i < self.length()):
                if (self._type(self._sequence[i]) == AkSequenceEnum.PLUS):
                    plusCount+=1
                    i+=1
                else:
                    break

            minusCount = 0
            while (i < self.length()):
                if (self._type(self._sequence[i]) == AkSequenceEnum.MINUS):
                    minusCount+=1
                    i+=1
                else:
                    break

            #if (zeroCount > 0):
            #    _transformed.append('z')

            if (plusCount > 0):
                _transformed.append(plusCount)

            if (minusCount > 0):
                _transformed.append(0-minusCount)

        return _transformed

    def _type(self, ch):
        if (ch == '+'):
            return AkSequenceEnum.PLUS
        elif (ch == '-'):
            return AkSequenceEnum.MINUS
        else:
            return AkSequenceEnum.ZERO

    def max(self, type=AkSequenceEnum.PLUS):
        if (type == AkSequenceEnum.PLUS):
            return max(self._transformed)
        elif (type == AkSequenceEnum.MINUS):
            maxValue = 0
            for i in range(len(self._transformed)):
                # skip '+' numbers
                if (self._transformed[i] > 0):
                    continue
                else:
                    if (abs(self._transformed[i]) > maxValue):
                        maxValue = abs(self._transformed[i])
            return maxValue

        return max(self._transformed)

    def min(self, type=AkSequenceEnum.PLUS, minFrom=2):
        if (type == AkSequenceEnum.MINUS):
            minValue = abs(min(self._transformed))
            for i in range(len(self._transformed)):
                if (self._transformed[i] > 0 ):
                    continue
                else:
                    if (abs(self._transformed[i]) < abs(minValue)) & (abs(self._transformed[i]) >= minFrom):
                        minValue = abs(self._transformed[i])
            return minValue

        elif (type == AkSequenceEnum.PLUS):
            minValue = max(self._transformed)
            for i in range(len(self._transformed)):
                # skip '-' numbers
                if (self._transformed[i] < 0):
                    continue
                else:
                    if (self._transformed[i] < minValue) & (self._transformed[i] >= minFrom):
                        minValue = self._transformed[i]
            return minValue


    def length(self):
        return len(self._sequence)

if __name__ == '__main__':

    sequence = AkSequence('00-++--++---++-++++--+0-+++++----++++-')

    print(sequence.text())
    print(sequence.transofred())

    plusMatrix, minusMatrix = sequence.serialityIndexMatrixes()
    print("Plus Matrix:", plusMatrix)
    print("Minus Matrix:", minusMatrix)