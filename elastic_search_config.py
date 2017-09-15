def query_elasticsearch(conf_props):

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