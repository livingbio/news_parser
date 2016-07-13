from bs4 import BeautifulSoup
import requests
import json
import sys
import os
import time
import tvbs_Parser


# =========== Get category url and make directory ===========

category_url = sys.argv[1]   # e.g. http://news.tvbs.com.tw/health
category = category_url.split("/")[-1]

dir = "./" + category
if not os.path.exists(dir):
    os.makedirs(dir)


# ================= Output category request =================

sourse_code_request = requests.get(category_url)
source_code = sourse_code_request.text.encode("utf-8")
soup = BeautifulSoup(source_code, 'html.parser')


hash_category_url = str(hash(category_url))
category_file = open(dir + "/" + hash_category_url, "w")
category_file.write(source_code)


no1_news = soup.select(".information-txt1 > a")[0]["href"]
page = 1
try:
    while True:
        try:
            category_page_url = "http://news.tvbs.com.tw/news/get_cate_news_json/" + no1_news.split("/")[-1] + "/" + category_url.split("/")[-1] + "/" + str(page)
            get_category_page_source_code_request = requests.get(category_page_url)
            get_category_page_source_code = get_category_page_source_code_request.text.encode(get_category_page_source_code_request.encoding)
        except requests.exceptions.ConnectionError:
            time.sleep(1)
            continue
        
        hash_category_page_url = str(hash(category_page_url))
        category_page_file = open(dir + "/" + hash_category_page_url, "w")
        category_page_file.write(get_category_page_source_code)
        
        get_news_dict = json.loads(get_category_page_source_code.decode("utf-8")[1:])
        if len(get_news_dict) == 0: # to know when the while-loop finish
            break
        
        page += 1            
except IndexError:
    pass


# ================= Output catrgory answer =================

answer_list = tvbs_Parser.get_category_urls(category_url)
output_answer_file = open(dir + "/" + category + "_category_answer", "w")
output_answer_file.write(" ".join(answer_list))
