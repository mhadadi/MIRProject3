from clustering import *
from constants import *
from vector_creator import *
from index import make_index

make_index()
# get_doc_term_frequency(doc_id=1,doc_type=DEFAULT_TYPE)
tf_vector = create_tf_vectors()
k = -1
# k_means(k, 0.1, tf_vector)
clusters, k_star, cost_list = clustering(k_upper_bound=k, theta=0.1, landa=100, alpha=1000, tf_vector=tf_vector)
print ("clusters: ", clusters)
print ("k*: ", k_star)
print ("cost list: ", cost_list)
