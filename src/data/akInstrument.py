from src.data.akNode import AkNode
from src.models.akTableModel import AkInstrumentTableModel
import src.Functions as func

class AkInstrument(AkNode, AkInstrumentTableModel):
    def __init__(self, name, items=[[]], headers=[], parent=None):
        AkNode.__init__(self, name, parent)
        AkInstrumentTableModel.__init__(self, name, items, headers, parent)

        self._items = items
        self.setupPeriods()

    def setupPeriods(self):
        self._daySection = AkSection("periods", self)

        for i in range(1, len(self._items) + 1):
            ohlc, olhc, undetermined = self.undeterminedAnalysis(i)
            AkPeriod(name='D' + str(i), ohlcItems=ohlc, olhcItems=olhc, undetermined=undetermined, parent=self._daySection)

            with open('D' + str(i) + '.txt', "w") as text_file:
                print('Instrument: ', self.name(), file=text_file)
                print('Period =', i, file=text_file)
                print('', file=text_file)

                print('OHLC:', file=text_file)
                self.display(ohlc, file=text_file)

                print('', file=text_file)
                print('OLHC:', file=text_file)
                self.display(olhc, file=text_file)

                print('', file=text_file)
                print('Undetermined:', file=text_file)
                self.display(undetermined, file=text_file)

    def undeterminedAnalysis(self, period):
        ohlc = []
        olhc = []
        undetermined = []

        # length of base table - D1
        length = len(self._items)

        for i in range(length - period + 1):
            items = self._items[i:i + period]

            max = items[0][2]
            maxIdx = 0

            min = items[0][3]
            minIdx = 0
            for j in range(1,len(items)):
                if (float(items[j][2]) > float(max)):
                    max = items[j][2]
                    maxIdx = j
                elif (float(items[j][3]) < float(min)):
                    min = items[j][3]
                    minIdx = j

            row = self.folding(items)

            if (minIdx > maxIdx):
               ohlc.append(row)
            elif (maxIdx > minIdx):
                olhc.append(row)
            else:
                undetermined.append(row)

        return ohlc, olhc, undetermined


    def folding(self, items):
        date = items[len(items) - 1][0]
        open = items[0][1]
        high = func.max(items)
        low = func.min(items)
        close = items[len(items)-1][4]

        row = []
        row.append(date)
        row.append(open)
        row.append(high)
        row.append(low)
        row.append(close)

        return row

    def display(self, list, file=None):
        if (list == []):
            print('[]', file=file)

        for row in list:
            print(row, file=file)

    def typeNode(self):
        return "INSTRUMENT"

class AkSection(AkNode):
    def __init__(self, name, parent=None):
        super(AkSection, self).__init__(name, parent)

    def typeNode(self):
        return "SECTION"

class AkPeriod(AkNode):
    __defaultHeaders = ["Date", "Open", "High", "Low", "Close"]
    def __init__(self, name, ohlcItems=[[]], olhcItems=[[]], undetermined=[[]], headers=__defaultHeaders, parent=None):
        super(AkPeriod, self).__init__(name, parent)

        self._ohlcModel = AkInstrumentTableModel(name, ohlcItems, headers, None)
        self._olhcModel = AkInstrumentTableModel(name, olhcItems, headers, None)
        self._undeterminedModel = AkInstrumentTableModel(name, undetermined, headers, None)

    def ohlcModel(self):
        return self._ohlcModel

    def olhcModel(self):
        return self._olhcModel

    def undeterminedModel(self):
        return self._undeterminedModel

    def typeNode(self):
        return "PERIOD"

if __name__ == '__main__':
    numbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]

    period = 4

