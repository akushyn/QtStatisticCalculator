from src.akFunctions import AkFunctions
from src.data import akAmplitude as Amplitude
from src.data import akStructure as Structure
from src.data.akEnums import AkSelectionMethod


class AkSeries(object):

    def __init__(self, value, components_x_data, parent):

        # значення серії
        self._value = value

        # дані компонент серії
        self._components_x_data = components_x_data

        # посилання на варіант періоду
        self._parent = parent

        # дані серії у зжатому вигляді
        self._x_data = []

    def value(self):
        """
        Метод повертає значення серії.
        :return: int
        """
        return self._value

    def components_x_data(self):
        """
        Метод повертає дані DOHLC компонентів серії.
        :return: [[],...] - DOHLC
        """
        return self._components_x_data

    @property
    def x_data(self):
        """
        Метод повертає дані серії у зжатому вигляді.
        :return: [[],...] - DOHLC
        """
        if self._x_data:
            return self._x_data

        # отримуємо рядок серії максимальної розмірності: 'period_value * series_value'
        # наприклад: якщо період 3У і серія +4, то на виході маємо рядок 12У періоду
        self._x_data = AkFunctions.fold(self.components_x_data(), self._parent.method())

        return self._x_data

    def length(self):
        """
        Метод повертає довжину серії.
        :return: int
        """
        return len(self._components_x_data)

    def start_date(self):
        """
        Метод повертає початкову дату серії.
        :return:
        """
        return self._components_x_data[1][0]

    def end_date(self):
        """
        Метод повертає кінцеву дату серії.
        :return:
        """
        return self._components_x_data[len(self._components_x_data) - 1][0]

    def __str__(self):
        s = ""
        s += "Series: " + str(self._value) + "\n"
        s += "Start Date: " + str(self.start_date()) + "\n"
        s += "End Date: " + str(self.end_date()) + "\n"

        return s


class AkSeriesCategory(object):
    def __init__(self, value, series, parent):

        # значення категорії серій
        self._value = value

        # список серій варіанту
        self._series = series

        # посилання на варіант періоду
        self._parent = parent

        # амплітуди серій категорії
        self._amplitudes = []

        # список структур OHLC, OLHC, UN серій категорії
        self._structures = []

    @property
    def x_data(self):
        """
        Метод повертає дані DOHLC серії.

        :return: [[],...]
        """
        x_data = []
        for s in self._series:
            x_data.append(s.x_data)

        return x_data

    def series(self):
        """
        Метод повертає список серій категорії.
        :return: [AkSeries(),...]
        """
        return self._series

    def components_x_data(self):
        """
        Метод повертає дані DOHLC компонент серій категорії.
        :return:
        """
        components = []

        # перебираємо серії категорії і формуємо список з компонент серій
        for s in self._series:
            components.append(s.components_x_data())

        return components

    def amplitudes(self):
        """
        Метод повертає значення амплітуд серій категорії.
        :return:
        """
        if self._amplitudes:
            return self._amplitudes

        # дані серій категорії
        x_data = self.x_data

        # типи амплітуд
        amplitude_types = AkSeriesCategory.amplitude_types()

        # точність обрахунків
        digits = self._parent.precision()

        # рахуємо амплітуди
        self._amplitudes = Amplitude.get_amplitudes(x_data, amplitude_types, digits)

        return self._amplitudes

    @staticmethod
    def amplitude_types():
        """
        Метод повертає типи амплітуд.
        :return:
        """
        return [AkSelectionMethod.absHL, AkSelectionMethod.OC]

    def structures(self, amplitudes=True, quantities=True):
        """
        Метод повертає список непорожніх структур: OHLC, OLHC, UN
        :return: [AkStructureEvents(),...]
        """
        if self._structures:
            return self._structures

        # дані серій категорії
        x_data = self.x_data

        # дані компонент серій категорії
        components_x_data = self.components_x_data()

        # рахуємо список структур
        structures_list = Structure.get_structures_list(x_data, components_x_data, self._parent)

        # рахуємо амплітуди структур
        if amplitudes:
            for s in structures_list:
                s.amplitudes()

        # рахуємо кількісні величини структур (positive, negative, zero) по методу ОС
        if quantities:
            for s in structures_list:
                s.quantities()

        # зберігаємо список структур
        self._structures = structures_list

        return self._structures

    def value(self):
        """
        Метод повертає значення серій категорії.

        :return: int
        """
        return self._value

    def count(self):
        """
        Метод повертає кількість серій у категорії.
        :return:
        """
        return len(self._series)

    def __str__(self):
        s = ""
        s += str(self._value) + ": " + str(self.count())

        return s


