# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connectionsView.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ConnectionsDialog(object):
    def setupUi(self, ConnectionsDialog):
        ConnectionsDialog.setObjectName("ConnectionsDialog")
        ConnectionsDialog.resize(342, 194)
        self.horizontalLayout = QtWidgets.QHBoxLayout(ConnectionsDialog)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listConnections = QtWidgets.QListView(ConnectionsDialog)
        self.listConnections.setObjectName("listConnections")
        self.horizontalLayout.addWidget(self.listConnections)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(10, 10, 5, -1)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btnAdd = QtWidgets.QPushButton(ConnectionsDialog)
        self.btnAdd.setObjectName("btnAdd")
        self.verticalLayout.addWidget(self.btnAdd)
        self.btnChange = QtWidgets.QPushButton(ConnectionsDialog)
        self.btnChange.setObjectName("btnChange")
        self.verticalLayout.addWidget(self.btnChange)
        self.btnRemove = QtWidgets.QPushButton(ConnectionsDialog)
        self.btnRemove.setObjectName("btnRemove")
        self.verticalLayout.addWidget(self.btnRemove)
        self.btnClose = QtWidgets.QPushButton(ConnectionsDialog)
        self.btnClose.setObjectName("btnClose")
        self.verticalLayout.addWidget(self.btnClose)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(ConnectionsDialog)
        QtCore.QMetaObject.connectSlotsByName(ConnectionsDialog)

    def retranslateUi(self, ConnectionsDialog):
        _translate = QtCore.QCoreApplication.translate
        ConnectionsDialog.setWindowTitle(_translate("ConnectionsDialog", "Dialog"))
        self.btnAdd.setText(_translate("ConnectionsDialog", "Add..."))
        self.btnChange.setText(_translate("ConnectionsDialog", "Change..."))
        self.btnRemove.setText(_translate("ConnectionsDialog", "Remove"))
        self.btnClose.setText(_translate("ConnectionsDialog", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ConnectionsDialog = QtWidgets.QDialog()
    ui = Ui_ConnectionsDialog()
    ui.setupUi(ConnectionsDialog)
    ConnectionsDialog.show()
    sys.exit(app.exec_())

