"""Модуль подсчитывает все необходимое для того, чтобы спарсить список актуальных групп."""

import pandas as pd
from openpyxl.utils.cell import coordinate_from_string


EXCEL_FILE = "shinobi.xlsx"


def convert_range_string(excel_range: str) -> dict:
    """
    Подсчитывает необходимое количество ячеек для отступов
    со всех сторон таблицы. Требует стартовое и конечное число ячеек.
    """

    upper_left, lower_right = excel_range.split(':')

    left_col, top_row = coordinate_from_string(upper_left)
    right_col, bottom_row = coordinate_from_string(lower_right)

    return {'usecols': f'{left_col}:{right_col}',
            'skiprows': int(top_row) - 1,
            'nrows': int(bottom_row) - int(top_row)}


def get_human_data() -> list:
    """
    Вытягивает человекочитаемую колонку с группами
    колледжа и конвертирует в список.
    """

    ready_groups = []

    excel_range = 'D5:BV5'
    keys = pd.ExcelFile(EXCEL_FILE)
    sheet_name = keys.sheet_names[len(keys.sheet_names)-1] # вытягивает последнюю (актуальную) страницу таблицы

    args = convert_range_string(excel_range)

    df = pd.read_excel(EXCEL_FILE, sheet_name=sheet_name, **args)

    human_data = df.loc[:, ~df.columns.str.contains('^Unnamed')] # обрубает пустые ячейки и переводит в человекоданные

    for i in human_data:
        ready_groups.append(str(i).replace(" ", ""))

    return(ready_groups)
