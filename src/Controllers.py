import csv

import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QFileDialog, QMessageBox

from src import Functions as func
from src.Models import AkTableModel, AkListModel, AkNotesTableModel
from src.controls.akFileDialog import AkFileDialog
from src.views.ui_calculatorMainView import Ui_CalculatorMainView
from src.views.ui_connectActionView import Ui_ConnectActionDialog
from src.views.ui_connectionsView import Ui_ConnectionsDialog
from src.views.ui_historicalView import Ui_HistoricalDialog
from src.views.ui_instrumentView import Ui_InstrumentsDialog
from src.views.ui_optionsView import Ui_OptionsDialog


class AkInstrumentsController(QtWidgets.QDialog, Ui_InstrumentsDialog):
    def __init__(self, model=None):
        super(AkInstrumentsController, self).__init__()
        self.model = model
        self.setupUi()

        self.setupConnections()
        self.setupModel()

    #----------------------------------------------------------------------
    # Private methods
    # ---------------------------------------------------------------------

    def setupUi(self):
        super(AkInstrumentsController, self).setupUi(self)

        self.setModal(True)
        self.setWindowTitle("Instrument Data Manager")


    def setupConnections(self):
        self.btnSearch.clicked.connect(self.OnSearchButton_click_Handler)
        self.btnSelectAll.clicked.connect(self.OnSelectAllButton_clickHandler)
        self.btnDeselectAll.clicked.connect(self.OnDeselectAllButton_clickHandler)
        self.btnOK.clicked.connect(self.OnOkButton_clickHandler)
        self.btnCancel.clicked.connect(self.OnCancelButton_clickHandler)
        self.btnNew.clicked.connect(self.OnNewButton_clickHandler)
        self.btnDelete.clicked.connect(self.OnDeleteButton_clickHandler)
        self.btnInsert.clicked.connect(self.OnInsertButton_clickHandler)
        self.btnRemove.clicked.connect(self.OnRemoveButton_clickHandler)

    def setupModel(self):
        pass

    #----------------------------------------------------------------------
    # Event handlers
    # ---------------------------------------------------------------------

    def OnSearchButton_click_Handler(self):
        print("OnSearchButton_click_Handler method called!")

    def OnSelectAllButton_clickHandler(self):
        print("OnSelectAllButton_clickHandler method called!")

    def OnDeselectAllButton_clickHandler(self):
        print("OnDeselectAllButton_clickHandler method called!")

    def OnOkButton_clickHandler(self):
        print("OnOkButton_clickHandler method called!")

    def OnCancelButton_clickHandler(self):
        self.close()

    def OnNewButton_clickHandler(self):
        print("OnNewButton_clickHandler method called!")

    def OnDeleteButton_clickHandler(self):
        print("OnDeleteButton_clickHandler method called!")

    def OnInsertButton_clickHandler(self):
        print("OnInsertButton_clickHandler method called!")

    def OnRemoveButton_clickHandler(self):
        print("OnRemoveButton_clickHandler method called!")

class AkConnectActionController(QtWidgets.QDialog, Ui_ConnectActionDialog):
    def __init__(self):
        super(AkConnectActionController, self).__init__()
        self.setupUi(self)
        self.setModal(True)
        self.setWindowTitle("Connect")

class AkDisconnectActionController(QtWidgets.QDialog, Ui_ConnectActionDialog):
    def __init__(self):
        super(AkDisconnectActionController, self).__init__()
        self.setupUi(self)
        self.setModal(True)
        self.setWindowTitle("Disconnect")

class AkConnectionsController(QtWidgets.QDialog, Ui_ConnectionsDialog):
    def __init__(self):
        super(AkConnectionsController, self).__init__()
        self.setupUi(self)
        self.setModal(True)
        self.setWindowTitle("Setup Connection")

    def doSmth(self):
        pass

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
        if dialog.exec_() == QtWidgets.QDialog.Accepted:
            names = dialog.selectedFiles()

        items = []
        for i in range(len(names)):
            name = names[i]
            headers, data = func.loadCSV(name)
            ohlcTable = AkTableModel(func.getShortName(name), data, headers)
            if(ohlcTable):
                self.model.insertRows(0, 1, [ohlcTable])

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

class AkOptionsController(QtWidgets.QDialog, Ui_OptionsDialog):
    def __init__(self):
        super(AkOptionsController, self).__init__()
        self.setupUi(self)
        self.setModal(True)
        self.setWindowTitle("Options")

