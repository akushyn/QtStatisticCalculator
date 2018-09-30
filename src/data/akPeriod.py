from src.akFunctions import AkFunctions
from src.data.akEnums import AkSelectionMethod
from src.data.akVariant import AkVariant
from src.models.akTableModel import AkTableModel


class AkPeriod(AkTableModel):

    default_headers = ["Date", "Open", "High", "Low", "Close"]

    def __init__(self, value, x_data, instrument=None, base_period=None, headers=default_headers, parent=None):
        super(AkPeriod, self).__init__("", x_data, headers, parent)

        # значення періоду
        self._value = value

        # базовий період
        self._basePeriod = base_period

        # зберігаємо посилання на інструмент аналізу
        self._instrument = instrument

        # дані поточного періоду DOHLC
        self._x_data = x_data

        # варіанти періоду
        self._variants = []

        self._seriesList = []
        self._seriesGroupList = []  # список груп серій, згрупованих по ключу, де ключ - значення серії

    def base_period(self):
        """
        Метод повертає базовий період для поточного періода.

        :return: AkPeriod()
        """
        return self._basePeriod

    @property
    def instrument(self):
        return self._instrument

    @property
    def x_data(self):
        """
        Таблиця даних DOHLC періоду.
        :return: [row1...rowN]
        """
        return self._x_data

    def base_data(self):
        if self.is_base():
            return self.x_data

        return self.base_period().x_data

    @property
    def value(self):
        """
        Метод повертає значення періоду.
        :return: int.
        """
        return self._value

    def amplitudes(self):
        """
        Метод повертає список амплітуд данних DOHLС для кожного варіанту періода для типів 'types'.
        """

        # результуючий список списків амплітуд
        amplitudes = []
        for variant in self.variants():
            # рахуємо амплітуди |HL|, OC для варіанту періоду
            amplitudes.append(variant.amplitudes())

        return amplitudes

    def amplitude_types(self):
        if self.is_base():
            return [AkSelectionMethod.GAP, AkSelectionMethod.absHL, AkSelectionMethod.OC]

        else:
            return [AkSelectionMethod.absHL, AkSelectionMethod.OC]

    def sequences(self):
        """
        Метод повертає список зжатих послідовностей для кожного варіанту періоду.
        """

        # результуючий список послідовностей
        sequences = []

        for variant in self.variants():
                sequences.append(variant.sequence())

        return sequences

    def structures(self, amplitudes=False, quantities=False):
        """
        Метод повертає список списків непорожніх структур OHLC, OLHC, UN для всіх варіантів періоду.

        :param: amplitudes. Визначає, чи рахувати амплітуди структур чи ні.
        :return: [AkStructure(), ...]
        """

        # якщо період базовий, то структури не рахуємо
        if self.is_base():
            return []

        # список списків структур для всіх варіантів періоду
        structures = []

        for variant in self.variants():
            structures.append(variant.structures(amplitudes, quantities))

        return structures

    def series_categories(self, amplitudes=True, structures=True, structure_amplitudes=True, structure_quantities=True):

        categories_list = []
        for variant in self.variants():
            categories = variant.series_categories(amplitudes, structures, structure_amplitudes, structure_quantities)

            if categories:
                categories_list.append(categories)

        return categories_list

    def get_name(self):
        """
        Метод повертає ім"я періоду: <тип>+<значення>
        :return: str.
        """
        return self.instrument.source_type().name + str(self.value)

    def is_base(self):
        if self._value == 1:
            return True

        return False

    def length(self):
        """
        Метод повертає кількість стрічок DOHLC даних періоду.
        :return: int.
        """
        return len(self.x_data)

    def variants(self):
        """
        Метод рахує і повертає унікальні варіанти даних періоду.

        :return: [AkVariant(), AkVariant(),...]
        """

        # якщо варіанти вже були пораховані раніше, то повертаємо пораховані
        if self._variants:
            return self._variants

        # якщо період базовий, то варіант один - вихідні дані
        if self._value == 1:
            self._variants = [AkVariant(0, self.x_data, self)]
            return self._variants

        variants = []
        for i in range(self._value):
            variant = []
            j = i
            while j < len(self.x_data):    # цикл по даним DOHLC
                variant.append(self.x_data[j])
                j += self._value

            if variant:
                variants.append(AkVariant(i, variant, self))

        self._variants = variants

        return variants

    def create_period(self, value):
        """
        Метод створює новий період на основі базового через алгоритм згортки даних.

        :param value: int. Значення періоду, який формується.
        :return: AkPeriod(value)
        """

        # якщо період не базовий, згортку не виконуємо
        if self._value > 1:
            return None

        if not self.is_base():
            raise Exception("Invalid base period.")

        # формуємо дані нового періоду
        new_data = AkPeriod.data_selection(self.base_data(), value, self.instrument.method)

        return AkPeriod(value=value, x_data=new_data, instrument=self.instrument, base_period=self)

    @classmethod
    def data_selection(cls, base_x_data, period_value, method):
        """
        Метод формує через згортку дані нового періоду.

        :param base_x_data: Дані базового періоду
        :param period_value: Значення періоду, який формуємо
        :param method: Метод селекції даних.
        :return: [[],...] - Дані сформованого періоду
        """
        # дані нового періоду
        new_data = []

        # метод селекції Close[i] - Close[i-1]
        if method == AkSelectionMethod.CC:
            # в циклі формуємо нові дані
            for i in range(len(base_x_data) - period_value):
                # вибираємо дані з базового періоду
                items = base_x_data[i:i + period_value + 1]

                # формуємо новий рядок через злиття
                item = AkFunctions.fold(items, method)
                new_data.append(item)

        # метод селекції Close[i] - Open[i]
        elif method == AkSelectionMethod.OC:
            # в циклі формуємо нові дані
            for i in range(len(base_x_data) - period_value + 1):
                # вибираємо дані з базового періоду
                items = base_x_data[i:i + period_value]

                # формуємо новий рядок через злиття
                item = AkFunctions.fold(items, method)
                new_data.append(item)

        return new_data

    def title(self):
        return str("Period: " + self.get_name() + "(" + self.instrument.source_type().value + ")")
