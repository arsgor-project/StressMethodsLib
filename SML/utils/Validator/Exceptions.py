class ColumnMismatchException(Exception):
    '''
    Тип исключения, когда названия столбцов не соответствуют описанию в json
    '''
    valid_column_list: list[str]
    real_colum_list: list[str]

    def __init__(self, _valid_column_list: list[str], _real_colum_list: list[str]):
        self.valid_column_list = _valid_column_list
        self.real_colum_list = _real_colum_list

    def find_differences(self, list1: list[str], list2: list[str]) -> str:
        if len(list1) != len(list2):
            return 'Ошибка: списки разной длины!'
        differences = []
        for index, (elem1, elem2) in enumerate(zip(list1, list2)):
            if elem1 != elem2:
                differences.append({'Номер позиции':index, 'Название в json': elem1, 'Название в исходных данных': elem2})
        return f"Ошибка! Несоответствие названий столбцов исходных данных.\nРазличия:\n{differences}"

    def __str__(self) -> str:
        return self.find_differences(self.valid_column_list, self.real_colum_list)

class TypeException(Exception):

    def __init__(self):
        pass

    def __str__(self) -> str:
        return ""