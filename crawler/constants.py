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

VOCAB = []