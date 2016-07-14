# -*- coding: utf-8 -*-
import os.path
import unittest
import requests
from requests import Response
from mock import patch
from datetime import datetime
import cts_parser
import json

path = os.path.dirname(os.path.abspath(__file__))

############################################# Fake Request #################################################
targetfile = open(path + '/fake_pages', 'r')
content = targetfile.read()
targetfile.close()
global fake_pages_dict
fake_pages_dict = json.loads(content)

def get_fake_request(url):
    global fake_pages_dict
    hashkey = hash(url)
    if str(hashkey) in fake_pages_dict.keys():
        fake_page = Response()
        fake_page_content = fake_pages_dict[str(hashkey)].encode('utf-8')
        fake_page._content = fake_page_content
        if "facebook" in url:
            fake_page.encoding = 'utf-8'
        else:
            fake_page.encoding = 'iso8859-1'
        return fake_page
    else:
        print "The url is not supported."


########################################## Get the target dict ##########################################
targetfile = open(path + '/target', 'r')
content = targetfile.read()
targetfile.close()
global target_dict
target_dict = json.loads(content)


########################################## Testing parser_page ##########################################
def data_for_parser_page(url):  #need revision   
    global target_dict
    hashkey = hash(url)
    if str(hashkey) in target_dict.keys():
        target = target_dict[str(hashkey)]
        #process post-time
        target["post_time"] = datetime.strptime(target["post_time"], '%Y-%m-%dT%H:%M:%S')
        length = len(target["comment"])
        for i in range(length):
            target["comment"][i]["post_time"] = datetime.strptime(target["comment"][i]["post_time"], '%Y-%m-%dT%H:%M:%S')
            length2 = len(target["comment"][i]["sub_comments"])
            for j in range(length2):
                target["comment"][i]["sub_comments"][j]["post_time"] = datetime.strptime(target["comment"][i]["sub_comments"][j]["post_time"], '%Y-%m-%dT%H:%M:%S')
        return target
    else:
        print "Cannot find the target."


######################################## Testing get_category_urls #######################################
def data_for_category_urls(url):
    global target_dict
    hashkey = hash(url)
    if str(hashkey) in target_dict.keys():
        target = target_dict[str(hashkey)]
        return target
    else:
        print "Cannot find the target."


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
        with patch.object(requests, 'get', side_effect = get_fake_request) as requests.get:
            #get the test_urls for testing parser_page
            test_urls_dic = {}
            with open(path + '/test_urls/parser_page') as f:
                for line in f:
                   (key, value) = line.split()
                   test_urls_dic[key] = value
            #test each url
            for i in range(1, len(test_urls_dic)):
                test_url = test_urls_dic[str(i)]
                print('You are testing url ' + str(i) + ' in test_urls for testing parser_page')
                result = cts_parser.parser_page(test_url)
                target = data_for_parser_page(test_url)

                if compare_dict(result, target) == True:
                    print "Test Result: Succeed"
                else:
                    print "Test Result: Fail"
            
    def test_get_category_urls(self):
        with patch.object(requests, 'get', side_effect = get_fake_request) as requests.get:
            #get the test_urls for testing get_category_urls
            test_urls_dic = {}
            with open(path + '/test_urls/get_category_urls') as f:
                for line in f:
                   (key, value) = line.split()
                   test_urls_dic[key] = value
            #test each url
            for i in range(1, len(test_urls_dic)):
                test_url = test_urls_dic[str(i)]
                print('You are testing url ' + str(i) + ' in test_urls for testing get_category_urls')
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


if __name__ == '__main__':
    unittest.main()