# coding: utf-8

from lettuce import *

from crawler import Crawler


@step('I search for "(.*)"')
def search_for(step, param):
    world.search_param = str(param)


@step('I check first product')
def run_crawler(step):
    crawler = Crawler()
    crawler.run(world.search_param)
    world.result = crawler.products[0]['name']

@step('I run the crawler')
def run_crawler(step):
    world.result = Crawler().run(world.search_param)


@step('I see the result "(.*)"')
def check_result(step, expected):
    expected = unicode(expected)
    assert world.result == expected, \
        "Got %s" % world.result
