# -*- coding: utf-8 -*-
import technews_parser
import requests
import pickle
import os.path

the_path_of_this_file = os.path.dirname(os.path.abspath(__file__))

#-----------------------------instructions----------------------------
#     use main functions at the bottom to create info for test case
#----------------------------------------------------------------------



#------------------------parser_page_fake_data-------------------
#store result for testing parser_page function
#----------------------------------------------------------------
def parser_page_fake_data(url):
    page_data = technews_parser.parser_page(url)
    appending_dict = {
        url: page_data
    }
    targetfile_read = open(the_path_of_this_file + '/pickle/parser_page/fake_data_pickle', 'r')
    parser_page_target= pickle.load(targetfile_read)

    temp_dict = parser_page_target.copy()
    appending_dict.update(temp_dict)

    targetfile = open(the_path_of_this_file + '/pickle/parser_page/fake_data_pickle', 'wb')
    pickle.dump(appending_dict, targetfile)
    targetfile.close()
    print('parser_page_fake_data is done')


#------------------------parser_page_fake_request----------------
#create the fake response for testing parser_page function
#----------------------------------------------------------------
def parser_page_fake_request(url):
    facebook_api_url = 'https://api.facebook.com/method/links.getStats?urls=' + url
    facebook_comment_api_url = 'http://graph.facebook.com/comments?filter=stream&fields=from,like_count,message,created_time,id,parent.fields(id)&id=' + url

    response1 = requests.get(url)
    response2 = requests.get(facebook_api_url)
    response3 = requests.get(facebook_comment_api_url)

    appending_dict = {
        url: response1,
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


#------------------------parser_page_test_urls---------------------
#store urls for testing parser_page function
#----------------------------------------------------------------
def parser_page_test_urls(url):
    # urls_list=[]
    targetfile_read = open(the_path_of_this_file + '/pickle/parser_page/test_urls_pickle', 'r')
    urls_list = pickle.load(targetfile_read)
    if url in urls_list:
        print('url already exist for testing parser_page')
    else:
        urls_list.append(url)
        targetfile = open(the_path_of_this_file + '/pickle/parser_page/test_urls_pickle', 'wb')
        pickle.dump(urls_list, targetfile)
        targetfile.close()
        print('parser_page_test_urls is done')


#------------------------get_category_urls_fake_data-------------
#store result for testing get_category_urls function
#-------------------------------------------------------------
def get_category_urls_fake_data(url):
    detail_urls = technews_parser.get_category_urls(url)
    appending_dict = {
        url: detail_urls
    }
    targetfile_read = open(the_path_of_this_file + '/pickle/get_category_urls/fake_data_pickle', 'r')
    get_category_urls_target= pickle.load(targetfile_read)

    temp_dict = get_category_urls_target.copy()
    appending_dict.update(temp_dict)

    targetfile = open(the_path_of_this_file + '/pickle/get_category_urls/fake_data_pickle', 'wb')
    pickle.dump(appending_dict, targetfile)
    targetfile.close()
    print('get_category_urls_fake_data is done')


#------------------------get_category_urls_html------------------
#create the html for testing get_category_urls function
#----------------------------------------------------------------
def get_category_urls_fake_request(url):
    response = requests.get(url)
    appending_dict = {
        url: response
    }
    targetfile_read = open(the_path_of_this_file + '/pickle/get_category_urls/fake_request_pickle', 'r')
    responses = pickle.load(targetfile_read)

    temp_dict = responses.copy()
    appending_dict.update(temp_dict)

    targetfile = open(the_path_of_this_file + '/pickle/get_category_urls/fake_request_pickle', 'wb')
    pickle.dump(appending_dict, targetfile)
    targetfile.close()
    print('get_category_urls_fake_request is done')


#------------------------get_category_urls_test_urls-------------
#store urls for testing get_category_urls function
#----------------------------------------------------------------
def get_category_urls_test_urls(url):
    # urls_list=[]
    targetfile_read = open(the_path_of_this_file + '/pickle/get_category_urls/test_urls_pickle', 'r')
    urls_list = pickle.load(targetfile_read)
    if url in urls_list:
        print('url already exist for testing get_category_urls')
    else:
        urls_list.append(url)
        targetfile = open(the_path_of_this_file + '/pickle/get_category_urls/test_urls_pickle', 'wb')
        pickle.dump(urls_list, targetfile)
        targetfile.close()
        print('get_category_urls_test_urls is done')


#----------------------main functions---------------------------
#main funcitons to create data, request and urls
#----------------------------------------------------------------
def create_parser_page_data_and_request(url_for_parser_page):
    parser_page_fake_data(url_for_parser_page)
    parser_page_fake_request(url_for_parser_page)
    parser_page_test_urls(url_for_parser_page)

def create_get_category_urls_data_and_request(url_for_get_category_urls):
    get_category_urls_fake_data(url_for_get_category_urls)
    get_category_urls_fake_request(url_for_get_category_urls)
    get_category_urls_test_urls(url_for_get_category_urls)

# create_parser_page_data_and_request('http://technews.tw/2015/11/26/apple-iphone-2018-oled-﻿panel/')
# create_get_category_urls_data_and_request('http://technews.tw/category/tablet/page/3/')
