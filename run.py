# Если используется Embedded Python(ничего не ломает)
import sys, os
from typing import Callable

import pandas as pd

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(0, '.')

import argparse
import os
import json
import importlib


def import_by_path(path: str):
    """
    Импортирует функцию/объект по полному пути:
    "my_library.math_utils.add" → импортирует add из my_library.math_utils
    """
    module_path, attr_name = path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    print(f"Вызов модуля {module}, функция {attr_name}")
    return getattr(module, attr_name)


def get_callable(path: str) -> Callable:
    module_path, attr_name = path.rsplit(".", 1)
    module = importlib.import_module(module_path)
    print(f"Вызов модуля {module}, функция {attr_name}")
    return getattr(module, attr_name)


def get_body(json_path: str) -> Callable:
    with open(json_path, 'r', encoding="utf-8") as f:
        data = json.load(f)
    body_name = data['MethodBody']
    return get_callable(body_name)


def get_validator(json_path: str) -> Callable:
    with open(json_path, 'r', encoding="utf-8") as f:
        data = json.load(f)
    body_name = data['MethodValidator']
    return get_callable(body_name)


def get_method_name(json_path: str) -> str:
    with open(json_path, 'r', encoding="utf-8") as f:
        data = json.load(f)
    method_name = data['MethodName']
    return method_name


def run_method_from_json(json_path: str, data_path: str):
    with open(json_path, 'r', encoding="utf-8") as f:
        data = json.load(f)

    method_path = data["MethodBody"]
    formulas_path = data["MethodFormulasPath"]

    func = import_by_path(method_path)
    if not callable(func):
        raise TypeError(f"{method_path} не является функцией")

    return func(data_path, formulas_path)


def dir_path(path):
    if os.path.isdir(path):
        return path
    else:
        raise argparse.ArgumentTypeError(f"readable_dir:{path} is not a valid path")


# SML/methods/Mises_v1/Mises_v1.json
# tests/resources/Mises_v1_test
# C:/Users/gorynin.ag/Desktop/freecad/python/StressMethodsLib/.venv/Scripts/python.exe run.py tests/resources/Mises_v1_test/Mises_v1.json tests/resources/Mises_v1_test

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Обработка всех файлов в папке")
    parser.add_argument('json_file')
    parser.add_argument('folder', type=dir_path)
    parser.add_argument('is_need_validate', type=bool)
    args = parser.parse_args()

    data_path = args.folder
    method_info_json = args.json_file
    validate = args.is_need_validate
    print(f'Передан путь {method_info_json}')
    print(f'Передан путь {data_path}')
    from SML.utils.Logger import Logger

    name: str = get_method_name(method_info_json)
    logger: Logger = Logger(name, data_path)
    data: pd.DataFrame = None
    run_func: Callable = get_body(method_info_json)
    if validate:
        print('Валидация активна')
        validator: Callable = get_validator(method_info_json)
        result, data_list = validator(method_info_json, data_path).validate(logger)
        run_func(logger, data_path=data_path, data_list=data_list)
    else:
        print('Валидация неактивна')
        run_func(logger, data_path=data_path)
    print(f"Расчет завершен")
