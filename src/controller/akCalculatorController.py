from PyQt5 import uic, QtCore
import sys
from PyQt5 import QtWidgets, QtGui
from PyQt5.QtWidgets import QMessageBox
import numpy as np

import src.controller.akFunctions as func


from src.model.akInstrument import AkInstrument
from src.model.akInstrumentListModel import AkInstrumentListModel
from src.model.akNotesModel import AkNotesModel
from src.model.akTableModel import AkTableModel

from src.view.ui_calculatorMainView import Ui_AkCalculatorMainView
from src.controller.akHistoricalController import AkHistoricalController
from src.controller.akInstrumentsController import AkInstrumentsController
from src.controller.akConnectionsController import AkConnectionsController
from src.controller.akConnectActionController import AkConnectActionController
from src.controller.akDisconnectActionController import AkDisconnectActionController
from src.controller.akOptionsController import AkOptionsController

class AkCalculatorController(QtWidgets.QMainWindow):
    def __init__(self):
        super(AkCalculatorController, self).__init__()



        self.ui = Ui_AkCalculatorMainView()
        self.ui.setupUi(self)


        self.initUI()


        headers, data = func.loadCSV("G:/Programming/Projects/QtStatisticCalculator/src/resources/^spx_y.csv")
        self.data = AkTableModel(data, headers)
        self.instrument = AkInstrument("spx_y", self.data)

        self.instrumentsModel = AkInstrumentListModel([self.instrument])
        self.notesModel = AkNotesModel()

        self.initControllers()
        self.setupConnections()
        self.loadModelData()
    #----------------------------------------------------------------------
    # Private methods
    # ---------------------------------------------------------------------

    def initControllers(self):
        self.instrumentsController = AkInstrumentsController()
        self.historicalController = AkHistoricalController(self.instrumentsModel)
        self.connectionsController = AkConnectionsController()
        self.connectActionController = AkConnectActionController()
        self.disconnectActionController = AkDisconnectActionController()
        self.optionsController = AkOptionsController()



    def initUI(self):
        self.ui.calendar.setGridVisible(True)

        self.ui.tableNotes.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.ui.tableNotes.setSelectionMode(QtWidgets.QAbstractItemView.SingleSelection)
        self.ui.tableNotes.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.ui.tableViewOHLC.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.ui.tableViewOHLC.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.ui.graphicsView.setTitle('My Graph')
        self.ui.graphicsView.setLabel('bottom', 'X axis')
        self.ui.graphicsView.setLabel('left', 'Y axis')
        self.ui.graphicsView.setBackground(QtGui.QColor(0, 0, 0))

        self.plotexample()

    def plotexample(self):
        a = np.array([1, 2, 3, 4, 5])
        b = np.array([6, 7, 8, 9, 10])
        self.ui.graphicsView.plot(a, b)
        self.ui.graphicsView.showGrid(x=True, y=True)

    def loadModelData(self):
        self.ui.tableNotes.setModel(self.notesModel)
        self.ui.listViewInstruments.setModel(self.instrumentsModel)


    def setupConnections(self):

        # Main menu events
        #-----------------
        self.ui.actionHistoricalView.triggered.connect(self.OnShowHistoricalView_Handler)
        self.ui.actionInstrumentView.triggered.connect(self.OnShowInstrumentView_Handler)
        self.ui.actionConnectionsView.triggered.connect(self.OnShowConnectionsView_Handler)
        self.ui.actionConnect.triggered.connect(self.OnShowConnectActionView_Handler)
        self.ui.actionDisconnect.triggered.connect(self.OnShowDisconnectActionView_Handler)
        self.ui.actionOptionsView.triggered.connect(self.OnShowOptionsView_Handler)
        self.ui.actionExit.triggered.connect(self.OnExitAppAction_Handler)

        self.ui.btnOK.clicked.connect(self.OnAddNoteButtonClick_Handler)
        self.ui.listViewInstruments.clicked.connect(self.OnListView_clickHandler)
    #----------------------------------------------------------------------
    # Event handlers
    # ---------------------------------------------------------------------

    def OnListView_clickHandler(self, index):
        data = self.ui.listViewInstruments.model().itemData(index.row())
        self.ui.tableViewOHLC.setModel(data)


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
        dateString = self.ui.calendar.selectedDate().toString('yyyy-MM-dd')
        noteString = self.ui.textNote.toPlainText()

        if(noteString != ''):
            self.notesModel.insertRows(0, 1, [dateString, noteString])

    def OnExitAppAction_Handler(self, event):
        reply = QMessageBox.question(self, "Message", "Are you sure you want to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.close()


    #----------------------------------------------------------------------
    # Get/Set methods
    # ---------------------------------------------------------------------

    def getModel(self):
        return self.instrumentsModel