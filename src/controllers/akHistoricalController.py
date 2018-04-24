import sys
from PyQt5 import QtWidgets, QtCore
from PyQt5.QtWidgets import QMessageBox, QFileDialog
from src.controls.akFileDialog import AkFileDialog
from src.models.akTableModel import AkInstrumentOHLCModel
from src.views.ui_historicalView import Ui_HistoricalDialog
import src.Functions as func
import csv

class AkHistoricalController(QtWidgets.QDialog, Ui_HistoricalDialog):
    def __init__(self, model=None):
        super(AkHistoricalController, self).__init__()
        self.model = model
        self.setupUi()

        self.setupConnections()
        self.setupModel()

    def setupUi(self):
        super(AkHistoricalController, self).setupUi(self)

        self.setModal(True)
        self.btnFilter.setEnabled(False)
        self.setWindowTitle("Historical Data Manager")
        self.dateEnd.setDate(QtCore.QDate.currentDate())

        self.btnImport.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.btnImport.customContextMenuRequested.connect(self.OnContextMenuImportButton_clickHandler)


    #----------------------------------------------------------------------
    # Private methods
    # ---------------------------------------------------------------------

    def setupModel(self):
        self.listViewImported.setModel(self.model)

    def setupConnections(self):
        self.btnImport.clicked.connect(self.OnImportButton_click_Handler)
        self.btnFilter.clicked.connect(self.OnFilterButton_clickHandler)
        self.listViewImported.clicked.connect(self.OnListView_clickHandler)
        self.toolButtonDelete.clicked.connect(self.OnToolButtonDelete_clickHandler)
        self.toolButtonClearAll.clicked.connect(self.OnToolButtonClearAll_clickHandler)

    #----------------------------------------------------------------------
    # Event handlers
    # ---------------------------------------------------------------------
    def OnContextMenuImportButton_clickHandler(self):
        print("context")

    def OnToolButtonDelete_clickHandler(self):
        pass
        #indexes = self.listViewImported.selectionModel().selectedRows()
        #if (indexes):

        #    reply = QMessageBox.question(self, "Confirmation", "Delete selected?",
        #                                QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        #    if reply == QMessageBox.Yes:
        #        pos = indexes[0].row()
        #        rows = len(indexes)
        #        self.listViewImported.model().removeRows(pos, rows)

    def OnToolButtonClearAll_clickHandler(self):
        pass


    def OnListView_clickHandler(self, index):
        data = self.listViewImported.model().itemData(index)
        if (data):
            self.btnFilter.setEnabled(True)
        self.ohlcTableView.setModel(data)

    def OnImportButton_click_Handler(self):
        dialog = AkFileDialog()
        names = []
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            names = dialog.selectedFiles()
        try:
            if (names):
                for i in range(len(names)):
                    name = names[i]
                    headers, data = func.loadCSV(name)
                    ohlcTable = AkInstrumentOHLCModel(func.getShortName(name), data, headers)
                    if(ohlcTable):
                        self.model.insertRows(0, 1, [ohlcTable])
        except IndexError as e:
            print("Invalid format:", sys.exc_info()[0])
            QMessageBox.warning(self, "Invalid .csv format", "The file, you've tried to import has invalid format.", QMessageBox.Ok)

    def OnFilterButton_clickHandler(self):
        fromDate = self.dateStart.date()
        toDate = self.dateEnd.date()

        reply = QMessageBox.warning(self, "Confirmation", "Are you sure you want to filter data? \nChanges can't be prevented.", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        # filter model data
        if reply == QMessageBox.Yes:
            self.ohlcTableView.model().filter(fromDate, toDate)





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