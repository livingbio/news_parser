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
            'http://news.tvbs.com.tw/world/663491',
            'http://news.tvbs.com.tw/politics/663309',
            'http://news.tvbs.com.tw/life/663386', ]


# --------------------- Test parser page ---------------------
#  fake_request_get_parser_page(url): return fake response
#  patch_request_get_parser_page(): hooked fake requests.get
#  get_answer_dic(url): according url to find file and get 
#                       answer dictionary
# ------------------------------------------------------------
comment_page = 1
def fake_request_get_parser_page(url):
    global comment_page
    global file_name 
    global dir 
    resp = None
    
    if url in news_url:
        file_name = "_".join(url.split("/")[-2:])
        dir = "./" + file_name
        with open(dir + "/parser_page_" + file_name, "r") as page_file:
            resp = Response()
            resp._content = page_file.read()
            resp.encoding = "utf-8"
    elif url.startswith("https://api.facebook.com/method/links.getStats?urls="):
        with open(dir + "/parser_page_fb_getStats_" + file_name, "r") as page_fb_getStats_file:
            resp = Response()
            resp._content = page_fb_getStats_file.read()
    elif url.startswith("http://graph.facebook.com/comments?filter=stream&fields=from,like_count,message,created_time,id,parent.fields(id)&id="):
        with open(dir + "/parser_page_fb_comment_" + file_name + "_" + str(comment_page), "r") as page_fb_comment_file:
            resp = Response()
            resp._content = page_fb_comment_file.read()
            comment_page += 1
    return resp

def patch_request_get_parser_page():
    global origin_get 
    origin_get = requests.get
    requests.get = fake_request_get_parser_page        

def get_answer_dic(url):
    file_name = "_".join(url.split("/")[-2:])
    dir = "./" + file_name
    answer_dic = {}
    
    with open(dir + "/" + file_name + "_answer", "r") as answer_file:
        answer_dic = json.load(answer_file)
    
    answer_dic["post_time"] = datetime.datetime.strptime(answer_dic["post_time"], '%Y/%m/%d %H:%M')
    
    for each_comment in answer_dic["comment"]:
        each_comment["post_time"] = datetime.datetime.strptime(each_comment["post_time"],'%Y-%m-%dT%H:%M:%S+0000')
    
        if len(each_comment["sub_comments"]) != 0:
            for each_sub_comment in each_comment["sub_comments"]:
                each_sub_comment["post_time"] = datetime.datetime.strptime(each_sub_comment["post_time"],'%Y-%m-%dT%H:%M:%S+0000')
    
    return answer_dic            
            

# ---------------- Test get category url ----------------
#  fake_request_get_category(url): return fake response
#  patch_request_get_category(): hooked fake requests.get
# -------------------------------------------------------
def fake_request_get_category(url):
    resp = None
    if url in category_url_list:
        category = url.split("/")[-1]
        with open("./" + category + "/" + category + "_category_0", "r") as category_file:
            resp = Response()
            resp._content = category_file.read()
            resp.encoding = "utf-8"
    elif url.startswith("http://news.tvbs.com.tw/news/get_cate_news_json/"):
        page = url.split("/")[-1]
        category = url.split("/")[-2]
        with open("./" + category + "/" + category + "_category_" + page, "r") as category_file:
            resp = Response()
            resp._content = category_file.read()
            resp.encoding = "utf-8"
    return resp

def patch_request_get_category():
    global origin_get 
    origin_get = requests.get
    requests.get = fake_request_get_category
    
def unpatch_request_get():
    global origin_get 
    requests.get = origin_get
     
# ==================== Test =======================
#  Test tvbs_Parser's two function: 
#  1. parser_page(page_url)
#  2. get_category_urls(category_url)
# =================================================
 
class TvbsParserTest(unittest.TestCase):
    
    # ---------- Testcase: parser page ----------
    def test_parser_page(self):
        global comment_page 
        patch_request_get_parser_page()
        for page_url in news_url:
            comment_page = 1
            page_dic = tvbs_Parser.parser_page(page_url)
            answer_dic = get_answer_dic(page_url)
            self.assertEqual(page_dic, answer_dic)
       
        unpatch_request_get()
        
    # ---------- Testcase: category url ----------    
    def test_get_category_urls(self):
        patch_request_get_category()
        for category_url in category_url_list:
            category = category_url.split("/")[-1]
            category_urls = tvbs_Parser.get_category_urls(category_url)
            answer_urls = open("./" + category + "/" + category + "_category_answer", "r").read().split(" ")
            self.assertEqual(category_urls, answer_urls)
        unpatch_request_get()
   

if __name__ == '__main__':
    unittest.main() 
