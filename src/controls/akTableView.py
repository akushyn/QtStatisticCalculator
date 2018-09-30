from PyQt5 import QtWidgets, QtCore

class AkTableView(QtWidgets.QTableView):
    def __init__(self, parent):
        super(AkTableView, self).__init__(parent)

        self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.OnPopupMenu_Handler)

        self.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def OnPopupMenu_Handler(self, position):
        pass
        #menu = QtWidgets.QMenu()
        #removeSelectedItems = menu.addAction("Remove selected")
        #action = menu.exec_(self.mapToGlobal(position))

        #if (action == removeSelectedItems):
        #    self.OnRemoveSelected_Handler()

    def OnRemoveSelected_Handler(self):
        indexes = self.selectionModel().selectedRows()
        if (indexes):
            pos = indexes[0].row()
            rows = len(indexes)
            self.model().removeRows(pos, rows)

    def OnTable_clickHandler(self, index):
        print('clicked')
