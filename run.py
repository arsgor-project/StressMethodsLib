# Если используется Embedded Python(ничего не ломает)
import sys, os
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


def run_method_from_json(json_path: str, data_path: str):
    with open(json_path, 'r', encoding="utf-8") as f:
        data = json.load(f)

    method_path = data["MethodBody"]
    
    func = import_by_path(method_path)
    if not callable(func):
        raise TypeError(f"{method_path} не является функцией")

    return func(data_path)

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
    args = parser.parse_args()
    
    data_path = args.folder
    method_info = args.json_file
    print(f"Передан путь {method_info}")
    print(f"Передан путь {data_path}")

    # прежде чем вызывать методику можно вызвать валидатор
    result  = run_method_from_json(method_info, data_path)
    print(f"Расчет завершен")


