from nltk.stem.lancaster import LancasterStemmer
from elasticsearch import Elasticsearch
import nltk
stemmer = LancasterStemmer()

import pandas as pd


def parse_json(row):
    
    rows=[]
    
    for value in row:
        text=value["text"]

        for nest_value in value["entity"] :
            if nest_value["value"] in text and nest_value["value"] is not "":
                text=text.replace(nest_value["value"],nest_value["entity_name"].replace("@",""))
        rows.append(text)
        
    return rows
    

def extract_tokens_elasticsearch(intents,es_host,es_port,model_trained_on_time):
	es=Elasticsearch(hosts=[{'host': es_host, 'port': int(es_port)}])
	words_dictionary=[]
	sentences=[]
	intent_labels=[]
	# 20170908-115012
				# results=es.search(index="20170911-053956-printer", body={"query": {"match": {"synonyms": { "query":"My Printer is behaving weird, everytime time I give a printing task, it just throws up an empty paper.You need to repair it immediately".lower(),"operator":"OR"}}},"highlight": {"pre_tags" : [""],"post_tags" : [""],"fields" : {"synonyms" : {}}}})

	for intent in intents["intents"]:
		for pattern in intent["samples"]:
			
			results=es.search(index=model_trained_on_time+'*', body={"query": {"match": {"synonyms": { "query":pattern["text"].lower(),"operator":"OR"}}},"highlight": {"pre_tags" : [""],"post_tags" : [""],"fields" : {"synonyms" : {}}}})
			# print (results)
			results=results["hits"]["hits"]
			entity_names=[]
			
			for result in results:
				entity_names.append((result["_source"]["entity_name"]).lower())
			w=nltk.word_tokenize(pattern["text"])
			words_dictionary.extend(w)
			sentences.append((w,intent["intent_name"],entity_names))
		if intent["intent_name"] not in intent_labels:
			intent_labels.append(intent["intent_name"])


	ignore_words=['?']
	words_dictionary = [stemmer.stem(w.lower()) for w in words_dictionary if w not in ignore_words]
	words_dictionary = sorted(list(set(words_dictionary)))

	
	intent_labels = sorted(list(set(intent_labels)))	
	print (len(sentences), "documents found")
	print (len(intent_labels), "labels found ", intent_labels)
	# print(sentences)
	return words_dictionary,sentences,intent_labels



def extract_tokens(intents):
	words_dictionary=[]
	sentences=[]
	intent_labels=[]



	entity_matching_dict=pd.DataFrame.from_records(intents["intents"])
	entity_matching_dict["samples"]=entity_matching_dict["samples"].apply(parse_json)
	entity_matching_dict=entity_matching_dict.to_dict (orient='split')["data"]


	for i in range(0,len(entity_matching_dict)):
		intent_index=entity_matching_dict[i][0]
		for pattern in entity_matching_dict[i][1]:
			
			w=nltk.word_tokenize(pattern)
			words_dictionary.extend(w)
			sentences.append((w,intent_index))
			if intent_index not in intent_labels:
				intent_labels.append(intent_index)


	ignore_words=['?']
	words_dictionary = [stemmer.stem(w.lower()) for w in words_dictionary if w not in ignore_words]
	words_dictionary = sorted(list(set(words_dictionary)))

	print (intent_labels)
	intent_labels = sorted(list(set(intent_labels)))	
	print (len(sentences), "documents found")
	print (len(intent_labels), "labels found ", intent_labels)
	print(sentences)
	return words_dictionary,sentences,intent_labels
