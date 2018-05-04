# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'importPreview.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ImportPreview(object):
    def setupUi(self, ImportPreview):
        ImportPreview.setObjectName("ImportPreview")
        ImportPreview.resize(733, 460)
        self.verticalLayout_4 = QtWidgets.QVBoxLayout(ImportPreview)
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.vBoxMain = QtWidgets.QVBoxLayout()
        self.vBoxMain.setObjectName("vBoxMain")
        self.splitter = QtWidgets.QSplitter(ImportPreview)
        self.splitter.setOrientation(QtCore.Qt.Horizontal)
        self.splitter.setObjectName("splitter")
        self.widget = QtWidgets.QWidget(self.splitter)
        self.widget.setObjectName("widget")
        self.vBoxInstruments = QtWidgets.QVBoxLayout(self.widget)
        self.vBoxInstruments.setContentsMargins(0, 0, 0, 0)
        self.vBoxInstruments.setObjectName("vBoxInstruments")
        self.hBoxAddInstrument = QtWidgets.QHBoxLayout()
        self.hBoxAddInstrument.setObjectName("hBoxAddInstrument")
        self.labelInstruments = QtWidgets.QLabel(self.widget)
        self.labelInstruments.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.labelInstruments.setObjectName("labelInstruments")
        self.hBoxAddInstrument.addWidget(self.labelInstruments)
        self.toolButtonAddInstrument = QtWidgets.QToolButton(self.widget)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/plus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.toolButtonAddInstrument.setIcon(icon)
        self.toolButtonAddInstrument.setIconSize(QtCore.QSize(16, 16))
        self.toolButtonAddInstrument.setObjectName("toolButtonAddInstrument")
        self.hBoxAddInstrument.addWidget(self.toolButtonAddInstrument)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hBoxAddInstrument.addItem(spacerItem)
        self.vBoxInstruments.addLayout(self.hBoxAddInstrument)
        self.treeViewInstruments = QtWidgets.QTreeView(self.widget)
        self.treeViewInstruments.setObjectName("treeViewInstruments")
        self.vBoxInstruments.addWidget(self.treeViewInstruments)
        self.widget1 = QtWidgets.QWidget(self.splitter)
        self.widget1.setObjectName("widget1")
        self.vBoxImported = QtWidgets.QVBoxLayout(self.widget1)
        self.vBoxImported.setContentsMargins(0, 0, 0, 0)
        self.vBoxImported.setSpacing(12)
        self.vBoxImported.setObjectName("vBoxImported")
        self.labelImported = QtWidgets.QLabel(self.widget1)
        self.labelImported.setStyleSheet("font: 10pt \"MS Shell Dlg 2\";")
        self.labelImported.setObjectName("labelImported")
        self.vBoxImported.addWidget(self.labelImported)
        self.listViewImportedFiles = QtWidgets.QListView(self.widget1)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.listViewImportedFiles.sizePolicy().hasHeightForWidth())
        self.listViewImportedFiles.setSizePolicy(sizePolicy)
        self.listViewImportedFiles.setObjectName("listViewImportedFiles")
        self.vBoxImported.addWidget(self.listViewImportedFiles)
        self.vBoxMain.addWidget(self.splitter)
        self.hBoxButtons = QtWidgets.QHBoxLayout()
        self.hBoxButtons.setObjectName("hBoxButtons")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.hBoxButtons.addItem(spacerItem1)
        self.buttonSave = QtWidgets.QPushButton(ImportPreview)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonSave.sizePolicy().hasHeightForWidth())
        self.buttonSave.setSizePolicy(sizePolicy)
        self.buttonSave.setObjectName("buttonSave")
        self.hBoxButtons.addWidget(self.buttonSave)
        self.buttonClose = QtWidgets.QPushButton(ImportPreview)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.buttonClose.sizePolicy().hasHeightForWidth())
        self.buttonClose.setSizePolicy(sizePolicy)
        self.buttonClose.setObjectName("buttonClose")
        self.hBoxButtons.addWidget(self.buttonClose)
        self.vBoxMain.addLayout(self.hBoxButtons)
        self.vBoxMain.setStretch(0, 1)
        self.verticalLayout_4.addLayout(self.vBoxMain)

        self.retranslateUi(ImportPreview)
        QtCore.QMetaObject.connectSlotsByName(ImportPreview)

    def retranslateUi(self, ImportPreview):
        _translate = QtCore.QCoreApplication.translate
        ImportPreview.setWindowTitle(_translate("ImportPreview", "Dialog"))
        self.labelInstruments.setText(_translate("ImportPreview", "Instrument list"))
        self.toolButtonAddInstrument.setText(_translate("ImportPreview", "Add"))
        self.labelImported.setText(_translate("ImportPreview", "Imported files"))
        self.buttonSave.setText(_translate("ImportPreview", "Save"))
        self.buttonClose.setText(_translate("ImportPreview", "Close"))

import Resources_rc

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ImportPreview = QtWidgets.QDialog()
    ui = Ui_ImportPreview()
    ui.setupUi(ImportPreview)
    ImportPreview.show()
    sys.exit(app.exec_())

