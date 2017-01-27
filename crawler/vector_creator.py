# GET /wiki_index/article/1/_termvectors
# {
#     "fields": ["title"],
#   "offsets" : true,
#   "payloads" : true,
#   "positions" : true,
#   "term_statistics" : true,
#   "field_statistics" : false
# }
from constants import *


def get_doc_term_frequency(doc_id, doc_type):
    a = ES_CLIENT.termvectors(index=INDEX_NAME, id=doc_id, doc_type=doc_type,
                              fields=[MAIN_TEXT],
                              offsets=False,
                              payloads=False,
                              positions=False,
                              field_statistics=False,
                              term_statistics=True)
    term_vec = a["term_vectors"][MAIN_TEXT]["terms"]
    tmp_dic = {}
    tokens = term_vec.keys()
    add_to_vocab(tokens)
    [tmp_dic.update({token: term_vec[token]["term_freq"]}) for token in tokens]
    print("****************************")
    print(tmp_dic)
    return {doc_id:tmp_dic}
    # .get(index=INDEX,id=doc_id,doc_type=doc_type,params=)


def add_to_vocab(tokens):
    for token in tokens:
        if not token in VOCAB:
            VOCAB.append(token)


def create_tf_vectors():
    tf_vector = dict()
    for doc_id in range(1, 20):
        tf_vector.update(get_doc_term_frequency(doc_id,DEFAULT_TYPE))
    print tf_vector
    return tf_vector




# ###TODO:  TEEEESSSSSTTTTTTT
# def create_doc_term_matrix():
#     matrix={}
#     for doc_id in range(1,20):#TODO: MAP_ID_TO_URL.keys():
#         count=0
#         print("doc id: ", doc_id)
#         tf_dic = get_doc_term_frequency(doc_id,DEFAULT_TYPE)
#         tmp_list = []
#         for i in range(len(VOCAB)):
#             print ("VOCAB{i}: ",VOCAB[i])
#             if VOCAB[i] in tf_dic:
#                 print ("tf[...]: ", tf_dic[VOCAB[i]])
#
#                 tmp_list.append(tf_dic[VOCAB[i]])
#                 count += tf_dic[VOCAB[i]]
#
#             else:
#                 tmp_list.append(0)
#             # tmp_list[i] = tf_dic[VOCAB[i]]
#         print tmp_list
#         print count
#         matrix.update({doc_id: tmp_list})
#     return matrix
