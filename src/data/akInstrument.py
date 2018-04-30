from enum import Enum
from src.data.akNode import AkNode

class AkSectionType(Enum):
    DAY     = 0
    WEEK    = 1
    MONTH   = 2
    QUARTER = 3
    YEAR    = 4

class AkInstrument(AkNode):
    def __init__(self, name, data=None, parent=None):
        super(AkInstrument, self).__init__(name, parent)

        self._daySection = AkSection("Day", self)
        self._weekSection = AkSection("Week", self)
        self._monthSection = AkSection("Month", self)
        self._quarterSection = AkSection("Quarter", self)

class AkSection(AkNode):
    def __init__(self, name, parent=None):
        super(AkSection, self).__init__(name, parent)

class AkPeriod(AkNode):
    def __init__(self, name, sector=None, data=[[]], parent=None):
        super(AkPeriod,self).__init__(name, parent)


