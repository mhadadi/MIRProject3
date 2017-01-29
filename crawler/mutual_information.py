from collections import Counter
from math import log

from constants import get_total_count_num, VOCAB, get_doc_id_list


# root method
def get_five_most_commons(clusters, tf_vector):
    return compute_mutual_information(clusters, tf_vector)


def compute_mutual_information(clusters,tf_vector):
    count_total_doc = float(get_total_count_num())
    I = dict(dict())
    five_most_common = dict()
    for cluster_id in clusters:
        if len(clusters[cluster_id]) == 0:
            continue
        p_c_1 = len(clusters[cluster_id])/count_total_doc
        in_cluster_doc_id_list = clusters[cluster_id]
        count_cluster_doc = len(in_cluster_doc_id_list)
        for vocab in VOCAB:
            p_t_1_c_1 = 0
            p_t_0_c_1 = 0
            p_t_1_c_0 = 0
            p_t_0_c_0 = 0
            count_doc_has_vocab = 0
            for doc_id in get_doc_id_list():
                if vocab in tf_vector[doc_id]:
                    # print (vocab, "vocab is in doc id:", doc_id)
                    count_doc_has_vocab += 1      #computing T_1
                if doc_id in in_cluster_doc_id_list:
                    if vocab in tf_vector[doc_id].keys():  # doc kalame t ra darad va dar khushe c hast
                        p_t_1_c_1 += 1
                else:
                    if vocab in tf_vector[doc_id].keys():
                        p_t_1_c_0 += 1

            # p_t_0_c_1 is ready for vocab
            p_t_0_c_1 = (count_cluster_doc - p_t_1_c_1) / count_total_doc
            # p_T_1_C_1 is ready for vocab!
            p_t_1_c_1 /= count_total_doc
            # p_t_0_c_0 is ready for vocab
            count_not_in_cluster_doc = count_total_doc - count_cluster_doc
            p_t_0_c_0 = (count_not_in_cluster_doc - p_t_1_c_0) / count_total_doc
            # p_T_1_C_1 is ready for vocab!
            p_t_1_c_0 /= count_total_doc

            p_t_1 = count_doc_has_vocab/count_total_doc

            # print ("t_1: ", p_t_1)
            # print ("c_1: ", p_c_1)
            # print ("p_t_0_c_0: ", p_t_0_c_0)
            # print ("p_t_1_c_0: ", p_t_1_c_0)
            # print ("p_t_0_c_1: ", p_t_0_c_1)
            # print ("p_t_1_c_1: ", p_t_1_c_1)

            if cluster_id not in I:
                I.update({cluster_id: {vocab: 0}})  # TODO
            if vocab not in I[cluster_id]:
                I[cluster_id].update({vocab: 0})
            I[cluster_id][vocab] += (((p_t_1_c_1 * log(p_t_1_c_1/(p_t_1 * p_c_1), 2)) if p_t_1_c_1 else 0) +
                                     ((p_t_1_c_0 * log(p_t_1_c_0/((1-p_c_1) * p_t_1), 2)) if p_t_1_c_0 else 0) +
                                     ((p_t_0_c_1 * log(p_t_0_c_1/((1-p_t_1) * p_c_1), 2)) if p_t_0_c_1 else 0) +
                                     ((p_t_0_c_0 * log(p_t_0_c_0/((1-p_t_1)*(1-p_c_1)), 2)) if p_t_0_c_0 else 0))


            # print ("I(c,t): ", I[cluster_id][vocab])

        five_most_common.update({cluster_id: dict(Counter(I[cluster_id]).most_common(5))})
        # print ("5 most common for cluster ",cluster_id,": ", five_most_common[cluster_id]
        # print(convert_dic_to_string(five_most_common[cluster_id]))
    return five_most_common


