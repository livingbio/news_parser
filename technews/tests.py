# -*- coding: utf-8 -*-
import technews_parser
import requests
import pickle
import os.path
from requests.models import Response
import unittest
from mock import patch

the_path_of_this_file = os.path.dirname(os.path.abspath(__file__))

def fake_request_get_parser_page(url):
    targetfile_read = open(the_path_of_this_file + '/pickle/parser_page/fake_request_pickle', 'r')
    parser_page_target= pickle.load(targetfile_read)
    fake_resp = parser_page_target[url]
    return fake_resp

def fake_request_get_get_categry_urls(url):
    targetfile_read = open(the_path_of_this_file + '/pickle/get_category_urls/fake_request_pickle', 'r')
    responses = pickle.load(targetfile_read)
    fake_resp = responses[url]
    return fake_resp


class TestTechnews(unittest.TestCase):
    def test_parser_page(self):
        with patch.object(requests, 'get', side_effect=fake_request_get_parser_page) as requests.get:
            # url = 'http://technews.tw/2016/01/06/iphone-6s-no-good-apple/'
            url = 'http://technews.tw/2015/11/26/apple-iphone-2018-oled-﻿panel/'
            result = technews_parser.parser_page(url)
            targetfile_read = open(the_path_of_this_file + '/pickle/parser_page/fake_data_pickle', 'r')
            responses = pickle.load(targetfile_read)
            target = responses[url]
            self.assertEqual(result, target)

    def test_get_category_urls(self):
        with patch.object(requests, 'get', side_effect=fake_request_get_get_categry_urls) as requests.get:
            # url = 'http://technews.tw/category/tablet/page/37/'
            url = 'http://technews.tw/category/tablet/page/38/'
            result = technews_parser.get_category_urls(url)
            targetfile_read = open(the_path_of_this_file + '/pickle/get_category_urls/fake_data_pickle', 'r')
            responses= pickle.load(targetfile_read)
            target = responses[url]
            self.assertEqual(result, target)


if __name__ == '__main__':
    unittest.main()
