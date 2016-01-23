import requests
from bs4 import BeautifulSoup
import datetime
import json
from pytz import timezone, all_timezones


def parser_page(url):
    #-------------get text from the url page------------------
    #
    #---------------------------------------------------------
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')


    #-------------url & source_press & title------------------
    #
    #---------------------------------------------------------
    url = url
    source_press = soup.select("div.indent a")[1]['href']
    title = soup.find('h1', {'class': 'entry-title'}).text


    #--------------------------post_time-------------------------
    #the post time of each news in datetime.datetime() format
    #
    #there are 2 methods to get it done, using method 1 by default
    #-------------------------------------------------------------

    #-------------------------post_time method 1 below-----------------------------
    post_time_text = soup.select("header.entry-header table td span.body")[1].text

    #-------------------------post_time method 2 below-----------------------------
    # for i in soup.findAll('span', {'class': 'head'}):
    #     if i.text == '發布日期':
    #         post_time_text = i.next_sibling.next_sibling.text
    post_time = datetime.datetime.strptime(post_time_text, '%Y 年 %m 月 %d 日 %H:%M ')


    #------------------journalist------------------------
    #the journalist of each news
    #----------------------------------------------------
    journalist = soup.find('a', {'rel': 'author'}).text


    #-------------------content--------------------------
    #content of each news
    #----------------------------------------------------
    content =""
    content_source_code = soup.select("div.indent p")
    for i in range(len(content_source_code)-1):
        content += content_source_code[i].text


    #-------------fb_like & fb_share-----------------------
    #fb likes count & share counts of each news
    #------------------------------------------------------
    def fb_plugin_count_page(url):
        code = requests.get('http://api.facebook.com/restserver.php?method=links.getStats&urls=' + url)
        html_text = code.text
        fb_plugin_page_soup = BeautifulSoup(html_text, 'html.parser')

        fb_like_count = fb_plugin_page_soup.find('total_count').string
        fb_share_count = fb_plugin_page_soup.find('share_count').string
        return(fb_like_count, fb_share_count)
    fb_like, fb_share = fb_plugin_count_page(url)


    #-----------------------category-----------------------
    #the category of news on the website
    #------------------------------------------------------
    category = []
    for i in soup.select('li.menu-item-has-children'):
        category_title = i.contents[0]
        item = category_title.text
        category.append(item)


    #-----------------------comment------------------------
    #the comments and their sub_comments of each news
    #------------------------------------------------------
    def fb_plugin_comment_page(url):
        # code = requests.get('http://graph.facebook.com/comments?id=' + url)
        code = requests.get('http://graph.facebook.com/comments?filter=stream&fields=from,like_count,message,created_time,id,parent.fields(id)&id=' + url)
        html_text = code.text
        fb_plugin_page_soup = BeautifulSoup(html_text, 'html.parser')
        fb_comments_string = str(fb_plugin_page_soup)
        fb_comments_json_page = json.loads(fb_comments_string)
        return (fb_comments_json_page)
    fb_comments_json = fb_plugin_comment_page(url)

    total_comments = []

    def make_fb_comments_dictionary(fb_comments_json):
        for comment in fb_comments_json['data']:
            comment_time_in_US = datetime.datetime.strptime(comment['created_time'], '%Y-%m-%dT%H:%M:%S%z')
            comment_time_in_TW = comment_time_in_US.astimezone(timezone('ROC'))

            while True:
                try:
                    if comment['parent']['id']:
                        for each_comment in total_comments:
                            if each_comment['id'] == comment['parent']['id']:
                                each_sub_comment = {
                                    'id': comment['id'],
                                    'actor': comment['from']['name'],
                                    'like': comment['like_count'],
                                    'content': comment['message'],
                                    'post_time': comment_time_in_TW,
                                    'source_type': 'facebook',
                                }
                                each_comment['sub_comments'].append(each_sub_comment)
                except KeyError:
                    each_comment = {
                        'id': comment['id'],
                        'actor': comment['from']['name'],
                        'like': comment['like_count'],
                        'content': comment['message'],
                        'post_time': comment_time_in_TW,
                        'source_type': 'facebook',
                        'sub_comments': [],
                    }
                    total_comments.append(each_comment)
                finally:
                    break
    make_fb_comments_dictionary(fb_comments_json)


    #--------------------return------------------------------------
    #collect all the data we get above in a dictionary, return it
    #--------------------------------------------------------------
    result = {
        "url": url,
        "source_press": source_press,
        "title": title,
        "post_time": post_time,
        "journalist": journalist,
        "content": content,
        "compare": None,
        "keyword": [],
        "fb_like": fb_like,
        "fb_share": fb_share,
        "category": category,
        "comment": total_comments,
    }

    return(result)


#-----------------------page_data---------------------------------
#call parser_page function with certain URL, store the data in to page_data
#-----------------------------------------------------------------

# page_data = parser_page('http://technews.tw/2016/01/04/tiobe-2015-programming-language-index/')
# page_data = parser_page('http://technews.tw/2016/01/06/iphone-6s-no-good-apple/')
page_data = parser_page('http://technews.tw/2015/11/26/apple-iphone-2018-oled-﻿panel/')
print(page_data)


def get_category_urls(category_url):
    #-------------get text from the url page------------------
    #
    #---------------------------------------------------------
    source_code = requests.get(category_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')


    #------------------detail_url-----------------------------
    #get each news url and append into a list called detail_url
    #---------------------------------------------------------
    detail_url = []
    for i in soup.findAll('h1', {'class': 'entry-title'}):
        detail_url.append(i.a.attrs['href'])
    return (detail_url)


#-----------------------crawling_urls_list------------------------------------------------
#call get_category_urls function with certain URL, store the data in to crawling_urls_list
#-----------------------------------------------------------------------------------------
crawling_urls_list = get_category_urls('http://technews.tw/category/tablet/')

# for i in crawling_urls_list:
#     ans = parser_page(i)
#     print(ans)
