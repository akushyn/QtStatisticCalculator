from PyQt5 import QtWidgets
from src.view.ui_connectActionView import Ui_Dialog

class AkConnectActionController(QtWidgets.QDialog):
    def __init__(self):
        super(AkConnectActionController, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setModal(True)
        self.setWindowTitle("Connect")
        self.show()