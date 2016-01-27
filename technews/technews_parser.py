# -*- coding: utf-8 -*-
import requests
from bs4 import BeautifulSoup
import datetime
import json
import pytz
from pytz import timezone, all_timezones
import pickle

#------------------function parse_page--------------------
#get data from a news page
#---------------------------------------------------------
def parser_page(url):
    #-------------result dictionary------------------
    #the result that this function return
    #------------------------------------------------
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

    #-------------get text from the url page------------------
    #
    #---------------------------------------------------------
    source_code = requests.get(url)

    plain_text = source_code.text

    soup = BeautifulSoup(plain_text, 'html.parser')
    # print(soup)


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
    post_time_text = post_time_text.encode('utf-8')

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


    keyword = []
    for i in soup.findAll('a', {'rel': 'tag'}):
        keyword.append(i.text)


    #-------------fb_like & fb_share-----------------------
    #fb likes count & share counts of each news
    #------------------------------------------------------
    def fb_plugin_count_page(url):
        code = requests.get('http://api.facebook.com/restserver.php?method=links.getStats&urls=' + url)
        html_text = code.text
        fb_plugin_page_soup = BeautifulSoup(html_text, 'html.parser')

        fb_like_count = fb_plugin_page_soup.find('total_count').string
        fb_share_count = fb_plugin_page_soup.find('share_count').string
        return(int(fb_like_count), int(fb_share_count))
    fb_like, fb_share = fb_plugin_count_page(url)


    #-----------------------category-----------------------
    #the category of news on the website
    #------------------------------------------------------
    category = []
    times_for_category = 0
    for i in soup.select("header.entry-header table td span.body")[2]:
        if times_for_category %2 == 1:
            category.append(i.text)
        times_for_category +=1


    # global category_urls
    category_urls = []
    for i in soup.select('ul.nav-menu > li > a'):
        category_urls.append(i['href'])


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

            comment_time_in_UTC = datetime.datetime.strptime(comment['created_time'], '%Y-%m-%dT%H:%M:%S+0000')
            # comment_time_in_UTC = parse(comment['created_time'])
            #
            # comment_time_in_TW = comment_time_in_UTC.astimezone(timezone('ROC'))
            # print(comment_time_in_TW)

            while True:
                try:
                    if comment['parent']['id']:
                        for each_comment in total_comments:
                            if each_comment['id'] == comment['parent']['id']:
                                each_sub_comment = {
                                    'id': comment['id'],
                                    'actor': comment['from']['name'],
                                    'like': int(comment['like_count']),
                                    'content': comment['message'],
                                    'post_time': comment_time_in_UTC,
                                    'source_type': 'facebook',
                                }
                                each_comment['sub_comments'].append(each_sub_comment)
                except KeyError:
                    each_comment = {
                        'id': comment['id'],
                        'actor': comment['from']['name'],
                        'like': int(comment['like_count']),
                        'content': comment['message'],
                        'post_time': comment_time_in_UTC,
                        'source_type': 'facebook',
                        'sub_comments': [],
                    }
                    total_comments.append(each_comment)
                finally:
                    break
    make_fb_comments_dictionary(fb_comments_json)


    #--------------------result------------------------------
    #get all the data above in a dictionary called result
    #
    #return with {'key1': 'value1', 'key2': 'value2',...}
    #--------------------------------------------------------
    # result = {
    #     "url": url,
    #     "source_press": source_press,
    #     "title": title,
    #     "post_time": post_time,
    #     "journalist": journalist,
    #     "content": content,
    #     "compare": None,
    #     "keyword": [],
    #     "fb_like": fb_like,
    #     "fb_share": fb_share,
    #     "category": category,
    #     "comment": total_comments,
    # }
    result['url'] = url
    result['source_press'] = source_press
    result['title'] = title
    result['post_time'] = post_time
    result['journalist'] = journalist
    result['content'] = content
    result['keyword'] = keyword
    result['fb_like'] = fb_like
    result['fb_share'] = fb_share
    result['category'] = category
    result['comment'] = total_comments

    return(result)


