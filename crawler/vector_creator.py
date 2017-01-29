# GET /wiki_index/article/1/_termvectors
# {
#     "fields": ["title"],
#   "offsets" : true,
#   "payloads" : true,
#   "positions" : true,
#   "term_statistics" : true,
#   "field_statistics" : false
# }
from index import get_total_count_num
from constants import *


def get_doc_term_frequency(doc_id, doc_type):
    a = ES_CLIENT.termvectors(index=INDEX_NAME, id=doc_id, doc_type=doc_type,
                              fields=[MAIN_TEXT],
                              offsets=False,
                              payloads=False,
                              positions=False,
                              field_statistics=False,
                              term_statistics=True, ignore=[400, 404])
    if "term_vectors" in a.keys() and MAIN_TEXT in a["term_vectors"].keys():
        term_vec = a["term_vectors"][MAIN_TEXT]["terms"]
        tmp_dic = {}
        tokens = term_vec.keys()
        add_to_vocab(tokens)
        [tmp_dic.update({token: term_vec[token]["term_freq"]}) for token in tokens]
        # print("****************************", " ",doc_id)
        # print(tmp_dic)
        return {doc_id: tmp_dic}
    else:
        ########## print ("no term vectors ", str(doc_id))
        return {doc_id: {}}
    # .get(index=INDEX,id=doc_id,doc_type=doc_type,params=)


def add_to_vocab(tokens):
    for token in tokens:
        if not token in VOCAB:
            VOCAB.append(token)


def create_tf_vectors():
    tf_vector = dict()
    for doc_id in get_doc_id_list():
        tf_vector.update(get_doc_term_frequency(doc_id,DEFAULT_TYPE))
    return tf_vector



