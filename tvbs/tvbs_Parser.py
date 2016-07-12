# -*- coding: utf-8 -*
from bs4 import BeautifulSoup
import requests
import datetime
import json
import time
import random

def parser_page(url):
    """Get information from tvbs news 
    
    Args: 
        url: tvbs news url
    Return:
        A dict contains information we want
    """

    # -------------- result dictionary --------------
    # this function will return this dictionary 
    # dictionary contains the info of given page
    # -----------------------------------------------
    result = {
        "url": None,
        "source_press": None,
        "title": None,
        "post_time": None,
        "journalist": None,
        "content": None,
        "compare": None,
        "keyword": None,
        "fb_like": None,
        "fb_share": None,
        "category": None,
        "comment": None,
        }
    
    # ----- get text from url page -----
    sourse_code_request = requests.get(url)
    sourse_code = sourse_code_request.text.encode(sourse_code_request.encoding).decode("utf-8")
    soup = BeautifulSoup(sourse_code, "html.parser")
#     print(sourse_code)
    
    # -------------- get result dict item --------------
    # use css selector to get result dict item 
    # --------------------------------------------------
    
    # ------------------- get url -------------------
    url = url
    
    # ------------------ get title ------------------
    try:
        title = soup.select(".titel26")[0].getText().strip()
    except IndexError:
        title = None
#     print(title)  
    
    # ---------------- get journalist ----------------
    try:
        journalist_list = soup.select(".under15")[1].getText().split()
        journalist = []
        for j in journalist_list[1:]:
            journalist.append(j)
            if j == "/":
                journalist.pop()
                break
    except IndexError :
        journalist = None
#     print(journalist)
     
    # ----------------- get post_time -----------------
    try:
        post_time_naive = soup.select(".under15")[0].getText()
        post_time = datetime.datetime.strptime(post_time_naive, '%Y/%m/%d %H:%M')
    except (IndexError, ValueError) :
        post_time = None
#     print(post_time)
     
    # ------------------ get content ------------------
    content_naive = soup.select(".newsdetail-content > p")
    content = ""
    for c in content_naive:
        content += c.getText()
#     print(content)    
         
    # ------------------ get keyword ------------------
    keywords = soup.select("[name=news_keywords]")[0]["content"].split(",")
#     print(keywords)
    
    # ----------------- get category -----------------
    category_dict = {"local":u"社會", "world":u"國際", "politics":u"政經", "life":u"民生消費", 
                     "china":u"兩岸", "entertainment":u"影劇", "sports":u"體育", "warm":u"暖聞",
                     "fun":u"奇趣", "health":u"健康","travel":u"Fun飯","supercars":u"玩車",
                     "tech":u"科技","hipster":u"文青"}
    category = category_dict[url.split("/")[3]]
#     print(category)

     
    # ----- get text from facebook request page (share/like) -----
    fb_sourse_code = requests.get("https://api.facebook.com/method/links.getStats?urls=" + url).text
    fb_soup = BeautifulSoup(fb_sourse_code, "html.parser")
    # ----------------- get fb_like -----------------
    try:
        fb_like = fb_soup.find("like_count").string
    except KeyError:
        fb_like = None
#     print(fb_like)
    # ----------------- get fb_share -----------------   
    try:
        fb_share = fb_soup.find("share_count").string
    except KeyError:
        fb_share = None
#     print(fb_share) 
   
    # ----- get text from facebook request page (comment) -----
     
    # -----------------  get fb comment -----------------
    # this method will return comment dict in one page  
    # ---------------------------------------------------
    def make_fb_comments_dictionary(url):
        fb_comment_sourse_code = requests.get(url).text
        fb_comment_sourse_code_dict = json.loads(fb_comment_sourse_code)
        try:  
            for comment in fb_comment_sourse_code_dict["data"]:
                try:
                    if "id" in comment.get("parent",{}).keys():
                        for each_comment in total_comments:
                            if each_comment['id'] == comment['parent']['id']:
                                 add_sub_comment = {
                                    'id': comment['id'],
                                    'actor': comment['from']['name'],
                                    'like': int(comment['like_count']),
                                    'content': comment['message'],
                                    'post_time': datetime.datetime.strptime(comment['created_time'], '%Y-%m-%dT%H:%M:%S+0000'),
                                    'source_type': 'facebook',
                                }
                                 each_comment['sub_comments'].append(add_sub_comment)
