class AkInstrument(object):
    def __init__(self, name='', data=[]):
        self._name = name

        self._series = {'D': [], 'W': [], 'M': [], 'Q': [], 'Y': []}
        self._dSeries = dSeries
        self._wSeries = wSeries
        self._mSeries = mSeries
        self._qSeries = qSeries
        self._ySeries = ySeries

    def getName(self):
        return self._name

    def setName(self, name):
        self._name = name

    def data(self):
        return self._data

    def setData(self, data):
        self._data = data