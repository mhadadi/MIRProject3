from elasticsearch import Elasticsearch

ES_CLIENT = Elasticsearch([{'host': 'localhost', 'port': 9200}])
INDEX_NAME = "wiki_index"


