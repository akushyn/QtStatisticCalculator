from PyQt5 import QtWidgets, uic
from src.view.ui_connectionsView import Ui_Dialog

class AkConnectionsController(QtWidgets.QDialog):
    def __init__(self):
        super(AkConnectionsController, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setModal(True)
        self.setWindowTitle("Setup Connection")
        self.show()

    def doSmth(self):
        pass