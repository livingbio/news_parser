# -*- coding: utf-8 -*-
from datetime import datetime
import cts_parser
import requests
import os.path
import unittest
from mock import patch
from requests import Response
import test_data_for_parser_page

path = os.path.dirname(os.path.abspath(__file__))


##################################### Testing parser_page #####################################
#urls for testing parser_page
test_urls = {
    "http://news.cts.com.tw/cts/general/201605/201605281756574.html#.V4EdH7h942w": 1,
    "http://news.cts.com.tw/cts/society/201606/201606071760311.html#.V4Rbxbh942w": 2,
    "http://news.cts.com.tw/nownews/money/201607/201607061770895.html#.V4Rca7h942x": 3,
}

def get_fake_request_parser_page(url):
    fb_like_url = 'https://api.facebook.com/method/links.getStats?urls='
    fb_comments_url = 'http://graph.facebook.com/comments?filter=stream&fields=from,like_count,message,created_time,id,parent.fields(id)&id='
    if fb_comments_url in url:  #fake_comments_n-n
        if 'general' in url:
            targetfile = open(path + '/tests/parser_page/fake_comments_1-1', 'r')
            fake_comments_content = targetfile.read()
            targetfile.close()

            fake_comments = Response()
            fake_comments._content = fake_comments_content
            fake_comments.encoding = 'utf-8'
            return fake_comments
        elif 'money' in url:
            targetfile = open(path + '/tests/parser_page/fake_comments_3-1', 'r')
            fake_comments_content = targetfile.read()
            targetfile.close()

            fake_comments = Response()
            fake_comments._content = fake_comments_content
            fake_comments.encoding = 'utf-8'
            return fake_comments
        else:
            if '&after' in url:
                targetfile = open(path + '/tests/parser_page/fake_comments_2-2', 'r')
                fake_comments_content = targetfile.read()
                targetfile.close()

                fake_comments = Response()
                fake_comments._content = fake_comments_content
                fake_comments.encoding = 'utf-8'
                return fake_comments
            else:
                targetfile = open(path + '/tests/parser_page/fake_comments_2-1', 'r')
                fake_comments_content = targetfile.read()
                targetfile.close()

                fake_comments = Response()
                fake_comments._content = fake_comments_content
                fake_comments.encoding = 'utf-8'
                return fake_comments

    elif fb_like_url in url:
        for key in test_urls.keys():
            if key in url:
                targetfile = open(path + '/tests/parser_page/fake_page_fb_' + str(test_urls[key]), 'r') #fake_page_fb_n
                fake_fb_page_content = targetfile.read()
                targetfile.close()

                fake_fb_page = Response()
                fake_fb_page._content = fake_fb_page_content
                fake_fb_page.encoding = 'iso8859-1'
                return fake_fb_page
    else:
        for key in test_urls.keys():
            if key in url:
                targetfile = open(path + '/tests/parser_page/fake_page_' + str(test_urls[key]), 'r') #fake_page_n
                fake_page_content = targetfile.read()
                targetfile.close()

                fake_page = Response()
                fake_page._content = fake_page_content
                fake_page.encoding = 'iso8859-1'
                return fake_page

def patch_request_get_parser_page():
    global ori_requests_get
    ori_requests_get = requests.get
    requests.get = get_fake_request_parser_page

def unpatch_request_get_parser_page():
    global ori_requests_get
    requests.get = ori_requests_get

def data_for_parser_page(url):    
    target = test_data_for_parser_page.target[url]
    return target

def urls_for_parser_page(number):
    global test_urls
    return_url = ''
    for key in test_urls.keys():
        if number == test_urls[key]:
            return_url = key
    print('You are testing url ' + str(number) + ' in test_urls for testing parser_page')
    return return_url


####################################testing get_category_urls###################################
def get_fake_request_get_category_urls(url):
    start_index = len("http://news.cts.com.tw/")
    end_index = url.index("index") - 1
    category = url[start_index:end_index]

    if "#cat_list" in url:
        targetfile = open(path + '/tests/get_category_urls/fake_page_' + category + '_1', 'r')
        fake_page_content = targetfile.read()
        targetfile.close()

        fake_page = Response()
        fake_page._content = fake_page_content
        fake_page.encoding = 'iso8859-1'
        return fake_page

    else:
        new_url = url[:-5] #delete ".html"
        start_index = len("http://news.cts.com.tw/" + category + "/index")
        page_index = int(new_url[start_index:])
        if page_index in range(2,21):
            targetfile = open(path + '/tests/get_category_urls/fake_page_' + category + '_' + str(page_index), 'r')
            fake_page_content = targetfile.read()
            targetfile.close()

            fake_page = Response()
            fake_page._content = fake_page_content
            fake_page.encoding = 'iso8859-1'
            return fake_page
        else:
            print "The url is not supported"

def patch_request_get_category_urls():
    global ori_requests_get
    ori_requests_get = requests.get
    requests.get = get_fake_request_get_category_urls

def unpatch_request_get_category_urls():
    global ori_requests_get
    requests.get = ori_requests_get

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
    targetfile = open(path + '/tests/get_category_urls/test_urls', 'r')
    content = targetfile.read()
    targetfile.close()

    start_index = content.index(str(number)) + len(str(number)) + 1
    target_content = content[start_index:]
    end_index = target_content.index(',')
    return_url = target_content[:end_index]
    print('You are testing url ' + str(number) + ' in test_urls for testing get_category_urls')
    #print return_url
    return return_url


##########################################compare two dictionaries#######################################
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


class TestCtsnews(unittest.TestCase):
    
    def test_get_parser_page(self):
        patch_request_get_parser_page()
        for i in range(3):
            test_url = urls_for_parser_page(i + 1)
            result = cts_parser.parser_page(test_url)
            target = data_for_parser_page(test_url)

            if compare_dict(result, target) == True:
                print "Test Result: Succeed"
            else:
                print "Test Result: Fail"
        unpatch_request_get_parser_page()
    
    def test_get_category_urls(self):
        patch_request_get_category_urls()
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
        unpatch_request_get_category_urls()
        

if __name__ == '__main__':
    unittest.main()