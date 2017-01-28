from index import *
import numpy
from numpy import linalg
from constants import *

p = []


# TODO : errors are not handling
def build_pmatrix(alpha):
    doc_id_list = get_doc_id_list()
    # print("docIDs_list",doc_id_list)
    V = float(1 / get_total_count_num())
    for doc_id_row in doc_id_list:
        p.append([])
        out_links = ES_CLIENT.get(index=INDEX_NAME, doc_type='article', id=doc_id_row, ignore=[400, 404])["_source"][
            "out_links"]
        # formula is (1-alpha)p+alpha*V

        if not out_links:
            p[doc_id_row - 1] = [V] * get_total_count_num()
        else:
            for doc_id_col in doc_id_list:
                if MAP_ID_TO_URL[doc_id_col] in out_links:
                    p[doc_id_row - 1].append(1)
                else:
                    p[doc_id_row - 1].append(0)
            if p[doc_id_row - 1].count(1) == 0:
                p[doc_id_row - 1] = [V] * get_total_count_num()

            else:
                count_one = p[doc_id_row - 1].count(1)
                for doc_id_col in doc_id_list:
                    p[doc_id_row - 1][doc_id_col - 1] /= count_one
                    p[doc_id_row - 1][doc_id_col - 1] = (1 - alpha) * p[doc_id_row - 1][doc_id_col - 1] + alpha * V
    #
    # for i in range(0,len(doc_id_list)):
    #     print("i row",i,"row",p[i],"sum",numpy.array(p[i]).sum())
    return p


# calculate left eigon vector
def find_eigenvector(x):
    values, vectors = linalg.eig(numpy.array(x).T)
    left_vector = vectors[:, values.argmax()].T
    left_vector /= left_vector.sum()
    return left_vector.real


def calculate_pagerank(alpha):
    p = build_pmatrix(alpha)
    pagerank_vector = find_eigenvector(p)
    pagerank_vector = pagerank_vector.tolist()

    # saving into elastic
    for doc_id in get_doc_id_list():
        ES_CLIENT.update(index=INDEX_NAME, doc_type=DEFAULT_TYPE, id=doc_id,
                         body={"doc": {"pagerank": pagerank_vector[doc_id - 1]}})
        # with open("json_files/" + MAP_ID_TO_FILE_NAME[doc_id], 'r') as f:
        #     data = json.load(f)
        # data["pagerank"]=pagerank_vector[doc_id-1]
        # with open("json_files/" + MAP_ID_TO_FILE_NAME[doc_id], 'w') as f:
        #     f.write(json.dumps(data))

    # print("pagernk vector is:",pagerank_vector , numpy.array(pagerank_vector).sum())
    return pagerank_vector



    # testing
    # x= [[0.02,0.02,0.88,0.02,0.02,0.02,0.02],
    #     [0.02,0.45,0.45,0.02,0.02,0.02,0.02],
    #     [0.31,0.02,0.31,0.31,0.02,0.02,0.02],
    #     [0.02,0.02,0.02,0.45,0.45,0.02,0.02],
    #     [0.02,0.02,0.02,0.02,0.02,0.02,0.88],
    #     [0.02,0.02,0.02,0.02,0.02,0.45,0.45],
    #     [0.02,0.02,0.02,0.31,0.31,0.02,0.31]]
    # x=[[1/6,2/3,1/6],[5/12,1/6,5/12],[1/6,2/3,1/6]]
    # print(find_eigenvector(x))

    # # print("final p is ", build_pmatrix(0.25))
    # p=build_pmatrix(0.25)
    # v=find_eigenvector(p)
    # x=v.max()
    # print(v.tolist().index(x))
    # # print(MAP_ID_TO_URL[v.tolist().index(x)])
    # print(find_eigenvector(x))
