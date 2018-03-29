from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog
from src.view.ui_historicalView import Ui_Dialog
import csv
import src.controller.akFunctions as fn
from src.model.akInstrumentDataTableModel import AkInstrumentDataTableModel

import sip
sip.setapi('QString', 2)
sip.setapi('QVariant', 2)

class AkHistoricalController(QtWidgets.QDialog):

    #model = PalleteTableModel(tableData, headers)


    def __init__(self):
        super(AkHistoricalController, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setModal(True)
        self.setWindowTitle("Historical Data Manager")
        self.show()

        self.initUI()
        self.setupConnections()
        self.loadData()

    #----------------------------------------------------------------------
    # Private methods
    # ---------------------------------------------------------------------

    def initUI(self):
        self.ui.tableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)

    def loadData(self):

        # load default file from PC
        # TODO : load data from config
        headers, data = self.loadCSV('G:/Programming/Projects/StatisticCalculatorQt/src/resources/^spx_y.csv')
        self.model = AkInstrumentDataTableModel(data, headers)
        self.ui.tableView.setModel(self.model)



    def setupConnections(self):
        self.ui.btnImport.clicked.connect(self.OnImportButton_click_Handler)
        self.ui.btnFilter.clicked.connect(self.OnFilterButton_clickHandler)
        self.ui.btnDownload.clicked.connect(self.OnDownloadButton_clickHandler)

    #----------------------------------------------------------------------
    # Event handlers
    # ---------------------------------------------------------------------

    def OnImportButton_click_Handler(self):
        fileName = self.openFileNameDialog()
        print(fileName)
        self.loadCSV(fileName)
        self.ui.tableView.setModel(self.model)

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

    # self.loadCSV(fileName)
    #        print(fileName)

    def loadCSV(self, fileName):
        data = []
        with open(fileName, "r") as fileInput:
            for row in csv.reader(fileInput):
                items = [field for field in row ]
                data.append(items)

            # remove 'Volume' column
            for row in data:
                del row[5]

            # get 'Headers'
            headers = data.pop(0)
        return headers, data


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



