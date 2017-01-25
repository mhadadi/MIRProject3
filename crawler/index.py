import os

from elasticsearch import Elasticsearch
import requests
import json

# start elastic server
def make_index():
    r = requests.get('http://localhost:9200')
    doc_id = 1

    # indexing every jsons
    delet_index()
    elastic_search_instance.indices.create(index='wiki_index')##TODO :shards=1
    file_list = os.listdir("json_files/")
    print("file lists:", file_list)
    for file in file_list:
        with open("json_files/" + file, 'r') as f:
            elastic_search_instance.index(index='wiki_index', doc_type='article', id=doc_id, body=json.load(f))
            print("index is build " + str(doc_id))
            print(elastic_search_instance.get(index='wiki_index', doc_type='article', id=doc_id))
            doc_id = doc_id + 1


#print(es.search(index="wiki_index", body={"query": {"match": {'main_text': 'سعدی'}}}))

#deleting index
def delet_index():
    elastic_search_instance.indices.delete(index="wiki_index", ignore=[400, 404])

total_doc_number=id -1
elastic_search_instance = Elasticsearch([{'host': 'localhost', 'port': 9200}])
make_index()
#page rank




