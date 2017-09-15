import json
import os
import sys
import logging
logger = logging.getLogger(__name__)


def check_config(config_file):
	data_file_path=""
	threshold=.25
	model_dir=""
	entity_classifier=""
	conf_props=None
	with open(config_file) as config: 
		conf_props=json.load(config)
		print(conf_props.keys())
		if "data" and "entity_classifier" and "model" not in list(conf_props.keys()):
			sys.exit("data,entity_classifier,model are the required configurations")
		elif "threshold" not in list(conf_props.keys()):
			data_file_path=conf_props["data"]
			# threshold=conf_props["threshold"]
			model_dir=conf_props["model"]
			entity_classifier=conf_props["entity_classifier"]
			print("Threshold is missing. Setting default to 0.25")
		else:
			data_file_path=conf_props["data"]
			threshold=conf_props["threshold"]
			model_dir=conf_props["model"]
			entity_classifier=conf_props["entity_classifier"]



	return data_file_path,threshold,model_dir,entity_classifier,conf_props


def check_elastic_search_conf(conf_props):

	es_host=None
	es_port=None
	if  "elasticsearch_host" not in conf_props and "elasticsearch_port" not in conf_props:
		print ("Setting elasticsearch default host and port settings")
		es_host="127.0.0.1"
		es_port="9200"
	elif "elasticsearch_port" not in conf_props and "elasticsearch_host" in conf_props:
		print("ES PORT Not Found. Setting to default")
		es_host=conf_props["elasticsearch_host"]
		es_port="9200"
	elif "elasticsearch_port"  in conf_props and "elasticsearch_host" not in conf_props:
		print("ES HOST NOT FOUND. Setting to default")
		es_port=conf_props["elasticsearch_port"]
		es_host="127.0.0.1"
	else:

		es_host=conf_props["elasticsearch_host"]
		es_port=conf_props["elasticsearch_port"]
	return es_host,es_port