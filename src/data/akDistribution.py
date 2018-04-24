from statistics import median
from enum import Enum

class AkDistributionType(Enum):
    HL = 0
    LH = 1
    OH = 2
    OL = 3
    HC = 4
    LC = 5

class AkDistribution(object):
    def __init__(self, type, distribution):
        self._type = type
        self._distribution = distribution

    def values(self):
        return self._distribution

    def type(self):
        return self._type

    def max(self):
        return max(self._distribution)

    def min(self):
        return min(self._distribution)

    def median(self):
        return median(self._distribution)


if __name__ == '__main__':

    distr = AkDistribution(AkDistributionType.HC, [5, 2, 3, 8, 9, -2])
    print(distr.median())
    print(distr.max())
    print(distr.min())