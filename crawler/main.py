from constants import *
from crawler.spiders.wiki_link_spider import WikiLinkSpider
from vector_creator import *
from index import make_index , delet_index
from clustering import clustering
from scrapy.crawler import CrawlerProcess
from scrapy.utils.project import get_project_settings
from vector_creator import create_tf_vectors
from pagerank import calculate_pagerank

while(True):
    print("please enter your choice or -1 for exit:")
    print("1 -> crawl")
    print("2 -> make index")
    print("3 -> cluster")
    print("4 -> calculate page rank")
    print("5 -> search")
    mode = int(input())

    #crawl
    if mode==1:
        print("enter URLs:")
        start_urls=input()
        print ("enter out degree:")
        out_degree=int(input())
        print("enter number of docs:")
        number_of_docs=int(input())
        #call crawler
        print("crawling starts :")
        settings = get_project_settings()
        settings.overrides['LOG_ENABLED'] = False
        process = CrawlerProcess(settings)
        # WikiLinkSpider.START_URLS=start_urls
        WikiLinkSpider.COUNT_MAX=number_of_docs
        WikiLinkSpider.OUT_MAX=out_degree
        process.crawl(WikiLinkSpider)
        process.start()
    #make index
    elif mode == 2:
        print("please enter your choice:")
        print("1 -> make index")
        print("2 -> delete index")
        mode=int(input())
        if mode==1:
            make_index()
        if mode==2:
            delet_index()
            print("index is deleted")
    #cluster
    elif mode == 3:#TODO
        print("enter k limit :")
        limit=int(input())
        clustering(limit,TETA,LANDA,ALPHA,create_tf_vectors() )

    #calculate pagerank
    elif mode == 4:
        print("enter alpha: ")
        alpha=float(input())
        pagerank_vector=calculate_pagerank(alpha)
        for doc_id in get_doc_id_list():
            print(MAP_ID_TO_FILE_NAME[doc_id],"pagerank is",pagerank_vector[doc_id-1] ,
                  " its address is: http://localhost:9200/wiki_index/"+DEFAULT_TYPE+"/"+str(doc_id)+"?pretty=true")
    # elif mode == 5:

    elif mode == -1:
            exit()
    else:
            print("enter valid mode number.")