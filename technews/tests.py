# -*- coding: utf-8 -*-
import technews_parser
import requests
import pickle
import os.path
import unittest
from mock import patch
import time

the_path_of_this_file = os.path.dirname(os.path.abspath(__file__))

#-------------------test parser_page-------------
#           info for testing parser_page
#------------------------------------------------

def get_fake_request_parser_page(url):
    targetfile_read = open(the_path_of_this_file + '/pickle/parser_page/fake_request_pickle', 'r')
    parser_page_target= pickle.load(targetfile_read)
    fake_resp = parser_page_target[url]
    return fake_resp

def get_fake_data_parser_page(url):
    targetfile_read = open(the_path_of_this_file + '/pickle/parser_page/fake_data_pickle', 'r')
    responses = pickle.load(targetfile_read)
    target = responses[url]
    return target

def get_test_urls_parser_page(number):
    targetfile_read = open(the_path_of_this_file + '/pickle/parser_page/test_urls_pickle', 'r')
    urls_list = pickle.load(targetfile_read)
    print('\nthere are ' + str(len(urls_list)) + ' urls for testing parser_page')
    print('maximum index for test is ' + str(len(urls_list)-1))
    print('you are testing url[' + str(number) + '] in urls for testing parser_page')
    time.sleep(2)

    try:
        print('testing ' + urls_list[number])
        time.sleep(2)
        print('------------------------------------------------')
        return urls_list[number]
    except IndexError:
        print("url index out of range, it doesn't exist, automatically use default url[0] now")
        print('testing ' + urls_list[0])
        time.sleep(2)
        print('------------------------------------------------')
        return urls_list[0]


#-------------------test get_category_urls-------------
#          info for testing get_category_urls
#------------------------------------------------------
def get_fake_request_get_categry_urls(url):
    targetfile_read = open(the_path_of_this_file + '/pickle/get_category_urls/fake_request_pickle', 'r')
    responses = pickle.load(targetfile_read)
    fake_resp = responses[url]
    return fake_resp

def get_fake_data_get_category_urls(url):
    targetfile_read = open(the_path_of_this_file + '/pickle/get_category_urls/fake_data_pickle', 'r')
    responses= pickle.load(targetfile_read)
    target = responses[url]
    return target

def get_test_urls_get_category_urls(number):
    targetfile_read = open(the_path_of_this_file + '/pickle/get_category_urls/test_urls_pickle', 'r')
    urls_list = pickle.load(targetfile_read)
    print('\nthere are ' + str(len(urls_list)) + ' urls for testing get_category_urls')
    print('maximum index for test is ' + str(len(urls_list)-1))
    print('you are testing url[' + str(number) + '] in urls for testing parser_page')
    time.sleep(2)

    try:
        print('testing ' + urls_list[number])
        time.sleep(2)
        print('------------------------------------------------')
        return urls_list[number]
    except IndexError:
        print("url index out of range, it doesn't exist, automatically use default url[0] now")
        print('testing ' + urls_list[0])
        time.sleep(2)
        print('------------------------------------------------')
        return urls_list[0]


#--------------------tests-------------------------
#                 Main tests
#--------------------------------------------------
class TestTechnews(unittest.TestCase):
    def test_parser_page(self):
        with patch.object(requests, 'get', side_effect=get_fake_request_parser_page) as requests.get:
            url = get_test_urls_parser_page(1)
            result = technews_parser.parser_page(url)
            target = get_fake_data_parser_page(url)
            self.assertEqual(result, target)

    def test_get_category_urls(self):
        with patch.object(requests, 'get', side_effect=get_fake_request_get_categry_urls) as requests.get:
            url = get_test_urls_get_category_urls(1)
            result = technews_parser.get_category_urls(url)
            target = get_fake_data_get_category_urls(url)
            self.assertEqual(result, target)


if __name__ == '__main__':
    unittest.main()
