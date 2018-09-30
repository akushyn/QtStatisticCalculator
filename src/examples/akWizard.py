from PyQt5 import QtWidgets

from src.views.ui_importWizardPage import Ui_Dialog


class AkWizardPage(QtWidgets.QWizardPage, Ui_Dialog):
    def __init__(self, parent=None):
        super(AkWizardPage, self).__init__(parent)
        self.setupUi(self)


class MagicWizard(QtWidgets.QWizard):
    def __init__(self, parent=None):
        super(MagicWizard, self).__init__(parent)
        self.addPage(AkWizardPage(self))
        self.addPage(Page2(self))
        self.setWindowTitle("Import Instrument Wizard")
        self.resize(640, 480)


class Page1(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(Page1, self).__init__(parent)
        self.setTitle("Select the option below to choose what would you like to do:")

        self.page = AkWizardPage()

        #self.comboBox.addItem("Python", "/path/to/filename1")
        #self.comboBox.addItem("PyQt5", "/path/to/filename2")

        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.page)
        self.setLayout(layout)


class Page2(QtWidgets.QWizardPage):
    def __init__(self, parent=None):
        super(Page2, self).__init__(parent)
        self.label1 = QtWidgets.QLabel()
        self.label2 = QtWidgets.QLabel()
        layout = QtWidgets.QVBoxLayout()
        layout.addWidget(self.label1)
        layout.addWidget(self.label2)
        self.setLayout(layout)

    def initializePage(self):
        self.label1.setText("Example text")
        self.label2.setText("Example text")


if __name__ == '__main__':
    import sys

    app = QtWidgets.QApplication(sys.argv)
    wizard = MagicWizard()
    wizard.show()
    sys.exit(app.exec_())