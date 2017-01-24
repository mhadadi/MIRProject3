from elasticsearch import Elasticsearch
import requests
import json


es = Elasticsearch([{'host': 'localhost', 'port': 9200}])
r = requests.get('http://localhost:9200')
i = 18
while r.status_code == 200:
    print("200 ok")
    r1 = requests.get('http://swapi.co/api/people/' + str(i))
    es.index(index='sw', doc_type='people', id=i, body=json.loads((r1.content).decode("utf-8")))
    i = i + 1

print(es.search(index="sw", body={"query": {"match": {'name': 'Darth Vader'}}}))
