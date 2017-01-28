import json
import os

from elasticsearch.exceptions import ElasticsearchException

from constants import *


def make_index():
    doc_id = 1
    # indexing every jsons
    delet_index()
    ES_CLIENT.indices.create(index=INDEX_NAME)  # TODO :shards=1
    file_list = os.listdir("json_files/")
    # print("file lists:", file_list)
    for tmp_file in file_list:
        with open("json_files/" + tmp_file, 'r') as f:
            jfile = json.load(f)
            # print("the content of json:", jfile)
            try:
                ES_CLIENT.index(index=INDEX_NAME, doc_type='article', id=doc_id, body=jfile)
                print("index is build " + str(doc_id))
                # print(ES_CLIENT.get(index=INDEX_NAME, doc_type='article', id=doc_id , ignore=[400,404]))
                MAP_ID_TO_URL[doc_id] = jfile["curr_link"]
                MAP_URL_TO_ID[jfile["curr_link"]] = doc_id
                doc_id += 1
            except ElasticsearchException as es1:
                print ("error indexing " , str(doc_id))

    return doc_id - 1


#   deleting index
def delet_index():
    ES_CLIENT.indices.delete(index=INDEX_NAME, ignore=[400, 404])


TOTAL_DOC_NUMBER = make_index()

# print("IT is a test",ES_CLIENT.get(index=INDEX_NAME, doc_type='article', id=2 , ignore=[400,404]))




