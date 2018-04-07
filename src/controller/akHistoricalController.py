from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog

import src.controller.akFunctions as func
from src.view.ui_historicalView import Ui_Dialog
import csv
import src.controller.akFunctions
from src.model.akTableModel import AkTableModel
from src.model.akInstrument import AkInstrument

import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

class AkHistoricalController(QtWidgets.QDialog):
    def __init__(self, model=None):
        super(AkHistoricalController, self).__init__()
        self.model = model
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.initUI()
        self.setupConnections()
        self.loadModelData()

    #----------------------------------------------------------------------
    # Private methods
    # ---------------------------------------------------------------------

    def initUI(self):
        self.setModal(True)
        self.setWindowTitle("Historical Data Manager")

        self.ui.tableViewOHLC.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.ui.tableViewOHLC.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

    def loadModelData(self):
        self.ui.listViewImported.setModel(self.model)

    def setupConnections(self):
        self.ui.btnImport.clicked.connect(self.OnImportButton_click_Handler)
        self.ui.btnFilter.clicked.connect(self.OnFilterButton_clickHandler)
        self.ui.listViewImported.clicked.connect(self.OnListView_clickHandler)


    #----------------------------------------------------------------------
    # Event handlers
    # ---------------------------------------------------------------------

    def OnListView_clickHandler(self, index):
        data = self.ui.listViewImported.model().itemData(index.row())
        self.ui.tableViewOHLC.setModel(data)

    def OnImportButton_click_Handler(self):
        pathFileName = self.openFileNameDialog()
        if (not pathFileName):
            return

        shortName = func.getShortName(pathFileName)

        headers, data = func.loadCSV(pathFileName)
        ohlc = AkTableModel(data, headers)

        self.instrument = AkInstrument(shortName, ohlc)
        self.model.insertRows(0, 1, [self.instrument])


    def OnFilterButton_clickHandler(self):
        print("OnFilterButton_clickHandler method called!")

    def OnDownloadButton_clickHandler(self):
        print("OnDownloadButton_clickHandler method called!")


    #----------------------------------------------------------------------
    # Other methods
    # ---------------------------------------------------------------------

    def openFileNameDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "", "CSV Files (*.csv)",
                                                  options=options)
        if fileName:
            print(fileName)
            return fileName

    def saveFileDialog(self):
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        fileName, _ = QFileDialog.getSaveFileName(self, "QFileDialog.getSaveFileName()", "",
                                                  "All Files (*);;Text Files (*.txt)", options=options)
        if fileName:
            return fileName

    def writeCSV(self, fileName):
        with open(fileName, "wb") as fileOutput:
            writer = csv.writer(fileOutput)
            for rowNumber in range(self.model.rowCount()):
                fields = [
                    self.model.data(
                        self.model.index(rowNumber, columnNumber),
                        QtCore.Qt.DisplayRole
                    )
                    for columnNumber in range(self.model.columnCount())
                ]
                writer.writerow(fields)



