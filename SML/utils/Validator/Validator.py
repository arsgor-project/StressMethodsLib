import json
import os.path as p
import sys
from abc import abstractmethod
from typing import Dict

import pandas as pd
from StressMethodsLib.SML.utils.Logger import Logger
from StressMethodsLib.SML.utils.Validator.Exceptions import ColumnMismatchException

class Validator:
	json_path: str
	data_path: str

	def __init__(self, _json_path: str, _data_path: str):
		self.json_path = _json_path
		self.data_path = _data_path

	@abstractmethod
	def validate(self, logger: Logger) -> tuple[bool, list[pd.DataFrame]]:
		is_valid: list[bool] = []
		data_list: list[pd.DataFrame] = []
		data: pd.DataFrame
		with open(self.json_path, 'r', encoding = "utf-8") as f:
			data = json.load(f)
			source_data = data['SourceData']
			for l in source_data['InputData']:
				file_path: str = p.abspath(p.join(self.data_path, p.normpath(l['FileName'])))
				data = pd.read_csv(file_path, delimiter=';', decimal=",")
				data_columns_name: list[str] = data.keys().tolist()
				data_types: list[str] = data.dtypes.tolist()
				valid_names: list[str] = []
				valid_types: Dict = {}
				for value in l['Structure']['Columns']:
					valid_names.append(value['Name'])
					valid_types[value['Name']] = value['Type']
				data.astype(valid_types)
				if data_columns_name == valid_names:
					is_valid.append(data_columns_name == valid_names)
				else:
					try:
						raise ColumnMismatchException(valid_names, data_columns_name)
					except ColumnMismatchException as e:
						print(e.__str__())
						logger.add_log(e.__str__(), 'ERROR')
						sys.exit(1)
				data_list.append(data)
		result = all(is_valid)
		if result:
			logger.add_log('Базовые данные прочитаны успешно и имеют необходимую структуру','INFO')
		else:
			logger.add_log('Данные не имеют необходимую структуру','ERROR')
			raise Exception('Data is not valid')
		return all(is_valid), data_list


	def validate_names(self, logger: Logger) -> tuple[bool, list[pd.DataFrame]]:
		pass

	def validate_types(self, logger: Logger):
		pass
