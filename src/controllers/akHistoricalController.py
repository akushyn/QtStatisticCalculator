import csv
import sys

from PyQt5 import QtWidgets, QtCore
from PyQt5.QtCore import QDir
from PyQt5.QtWidgets import QMessageBox, QFileDialog, QFileSystemModel
from src.akFunctions import AkFunctions
from src.controls.akFileDialog import AkFileDialog
from src.data.akInstrument import AkInstrument
from src.data.akPeriod import AkPeriod
from src.views.ui_historicalView import Ui_HistoricalDialog


class AkHistoricalController(QtWidgets.QDialog, Ui_HistoricalDialog):
    def __init__(self, model=None):
        super(AkHistoricalController, self).__init__()
        self._model = model
        self.setupUi()

        self.setupConnections()
        self.setupModel()

    def setupUi(self):
        super(AkHistoricalController, self).setupUi(self)

        self.setModal(True)
        self.setWindowTitle("Historical Data Manager")
        self.dateEnd.setDate(QtCore.QDate.currentDate())
        self.btnFilter.setEnabled(False)

    #----------------------------------------------------------------------
    # Private methods
    # ---------------------------------------------------------------------

    def setupModel(self):
        self.listViewImported.setModel(self._model)

        fileName = "G:/Programming/Projects/QtStatisticCalculator/^spx_y_test.csv"
        name = AkFunctions.getShortName(fileName)
        headers, data = AkFunctions.loadCSV(fileName)
        xPeriod = AkPeriod(1, data, headers=headers)

        instrument = AkInstrument(name, [xPeriod])
        self._model.insertRows(0, len([instrument]), [instrument])

        fileSystemModel = QFileSystemModel()
        fileSystemModel.setFilter(QDir.AllDirs | QDir.NoDotAndDotDot | QDir.AllEntries)

        filters = ["*.csv"]
        fileSystemModel.setNameFilters(filters)
        fileSystemModel.setNameFilterDisables(False)

        fileSystemModel.setRootPath(QDir.currentPath())

        self.treeViewWindowFiles.setModel(fileSystemModel)
        self.treeViewWindowFiles.hideColumn(1)
        self.treeViewWindowFiles.hideColumn(2)
        self.treeViewWindowFiles.hideColumn(3)
        #self.treeViewWindowFiles.setRootIndex(fileSystemModel.index(QDir.currentPath()))


    def setupConnections(self):
        self.btnImport.clicked.connect(self.onImportButton_click_Handler)
        self.btnFilter.clicked.connect(self.OnFilterButton_clickHandler)
        self.listViewImported.clicked.connect(self.onListViewImported_clickHandler)

    #----------------------------------------------------------------------
    # Event handlers
    # ---------------------------------------------------------------------

    def onListViewImported_clickHandler(self):
        index = self.listViewImported.selectedIndexes()[0]
        model = index.model()

    def OnTreeView_clickHandler(self, index):
        index = self.treeViewImported.selectedIndexes()[0]
        model = index.model()
        item = model.getNode(index)

        if (item.typeNode() == 'PERIOD'):
            self.ohlcTableView.setModel(item)
            self.ohlcTableView.verticalHeader().setVisible(True)
        else:
            self.ohlcTableView.verticalHeader().setVisible(False)
            self.ohlcTableView.setModel(AkInstrumentTableModel())

        if (self.ohlcTableView.model() is not None) and (self.ohlcTableView.model().rowCount() > 1):
            self.btnFilter.setEnabled(True)
        else:
            self.btnFilter.setEnabled(False)

    def onImportButton_click_Handler(self):
        dialog = AkFileDialog()

        selectedFiles = []
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            selectedFiles = dialog.selectedFiles()
        try:
            if (selectedFiles):
                importedFiles = []
                for i in range(len(selectedFiles)):
                    selectedFile = selectedFiles[i]
                    headers, data = AkFunctions.loadCSV(selectedFile)

                    xPeriod = AkPeriod(1, data, headers=headers)
                    instrument = AkInstrument(AkFunctions.getShortName(selectedFile), [xPeriod])
                    importedFiles.append(instrument)

                if (importedFiles):
                    self._model.insertRows(0, len(importedFiles), importedFiles)
        except Exception as e:
            print("Invalid format:", sys.exc_info()[0])
            QMessageBox.warning(self, "Invalid .csv format", "The file, you've tried to import has invalid format.", QMessageBox.Ok)

    def reduce(self):
        print("reducing")

    def OnFilterButton_clickHandler(self):
        model = self.ohlcTableView.model()

        if (model is not None) and (model.rowCount() > 1):
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
            for rowNumber in range(self._model.rowCount()):
                fields = [
                    self._model.data(
                        self._model.index(rowNumber, columnNumber),
                        QtCore.Qt.DisplayRole
                    )
                    for columnNumber in range(self._model.columnCount())
                ]
                writer.writerow(fields)