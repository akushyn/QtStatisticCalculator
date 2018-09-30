from src.akFunctions import AkFunctions
from src.data import akAmplitude as Amplitude
from src.data.akAmplitude import AkSelectionMethod
from src.data.akEnums import AkStructureSignType, AkStructureType


class AkStructureEvents(object):
    def __init__(self, events_x_data, structure_type, parent):

        # список подій структури
        self._events_x_data = events_x_data

        # тип структур
        self._structure_type = structure_type

        # для кого створений об"єкт структура (variant / series)
        self._parent = parent

        # амплітуди структур
        self._amplitudes = []

        self._quantities = {}

    def structure_type(self):
        return self._structure_type

    def get_name(self):
        return self.structure_type().value

    def amplitudes(self):
        """
        Метод повертає амплітуди структур.

        :return: [AkAmplitude(type),...]
        """

        if not self._amplitudes:
            precision = self._parent.precision()
            self._amplitudes = Amplitude.get_amplitudes(self._events_x_data, self.amplitude_types(), digits=precision)

        return self._amplitudes

    def amplitude_types(self):
        """
        Метод повертає список типів амплітуд, які потрібно порахувати для даного типу структур.

        :return: [AkAmplitudeType(), AkAmplitudeType(),...]
        """
        if self._structure_type == AkStructureType.OHLC:
            return [AkSelectionMethod.OH, AkSelectionMethod.HL, AkSelectionMethod.LC, AkSelectionMethod.OC]

        elif self._structure_type == AkStructureType.OLHC:
            return [AkSelectionMethod.OL, AkSelectionMethod.LH, AkSelectionMethod.HC, AkSelectionMethod.OC]

        elif self._structure_type == AkStructureType.UN:
            return [AkSelectionMethod.absHL, AkSelectionMethod.OC]

        raise Exception('The type of structure is incorrect.')

    def events_x_data(self):
        """
        Метод повертає дані подій структури

        :return: [[],...] - список даних DOHLC
        """
        return self._events_x_data

    def events_count(self):
        """
        Метод повертає кількість подій структури.

        :return: int.
        """
        return len(self._events_x_data)

    def positive_count(self):
        """
        Метод повертає кількість подій по методу OC > 0.

        :return: int.
        """
        return self.quantities()[AkStructureSignType.Positive.name]

    def negative_count(self):
        """
        Метод повертає кількість подій по методу ОС < 0

        :return: int.
        """
        return self.quantities()[AkStructureSignType.Negative.name]

    def zero_count(self):
        """
        Метод повертає кількість подій по методу ОС = 0

        :return: int.
        """
        return self.quantities()[AkStructureSignType.Zero.name]

    def quantities(self):
        """
        Метод повертає словних непорожніх кількостей подій (positive_count, negative_count, zero_count) по методу ОС.

        :return: {positive_count: int, negative_count: int, zero_count: int}
        """
        if self._quantities:
            return self._quantities

        # амплітуда ОС для подій структури
        points = Amplitude.get_amplitude(self.events_x_data(), AkSelectionMethod.OC).points()

        # лічильники positive_count, negative_count, zero_count
        positive_count = 0
        negative_count = 0
        zero_count = 0

        for point in points:
            if point > 0:
                positive_count += 1
            elif point < 0:
                negative_count += 1
            else:
                zero_count += 1

        if positive_count:
            self._quantities[AkStructureSignType.Positive.name] = positive_count

        if negative_count:
            self._quantities[AkStructureSignType.Negative.name] = negative_count

        if zero_count:
            self._quantities[AkStructureSignType.Zero.name] = zero_count

        return self._quantities

    def __str__(self):
        return "Q(" + self.get_name() + "): " + str(self._quantities)


def get_structures_list(x_data, components_x_data, parent):
    """
    Метод визначає і повертає списки типів структур OHLC, OLHC, UN.

    :param x_data:
    :param components_x_data:
    :param parent:
    :return: [AkStructure(OHLC), AkStructure(OLHC), AkStructure(UN)]
    """

    # лічильники структур
    ohlc_x_data = []
    olhc_x_data = []
    un_x_data = []

    # список усіх типів структур (OHLC, OLHC, UN)
    structures_list = []

    for i in range(len(x_data)):

        # ідентифікуємо тип структури
        structure_type = identify_structure_type(components_x_data[i])

        # добавляємо подію у список структур
        event = x_data[i]
        if structure_type == AkStructureType.OLHC:
            olhc_x_data.append(event)
        elif structure_type == AkStructureType.OHLC:
            ohlc_x_data.append(event)
        else:
            un_x_data.append(event)

    # формуємо список непорожніх типів структур
    if ohlc_x_data:
        structures_list.append(AkStructureEvents(ohlc_x_data, AkStructureType.OHLC, parent))
    if olhc_x_data:
        structures_list.append(AkStructureEvents(olhc_x_data, AkStructureType.OLHC, parent))
    if un_x_data:
        structures_list.append(AkStructureEvents(un_x_data, AkStructureType.UN, parent))

    return structures_list


def identify_structure_type(components_data):
    """
    Метод визначає тип структури по вихідним данним.

    :param components_data: Компоненти вихідних даних базового періоду
    :return: AkStructureType()
    """

    # по замовчуванню, всі структури Undefined
    structure_type = AkStructureType.UN

    # шукаємо індекси максимального і мінімального компонентів даних
    max_value, max_index = AkFunctions.max(components_data)
    min_value, min_index = AkFunctions.min(components_data)

    # спочатку був high, потім low
    if min_index > max_index:
        # < 0
        structure_type = AkStructureType.OHLC
    elif max_index > min_index:
        # > 0
        structure_type = AkStructureType.OLHC

    return structure_type
