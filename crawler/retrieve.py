from constants import ES_CLIENT,INDEX_NAME
def normal_retrieve  (title_weight,abstract_weight, main_text_weight):
    query="{fun}"
    res = ES_CLIENT.search(index=INDEX_NAME, body=query)
def cluster_retrieve (title_weight,abstract_weight, main_text_weight, cluster_id):

def pagerank_retrieve (title_weight,abstract_weight, main_text_weight):

