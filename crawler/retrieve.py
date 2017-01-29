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


def normal_retrieve_pagerank(title_weight, abstract_weight, main_text_weight, title_query, abstract_query,
                             main_text_query):
    return ES_CLIENT.search(index=INDEX_NAME, doc_type=DEFAULT_TYPE, body={
        "query": {
            "function_score": {
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
                },
                "field_value_factor": {
                    "field": "pagerank",
                },
                "score_mode": "sum",
            }

        }

    })


def cluster_retrieve(title_weight, abstract_weight, main_text_weight, title_query, abstract_query, main_text_query,
                     cluster_id):
    return ES_CLIENT.search(index=INDEX_NAME, doc_type=DEFAULT_TYPE, body={
        "query": {
            "bool": {
                "must": {
                    "term": {CLUSTER_ID: cluster_id}
                },
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


def cluster_retrieve_pagerank(title_weight, abstract_weight, main_text_weight, title_query, abstract_query,
                              main_text_query, cluster_id):
    return ES_CLIENT.search(index=INDEX_NAME, doc_type=DEFAULT_TYPE, body={
        "query": {
            "function_score": {
                "query": {
                    "bool": {
                        "must": {
                            "term": {CLUSTER_ID: cluster_id}
                        },
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
                },
                "field_value_factor": {
                    "field": "pagerank",
                },
                "score_mode": "sum",
            }

        }

    })


def get_url_by_id(id):
    return ES_CLIENT.get(index=INDEX_NAME, doc_type=DEFAULT_TYPE, id=id)["_source"][CURR_LINK]
