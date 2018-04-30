from PyQt5 import QtWidgets
from src.views.ui_importPreview import Ui_ImportPreview


class AkImportPreviewController(QtWidgets.QDialog, Ui_ImportPreview):
    def __init__(self):
        super(AkImportPreviewController, self).__init__()
        self.setupUi()

        self.setupConnections()
        self.setupModel()

    def setupUi(self):
        super(AkImportPreviewController, self).setupUi(self)

        self.setModal(True)
        self.setWindowTitle("Import Preview")


    def setupConnections(self):
        pass

    def setupModel(self):
        pass