import requests
from bs4 import BeautifulSoup
import re

from django.core.management import BaseCommand

from otomoto.models import (
    Car,
    CarBrand,
    CarCategory,
    CarModel,
    CarOffer,
    Color
)


class Command(BaseCommand):

    def add_arguments(self, parser):
        parser.add_argument(
            'car_brand', help='Brand of cars you want to scrape')
        parser.add_argument('pages', type=int,
                            help='Number of pages to scrape')

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
        self.same_car = 0
        self.car_brand = kwargs['car_brand']
        self.pages = kwargs['pages']
        self.proxies = None
        self.actual_proxy = None
        self.used_proxies = set()
        self.car_links = self.get_car_links()
        # print(self.car_links)
        self.scrape_cars()

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
            proxies.add(
                f"{proxy.find_all('td')[0].string}:{proxy.find_all('td')[1].string}")
        return proxies

    def check_request(self, soup):
        if 'denied' in soup.find('head').find('title').string.lower():
            return False
        return True

    def get_car_links(self):
        car_links = set()
        counter = 1
        while counter <= self.pages:
            link = f'https://www.otomoto.pl/osobowe/{self.car_brand}/?search_filter_enum_damaged=&page={counter}'
            try:
                soup = BeautifulSoup(
                    requests.get(link, proxies={
                        'http': self.actual_proxy,
                        'https': self.actual_proxy},
                        timeout=4,
                        headers=self.headers
                    ).text,
                    'html.parser'
                )
                self.check_request(soup)
                if not self.check_request(soup):
                    self.used_proxies.add(self.actual_proxy)
                    self.get_actual_proxy()
                    continue
            except:
                self.used_proxies.add(self.actual_proxy)
                self.get_actual_proxy()
            else:
                for car_link in soup.find_all(class_='adListingItem'):
                    car_links.add(car_link.find(
                        'a', class_='offer-title__link').get('href'))
                counter += 1

        return car_links

    def get_car_brand(self, car):
        car_brand, _ = CarBrand.objects.get_or_create(
            name=car.get('Marka pojazdu', 'undefined')
        )
        return car_brand

    def get_car_model(self, car):
        car_model, _ = CarModel.objects.get_or_create(
            name=car.get('Model pojazdu', 'undefined')
        )
        return car_model
    
    def get_car_category(self, car):
        car_category, _ = CarCategory.objects.get_or_create(
            name=car.get('Kategoria', 'undefined')
        )
        return car_category
    
    def get_car(self, car):
        car_brand = self.get_car_brand(car)
        car_model = self.get_car_model(car)
        car_category = self.get_car_category(car)
        car, _ = Car.objects.get_or_create(
            brand=car_brand,
            model=car_model,
            category=car_category
        )
        return car

    def get_color(self, car):
        color, _ = Color.objects.get_or_create(
            name=car.get('Kolor', 'undefined')
        )
        return color

    def format_data(self, car):
        # format car's data such like
        # year, price, mileage, horsepower, state
        car['Przebieg'] = self.get_number(car['Przebieg'])
        car['Moc'] = self.get_number(car['Moc'])
        return car


    def add_car_to_db(self, car):
        car = self.format_data(car)
        print(' ')
        print(car)
        print(' ')
        # car = self.get_car(car)
        # color = self.get_color(car)
        # otomoto_id = car.get('id')
        # if not otomoto_id:
        #     print('Nie udalo sie dodac auta: ', car)
        #     return False
        # _, added = CarOffer.objects.get_or_create(
        #     otomoto_id=otomoto_id,
        #     defaults={
        #         'car': car,
        #         'link': car.get('link'),
        #         'photo': car.get('img'),
        #         'year': car.get('Rok produkcji')
        #     }

        # )

    def get_number(self, number):
        number = ' '.join(number.split()).replace(' ', '', 1)
        return number[:number.find(' ')]

    def scrape_car(self, link):
        try:
            soup = BeautifulSoup(
                requests.get(link, proxies={
                    'http': self.actual_proxy,
                    'https': self.actual_proxy},
                    timeout=4,
                    headers=self.headers
                ).text,
                'html.parser'
            )
            car = {}
            #print(soup.find('div', class_='offer-content__metabar').find_all(class_='offer-meta__item')[1].find('offer-meta__value'))
            car['link'] = link
            car['id'] = soup.find('div', class_='offer-content__metabar').find_all(
                class_='offer-meta__item')[1].find(class_='offer-meta__value').string
            car['img'] = soup.find('img', class_='bigImage').get('data-lazy')
            price = soup.find('span', class_='offer-price__number').get_text() #.strip().replace(' ', '')
            car['price'] = self.get_number(price)
            for row in soup.find('div', class_='offer-params').find_all(class_='offer-params__item'):
                label = row.find(class_='offer-params__label').string
                try:
                    value = row.find(
                        class_='offer-params__value').get_text().replace('\n', '').strip()
                except:
                    value = None
                car[label] = value
            self.add_car_to_db(car)
            return True
        except AttributeError as e:
            print('wrong info about car')
            print(e)
            return True
        
        except KeyError as e:
            print('key wrong car')
            print(e)
            return True

        except Exception as e:
            print('some exception maybe new proxy required')
            print(car)
            print(type(e))
            self.same_car += 1
            if self.same_car == 3:
                self.same_car = 0
                print('smth wrong with this car, we will skip this one')
                return True
            self.used_proxies.add(self.actual_proxy)
            self.get_actual_proxy()
            return False

    def scrape_cars(self):
        links = list(self.car_links)
        current_link = links.pop()
        while links:
            print(len(links))
            if self.scrape_car(current_link):
                current_link = links.pop()
                
            

