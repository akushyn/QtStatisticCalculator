from PyQt5 import QtCore

from src.model.akTableModel import AkTableModel

class AkNotesModel(AkTableModel):
    def __init__(self):
        super(AkNotesModel, self).__init__(items = [['', '']], headers = ["Date", "Note"], parent=None)

    def flags(self, QModelIndex):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable