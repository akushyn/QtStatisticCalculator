from PyQt5 import QtCore, QtGui

class AkInstrumentDataTableModel(QtCore.QAbstractTableModel):
    defaultHeaders = ["Date", "Open", "High", "Low", "Close"]
    def __init__(self, items = [[]], headers = defaultHeaders, parent = None):
        super(AkInstrumentDataTableModel, self).__init__(parent)
        self.__items = items
        self.__headers = headers


    def rowCount(self, parent):
        return len(self.__items)

    def columnCount(self, parent=None):
        return len(self.__items[0])

    def flags(self, QModelIndex):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

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
            color = QtGui.QColor(value)

            if (color.isValid()):
                self.__items[row][column] = color
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
