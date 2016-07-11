# -*- coding: utf-8 -*-
import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup

############################parser_page(url)############################

def parser_page(url):
    resp = requests.get(url)
    soup = BeautifulSoup(resp.text.encode('iso8859-1').decode('utf-8'), 'html.parser')

    #for return
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

    str_url = url
    url = unicode(str_url, "utf-8") #turn into unicode

    try:
        source_press = soup.select('.datenews > a')[0]['href']
    except IndexError:
        source_press = None

    try:
        title_with_blank = soup.find('h1', {'class': 'newsbigtitle'}).text
        title = ' '.join(title_with_blank.split())
    except IndexError:
        title = None

    try:
        time_with_blank = soup.find('div', {'class': 'timebar'}).text
        time_no_blank = ' '.join(time_with_blank.split())              #delete blanks
        time = time_no_blank[:16]                                      #get time
        post_time = datetime.strptime(time, '%Y/%m/%d %H:%M')          #turn into type: datetime.datetime
    except IndexError:
        post_time = None

    #need more processing, contains things other than journalist's name
    try:
        journalist_with_blank = soup.find('div', {'class': 'timebar'}).text
        journalist_no_blank = ' '.join(journalist_with_blank.split())
        journalist = journalist_no_blank[17:]
    except IndexError:
        journalist = None

    #content is necessary
    content = ""
    content_list = soup.select('.newscontents > p')
    for i in range(len(content_list)):
        content += content_list[i].text

    #
    #pass getting "compare", since there's no "compare"
    #
    
    try:
        keyword = []
        key = soup.select('li > .newslistbar')
        for i in range(len(key)):
            keyword.append(key[i].text)
    except IndexError:
        keyword = None


    def fb_count_page(fb_url):
        count_page = requests.get('https://api.facebook.com/method/links.getStats?urls=' + fb_url)
        soup = BeautifulSoup(count_page.text, 'html.parser')
        fb_like = int(soup.find('like_count').string)
        fb_share = int(soup.find('share_count').string)
        return (fb_like, fb_share)

    fb_like, fb_share = fb_count_page(url)

    try:
        category = []
        cat = soup.select('.active')
        category.append(cat[2].text)
    except IndexError:
        pass

    #-------------------------------------------comments----------------------------------------------
    def fb_comment_page(fb_comment_url):
        comment_page = requests.get(fb_comment_url)
        comment_soup = BeautifulSoup(comment_page.text, 'html.parser')

        comment_string = str(comment_soup)
        comment_json_page = json.loads(comment_string)
        return comment_json_page

    def get_fb_comments(fb_comment_json):
        
        #for return
        comment_result = {
            "page_comments": None,
            "after": None,
        }
        page_comments = []
        after = ''

        try:
            for comment in fb_comment_json['data']:
                if 'parent' in comment.keys():
                    for each_comment in page_comments:
                        if each_comment['id'] == comment['parent']['id']:
                            each_sub_comment = {
                                'actor': comment['from']['name'],
                                'like': int(comment['like_count']),
                                'dislike': None,  #can't find 'dislike'
                                'message': comment['message'],
                                'post_time': datetime.strptime(comment['created_time'], '%Y-%m-%dT%H:%M:%S+0000'),
                                'source_type': 'facebook',
                            }
                            each_comment['sub_comments'].append(each_sub_comment)
                    
                else: #a comment without parent is not a sub_comment
                    each_comment = {
                        'id': comment['id'],
                        'actor': comment['from']['name'],
                        'like': int(comment['like_count']),
                        'dislike': None,  #can't find 'dislike'
                        'message': comment['message'],
                        'post_time': datetime.strptime(comment['created_time'], '%Y-%m-%dT%H:%M:%S+0000'),
                        'source_type': 'facebook',
                        'sub_comments': [],
                    }
                    page_comments.append(each_comment)

            #get 'after' 
            if "next" in fb_comment_json['paging'].keys():
                after = fb_comment_json['paging']['cursors']['after']
            else:
                after_url = ''

        except KeyError: #there's no comments
            pass

        comment_result['page_comments'] = page_comments
        comment_result['after'] = after
        return (comment_result)

    #start to get comments
    total_comments = []
    partial_url = 'http://graph.facebook.com/comments?filter=stream&fields=from,like_count,message,created_time,id,parent.fields(id)&id='
    fb_comment_url = partial_url + url                             #url for the first comment page
    fb_comment_json = fb_comment_page(fb_comment_url)              #get the first comment page
    comments_and_after = get_fb_comments(fb_comment_json)          #get comments and after
    
    while comments_and_after['after'] != '':                                    #page with next
        total_comments.extend(comments_and_after['page_comments'])              #first update total_comments
        after_url = partial_url + url + "&after=" + comments_and_after['after']
        fb_comment_json = fb_comment_page(after_url)
        comments_and_after = get_fb_comments(fb_comment_json)
    else:
        total_comments.extend(comments_and_after['page_comments'])
    #----------------------------------------------end comments-----------------------------------------

    result['url'] = url
    result['source_press'] = source_press
    result['title'] = title
    result['post_time'] = post_time
    result['journalist'] = journalist
    result['content'] = content
    result['compare'] = None
    result['keyword'] = keyword
    result['fb_like'] = fb_like
    result['fb_share'] = fb_share
    result['category'] = category
    result['comment'] = total_comments
    return(result)

"""
parser_result =  parser_page("http://news.cts.com.tw/cts/general/201605/201605281756574.html#.V4EdH7h942w")
for key in parser_result.keys():
    print key, ": ", parser_result[key]
"""

#############################get_category_urls(category_url)###########################

def get_category_urls(category_url):
    resp = requests.get(category_url)
    soup = BeautifulSoup(resp.text.encode('iso8859-1').decode('utf-8'), 'html.parser')

    detail_urls = [] #for return

    #for the first page
    news_type1 = soup.select('.news_right > a') #news without media
    for i in news_type1:
        news = i['href']
        detail_urls.append(news)
    news_type2 = soup.select('.block100 > a')   #news with media
    for i in news_type2:
        news = i['href']
        detail_urls.append(news)

    #get how many pages
    pages = soup.select('.btn')
    last_page = pages[len(pages) - 1]['href'][:-5] #delete ".html"
    index = last_page.index("index") + 5           #get the index of the page index
    pages = int(last_page[index:])
    
    #for the rest pages
    for i in range(2, pages + 1):
        length = len(".html#cat_list")
        page_url = category_url[:-length] + str(i) + ".html" #add page index and ".html"
        resp = requests.get(page_url)
        soup = BeautifulSoup(resp.text.encode('iso8859-1').decode('utf-8'), 'html.parser')

        news_type1 = soup.select('.news_right > a')
        for i in news_type1:
            news = i['href']
            detail_urls.append(news)
        news_type2 = soup.select('.block100 > a')
        for i in news_type2:
            news = i['href']
            detail_urls.append(news)
        
    return detail_urls

"""
get_category_urls("http://news.cts.com.tw/weather/index.html#cat_list")
print detail_urls
"""