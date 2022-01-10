import datetime

from collections import namedtuple

import bs4
import requests

InnerBlock = namedtuple('Block', 'title,price,adres,date,url')


class Block(InnerBlock):

    def __str__(self):
        return f'{self.title}\t{self.price} {self.currency}\t{self.adres}\t{self.date}\t{self.url}'


class AvitoParser:

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.169 Safari/537.36',
            'Accept-Language': 'ru',
        }

    def get_page(self, params=None):

        url = 'https://www.avito.ru/vologda/kvartiry/sdam-ASgBAgICAUSSA8gQ?'
        r = self.session.get(url, params=params)
        return r.text

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
        price1 = price_blocks[0:6]
        price2 = price1.strip('₽')
        price = int(price2.replace(' ', ''))

        srok_block = item.select_one('div.snippet-price-row span')
        srok_blocks = srok_block.string.strip()
        srok1 = srok_blocks[10:19]
        srok = srok1.lstrip()


        print(price, srok)
        return

        address_block = item.select_one('span.item-address__string')
        address = address_block.string.strip()

        date_block = item.select_one('div.snippet-date-info')
        date = date_block.get('data-tooltip')

        return Block(
            url=url,
            title=title,
            price=price,
            currency=currency,
            address=address,
            date=date,
        )

    def get_blocks(self):
        text = self.get_page()
        soup = bs4.BeautifulSoup(text, 'lxml')
        page_count = soup.select('span.pagination-item-1WyVp')
        page_count = int(page_count[-2].get_text())

        for p in range(1, 2):
            print(f'Парсинг страницы {p} из {page_count}...')
            text = self.get_page(params={'p': p})
            soup = bs4.BeautifulSoup(text, 'lxml')
            container = soup.select(
                'div.item.item_table.clearfix.js-catalog-item-enum.item-with-contact.js-item-extended')
            for item in container:
                block = self.parse_block(item=item)
                print(block)


def main():
    p = AvitoParser()
    p.get_blocks()


if __name__ == '__main__':
    main()
