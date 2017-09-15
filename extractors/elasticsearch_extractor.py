from elasticsearch import Elasticsearch 
import pandas as pd

import sys


def elasticsearch_indexer(intents,entities,conf_props,model_trained_on_time,es_host,es_port):

	es=Elasticsearch(hosts=[{'host': es_host, 'port': int(es_port)}])

	intents=intents["intents"]
	entities=entities["entities"]
	
	updated_entities=[]
	entity_data={}
	for entity in entities:
		temp_synonym=entity["synonyms"]
		
		temp_synonym.append(entity["value"])

		entity_name=entity["entity_name"]
		if entity_name in entity_data:
			entity_data[entity_name]=temp_synonym+entity_data[entity_name]
		else:
			print("Creating index for "+ entity_name)
			es.indices.create(index=model_trained_on_time+"-"+entity_name.lower(), ignore=400)
			
			entity_data[entity_name]=temp_synonym


	# entity_matching_dict=pd.DataFrame.from_records(intents)
	
	# entity_matching_dict=entity_matching_dict.from_records(list(entity_matching_dict["samples"]))
	# entity_matching_dict=pd.DataFrame(entity_matching_dict[0].append(entity_matching_dict[1])).to_dict(orient='list')[0]

	samples=[entity for i in intents if "samples" in i for entity in i["samples"] ]
	
	entity_matching_dict=[entity for i in samples for entity in i["entity"]]	

	for ent in entity_matching_dict:
		entity_name=ent['entity_name'].replace("@","")
		entity_value=ent["value"]
	if entity_name not in entity_data and entity_name is not "":
		sys.exit("Entity "+entity_name+" not found in given entities")
	elif entity_name in entity_data and entity_value not in entity_data[entity_name]:
		entity_data[entity_name].append(entity_value)
		print("Adding not listed synonym")


	# for i in entity_matching_dict:
	# 	entity_list=i["entity"]
	# 	for ent in entity_list:
	# 		entity_name=ent['entity_name'].replace("@","")
	# 		entity_value=ent["value"]
	# 		if entity_name not in entity_data and entity_name is not "":
	# 			sys.exit("Entity "+entity_name+" not found in given entities")

	# 		elif entity_name in entity_data and entity_value not in entity_data[entity_name]:
	# 			entity_data[entity_name].append(entity_value)
	# 			print("Adding not listed synonym")
		
	
	entity_list_name=[]
	for k,v in entity_data.items():
		
		es.index(index=model_trained_on_time+"-"+k.lower(),body={"entity_name":k.lower(),"synonyms":entity_data[k]},doc_type="entity_extractors",id=1)
		entity_list_name.append(k.lower())

	return entity_list_name
		

def query_elasticsearch(query,index_name,es_host,es_port):

	es=Elasticsearch(hosts=[{'host': es_host, 'port': int(es_port)}])
	
	
	results=es.search(index=index_name+'*', body={"query": {"match": {"synonyms": { "query":query,"operator":"OR"}}},"highlight": {"pre_tags" : [""],"post_tags" : [""],"fields" : {"synonyms" : {}}}})

	
	results=results["hits"]["hits"]
	return_results=[]
	entity_list=[]
	
	for result in results:

		entity_index_name=result["_index"]
		entity_name=result["_source"]["entity_name"]
		matched_words=result["highlight"]["synonyms"]
		
		entity_list.append(entity_name.lower())
		return_results.append({"entity_name":entity_name,"matched_words":matched_words})
	
	return query,return_results,entity_list