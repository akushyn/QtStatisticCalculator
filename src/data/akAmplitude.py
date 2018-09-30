from src.data.akEnums import AkSelectionMethod


class AkAmplitude(object):

    def __init__(self, amplitude_type, values):

        # тип амплітуди
        self._amplitude_type = amplitude_type

        # списки значеннь амплітуди [Date, Point, Percent]
        self._values = values

    def amplitude_type(self):
        """
        Метод повертає тип амплітуди.

        :return: AkAmplitudeType()
        """

        return self._amplitude_type

    def name(self):
        """
        Метод повертає ім"я амплітуди в класичному математичному виді.

        :return: str()
        """
        # повертаємо повне ім"я амплітуди
        amplitude_name = str(self.amplitude_type().name)

        # якщо ім"я містить 'abs', то перетворюємо стрічку виду |HL|
        if 'abs' in amplitude_name:
            return "|" + amplitude_name[3:] + "|"

        return amplitude_name

    def values(self):
        """
        Метод повертає значення амлітуди.

        :return: [[date, point, percent], ...]
        """
        return self._values

    @staticmethod
    def headers():
        return ["Date", "Points", "Percent"]

    def length(self):
        """
        Метод повертає довжину даних амплітуди
        :return: int
        """
        return len(self._values)

    def points(self):
        """
        Метод повертає список значень 'points' амплітуди.

        :return: [double, double,...]
        """

        # результуючий вектор
        point_values = []

        # цикл по довжині даних амплітуди, вибираємо 'points' стовпець
        for i in range(self.length()):
            point_values.append(self._values[i][1])

        return point_values

    def percent(self):
        """
        Метод повертає список значень 'percent' амплітуди.

        :return: [double, double,...]
        """

        # результуючий вектор
        percent_values = []

        # цикл по довжині даних амплітуди, вибираємо 'percent' стовпець
        for i in range(self.length()):
            percent_values.append(self._values[i][2])

        return percent_values


def get_amplitude(x_data, amplitude_type, digits=4, base_data=False):
    """
    Метод повертає амплітуду заданого типу із заданою точністю.

    :param x_data - Вихідні дані DOHLC
    :param amplitude_type: AkAmplitudeType() - Тип амплітуди.
    :param digits: int() - Точність обрахунків.
    :param base_data: bool - Рахуємо для базових даних

    :return: AkAmplitude()
    """

    if not x_data:
        return None

    values = []

    # рахуємо амплітуду GAP
    if amplitude_type == AkSelectionMethod.GAP:
        return get_gap_amplitude(x_data, digits)

    # рахуємо амплітуду Close-Close
    elif amplitude_type == AkSelectionMethod.CC:
        return get_close_close_amplitude(x_data, digits, base_data=base_data)

    # рахуємо одну із амплітуд OH, HL, LC, OL, LH, HC
    else:
        s_idx, e_idx, absolute = _amplitude_type_to_columns(amplitude_type)
        for i in range(len(x_data)):
            date = x_data[i][0]
            if absolute:
                point_value = round(abs(float(x_data[i][e_idx]) - float(x_data[i][s_idx])), digits)
                percent_value = round(abs(((float(x_data[i][e_idx]) - float(x_data[i][s_idx])) /
                                           float(x_data[i][e_idx])) * 100), digits)
            else:
                point_value = round(float(x_data[i][e_idx]) - float(x_data[i][s_idx]), digits)
                percent_value = round(((float(x_data[i][e_idx]) - float(x_data[i][s_idx])) /
                                       float(x_data[i][e_idx])) * 100, digits)

            values.append([date, point_value, percent_value])

    return AkAmplitude(amplitude_type, values)


def get_amplitudes(x_data, types, digits=4):
    """
    Метод повертає список амплітуд заданих типів.

    :param x_data: DOHLC
    :param types: list[AkAmplitudeType].
    Типи амплітуд, які потрібно порахувати.

    :param digits: int()
    Точність обрахунків.

    :return: [AkAmplitude(), ...]
    """
    if not x_data:
        return []

    amplitudes = []
    for amplitude_type in types:
        amplitudes.append(get_amplitude(x_data, amplitude_type, digits))

    return amplitudes


def get_gap_amplitude(x_data, digits=4):
    """
    Метод повертає амплітуду геп.

    :param x_data: дані DOHLC
    :param digits: точність обрахунків
    :return: list[{date: [pointValue, percentValue]}]
    """

    values = list()

    # gap[0] by default = None
    values.append([x_data[0][0], None, None])

    # Gap[i] = Open[i] - Close[i-1]
    for i in range(1, len(x_data)):
        date = x_data[i][0]
        point_value = round(float(x_data[i][1]) - float(x_data[i - 1][4]), digits)
        percent_value = round(((float(x_data[i][1]) - float(x_data[i - 1][4])) / float(x_data[i][1])) * 100, digits)

        values.append([date, point_value, percent_value])

    return AkAmplitude(AkSelectionMethod.GAP, values)


def get_close_close_amplitude(x_data, digits=4, base_data=False):
    values = []

    if base_data:
        # першого елементу нема, тому по замовчуванню None
        values.append([x_data[0][0], None, None])
    else:
        # числове значення різниці
        point0 = round(float(x_data[0][4]) - float(x_data[0][1]), digits)

        # значення різниці в %
        percent0 = round(((float(x_data[0][4]) - float(x_data[0][1])) / float(x_data[0][4])) * 100, digits)

        values.append([x_data[0][0], point0, percent0])

    # CC[i] = Close[i] - Close[i-1]
    for i in range(1, len(x_data)):
        # дата
        date = x_data[i][0]

        # числове значення різниці
        point_value = round(float(x_data[i][4]) - float(x_data[i - 1][4]), digits)

        # значення різниці в %
        percent_value = round(((float(x_data[i][4]) - float(x_data[i - 1][4])) / float(x_data[i][4])) * 100, digits)

        # добавляємо нове значення у список
        values.append([date, point_value, percent_value])

    return AkAmplitude(AkSelectionMethod.CC, values)


def _amplitude_type_to_columns(amplitude_type):
    """
    Convert AkAmplitudeType to column numbers.
    :param amplitude_type: AkAmplitudeType
    :return: int(), int(), bool()
    """

    idx_list = [int(x) for x in str(amplitude_type.value)]
    if idx_list[2] == 1:
        absolute = True
    else:
        absolute = False

    return idx_list[0], idx_list[1], absolute
