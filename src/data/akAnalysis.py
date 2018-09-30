from src.data.akEnums import AkAnalysisType
from src.data.export.akExport import AkExport


class AkAnalysisFactory:
    """
    Фабрика типів аналізу.
    """
    factories = {}

    def create_analysis(analysis_type, instrument):
        """
        Метод створює екземпляр аналізу за типом 'type'.

        :param analysis_type: AkAnalysisType().
        :param instrument: AkInstrument().
        :return: virtual AkAnalysis() object.
        """
        if analysis_type not in AkAnalysisFactory.factories:
            AkAnalysisFactory.factories[analysis_type] = eval('Ak' + analysis_type.name + 'Analysis.Factory()')
        return AkAnalysisFactory.factories[analysis_type].create(instrument)

    create_analysis = staticmethod(create_analysis)


class AkAnalysis(object):
    """
    Базовий абстрактний клас для аналізу.
    """

    def __init__(self, instrument):
        self._periods = []
        self._instrument = instrument

    def name(self):
        """
        Метод повертає ім"я аналізу

        :return: str()
        """
        return self.type().name

    def type(self):
        pass

    @property
    def instrument(self):
        return self._instrument

    @property
    def periods(self):
        """
        Метод повертає список періодів аналізу.

        :return: list()
        """
        return self._periods

    def add_period(self, period):
        """
        Метод додає період 'period' до списку періодів аналізу.

        :param period: AkPeriod()
        """
        self._periods.append(period)

    def prepare_data(self, x_period):
        """
        Абстрактний метод підготовки даних для аналізу.

        :param x_period: AkPeriod()
        """
        pass

    def do_analyze(self):
        """
        Абстрактний метод аналізу даних.
        """
        pass

    def export(self, text_file):
        """
        Абстрактний метод для виводу даних.
        """
        pass

    def generate_periods(self, x_period, period_values):
        for value in period_values:
            if value == 1:
                self.add_period(x_period)
                continue
            new_period = x_period.create_period(value)
            self.add_period(new_period)


# ======================================================================================================================
# КАЛЕНДАРНИЙ АНАЛІЗ
# ======================================================================================================================
class AkCalendarAnalysis(AkAnalysis):
    """
    Реалізація класу КАЛЕНДАРНОГО АНАЛІЗУ.
    """

    def __init__(self, instrument):
        super(AkCalendarAnalysis, self).__init__(instrument)

    def type(self):
        """
        Метод повертає тип КАЛЕНДАРНОГО АНАЛІЗУ.
        """
        return AkAnalysisType.Calendar

    def prepare_data(self, x_period):
        """
        Підготовка даних для КАЛЕНДАРНОГО АНАЛІЗУ

        :param x_period: базовий період, DOHLC
        """
        self.add_period(x_period)

    def do_analyze(self):
        """
        Метод КАЛЕНДАРНОГО АНАЛІЗУ.
        """
        for period in self.periods:
            period.amplitudes()

    def export(self, text_file):
        """
        Вивід даних у .txt файл КАЛЕНДАРНОГО АНАЛІЗУ.

        :param text_file: .txt
        """
        if not text_file:
            return

        for period in self.periods:
            AkExport.print_period(period, period_amplitudes=True, file=text_file)

    class Factory:
        """
        Factory метод, повертає екземпляр КАЛЕНДАРНОГО АНАЛІЗУ.
        """

        @staticmethod
        def create(instrument):
            return AkCalendarAnalysis(instrument)


# ======================================================================================================================
# ПЕРІОДНИЙ АНАЛІЗ
# ======================================================================================================================
class AkPeriodAnalysis(AkAnalysis):
    """
    Реалізація класу ПЕРІОДНОГО АНАЛІЗУ.
    """

    def __init__(self, instrument):
        """
        Ініціалізація екземпляра класу ПЕРІОДНОГО АНАЛІЗУ.
        """
        super(AkPeriodAnalysis, self).__init__(instrument)

    def type(self):
        """
        Метод повертає тип ПЕРІОДНОГО АНАЛІЗУ.
        """
        return AkAnalysisType.Period

    def prepare_data(self, x_period):
        """
        Підготовка даних для ПЕРІОДНОГО АНАЛІЗУ.

        :param x_period: базовий період, DOHLC
        """

        values = self.instrument.period_values
        self.generate_periods(x_period, values)

    def do_analyze(self):
        """
        Метод ПЕРІОДНОГО АНАЛІЗУ.
        """
        for period in self.periods:
            # рахуємо амплітуди |HL|, OC для періоду
            period.amplitudes()

            # повертаємо список непорожніх структур OHLC, OLHC, UN
            # рахуємо попутно амплітуди структур, amplitudes=True/False, quantities=True/False
            period.structures(amplitudes=True, quantities=True)

    def export(self, text_file):
        """
        Вивід даних у .txt файл ПЕРІОДНОГО АНАЛІЗУ.

        :param text_file: .txt
        """

        for period in self.periods:
            AkExport.print_period(period, period_amplitudes=True, structures=True, structure_amplitudes=False,
                                  file=text_file)

    class Factory:
        """
        Factory метод, повертає екземпляр ПЕРІОДНОГО АНАЛІЗУ.
        """

        @staticmethod
        def create(instrument):
            return AkPeriodAnalysis(instrument)


# ======================================================================================================================
# СЕРІЙНИЙ АНАЛІЗ
# ======================================================================================================================
class AkSeriesAnalysis(AkAnalysis):
    """
    Реалізація класу СЕРІЙНОГО АНАЛІЗУ.
    """

    def __init__(self, instrument):
        super(AkSeriesAnalysis, self).__init__(instrument)

    def type(self):
        """
        Метод повертає тип СЕРІЙНОГО АНАЛІЗУ.
        """
        return AkAnalysisType.Series

    def prepare_data(self, x_period):
        """
        Підготовка даних для СЕРІЙНОГО АНАЛІЗУ.

        :param x_period: базовий період, DOHLC
        """

        values = self.instrument.period_values
        self.generate_periods(x_period, values)

    def do_analyze(self):
        """
            Метод СЕРІЙНОГО АНАЛІЗУ.
        """
        for period in self.periods:
            period.series_categories(amplitudes=True, structures=True, structure_amplitudes=True,
                                     structure_quantities=True)

    def export(self, text_file):
        """
        Вивід даних у .txt файл СЕРІЙНОГО АНАЛІЗУ.

        :param text_file: .txt
        """
        for period in self.periods:
            AkExport.print_series_categories(period, structures=True, structure_amplitudes=True,
                                             file=text_file)

    class Factory:
        """
        Factory метод, повертає екземпляр СЕРІЙНОГО АНАЛІЗУ.
        """

        @staticmethod
        def create(instrument):
            return AkSeriesAnalysis(instrument)


# ======================================================================================================================
# КОМБІНАЦІЙНИЙ АНАЛІЗ
# ======================================================================================================================

class AkCombinationsAnalysis(AkAnalysis):
    def __init__(self, instrument):
        super(AkCombinationsAnalysis, self).__init__(instrument)

    def type(self):
        return AkAnalysisType.Combinations

    def prepare_data(self, x_period):
        pass

    def do_analyze(self):
        pass

    class Factory:
        @staticmethod
        def create(instrument):
            return AkCombinationsAnalysis(instrument)

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
        ['2018-12-31', '24809.30', '26616.71', '23344.52', '25326.16']
    ]
