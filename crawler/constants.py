import os

from elasticsearch import Elasticsearch

ES_CLIENT = Elasticsearch(hosts=[{'host': 'localhost', 'port': 9200}], timeout=180)
INDEX_NAME = "wiki_index"
MAIN_TEXT = "main_text"
TITLE = "title"
INFO_BOX = "info_box"
ABSTRACT = "abstract"
CURR_LINK = "curr_link"
OUT_LINKS = "out_links"
DEFAULT_TYPE = "article"
CLUSTER_ID="cluster_id"

#clustering consts
TETA = 1
LANDA = 100
ALPHA = 100


VOCAB = []
MAP_ID_TO_URL = {}
MAP_URL_TO_ID = {}
MAP_ID_TO_FILE_NAME = {}

FILE_LIST = os.listdir("json_files/")


def get_doc_id_list():
    return MAP_ID_TO_URL.keys()

def get_total_count_num():
    return len(get_doc_id_list())