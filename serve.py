import os
import argparse
from do_serve import do_serve, get_model
from check_config import check_config
# from tokenizer import tokenizer
import logging
import random
from flask import Flask
from flask import request
from flask import make_response
import pickle
from do_train import get_intents
app = Flask(__name__)

logger = logging.getLogger(__name__)

model=None
query=None
words_dictionary=None
intent_labels=None
entity_labels=None
model=None
index_name=None
conf_props=None
entity_classifier=None
threshold=None
intents=None
context={}
import json

def create_argparser():
    parser = argparse.ArgumentParser(description='train a custom language parser')
    parser.add_argument('-c', '--config', required=True,help="NLU configuration file")
    # parser.add_argument('-q', '--query', required=True,help="NLU query to be processed")

    return parser


def init():  # pragma: no cover
    

    parser = create_argparser()
    args = parser.parse_args()
    
    return args


@app.route('/query', methods=['POST'])
def query():
    req = request.get_json(silent=True, force=True)
    res=None
    if req.get("query"):
        query=req.get("query")
        res=do_serve(query, words_dictionary, intent_labels, entity_labels, model, index_name,conf_props,entity_classifier,threshold)
        print (res)
        res=response(res["intent"],query)
    r = make_response(json.dumps(res))
    
    r.headers['Content-Type'] = 'application/json'
    return r


def response(results,query,user_id='123'):
    print(context,64)
    # if we have a classification then find the matching intent tag
    if results:
        # loop as long as there are matches to process
        for i in intents['intents']:
            print(i,68)
                # find a tag matching the first result
            if i['intent_name'] == results:
                print(results)
                    # set context for this intent if necessary
                if  i["response"][0]["affected_context"] is not "" :
                       
                    context[user_id] = i["response"][0]['affected_context']       
                    # check if this intent is contextual and applies to this user's conversation
                    print(context,76)
                if i["context_in"] is "" or \
                    (user_id in context and i['context_in'] is not "" and i['context_in'] == context[user_id]):
                        # if show_details: print ('tag:', i['tag'])
                        # a random response from th  
                    print(81)                               
                    return {"response":(random.choice(i['response'][0]['text_response'])),"context_in":i["context_in"],"context_out":i["response"][0]['affected_context']}



if __name__ == '__main__':
    args = init()
    
    data_file_path,threshold,model_dir,entity_classifier,conf_props=check_config(args.config)
    

    data = pickle.load( open( model_dir+"/trained_data", "rb" ) )
    words_dictionary=data["words"]
    intent_labels=data["classes"]
    entity_labels=data["entity_class"]
    
    model,index_name=get_model(model_dir)
    intents=get_intents(data_file_path)
    

    port = int(os.getenv('PORT', 5001))

    print("Starting app on port %d" % port)

    app.run(debug=False, port=port, host='0.0.0.0')

    logger.info("Finished training")    





