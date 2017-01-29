import json

import scrapy
from bs4 import BeautifulSoup
from scrapy.exceptions import CloseSpider
from time import sleep


class WikiLinkSpider(scrapy.Spider):
    name = "wikilinks"
    COUNT_MAX = 1000  # TODO : 1000 pishfarze
    OUT_MAX = 10
    START_URLS=['https://fa.wikipedia.org/wiki/%D8%B3%D8%B9%D8%AF%DB%8C']

    scraped_count = 0

    def start_requests(self):
        for url in self.START_URLS:
            yield scrapy.Request(url=url, callback=self.parse)

    def save_data_as_json(self, data):
        with open("json_files/file" + str(self.scraped_count) + '.json', 'w') as f:
            # json.dump(data, f, encoding='utf-8')
            json.dump(data, f)

    def parse(self, response):
        # print("stats:", self.crawler.stats.get_stats()['response_received_count'])
        # print("stats:", self.crawler.stats.get_stats())
        if self.crawler.stats.get_stats()['response_received_count'] >= self.COUNT_MAX and \
                        self.scraped_count >= self.COUNT_MAX:
            # self.crawler.stats.get_stats()['item_scraped_count'] >= self.COUNT_MAX:
            raise CloseSpider(reason="API usage exceeded")

        soup = BeautifulSoup(response.text, 'lxml')
        # title = soup.title.string
        # print("aaaaa",soup.find(attrs={"id":"firstHeading"}).get_text())
        title = soup.find(attrs={"id": "firstHeading"}).get_text()

        main_text = ''
        out_links = []

        # print("title: ", title)
        for content_text in soup.find_all(attrs={'id': 'mw-content-text'}):
            paragraphs = content_text.find_all('p')
            links = content_text.find_all('a')
            for link in links:
                if link.parent.name=="p":
                    out_link=link.get('href')
                    out_links.append(response.urljoin(out_link))
            info = content_text.find(attrs={'class': 'infobox'})
            # print("info: ", info)
            abstract = ""
            for parag in paragraphs:
                if parag.parent.get('id') == 'mw-content-text':
                    if not abstract:
                        abstract = parag.get_text()
                        # print("abstract: ", abstract)
                    # print("parent of p: ", [parent.get('id') for parent in parag.parents])
                    main_text += (' ' + parag.get_text())

            # finding links
            out_degree = 0
            for link in links:  # TODO: change to input parameter
                # print("parent of link: ", [parent.name for parent in link.parents])
                # print("count " ,  self.count)
                if link.parent.name == 'p':
                    # if ':' in link.text:
                    #     print("linnnk hasssss :", link.text)
                    if (':' not in link.text) and (link.get('href') is not None) and ('wiki' in link.get('href')):
                        next_page = link.get('href')
                        out_degree += 1
                        if self.crawler.stats.get_stats()['response_received_count'] < self.COUNT_MAX:
                            out_links.append(response.urljoin(next_page))
                            yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

                        if out_degree >= self.OUT_MAX:
                            break

            info_box = {}
            if info:
                for table_row in info.find_all('tr'):
                    # print("table row: ", table_row)
                    # print ("td: ", table_row.find('td'))
                    td = table_row.find('td')
                    th = table_row.find('th')
                    if th and td:
                        info_box[th.get_text()] = td.get_text()
            # print('info_box: ', self.scraped_count, " ", info_box)

            # export or yield data
            data = {
                'title': title,
                'abstract': abstract,
                'main_text': main_text,
                'curr_link': str(response.url),
                'out_links': out_links,
                'info_box': info_box,
                'pagerank':0,
                'cluster_title':"",
                'cluster_id':0
            }

            self.scraped_count += 1

            #progress_bar
            if self.scraped_count%(self.COUNT_MAX//20)==0:
                progressbar='+'*(self.scraped_count//(self.COUNT_MAX//20))+'-'*(20-(self.scraped_count//(self.COUNT_MAX//20)))
                print("crawling progress:",progressbar)

            self.save_data_as_json(data=data)

