from check_config import *
from tokenizers import tokenizer
from do_train import get_intents
from classifiers.model_skel import generate_model,load_model
from classifiers.model_predict import predict
from extractors import elasticsearch_extractor
import os
import sys

import pickle
import numpy as np
import nltk
import json
from nltk.stem.lancaster import LancasterStemmer
stemmer = LancasterStemmer()

def parse_sentence(sentence_info,words_dictionary,entity_labels):
    sentence_words=nltk.word_tokenize(sentence_info[0])
    sentence_words=[stemmer.stem(word.lower()) for word in sentence_words]
    bag=[0]*len(words_dictionary)
    for s in sentence_words:
        for i,w in enumerate(words_dictionary):
            if w == s: 
                bag[i] = 1
                print ("found in bag: %s" % w)
    for entity in entity_labels:
    	if entity.lower() in sentence_info[1]:
    		bag.append(1)
    	else:
    		bag.append(0)

    return(np.array(bag))




def get_model(model_dir):
	model=None
	es_index_name=""
	with open(model_dir+"/metadata.json") as metadata:
		metainfo=json.load(metadata)
		model_address=model_dir+"/"+metainfo["model_dir"]+"/model.tflearn"
		shape=metainfo["shape"]
		model=load_model(shape,model_address)
		es_index_name=metainfo["model_created_on"]
	return model,es_index_name




def do_serve(query,words_dictionary,intent_labels,entity_labels,model,es_index_name,conf_props,entity_classifier,threshold):


	if entity_classifier=="elasticsearch":
		es_host,es_port=check_elastic_search_conf(conf_props)
		
		query,return_results,entity_list=elasticsearch_extractor.query_elasticsearch(query,es_index_name,es_host,es_port)
		

		predicted_results=dict(predict(model,parse_sentence((query,entity_list),words_dictionary,entity_labels),threshold,intent_labels))
		
		predicted_results=dict([(str(k), str(v)) for k, v in predicted_results.items()])
		return ({"intent":max(predicted_results),"entity":return_results})
	return {}


	


