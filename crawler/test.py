from mutual_information import compute_mutual_information
from clustering import *
from index import make_index
from vector_creator import *

make_index()
# get_doc_term_frequency(doc_id=1,doc_type=DEFAULT_TYPE)
tf_vector = create_tf_vectors()
k = 10
# k_means(k, 0.1, tf_vector)
clusters, k_star, cost_list = clustering(k_upper_bound=k, theta=10, landa=100, alpha=100, tf_vector=tf_vector)
print ("clusters: ", clusters)
print ("k*: ", k_star)
print ("cost list: ", cost_list)

compute_mutual_information(clusters,tf_vector)