import json
import os.path as p
from abc import abstractmethod

import pandas as pd
from .Logger import Logger

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
				data = pd.read_csv(file_path, delimiter = ';', decimal = ",")
				data_columns_name: list[str] = data.keys().tolist()
				valid_names: list[str] = []
				for name in l['Structure']['Columns']:
					valid_names.append(name['Name'])
				is_valid.append(data_columns_name == valid_names)
				data_list.append(data)
		result = all(is_valid)
		if result:
			logger.add_log('Базовые данные прочитаны успешно и имеют необходимую структуру','INFO')
		else:
			logger.add_log('Данные не имеют необходимую структуру','ERROR')
			raise Exception('Data is not valid')
		return all(is_valid), data_list
