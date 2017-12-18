from sklearn import preprocessing, model_selection

from sklearn.linear_model import LinearRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.svm import SVC
from sklearn.naive_bayes import BernoulliNB
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors.nearest_centroid import NearestCentroid
from sklearn import model_selection

from sklearn.metrics import accuracy_score
from sklearn.utils import shuffle
from sklearn import tree

import numpy as np
import pandas as pd

def get_hospital_address(place):
	print (place)
	res = {}
	vet_hospital = pd.read_csv("data/vet_hospital.csv")
	res['hospital_name'] = vet_hospital[vet_hospital['place'] == place]['hospital_name'].item()
	res['phone_no'] = vet_hospital[vet_hospital['place'] == place]['phone_no'].item()
	res['address'] = vet_hospital[vet_hospital['place'] == place]['address'].item()
	res['state'] = vet_hospital[vet_hospital['place'] == place]['state'].item()
	res['longitude'] = vet_hospital[vet_hospital['place'] == place]['longitude'].item()
	res['latitude'] = vet_hospital[vet_hospital['place'] == place]['latitude'].item()
	return res

def pred2(olist):
	res =[]
	other_symptoms = pd.read_csv("data/other_symptoms.csv")
	if len(olist) == 0:
		res.append(0)
	else:
		for i in olist:
			disease = other_symptoms[other_symptoms['other_symptoms'] == i]['disease'].item()
			if disease not in res:
				res.append(disease)
	return res

def getListFromString(slist):
	if slist:
		alist = slist.split("'")
		alist.remove('[')
		alist.remove(']')
		return list(filter(lambda a: a != ', ', alist))
	else:
		return []

def get_other_symptoms():
	other_symptoms = pd.read_csv("data/other_symptoms.csv")
	return other_symptoms["other_symptoms"]


def get_disease_info(ind):
	res = {}
	diseases = pd.read_csv("data/diseases.csv")
	farmer_steps = pd.read_csv("data/farmer_steps.csv")
	contacts = pd.read_csv("data/contacts.csv")
	samples = pd.read_csv("data/samples.csv")
	tests = pd.read_csv("data/tests.csv")
	how_to_diagnose = pd.read_csv("data/how_to_diagnose.csv")
	res["name"] = diseases[diseases['pk'] == ind]['name'].item()
	res["description"] = diseases[diseases['pk'] == ind]['description'].item()
	res["steps"] = farmer_steps[farmer_steps['fk'] == ind]['steps'].values
	res["contacts"] = contacts[contacts['fk'] == ind]['contact'].values
	res["samples"] = samples[samples['fk'] == ind]['sample'].values
	res["tests"] = tests[tests['fk'] == ind]['test'].values
	res["how_to_diagnose"] = how_to_diagnose[how_to_diagnose['fk'] == ind]['how_to_diagnose'].values
	return res
def get_names(ind):
	resb = []
	diseases = pd.read_csv("data/diseases.csv")
	for i in ind:
		resb.append(diseases[diseases['pk'] == i]['name'].item())
	return resb

def ml_algo(inp):
	df = pd.read_csv("data/final_preprocess.csv")
	X = np.array(df.drop(['Result'], axis=1))
	y = np.array(df['Result'])
	X, y = shuffle(X,y, random_state=1)
	X_train, X_test, y_train, y_test = model_selection.train_test_split(X,y,test_size=0.2)

	model_centroid = NearestCentroid().fit(X_train, y_train)
	model_knn = KNeighborsClassifier(25).fit(X_train, y_train)
	model_svm = SVC().fit(X_train, y_train)
	model_lr =LinearRegression().fit(X_train, y_train)
	model_nb = BernoulliNB().fit(X_train, y_train)
	# criterion-> gini or entropy; splitter-> best or random; max_depth-> any integer value or None;
	# min_samples_split-> min no. of samples reqd. to split an internal node;
	# min_samples_leaf -> The minimum number of samples required to be at a leaf node. 
	# min_impurity_split -> It defines the threshold for early stopping tree growth.
	model_dtree = DecisionTreeClassifier(criterion = "entropy", random_state = 100, max_depth=3, min_samples_leaf=5).fit(X_train, y_train)

	# print ("[1] ACCURACY OF DIFFERENT MODELS ",'\n___________________')
	accu_centroid = model_centroid.score(X_test, y_test)
	# print ("NearestCentroid -> ", accu_centroid)
	accu_knn = model_knn.score(X_test, y_test)
	# print ("Knn             -> ",accu_knn)
	accu_svm = model_svm.score(X_test, y_test)
	# print ("SVM             -> ", accu_svm,)
	accu_lr = model_lr.score(X_test, y_test)
	# print ("Linear Regr     -> ", accu_lr)
	accu_nb = model_nb.score(X_test, y_test)
	# print ("Naive Bayes     -> ", accu_nb)
	accu_dtree = model_dtree.score(X_test, y_test)
	# print ("Decission Tree  -> ", accu_dtree, "\n")

	result_centroid = model_centroid.predict(inp)
	result_knn = model_knn.predict(inp)
	result_svm = model_svm.predict(inp)
	result_lr = model_lr.predict(inp)
	result_nb = model_nb.predict(inp)
	result_dtree = model_dtree.predict(inp)

	# disease-name, description, [list of step to be taken], [list of to whom we can contact]
	


	# print ("[2] PREDICTION ",'\n___________________')
	# print ("NearestCentroid -> ", result_centroid)
	# print ("knn             -> ", result_centroid)
	# print ("svm             -> ", result_svm)
	# print ("LinearReg       -> ", result_lr)
	# print ("Naive Bayes     -> ", result_nb)
	# print ("Decission Tree  -> ", result_dtree)
	
	# return map_disease[str(result_knn[0])]
	return result_knn[0]

if __name__ == '__main__':
	ab = [1,1,0,1,1,0,0,1,0,1,0,0]
	# bc = ml_algo(ab)
	# get_disease_info(bc)
	# get_names(ab)
	nn = get_other_symptoms()
	for i in nn:
		print (i)
