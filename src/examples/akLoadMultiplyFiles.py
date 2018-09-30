from PyQt5 import QtCore, QtGui, QtWidgets

class FileDialog(QtWidgets.QFileDialog):
    def __init__(self, *args, **kwargs):
        super(FileDialog, self).__init__(*args, **kwargs)
        self.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)
        self.setFileMode(QtWidgets.QFileDialog.ExistingFiles)

    def accept(self):
        super(FileDialog, self).accept()

class Window(QtWidgets.QWidget):
    def __init__(self):
        super(Window, self).__init__()
        self.button = QtWidgets.QPushButton('Test', self)
        self.button.clicked.connect(self.handleButton)
        layout = QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.button)

    def handleButton(self):
        dialog = FileDialog()
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            print(dialog.selectedFiles())

if __name__ == '__main__':

    import sys
    app = QtWidgets.QApplication(sys.argv)
    window = Window()
    window.show()
    sys.exit(app.exec_())