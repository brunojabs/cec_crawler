# coding: utf-8

from lettuce import *

from crawler import Crawler


@step('I search for "(.*)"')
def search_for(step, param):
    world.search_param = str(param)


@step('I run the crawler')
def run_crawler(step):
    world.result = Crawler().run(world.search_param)


@step('I see the result "(.*)"')
def check_result(step, expected):
    expected = str(expected)
    assert world.result == expected, \
        "Got %s" % world.result
