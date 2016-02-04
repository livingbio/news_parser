# -*- coding: utf-8 -*-
import technews_parser
import requests
import pickle
import os.path

the_path_of_this_file = os.path.dirname(os.path.abspath(__file__))

# url_for_parser_page = 'http://technews.tw/2015/11/26/apple-iphone-2018-oled-﻿panel/'
# url_for_parser_page = 'http://technews.tw/2016/01/06/iphone-6s-no-good-apple/'
# url_for_get_category_urls = 'http://technews.tw/category/tablet/page/38/'
# url_for_get_category_urls = 'http://technews.tw/category/tablet/page/37/'

#------------------------parser_page_pickle---------------------
#pickle result for parser_page function
#----------------------------------------------------------------
def parser_page_pickle():
    page_data = technews_parser.parser_page(url_for_parser_page)
    appending_dict = {
        url_for_parser_page: page_data
    }
    targetfile_read = open(the_path_of_this_file + '/pickle/parser_page/fake_data_pickle', 'r')
    parser_page_target= pickle.load(targetfile_read)

    temp_dict = parser_page_target.copy()
    appending_dict.update(temp_dict)

    targetfile = open(the_path_of_this_file + '/pickle/parser_page/fake_data_pickle', 'wb')
    pickle.dump(appending_dict, targetfile)
    targetfile.close()
    print('parser_page_pickle is done')


#------------------------parser_page_fake_request-----------------------
#create the fake response for testing parser_page function
#----------------------------------------------------------------
def parser_page_fake_request():
    facebook_api_url = 'https://api.facebook.com/method/links.getStats?urls=' + url_for_parser_page
    facebook_comment_api_url = 'http://graph.facebook.com/comments?filter=stream&fields=from,like_count,message,created_time,id,parent.fields(id)&id=' + url_for_parser_page

    response1 = requests.get(url_for_parser_page)
    response2 = requests.get(facebook_api_url)
    response3 = requests.get(facebook_comment_api_url)

    appending_dict = {
        url_for_parser_page: response1,
        facebook_api_url: response2,
        facebook_comment_api_url: response3,
    }

    targetfile_read = open(the_path_of_this_file + '/pickle/parser_page/fake_request_pickle', 'r')
    parser_page_target= pickle.load(targetfile_read)

    temp_dict = parser_page_target.copy()
    appending_dict.update(temp_dict)

    targetfile = open(the_path_of_this_file + '/pickle/parser_page/fake_request_pickle', 'wb')
    pickle.dump(appending_dict, targetfile)
    targetfile.close()
    print('parser_page_fake_request is done')


#------------------------get_category_urls_pickle-------------
#pickle result for get_category_urls function
#-------------------------------------------------------------
def get_category_urls_pickle():
    detail_urls = technews_parser.get_category_urls(url_for_get_category_urls)
    appending_dict = {
        url_for_get_category_urls: detail_urls
    }
    targetfile_read = open(the_path_of_this_file + '/pickle/get_category_urls/fake_data_pickle', 'r')
    get_category_urls_target= pickle.load(targetfile_read)

    temp_dict = get_category_urls_target.copy()
    appending_dict.update(temp_dict)

    targetfile = open(the_path_of_this_file + '/pickle/get_category_urls/fake_data_pickle', 'wb')
    pickle.dump(appending_dict, targetfile)
    targetfile.close()
    print('get_category_urls_pickle is done')


#------------------------get_category_urls_html------------------
#create the html for testing get_category_urls function
#----------------------------------------------------------------
def get_category_urls_fake_request():
    response = requests.get(url_for_get_category_urls)

    appending_dict = {
        url_for_get_category_urls: response
    }
    targetfile_read = open(the_path_of_this_file + '/pickle/get_category_urls/fake_request_pickle', 'r')
    responses = pickle.load(targetfile_read)

    temp_dict = responses.copy()
    appending_dict.update(temp_dict)

    targetfile = open(the_path_of_this_file + '/pickle/get_category_urls/fake_request_pickle', 'wb')
    pickle.dump(appending_dict, targetfile)
    targetfile.close()
    print('get_category_urls_fake_request is done')

# parser_page_pickle()
# parser_page_fake_request()
# get_category_urls_pickle()
# get_category_urls_fake_request()

#------------------------each_newsData_pickle---------------------------------------
#pickle result for each_newsData_of_a_category_from_startPage_to_endPage function
#-----------------------------------------------------------------------------------
# def each_newsData_pickle():
#     pages_data = technews_parser.each_newsData_of_a_category_from_startPage_to_endPage('http://technews.tw/category/tablet/', 35, 36)
#     targetfile = open(the_path_of_this_file + '/pickle/each_newsData_of_a_category_from_startPage_to_endPage/each_newsData_of_a_category_from_startPage_to_endPage_pickle', 'wb')
#     pickle.dump(pages_data, targetfile)
#     targetfile.close()
