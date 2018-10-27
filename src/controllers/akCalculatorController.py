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
from src.data.akEnums import AkSelectionMethod
from src.data.akInstrument import AkInstrument
from src.models.akListModel import AkInstrumentListModel
from src.views.ui_calculatorMainView import Ui_CalculatorMainView


class AkCalculatorController(QtWidgets.QMainWindow, Ui_CalculatorMainView):
    def __init__(self):
        super(AkCalculatorController, self).__init__()
        super(AkCalculatorController, self).setupUi(self)

        self._instruments_list_model = AkInstrumentListModel()
        self._historical_view_controller = AkHistoricalController(self)

        self.setup_ui()


        self.instruments_list_view.setModel(self._instruments_list_model)

        # connections
        self.action_historical_view.triggered.connect(self.show_historical_view)
        self.calculate_button.clicked.connect(self.calculate_button_clicked)

    def setup_ui(self):
        """
        Метод ініціалізує компоненти основного вікна.
        :return:
        """

        self.journal_calendar.setGridVisible(True)

        self.journal_notes_table.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self.journal_notes_table.horizontalHeader().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        #self.graphicsView.setTitle('My Graph')
        #self.graphicsView.setLabel('bottom', 'X axis')
        #self.graphicsView.setLabel('left', 'Y axis')
        #self.graphicsView.setBackground(QtGui.QColor(0, 0, 0))

        #self.plotexample()

    #----------------------------------------------------------------------
    # Private methods
    # ---------------------------------------------------------------------

    def get_instruments_model(self):
        return self._instruments_list_model

    def setup_connections(self):
        pass
        # Main menu events
        #-----------------
        #self.historical_view_action.triggered.connect(self.show_historical_view())
        #self.instruments_view_action.triggered.connect(self.show_instruments_view())



        #self.actionHistoricalView.triggered.connect(self.show_historical_view)
        #self.actionInstrumentView.triggered.connect(self.show_instruments_view)
        #self.actionConnectionsView.triggered.connect(self.show_connections_view)
        #self.actionConnect.triggered.connect(self.OnShowConnectActionView_Handler)
        #self.actionDisconnect.triggered.connect(self.OnShowDisconnectActionView_Handler)
        #self.actionOptionsView.triggered.connect(self.OnShowOptionsView_Handler)
        #self.actionExit.triggered.connect(self.OnExitAppAction_Handler)

        #self.btnOK.clicked.connect(self.OnAddNoteButtonClick_Handler)
        #self.notesTableView.clicked.connect(self.OnNotesTable_clickHandler)


        #self.instrumentsListView.clicked.connect(self.onInstrumentListView_clickHandler)

    def setup_controllers(self):
        self._instruments_controller = AkInstrumentsController()
        #self._historical_controller = AkHistoricalController(self.instrumentsListModel)
        #self.connectionsController = AkConnectionsController()
        #self.connectActionController = AkConnectActionController()
        #self.disconnectActionController = AkDisconnectActionController()
        #self.optionsController = AkOptionsController()


        self.setup_connections()


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

    def calculate_button_clicked(self):
        #indexes = self.instrumentsListView.selectionModel().selectedIndexes()

        #if not indexes:
        #    self.statusbar.showMessage("No instrument selected", 3000)
        #    return

        #instrumentListModel = self.instrumentsListView.model()
        #selection = indexes[0]

        #instrument = instrumentListModel.itemData(selection)


        xData = [
            ['1999-12-31', '9212.80', '11568.80', '8994.30', '11497.10'],
            ['2000-12-29', '11501.80', '11750.30', '9651.68', '10786.80'],
            ['2001-12-31', '10790.90', '11350.00', '8062.34', '10021.50'],
            ['2002-12-31', '10021.70', '10673.10', '7197.49', '8341.63'],
            ['2003-12-31', '8342.38', '10462.40', '7416.64', '10453.90'],
            ['2004-12-31', '10452.70', '10868.10', '9708.40', '10783.00'],
            ['2005-12-30', '10783.80', '10984.50', '10000.50', '10717.50'],
            ['2006-12-29', '10718.30', '12529.90', '10661.20', '12463.20'],
            ['2007-12-31', '12459.50', '14198.10', '11939.60', '13264.80'],
            ['2008-12-31', '13261.80', '13279.50', '7449.38', '8776.39'],
            ['2009-12-31', '8772.25', '10580.30', '6469.95', '10428.00'],
            ['2010-12-31', '10430.70', '11625.00', '9614.32', '11577.51'],
            ['2011-12-30', '11577.43', '12876.00', '10404.49', '12217.56'],
            ['2012-12-31', '12221.19', '13661.87', '12035.09', '13104.14'],
            ['2013-12-31', '13104.30', '16588.25', '13104.30', '16576.66'],
            ['2014-12-31', '16572.17', '18103.45', '15340.69', '17823.07'],
            ['2015-12-31', '17823.07', '18351.36', '15370.33', '17425.03'],
            ['2016-12-30', '17405.48', '19987.63', '15450.56', '19762.60'],
            ['2017-12-29', '19872.90', '24876.07', '19677.94', '24719.22'],
            ['2018-12-31', '24809.30', '26616.71', '23344.52', '25326.16']]

        analysis_list = [AkAnalysisType.Calendar, AkAnalysisType.Period, AkAnalysisType.Series]
        instrument_ = AkInstrument("DJ", sources=[xData], analysis_types=analysis_list, method=AkSelectionMethod.CC,
                                   precision=3)

        analizator = AkAnalizator()
        analizator.instrument = instrument_

        analizator.do_analyze()

    def show_historical_view(self):
        self._historical_view_controller.show()

    def show_instruments_view(self):
        if (self._instruments_controller):
            self._instruments_controller.show()

    def show_connections_view(self):
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