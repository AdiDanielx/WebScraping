from ssl import SSLError
import requests
from bs4 import BeautifulSoup
import re
from collections import deque
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import trafilatura
import os
import yaml 

class WebScraping():

    def __init__(self, config_file):
        with open(config_file, 'r') as f:
            config = yaml.safe_load(f)
        self.url = config['url']
        self.chromeDriverPath = config['chromeDriverPath']

    def all_pages(self):
        urls = set()
        queue = deque([self.url])
        while queue:
            self.url = queue.popleft()
            try:
                r = requests.get(self.url)
                r.encoding = 'utf-8'
            except SSLError as e:
                print(f"SSLError occurred: {e}")
            s = BeautifulSoup(r.content, "html.parser")
            for i in s.find_all("a"):
                href = i.get('href')
                if href and href.startswith("/"):
                    site_url = re.search("^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/\n]+)", self.url)
                    new_site = site_url.group(0) + href
                    if any(substring in new_site for substring in ['/ar/', '/arb/', '/ru/','/en/','/fr/']):
                        continue
                    if new_site not in urls:
                        urls.add(new_site)
                        print(new_site)
                        queue.append(new_site)
        return urls
    
    def extract_html(self,chromeDriverPath,web_url):
        chrome_options = Options()
        chrome_options.add_argument("--headless")  # To run Chrome in headless mode (no GUI)
        service = Service(executable_path=chromeDriverPath)
        driver = webdriver.Chrome(service=service, options=chrome_options)
        driver.get(web_url)
        html_content = driver.page_source
        driver.quit()
        return html_content
    
    def page(self,web_url):
        html_content = self.extract_html(self.chromeDriverPath, web_url)
        page_text = trafilatura.extract(html_content,  as_dict=True)
        soup = BeautifulSoup(html_content, 'html.parser')
        page_title = soup.title.text if soup.title else 'defult'
        page_title = re.sub(r'[\r\n\t:|]+', '_', page_title)
        page_dir = os.path.join('kolzchut', page_title)
        if not os.path.exists(page_dir):
            os.makedirs(page_dir)
        with open(os.path.join(page_dir, f"{page_title}.txt"), 'w', encoding='utf-8') as f:
            f.write(page_text)

    def scrap_all(self):
        for u in self.url:
            ListallPages=[]
            ListallPages = self.all_pages()
            for link in ListallPages:
                self.page(link)

yaml_path = 'C:\\Users\\adida\OneDrive - post.bgu.ac.il\\WebSraping\\requests.yaml'
a = WebScraping(yaml)
B  = a.scrap_all()