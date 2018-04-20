# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connectActionView.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ConnectActionDialog(object):
    def setupUi(self, ConnectActionDialog):
        ConnectActionDialog.setObjectName("ConnectActionDialog")
        ConnectActionDialog.resize(281, 263)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(ConnectActionDialog.sizePolicy().hasHeightForWidth())
        ConnectActionDialog.setSizePolicy(sizePolicy)
        self.horizontalLayout = QtWidgets.QHBoxLayout(ConnectActionDialog)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listConnections = QtWidgets.QListView(ConnectActionDialog)
        self.listConnections.setObjectName("listConnections")
        self.horizontalLayout.addWidget(self.listConnections)

        self.retranslateUi(ConnectActionDialog)
        QtCore.QMetaObject.connectSlotsByName(ConnectActionDialog)

    def retranslateUi(self, ConnectActionDialog):
        _translate = QtCore.QCoreApplication.translate
        ConnectActionDialog.setWindowTitle(_translate("ConnectActionDialog", "Dialog"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ConnectActionDialog = QtWidgets.QDialog()
    ui = Ui_ConnectActionDialog()
    ui.setupUi(ConnectActionDialog)
    ConnectActionDialog.show()
    sys.exit(app.exec_())

