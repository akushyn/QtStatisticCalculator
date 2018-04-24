from PyQt5 import QtWidgets
from src.views.ui_connectionsView import Ui_ConnectionsDialog


class AkConnectionsController(QtWidgets.QDialog, Ui_ConnectionsDialog):
    def __init__(self):
        super(AkConnectionsController, self).__init__()
        self.setupUi(self)
        self.setModal(True)
        self.setWindowTitle("Setup Connection")

    def doSmth(self):
        pass