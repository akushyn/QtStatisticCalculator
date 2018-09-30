import numpy as np
from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox

from src.controllers.akConnectActionController import AkConnectActionController, AkDisconnectActionController
from src.controllers.akConnectionsController import AkConnectionsController
from src.controllers.akHistoricalController import AkHistoricalController
from src.controllers.akInstrumentsController import AkInstrumentsController
from src.controllers.akOptionsController import AkOptionsController
from src.data.akAnalizator import AkAnalizator
from src.data.akAnalysis import AkAnalysisType
from src.models.akListModel import AkInstrumentListModel
from src.views.ui_calculatorMainView import Ui_CalculatorMainView


class AkCalculatorController(QtWidgets.QMainWindow, Ui_CalculatorMainView):
    def __init__(self):
        super(AkCalculatorController, self).__init__()
        self.setupUi()

        self.setupModel()
        self.setupConnections()
        self._setup_controllers()

    #----------------------------------------------------------------------
    # Private methods
    # ---------------------------------------------------------------------

    def setupUi(self):
        super(AkCalculatorController, self).setupUi(self)

        self.calendar.setGridVisible(True)

        self.notesTableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.notesTableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.graphicsView.setTitle('My Graph')
        self.graphicsView.setLabel('bottom', 'X axis')
        self.graphicsView.setLabel('left', 'Y axis')
        self.graphicsView.setBackground(QtGui.QColor(0, 0, 0))

        self.plotexample()

    #----------------------------------------------------------------------
    # Private methods
    # ---------------------------------------------------------------------

    def setupModel(self):
        self.instrumentsListModel = AkInstrumentListModel()
        self.instrumentsListView.setModel(self.instrumentsListModel)


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
        self.notesTableView.clicked.connect(self.OnNotesTable_clickHandler)
        self.btnCalculate.clicked.connect(self.OnCalculateButton_clickHandler)

        self.instrumentsListView.clicked.connect(self.onInstrumentListView_clickHandler)

    def _setup_controllers(self):
        self.instrumentsController = AkInstrumentsController()
        self.historicalController = AkHistoricalController(self.instrumentsListModel)
        self.connectionsController = AkConnectionsController()
        self.connectActionController = AkConnectActionController()
        self.disconnectActionController = AkDisconnectActionController()
        self.optionsController = AkOptionsController()

    def plotexample(self):
        a = np.array([1, 2, 3, 4, 5])
        b = np.array([6, 7, 8, 9, 10])
        self.graphicsView.plot(a, b)
        self.graphicsView.showGrid(x=True, y=True)



    #----------------------------------------------------------------------
    # Event handlers
    # ---------------------------------------------------------------------

    def onInstrumentListView_clickHandler(self):
        indexes = self.instrumentsListView.selectionModel().selectedIndexes()
        model = self.instrumentsListView.model()
        if (indexes):
            selection = indexes[0]
            instrument = model.itemData(selection)
            print(selection)

    def OnNotesTable_clickHandler(self, index):
        sellData = self.notesTableView.model().data(index, role=QtCore.Qt.DisplayRole)
        self.textNote.setPlainText(sellData)

    def OnCalculateButton_clickHandler(self):
        indexes = self.instrumentsListView.selectionModel().selectedIndexes()

        if (not indexes):
            self.statusbar.showMessage("No instrument selected", 3000)
            return

        instrumentListModel = self.instrumentsListView.model()
        selection = indexes[0]

        instrument = instrumentListModel.itemData(selection)

        analizator = AkAnalizator()
        analizator.set_instrument(instrument)

        analizator.setAnalysisTypes([AkAnalysisType.Series])
        analizator.do_analyze()

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
            self.notesTableModel.insertRows(0, 1, [dateString, noteString])

    def OnExitAppAction_Handler(self, event):
        reply = QMessageBox.question(self, "Message", "Are you sure you want to quit?", QMessageBox.Yes | QMessageBox.No, QMessageBox.No)

        if reply == QMessageBox.Yes:
            self.close()