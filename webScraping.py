from ssl import SSLError

import requests
from bs4 import BeautifulSoup
import re
from collections import deque

def scrape(site):
    urls = set()
    queue = deque([site])

    while queue:
        site = queue.popleft()
        try:
            r = requests.get(site)
            r.encoding = 'utf-8'
        except SSLError as e:
            print(f"SSLError occurred: {e}")
        s = BeautifulSoup(r.content, "html.parser")
        for i in s.find_all("a"):
            href = i.get('href')
            if href and href.startswith("/"):
                site_url = re.search("^(?:https?:\/\/)?(?:[^@\/\n]+@)?(?:www\.)?([^:\/\n]+)", site)
                new_site = site_url.group(0) + href
                if new_site not in urls:
                    urls.add(new_site)
                    print(new_site)
                    queue.append(new_site)
    return urls
