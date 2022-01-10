import datetime
import urllib.parse
from logging import getLogger

from collections import namedtuple

import bs4
import requests

from django.core.management.base import BaseCommand
from django.core.management.base import CommandError


from aparser.models import Product


logger = getLogger(__name__)


class AvitoParser:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'Accept-Language': 'ru',
        }

    def get_page(self, params=None):

        url = 'https://www.avito.ru/vologda/kvartiry/prodam-ASgBAgICAUSSA8YQ'
        r = self.session.get(url, params=params)
        return r.text

    @staticmethod
    def parse_date(item: str):
        params = item.strip().split(' ')

        if len(params) == 3:
            day, month_hru, time = params
            day = int(day)
            months_map = {
                'января': 1,
                'февраля': 2,
                'марта': 3,
                'апреля': 4,
                'мая': 5,
                'июня': 6,
                'июля': 7,
                'августа': 8,
                'сентября': 9,
                'октября': 10,
                'ноября': 11,
                'декабря': 12,
            }
            month = months_map.get(month_hru)
            if not month:
                logger.error('Не смогли разобрать месяц:', item)
                return

            today = datetime.datetime.today()
            time = datetime.datetime.strptime(time, '%H:%M')
            return datetime.datetime(day=day, month=month, year=today.year, hour=time.hour, minute=time.minute)

        else:
            logger.error('Не смогли разобрать формат:', item)
            return

    def parse_block(self, item):
        # Выбрать блок со ссылкой
        url_block = item.select_one('a.snippet-link')
        href = url_block.get('href')
        if href:
            url = 'https://www.avito.ru' + href
        else:
            url = None

        # Выбрать блок с названием
        title_block = item.select_one('a.snippet-link')
        title = title_block.get('title')

        price_block = item.select_one('div.snippet-price-row span')
        price_blocks = price_block.string.strip()
        txt = price_blocks
        price = txt.strip("₽' ")
        price = int(price.replace(' ', ''))

        address_block = item.select_one('span.item-address__string')
        address = address_block.string.strip()

        published_date = None
        date_block = item.select_one('div.snippet-date-info')
        absolute_date = date_block.get('data-tooltip')
        if absolute_date:
            published_date = self.parse_date(item=absolute_date)


        try:
            pr = Product.objects.get(url=url)
            pr.title=title
            pr.price=price
            pr.address=address
            pr.save()
        except Product.DoesNotExist:
            pr = Product(
                url=url,
                title=title,
                price=price,
                address=address,
                published_date=published_date,
            ).save()

        logger.debug(f'product {pr}')

    def get_blocks(self):
        text = self.get_page()
        soup = bs4.BeautifulSoup(text, 'lxml')
        page_count = soup.select('span.pagination-item-1WyVp')
        page_count = int(page_count[-2].get_text())

        for p in range(1, page_count):
            print(f'Парсинг страницы {p} из {page_count}...')
            text = self.get_page(params={'p': p})
            soup = bs4.BeautifulSoup(text, 'lxml')
            container = soup.select('div.item.item_table.clearfix.js-catalog-item-enum.item-with-contact.js-item-extended')
            for item in container:
                self.parse_block(item=item)


class Command(BaseCommand):
    help = 'Парсинг Avito'

    def handle(self, *args, **options):
        p = AvitoParser()
        p.get_blocks()



