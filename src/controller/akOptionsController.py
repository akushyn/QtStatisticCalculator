from PyQt5 import QtWidgets
from src.view.ui_optionsView import Ui_Dialog

class AkOptionsController(QtWidgets.QDialog):
    def __init__(self):
        super(AkOptionsController, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setModal(True)
        self.setWindowTitle("Options")
        #self.show()