from PyQt5 import QtWidgets
from src.views.ui_instrumentView import Ui_InstrumentsDialog


class AkInstrumentsController(QtWidgets.QDialog, Ui_InstrumentsDialog):
    def __init__(self, model=None):
        super(AkInstrumentsController, self).__init__()
        self.model = model
        self.setupUi()

        self._setup_connections()
        self._setup_model()

    #----------------------------------------------------------------------
    # Override methods
    # ---------------------------------------------------------------------

    def setupUi(self):
        super(AkInstrumentsController, self).setupUi(self)

        self.setModal(True)
        self.setWindowTitle("Instrument Data Manager")

    #----------------------------------------------------------------------
    # Private methods
    # ---------------------------------------------------------------------

    def _setup_connections(self):
        self.btnSearch.clicked.connect(self.OnSearchButton_click_Handler)
        self.btnSelectAll.clicked.connect(self.OnSelectAllButton_clickHandler)
        self.btnDeselectAll.clicked.connect(self.OnDeselectAllButton_clickHandler)
        self.btnOK.clicked.connect(self.OnOkButton_clickHandler)
        self.btnCancel.clicked.connect(self.OnCancelButton_clickHandler)
        self.btnNew.clicked.connect(self.OnNewButton_clickHandler)
        self.btnDelete.clicked.connect(self.OnDeleteButton_clickHandler)
        self.btnInsert.clicked.connect(self.OnInsertButton_clickHandler)
        self.btnRemove.clicked.connect(self.OnRemoveButton_clickHandler)

    def _setup_model(self):
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