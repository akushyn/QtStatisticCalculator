from enum import Enum

class AkInstrument(object):
    def __init__(self, name='', dSeries=[], wSeries=[], mSeries=[], qSeries=[], ySeries=[]):
        self._name = name
        self._dSeries = dSeries
        self._wSeries = wSeries
        self._mSeries = mSeries
        self._qSeries = qSeries
        self._ySeries = ySeries

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name

    def data(self):
        return self._data

    def setData(self, data):
        self._data = data

class AkNode(object):
    def __init__(self, name, parent=None):
        self._name = name
        self._children = []
        self._parent = parent

        if (parent is not None):
            parent.addChild(self)

    def addChild(self, child):
        self._children.append(child)

    def getName(self):
        return self._name

    def getChild(self, row):
        return self._children[row]

    def getChildCount(self):
        return len(self._children)

    def getParent(self):
        return self._parent

    def getRow(self):
        if (self._parent is not None):
            return self._parent._children.index(self)


    def log(self, tabLevel=-1):
        output = ""
        tabLevel += 1

        for i in range(tabLevel):
            output += "\t"

        output += "|---" + self._name + "\n"

        for child in self._children:
            output += child.log(tabLevel)

        tabLevel -= 1
        output += "\n"

        return output

    def __repr__(self):
        return self.log()

class AkSerialityType(Enum):
    Compact = 1
    Stretch = 2

class AkSeriality(object):
    def __init__(self, sequence=[], type=AkSerialityType.Compact):
        self._sequence = sequence
        self._type = type

    def findPattern(self, pattern):
        
        str = '+-0++-+++0-'
