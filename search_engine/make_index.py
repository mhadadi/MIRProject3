import os

from elasticsearch import Elasticsearch
import requests
import json


#start elastic server
es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
r = requests.get('http://localhost:9200')
id = 1
# while r.status_code == 200:
#     print("200 ok")
file_list = os.listdir("json_files/")
print("file lists:", file_list)
for file in file_list:
    with open("json_files/" + file, 'r') as f:
        es.index(index='wiki_index', doc_type='article', id=id, body=json.load(f))
        print("index is build " + str(id))
        id = id + 1


print(es.search(index="wiki_index", body={"query": {"match": {'title': 'سعدی'}}}))
