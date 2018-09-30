from src.data import akAmplitude as Amplitude
from src.data import akSequence as Sequence
from src.data import akSeries as Series
from src.data import akStructure as Structure


class AkVariant:
    """
    Реалізація класу варіанта періода.
    Кожен період має один або кілька можливих варіантів.

    Базовий період має один варіант - вихідні дані.
    Період 2 має не більше 2х варіантів і тд.

    Максимальна кількість варіантів не може перевищувати значення періоду, до якого варіант належить.

    """

    def __init__(self, number, x_data, parent):
        # порядковий номер варіанту
        self._number = number

        # період, до якого належить даний варіант
        self._parent = parent

        # дані варіанту
        self._x_data = x_data

        # амплітуди варіанту періода
        self._amplitudes = []

        # список структур OHLC, OLHC, UN
        self._structures = []

        # зжата послідовність варіанту
        self._sequence = []

        # групи серій, згруповані по значенню серії
        self._series_categories = []

        # словник пар <значення серії> : <кількість серій> категорій варіанта
        self._series_quantities = {}

    @property
    def x_data(self):
        """
        Таблиця даних DOHLC варіанту.

        :return: [row1...rowN]
        """
        return self._x_data

    def number(self):
        """
        Метод повертає значення номера варіанту в періоді.

        :return: int.
        """
        return self._number

    def length(self):
        """
        Метод повертає кількість даних DOHLC варіанту.

        :return: int.
        """
        return len(self._x_data)

    def amplitudes(self):
        """
        Метод повертає амплітуди данних DOHLС варіанту періода для типів 'types'.

        :return: [AkAmplitude(), ...]
        """

        if not self._amplitudes:
            precision = self.precision()
            self._amplitudes = Amplitude.get_amplitudes(self._x_data, self._parent.amplitude_types(), digits=precision)

        return self._amplitudes

    def sequence(self):
        """
        Метод повертає зжату послідовність варіанту періоду.

        :return: [int,...]
        """
        if self._sequence:
            return self._sequence

        base_data = False
        if self.is_base_period():
            base_data = True

        self._sequence = Sequence.get_sequence(self._x_data, self.method(), base_data=base_data)

        return self._sequence

    def period_value(self):
        return self._parent.value

    def base_period_data(self):
        return self._parent.base_data()

    def is_base_period(self):
        if self._parent.is_base():
            return True

        return False

    def precision(self):
        return self._parent.instrument.precision

    def method(self):
        return self._parent.instrument.method

    def components_x_data(self):

        base_x_data = self.base_period_data()
        period_value = self.period_value()
        variant_number = self.number()

        components = []
        for i in range(self.length()):
            if i == 0 and (variant_number == 0):
                # повертаємо компоненти базового періоду для варіанту
                component = base_x_data[i * period_value: i * period_value + period_value + 1]
            else:
                component = base_x_data[
                            i * period_value + variant_number + 1: i * period_value + period_value + variant_number + 1]

            components.append(component)

        return components

    def structures(self, amplitudes=False, quantities=False):
        """
        Метод повертає список непорожніх структур OHLC, OLHC, UN варіанту періоду.

        :param: amplitudes. Визначає, чи рахувати набір амплітуд для варіанту періоду.
        :return: [AkStructure(), ...]
        """
        if self._structures:
            return self._structures

        if self.is_base_period():
            return []

        # дані варіанту
        x_data = self.x_data

        # дані компонент варіанту
        components_x_data = self.components_x_data()

        # повертаємо список непорожніх структур (OHLC, OLHC, UN) варіанту: [AkStructure(),...]
        structures_list = Structure.get_structures_list(x_data, components_x_data, self)

        # рахуємо амплітуди структур
        if amplitudes:
            for s in structures_list:
                s.amplitudes()

        # рахуємо кількість структур (positive, negative, zero) по методу ОС
        if quantities:
            for s in structures_list:
                s.quantities()

        # отримуємо список непорожніх структур OHLC, OLHC, UN варіанту періода
        self._structures = structures_list

        return self._structures

    def series_categories(self, amplitudes=False, structures=False, structure_amplitudes=False,
                          structure_quantities=False):
        """
        Метод повертає список категорій серій.
        Для кожної категорії серій в залежності від вхідних параметрів рахуємо амплітуди,
        структури, амплітуди структур і кількісні величини структур.

        :param amplitudes: bool - рахуємо динаміку серій категорії.
        :param structures: bool - рахуємо структури серій категорії
        :param structure_amplitudes: bool - рахуємо амплітуди структур.
        :param structure_quantities: bool - рахуємо кількісні величини структур

        :return: [AkSeriesCategory(),...] - список категорій серій варіанту
        """
        # якщо категорії серій пораховані раніше
        if self._series_categories:
            return self._series_categories

        # список категорій серій [AkSeriesCategory(),...]
        categories = Series.get_series_categories(variant=self)

        if not categories:
            return []

        # рахуємо попутно динаміку серій |HL|, OC
        if amplitudes:
            for category in categories:
                category.amplitudes()

        # визначаємо структури і динаміку структур
        if structures:
            for category in categories:
                category.structures(amplitudes=structure_amplitudes, quantities=structure_quantities)

        self._series_categories = categories

        return self._series_categories

    def series_quantities(self):
        """
        Метод повертає словник пар <значення серії> : <кількість серій> всіх категорій варіанта
        :return: {<series_value>: <series_count>, ...}
        """
        if self._series_quantities:
            return self._series_quantities

        quantities = {}
        for category in self.series_categories():
            quantities[category.value()] = category.count()

        self._series_quantities = quantities

        return self._series_quantities
