from PyQt5 import QtWidgets
from src.views.ui_connectActionView import Ui_ConnectActionDialog


class AkConnectActionController(QtWidgets.QDialog, Ui_ConnectActionDialog):
    def __init__(self):
        super(AkConnectActionController, self).__init__()
        self.setupUi(self)
        self.setModal(True)
        self.setWindowTitle("Connect")

class AkDisconnectActionController(QtWidgets.QDialog, Ui_ConnectActionDialog):
    def __init__(self):
        super(AkDisconnectActionController, self).__init__()
        self.setupUi(self)
        self.setModal(True)
        self.setWindowTitle("Disconnect")
