import json
import random
from math import sqrt

from numpy.core.numeric import Inf

from mutual_information import get_five_most_commons
from constants import *


def clustering(k_upper_bound, theta, landa, alpha, tf_vector):
    clusters, k_star, cost_list = compute_best_k(k_upper_bound, theta, landa, alpha, tf_vector)
    print("calculating title of clusters...")
    cluster_labels = get_five_most_commons(clusters, tf_vector)
    for cluster_id in clusters.keys():
        cluster_labels[cluster_id] = convert_dic_to_string(cluster_labels[cluster_id])
        print("updating cluster id and title of docs...")
        for doc_id in clusters[cluster_id]:
            ES_CLIENT.update(index=INDEX_NAME,doc_type=DEFAULT_TYPE,id=doc_id,
                body={"doc":{"cluster_id": cluster_id}})
            ES_CLIENT.update(index=INDEX_NAME, doc_type=DEFAULT_TYPE, id=doc_id,
                             body={"doc": {"cluster_title": cluster_labels[cluster_id]}})
    return clusters, cluster_labels, k_star, cost_list


def select_first_mean_points(k, tf_vector):
    # todo: add heuristic or randomness!
    first_points = []
    try:
        rand_doc_id = random.sample(range(1, len(get_doc_id_list()) + 1), k)
    except ValueError:
        print ('Sample size exceeded population size.')
    for i in range(k):

        print ("first rand doc id: " + str(rand_doc_id[i]))
        first_points.append(tf_vector[rand_doc_id[i]])
    return first_points


# todo: handle empty clusters!
def compute_best_k(k_upper_bound, theta, landa, alpha, tf_vector):
    cost_list = [Inf]
    prev_clusters = dict
    clusters = dict
    if k_upper_bound == -1:
        k_upper_bound = Inf
    k = 1
    while k <= k_upper_bound:
        clusters, j_cost = k_means(k, theta, tf_vector)
        j_cost += landa * k
        print ("trying k=", str(k), "...")
        print (abs(cost_list[-1] - j_cost))
        print (j_cost)
        if abs(cost_list[-1] - j_cost) < alpha: # todo: change if needed!
            cost_list.append(j_cost)
            return prev_clusters, k-1, cost_list
        cost_list.append(j_cost)
        prev_clusters = clusters
        k += 1
    print ("no expected clustering in this range of k, please increase upper bound.")
    return clusters, k_upper_bound, cost_list


def value(dic, key):
    if key in dic:
        return dic[key]
    return 0


# # cosine
# def compute_distance(vector, miu):
#     print ("keyss: ", vector.keys())
#     size = sum(vector[key]*vector[key] for key in vector.keys())
#     dist = 0
#     key_intersect = list(set(vector.keys()) & set(miu.keys()))
#     for key in key_intersect:
#         dist += vector[key] * miu[key]
#     return dist/size

# Euclidean distance
def compute_distance(vector, miu):
    if not miu:
        return Inf
    key_union = list(set(vector.keys()) | set(miu.keys()))
    dist = 0
    for key in key_union:
        dist += pow((value(vector, key) - value(miu, key)), 2)
    return sqrt(dist)


# todo: test!
def compute_mean(cluster_doc_ids_list, tf_vector):
    miu = dict()
    c_len = float(len(cluster_doc_ids_list))
    # compute sum of tf's for doc in this cluster
    for doc_id in cluster_doc_ids_list:
        terms_tf = tf_vector[doc_id]
        for term in terms_tf.keys():
            if term not in miu:
                miu.update({term: 0})
            miu[term] += (terms_tf[term])

    miu = {miu_item: miu[miu_item]/c_len for miu_item in miu.keys()}
    # for miu_item in miu.keys():
    #     miu[miu_item] /= c_len
    return miu


# fixed k algorithm
def k_means(k, theta, tf_vector):
    mean_points = select_first_mean_points(k, tf_vector)
    # print ("first_points: ", mean_points[3])
    prev_cost = 0
    next_cost = Inf
    doc_id_list = get_doc_id_list()
    print (doc_id_list)
    print (tf_vector.keys())
    iterate = 0
    clusters = dict()
    while abs(prev_cost-next_cost) > theta:
        clusters = dict()
        j = 0
        #  one iteration of k_means
        for doc_id in doc_id_list:
            min_dist = Inf
            ci = -1
            for cluster_id in range(k):
                # compute distance between a doc vector and a M vector(mean of cluster i)
                dist = compute_distance(tf_vector[doc_id], mean_points[cluster_id])
                if dist < min_dist:
                    min_dist = dist
                    ci = cluster_id
                    # print "in iteration " + str(iterate) + " for doc " + str(doc_id) + "cluster changed to " + str(
                    #     ci) + " with min_dist: " + str(min_dist)

            # print "ci: "+str(ci) + "doc_id: " + str(doc_id)
            # assigning cluster to doc
            if ci in clusters.keys():
                if not doc_id in clusters[ci]:
                    clusters[ci].append(doc_id)
            else:
                clusters.update({ci: [doc_id]})

            j += min_dist
            # print "for doc id " + str(doc_id) + " added to j: " + str(min_dist)
        prev_cost = next_cost
        next_cost = j

        # compute new cluster means
        ####### print clusters
        for cluster_id in range(k):
            if cluster_id in clusters.keys():
                miu_i = compute_mean(clusters[cluster_id], tf_vector)
                # update means...
                mean_points[cluster_id] = miu_i
            # empty cluster!
            else:
                mean_points[cluster_id] = None
        iterate += 1
        # print clusters
        print("cost in iteration " + str(iterate) + ": " + str(next_cost))
    return clusters, next_cost

# test compute_distance
# print compute_distance({'x': 10, 'y': 5}, {'x': 7, 'y': 9, 'z':sqrt(24)})
# print compute_distance({'x': 10, 'y': 5}, {})


def convert_dic_to_string(dic):
    str = ""
    for term in dic.keys():
        str += (term + " ")
    return str