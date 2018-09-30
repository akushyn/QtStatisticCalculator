from src.akFunctions import AkFunctions
from src.data.akAnalysis import AkAnalysisFactory
from src.data.akEnums import AkSelectionMethod
from src.data.akPeriod import AkPeriod
from src.data.export.akExport import AkExport
from typing import IO


class AkInstrument(object):
    """
    Реалізація класу ІНСТРУМЕНТ
    """
    def __init__(self, name, sources, analysis_types=list(), period_values=list(), method=AkSelectionMethod.CC,
                 precision=3):
        """
        Ініціалізація екземпляру класу ІНСТРУМЕНТ.

        :param name: str(). Ім"я інструменту.
        :param sources: [x_data, x_data,...]. Список даних інструменту.
        """

        # ім"я інструмента
        self._name = name

        # список базових періодів, завантажених зовні
        self._sources = sources

        # список типів аналізу інструмента
        self._analyzes = []

        # метод селекції даних інструмента
        self._method = method

        # точність обрахунків для інструмента
        self._precision = precision

        # список типів аналізу
        self._analysis_types = analysis_types

        # список значень періодів для аналізу
        self._period_values = period_values

    @property
    def name(self):
        """
        Метод повертає ім"я інструмента.

        :return: str()
        """
        return self._name

    @name.setter
    def name(self, name):
        """
        Метод встановлює ім"я інструмента.

        :param name: str()
        """
        self._name = name

    @property
    def analysis_types(self):
        """
        Метод повертає список типів аналізу інструмента.

        :return: [AkAnalysisType(),...]
        """
        return self._analysis_types

    @analysis_types.setter
    def analysis_types(self, analysis_types):
        """
        Метод встановлює список типів аналізу інструмента.

        :param analysis_types: [AkAnalysisType(),...]
        """

        self._analysis_types = analysis_types

    @property
    def period_values(self):
        """
        Метод повертає список значень періодів для аналізу інструмента.
        :return: [int, int,...]
        """
        if self._period_values:
            return self._period_values
        else:
            for source in self._sources:
                self._period_values = list(range(1, len(source)))

        return self._period_values

    @period_values.setter
    def period_values(self, period_values):
        """
        Метод встановлює список значень періодів для аналізу інструмента.
        :param period_values: [int, ...]
        """
        self._period_values = period_values

    @property
    def analyzes(self):
        """
        Метод повертає список об"эктів аналізів інструмента.
        :return: [AkAnalysis(), AkAnalysis()...]
        """
        return self._analyzes

    @property
    def method(self):
        """
        Метод повертає метод селекції даних для інструменту.
        :return: AkSelectionMethod()
        """
        return self._method

    @property
    def precision(self):
        """
        Метод повертає точність обрахунків інструмента.
        :return: int.
        """
        return self._precision

    def add_analysis(self, analysis):
        """
        Метод додає новий вид аналізу до списку аналізів інструмента.

        :param analysis: AkAnalysis()
        """
        if analysis and analysis not in self._analyzes:
            self._analyzes.append(analysis)

    @property
    def sources(self):
        """
        Метод повертає список базових періодів інструмента.

        :return: [x_data, ...]. Список даних DOHLC інструмента.
        """
        return self._sources

    def add_source(self, source):
        """
        Метод додає новий базовий період інструмента.

        :param source: дані DOHLC
        """
        self._sources.append(source)

    def source_type(self):
        source = self._sources[0]

        return AkFunctions.dataType(source[0][0], source[1][0])

    def calculate(self):
        """
        Вхідна точка обрахунків. Калькуляція необхідної інформація для інструмента.
        """

        for source in self._sources:
            x_period = AkPeriod(1, source, instrument=self)

            if not x_period.x_data:
                raise Exception("Invalid source data.")

            for analysis_type in self.analysis_types:
                analysis = AkAnalysisFactory.create_analysis(analysis_type, self)

                analysis.prepare_data(x_period)
                analysis.do_analyze()

                self.add_analysis(analysis)

    def export_to_file(self, ext='.txt'):
        for i in range(len(self._sources)):
            for analysis in self.analyzes:
                file_name = self.name + analysis.type().name + ext
                with open(file_name, "w+") as text_file:  # type: IO[str]
                    print('Instrument: ' + self.name, file=text_file)
                    print("", file=text_file)
                    print("Method: " + self.method.name, file=text_file)
                    print("Precision: " + str(self.precision), file=text_file)
                    AkExport.print_underline(len('Instrument: ' + self.name), "=", text_file=text_file)
                    print('', file=text_file)

                    analysis.export(text_file)
