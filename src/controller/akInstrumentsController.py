from PyQt5 import QtWidgets, uic
from src.view.ui_instrumentView import Ui_Dialog

class AkInstrumentsController(QtWidgets.QDialog):
    def __init__(self):
        super(AkInstrumentsController, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.setModal(True)
        self.setWindowTitle("Instrument Data Manager")
        self.show()

        self.initUI()
        self.setupConnections()
        self.loadData()

    #----------------------------------------------------------------------
    # Private methods
    # ---------------------------------------------------------------------

    def initUI(self):
        pass

    def loadData(self):
        pass


    def setupConnections(self):
        self.ui.btnSearch.clicked.connect(self.OnSearchButton_click_Handler)
        self.ui.btnSelectAll.clicked.connect(self.OnSelectAllButton_clickHandler)
        self.ui.btnDeselectAll.clicked.connect(self.OnDeselectAllButton_clickHandler)
        self.ui.btnOK.clicked.connect(self.OnOkButton_clickHandler)
        self.ui.btnCancel.clicked.connect(self.OnCancelButton_clickHandler)
        self.ui.btnNew.clicked.connect(self.OnNewButton_clickHandler)
        self.ui.btnDelete.clicked.connect(self.OnDeleteButton_clickHandler)
        self.ui.btnInsert.clicked.connect(self.OnInsertButton_clickHandler)
        self.ui.btnRemove.clicked.connect(self.OnRemoveButton_clickHandler)

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
        print("OnCancelButton_clickHandler method called!")

    def OnNewButton_clickHandler(self):
        print("OnNewButton_clickHandler method called!")

    def OnDeleteButton_clickHandler(self):
        print("OnDeleteButton_clickHandler method called!")

    def OnInsertButton_clickHandler(self):
        print("OnInsertButton_clickHandler method called!")

    def OnRemoveButton_clickHandler(self):
        print("OnRemoveButton_clickHandler method called!")