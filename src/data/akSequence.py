from src.data import akAmplitude as Amplitude
from src.data.akAmplitude import AkSelectionMethod


def get_sequence(x_data, method=AkSelectionMethod.CC, base_data=False):
    """
    Метод трансформує, зжимає дані DOHLC у послідовність.

    :param base_data: чи рахуємо послідовність для базових даних.
    :param x_data: дані DOHLC, для яких повертаємо зжату послідовність
    :param method: метод селекції даних.

    :return: [int,...]
    """

    # селекція по методу Close-Close: Close[i] - Close[i-1]
    # селекція по методу Open-Close: Close[i] - Open[i]

    if method not in [AkSelectionMethod.CC, AkSelectionMethod.OC]:
        raise Exception("Error: Invalid selection method!")

    # рахуємо амплітуду по заданому методу селекції: AkAmplitude()
    selection = Amplitude.get_amplitude(x_data, method, base_data=base_data)

    # повертаємо точки (% нам не потрібні)
    x = selection.points()

    # на початку порівнюємо нульовий і перший елементи
    index = 1
    x0 = x[0]

    # якщо нульовий елемент None, то порівнюємо спочатку перший і другий елементи
    # зміщуємо індекси вправо на 1
    if x0 is None:
        index += 1
        x0 = x[index - 1]

    # задаємо початкове значення лічильника елемента
    count = 0
    if x0 > 0:
        count = 1
    elif x0 < 0:
        count = -1

    sequence = []
    for i in range(index, len(x)):
        # ++, поточний і попередній +, тому збільшуємо лічильник '+'
        if (x[i] > 0) and (x[i-1] >= 0):
            count += 1

        # --, поточний і попередній -, тому збільшуємо лічильник '-'
        elif (x[i] < 0) and (x[i-1] <= 0):
            count -= 1

        # -+, поточний і попередній відрізняються, тому зберігаємо попередній
        elif (x[i] > 0) and (x[i-1] < 0):
            sequence.append(count)
            count = 1

        # +-, поточний і попередній відрізняються, тому зберігаємо попередній
        elif (x[i] < 0) and (x[i-1] > 0):
            sequence.append(count)
            count = -1

        # - або + і 0
        elif (x[i] == 0) and (x[i-1] != 0):
            sequence.append(count)
            sequence.append(0)
            count = 0

        # 00 - дуже рідкий випадок, але можливий
        elif (x[i] == 0) and (x[i-1] == 0):
            sequence.append(0)

    # додаємо останній елемент в послідовність
    sequence.append(count)

    return sequence
