from constants import *
from vector_creator import *
from index import make_index
from crawler.spiders import wiki_link_spider
import os

while(True):
    print("please enter your choice:")
    print("1 -> crawl")
    print("2 -> make index")
    print("3 -> cluster")
    print("4 -> calculate page rank")
    print("5 -> search")
    mode = int (input())
    if mode==1:
        start_urls=[]
        print("enter URLs:")
        start_urls=input()
        print ("enter out degree:")
        out_degree=input()
        print("enter number of docs:")
        number_of_docs=input()
        #call crawler
        wikilink_spider=wiki_link_spider(start_urls,out_degree,number_of_docs)

    #
    # elif mode == 2:
    # elif mode == 3:
    # elif mode == 4:
    # elif mode == 5:

