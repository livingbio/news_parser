# -*- coding: utf-8 -*-
from requests import Response
import tvbs_Parser
import requests
import unittest
import datetime
import json

category_url_list = ['http://news.tvbs.com.tw/health',
                     'http://news.tvbs.com.tw/supercars',
                     'http://news.tvbs.com.tw/hipster',
                     'http://news.tvbs.com.tw/warm', ]

news_url = ['http://news.tvbs.com.tw/politics/661869',
            'http://news.tvbs.com.tw/life/663712',
            'http://news.tvbs.com.tw/politics/663309',
            'http://news.tvbs.com.tw/life/663386', ]


# ----------------------------------------------------------------
#  fake_request_get(url): return fake response
#  patch_request_get(): hooked fake requests.get
#  unpatch_request_get(): recover requests.get
#  get_answer_dic(url): according url to find file and get answer
#                       dictionary for parser page test
# ----------------------------------------------------------------
def fake_request_get(url):
    global dir
    hash_url = str(hash(url))
    resp = None
    with open(dir + "/" + hash_url, "r") as response_file:
        resp = Response()
        resp._content = response_file.read()
        resp.encoding = "utf-8"
    return resp

def patch_request_get():
    global origin_get 
    origin_get = requests.get
    requests.get = fake_request_get
    
def unpatch_request_get():
    global origin_get 
    requests.get = origin_get

def get_answer_dic(url):
    global dir
    file_name = "_".join(url.split("/")[-2:])
    
    with open(dir + "/" + file_name + "_answer", "r") as answer_file:
        answer_dic = json.load(answer_file)
    
    answer_dic["post_time"] = datetime.datetime.strptime(answer_dic["post_time"], '%Y/%m/%d %H:%M')
    
    for each_comment in answer_dic["comment"]:
        each_comment["post_time"] = datetime.datetime.strptime(each_comment["post_time"], '%Y-%m-%dT%H:%M:%S+0000')
    
        if len(each_comment["sub_comments"]) != 0:
            for each_sub_comment in each_comment["sub_comments"]:
                each_sub_comment["post_time"] = datetime.datetime.strptime(each_sub_comment["post_time"], '%Y-%m-%dT%H:%M:%S+0000')
    
    return answer_dic      
              
     
# ==================== Test =======================
#  Test tvbs_Parser's two function: 
#  1. parser_page(page_url)
#  2. get_category_urls(category_url)
# =================================================
 
class TvbsParserTest(unittest.TestCase):
    
    # ---------- Testcase: parser page ----------
    def test_parser_page(self):
        global dir
        patch_request_get()
        for page_url in news_url:
            dir = "./" + "_".join(page_url.split("/")[-2:])
            page_dic = tvbs_Parser.parser_page(page_url)
            answer_dic = get_answer_dic(page_url)
            try:
                self.assertEqual(page_dic, answer_dic)
            except AssertionError:
                print(page_url + " test fail")
        unpatch_request_get()
        
    # ---------- Testcase: category url ----------    
    def test_get_category_urls(self):
        patch_request_get()
        global dir
        for category_url in category_url_list:
            category = category_url.split("/")[-1]
            dir = "./" + category
            category_urls = tvbs_Parser.get_category_urls(category_url)
            answer_urls = open(dir + "/" + category + "_category_answer", "r").read().split(" ")
            try:
                self.assertEqual(category_urls, answer_urls)
            except AssertionError:
                print(category_url + " test fail")
        unpatch_request_get()
   
if __name__ == '__main__':
    unittest.main() 
