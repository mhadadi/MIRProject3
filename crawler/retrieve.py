from constants import *
def normal_retrieve(title_weight,abstract_weight,main_text_weight):
    ES_CLIENT.search(index=INDEX_NAME, doc_type=DEFAULT_TYPE, body={"function_score": {
    "query": {
        { "query_string": {"query": "سعدی شیرازی"} }
    },
    "functions": {
        "DECAY_FUNCTION": {
            "recencyboost": {
                "origin": "0",
                "scale": title_weight
            }
        }
    },
    "score_mode": "sum"
}})