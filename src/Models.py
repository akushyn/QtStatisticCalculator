from PyQt5 import QtCore, QtGui

class AkListModel(QtCore.QAbstractListModel):
    DEFAULT_NAME = "NAME_"

    def __init__(self, items = [], parent = None):
        super(AkListModel, self).__init__(parent)
        self._items = items

    def rowCount(self, parent):
        return len(self._items)

    def headerData(self, section, orientation, role=None):
        if (role == QtCore.Qt.DisplayRole):
            if (orientation == QtCore.Qt.Horizontal):
                return QtCore.QVariant(section)#QtCore.QVariant("Pallete")
            else:
                return QtCore.QVariant(section)

    def data(self, index, role=None):
        if (role == QtCore.Qt.ToolTipRole):
            return self._items[index.row()].getName()

        if (role == QtCore.Qt.DisplayRole):
            return self._items[index.row()].getName()

        if (role == QtCore.Qt.EditRole):
            return self._items[index.row()].getName()


    def flags(self, QModelIndex):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

    def setData(self, index, value, role=QtCore.Qt.EditRole):

        if (role == QtCore.Qt.EditRole):
            row = index.row()

            self._items[row].setName(value)
            self.dataChanged.emit(index, index)
            return True

        if (role == QtCore.Qt.DisplayRole):
            row = index.row()

        return False

    def setItemData(self, index, data, p_int=None, Any=None):
        self._items[index] = data
        #self._items[index].dataChanged.emit(index, index)

    def itemData(self, index):
        return self._items[index.row()]

    def distributionModel(self, index):
        if (index.isValid()):
            print(index.parent())

        self._items[index.row()].distributionModel()

        #distr = [[]]
        #rowCount = self.rowCount()
        #for i in range(rowCount):
        #    # O=1, H=2, L=3, C=4
        #    distr[0].append(float(self[i][2]) - float(ohlc[i][3]))  # HL
        #    distr[1].append(float(ohlc[i][2]) - float(ohlc[i][1]))  # OH
        #    distr[2].append(float(ohlc[i][1]) - float(ohlc[i][3]))  # OL
        #    distr[3].append(float(ohlc[i][2]) - float(ohlc[i][4]))  # HC
        #    distr[4].append(float(ohlc[i][4]) - float(ohlc[i][3]))  # LC
        #return AkTableModel(self.getName(), distr, ['HL', 'OH', 'OL', 'HC', 'LC'])

    def insertRows(self, position, rows, values = [], parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)

        if (not values):
            for i in range(rows):
                it = AkTableModel(self.DEFAULT_NAME)
                self._items.insert(position, it)
                self.setItemData(i, it.data())
        else:
            for i in range(rows):
                self._items.insert(position, values[i])
                self.setItemData(i, values[i])

        self.endInsertRows()


    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)

        for i in range(rows):
            it = self._items[position].modelReset()
            self._items.remove(it)

        self.endRemoveRows()

class AkTableModel(QtCore.QAbstractTableModel):
    __defaultHeaders = ["Date", "Open", "High", "Low", "Close"]
    def __init__(self, name='', items = [[]], headers = __defaultHeaders, parent = None):
        super(AkTableModel, self).__init__(parent)
        self.__name = name
        self.__items = items
        self.__headers = headers

    def getName(self):
        return self.__name

    def setName(self, name):
        self.__name = name

    def rowCount(self, parent=None):
        return len(self.__items)

    def columnCount(self, parent=None):
        return len(self.__items[0])

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
            return self.__items[row][column]

        if (role == QtCore.Qt.DisplayRole):
            row = index.row()
            column = index.column()
            value = self.__items[row][column]

            return value

        if (role == QtCore.Qt.EditRole):
            return self.__items[index.row()][index.column()]

    def setData(self, index, value, role=None):

        if (role == QtCore.Qt.EditRole):
            row = index.row()
            column = index.column()
            self.__items[row][column] = value
            self.dataChanged.emit(index, index)

            return True

        if (role == QtCore.Qt.DisplayRole):
            row = index.row()

        return False

    def insertRows(self, position, rows, values, parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)

        for i in range(rows):
            self.__items.insert(position, values)

        self.endInsertRows()
        return True


    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)

        for i in range(rows):
            value = self.__items[position]
            self.__items.remove(value)

        self.endRemoveRows()
        return True

    def modelReset(self):
        self.beginResetModel()

        rowCount = self.rowCount()
        self.removeRows(0, rowCount)
        #self.insertRows(0, 1, ['','','','',''])

        self.endResetModel()

    def insertColumns(self, position, columns, parent=QtCore.QModelIndex()):
        self.beginInsertColumns(parent, position, position + columns - 1)

        rowCount = len(self.__items)
        for i in range(columns):
            for j in range(rowCount):
                self.__items[j].insert(position, QtGui.QColor("#000000"))

        self.endInsertColumns()
        return True

    def removeColumns(self, position, columns, parent=QtCore.QModelIndex()):
        self.beginRemoveColumns(parent, position, position + columns - 1)

        for i in range(columns):
            for row in self.__items:
                del row[position]

        self.endRemoveColumns()

    def distributionModel(self):
        print(self.getName())

        #dist = [[]]

        #for i in range()

    def filter(self, fromDate, toDate):
        position = -1
        rows = 0
        for i in range(self.rowCount()):
            date = QtCore.QDate.fromString(self.__items[i][0], 'yyyy-MM-dd')
            if (date < fromDate):
                if (position == -1):
                    position = i
                rows+=1

        self.removeRows(position, rows)

        position = -1
        rows = 0
        for i in range(self.rowCount()):
            date = QtCore.QDate.fromString(self.__items[i][0], 'yyyy-MM-dd')
            if (date > toDate):
                if (position == -1):
                    position = i
                rows+=1

        self.removeRows(position, rows)


class AkNotesTableModel(AkTableModel):
    def __init__(self):
        super(AkNotesTableModel, self).__init__(items = [['', '']], headers = ["Date", "Note"], parent=None)

    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable


class AkDistributionsModel(AkTableModel):
    def __init__(self):
        super(AkDistributionsModel, self).__init__(items=[[]], headers=['HL', 'OH', 'OL', 'HC', 'LC'])