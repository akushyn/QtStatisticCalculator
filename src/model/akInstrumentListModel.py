from PyQt5 import QtCore, QtGui

class AkNameListModel(QtCore.QAbstractListModel):
    DEFAULT_NAME = "NAME_"

    def __init__(self, names = [], parent = None):
        super(AkNameListModel, self).__init__(parent)
        self.names = names

    def rowCount(self, parent):
        return len(self.names)

    def headerData(self, section, orientation, role=None):
        if (role == QtCore.Qt.DisplayRole):
            if (orientation == QtCore.Qt.Horizontal):
                return QtCore.QVariant(section)#QtCore.QVariant("Pallete")
            else:
                return QtCore.QVariant(section)

    def data(self, index, role=None):
        if (role == QtCore.Qt.ToolTipRole):
            return "Hex code:" + self.names[index.row()]

        if (role == QtCore.Qt.DisplayRole):
            row = index.row()
            value = self.names[row]
            return value

        if (role == QtCore.Qt.EditRole):
            return self.names[index.row()]


    def flags(self, QModelIndex):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

    def setData(self, index, value, role=QtCore.Qt.EditRole):

        if (role == QtCore.Qt.EditRole):
            row = index.row()

            self.names[row] = value
            self.dataChanged.emit(index, index)
            return True

        if (role == QtCore.Qt.DisplayRole):
            row = index.row()

        return False

    def insertRows(self, position, rows, values = [], parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)

        if (not values):
            for i in range(rows):
                self.names.insert(position, self.DEFAULT_NAME + str(i))
        else:
            for i in range(rows):
                self.names.insert(position, values[i])

        self.endInsertRows()


    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)

        for i in range(rows):
            value = self.names[position]
            self.names.remove(value)

        self.endRemoveRows()
