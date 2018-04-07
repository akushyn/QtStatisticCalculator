class AkInstrument(object):
    def __init__(self, name, data):
        self._name = name
        self._data = data


    def name(self):
        return self._name

    def setName(self, name):
        self._name = name

    def data(self):
        return self._data

    def setData(self, data):
        self._data = data