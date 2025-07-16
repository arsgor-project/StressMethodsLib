'''
главное тело методики
считаем, что данные введены корректно
'''
import pandas as pd
import os.path as p

def run(data_path):
    print(data_path)

    # чтение файлов
    inputData = pd.read_csv(p.join(data_path, "InputData.csv"), delimiter=';', decimal=",")
    loadCases = pd.read_csv(p.join(data_path, "loadCases.csv"), delimiter=';', decimal=",")

    num_zones = inputData.shape[0]
    num_loadcases = loadCases.shape[0]
    print(inputData.info())

    zones = []
    for i in range(num_zones):    
        zone_file = inputData.at[i , 'fe_data']
        zone_df = pd.read_csv(p.join(data_path, zone_file), delimiter=';', decimal=",", skipfooter=1, engine='python')
        zones.append(zone_df)

    print(zones[0].info())

    # расчет для каждой зоны
    detail_list = []
    zone_list =   []
    FE_list = []
    CritLC_ID_list = []
    CritLC_Name_list = []
    th_list = []
    sVM_list = []
    sVr_list = []
    safetyFactor_list = []

    for i in range(num_zones):
        
        fe_results = zones[i]
        zone_name = inputData.at[i ,   'fe_zone']
        detail_name = inputData.at[i , 'detail_name']
        th =  inputData.at[i , 'thickness']   
        sigma_vr = inputData.at[i , 'sigma_v']

        sorted = fe_results.sort_values('qvonmisesMax', ascending=False)
        qVonMises =  sorted.at[0, 'qvonmisesMax']
        critElemID = sorted.at[0 , 'CriticalElemID']
        critLC_ID =  sorted.at[0 , 'LC_ID']
        critLC_Name =  sorted.at[0 , 'LC_Name']
        
        sigmaVonMises = qVonMises/th
        safetyFactor =  sigma_vr/sigmaVonMises
        #print(th, sigma_vr,  qVonMises, sigmaVonMises, critElemID, critLC_ID, critLC_Name, safetyFactor)
        
        detail_list.append(detail_name)
        zone_list.append(zone_name)
        FE_list.append(critElemID)
        CritLC_Name_list.append(critLC_Name)
        th_list.append(th)
        sVM_list.append(sigmaVonMises)
        sVr_list.append(sigma_vr)
        safetyFactor_list.append(safetyFactor)

    output_data = {'Деталь': detail_list,
                   'Зона': zone_list,
                   'Номер КЭ': FE_list,
                   'Определяющий РС': CritLC_Name_list,
                   't, [мм]': th_list,
                   'sigma_vonMises': sVM_list,
                   'sigma_вр': sVr_list,
                   'Коэффициент запаса': safetyFactor_list}
    output_df = pd.DataFrame(output_data)

    print(output_df)
    output_df.to_csv(p.join(data_path, "safetyFactors.csv"), sep=';', decimal=",",)





    





