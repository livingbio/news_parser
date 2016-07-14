# -*- coding: utf-8 -*-
from requests import Response
import tvbs_Parser
import os
import unittest
import datetime
import json
import sqlite3
import mock

file_path = os.path.dirname(os.path.abspath(__file__))

# =========================== Function ===========================
#  fake_request_get(url): return fake response
#  get_answer_dic(url): according url to find file and get answer
#                       dictionary for parser page test
# ================================================================

def fake_request_get(url):
    hash_url = str(hash(url))
    cursor = conn.execute("SELECT  *  from ResponseList WHERE NAME = ?", (hash_url,))

    resp = Response()
    resp._content = cursor.fetchone()[1].encode("utf-8")
    resp.encoding = "utf-8"
    
    return resp

def get_answer_dic(url):
    hash_url = str(hash(url))
    cursor = conn.execute("SELECT  *  from ResponseList WHERE NAME = ?", (hash_url + "_answer",))

    answer_dic = json.loads(cursor.fetchone()[1].encode("utf-8"))
    
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
    
    def setUp(self):
        global conn
        conn = sqlite3.connect(file_path + '/testcase.db')
        
        page_cursor = conn.execute("SELECT  *  from PageList")
        self.page_url_list = []
        for row in page_cursor:
            self.page_url_list.append(row[0])
            
        category_cursor = conn.execute("SELECT  *  from CategoryList")
        self.category_url_list = []
        for row in category_cursor:
            self.category_url_list.append(row[0])
            
    @mock.patch('requests.get', side_effect=fake_request_get)
    def test_parser_page(self, mock_get):
        for page_url in self.page_url_list:
            page_dic = tvbs_Parser.parser_page(page_url)
            answer_dic = get_answer_dic(page_url)
            try:
                self.assertEqual(page_dic, answer_dic)
            except AssertionError:
                print(page_url + " test fail")

    @mock.patch('requests.get', side_effect=fake_request_get)
    def test_get_category_urls(self, mock_get):
        for category_url in self.category_url_list:
            category_news_url_list = tvbs_Parser.get_category_urls(category_url)
            
            cursor = conn.execute("SELECT  *  from ResponseList WHERE NAME = ?", (str(hash(category_url)) + "_category_answer",))
            answer_urls = cursor.fetchone()[1].encode("utf-8").split(" ")
            try:
                self.assertEqual(category_news_url_list, answer_urls)
            except AssertionError:
                    print(category_url + " test fail")

         
if __name__ == '__main__':
    unittest.main() 
