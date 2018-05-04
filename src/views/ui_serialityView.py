# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'serialityView.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(554, 323)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(Dialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.formLayout = QtWidgets.QFormLayout()
        self.formLayout.setSizeConstraint(QtWidgets.QLayout.SetFixedSize)
        self.formLayout.setObjectName("formLayout")
        self.labelName = QtWidgets.QLabel(Dialog)
        self.labelName.setObjectName("labelName")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.labelName)
        self.lineName = QtWidgets.QLineEdit(Dialog)
        self.lineName.setObjectName("lineName")
        self.formLayout.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.lineName)
        self.labelSequence = QtWidgets.QLabel(Dialog)
        self.labelSequence.setObjectName("labelSequence")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.labelSequence)
        self.lineSequence = QtWidgets.QLineEdit(Dialog)
        self.lineSequence.setObjectName("lineSequence")
        self.formLayout.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.lineSequence)
        self.labelAmount = QtWidgets.QLabel(Dialog)
        self.labelAmount.setObjectName("labelAmount")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.labelAmount)
        self.hSliderSequenceCount = QtWidgets.QSlider(Dialog)
        self.hSliderSequenceCount.setOrientation(QtCore.Qt.Horizontal)
        self.hSliderSequenceCount.setObjectName("hSliderSequenceCount")
        self.formLayout.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.hSliderSequenceCount)
        self.verticalLayout.addLayout(self.formLayout)
        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem, 0, 3, 1, 1)
        self.btnPlus = QtWidgets.QToolButton(Dialog)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("../icons/Plus_Sign-512.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnPlus.setIcon(icon)
        self.btnPlus.setObjectName("btnPlus")
        self.gridLayout.addWidget(self.btnPlus, 0, 1, 1, 1)
        self.btnMinus = QtWidgets.QToolButton(Dialog)
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap("../icons/minus-512.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.btnMinus.setIcon(icon1)
        self.btnMinus.setObjectName("btnMinus")
        self.gridLayout.addWidget(self.btnMinus, 0, 2, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout.addItem(spacerItem1, 0, 0, 1, 1)
        self.verticalLayout.addLayout(self.gridLayout)
        spacerItem2 = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout.addItem(spacerItem2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setContentsMargins(20, -1, 20, -1)
        self.horizontalLayout.setSpacing(10)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.btnDeleteSequence = QtWidgets.QPushButton(Dialog)
        self.btnDeleteSequence.setObjectName("btnDeleteSequence")
        self.horizontalLayout.addWidget(self.btnDeleteSequence)
        self.btnAddSequence = QtWidgets.QPushButton(Dialog)
        self.btnAddSequence.setObjectName("btnAddSequence")
        self.horizontalLayout.addWidget(self.btnAddSequence)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.verticalLayout.setStretch(2, 1)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.tableSequence = QtWidgets.QTableWidget(Dialog)
        self.tableSequence.setObjectName("tableSequence")
        self.tableSequence.setColumnCount(2)
        self.tableSequence.setRowCount(0)
        item = QtWidgets.QTableWidgetItem()
        self.tableSequence.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableSequence.setHorizontalHeaderItem(1, item)
        self.tableSequence.horizontalHeader().setStretchLastSection(True)
        self.tableSequence.verticalHeader().setSortIndicatorShown(False)
        self.tableSequence.verticalHeader().setStretchLastSection(False)
        self.horizontalLayout_3.addWidget(self.tableSequence)
        self.horizontalLayout_3.setStretch(1, 3)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.labelName.setText(_translate("Dialog", "Name"))
        self.labelSequence.setText(_translate("Dialog", "Sequence"))
        self.labelAmount.setText(_translate("Dialog", "Amount"))
        self.btnPlus.setText(_translate("Dialog", "..."))
        self.btnMinus.setText(_translate("Dialog", "..."))
        self.btnDeleteSequence.setText(_translate("Dialog", "Delete"))
        self.btnAddSequence.setText(_translate("Dialog", "Add"))
        item = self.tableSequence.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "Name"))
        item = self.tableSequence.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Sequence"))

import Resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    Dialog = QtWidgets.QDialog()
    ui = Ui_Dialog()
    ui.setupUi(Dialog)
    Dialog.show()
    sys.exit(app.exec_())

