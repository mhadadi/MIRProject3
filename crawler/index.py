import json
import os

import requests
from twisted.conch.scripts.cftp import _ignore

from constants import ES_CLIENT,INDEX_NAME


# start elastic server
def make_index():
    # r = requests.get('http://localhost:9200')
    doc_id = 1

    # indexing every jsons
    delet_index()
    ES_CLIENT.indices.create(index=INDEX_NAME)##TODO :shards=1
    file_list = os.listdir("json_files/")
    print("file lists:", file_list)
    for file in file_list:
        with open("json_files/" + file, 'r') as f:
            print("index is being build " + str(doc_id) + str(file))
            ES_CLIENT.index(index=INDEX_NAME, doc_type='article', id=doc_id, body=json.load(f), ignore=400)
            print(ES_CLIENT.get(index=INDEX_NAME, doc_type='article', id=doc_id, ignore=404))
            doc_id = doc_id + 1
    return doc_id-1

#deleting index
def delet_index():
    ES_CLIENT.indices.delete(index=INDEX_NAME, ignore=[400, 404])


TOTAL_DOC_NUMBER = make_index()
#page rank




