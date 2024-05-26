from bs4 import BeautifulSoup
import os
import re
import trafilatura
from scrapy.spiders import CrawlSpider , Rule
from scrapy.linkextractors import LinkExtractor

class WebScraper(CrawlSpider):


    name ='adi'
    start_urls = ['https://www.kolzchut.org.il/']
    allowed_domains = ['kolzchut.org.il']
    rules = [Rule (LinkExtractor(allow=(allowed_domains[0])), callback='parse_item', follow=True)]

    def parse_item(self, response):
        if any(substring in response.url for substring in ['/ar/', '/arb/', '/ru/', '/en/', '/fr/']):
            return
        html = trafilatura.fetch_url(response.url)
        page_text = trafilatura.extract(html,  as_dict=True)
        soup = BeautifulSoup(response.text, 'html.parser')
        page_title = soup.title.text if soup.title else 'defult'
        page_title = re.sub(r'[\r\n\t:|]+', '_', page_title)
        page_dir = os.path.join('kolzchut', page_title)
        if not os.path.exists(page_dir):
            os.makedirs(page_dir)
        with open(os.path.join(page_dir, f"{page_title}.txt"), 'w', encoding='utf-8') as f:
            f.write(page_text)
