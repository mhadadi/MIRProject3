import json
import os

from elasticsearch.exceptions import ElasticsearchException

from constants import *


def make_index():
    # indexing every jsons
    doc_id = 1
    delet_index()
    ES_CLIENT.indices.create(index=INDEX_NAME)  # TODO :shards=1
    # print("file lists:", file_list)
    for tmp_file in FILE_LIST:
        with open("json_files/" + tmp_file, 'r') as f:
            jfile = json.load(f)
            # print("the content of json:", jfile)
            try:
                ES_CLIENT.index(index=INDEX_NAME, doc_type='article', id=doc_id, body=jfile)
                print("index is build " + str(doc_id))
                # print(ES_CLIENT.get(index=INDEX_NAME, doc_type='article', id=doc_id , ignore=[400,404]))
                MAP_ID_TO_URL[doc_id] = jfile["curr_link"]
                MAP_URL_TO_ID[jfile["curr_link"]] = doc_id
                MAP_ID_TO_FILE_NAME.update({doc_id: tmp_file})
                doc_id += 1
            except ElasticsearchException as es1:
                print ("error indexing ",tmp_file," not used id: ", str(doc_id))

    print MAP_ID_TO_FILE_NAME
    print len(MAP_ID_TO_FILE_NAME.keys())
#   deleting index
def delet_index():
    ES_CLIENT.indices.delete(index=INDEX_NAME, ignore=[400, 404])



# print("IT is a test",ES_CLIENT.get(index=INDEX_NAME, doc_type='article', id=2 , ignore=[400,404]))




