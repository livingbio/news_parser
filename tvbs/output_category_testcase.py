from bs4 import BeautifulSoup
import requests
import json
import sys
import os
import time
import tvbs_Parser
import sqlite3

# ======= Establish db connection and get category url =======

conn = sqlite3.connect('TestCase.db')
conn.text_factory = str

category_url = sys.argv[1]   # e.g. http://news.tvbs.com.tw/health


# ========= Handle request and store response in db =========

sourse_code_request = requests.get(category_url)
source_code = sourse_code_request.text.encode("utf-8")
soup = BeautifulSoup(source_code, 'html.parser')

hash_category_url = str(hash(category_url))
conn.execute("insert into ResponseList (NAME, RESULT, ORIGIN) values (?,?,?)", (hash_category_url , source_code, category_url))
  
no1_news = soup.select(".information-txt1 > a")[0]["href"]
page = 1
try:
    while True:
        try: # handle connection error
            category_page_url = "http://news.tvbs.com.tw/news/get_cate_news_json/" + no1_news.split("/")[-1] + "/" + category_url.split("/")[-1] + "/" + str(page)
            get_category_page_source_code_request = requests.get(category_page_url)
            get_category_page_source_code = get_category_page_source_code_request.text.encode(get_category_page_source_code_request.encoding)
        except requests.exceptions.ConnectionError:
            time.sleep(1)
            continue
        
        hash_category_page_url = str(hash(category_page_url))
        conn.execute("insert into ResponseList (NAME, RESULT, ORIGIN) values (?,?,?)", (hash_category_page_url , get_category_page_source_code, category_url))
        
        get_news_dict = json.loads(get_category_page_source_code.decode("utf-8")[1:])
        if len(get_news_dict) == 0: # to know when the while-loop finish
            break
        
        page += 1            
except IndexError:
    pass


# ================== Store category answer ==================

answer_list = tvbs_Parser.get_category_urls(category_url)
conn.execute("insert into ResponseList (NAME, RESULT, ORIGIN) values (?,?,?)", (hash_category_url+ "_category_answer" , " ".join(answer_list), category_url))


# ======== Commit change of db and add testcase list ========

conn.execute("insert into CategoryList (NAME) values (?)", (category_url,))

conn.commit()
conn.close()