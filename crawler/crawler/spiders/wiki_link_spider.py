import scrapy
from bs4 import BeautifulSoup
from scrapy import statscollectors
from scrapy.exceptions import CloseSpider


class WikiLinkSpider(scrapy.Spider):
    name = "wikilinks"
    COUNT_MAX = 100  # TODO : 1000 pishfarze
    OUT_MAX = 10
    count = 0

    def start_requests(self):
        urls = [
            'https://fa.wikipedia.org/wiki/%D8%B3%D8%B9%D8%AF%DB%8C'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # print("stats:", self.crawler.stats.get_stats()['response_received_count'])
        # print("stats:", self.crawler.stats.get_stats())
        if self.crawler.stats.get_stats()['response_received_count'] >= self.COUNT_MAX and \
                        self.crawler.stats.get_stats()['item_scraped_count'] >= self.COUNT_MAX:
            raise CloseSpider(reason="API usage exceeded")

        soup = BeautifulSoup(response.text, 'lxml')
        title = soup.title.string
        abstract = ''
        main_text = ''
        # print("title: ", title)
        for content_text in soup.find_all(attrs={'id': 'mw-content-text'}):
            paragraphs = content_text.find_all('p')
            abstract = paragraphs[0].get_text()
            print ("abstract: ", abstract)
            for parag in paragraphs:
                if parag.parent.get('id') == 'mw-content-text':


                    # print("parent of p: ", [parent.get('id') for parent in parag.parents])
                    main_text += (' ' + parag.get_text())
            yield {
                'title': title,
                'abstract': abstract,
                'main_text': main_text
            }

            # finding links
            out_degree = 0
            for link in content_text.find_all('a'):  # TODO: change to input parameter
                # print("parent of link: ", [parent.name for parent in link.parents])
                # print("count " ,  self.count)
                if link.parent.name == 'p':
                    next_page = link.get('href')
                    self.count += 1
                    out_degree += 1
                    if self.crawler.stats.get_stats()['response_received_count'] < self.COUNT_MAX:
                        yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

                    if out_degree >= self.OUT_MAX:
                        break
