from clustering import *
from constants import *
from vector_creator import *
from index import make_index

make_index()
# get_doc_term_frequency(doc_id=1,doc_type=DEFAULT_TYPE)
tf_vector = create_tf_vectors()
k = 5
# k_means(k, 0.1, tf_vector)
print clustering(10,0.1,10,10,tf_vector)