def get_compact_series(variant):
    """
    Метод повертає список об"єктів компактних серій послідовності для варіанту періода.

    :param variant: варіант періода
    :return: [AkSeries(),...]
    """

    # дані базового періоду
    base_x_data = variant.base_period_data()

    # повертаємо послідовність
    sequence = variant.sequence()

    # значення періоду
    period_value = variant.period_value()

    # значення варіанту періода
    variant_number = variant.number()

    series_list = []
    for i in range(len(sequence)):
        # рахуємо дистанцію тільки для елементів > 1 (необхідна умова компактності серії)
        if abs(sequence[i]) < 2:
            continue

        # рахуємо індекси даних серії
        from_index, to_index = get_series_data_indexes(i, sequence, period_value, variant_number)

        # створюємо об"єкт нової серії
        new_series = AkSeries(sequence[i], base_x_data[from_index: to_index + 1], parent=variant)

        # додаємо серію до результуючого списку
        series_list.append(new_series)

    return series_list


def get_series_data_indexes(index, sequence, period_value, variant_number):
    """
    Рахуємо індекси даних серії у послідовності.

    :param index: індекс елемента послідовності
    :param sequence: послідовність варіанта періоду
    :param period_value: значення періоду
    :param variant_number: номер варіанту
    :return: int, int.
    """

    # початкова значення індексів
    from_index = 0
    to_index = 0

    # список значень послідовності по модулю
    abs_sequence = [abs(x) for x in sequence]

    # перебираємо елементи зжатої послідовності
    for i in range(len(sequence)):
        # якщо досягнули індекс серії, то підрахунок відстані завершуємо
        if i >= index:
            from_index += sum(abs_sequence[:i]) * (period_value - 1) + variant_number
            to_index = from_index + abs(sequence[index]) * period_value
            break

        # для елементів послідовності '0', '-1', '+1' вага рівна 1
        if (sequence[i] == 0) or (sequence[i] == 1) or (sequence[i] == -1):
            from_index += 1
        else:
            from_index += abs(sequence[i])

    return from_index, to_index


def get_series_categories(variant, sorted_by_value=True):
    """
    Метод повертає список категорій серій.

    :param variant: варіант періоду
    :param sorted_by_value: сортувати категорії по значенню серії.

    :return: [AkSeriesCategory(min),... AkSeriesCategory(max)]
    """

    # повертаємо список компактних серій: [AkSeries(),...]
    # TODO : провірити дані серій
    series_list = get_compact_series(variant)

    if not series_list:
        return []

    # групуємо серії по типу
    groups = {}
    for s in series_list:
        value = s.value()
        if value in groups.keys():
            values = list(groups[value])
            values.append(s)
            groups[value] = values
        else:
            # нове значення серії
            groups[value] = [s]

    # категорії серій
    series_categories = []

    # повертаємо список значень серій
    series_values = groups.keys()

    # при необхідності, сортуємо групи по значенню від найменшого до найбільшого
    if sorted_by_value:
        series_values = sorted(groups.keys())

    for value in series_values:
        category = AkSeriesCategory(value, groups[value], parent=variant)
        series_categories.append(category)

    return series_categories


def get_quantities(series_list):
    """
    Метод повертає структуру даних <series number> : <events_count>,
    яка описує кількість подій для кожного значення серії.

    """

    # порахуємо групи серій
    group_list = get_series_categories(series_list)

    quantities = {}
    for group in group_list:
        quantities[group.number()] = group.events_count()

    return quantities
