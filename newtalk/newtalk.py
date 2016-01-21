import requests
import urllib2
import urllib
import time
import datetime
import json
import re
from bs4 import BeautifulSoup

url = 'http://newtalk.tw/news/view/2016-01-14/69148'
data = urllib2.urlopen(url)
soup = BeautifulSoup(data, 'html5lib')


def parser_page(url):

    page_data = parser_page(news detail url)

    return {
        "url": string
        "source_press": None
        "title": string
        "post_time": datetime.datetime()
        "journalist": string
        "content": string
        "compare": None,
        "keyword": [string, string, ...]
        "fb_like": int
        "category": [category, category]
        "comment": [{
            "actor": str
            "like": int
            "content": str
            "post_time": datetime.datetime
            "source_type": string

            sub_comments: [{
                "actor": str
                "like": int
                "dislike": int
                "content": str
                "post_time": datetime.datetime
                "source_type": string
            }]
        }]
    }


    url = str(soup.select('meta[property="og:url"]'))[16:60]
    title = soup.find('div', {'class': 'content_title'}).text
    journalist = str(soup.find('a', {'itemprop': 'author'}))[86:95]
    content = soup.select('div > txt').text
    keyword = soup.select('div[class=tag_for_item]')


# get post_time
post_time_raw = str(soup.find('div', {'class': 'content_date'}))
post_time = datetime.datetime(*map(int, re.findall(r'\d+', post_time_raw))[0:5])
update_time = datetime.datetime(*map(int, re.findall(r'\d+', post_time_raw))[5:12])


# get keywords
keyword_pool = soup.select('div[class=tag_for_item]')
keyword = [tag.text for tag in keyword_pool]



# get fb_like
fblike_url = 'https://www.facebook.com/v2.5/plugins/like.php?' + 'href=' + urllib.quote_plus(url.encode())
fblike_data = urllib2.urlopen(fblike_url)
soap = BeautifulSoup(fblike_data, 'html5lib')
fb_like_article = str(soap.select('div > span > span')[0])
fb_like = map(int, re.findall(r'\d+', fb_like_article))


# get category
category = soup.find('div', {'class': 'tag_for_category clearfix'}).text




# get comment
comment_url = 'https://graph.facebook.com/comments?id=' + url + '&filter=stream&fields=parent.fields(id),message,from,created_time,like_count&after=WTI5dGJXVnVkRjlqZAFhKemIzSTZAOall6TXpZAME5UQXdORE16TURNd09qRTBOVEkxTVRVMU9UTT0ZD%22'
comment_data = requests.get(comment_url).json()

top_comments = []
sub_comments = []

for info in comment_data['data']:

    c_actor = info['from']['name']
    c_like = info['like_count']
    c_dislike = 0
    c_content = info['message']
    c_source_type = 'fb'
    c_post_time = datetime.datetime(*map(int, re.findall(r'\d+', info['created_time'])))


    if not info.get('parent', False):
        top_comments.append(info)

    else:
        sub_comments.append(info)

for sub_comment in sub_comments:
    for top_comment in top_comments:
        if top_comment['from']['id'] == sub_comment['parent']['id'][0:15]:
            c_sub_comment = sub_comment



# get category url

def get_category_urls(category_url):

    count = 1
    main_url = 'http://newtalk.tw/news/category/' + str(count)
    while count < 6:
        return main_url
        count + 1

    cat_data = urllib2.urlopen(main_url)
    catsoup = BeautifulSoup(cat_data, 'html5lib')



    detail_urls = get_category_urls(category_url)

    return [detail_url, detail_url, detail_url]
