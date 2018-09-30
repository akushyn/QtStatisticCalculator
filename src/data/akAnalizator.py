from src.data.akAnalysis import AkAnalysisType
from src.data.akEnums import AkSelectionMethod
from src.data.akInstrument import AkInstrument


class AkAnalizator:

    def __init__(self, instrument=None):

        # інструмент для аналізу
        self._instrument = instrument

    @property
    def instrument(self):
        """
        Метод повертає інструмент аналізу.
        :return: AkInstrument()
        """
        return self._instrument

    @instrument.setter
    def instrument(self, instrument):
        self._instrument = instrument

    def do_analyze(self):
        if self.instrument:
            self._instrument.calculate()
            self._instrument.export_to_file()

if __name__ == '__main__':
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
