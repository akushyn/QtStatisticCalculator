from PyQt5 import QtWidgets
from src.view.ui_connectActionView import Ui_Dialog

class AkDisconnectActionController(QtWidgets.QDialog):
    def __init__(self):
        super(AkDisconnectActionController, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setModal(True)
        self.setWindowTitle("Disconnect")
        self.show()