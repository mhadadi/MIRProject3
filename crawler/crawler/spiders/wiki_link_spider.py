import scrapy
from bs4 import BeautifulSoup


class WikiLinkSpider(scrapy.Spider):
    name = "wikilinks"
    COUNT_MAX = 100  #TODO : 1000 pishfarze
    OUT_MAX = 10
    count = 0

    def start_requests(self):
        urls = [
            'https://fa.wikipedia.org/wiki/%D8%B3%D8%B9%D8%AF%DB%8C'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    # def parse(self, response):
    #     page = response.url.split("/")[-2]
    #     filename = 'quotes-%s.html' % page
    #     with open(filename, 'wb') as f:
    #         f.write(response.body)
    #     self.log('Saved file %s' % filename)

    def parse(self, response):
        # use lxml to get decent HTML parsing speed
        soup = BeautifulSoup(response.text, 'lxml')
        title = soup.title.string
        abstract = ''
        main_text = ''
        print("title: ", title)
        for content_text in soup.find_all(attrs={'id': 'mw-content-text'}):
            paragraphs = content_text.find_all('p')
            abstract = paragraphs[0].get_text()
            print ("intro: ", abstract)
            for parag in paragraphs:
                print("parent of p: ", [parent.name for parent in parag.parents])
                main_text += (' ' + parag.get_text())
            yield {
                'title': title,
                'abstract': abstract,
                'main_text': main_text
            }
            # finding links
            out_degree = 0;
            for link in content_text.find_all('a'):   #TODO: change to input parameter
                print("parent of link: ", [parent.name for parent in link.parents])
                print("count " ,  self.count)
                if link.parent.name == 'p':
                    print ("in if by parent: ", link.parent.name)
                    if self.count < self.COUNT_MAX:
                        next_page = link.get('href')
                        self.count += 1
                        out_degree +=1

                        yield scrapy.Request(response.urljoin(next_page), callback=self.parse)

                if out_degree >= self.OUT_MAX:
                    break



#
# class BlogSpider(scrapy.Spider):
#     name = 'blogspider'
#     start_urls = ['https://blog.scrapinghub.com']
#
#     def parse(self, response):
#         for title in response.css('h2.entry-title'):
#             yield {'title': title.css('a ::text').extract_first()}
#
#         next_page = response.css('div.prev-post > a ::attr(href)').extract_first()
#         if next_page:
#             yield scrapy.Request(response.urljoin(next_page), callback=self.parse)
