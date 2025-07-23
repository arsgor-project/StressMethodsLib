'''
главное тело методики
считаем, что данные введены корректно
'''
import pandas as pd
import os.path as p

from ...utils.Logger import Logger


def run(data_path: str, formulas_path: str) -> None:
	print(data_path)

	# Создаем объект логгера
	logger = Logger('Расчет КЗ областей по Мизесу', data_path)

	# чтение файлов
	input_path: str = p.join(data_path, "InputData.csv")
	inputData = pd.read_csv(input_path, delimiter = ';', decimal = ",")
	logger.add_log(f'Прочитан файл исходных данных по пути - {input_path}', 'INFO')

	load_case_path: str = p.join(data_path, "loadCases.csv")
	loadCases = pd.read_csv(p.join(data_path, "loadCases.csv"), delimiter = ';', decimal = ",")
	logger.add_log(f'Прочитан файл случаев нагружения по пути - {load_case_path}', 'INFO')


	num_zones = inputData.shape[0]
	num_loadcases = loadCases.shape[0]
	print(inputData.info())

	zones = []
	for i in range(num_zones):
		zone_file = inputData.at[i, 'fe_data']
		zone_file_path = p.join(data_path, zone_file)
		zone_df = pd.read_csv(zone_file_path, delimiter = ';', decimal = ",", skipfooter = 1,
							  engine = 'python')
		zones.append(zone_df)
		logger.add_log(f'Прочитаны зоны из файла - {zone_file_path}', 'INFO')

	print(zones[0].info())

	# расчет для каждой зоны
	detail_list = []
	zone_list = []
	FE_list = []
	CritLC_ID_list = []
	CritLC_Name_list = []
	qVonMisesMax = []
	th_list = []
	sVM_list = []
	sVr_list = []
	safetyFactor_list = []

	for i in range(num_zones):
		fe_results = zones[i]
		zone_name = inputData.at[i, 'fe_zone']
		detail_name = inputData.at[i, 'detail_name']
		th = inputData.at[i, 'thickness']
		sigma_vr = inputData.at[i, 'sigma_v']

		sorted = fe_results.sort_values('qvonmisesMax', ascending = False)
		qVonMises = sorted.at[0, 'qvonmisesMax']
		critElemID = sorted.at[0, 'CriticalElemID']
		critLC_ID = sorted.at[0, 'LC_ID']
		critLC_Name = sorted.at[0, 'LC_Name']

		sigmaVonMises = qVonMises / th
		logger.add_log(f'Выполнен расчет напряжений по мизесу по критическим силам детали \'{detail_name}\' в зоне \'{zone_name}\'','INFO')
		safetyFactor = sigma_vr / sigmaVonMises
		logger.add_log(f'Выполнен расчет КЗ детали \'{detail_name}\'','INFO')
		# print(th, sigma_vr,  qVonMises, sigmaVonMises, critElemID, critLC_ID, critLC_Name, safetyFactor)

		detail_list.append(detail_name)
		zone_list.append(zone_name)
		FE_list.append(critElemID)
		CritLC_Name_list.append(critLC_Name)
		qVonMisesMax.append(qVonMises)
		th_list.append(th)
		sVM_list.append(sigmaVonMises)
		sVr_list.append(sigma_vr)
		safetyFactor_list.append(safetyFactor)

	output_data = {'Деталь': detail_list,
				   'Зона': zone_list,
				   'Номер КЭ': FE_list,
				   'Определяющий РС': CritLC_Name_list,
				   't, [мм]': th_list,
				   "q_vonMises": qVonMisesMax,
				   'sigma_vonMises': sVM_list,
				   'sigma_вр': sVr_list,
				   'Коэффициент запаса': safetyFactor_list}
	output_df = pd.DataFrame(output_data)

	print(output_df)
	output_path: str = p.join(data_path, "safetyFactors.csv")
	output_df.to_csv(output_path, sep = ';', decimal = ",", )
	logger.add_log(f'Записан файл с результатми по пути - {output_path}','INFO')
	logger.print_log()
	logger.save_log()
	# return output_df