#-----------------------Testing page_data----------------------------------
#call parser_page function with certain URL, store the data in to page_data
#--------------------------------------------------------------------------
# page_data = parser_page('http://technews.tw/2016/01/04/tiobe-2015-programming-language-index/')
# page_data = parser_page('http://technews.tw/2016/01/06/iphone-6s-no-good-apple/')
page_data = parser_page('http://technews.tw/2015/11/26/apple-iphone-2018-oled-﻿panel/')

#------------------------parser_page_pickle---------------------
#pickle result for parser_page function
#----------------------------------------------------------------
# targetfile = open('pickle/parser_page/parser_page_pickle', 'wb')
# pickle.dump(page_data, targetfile)
# targetfile.close()

# targetfile_read = open('pickle/parser_page/parser_page_pickle', 'r')
# b = pickle.load(targetfile_read)
# print(b)



# with open('parser_page.html', 'w') as outfile:
#     response = requests.get('http://technews.tw/2015/11/26/apple-iphone-2018-oled-﻿panel/')
#     for block in response.iter_content(1024):
#         outfile.write(block)


# with open('parser_page.json', 'w') as outfile:
#     page_data['post_time'] = str(page_data['post_time'])
#     for comment in page_data['comment']:
#         comment['post_time'] = str(comment['post_time'])
#         while True:
#             try:
#                 if comment['sub_comments'][0]:
#                     for i in comment['sub_comments']:
#                         i['post_time'] = str(i['post_time'])
#             except IndexError:
#                 continue
#             finally:
#                 break
#
#     json.dump(page_data, outfile)


# fr = open('parser_page.json', 'r')
# parser_page_json = json.load(fr)

# print(parser_page_json['keyword'][3])


