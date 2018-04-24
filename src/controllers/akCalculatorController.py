from PyQt5 import QtWidgets, QtGui, QtCore
from PyQt5.QtWidgets import QMessageBox

from src.Functions import loadCSV
from src.controllers.akConnectActionController import AkConnectActionController, AkDisconnectActionController
from src.controllers.akConnectionsController import AkConnectionsController
from src.controllers.akHistoricalController import AkHistoricalController
from src.controllers.akInstrumentsController import AkInstrumentsController
from src.controllers.akOptionsController import AkOptionsController
from src.data.akInstrumentNode import AkInstrumentNode, AkSection, AkSectionType
from src.data.akSeriality import AkSequence
from src.models.akListModel import AkInstrumentListModel
from src.models.akTableModel import AkInstrumentOHLCModel, AkTableModel, AkNotesModel
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

        self.graphicsView.setTitle('My Graph')
        self.graphicsView.setLabel('bottom', 'X axis')
        self.graphicsView.setLabel('left', 'Y axis')
        self.graphicsView.setBackground(QtGui.QColor(0, 0, 0))

        self.plotexample()

    #----------------------------------------------------------------------
    # Private methods
    # ---------------------------------------------------------------------

    def _setup_model(self):
        fileName = "G:/Programming/Projects/QtStatisticCalculator/src/resources/^spx_y.csv"
        headers, data = func.loadCSV(fileName)
        items = AkInstrumentOHLCModel(func.getShortName(fileName), data, headers)

        self.instrumentsModel = AkInstrumentListModel([items])
        self.notesModel = AkNotesModel()


        self.notesTableView.setModel(self.notesModel)
        self.instrumentsListView.setModel(self.instrumentsModel)

        rootNode = AkInstrumentNode("Instruments")

        _eurusd = AkInstrumentNode("EURUSD", rootNode)
        _gbpusd = AkInstrumentNode("GBPUSD", rootNode)
        _gold = AkInstrumentNode("GOLD", rootNode)

        instruments = []
        instruments.append(_eurusd)
        instruments.append(_gbpusd)
        instruments.append(_gold)

        for i in range(3):
            dSection = AkSection('D', instruments[i])
            dSection = AkSection('W', instruments[i])
            dSection = AkSection('M', instruments[i])
            dSection = AkSection('Q', instruments[i])


        treeModel = AkInstrumentGraphModel(rootNode)
        self.instrumentsTreeView.setModel(treeModel)


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
        self.instrumentsListView.clicked.connect(self.OnListView_clickHandler)
        self.notesTableView.clicked.connect(self.OnNotesTable_clickHandler)
        self.btnCalculate.clicked.connect(self.OnCalculateButton_clickHandler)

    def _setup_controllers(self):
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

                serialityInfo = model.getSerialityInfo(selection)

                with open("Output.txt", "w") as text_file:
                    print("Instrument:", serialityInfo.getInstrumentName(), file=text_file)
                    print("Sequence: ", serialityInfo.getSequence().sequence(), file=text_file)
                    print("Min: ", serialityInfo.getIndexes().min(), file=text_file)
                    print("Max: ", serialityInfo.getIndexes().max(), file=text_file)

                    for degree in serialityInfo.getIndexes().degrees():
                        print("Quantity[", degree, "]= ", serialityInfo.getIndexes().quantity(degree), file=text_file)

                    print("Degrees: ", serialityInfo.getIndexes().degrees(), file=text_file)
                    print("Indexes Matrix: ", serialityInfo.getIndexes().matrix(), file=text_file)


                    ohlcDictionary = serialityInfo.getOHLC()
                    datesDictionary = serialityInfo.getDates()

                    print("", file=text_file)
                    print("--------------------------------------------------", file=text_file)
                    for degree in ohlcDictionary.degrees():
                        print("Seriality:", degree, file=text_file)
                        print("Quantity:", serialityInfo.getIndexes().quantity(degree), file=text_file)
                        print("Events start dates:", datesDictionary.dates(degree), file=text_file)

                        lst = ohlcDictionary.ohlc(degree)
                        for i in range(len(lst)):
                            print(lst[i], file=text_file)
                        print("", file=text_file)



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