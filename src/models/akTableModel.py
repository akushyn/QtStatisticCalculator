from PyQt5 import QtCore, QtGui


class AkTableModel(QtCore.QAbstractTableModel):
    headers = ["Date", "Open", "High", "Low", "Close"]
    def __init__(self, name='', xData = [[]], headers = headers, parent = None):
        super(AkTableModel, self).__init__(parent)
        self._name = name
        self._x_data = xData
        self._headers = headers

    def name(self):
        return self._name

    def setName(self, name):
        self._name = name

    def headers(self):
        return self._headers

    def rowCount(self, parent=None):
        return len(self._x_data)

    def columnCount(self, parent=None):
        return len(self._x_data[0])

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
            return self._x_data[row][column]

        if (role == QtCore.Qt.DisplayRole):
            row = index.row()
            column = index.column()
            value = self._x_data[row][column]

            return value

        if (role == QtCore.Qt.EditRole):
            return self._x_data[index.row()][index.column()]

    def setData(self, index, value, role=None):

        if (role == QtCore.Qt.EditRole):
            row = index.row()
            column = index.column()
            self._x_data[row][column] = value
            self.dataChanged.emit(index, index)

            return True

        if (role == QtCore.Qt.DisplayRole):
            row = index.row()

        return False

    def insertRows(self, position, rows, values, parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)

        for i in range(rows):
            self._x_data.insert(position, values)

        self.endInsertRows()
        return True


    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)

        for i in range(rows):
            value = self._x_data[position]
            self._x_data.remove(value)

        self.endRemoveRows()
        return True

    def insertColumns(self, position, columns, parent=QtCore.QModelIndex()):
        self.beginInsertColumns(parent, position, position + columns - 1)

        rowCount = len(self._x_data)
        for i in range(columns):
            for j in range(rowCount):
                self._x_data[j].insert(position, QtGui.QColor("#000000"))

        self.endInsertColumns()
        return True

    def removeColumns(self, position, columns, parent=QtCore.QModelIndex()):
        self.beginRemoveColumns(parent, position, position + columns - 1)

        for i in range(columns):
            for row in self._x_data:
                del row[position]

        self.endRemoveColumns()

