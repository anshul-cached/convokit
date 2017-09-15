import tflearn
import tensorflow as tf
import datetime
import os
import sys
import tensorflow as tf
from tensorflow.python.framework import dtypes
from tensorflow.python.ops import standard_ops



def generate_model(len_train_X,len_train_Y):
	tf.reset_default_graph()

	net = tflearn.input_data(shape=[None, len_train_X])
	net = tflearn.fully_connected(net, 8)
	net = tflearn.fully_connected(net, 8)
	net = tflearn.fully_connected(net, len_train_Y, activation='softmax')
	net = tflearn.regression(net)

	model = tflearn.DNN(net, tensorboard_dir='tflearn_logs')
	return model



def load_model(shape,model_path):
	
	model=generate_model(shape[0],shape[1])

	model.load(model_path)

	return model