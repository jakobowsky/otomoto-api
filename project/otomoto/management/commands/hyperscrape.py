import requests
from bs4 import BeautifulSoup
import re
import time
import asyncio
import aiohttp
import functools

from django.core.management import BaseCommand

from otomoto.models import (
    Car,
    CarBrand,
    CarCategory,
    CarModel,
    CarOffer,
    Color
)

from concurrent.futures import ProcessPoolExecutor, as_completed

#For the future purposes - asynchronic

class Command(BaseCommand):

    def handle(self, *args, **kwargs):

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) '
            'AppleWebKit/537.11 (KHTML, like Gecko) '
            'Chrome/23.0.1271.64 Safari/537.11',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.3',
            'Accept-Encoding': 'none',
            'Accept-Language': 'en-US,en;q=0.8',
            'Connection': 'keep-alive'
        }

        # self.proxies = None
        # self.actual_proxy = None
        # self.used_proxies = set()
        # self.get_actual_proxy()
        # print(self.actual_proxy)
        # print(self.try_proxy(self.actual_proxy))

        p = '203.128.94.102:48476'
        self.proxy = {"http": p, "https": p}
        print(self.try_proxy(self.proxy))

        urls = ['http://www.google.com',
                'http://www.yandex.ru', 'http://www.python.org']

        async def main():
            loop = asyncio.get_event_loop()
            future1 = loop.run_in_executor(None, lambda: requests.get(
                url='http://www.google.com',
                headers=self.headers,
                proxies=self.proxy,
                timeout=4,
            ))
            future2 = loop.run_in_executor(None, lambda: requests.get(
                url='http://www.google.com',
                headers=self.headers,
                proxies=self.proxy,
                timeout=4,
            ))
            response1 = await future1
            response2 = await future2
            print(response1.text)
            print(response2.text)

        loop = asyncio.get_event_loop()
        loop.run_until_complete(main())

        # @asyncio.coroutine
        # def main():
        #     loop = asyncio.get_event_loop()

        # future1 = loop.run_in_executor(None, lambda: requests.get(
        #     url='http://www.google.com',
        #     headers=self.headers,
        #     proxies=self.proxy
        # ))

        # future2 = loop.run_in_executor(None, lambda: requests.get(
        #     url='http://www.google.com',
        #     headers=self.headers,
        #     proxies=self.proxy
        # ))

        #     response1 = yield from future1
        #     response2 = yield from future2
        #     print(response1)
        #     print(response2)

        # loop = asyncio.get_event_loop()
        # loop.run_until_complete(main())

        # /////////////////////////////////////////
        # OLD CODE
        # async def fetch(session, id):
        #     print('Starting {}'.format(id))
        #     url = id

        #     async with session.get(url, proxy=self.proxy) as response:
        #         return BeautifulSoup(await response.content, 'html.parser')

        # async def main(id):
        #     async with aiohttp.ClientSession() as session:
        #         soup = await fetch(session, id)
        #         if 'No record found' in soup.title.text:
        #             print(id, 'na')

        # loop = asyncio.get_event_loop()
        # future = [asyncio.ensure_future(main(id)) for id in urls]

        # loop.run_until_complete(asyncio.wait(future))
        # /////////////////////////////////////////

    # def parse(self,url):
    #     r = requests.get(url)
    #     soup = BeautifulSoup(r.content, 'html.parser')
    #     return soup.find_all('a')

    # rs = (grequests.get(u) for u in urls)
    # requests = grequests.map(rs)
    # for response in requests:
    #     print(response)
    # ////////////////////////////////////////////////////////////////

    def get_actual_proxy(self):
        # we have to change proxy each time when we get banned
        print(self.used_proxies)
        self.proxies = self.get_proxies()
        for proxy in self.proxies:
            print('looking for new proxy')
            if self.try_proxy(proxy):
                if proxy not in self.used_proxies:
                    print('got new one')
                    self.actual_proxy = proxy
                    return

    def try_proxy(self, proxy):
        try:
            requests.get('https://httpbin.org/ip',
                         proxies={"http": proxy, "https": proxy}, timeout=4)
            return True
        except:
            # print(f'bad proxy {proxy}')
            return False

    def get_proxies(self):
        proxy_url = 'https://free-proxy-list.net/'
        soup = BeautifulSoup(requests.get(proxy_url).text, 'html.parser')
        proxies = set()
        for proxy in soup.find(id='proxylisttable').tbody.find_all('tr'):
            if proxy.find_all('td')[6].string == 'no':
                proxies.add(
                    f"{proxy.find_all('td')[0].string}:{proxy.find_all('td')[1].string}")
        return proxies
