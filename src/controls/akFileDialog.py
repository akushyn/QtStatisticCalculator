from PyQt5 import QtWidgets

class AkFileDialog(QtWidgets.QFileDialog):
    def __init__(self, *args, **kwargs):
        super(AkFileDialog, self).__init__(*args, **kwargs)
        self.setOption(QtWidgets.QFileDialog.DontUseNativeDialog, True)
        self.setFileMode(QtWidgets.QFileDialog.ExistingFiles)
        self.setNameFilter('CSV Files (*.csv)')

    def accept(self):
        super(AkFileDialog, self).accept()