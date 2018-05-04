from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox

from src.Functions import loadCSV
from src.controllers.akConnectActionController import AkConnectActionController, AkDisconnectActionController
from src.controllers.akConnectionsController import AkConnectionsController
from src.controllers.akHistoricalController import AkHistoricalController
from src.controllers.akInstrumentsController import AkInstrumentsController
from src.controllers.akOptionsController import AkOptionsController
from src.data.akAmplitudeDictionary import AkAmplitudeDictionary, AkCalculationMode
from src.data.akInstrument import AkInstrument
from src.data.akNode import AkNode
from src.models.akListModel import AkInstrumentListModel
from src.models.akTableModel import AkInstrumentTableModel, AkTableModel, AkNotesTableModel
from src.models.akTreeModel import AkInstrumentGraphModel
from src.views.ui_calculatorMainView import Ui_CalculatorMainView
import numpy as np
from src import Functions as func

class AkCalculatorController(QtWidgets.QMainWindow, Ui_CalculatorMainView):
    def __init__(self):
        super(AkCalculatorController, self).__init__()
        self.setupUi()

        self._setup_model()
        self._setup_connections()
        self._setup_controllers()

    #----------------------------------------------------------------------
    # Private methods
    # ---------------------------------------------------------------------

    def setupUi(self):
        super(AkCalculatorController, self).setupUi(self)

        self.calendar.setGridVisible(True)

        self.notesTableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.notesTableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.ohlcTableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.ohlcTableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.olhcTableView.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.olhcTableView.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        self.graphicsView.setTitle('My Graph')
        self.graphicsView.setLabel('bottom', 'X axis')
        self.graphicsView.setLabel('left', 'Y axis')
        self.graphicsView.setBackground(QtGui.QColor(0, 0, 0))

        self.plotexample()

    #----------------------------------------------------------------------
    # Private methods
    # ---------------------------------------------------------------------

    def _setup_model(self):
        self.notesTableModel = AkNotesTableModel()
        self.notesTableView.setModel(self.notesTableModel)

        rootNode = AkNode("Root")
        self._instrumentsTreeModel = AkInstrumentGraphModel(rootNode, headers=["Instruments"])
        self.instrumentsTreeView.setModel(self._instrumentsTreeModel)

    def _setup_connections(self):

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
        self.instrumentsTreeView.clicked.connect(self.OnTreeView_clickHandler)
        self.notesTableView.clicked.connect(self.OnNotesTable_clickHandler)
        self.btnCalculate.clicked.connect(self.OnCalculateButton_clickHandler)

    def _setup_controllers(self):
        self.instrumentsController = AkInstrumentsController()
        self.historicalController = AkHistoricalController(self._instrumentsTreeModel)
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

    def OnInstrumentSelection_changedHandler(self):
        print('OnInstrumentSelection_changedHandler')

    def OnContextMenuButton_clickHandler(self):
        pass

    def OnTreeView_clickHandler(self, index):
        index = self.instrumentsTreeView.selectedIndexes()[0]
        model = index.model()
        item = model.getNode(index)

        if (item.typeNode() == 'PERIOD'):
            if (item.ohlcModel().rowCount() > 0):
                self.ohlcTableView.setModel(item.ohlcModel())
                self.ohlcTableView.verticalHeader().setVisible(True)
            else:
                self.ohlcTableView.verticalHeader().setVisible(False)
                self.ohlcTableView.setModel(AkInstrumentTableModel())

            if (item.olhcModel().rowCount() > 0):
                self.olhcTableView.setModel(item.olhcModel())
                self.olhcTableView.verticalHeader().setVisible(True)
            else:
                self.olhcTableView.verticalHeader().setVisible(False)
                self.olhcTableView.setModel(AkInstrumentTableModel())

        else:
            self.ohlcTableView.verticalHeader().setVisible(False)
            self.ohlcTableView.setModel(AkInstrumentTableModel())

            self.olhcTableView.verticalHeader().setVisible(False)
            self.olhcTableView.setModel(AkInstrumentTableModel())

    def OnNotesTable_clickHandler(self, index):
        sellData = self.notesTableView.model().data(index, role=QtCore.Qt.DisplayRole)
        self.textNote.setPlainText(sellData)

    def OnCalculateButton_clickHandler(self):
        indexes = self.instrumentsTreeView.selectionModel().selectedIndexes()
        model = self.instrumentsTreeView.model()
        if (not indexes):
            self.statusbar.showMessage("No instrument selected", 3000)
            return

        selection = indexes[0]
        model.exportToFile(selection)

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