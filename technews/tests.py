# -*- coding: utf-8 -*-
import technews_parser
import json
import requests
import pickle
import os.path
from requests.models import Response

the_path_of_this_file = os.path.dirname(os.path.abspath(__file__))
# print(__file__)
# print('**************' + the_path_of_this_file)

# assert result == target, 'target error {} != {}'.format(result, target)

def test_parser_page():
    # url = 'http://technews.tw/2015/11/26/apple-iphone-2018-oled-﻿panel/'
    url = 'http://technews.tw/2016/01/06/iphone-6s-no-good-apple/'
    _ = requests.get
    def fake_request_get(url):
        targetfile_read = open(the_path_of_this_file + '/pickle/parser_page/fake_request_pickle', 'r')
        parser_page_target= pickle.load(targetfile_read)
        fake_resp = parser_page_target[url]
        return fake_resp

    requests.get = fake_request_get
    result = technews_parser.parser_page(url)
    requests.get = _

    targetfile_read = open(the_path_of_this_file + '/pickle/parser_page/fake_data_pickle', 'r')
    responses = pickle.load(targetfile_read)
    target = responses[url]

    for i in target:
        assert result[i] == target[i], i + ' field has error: {} != {}'.format(result[i], target[i])
    print(result['journalist'])
    print(target['journalist'])
    print('done test_parser_page')


def test_get_category_urls():
    # url = 'http://technews.tw/category/tablet/page/38/'
    url = 'http://technews.tw/category/tablet/page/37/'
    _ = requests.get
    def fake_request_get(url):
        targetfile_read = open(the_path_of_this_file + '/pickle/get_category_urls/fake_request_pickle', 'r')
        responses = pickle.load(targetfile_read)
        fake_resp = responses[url]
        return fake_resp

    requests.get = fake_request_get
    result = technews_parser.get_category_urls(url)
    requests.get = _

    targetfile_read = open(the_path_of_this_file + '/pickle/get_category_urls/fake_data_pickle', 'r')
    fake_data= pickle.load(targetfile_read)
    target = fake_data[url]

    for i in range(len(result)):
        assert result[i] == target[i], 'get_category_urls function has error at the result and target\'s list[' + str(i) + '] : {} != {}'.format(result[i], target[i])
    print(result[2])
    print(target[2])
    print('done test_get_category_urls')


if __name__ == '__main__':
    test_parser_page()
    test_get_category_urls()
