from index import *
import numpy
from numpy import linalg
p=[]
def build_pmatrix (alpha ):
    doc_id_list= get_doc_id_list()
    print("docIDs_list",doc_id_list)
    V=float(1/TOTAL_DOC_NUMBER)
    for doc_id_row in doc_id_list:
        p.append([])
        out_links=ES_CLIENT.get(index=INDEX_NAME, doc_type='article', id=doc_id_row , ignore=[400,404])["_source"]["out_links"]
        if not out_links:
            p[doc_id_row - 1] = [V]*TOTAL_DOC_NUMBER
            print("aaa",   p[doc_id_row - 1])
            break
        else:
            for doc_id_col in doc_id_list:
                if MAP_ID_TO_URL[doc_id_col] in out_links:
                    p[doc_id_row-1].append(1)
                else:
                    p[doc_id_row-1].append(0)
            if p[doc_id_row-1].count(1)==0:
                p[doc_id_row - 1] = [V] * TOTAL_DOC_NUMBER
                print("bbb", p[doc_id_row - 1])

            else:
                count_one = p[doc_id_row - 1].count(1)
                print("count one",count_one)
                for doc_id_col in doc_id_list:
                    p[doc_id_row-1][doc_id_col-1]/=count_one
                    p[doc_id_row-1][doc_id_col-1]=(1-alpha)*p[doc_id_row-1][doc_id_col-1]+alpha*V
                print("ccc", p[doc_id_row - 1])

    # formula is (1-alpha)p+alpha*V

    # p_out=(1-alpha)*numpy.array(p)+alpha*numpy.array(V*TOTAL_DOC_NUMBER)
    p_out=(1-alpha)*numpy.array(p)+alpha*V


    # for doc_id_row in docIDs_list:
    #     p.append([])
    #     out_degrees=ES_CLIENT.get(index=INDEX_NAME, doc_type='article', id=doc_id_row , ignore=[400,404])["_source"]["out_links"]
    #     print("out degrees is", doc_id_row,"len out degree",len(out_degrees))
    #     for doc_id_col in docIDs_list:
    #         if not out_degrees:
    #             p[doc_id_row-1].append(V)
    #         else:
    #             if MAP_ID_TO_URL[doc_id_col] in out_degrees:
    #                 p[doc_id_row-1].append((1-alpha)*(float(1/len(out_degrees)))+alpha*V)
    #             else:
    #                 p[doc_id_row-1].append(alpha*V)

    for i in range(0,len(doc_id_list)):
        print("i row",i,"row",p_out[i],"sum",numpy.array(p_out[i]).sum())
    return p_out
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

# print("final p is ", build_pmatrix(0.25))
p=build_pmatrix(0.25)
