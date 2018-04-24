from PyQt5 import QtWidgets
from src.views.ui_optionsView import Ui_OptionsDialog

class AkOptionsController(QtWidgets.QDialog, Ui_OptionsDialog):
    def __init__(self):
        super(AkOptionsController, self).__init__()
        self.setupUi(self)
        self.setModal(True)
        self.setWindowTitle("Options")