class AkCalculatorController(QtWidgets.QMainWindow, Ui_CalculatorMainView):
    def __init__(self):
        super(AkCalculatorController, self).__init__()
        self.setupUi()

        self.setupModel()
        self.setupConnections()
        self.setupControllers()

    def setupUi(self):
        super(AkCalculatorController, self).setupUi(self)

        self.calendar.setGridVisible(True)

        self.notesTableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.notesTableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.ohlcTableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.ohlcTableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.graphicsView.setTitle('My Graph')
        self.graphicsView.setLabel('bottom', 'X axis')
        self.graphicsView.setLabel('left', 'Y axis')
        self.graphicsView.setBackground(QtGui.QColor(0, 0, 0))

        self.plotexample()

    #----------------------------------------------------------------------
    # Private methods
    # ---------------------------------------------------------------------

    def setupControllers(self):
        self.instrumentsController = AkInstrumentsController()
        self.historicalController = AkHistoricalController(self.instrumentsModel)
        self.connectionsController = AkConnectionsController()
        self.connectActionController = AkConnectActionController()
        self.disconnectActionController = AkDisconnectActionController()
        self.optionsController = AkOptionsController()

    def plotexample(self):
        a = np.array([1, 2, 3, 4, 5])
        b = np.array([6, 7, 8, 9, 10])
        self.graphicsView.plot(a, b)
        self.graphicsView.showGrid(x=True, y=True)

    def setupModel(self):
        fileName = "G:/Programming/Projects/QtStatisticCalculator/src/resources/^spx_y.csv"
        headers, data = func.loadCSV(fileName)
        items = AkTableModel(func.getShortName(fileName), data, headers)

        self.instrumentsModel = AkListModel([items])
        self.notesModel = AkNotesTableModel()


        self.notesTableView.setModel(self.notesModel)
        self.instrumentsListView.setModel(self.instrumentsModel)


    def setupConnections(self):

        # Main menu events
        #-----------------
        self.actionHistoricalView.triggered.connect(self.OnShowHistoricalView_Handler)
        self.actionInstrumentView.triggered.connect(self.OnShowInstrumentView_Handler)
        self.actionConnectionsView.triggered.connect(self.OnShowConnectionsView_Handler)
        self.actionConnect.triggered.connect(self.OnShowConnectActionView_Handler)
        self.actionDisconnect.triggered.connect(self.OnShowDisconnectActionView_Handler)
        self.actionOptionsView.triggered.connect(self.OnShowOptionsView_Handler)
        self.actionExit.triggered.connect(self.OnExitAppAction_Handler)

        self.btnOK.clicked.connect(self.OnAddNoteButtonClick_Handler)
        self.instrumentsListView.clicked.connect(self.OnListView_clickHandler)
        self.notesTableView.clicked.connect(self.OnNotesTable_clickHandler)
        self.btnCalculate.clicked.connect(self.OnCalculateButton_clickHandler)
    #----------------------------------------------------------------------
    # Event handlers
    # ---------------------------------------------------------------------

    def OnInstrumentSelection_changedHandler(self):
        print('OnInstrumentSelection_changedHandler')

    def OnContextMenuButton_clickHandler(self):
        pass

    def OnListView_clickHandler(self, index):
        data = self.instrumentsListView.model().itemData(index)
        self.ohlcTableView.setModel(data)

    def OnNotesTable_clickHandler(self, index):
        sellData = self.notesTableView.model().data(index, role=QtCore.Qt.DisplayRole)
        self.textNote.setPlainText(sellData)

    def OnCalculateButton_clickHandler(self):
            indexes = self.instrumentsListView.selectionModel().selectedIndexes()
            model = self.instrumentsListView.model()
            if (indexes):
                selection = indexes[0]
                distributions = model.distributionModel(selection)


    def OnShowHistoricalView_Handler(self):
        if (self.historicalController):
            self.historicalController.show()

    def OnShowInstrumentView_Handler(self):
        if (self.instrumentsController):
            self.instrumentsController.show()

    def OnShowConnectionsView_Handler(self):
        if(self.connectionsController):
            self.connectionsController.show()

    def OnShowConnectActionView_Handler(self):
        if (self.connectActionController):
            self.connectActionController.show()

    def OnShowDisconnectActionView_Handler(self):
        if (self.disconnectActionController):
            self.disconnectActionController.show()

    def OnShowOptionsView_Handler(self):
        if (self.optionsController):
            self.optionsController.show()


    def OnAddNoteButtonClick_Handler(self):
        dateString = self.calendar.selectedDate().toString('yyyy-MM-dd')
        noteString = self.textNote.toPlainText()

        if(noteString != ''):
            self.notesModel.insertRows(0, 1, [dateString, noteString])

    def OnExitAppAction_Handler(self, event):
        reply = QMessageBox.question(self, "Message", "Are you sure you want to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.close()


