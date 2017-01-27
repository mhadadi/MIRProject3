from index import *
import numpy
from numpy import linalg
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

# def find_eigenvector(x):
#     values, matrixl, matrixr= eig(x, left=True)
#     matrixl=matrixl.real
#     print(matrixl)
#     left_vector=matrixl[:,0].T
#     print("left vector is ",left_vector)
#     left_vector/=left_vector.sum()
#     return left_vector.real

def find_eigenvector(x):
    values, vectors= linalg.eig(x.T)
    left_vector=vectors[:, values.argmax()]
    left_vector/=left_vector.sum()
    return left_vector.real



#
# x=   [[0.02,0.02,0.88,0.02,0.02,0.02,0.02],
#                 [0.02,0.45,0.45,0.02,0.02,0.02,0.02],
#                 [0.31,0.02,0.31,0.31,0.02,0.02,0.02],
#                 [0.02,0.02,0.02,0.45,0.45,0.02,0.02],
#                 [0.02,0.02,0.02,0.02,0.02,0.02,0.88],
#                 [0.02,0.02,0.02,0.02,0.02,0.45,0.45],
#                 [0.02,0.02,0.02,0.31,0.31,0.02,0.31]]
# x=[[1/6,2/3,1/6],[5/12,1/6,5/12],[1/6,2/3,1/6]]
print(find_eigenvector([[0.1,0.9],[0.3,0.7]]))