# -*- coding: utf-8 -*-
import requests
import urllib2
import urllib
import datetime
import json
import re
from bs4 import BeautifulSoup




def parser_page(url):

    url = 'http://newtalk.tw/news/view/2016-01-14/69148'
    data = urllib2.urlopen(url)
    soup = BeautifulSoup(data, 'html5lib')


    url = str(soup.select('meta[property="og:url"]'))[16:60]
    title = soup.find('div', {'class': 'content_title'}).text
    journalist = str(soup.find('a', {'itemprop': 'author'}))[86:95]
    content = soup.select('div > txt').text
    keyword = soup.select('div[class=tag_for_item]')


    # get post_time
    post_time_raw = str(soup.find('div', {'class': 'content_date'}))
    post_time = datetime.datetime(*map(int, re.findall(r'\d+', post_time_raw))[0:5])
    # update_time = datetime.datetime(*map(int, re.findall(r'\d+', post_time_raw))[5:12])


    # get keywords
    keyword = []
    keyword_pool = soup.select('div[class=tag_for_item]')
    keyword = [tag.text for tag in keyword_pool]


    # get fb_like
    fblike_url = 'https://www.facebook.com/v2.5/plugins/like.php?' + 'href=' + urllib.quote_plus(url.encode())
    fblike_data = urllib2.urlopen(fblike_url)
    soap = BeautifulSoup(fblike_data, 'html5lib')
    fb_like_article = str(soap.select('div > span > span')[0])
    fb_like = map(int, re.findall(r'\d+', fb_like_article))


    # get category
    category = []
    category = soup.find('div', {'class': 'tag_for_category clearfix'}).text


    # get comment
    comment_url = 'https://graph.facebook.com/comments?id=' + url + '&filter=stream&fields=parent.fields(id),message,from,created_time,like_count&after=WTI5dGJXVnVkRjlqZAFhKemIzSTZAOall6TXpZAME5UQXdORE16TURNd09qRTBOVEkxTVRVMU9UTT0ZD%22'
    comment_data = requests.get(comment_url).json()

    top_comments = []
    sub_comments = []

    for info in comment_data['data']:

        actor = info['from']['name']
        like = info['like_count']
        c_content = info['message']
        c_post_time = datetime.datetime(*map(int, re.findall(r'\d+', info['created_time'])))


        if not info.get('parent', False):
            top_comments.append(info)

        else:
            sub_comments.append(info)

    for sub_comment in sub_comments:
        for top_comment in top_comments:
            if top_comment['from']['id'] == sub_comment['parent']['id'][0:15]:
                c_sub_comment = sub_comment


    page_data = {
        "url": url,
        "source_press": None,
        "title": title,
        "post_time": post_time,
        "journalist": journalist,
        "content": content,
        "compare": None,
        "keyword": keyword,
        "fb_like": fb_like,
        "category": category,
        "top_comments": [{
            "actor": actor,
            "like": like,
            "dislike": None,
            "content": c_content,
            "post_time": c_post_time,
            "source_type": 'Facebook',

            "sub_comments": [{
                "actor": actor,
                "like": like,
                "dislike": None,
                "content": c_content,
                "post_time": c_post_time,
                "source_type": 'Facebook',
            }]
        }]
    }

    return page_data


# get category url
def get_category_urls(category_url):
    detail_urls = []
    cat_type = ['1/政治經濟/', '2/國際中國/', '3/生活科技/', '4/司法人權/', '5/藝文媒體/']
    main_url = 'http://newtalk.tw/news/category/'
    for t in cat_type:
        prefix_url = main_url + '%s' %t
        for i in range(1446):
            category_url = prefix_url + str(i)

            cat_data = requests.get(category_url)
            catsoup = BeautifulSoup(cat_data.text)
            detail_urls_pool = catsoup.select('div[class=news_title] > a')
            detail_urls = [a.attrs for a in detail_urls_pool]

    return detail_urls
