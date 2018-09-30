from prettytable import PrettyTable

from src.akFunctions import AkFunctions


class AkExport(object):

    @classmethod
    def print_series_categories(cls, period, structures=True, structure_amplitudes=True, file=None):

        # якщо у періоді в жодному із варіантів нема серій
        if not period.series_categories():
            return

        # друкуємо заголовок періода
        cls.print_title(period.get_name(), file, underline=False)
        digits = period.instrument.precision

        for variant in period.variants():

            # варіант без серій пропускаємо
            if not variant.series_categories():
                continue

            # заголовок таблички
            variant_title = period.get_name() + "[" + str(variant.number() + 1) + "]"

            # PrettyTable
            p_table = PrettyTable()
            p_table.field_names = ["Value", "Count"]
            p_table.title = variant_title

            for category in variant.series_categories():
                p_table.add_row([category.value(), category.count()])

            p_table.align = 'r'
            cls.print_pretty_table(p_table, file=file)

            for category in variant.series_categories():

                # друкуємо структури категорії варіанта
                if structures:

                    if category.structures():
                        # друкуємо заголовов категорії варіанту
                        cls.print_title("Category: " + str(category.value()) + "(" + str(category.count()) + ")", file,
                                        underline=True, underline_char='=', enter=True)

                        s_table = PrettyTable()
                        s_table.title = "Series"
                        s_table.field_names = ["Start Date", "End Date"]

                        for s in category.series():
                            s_table.add_row([s.start_date(), s.end_date()])

                        s_table.align = 'r'
                        cls.print_pretty_table(s_table, file=file)

                        # друкуємо кількісні величини структур
                        AkExport.print_structures_quantities(category.structures(), text_file=file)

                        # друкуємо структури і їх динаміки
                        for structure in category.structures():
                            AkExport.print_structure(structure, structure_amplitudes, digits, file)

    @classmethod
    def create_pretty_table(cls, x_data, title="", headers=None, digits=4):
        """
        Метод створює відформатовану таблицю на вивід.

        :param x_data: дані DOHLC
        :param title: назва таблиці
        :param headers: заголовки стовпців
        :param digits: точність виводу
        """

        if headers is None:
            headers = ["Date", "Open", "High", "Low", "Close"]

        # форматуємо дані варіанту
        x_data = cls.format_table(x_data, digits=digits)

        # PrettyTable
        p_table = PrettyTable()
        p_table.field_names = headers
        p_table.title = title

        # добавляємо дані у PrettyTable
        for row in x_data:
            p_table.add_row(row)

        return p_table

    @classmethod
    def print_period(cls, period, period_amplitudes=True, structures=False, structure_amplitudes=False, file=None):

        cls.print_title(period.get_name(), file, underline=False, underline_char='=')
        digits = period.instrument.precision

        for variant in period.variants():
            p_table = cls.create_pretty_table(variant.x_data,
                                              title=period.get_name() + "[" + str(variant.number() + 1) + "]",
                                              digits=digits)

            # друкуємо амплітуди варіанта періода
            if period_amplitudes:
                amplitudes = variant.amplitudes()
                for amplitude in amplitudes:
                    # дані амплітуди : points , percent
                    points_column = cls.format_list(amplitude.points(), digits=digits)
                    percent_column = cls.format_list(amplitude.percent(), digits=digits)

                    p_table.add_column(amplitude.name() + ", pp", points_column, align='r')
                    p_table.add_column(amplitude.name() + ", %", percent_column, align='r')

            # вирівнювання даних таблиці по правому краю
            p_table.align = 'r'

            # друк таблиці
            cls.print_pretty_table(p_table, file=file)

            # друкуємо структури варіанта періоду
            if structures:
                if variant.structures():
                    AkExport.print_structures_quantities(variant.structures(), text_file=file)

                    for structure in variant.structures():
                        AkExport.print_structure(structure, structure_amplitudes, digits, file)

    @classmethod
    def format_list(cls, values, ignored=None, include_ignored=True, digits=4):
        """
        Метод повертає відформатований список дійсних значень з точністю 'digits' після коми.

        :param values: [float,...]  - список значень для форматування
        :param ignored: [int, ...]  - список індексів значень, які не форматуємо
        :param include_ignored: bool - Визначає, чи включаємо у результат ігноруючі значення.
        :param digits: int          - Точність форматування (кількість знаків після коми)

        :return: [float, ...]       - Відформатований список дійсних значень.
        """
        if ignored is None:
            ignored = []

        formatted = []
        for i in range(len(values)):
            # значення по індексу не форматуємо
            if (i in ignored) or (values[i] is None):
                # включаємо значення у результат
                if include_ignored:
                    formatted.append(values[i])
                continue

            # форматуємо число і додаємо у результуючий список
            formatted.append(AkFunctions.toFixed(values[i], digits))

        return formatted

    @classmethod
    def format_table(cls, x_data, ignored_colls=None, include_ignored=True, digits=4):
        """
        Метод форматує дані типу DOHLC з точністю 'digits'


        :param x_data: [[], ...] - Дані DOHLC
        :param ignored_colls:
        :param include_ignored:
        :param digits: int      - Точність форматування

        :return: [[], ...]      - Відформатовані дані DOHLC
        """
        if ignored_colls is None:
            ignored_colls = [0]

        new_data = []
        for row in x_data:
            # форматуємо рядок даних, перше значення дати ігноруємо, але включаємо у результат
            new_data.append(cls.format_list(row, ignored=ignored_colls, include_ignored=include_ignored, digits=digits))

        return new_data

    @classmethod
    def print_title(cls, title, file=None, underline=False, underline_char='-', underline_count=0, enter=False):
        print(title, file=file)

        if underline:
            if underline_count == 0:
                underline_count = len(title)
            cls.print_underline(underline_count, underline_char, file)

        if enter:
            print("", file=file)

    @classmethod
    def print_underline(cls, length, char, text_file):
        underline_str = ""
        for i in range(length):
            underline_str += char

        print(underline_str, file=text_file)

    @classmethod
    def print_list_values(cls, values, text_file=None, title='', underline=False, underlined_char='-', enter=False):
        if title != '':
            cls.print_title(title, text_file, underline, underlined_char, enter)

        print(values, file=text_file)

    @classmethod
    def print_pretty_table(cls, p_table, file=None):
        # друк таблиці
        print(p_table, file=file)
        print('', file=file)

    @classmethod
    def print_structure(cls, structure, amplitudes=True, digits=4, text_file=None):

        p_table = cls.create_pretty_table(structure.events_x_data(), title=structure.get_name(), digits=digits)

        # вирівнювання даних таблиці по правому краю
        p_table.align = 'r'

        if amplitudes:
            amplitudes = structure.amplitudes()
            for amplitude in amplitudes:
                # формуємо дані амплітуди : points , percent
                points_column = cls.format_list(amplitude.points(), digits=digits)
                percent_column = cls.format_list(amplitude.percent(), digits=digits)

                p_table.add_column(amplitude.name() + ", pp", points_column, align='r')
                p_table.add_column(amplitude.name() + ", %", percent_column, align='r')

        # друк таблиці
        cls.print_pretty_table(p_table, text_file)

    @classmethod
    def print_structures_quantities(cls, structures, text_file=None):
        if not structures:
            return

        s_table = PrettyTable()

        s_table.title = "Structures"
        s_table.min_table_width = len(s_table.title) + 10

        headers = []
        values = []

        for s in structures:
            if s.events_count() > 0:
                headers.append(s.get_name())
                values.append(s.events_count())

        s_table.field_names = headers
        s_table.add_row(values)

        print(s_table, file=text_file)
        print("", file=text_file)

        for s in structures:
            print(s, file=text_file)
        print("", file=text_file)
