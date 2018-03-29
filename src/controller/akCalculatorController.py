from PyQt5 import uic
import sys
from PyQt5 import QtWidgets
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
        #self.setCentralWidget(self)
        self.setupConnections()


    #----------------------------------------------------------------------
    # Private methods
    # ---------------------------------------------------------------------

    def initUI(self):
        pass

    def loadData(self):
        pass


    def setupConnections(self):
        self.ui.actionHistoricalView.triggered.connect(self.OnShowHistoricalView_Handler)
        self.ui.actionInstrumentView.triggered.connect(self.OnShowInstrumentView_Handler)
        self.ui.actionConnectionsView.triggered.connect(self.OnShowConnectionsView_Handler)
        self.ui.actionConnect.triggered.connect(self.OnShowConnectActionView_Handler)
        self.ui.actionDisconnect.triggered.connect(self.OnShowDisconnectActionView_Handler)
        self.ui.actionOptionsView.triggered.connect(self.OnShowOptionsView_Handler)

        self.ui.btnOK.clicked.connect(self.OnAddNoteButtonClick_Handler)
    #----------------------------------------------------------------------
    # Event handlers
    # ---------------------------------------------------------------------

    def OnShowHistoricalView_Handler(self):
        print("AkHistoricalView called!")
        self.historicalController = AkHistoricalController()

    def OnShowInstrumentView_Handler(self):
        print("AkInstrumentView called!")
        self.instrumentsController = AkInstrumentsController()

    def OnShowConnectionsView_Handler(self):
        print("AkConnectionManagerController called!")
        self.connectionsController = AkConnectionsController()

    def OnShowConnectActionView_Handler(self):
        print("AkConnectViewController called!")
        self.connectActionController = AkConnectActionController()

    def OnShowDisconnectActionView_Handler(self):
        print("AkDisconnectViewController called!")
        self.disconnectActionController = AkDisconnectActionController()

    def OnShowOptionsView_Handler(self):
        print("AkOptionsController called!")
        self.optionsController = AkOptionsController()


    def OnAddNoteButtonClick_Handler(self):
        pass