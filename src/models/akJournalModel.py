from PyQt5 import QtCore

from src.models.akTableModel import AkTableModel


class AkJournalModel(AkTableModel):
    def __init__(self):
        super(AkJournalModel, self).__init__(xData= [['', '']], headers = ["Date", "Note"], parent=None)

    def flags(self, index):
        return QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsEditable
