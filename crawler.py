# coding: utf-8

"""
    CEC - Crawler
    ~~~~~

    Mini crawler para extrair informações da página de busca do site CEC.

    Uso:
        python crawler.py <parametro de busca>

    Exemplo:
        python crawler.py tijolo

    :copyright: (c) 2014 by Lucas Magnum.
"""

import logging
import os
import re
import sqlite3

import requests
from bs4 import BeautifulSoup


FMT = '[%(levelname)s] - %(message)s'

handler = logging.StreamHandler()
handler.setFormatter(logging.Formatter(FMT))

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)
logger.addHandler(handler)

# remover \t do texto
clean_str = lambda text: u''.join(text.splitlines()).strip()


class Crawler(object):
    DOMAIN = 'http://www.cec.com.br'
    SEARCH_URL = '/busca-produto?text=%s'

    def __init__(self, filename='dados.db'):
        self.url = None
        self.db = CrawlerDB(filename=filename)

        self.products = []
        self._cached_pages = {}
        self.links = []

    def get(self, path_url):
        url = '%s%s' % (self.DOMAIN, path_url)

        content = self._cached_pages.get(url, None)

        if content is None:
            try:
                response = requests.get(url)
            except Exception:
                raise Exception(u'Não foi possível realizar a consulta')

            self._cached_pages[url] = BeautifulSoup(response.content)

        self.url = url
        logger.debug('Url visitada %s' % self.url)

        return self._cached_pages[url]

    def run(self, search_param):
        main_page = self.get(self.SEARCH_URL % search_param)
        self.find_products(html=main_page)
        return u'%s products found' % len(self.products)

    def find_products(self, html):
        products_divs = html.findAll('div', attrs={'class': 'hproduct'})

        if products_divs:
            logger.debug('%d produtos encontrados \n' % len(products_divs))

            for product_div in products_divs:
                self.save_product(product_div)

            next_page = self.next_page(html)
            if next_page:
                self.find_products(next_page)

        else:
            logger.debug('Nenhum produto encontrado')

    def next_page(self, page):
        nav = page.find('nav', attrs={'class': 'paginador'})
        if nav:
            next_page = nav.find('a', text=u'Próxima')
            if next_page:
                return self.get(next_page.attrs['href'])
        return
    def save_product(self, product_div):
        if product_div.findChildren():
            img = product_div.find('img')
            price = product_div.find('strong', attrs={'class': 'price'})
            brand = product_div.find('span', attrs={'class': 'brand'})
            name = brand.previous_element.extract()

            price_txt = '.'.join(re.findall('\d+', price.text))

            product_dict = {
                'name': clean_str(name),
                'price': price_txt,
                'brand': clean_str(brand.text),
                'img_url': img.attrs['src'],
                'url': self.url
            }

            self.products.append(product_dict)

            self.db.insert(**product_dict)


class CrawlerDB(object):
    TABLE = """
        CREATE TABLE IF NOT EXISTS products (
            name TEXT,
            price REAL,
            brand TEXT,
            img_url TEXT,
            url TEXT
        );
    """

    def __init__(self, filename):
        self.filename = os.path.join(os.path.dirname(__file__), filename)
        self.connection = sqlite3.connect(
            self.filename
        )
        self.connection.text_factory = str
        self.cursor = self.connection.cursor()
        self.execute(self.TABLE)

    def execute(self, sql, commit=True):
        self.connection.execute(sql)
        if commit:
            self.connection.commit()

    def insert(self, **kwargs):
        self.execute(
            u"""
                INSERT INTO products VALUES
                ('{name}', '{price}', '{brand}', '{img_url}', '{url}')
            """.format(**kwargs)
        )


if __name__ == '__main__':
    import argparse

    parser = argparse.ArgumentParser(
        usage=u"%(prog)s <parametro de busca>",
        description= u"Mini crawler para extrair informações da página \
            de busca do site CEC"
    )
    parser.add_argument(
        "search_param",
        action="store",
        type=str,
        help=u"Parâmetro que será utilizado para busca no site CEC")

    parser.add_argument(
        "--filename",
        action="store",
        type=str,
        dest="filename",
        default="products.db",
        help=u"Nome do arquivo onde os dados serão salvos."
    )

    params = parser.parse_args()

    crawler = Crawler(params.filename)
    crawler.run(search_param=params.search_param)
