from statistics import median
from enum import Enum
import math
from decimal import Decimal

class AkClasterType(Enum):
    OHLC = 0
    OLHC = 1
    All = 2

class AkCalculationMode(Enum):
    Points = 0
    Logarithm = 1

class AkAmplitudeDictionary(object):
    def __init__(self, ohlcData, parent=None):
        self._ohlcData = ohlcData
        self._name = ''
        self._dates = []

        if (parent is not None):
            self._name = parent.getName()

    def getName(self):
        return self._name

    def _calc_amplitude_dict(self, calculationMode=AkCalculationMode.Points, clasterType=AkClasterType.All, digits=2):
        if (self._ohlcData is None):
            return {}

        amplitudes = {}

        HL = []
        OH = []
        LC = []
        LH = []
        OL = []
        HC = []
        self._dates.clear()

        for i in range(len(self._ohlcData)):
            self._dates.append(self._ohlcData[i][0])

            if (calculationMode == AkCalculationMode.Points):
                # HL < 0
                HL.append(round(float(self._ohlcData[i][2]) - float(self._ohlcData[i][3]), digits) )   # HL
                OH.append(round(float(self._ohlcData[i][2]) - float(self._ohlcData[i][1]), digits))   # OH
                LC.append(round(float(self._ohlcData[i][4]) - float(self._ohlcData[i][3]), digits))   # LC

                # HL > 0
                LH.append(round(float(self._ohlcData[i][2]) - float(self._ohlcData[i][3]), digits))   # LH
                OL.append(round(float(self._ohlcData[i][1]) - float(self._ohlcData[i][3]), digits))   # OL
                HC.append(round(float(self._ohlcData[i][2]) - float(self._ohlcData[i][4]), digits))   # HC

            else:
                # HL < 0
                HL.append(round(math.log(float(self._ohlcData[i][2]) / float(self._ohlcData[i][3])), digits)) # HL
                OH.append(round(math.log(float(self._ohlcData[i][2]) / float(self._ohlcData[i][1])), digits)) # OH
                LC.append(round(math.log(float(self._ohlcData[i][4]) / float(self._ohlcData[i][3])), digits)) # LC

                # HL > 0
                LH.append(round(math.log(float(self._ohlcData[i][2]) / float(self._ohlcData[i][3])), digits)) # LH
                OL.append(round(math.log(float(self._ohlcData[i][1]) / float(self._ohlcData[i][3])), digits)) # OL
                HC.append(round(math.log(float(self._ohlcData[i][2]) / float(self._ohlcData[i][4])), digits)) # HC


        amplitudes['HL'] = HL
        amplitudes['OH'] = OH
        amplitudes['LC'] = LC

        amplitudes['LH'] = LH
        amplitudes['OL'] = OL
        amplitudes['HC'] = HC

        # OHLC
        if (clasterType == AkClasterType.OHLC):
            return {'HL': HL, 'OH': OH, 'LC': LC}

        # OLHC
        elif (clasterType == AkClasterType.OLHC):
            return {'LH': LH, 'OL': OL, 'HC': HC}

        # All
        return amplitudes


    def amplitudes(self, calculationMode=AkCalculationMode.Points, clasterType=AkClasterType.All, digits=2):
        return self._calc_amplitude_dict(calculationMode, clasterType, digits)

    def dates(self):
        return self._dates

if __name__ == '__main__':
    pass
