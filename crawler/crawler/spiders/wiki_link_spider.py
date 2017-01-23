import scrapy


class WikiLinkSpider(scrapy.Spider):
    name = "wikilinks"

    def start_requests(self):
        urls = [
            'https://fa.wikipedia.org/wiki/%D8%B3%D8%B9%D8%AF%DB%8C'
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        page = response.url.split("/")[-2]
        filename = 'quotes-%s.html' % page
        with open(filename, 'wb') as f:
            f.write(response.body)
        self.log('Saved file %s' % filename)
