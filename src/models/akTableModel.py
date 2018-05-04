from PyQt5 import QtCore, QtGui
from src.data.akAmplitudeDictionary import AkAmplitudeDictionary
from src.data.akSeriality import AkSeriality

class AkTableModel(QtCore.QAbstractTableModel):
    __defaultHeaders = ["Date", "Open", "High", "Low", "Close"]
    def __init__(self, name='', items = [[]], headers = __defaultHeaders, parent = None):
        super(AkTableModel, self).__init__(parent)
        self.__name = name
        self._items = items
        self._headers = headers

    def name(self):
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
                if (section < len(self._headers)):
                    return self._headers[section]
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

class AkInstrumentTableModel(AkTableModel):
    def __init__(self, name = '', items=[[]], headers=[], parent=None):
        super(AkInstrumentTableModel, self).__init__(name, items, headers, parent)
        self._items = items

        self._seriality = AkSeriality(ohlcData=items, parent=self)
        self._amplitude = AkAmplitudeDictionary(ohlcData=items, parent=self)
        #self._amplitude = AkAmplitude(self.name(), items)

    def distributionTable(self):
        print(self.name())

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

    def getSeriality(self):
        return self._seriality


    def exportToFile(self, pathFileName=''):
        fileName = 'export_' + pathFileName + self.name() + '.txt'
        seriality = self.getSeriality()
        serialityIndexes =  seriality.getSerialityIndexesDictionary()

        ohlcDictionary = seriality.getSerialityOHLCDictionary()
        datesDictionary = seriality.getSerialityStartDatesDictionary()

        with open(fileName, "w") as text_file:
            print("Instrument:", self.name(), file=text_file)
            print("----------------------------------------------------------------------------------------------------", file=text_file)
            print("Sequence: ", seriality.getSerialitySequenceList(), file=text_file)
            print("Min: ", min(serialityIndexes.keys()), file=text_file)
            print("Max: ", max(serialityIndexes.keys()), file=text_file)

            print("Quantities: ", seriality.getSerialityQuantitiesDictionary(), file=text_file)
            print("Degrees: ", serialityIndexes.keys(), file=text_file)
            print("Indexes Matrix: ", serialityIndexes, file=text_file)

            print('', file=text_file)
            print("----------------------------------------------------------------------------------------------------", file=text_file)
            for degree in ohlcDictionary.keys():
                print("Seriality:", degree, file=text_file)
                print("Quantity:", len(serialityIndexes[degree]), file=text_file)
                print("Events start dates:", datesDictionary[degree], file=text_file)
                print('', file=text_file)
                ohlcTable = ohlcDictionary[degree]
                print("OHLC Data: ", file=text_file)
                for i in range(len(ohlcTable)):
                    print(ohlcTable[i], file=text_file)
                print('', file=text_file)

                amplitudeDict = AkAmplitudeDictionary(ohlcTable)
                amplitudes = amplitudeDict.amplitudes()
                print("Amplitudes: ", file=text_file)

                for key in amplitudes.keys():
                    print(key, amplitudes[key], file=text_file)

                print("----------------------------------------------------------------------------------------------------", file=text_file)




class AkNotesTableModel(AkTableModel):
    def __init__(self):
        super(AkNotesTableModel, self).__init__(items = [['', '']], headers = ["Date", "Note"], parent=None)

    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable

class AkDistributionsModel(AkTableModel):
    def __init__(self):
        super(AkDistributionsModel, self).__init__(items=[[]], headers=['HL', 'OH', 'OL', 'HC', 'LC'])