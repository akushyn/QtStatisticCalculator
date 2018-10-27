from PyQt5 import QtCore

class AkInstrumentListModel(QtCore.QAbstractListModel):
    """
    Instrument list model - list of instruments.
    """

    def __init__(self, instruments = [], parent = None):
        super(AkInstrumentListModel, self).__init__(parent)
        self._instruments = instruments

    def rowCount(self, parent=QtCore.QModelIndex()):
        return len(self._instruments)

    def headerData(self, section, orientation, role=None):
        if (role == QtCore.Qt.DisplayRole):
            if (orientation == QtCore.Qt.Vertical):
                return "Instruments"
            else:
                return QtCore.QVariant(section)

    def data(self, index, role=None):
        if (role == QtCore.Qt.ToolTipRole) or (role == QtCore.Qt.DisplayRole) or (role == QtCore.Qt.EditRole):
            return self._instruments[index.row()].name

    def flags(self, QModelIndex):
        return QtCore.Qt.ItemIsEditable | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled

    def setData(self, index, value, role=QtCore.Qt.EditRole):

        if (role == QtCore.Qt.EditRole):
            row = index.row()

            self._instruments[row].name = value
            self.dataChanged.emit(index, index)
            return True

        if (role == QtCore.Qt.DisplayRole):
            row = index.row()

        return False

    def itemData(self, index):
        return self._instruments[index.row()]

    def insertRows(self, position, rows, instruments = [], parent=QtCore.QModelIndex()):
        self.beginInsertRows(parent, position, position + rows - 1)

        for i in range(rows):
            self._instruments.insert(position, instruments[i])

        self.endInsertRows()


    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        self.beginRemoveRows(parent, position, position + rows - 1)

        for i in range(rows):
            inst = self._instruments[position].modelReset()
            self._instruments.remove(inst)

        self.endRemoveRows()