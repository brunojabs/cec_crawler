# coding: utf-8

"""
    Crawler para buscas no site CEC.
    Deve receber uma url e retornar o nome do item, valor e url da imagem.

    Uso:
        python crawler.py tijolo
"""
import re
import sys

import requests
from bs4 import BeautifulSoup


clean_str = lambda text: re.sub('\s+', '', text)


class Crawler(object):
    URL = 'http://www.cec.com.br/busca-produto?text=%s'

    def get(self, param):
        try:
            response = requests.get(self.URL % param)
        except Exception as e:
            raise e(u'Não foi possível realizar a consulta')

        return BeautifulSoup(response.content)

    def run(self, param):
        html = self.get(param)
        self.find_products(html)

    def find_products(self, html):
        products_divs = html.findAll('div', attrs={'class': 'hproduct'})

        if products_divs:
            for product_div in products_divs:
                self.save_product(product_div)

    def save_product(self, product_div):
        img = product_div.find('img')
        preco = product_div.find('strong', attrs={'class': 'price'})
        descricao = product_div.find('h3')

        print u'Nome: {descricao}, Valor: {preco}, Img: {img} \n'.format(
            img=img.attrs['src'],
            preco=preco.text,
            descricao=clean_str(descricao.text)
        )


if __name__ == '__main__':

    try:
        param = sys.argv[1]
    except:
        pass
    else:
        crawler = Crawler()
        crawler.run(param=param)