from datetime import datetime
from typing import Literal
import os.path as p


class Logger:
	log_list: list[str]
	log_path: str
	name: str

	def __init__(self, _name: str, _log_path: str):
		self.name = _name
		self.log_path = _log_path
		self.log_list = []
		d_t = datetime.now().__str__()
		self.log_list.append(': '.join(['TITLE', ' | '.join([self.name, d_t])]))

	def add_log(self, log_str: str, log_type: Literal['INFO', 'DEBUG']) -> None:
		d_t = datetime.now().__str__()
		self.log_list.append(': '.join([log_type, ' | '.join([log_str, d_t])]))

	def print_log(self) -> None:
		for l in self.log_list:
			print(l)

	def save_log(self) -> None:
		if p.exists(self.log_path) == False:
			raise Exception('Пути для записи лога не существует!')
		with open(p.join(self.log_path, 'log.txt'), 'w') as f:
			for line in self.log_list:
				f.write(f'{line}\n')
