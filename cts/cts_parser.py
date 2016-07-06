import requests
import json
from datetime import datetime
from bs4 import BeautifulSoup

def parser_page(url):
    res = requests.get(url)
    soup = BeautifulSoup(res.text, 'html.parser')

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


    url = url

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
        tj_with_blank = soup.find('div', {'class': 'timebar'}).text
        time_and_journalist = ' '.join(tj_with_blank.split())
        
        time = time_and_journalist[:16]
        post_time = datetime.strptime(time, '%Y/%m/%d %H:%M')
        slash = time_and_journalist.index("/")
        journalist = time_and_journalist[17:]
    except IndexError:
        post_time = None
        journalist = None

    try:
        content = ""
        con = soup.select('div > p')
        for i in range(1, len(con)):
            content += con[i].text
    except IndexError:
        content = None

    #"compare": string

    try:
        keyword = []
        key = soup.select('li > .newslistbar')
        for i in range(len(key)):
            keyword.append(key[i].text)
    except IndexError:
        keyword = None

    def fb_count_page(fb_count_url):
        count_page = requests.get('https://api.facebook.com/method/links.getStats?urls=' + url)
        count_soup = BeautifulSoup(count_page.text, 'html.parser')
        fb_like = int(count_soup.find('total_count').string)
        fb_share = int(count_soup.find('share_count').string)
        return (fb_like, fb_share)

    fb_like, fb_share = fb_count_page(url)

    try:
        category = []
        cat = soup.select('.active')
        category.append(cat[2].text)
    except IndexError:
        pass
    
    #comment
    total_comments = []

    def fb_comment_page(fb_comment_url):
        comment_page = requests.get(fb_comment_url)
        comment_soup = BeautifulSoup(comment_page.text, 'html.parser')

        comment_string = str(comment_soup)
        comment_json_page = json.loads(comment_string)
        return comment_json_page

    after_url = ''
    def create_comment_dictionary(fb_comment_json):
        try:
            for comment in fb_comment_json['data']:
                try:
                    if comment['parent']['id']:
                        for each_comment in total_comments:
                            if each_comment['id'] == comment['parent']['id']:
                                each_sub_comment = {
                                    'actor': comment['from']['name'],
                                    'like': int(comment['like_count']),
                                    'dislike': None,
                                    'message': comment['message'],
                                    'post_time': datetime.strptime(comment['created_time'], '%Y-%m-%dT%H:%M:%S+0000'),
                                    'source_type': 'facebook',
                                }
                                each_comment['sub_comments'].append(each_sub_comment)

                except KeyError:
                    each_comment = {
                        'id': comment['id'],
                        'actor': comment['from']['name'],
                        'like': int(comment['like_count']),
                        'dislike': None,
                        'message': comment['message'],
                        'post_time': datetime.strptime(comment['created_time'], '%Y-%m-%dT%H:%M:%S+0000'),
                        'source_type': 'facebook',
                        'sub_comments': [],
                    }
                    total_comments.append(each_comment)
        
            if "next" in fb_comment_json['paging']:
                after = fb_comment_json['paging']['cursors']['after']
                global after_url
                after_url = 'http://graph.facebook.com/comments?filter=stream&fields=from,like_count,message,created_time,id,parent.fields(id)&id=' + url + "&after=" + after
            else:    
                global after_url
                after_url = ''

        except KeyError: #no comment
            pass
        return total_comments

    #for page 1
    comment_url = 'http://graph.facebook.com/comments?filter=stream&fields=from,like_count,message,created_time,id,parent.fields(id)&id=' + url
    fb_comment_json = fb_comment_page(comment_url)
    create_comment_dictionary(fb_comment_json)

    #for the rest pages
    while after_url != '':
        fb_comment_json_after = fb_comment_page(after_url)
        create_comment_dictionary(fb_comment_json_after)

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

  
def get_category_urls(category_url):
    res = requests.get(category_url)
    soup = BeautifulSoup(res.text, 'html.parser')

    detail_urls = [] #for return

    #the first page
    news_type1 = soup.select('.news_right > a')
    for i in news_type1:
        news = i['href']
        detail_urls.append(news)
    news_type2 = soup.select('.block100 > a')
    for i in news_type2:
        news = i['href']
        detail_urls.append(news)

    #get how many pages
    pages = soup.select('.btn')
    num = pages[len(pages) - 1]['href'][:-5]
    index = num.index("index") + 5
    num = int(num[index:])

    #the rest pages
    for i in range(2, num + 1):
        new_url = category_url[:-5] + str(i) + ".html"
        res = requests.get(category_url)
        soup = BeautifulSoup(res.text, 'html.parser')

        news_type1 = soup.select('.news_right > a')
        for i in news_type1:
            news = i['href']
            detail_urls.append(news)
        news_type2 = soup.select('.block100 > a')
        for i in news_type2:
            news = i['href']
            detail_urls.append(news)
        
    return detail_urls