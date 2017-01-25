from index import *
from numpy import linalg as LA
p=[]
def build_pmatrix (alpha ):
    docIDs_list= MAP_ID_TO_URL.keys()
    V=float(1/TOTAL_DOC_NUMBER)
    for doc_id_row in docIDs_list:
        p[doc_id_row]=[]
        out_degrees=ES_CLIENT.get(index=INDEX_NAME, doc_type='article', id=doc_id_row , ignore=[400,404])["source"]["out_links"]
        for doc_id_col in docIDs_list:
            if not out_degrees:
                p[doc_id_row][doc_id_col]=alpha*V
            else:
                if doc_id_col in out_degrees:
                    p[doc_id_row][doc_id_col]=(1-alpha)*(float(1/len(out_degrees)))+alpha*V
                else:
                    p[doc_id_row][doc_id_col]=0

def find_eigenvector():
    w, v = LA.eig(p)
    print("eigen vector of p is:",v)
