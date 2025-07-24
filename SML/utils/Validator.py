import json
import os.path as p

import pandas as pd


class Validator:
	json_path: str
	data_path: str

	def __init__(self, _json_path: str, _data_path: str):
		self.json_path = _json_path
		self.data_path = _data_path

	def validate(self) -> bool:
		is_valid: list[bool] = []
		with open(self.json_path, 'r', encoding = "utf-8") as f:
			data = json.load(f)
			source_data = data['SourceData']
			for l in source_data['InputData']:
				file_path: str = p.abspath(p.join(self.data_path, p.normpath(l['FileName'])))
				data_columns_name: list[str] = pd.read_csv(file_path, delimiter = ';', decimal = ",").keys().tolist()
				valid_names: list[str] = []
				for name in l['Structure']['Columns']:
					valid_names.append(name['Name'])
				is_valid.append(data_columns_name == valid_names)
		return all(is_valid)
