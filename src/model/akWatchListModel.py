from src.model.akInstrumentListModel import AkInstrumentListModel

defaultWatchListNames = "Default"

class AkWatchListModel(AkInstrumentListModel):
    def __init__(self):
        super(AkWatchListModel, self).__init__(items=defaultWatchListNames, parent=None)

