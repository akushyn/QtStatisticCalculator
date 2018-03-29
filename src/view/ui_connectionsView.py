# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'connectionsView.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(342, 194)
        self.horizontalLayout = QtWidgets.QHBoxLayout(Dialog)
        self.horizontalLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.listConnections = QtWidgets.QListView(Dialog)
        self.listConnections.setObjectName("listConnections")
        self.horizontalLayout.addWidget(self.listConnections)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setContentsMargins(10, 10, 5, -1)
        self.verticalLayout.setSpacing(10)
        self.verticalLayout.setObjectName("verticalLayout")
        self.btnAdd = QtWidgets.QPushButton(Dialog)
        self.btnAdd.setObjectName("btnAdd")
        self.verticalLayout.addWidget(self.btnAdd)
        self.btnChange = QtWidgets.QPushButton(Dialog)
        self.btnChange.setObjectName("btnChange")
        self.verticalLayout.addWidget(self.btnChange)
        self.btnRemove = QtWidgets.QPushButton(Dialog)
        self.btnRemove.setObjectName("btnRemove")
        self.verticalLayout.addWidget(self.btnRemove)
        self.btnClose = QtWidgets.QPushButton(Dialog)
        self.btnClose.setObjectName("btnClose")
        self.verticalLayout.addWidget(self.btnClose)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem)
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.btnAdd.setText(_translate("Dialog", "Add..."))
        self.btnChange.setText(_translate("Dialog", "Change..."))
        self.btnRemove.setText(_translate("Dialog", "Remove"))
        self.btnClose.setText(_translate("Dialog", "Close"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

