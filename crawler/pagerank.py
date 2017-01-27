from index import *
import numpy
from numpy import linalg
p=[]
def build_pmatrix (alpha ):
    docIDs_list= MAP_ID_TO_URL.keys()
    print("docIDs_list",docIDs_list)
    V=float(1/TOTAL_DOC_NUMBER)
    #formula is (1-alpha)p+alpha*V
    for doc_id_row in docIDs_list:
        p.append([])
        out_degrees=ES_CLIENT.get(index=INDEX_NAME, doc_type='article', id=doc_id_row , ignore=[400,404])["_source"]["out_links"]
        print("out degrees is",out_degrees , doc_id_row)
        for doc_id_col in docIDs_list:
            if not out_degrees:
                p[doc_id_row-1].append(alpha*V)
            else:
                if MAP_ID_TO_URL[doc_id_col] in out_degrees:
                    p[doc_id_row-1].append((1-alpha)*(float(1/len(out_degrees)))+alpha*V)
                else:
                    p[doc_id_row-1].append(0)
    return p
#calculate left eigon vector
def find_eigenvector(x):
    values, vectors= linalg.eig(numpy.array(x).T)
    left_vector=vectors[:, values.argmax()].T
    left_vector/=left_vector.sum()
    return left_vector.real



#
# x= [[0.02,0.02,0.88,0.02,0.02,0.02,0.02],
#     [0.02,0.45,0.45,0.02,0.02,0.02,0.02],
#     [0.31,0.02,0.31,0.31,0.02,0.02,0.02],
#     [0.02,0.02,0.02,0.45,0.45,0.02,0.02],
#     [0.02,0.02,0.02,0.02,0.02,0.02,0.88],
#     [0.02,0.02,0.02,0.02,0.02,0.45,0.45],
#     [0.02,0.02,0.02,0.31,0.31,0.02,0.31]]
# x=[[1/6,2/3,1/6],[5/12,1/6,5/12],[1/6,2/3,1/6]]
# print(find_eigenvector(x))

print("final p is ", build_pmatrix(0.1))

