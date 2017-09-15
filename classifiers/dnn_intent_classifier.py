import tflearn
import tensorflow as tf
import datetime
import os
import sys
from classifiers import model_skel 

def start_learning(train_X,train_Y,save_location,model_trained_on_time):
	
	model=model_skel.generate_model(len(train_X[0]),len(train_Y[0]))

	model.fit(train_X, train_Y, n_epoch=1000, batch_size=8, show_metric=True)
	
	# model_trained_on_time=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
	
	if not os.path.exists(save_location):
		os.mkdir(save_location)
	
	os.mkdir(save_location+"/model-"+model_trained_on_time)
	
	model_path=save_location+"/model-"+model_trained_on_time+"/model.tflearn"

	model.save(model_path)

	return len(train_X[0]),len(train_Y[0])