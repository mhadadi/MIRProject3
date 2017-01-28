from constants import *
def normal_retrieve(title_weight, abstract_weight, main_text_weight, title_query,introduction_query,text_query):
    print(ES_CLIENT.search(index=INDEX_NAME, doc_type=DEFAULT_TYPE, body={
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
                            "query": text_query,
                            "boost": abstract_weight
                        }}},
                    {"match": {
                        MAIN_TEXT: {
                            "query": introduction_query,
                            "boost": main_text_weight
                        }}},
                ]
            }
        }

}))