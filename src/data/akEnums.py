from enum import Enum


class AkAnalysisType(Enum):
    """
    Клас представляє типи аналізів інструмента
    """

    Period = 'period.analysis'
    Calendar = 'calendar.analysis'
    Series = 'getSeriesList.analysis'
    Combinations = 'variants.analysis'


class AkSourceType(Enum):
    """
    Клас представляє типи вхідних даних.
    """

    D = 'Day'
    W = 'Week'
    M = 'Month'
    Q = 'Quarter'
    Y = 'Year'


class AkStructureType(Enum):
    """
    Клас представляє типи структур даних.
    """

    OHLC = 'OHLC'
    OLHC = 'OLHC'
    UN = 'UN'


class AkStructureSignType(Enum):
    Positive = 1
    Negative = -1
    Zero = 0


class AkCalculationMode(Enum):
    """
    Клас представляє типи обрахунків даних.
    """

    Points = 0
    Percent = 1


class AkSelectionMethod(Enum):
    """
    Тип амплітуди.

    Кожен стовпець має індекс мапінгу.
    D - 0
    O - 1
    H - 2
    L - 3
    C - 4
    """

    absOH = 121     # |High[i] - Open[i]|
    absHL = 231     # |Low[i] - High[i]|
    absLC = 341     # |Close[i] - Low[i]|

    absOL = 131     # |Low[i] - Open[i]|
    absHC = 241     # |Close[i] - High[i]|
    absOC = 141     # |Close[i] - Open[i]|

    OH = 120        # High[i] - Open[i]
    HL = 230        # Low[i] - High[i]
    LC = 340        # Close[i] - Low[i]

    OL = 130        # Low[i] - Open[i]
    LH = 320        # High[i] - Low[i]
    HC = 240        # Close[i] - High[i]

    OC = 140        # Close[i] - Open[i]
    CC = 440        # Close[i] - Close[i-1]
    GAP = 410       # Open[i] - Close[i-1]


class AkClasterSign(Enum):
    Positive = 1
    Negative = -1
    Zero = 0


class AkPatternType(Enum):
    POSITIVE = 1
    NEGATIVE = -1
