import requests
from bs4 import BeautifulSoup
import datetime
import json
from pytz import timezone, all_timezones

def parser_page(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')

    url = url
    # source_press = soup.select("div.indent ul li a")[0]['href']
    # source_press = soup.select("div.indent")[0].text
    # ans = source_press.encode('utf8')
    # print(ans)


    title = soup.find('h1', {'class': 'entry-title'}).string

    #____get time method 1
    post_time_string = soup.select("header.entry-header table td span.body")[1].string

    #____get time method 2
    # for i in soup.findAll('span', {'class': 'head'}):
    #     if i.string == '發布日期':
    #         post_time_string = i.next_sibling.next_sibling.string
    post_time = datetime.datetime.strptime(post_time_string, '%Y 年 %m 月 %d 日 %H:%M ')

    journalist = soup.find('a', {'rel': 'author'}).string

    content =""
    #____get content method 1
    content_source_code = soup.select("div.indent p")
    for i in content_source_code:
        content += i.text

    #____get content method 2
    # for i in soup.findAll('div', {'class': 'indent'}):
    #     for m in i.findAll('p'):
    #         content += m.text

    category = []
    for i in soup.select('li.menu-item-has-children'):
        category_title = i.contents[0]
        item = category_title.string
        category.append(item)


    def fb_plugin_count_page(url):
        code = requests.get('http://api.facebook.com/restserver.php?method=links.getStats&urls=' + url)
        html_text = code.text
        fb_plugin_page_soup = BeautifulSoup(html_text, 'html.parser')

        fb_like_count = fb_plugin_page_soup.find('total_count').string
        fb_share_count = fb_plugin_page_soup.find('share_count').string
        return(fb_like_count, fb_share_count)


    fb_like, fb_share = fb_plugin_count_page(url)


    def fb_plugin_comment_page(url):
        code = requests.get('http://graph.facebook.com/comments?id=' + url)
        html_text = code.text
        fb_plugin_page_soup = BeautifulSoup(html_text, 'html.parser')
        fb_comments_string = str(fb_plugin_page_soup)
        fb_comments_json_page = json.loads(fb_comments_string)
        return (fb_comments_json_page)


    fb_comments_json = fb_plugin_comment_page(url)


    total_comments = []
    for comment in fb_comments_json['data']:
        comment_time_in_US = datetime.datetime.strptime(comment['created_time'], '%Y-%m-%dT%H:%M:%S%z')
        comment_time_in_TW = comment_time_in_US.astimezone(timezone('ROC'))

        each_comment = {
            'actor': comment['from']['name'],
            'like': comment['like_count'],
            'content': comment['message'],
            'post_time': comment_time_in_TW,
            'source_type': 'facebook',
            'sub_comments':[],
        }
        total_comments.append(each_comment)

    print(total_comments)

# parser_page('http://technews.tw/2016/01/04/tiobe-2015-programming-language-index/')
parser_page('http://technews.tw/2016/01/06/iphone-6s-no-good-apple/')


def get_category_urls(category_url):
    source_code = requests.get(category_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    detail_url = []
    for i in soup.findAll('h1', {'class': 'entry-title'}):
        detail_url.append(i.a.attrs['href'])
    return(detail_url)

# get_category_urls('http://technews.tw/category/tablet/')
