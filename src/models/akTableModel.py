from PyQt5 import QtCore, QtGui

from src.data.akSeriality import AkSerialityInfo, AkSequence, AkSerialityIndexes, AkPattern, AkSerialityDates, \
    AkSerialityOHLC


class AkTableModel(QtCore.QAbstractTableModel):
    __defaultHeaders = ["Date", "Open", "High", "Low", "Close"]
    def __init__(self, name='', items = [[]], headers = __defaultHeaders, parent = None):
        super(AkTableModel, self).__init__(parent)
        self.__name = name
        self._items = items
        self.__headers = headers

    def getName(self):
        return self.__name

    def setName(self, name):
        self.__name = name

    def rowCount(self, parent=None):
        return len(self._items)

    def columnCount(self, parent=None):
        return len(self._items[0])

    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

    def headerData(self, section, orientation, role=None):
        if (role == QtCore.Qt.DisplayRole):
            if (orientation == QtCore.Qt.Horizontal):
                if (section < len(self.__headers)):
                    return self.__headers[section]
                else:
                    return "Not Defined"
            else:
                return QtCore.QVariant(section)

    def data(self, index, role=None):
        if (role == QtCore.Qt.ToolTipRole):
            row = index.row()
            column = index.column()
            return self._items[row][column]

        if (role == QtCore.Qt.DisplayRole):
            row = index.row()
            column = index.column()
            value = self._items[row][column]

            return value

        if (role == QtCore.Qt.EditRole):
            return self._items[index.row()][index.column()]

    def setData(self, index, value, role=None):

        if (role == QtCore.Qt.EditRole):
            row = index.row()
            column = index.column()
            self._items[row][column] = value
            self.dataChanged.emit(index, index)

            return True

        if (role == QtCore.Qt.DisplayRole):
            row = index.row()

        return False

    def insertRows(self, position, rows, values, parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)

        for i in range(rows):
            self._items.insert(position, values)

        self.endInsertRows()
        return True


    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)

        for i in range(rows):
            value = self._items[position]
            self._items.remove(value)

        self.endRemoveRows()
        return True

    def insertColumns(self, position, columns, parent=QtCore.QModelIndex()):
        self.beginInsertColumns(parent, position, position + columns - 1)

        rowCount = len(self._items)
        for i in range(columns):
            for j in range(rowCount):
                self._items[j].insert(position, QtGui.QColor("#000000"))

        self.endInsertColumns()
        return True

    def removeColumns(self, position, columns, parent=QtCore.QModelIndex()):
        self.beginRemoveColumns(parent, position, position + columns - 1)

        for i in range(columns):
            for row in self._items:
                del row[position]

        self.endRemoveColumns()

class AkInstrumentOHLCModel(AkTableModel):
    def __init__(self, name = '', items=[[]], headers=[], parent=None):
        super(AkInstrumentOHLCModel, self).__init__(name, items, headers, parent)
        self._items = items

    def distributionTable(self):
        print(self.getName())

    def filter(self, fromDate, toDate):
        position = -1
        rows = 0
        for i in range(self.rowCount()):
            date = QtCore.QDate.fromString(self._items[i][0], 'yyyy-MM-dd')
            if (date < fromDate):
                if (position == -1):
                    position = i
                rows+=1

        self.removeRows(position, rows)

        position = -1
        rows = 0
        for i in range(self.rowCount()):
            date = QtCore.QDate.fromString(self._items[i][0], 'yyyy-MM-dd')
            if (date > toDate):
                if (position == -1):
                    position = i
                rows+=1

        self.removeRows(position, rows)

    def getSequence(self):
        rowCount = self.rowCount()
        seq = []

        diff = self._open_close_diff(0)
        if (diff > 0):
            seq.append(1)
        elif (diff < 0):
            seq.append(-1)
        else:
            seq.append(0)

        for i in range(1, rowCount):
            if (self._open_close_diff(i) > 0):
                if (seq[i - 1] > 0):
                    seq.append(seq[i - 1] + 1)
                elif (seq[i - 1] <= 0):
                    seq.append(1)

            if (self._open_close_diff(i) < 0):
                if (seq[i - 1] >= 0):
                    seq.append(-1)
                elif (seq[i - 1] < 0):
                    seq.append(seq[i - 1] - 1)

            if (self._open_close_diff(i) == 0):
                seq.append(0)

        return AkSequence(seq)


    def _open_close_diff(self, idx):
        return float(self._items[idx][4]) - float(self._items[idx][1])

    def getSerialityIndexes(self):
        sequence = self.getSequence()

        indexesDictionary = {}
        for degree in range(sequence.min(), sequence.max() + 1):
            pattern = AkPattern(degree)
            indexes = sequence.patternIndexes(pattern)
            if (indexes):
                indexesDictionary[degree] = indexes

        return AkSerialityIndexes(indexesDictionary)

    def getSerialityOHLC(self):
        serialityIndexes = self.getSerialityIndexes()

        ohlcDictionary = {}
        for degree in serialityIndexes.degrees():
            ohlc = []
            for idx in serialityIndexes.indexes(degree):
                for i in range(abs(degree)):  # use abs! because degree cat be negative value
                    ohlc.append(self._items[idx + i])
            ohlcDictionary[degree] = ohlc

        return AkSerialityOHLC(ohlcDictionary)

    def getSerialityDates(self):
        serialityIndexes = self.getSerialityIndexes()

        datesDictionary = {}
        for degree in serialityIndexes.degrees():
            datesList = []
            indexes = serialityIndexes.indexes(degree)
            for idx in indexes:
                datesList.append(self._items[idx][0])
            datesDictionary[degree] = datesList

        return AkSerialityDates(datesDictionary)

    def getSerialityInfo(self):
        info = AkSerialityInfo()

        info.setSequence(self.getSequence())
        info.setIndexes( self.getSerialityIndexes())
        info.setInstrumentName(self.getName())
        info.setOHLC(self.getSerialityOHLC())
        info.setDates(self.getSerialityDates())

        return info

class AkNotesModel(AkTableModel):
    def __init__(self):
        super(AkNotesModel, self).__init__(items = [['', '']], headers = ["Date", "Note"], parent=None)

    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable

class AkDistributionsModel(AkTableModel):
    def __init__(self):
        super(AkDistributionsModel, self).__init__(items=[[]], headers=['HL', 'OH', 'OL', 'HC', 'LC'])