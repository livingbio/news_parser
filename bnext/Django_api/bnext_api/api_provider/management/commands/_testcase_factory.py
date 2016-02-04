"""
testcase_factory.py
============================================
generating testcase for tests.py

link to bnext: http://www.bnext.com.tw/
============================================
"""

# -*- coding: utf-8 -*-

import _bnext_parser as bnext_parser
import requests
import pickle as pkl
import os.path
import time
import sys

from bs4 import BeautifulSoup
from requests import ConnectionError
from datetime import datetime
from random import randint

_RETRY_LIMIT = 3
_pseudo_request_response_dict = {}

category_url_list = [
    'http://www.bnext.com.tw/categories/internet/',
    'http://www.bnext.com.tw/categories/tech/',
    'http://www.bnext.com.tw/categories/marketing/',
    'http://www.bnext.com.tw/categories/startup/',
    'http://www.bnext.com.tw/categories/people/',
    'http://www.bnext.com.tw/categories/skill/']


# Uncomment to generate small testcase
# category_url_list = ['http://www.bnext.com.tw/categories/internet/']


def try_response(url, _RETRY_LIMIT=3):
    retry = 0
    while retry < _RETRY_LIMIT:
        try:
            res = requests.get(url)
            break
        except ConnectionError:
            retry += 1
            print('({}/{}) retrying...'.format(retry, _RETRY_LIMIT))
            time.sleep(randint(10, 15))
    assert (retry < _RETRY_LIMIT), "maximum retry limit reached"
    return res


# these are for generating testcases,
# you should never call this unless you are tsaiJN :)
# ==================================================================
"""
 implementation:
  go through urls provided by generate_get_category_urls_testcase()
"""


def generate_parser_page_testcase(ground_input):
    generating_time = datetime.now()
    ground_truth = []
    global _pseudo_request_response_dict

    for i, url in enumerate(ground_input):

        # ========================================================================================
        # First, getting testcase ground truth
        # ========================================================================================
        print('({}/{}) {}'.format(i + 1, len(ground_input), url))
        retry = 0
        while retry < _RETRY_LIMIT:
            try:
                ret = bnext_parser.parser_page(url)
                ground_truth.append(ret)
                break
            except ConnectionError:
                retry += 1
                print('({}/{}) retrying...'.format(retry, _RETRY_LIMIT))
                time.sleep(randint(10, 15))
        assert (retry < _RETRY_LIMIT), "maximum retry limit reached"
        _pseudo_request_response_dict[url] = try_response(url)
# ========================================================================================
# Next, getting needed responses for "mocking requests.get()""
# ========================================================================================

        utility_string1 = 'https://graph.facebook.com/fql?q=SELECT%20like_count,%20total_count,%20share_count,%20click_count,%20commentsbox_count%20FROM%20link_stat%20WHERE%20url%20=%20%22{}%22'

        # + '&limit=3' # limit is just for testing
        utility_string2 = 'https://graph.facebook.com/comments?id={}&filter=stream&fields=parent.fields(id),message,from,created_time,like_count{}'
        res = try_response(url)
        _pseudo_request_response_dict['url'] = res
        res_fb1 = try_response(utility_string1.format(url))
        _pseudo_request_response_dict[utility_string1.format(url)] = res_fb1

        suffix = ''
        while True:
            res_fb2 = try_response(utility_string2.format(url, suffix))
            _pseudo_request_response_dict[
                utility_string2.format(url, suffix)] = res_fb2
            data = res_fb2.json()['data']
            if len(data) == 0:
                break
            paging = res_fb2.json()['paging']
            if 'next' not in paging.keys():
                break
            else:
                suffix = paging['next']
                suffix = suffix[suffix.find('&after='):]
# ========================================================================================
# Dumping testcases to file
# ========================================================================================

    with open('./_resources/testcase/parser_page_testcase.pkl', 'w') as f:
        obj = {'ground_input': ground_input, 'ground_truth': ground_truth,
               'generating_time': generating_time}

        pkl.dump(obj, f)


"""
 implementation:
  dense test last 3 page of each category, 40 url each
  most of the old news don't have keyword
"""


def generate_get_category_testcase(ground_input):
    global _pseudo_request_response_dict

    generating_time = datetime.now()
    ground_truth = []

    for url in ground_input:
        ret = bnext_parser.get_category_urls(url, back_counting_offset=3)
        ground_truth.append(ret[-40:])

# ========================================================================================
# Getting needed responses for "mocking requests.get()""
# ========================================================================================
        res = requests.get(url)
        _pseudo_request_response_dict[url] = res
        prefix = 'http://www.bnext.com.tw'
        soup = BeautifulSoup(res.content)
        page_list = soup.find('ul', 'pagination')
        last_page = page_list.findAll('a')[-1]['href']
        midfix = '?p='
        last_page = int(last_page.split('=')[-1]) + 1
        starting_page = last_page - 3

        for page in range(starting_page, last_page):
            res = try_response(url + midfix + str(page))
            _pseudo_request_response_dict[url + midfix + str(page)] = res

# ========================================================================================
# Dumping testcases to file
# ========================================================================================

    obj = {'ground_input': ground_input, 'ground_truth': ground_truth,
           'generating_time': generating_time}

    with open(
      './_resources/testcase/get_category_urls_testcase.pkl',
      'w') as f:

        pkl.dump(obj, f)

    return ground_truth


def generate_testcase_ensemble():
    global category_url_list
    global _pseudo_request_response_dict

    # load category_urls ground truth if already have it
    if os.path.isfile(
      './_resources/testcase/get_category_urls_testcase.pkl') and False:
        url_list = pkl.load(
            open(
                './_resources/testcase/get_category_urls_testcase.pkl'
            )
        )['ground_truth']
    else:
        url_list = generate_get_category_testcase(category_url_list)

    # flatten url_list
    url_list = [
        url_list_3 for url_list_2 in url_list for url_list_3 in url_list_2]

    generate_parser_page_testcase(url_list)

# ========================================================================================
# Dumping mocking meta
# ========================================================================================
    pkl.dump(_pseudo_request_response_dict, open(
        './_resources/_pseudo_request_response_dict.pkl', 'w'))

# ================================== end of generating testcase ==========


if __name__ == '__main__':
    generate_testcase_ensemble()
