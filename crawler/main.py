from clustering import clustering
from constants import *
from crawler.spiders.wiki_link_spider import WikiLinkSpider
from vector_creator import *
from index import make_index, delet_index
# from clustering import clustering
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from vector_creator import create_tf_vectors
from pagerank import calculate_pagerank
from retrieve import normal_retrieve, get_url_by_id

while (True):
    print("please enter your choice or -1 for exit:")
    print("1 -> crawl")
    print("2 -> make index")
    print("3 -> cluster")
    print("4 -> calculate page rank")
    print("5 -> search")
    mode = int(input())

    # crawl
    if mode == 1:
        print("enter URLs:")
        start_urls = input()
        print ("enter out degree:")
        out_degree = int(input())
        print("enter number of docs:")
        number_of_docs = int(input())
        # call crawler
        print("crawling starts :")
        settings = get_project_settings()
        settings.overrides['LOG_ENABLED'] = False
        process = CrawlerProcess(settings)
        # WikiLinkSpider.START_URLS=start_urls
        WikiLinkSpider.COUNT_MAX = number_of_docs
        WikiLinkSpider.OUT_MAX = out_degree
        process.crawl(WikiLinkSpider)
        process.start()
    # make index
    elif mode == 2:
        print("please enter your choice:")
        print("1 -> make index")
        print("2 -> delete index")
        mode1 = int(input())
        if mode1 == 1:
            make_index()
        if mode1 == 2:
            delet_index()
            print("index is deleted")
    # cluster
    elif mode == 3:  # TODO
        print("enter k limit :")
        limit = int(input())
        clusters, cluster_labels, k_star, cost_list = clustering(limit, TETA, LANDA, ALPHA, create_tf_vectors())
        print("k* is: ", k_star)
        print("cost in each level to reach k*: ", cost_list)
        print("Clusters: ")
        for cluster_id in cluster_labels:
            print("cluster id: ", cluster_id, ", cluster title: ", cluster_labels[cluster_id],", for doc ids", clusters[cluster_id])
        for doc_id in get_doc_id_list():
            print(doc_id,"'s address is: http://localhost:9200/wiki_index/" + DEFAULT_TYPE + "/" + str(doc_id) +"?pretty=true")


    # calculate pagerank
    elif mode == 4:
        print("enter alpha: ")
        alpha = float(input())
        pagerank_vector = calculate_pagerank(alpha)
        for doc_id in get_doc_id_list():
            print(MAP_ID_TO_FILE_NAME[doc_id], "pagerank is", pagerank_vector[doc_id - 1],
                  " its address is: http://localhost:9200/wiki_index/" + DEFAULT_TYPE + "/" + str(doc_id))
    elif mode == 5:
        print("choose mode")
        print("1 -> normal search")
        print("2 -> in cluster search ")
        mode2=int(input())
        print("enter title query and weight")
        title_query=input()
        title_weight=int (input())
        print("enter abstract query and waight")
        abstract_query=input()
        abstract_weight=int(input())
        print("enter maintext query and waight")
        main_text_query=input()
        main_text_weight=int (input())
        result_list=normal_retrieve(title_query=title_query,title_weight=title_weight,
                        abstract_weight=abstract_weight,abstract_query=abstract_query,
                        main_text_weight=main_text_weight, main_text_query=main_text_query)
        # print(result_list["hits"]['hits'][0])
        retrieved_doc_list = result_list["hits"]["hits"]
        retrieved_doc_ids = []
        print("dd", retrieved_doc_list[0]["_id"])
        for i in range(len(retrieved_doc_list)):
            retrieved_doc_ids.append(retrieved_doc_list[i]["_id"])
        print("sorted retrieved doc ids are: ", retrieved_doc_ids)
        print("enter one two show URL: ")
        id = input()
        if id in retrieved_doc_ids:
            get_url_by_id(id)
        # print(result_list["hits"])
        # print(result_list["hits"]["hits"])
        # print(result_list["hits"]["total"])
        # print(result_list["hits"]["max_score"])

        # get_url_by_id()

    elif mode == -1:
        exit()