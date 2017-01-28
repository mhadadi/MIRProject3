from constants import *


def normal_retrieve(title_weight, abstract_weight, main_text_weight, title_query, abstract_query, main_text_query):
    return ES_CLIENT.search(index=INDEX_NAME, doc_type=DEFAULT_TYPE, body={
        "query": {
            "bool": {
                "should": [
                    {"match": {
                        TITLE: {
                            "query": title_query,
                            "boost": title_weight
                        }}},
                    {"match": {
                        ABSTRACT: {
                            "query": abstract_query,
                            "boost": abstract_weight
                        }}},
                    {"match": {
                        MAIN_TEXT: {
                            "query": main_text_query,
                            "boost": main_text_weight
                        }}},
                ]
            }
        }

    })


def get_url_by_id(id):
    return ES_CLIENT.get(index=INDEX_NAME, doc_type=DEFAULT_TYPE, id=id)["_source"][CURR_LINK]


def get_in_fix_cluster(title_weight, abstract_weight, main_text_weight, title_query, abstract_query, main_text_query,
                       cluster_id):
    return ES_CLIENT.search(index=INDEX_NAME, doc_type=DEFAULT_TYPE, body={
        "query": {
            "bool": {
                "must": {"term": {"cluster_id": cluster_id}},
                "should": [
                    {"match": {
                        TITLE: {
                            "query": title_query,
                            "boost": title_weight
                        }}},
                    {"match": {
                        ABSTRACT: {
                            "query": abstract_query,
                            "boost": abstract_weight
                        }}},
                    {"match": {
                        MAIN_TEXT: {
                            "query": main_text_query,
                            "boost": main_text_weight
                        }}},
                ]
            }
        }

    })
