from PyQt5 import QtWidgets

from src.models.akTableModel import AkInstrumentTableModel


class AkTreeView(QtWidgets.QTreeView):
    def __init__(self, parent):
        super(AkTreeView, self).__init__(parent)

        self.clicked.connect(self.OnTreeView_clickHandler)

    def OnTreeView_clickHandler(self, index):
        pass