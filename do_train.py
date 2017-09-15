import logging
import pickle
from tokenizers import tokenizer
import os
import sys
import datetime
from elasticsearch import Elasticsearch
from extractors import elasticsearch_extractor
logger = logging.getLogger(__name__)

from check_config import *
import json
import pandas as pd
import numpy as np
from classifiers import dnn_intent_classifier
import pickle
from nltk.stem.lancaster import LancasterStemmer
import nltk
import random
stemmer = LancasterStemmer()
def generate_io(words_dictionary,sentences,intent_labels,entity_labels):
	training=[]
	output=[]
	
	output_empty=[0]*len(intent_labels)

	for sentence in sentences:
		bag=[]
		
		pattern_words=sentence[0]
		pattern_words = [stemmer.stem(word.lower()) for word in pattern_words]
    	

		for w in words_dictionary:
			if w in pattern_words:
				bag.append(1)
			else:
				bag.append(0)
        
		for entity in entity_labels:
			if entity.lower() in sentence[2]:
				# print(entity,sentence[2])
				bag.append(1)
			else:
				# print(entity,0,sentence[2])
				bag.append(0)


		output_row = list(output_empty)
		output_row[intent_labels.index(sentence[1])] = 1
		training.append([bag,output_row])
	
	random.shuffle(training)
	training = np.array(training)

	train_x = list(training[:,0])
	train_y = list(training[:,1])
	return train_x,train_y

def do_train(config_file):
	data_file_path,threshold,model_dir,entity_classifier,conf_props=check_config(config_file)	

	intents=get_intents(data_file_path)
	entities=get_entities(data_file_path)
	model_trained_on_time=datetime.datetime.now().strftime('%Y%m%d-%H%M%S')
	words_dictionary=[]
	sentences=[]
	intent_labels=[]
	entity_labels=[]
	if entity_classifier=="elasticsearch":
		es_host,es_port=check_elastic_search_conf(conf_props)
		entity_labels=elasticsearch_extractor.elasticsearch_indexer(intents,entities,conf_props,model_trained_on_time, es_host, es_port)
		
		words_dictionary,sentences,intent_labels=tokenizer.extract_tokens_elasticsearch(intents,es_host,es_port,model_trained_on_time)
	else:
		sys.exit("Unmatched entity classifier")

	# words_dictionary,sentences,intent_labels=tokenizer.extract_tokens(intents)		




	train_X,train_Y=generate_io(words_dictionary,sentences,intent_labels,entity_labels)
	len_train_x,len_train_y=dnn_intent_classifier.start_learning(train_X,train_Y,model_dir,model_trained_on_time)
	with open(model_dir+"/metadata.json","w") as metadata:
		metainfo=json.dumps({"model_created_on":model_trained_on_time,"model_dir":"model-"+model_trained_on_time,"shape":[len_train_x,len_train_y]})
		metadata.write(metainfo)

	pickle.dump( {'words':words_dictionary, "entity_class":entity_labels,'classes':intent_labels, 'train_X':train_X, 'train_Y':train_Y}, open( model_dir+"/trained_data", "wb" ) )





def get_intents(data_file_path):
	intents=[]
	# data_file_dir=os.path.dirname(data_file_path)
	with open(data_file_path+"/intents.json") as intents_file:
		intents=json.load(intents_file)
	return intents

def  get_entities(data_file_path):
	entities=[]
	with open(data_file_path+"entities.json") as entities_file:
		entities=json.load(entities_file)

	return entities