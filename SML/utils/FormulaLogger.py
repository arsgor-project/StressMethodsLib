from typing import Any, Literal, Dict
import mdtex2html
import os.path as p
import pandas as pd
import re


def formula_logger(func):
	def wrapper(*args, **kwargs):
		data_path: str = p.abspath(args[0])
		if p.exists(data_path) == False:
			raise Exception('Директории для расчета не существует!')
		formulas_path: str = p.abspath(args[1])
		if p.exists(formulas_path) == False:
			raise Exception('Файла с описанием формул не существует!')
		result: pd.DataFrame = func(*args, **kwargs)
		parameters, formulas = formula_file_parse(formulas_path)
		log_file_path = make_log_file(data_path, result, parameters, formulas)
		print(f"Лог файл записан по пути {log_file_path}")
		# res = mdtex2html.convert(r'$$ \sigma = \sqrt{ \frac{1}{N} \sum_{i=1}^{N} (x_i - \mu)^2 } $$')
		# with open(p.join(data_path, 'test.html'), 'w') as f:
		# 	f.write(res)
	return wrapper

def formula_file_parse(formulas_path: str) -> tuple[Dict, list[str]]:
	parameters: Dict = {}
	formulas: list[str] = []
	flag: Literal['p','f']
	with open(formulas_path, 'r', encoding = 'utf-8') as f:
		for line in f:
			if "[Parameters]" in line:
				flag = 'p'
				continue
			elif "[Formulas]" in line:
				flag = 'f'
				continue
			match flag:
				case 'p':
					par = line.strip().split(' : ')
					parameters[par[0]] = par[1].split('-')
				case 'f':
					formulas.append(line)
	return parameters, formulas

def make_log_file(data_path: str, data: pd.DataFrame, parameters: Dict, formulas: list[str]) -> str:
	log_file_path: str = p.join(data_path, 'calculation_log.html')
	res_str: str = '**Легенда**\n\n'
	# Пишем легенду
	for f in formulas:
		res_str += f'{formula_parse(f, parameters, data, legend = True)}\n'
	res_str += '**Расчет**\n\n'
	# Формируем результаты расчетов
	for i in range(data.shape[0]):
		for f in formulas:
			res_str += f'{formula_parse(f, parameters, data, i)}\n'
	result: str = mdtex2html.convert(res_str)
	with open(log_file_path, 'w') as f:
		f.write(result)
	return log_file_path


def get_key_by_value(dictionary: Dict, target_value: Any):
	for key, value in dictionary.items():
		if target_value in value:
			return key
	return None


def find_words_starting_with(words_list: list, char: str):
	words = ' '.join(map(str, words_list)).split()  # Разделение строки на слова
	result = []
	for word in words:
		if word.startswith(char):
			result.append(word)
	return result


def formula_parse(formula: str, parameters: Dict, data: pd.DataFrame, num: int = 0, legend: bool = False) -> str:
	f: str = formula
	# Находим все параметры в строке формулы
	pars = [re.sub(r'[^a-zA-Z0-9\s\/]', ' ', p) for p in formula.split() if '/p' in p]
	pars = find_words_starting_with(pars, '/p')
	# pars = [find_words_starting_with(p, '/p') for p in pars]
	# Ищем эти параметры в параметрах
	for par in pars:
		par_cut = par.split('/p')[1]
		par_vals = [row[0] for row in list(parameters.values())]
		if par_cut in par_vals:
			key: str = get_key_by_value(parameters, par_cut)
			if legend:
				value: str = parameters[key][1].replace(' ','\\;')
			else:
				value: str = str(round(data.at[num, key], 4)) if type(data.at[num, key]) is not str else str(data.at[num, key]).replace(' ','\\;')
			f = f.replace(par, value)
	return f


