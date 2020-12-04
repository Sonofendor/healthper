import pandas as pd

DATAPATH = 'C:\\project\\data.csv'
SYMPTOMSPATH = 'C:\\project\\symptoms_unique.csv'
DISEASEPATH = 'C:\\project\\diseases_unique.csv'

def map_labels_to_dataset(data_path, symptoms_path, disease_path):
	'''Заменяет числовые id в data.csv на названия симптомов и болезней'''
	data = pd.read_csv(data_path, index_col=0)
	diseases = pd.read_csv(disease_path, index_col=0)
	symptoms = pd.read_csv(symptoms_path, index_col=0)

	for id in range(1, data.disease_id.max() + 1):
	    data.loc[data.disease_id == id, 'disease_id'] = diseases.loc[float(id), 'unified']
	data.loc[data.disease_id == 0, 'disease_id'] = 'Здоров'
	
	new_columns = []
	for id in range(1,274):
	    symptom = symptoms.loc[float(id), 'unified']
	    if isinstance(symptom, pd.Series):
	        symptom = symptom.max()
	    new_columns.append(symptom)
	
	data.columns = new_columns + ['disease']
	
	return data

def link_symptoms_to_diseases(data_path, symptoms_path, disease_path):
	'''Возвращает словарь, в котором ключ - название болезни, значение - список симптомов'''
	mapped_data = map_labels_to_dataset(DATAPATH,SYMPTOMSPATH,DISEASEPATH)

	dictionary = dict.fromkeys(mapped_data.disease.unique())

	for disease in dictionary.keys():
		if disease == 'Здоров':
			continue
		dictionary[disease] = mapped_data.columns[(mapped_data[mapped_data.disease == disease] != 0).any()][:-1].tolist()

	return dictionary

def input_symptoms(symptoms_path):
	'''ввод симптомов из консоли'''
	symptoms = pd.read_csv(symptoms_path, index_col=0)
	current_symptoms = []
	print('Введите свои симптомы (0 - конец): ')
	while 1 == 1:
		symptom = input()
		if symptom in symptoms.unified.unique():
			current_symptoms.append(symptom)
		elif symptom == '0':
			break
		else:
			print('Симптом не существует!')
	return current_symptoms

def get_symptoms_by_current(current_symptoms, data_path, symptoms_path, disease_path):
	'''возвращает все возможные симптомы по введенным'''
	mapper = link_symptoms_to_diseases(data_path, symptoms_path, disease_path)
	symptoms_all = []
	for symptom in current_symptoms:
		for disease, disease_symptoms in mapper.items():
			if disease_symptoms is None:
				continue
			if symptom in disease_symptoms:
				symptoms_all += disease_symptoms
	symptoms_all = list(set(symptoms_all))
	return symptoms_all

def ask_symptoms(data_path, symptoms_path, disease_path):
	'''спрашивает симптомы из консоли и создает числовой массив'''
	symptoms = pd.read_csv(symptoms_path, index_col=0)

	pdv = dict.fromkeys(symptoms.unified.unique(), 0)
	
	current_symptoms = input_symptoms(symptoms_path)
	symptoms_all = get_symptoms_by_current(current_symptoms, data_path, symptoms_path, disease_path)
	
	symptoms_to_ask = [s for s in symptoms_all if s not in current_symptoms]
	for symptom in symptoms_to_ask:
		not_answered = True
		while not_answered:
			print('У вас есть симптом ' + symptom + '? (1 - да, 0 - нет, 0.5 - не знаю)')
			try:
				answer = float(input())
				if answer not in [0.0, 0.5, 1.0]:
					print('Неправильный ответ!')
				else:
					pdv[symptom] = answer
					not_answered = False
			except ValueError:
				print('Число введи, ебан')
	
	return pdv

#def get_n_max(array, labels, n = 3):
#	'''выбирает n максимальных значений из массива и возвращает соответствующие метки'''
#	values = []
#	chosen_labels = []
#	for i in range(0,len(array)):
#		ind = array[i].argsort()[-n:][::-1]
#		values.append(array[i][ind])
#		chosen_labels.append(labels[ind])
#	return values, chosen_labels





if __name__ == '__main__':
	myarray = ask_symptoms(DATAPATH, SYMPTOMSPATH, DISEASEPATH)
	print(myarray)