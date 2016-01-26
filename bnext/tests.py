"""
test.py
============================================
testing the correctness of:
    * bnext_parser.parser_page(url)
    * bnext_parser.get_category_urls(url)

link to bnext: http://www.bnext.com.tw/
============================================
"""


# -*- coding: utf-8 -*-

import bnext_parser
import requests
import pickle as pkl
import os.path
import unittest
import time
import sys

from mock import patch
from bs4 import BeautifulSoup
from requests import ConnectionError
from datetime import datetime
from random import randint


_RETRY_LIMIT = 3
_response_pool = None


category_url_list = ['http://www.bnext.com.tw/categories/internet/',
                     'http://www.bnext.com.tw/categories/tech/',
                     'http://www.bnext.com.tw/categories/marketing/',
                     'http://www.bnext.com.tw/categories/startup/',
                     'http://www.bnext.com.tw/categories/people/',
                     'http://www.bnext.com.tw/categories/skill/']


def print_time(obj):
    print('test_case generating time: ')
    print(obj['generating_time'])
    print('\n')
    return


def pseudo_get(url):
    global _response_pool

    # load responses if haven't load
    if _response_pool is None:
        _response_pool = pkl.load(
            open('./bnext/resources/_pseudo_request_response_dict.pkl'))

    return _response_pool[url]


def _test_parser_page(test_file):

    print("\n======================= parser page ==========================\n")
    print("".join([
        "Testing parser_page(), don't warry if you see some log on the fly,\n",
        "they are for the porpose of analyzing webpage, the fail of testing\n",
        "would be shown by [assert]\n"
        ])
    )

    if os.path.isfile(test_file) is False:
        print("".join([
            "Error: can't find test_file: {}, please check filename or",
            "generate new test_file\n"
            ]).format(test_file)
        )

        return False

    f = open(test_file)
    obj = pkl.load(f)
    print_time(obj)

    ground_input = obj['ground_input']
    ground_truth = obj['ground_truth']

    for i, url in enumerate(ground_input):
        print('({}/{}) {}'.format(i + 1, len(ground_input), url))

        retry = 0
        while retry < _RETRY_LIMIT:
            try:
                ret = bnext_parser.parser_page(url)
                break
            except ConnectionError:
                retry += 1
                print('({}/{}) retrying...'.format(retry, _RETRY_LIMIT))
                time.sleep(randint(10, 15))

        if ret != ground_truth[i]:
            print('test failed: {}\n'.format(url))
            return

        if ret != ground_truth[i]:
            print('test failed: {}\n'.format(url))
            return False
        # time.sleep(randint(1, 3))

    print('\nSuccess')
    return True


def _test_get_category_urls(test_file):

    print("\n====================== category urls =========================\n")
    print("".join([
        "Testing get_category_urls(), don't warry if you see some log on \n",
        "the fly, they are for the porpose of analyzing webpage, the fail \n",
        "of testing would be shown by [assert]\n"
        ])
    )

    if os.path.isfile(test_file) is False:
        print("".join([
            "Error: can't find test_file: {}, please check filename or",
            " generate new test_file\n"
            ]).format(test_file)
        )
        return False

    f = open(test_file)
    obj = pkl.load(f)
    print_time(obj)

    ground_input = obj['ground_input']
    ground_truth = obj['ground_truth']

    for i, url in enumerate(ground_input):
        retry = 0
        while retry < _RETRY_LIMIT:
            try:
                ret = bnext_parser.get_category_urls(url,
                                                     back_counting_offset=3)
                ret = ret[-40:]
                if ret != ground_truth[i]:
                    print('test failed: {}\n'.format(url))
                    return False
                break
            except ConnectionError:
                retry += 1
                print('({}/{}) retrying...'.format(retry, _RETRY_LIMIT))
                time.sleep(randint(10, 15))

        sys.stdout.write('.')
        # time.sleep(1)

    return True
    print('\nSuccess')


# ===============================================================================================
# Unit test framework
# ===============================================================================================
class TestEnsemble(unittest.TestCase):

    def test_get_category_urls(self):
        with patch.object(requests, 'get',
                          side_effect=pseudo_get) as requests.get:
            ret = _test_parser_page(
                './bnext/resources/testcase/parser_page_testcase.pkl')
            self.assertTrue(ret)

    def test_parser_page(self):
        with patch.object(requests,
                          'get',
                          side_effect=pseudo_get) as requests.get:
            ret = _test_get_category_urls(
                './bnext/resources/testcase/get_category_urls_testcase.pkl')

            self.assertTrue(ret)


if __name__ == '__main__':
    unittest.main()
    print("Done testing.\n")
