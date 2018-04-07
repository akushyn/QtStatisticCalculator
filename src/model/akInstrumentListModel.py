from PyQt5 import QtCore, QtGui

from src.model.akInstrument import AkInstrument


class AkInstrumentListModel(QtCore.QAbstractListModel):
    DEFAULT_NAME = "NAME_"

    def __init__(self, items = [], parent = None):
        super(AkInstrumentListModel, self).__init__(parent)
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
            return self._items[index.row()].name()

        if (role == QtCore.Qt.DisplayRole):
            row = index.row()
            value = self._items[row]
            return value.name()

        if (role == QtCore.Qt.EditRole):
            return self._items[index.row()].name()


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
        self._items[index].setData(data)
        #self.dataChanged.emit(index, index)

    def itemData(self, index):
        return self._items[index].data()

    def insertRows(self, position, rows, values = [], parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)

        if (not values):
            for i in range(rows):
                it = AkInstrument(self.DEFAULT_NAME, None)
                self._items.insert(position, it)
                self.setItemData(i, it.data())
        else:
            for i in range(rows):
                self._items.insert(position, values[i])
                self.setItemData(i, values[i].data())

        self.endInsertRows()


    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)

        for i in range(rows):
            it = self._items[position]
            self._items.remove(it)

        self.endRemoveRows()