#                                  print(add_sub_comment)
                    else:
                        add_comment = {
                               'id': comment['id'],
                               'actor': comment['from']['name'],
                               'like': int(comment['like_count']),
                               'content': comment['message'],
                               'post_time': datetime.datetime.strptime(comment['created_time'], '%Y-%m-%dT%H:%M:%S+0000'),
                               'source_type': 'Facebook',
                               'sub_comments': [],
                               }    
                        total_comments.append(add_comment)
                         
                        if "next" in fb_comment_sourse_code_dict.get("paging",{}):
                            make_fb_comments_dictionary("http://graph.facebook.com/comments?filter=stream&fields=from,like_count,message,created_time,id,parent.fields(id)&id=" + url + "&after=" + fb_comment_sourse_code_dict["paging"]["cursors"]["after"])
                 
                except KeyError:
                    pass
        except KeyError:
            pass
 
    # ----------------------- fb_comment ------------------------
    total_comments = []
    make_fb_comments_dictionary("http://graph.facebook.com/comments?filter=stream&fields=from,like_count,message,created_time,id,parent.fields(id)&id=" + url)

#     print(len(total_comments))
#     print(total_comments)     
     
    # ----------------------- result ------------------------
    # get all the data above in a dictionary called result
    # return with {'key1': 'value1', 'key2': 'value2',...}
    # -------------------------------------------------------
    result['url'] = url
    result['title'] = title
    result['post_time'] = post_time
    result['journalist'] = " ".join(journalist)
    result['content'] = content
    result['keyword'] = keywords
    result['fb_like'] = int(fb_like)
    result['fb_share'] = int(fb_share)
    result['category'] = category
    result['comment'] = total_comments
     
    #print(result)
    return result
    
def get_category_urls(category_url):
    """Get all urls of tvbs news in certain category 
    
    Args: 
        category_url: tvbs news category url e.g. http://news.tvbs.com.tw/pets/
    Return:
        A list of all urls of tvbs news in certain category 
    """
    
    # -------------- urls list --------------
    # this function will return this list
    # list contains all news url of category 
    # ---------------------------------------
    detail_urls = []
    
    # ------- get text from url page ------
    sourse_code_request = requests.get(category_url)
    source_code = sourse_code_request.text.encode(sourse_code_request.encoding).decode("utf-8")
    soup = BeautifulSoup(source_code, 'html.parser')
#     print(source_code)

    # --------- get category name ---------
    
    try:
        category_name = category_url.split('/')[-1]
    except IndexError:
        pass
#     print(category_name)

    # ---------- get No.1~3 news ----------
    no1_news = soup.select(".information-txt1 > a")[0]["href"]
    detail_urls.append(category_url + "/" + no1_news.split("/")[-1])
    no2_news = soup.select(".information-txt1 > a")[1]["href"]
    detail_urls.append(category_url + "/" + no2_news.split("/")[-1])
    no3_news = soup.select(".information-txt1 > a")[2]["href"]
    detail_urls.append(category_url + "/" + no3_news.split("/")[-1])
#     print(no1_news, no2_news, no3_news)
  
    #  ---------- get other news ----------
    page = 1
    try:
        while True:
            try:
                get_news_source_code_request = requests.get("http://news.tvbs.com.tw/news/get_cate_news_json/" + no1_news.split("/")[-1] + "/" + category_name + "/" + str(page))
                get_news_source_code = get_news_source_code_request.text.encode(get_news_source_code_request.encoding).decode("utf-8")
            except requests.exceptions.ConnectionError:
                time.sleep(1)
#                 print(page)
                continue
            get_news_dict = json.loads(get_news_source_code[1:])
            if len(get_news_dict) == 0:
                break
            for i in get_news_dict:
                detail_urls.append(category_url + "/" + i["news_id"])
            page += 1             
    except IndexError:
         pass
        
#     print(detail_urls)
#     print(len(detail_urls))
    return detail_urls

# parser_page("http://news.tvbs.com.tw/politics/661869")
# parser_page("http://news.tvbs.com.tw/life/662570")
# get_category_urls("http://news.tvbs.com.tw/health")
# get_category_urls("http://news.tvbs.com.tw/tech")