#-------------Function get_category_urls----------------------
#get url of each news from a certain page
#
#return with [news1_url, news2_url, news3_url,....]
#-------------------------------------------------------------
def get_category_urls(category_url):
    #-------------get text from the url page------------------
    #
    #---------------------------------------------------------
    source_code = requests.get(category_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')

    #------------------detail_urls-----------------------------
    #get each news url and append into a list called detail_urls
    #---------------------------------------------------------
    detail_urls = []
    for i in soup.findAll('h1', {'class': 'entry-title'}):
        detail_urls.append(i.a.attrs['href'])
    return(detail_urls)


#---------------Testing detail_urls-----------------------------------------------------
#call get_category_urls function with certain URL, store the urls list in to detail_urls
#---------------------------------------------------------------------------------------
detail_urls = get_category_urls('http://technews.tw/category/tablet/')
# print(detail_urls)

#------------------------get_category_urls_pickle---------------------
#pickle result for get_category_urls function
#----------------------------------------------------------------
# targetfile = open('pickle/get_category_urls/get_category_urls_pickle', 'wb')
# pickle.dump(detail_urls, targetfile)
# targetfile.close()
#
# targetfile_read = open('pickle/get_category_urls/get_category_urls_pickle', 'r')
# b = pickle.load(targetfile_read)
# print(b)


# with open('get_category_urls.html', 'w') as outfile:
#     response = requests.get('http://technews.tw/category/tablet//')
#     for block in response.iter_content(1024):
#         outfile.write(block)


# with open('get_category_urls.json', 'w') as outfile:
#     json.dump(detail_urls, outfile)

# gFile = open('get_category_urls.json', 'r')
# get_category_urls_json = json.load(gFile)
# print(type(get_category_urls_json))


#-------------Function switch_page_and_get_detail_urls-----------------
#get url of each news with looping pages in a certain category

#return with [[url1,url2,url3...in page 1], [url1,url2...in page 2],...]
#----------------------------------------------------------------------
def switch_page_and_get_detail_urls(the_url_of_category_to_switch_page, start_page, end_page):
    # urls_of_pages_in_a_certain_category = []
    urls_of_a_category_list_index_by_page = []
    if start_page >= 1:
        number_of_page = start_page
    else:
        number_of_page = 1

    if isinstance(end_page, int) == False:
        end_page = None

    while True:
        try:
            num = str(number_of_page)
            current_page_url = the_url_of_category_to_switch_page + 'page/' + num
            certain_page_urls_list = get_category_urls(current_page_url)

            # urls_of_pages_in_a_certain_category.append(current_page_url)
            urls_of_a_category_list_index_by_page.append(certain_page_urls_list)
            if number_of_page >= end_page:
                print('The end page URL is ' + the_url_of_category_to_switch_page + 'page/' + str(number_of_page))
                break
            number_of_page += 1

        except AttributeError:
            print('The end page URL is ' + the_url_of_category_to_switch_page + 'page/' + str(number_of_page-1))
            break
    return (urls_of_a_category_list_index_by_page)


#-------------Function each_newsData_of_a_category_from_startPage_to_endPage-----------------------------
#get data of each news with looping pages in a certain category
#
#return with [{data1}, {data2}, {data3},...]
#--------------------------------------------------------------------------------------------------------
def each_newsData_of_a_category_from_startPage_to_endPage(the_url_of_category_to_switch_page, start_page, end_page):
    each_newsData_of_a_category_list = []
    urls_of_a_category_list_index_by_page_list = switch_page_and_get_detail_urls(the_url_of_category_to_switch_page, start_page, end_page)
    for page in urls_of_a_category_list_index_by_page_list:
        for news_url in page:
            data = parser_page(news_url)
            print('crawling ' + news_url)
            each_newsData_of_a_category_list.append(data)
    return(each_newsData_of_a_category_list)


#-----------------------Testing pages_data----------------------------------------------------
#call each_newsData_of_a_category_from_startPage_to_endPage function with certain category URL
#
#store the data in to pages_data
#---------------------------------------------------------------------------------------------
# pages_data = each_newsData_of_a_category_from_startPage_to_endPage('http://technews.tw/category/tablet/', 1, 1)
# print(pages_data)


# with open('newsData_from_startPage_to_endPage.json', 'w') as outfile:
#     for each_newsData in pages_data:
#         each_newsData['post_time'] = str(each_newsData['post_time'])
#         for comment in each_newsData['comment']:
#             comment['post_time'] = str(comment['post_time'])
#             while True:
#                 try:
#                     if comment['sub_comments'][0]:
#                         for i in comment['sub_comments']:
#                             i['post_time'] = str(i['post_time'])
#                 except IndexError:
#                     continue
#                 finally:
#                     break
#         print('fixing post_time')
#     json.dump(pages_data, outfile)

# bFile = open('newsData_from_startPage_to_endPage.json', 'r')
# newsData_from_startPage_to_endPage_json = json.load(bFile)
# print(type(newsData_from_startPage_to_endPage_json))


#-----------------------categories_urls_of_technews--------------------
#category urls of technews,
#
#retrieved by the variable "category_urls" in parser_page function
#---------------------------------------------------------------------
categories_urls_of_technews = ['http://technews.tw/category/smartphone/', 'http://technews.tw/category/tablet/', 'http://technews.tw/category/internet/', 'http://technews.tw/category/%E5%90%8D%E4%BA%BA%E5%A0%82/', 'http://technews.tw/category/component/', 'http://technews.tw/category/%e5%b0%96%e7%ab%af%e7%a7%91%e6%8a%80/', 'http://technews.tw/category/biotech/', 'http://technews.tw/category/%e8%83%bd%e6%ba%90%e7%a7%91%e6%8a%80/', 'http://technews.tw/selects/', 'http://technews.tw/category/human-resource/', 'http://technews.tw/category/realtime-news/', 'http://technews.tw/category/business/', 'http://technews.tw/category/picks/', 'http://technews.tw/aboutus/', 'http://technews.tw/contact/']
