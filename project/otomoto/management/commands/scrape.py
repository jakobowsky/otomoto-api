import requests
from bs4 import BeautifulSoup

from django.core.management import BaseCommand


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument('car_brand', help='Brand of cars you want to scrape')
        parser.add_argument('pages', type=int , help='Number of pages to scraoe')

    def handle(self, *args, **kwargs):
        self.car_brand = kwargs['car_brand']
        self.pages = kwargs['pages']
        self.proxies = self.get_proxies()
        for proxy in self.proxies[:10]:
            self.try_proxy(proxy)

    def try_proxy(self, proxy):
        try:
            response = requests.get('https://httpbin.org/ip', proxies={"http": proxy, "https": proxy}, timeout=3)
            print (response.text)
        except:
            print(f'bad proxy {proxy}')

    def get_proxies(self):
        proxy_url = 'https://free-proxy-list.net/'
        soup = BeautifulSoup(requests.get(proxy_url).text, 'html.parser')
        proxies = set()
        for proxy in soup.find(id='proxylisttable').tbody.find_all('tr'):
            proxies.add(f"{proxy.find_all('td')[0].string}:{proxy.find_all('td')[1].string}")
        return proxies
