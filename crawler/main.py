from clustering import k_means
from constants import *
from vector_creator import *
from index import make_index
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
import os

# make_index()
# # get_doc_term_frequency(doc_id=1,doc_type=DEFAULT_TYPE)
# tf_vector = create_tf_vectors()
# k = 5
# k_means(k, 1, tf_vector)
while(True):
    print("please enter your choice:")
    print("1 -> crawl")
    print("2 -> make index")
    print("3 -> cluster")
    print("4 -> calculate page rank")
    print("5 -> search")
    mode = int (input())
    if mode==1:
        input_urls=[]
        print("enter URLs:")
        input_urls=input()
        print ("enter out degree:")
        out_degree=input()
        print("enter number of docs:")
        number_of_docs=input()
        #call crawler
        os.chdir('./crawler')
        settings = get_project_settings()
        process = CrawlerProcess(settings)
            process.crawl('wikipedia', start_urls=start_urls, out_degree=out_degree, total_pages=total_pages,
                          output_path='../data/')
            process.start()
    elif mode == 2:
    elif mode == 3:
    elif mode == 4:
    elif mode == 5:

