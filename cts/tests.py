# -*- coding: utf-8 -*-
import os.path
import unittest
import requests
from requests import Response
from mock import patch
from datetime import datetime
import cts_parser
import test_data_for_parser_page

path = os.path.dirname(os.path.abspath(__file__))

############################################# Fake Request #################################################
global fake_page_dic
fake_page_dic = {}
with open(path + '/fake_page_dic') as f:
    for line in f:
       (key, value) = line.split()
       fake_page_dic[key] = value

def get_fake_request(url):
    global fake_page_dic
    file_index = fake_page_dic[url]
    if file_index != None:
        targetfile = open(path + '/tests/fake_page_' + str(file_index), 'r')
        fake_page_content = targetfile.read()
        targetfile.close()

        fake_page = Response()
        fake_page._content = fake_page_content
        if "facebook" in url:
            fake_page.encoding = 'utf-8'
        else:
            fake_page.encoding = 'iso8859-1'
        return fake_page
    else:
        print "The url is not supported."

def patch_request_get():
    global ori_requests_get
    ori_requests_get = requests.get
    requests.get = get_fake_request

def unpatch_request_get():
    global ori_requests_get
    requests.get = ori_requests_get


########################################## Testing parser_page ##########################################
def data_for_parser_page(url):  #need revision   
    target = test_data_for_parser_page.target[url]
    return target

def urls_for_parser_page(number):
    test_urls_dic = {}
    with open(path + '/tests/parser_page/test_urls') as f:
        for line in f:
           (key, value) = line.split()
           test_urls_dic[key] = value
    return_url = test_urls_dic[str(number)]
    print('You are testing url ' + str(number) + ' in test_urls for testing parser page')
    return return_url


######################################## Testing get_category_urls #######################################
def data_for_category_urls(url):
    targetfile = open(path + '/tests/get_category_urls/test_data', 'r')
    content = targetfile.read()
    targetfile.close()
    
    start_index = content.index(url) + len(url) + 1  #after the category url
    target_content = content[start_index:]
    end_index = target_content.index(';')            #before next category url
    target_content = target_content[:end_index]      #target content that we want
    number = target_content.count(',') + 1

    detail_urls = []
    for i in range(number):
        index = target_content.index('.html') + len('.html')
        detail_urls.append(target_content[0:index])
        target_content = target_content[index+1:]
    return detail_urls

def urls_for_category_urls(number):
    test_urls_dic = {}
    with open(path + '/tests/get_category_urls/test_urls') as f:
        for line in f:
           (key, value) = line.split()
           test_urls_dic[key] = value
    return_url = test_urls_dic[str(number)]
    print('You are testing url ' + str(number) + ' in test_urls for testing get_category_urls')
    return return_url


########################################## Compare two dictionaries #########################################
def compare_dict(dict1, dict2):
    if dict1 == None or dict2 == None:
        return False
    if type(dict1) is not dict or type(dict2) is not dict:
        return False
    if not (len(dict1.keys()) == len(dict2.keys())):
        return False
    dicts_equal = True
    for key in dict1.keys():
        if dict1[key] != dict2[key]:
            print "the first different key: ", key
            dicts_equal = False
            break
    return dicts_equal


################################################### Tests ####################################################
class TestCtsnews(unittest.TestCase):
    
    def test_get_parser_page(self):
        patch_request_get()
        for i in range(3):
            test_url = urls_for_parser_page(i + 1)
            result = cts_parser.parser_page(test_url)
            #print result['comment']
            target = data_for_parser_page(test_url)

            if compare_dict(result, target) == True:
                print "Test Result: Succeed"
            else:
                print "Test Result: Fail"
        unpatch_request_get()
    
    def test_get_category_urls(self):
        patch_request_get()
        for i in range(3):
            test_url = urls_for_category_urls(i + 1)
            result = cts_parser.get_category_urls(test_url)
            target = data_for_category_urls(test_url)
            
            equal = True
            for i in range(len(result)):
                if result[i] != target[i]:
                    equal = False
                    print "Test Result: Fail"
                    break
            else:
                print "Test Result: Succeed"
        unpatch_request_get()
    

if __name__ == '__main__':
    unittest.main()