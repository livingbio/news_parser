# -*- coding: utf-8 -*-
import technews_parser
import json
import requests
import pickle
# from bs4 import BeautifulSoup


def test_parser_page(url):
    result = technews_parser.parser_page(url)
    # assert result == target, 'target error {} != {}'.format(result, target)

    # temp = open('parser_page.html', 'r')
    # soup = temp.read()
    # print(soup)

    targetfile_read = open('pickle/parser_page/parser_page_pickle', 'r')
    parser_page_target= pickle.load(targetfile_read)

    # print(parser_page_target['keyword'][3])
    # print(result['keyword'][3])

    # fr = open('parser_page.json', 'r')
    # parser_page_json = json.load(fr)
    # result['journalist'] = 'Spiderman'

    for i in parser_page_target:
        assert result[i] == parser_page_target[i], i + ' field has error: {} != {}'.format(result[i], parser_page_target[i])

    print(result['journalist'])
    print(parser_page_target['journalist'])
    print('done test_parser_page')

# test_parser_page_result = test_parser_page('http://technews.tw/2015/11/26/apple-iphone-2018-oled-﻿panel/')



def test_get_category_urls(url):
    result = technews_parser.get_category_urls(url)

    targetfile_read = open('pickle/get_category_urls/get_category_urls_pickle', 'r')
    target= pickle.load(targetfile_read)

    # result[3] = 'MISTAKE'
    for i in range(len(result)):
        assert result[i] == target[i], 'get_category_urls function has error at the result and target\'s list[' + str(i) + '] : {} != {}'.format(result[i], target[i])

    print(target[3])
    print(result[3])
    print('done get_category_urls test')

# test_get_category_urls_result = test_get_category_urls('http://technews.tw/category/tablet/')
