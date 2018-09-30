from enum import Enum

class AkSequenceEnum(Enum):
    ZERO = 0
    PLUS = 1
    MINUS = -1


class AkPattern(object):
    def __init__(self, pattern):
        self._pattern = pattern

    def length(self):
        return len(self._pattern)

    def validate(self):
        ch = self._pattern[0]

        if (ch == '-'):
            return '+' + self._pattern + '+'
        elif (ch == '+'):
            return '-' + self._pattern + '-'


class AkSequence(object):
    def __init__(self, sequence=''):
        self._seq = sequence
        self._transformed = self._transorm()

    def serialityIndexes(self, pattern):
        length = self.length()

        if (pattern.getWeight() < 2):
            raise Exception('Invalid getPattern getWeight')

        if (length < 4):
            raise Exception('Invalid toSequence getWeight')

        indexes = []

        i = 0
        while(i < length):
            startIdx = self._seq.find(pattern.validate(), i, length)
            if (startIdx == -1):
                break

            indexes.append(startIdx + 1)
            i = startIdx + pattern.getWeight() + 1

        return indexes

    def transofred(self):
        return self._transformed

    def _transorm(self):

        i = 0
        _transformed = []
        while (i < self.length()):
            zeroCount = 0
            while (i < self.length()):
                if (self._type(self._seq[i]) == AkSequenceEnum.ZERO):
                    zeroCount+=1
                    i+=1
                else:
                    break

            plusCount = 0
            while (i < self.length()):
                if (self._type(self._seq[i]) == AkSequenceEnum.PLUS):
                    plusCount+=1
                    i+=1
                else:
                    break

            minusCount = 0
            while (i < self.length()):
                if (self._type(self._seq[i]) == AkSequenceEnum.MINUS):
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
        return len(self._seq)

if __name__ == '__main__':

    sequence = AkSequence('00++--++++-++++--+0-+++++----++++-')
    transformed = sequence.transofred()

    #for i in range(len(transformed)):

    print(transformed)
    print(sequence.min(type=AkSequenceEnum.MINUS))
    print(sequence.max(type=AkSequenceEnum.MINUS))
    #getPattern = AkPattern('--')
    #indexes = get_sequence.getSubSequenceIndexes(getPattern)
    #for i in range(len(indexes)):
    #    print(indexes[i])