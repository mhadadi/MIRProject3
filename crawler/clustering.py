# todo:
import math
from math import sqrt

from numpy.core.numeric import Inf
from pyasn1.type import char

from constants import *


def select_first_mean_points(k,tf_vector):
    # todo: add heuristic or randomness!
    first_points = []
    for i in range(k):
        first_points.append(tf_vector[i+1])
    return first_points


# todo:
def compute_best_k(k_upper_bound):
    return k_upper_bound


def compute_j(clusters_cost):
    j = 0
    for key in clusters_cost.keys():
        j += clusters_cost[key]
    return j


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
    key_union = list(set(vector.keys()) | set(miu.keys()))
    dist = 0
    for key in key_union:
        dist += pow((value(vector, key) - value(miu, key)), 2)
    return sqrt(dist)


# todo: test!
def compute_mean(cluster_doc_ids_list, tf_vector):
    miu = dict()
    c_len = len(cluster_doc_ids_list)
    # compute sum of tf's for doc in this cluster
    for doc_id in cluster_doc_ids_list:
        terms_tf = tf_vector[doc_id]
        for term in terms_tf.keys():
            if term not in miu:
                miu.update({term: 0})
            miu[term] += (terms_tf[term]/c_len)
    return miu


# fixed k algorithm
def k_means(k, theta, tf_vector):
    mean_points = select_first_mean_points(k, tf_vector)
    # print ("first_points: ", mean_points[3])
    cost = Inf
    doc_id_list = get_doc_id_list()
    print doc_id_list
    print tf_vector.keys()
    iterate = 0
    while cost > theta:
        clusters = dict()
        clusters_cost = dict()
        j=0
        #  one iteration of k_means
        for doc_id in doc_id_list:
            min_dist = Inf
            ci = -1
            for i in range(k):
                # print("in for")
                # print ("tf_vector", tf_vector[doc_id])
                # compute distance between a doc vector and a M vector(mean of cluster i)
                dist = compute_distance(tf_vector[doc_id], mean_points[i])
                if dist < min_dist:
                    min_dist = dist
                    ci = i
            # print "ci: "+str(ci) + "doc_id: " + str(doc_id)
            # assigning cluster to doc
            if ci in clusters.keys():
                if not doc_id in clusters[ci]:
                    clusters[ci].append(doc_id)
            else:
                clusters.update({ci: [doc_id]})

            j += min_dist

        cost = j
        #niazi nabud bedunim male kudum khushan cost ha!!
        #     # updatind cluster cost
        #     if ci in clusters_cost.keys():
        #         clusters_cost[ci] += min_dist
        #     else:
        #         clusters_cost.update({ci: min_dist})
        #
        # # compute cost of clustering
        # cost = compute_j(clusters_cost)

        # compute new cluster means
        ####### print clusters
        for i in range(k):
            miu_i = compute_mean(clusters[i], tf_vector)
            # if i==3:
            #     print "centroid of third cluster " + str(miu_i)
            #     print tf_vector[3]
            # update means...
            mean_points[i] = miu_i
        iterate += 1
        print("cost in iteration " + str(iterate) + ": " + str(cost))

