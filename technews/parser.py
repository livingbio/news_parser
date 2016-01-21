import requests
from bs4 import BeautifulSoup
import datetime

def parser_page(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    # print (soup.prettify().encode('utf-8'))
    url = url
    title = soup.find('h1', {'class': 'entry-title'}).string
    journalist = soup.find('a', {'rel': 'author'}).string
    category = []
    for i in soup.findAll('li', {'class': 'menu-item-has-children'}):
        attr = i.contents[0]
        item = attr.string
        category.append(item)

    # print(category)

    for i in soup.findAll('div', {'class': 'indent'}):
        for m in i.findAll('p'):
            print(m.string)

    # comment = soup.find('div', {'class': 'clearfix'})

    # for i in soup.findAll('span', {'class': 'head'}):
    #     if i.string == '發布日期':
    #         target = i.next_sibling
    #         print(target)

    # fb_like = soup.find('span', {'class': 'pluginCountTextDisconnected'}).string

parser_page('http://technews.tw/2016/01/04/tiobe-2015-programming-language-index/')


def get_category_urls(category_url):
    source_code = requests.get(category_url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')
    detail_url = []
    for i in soup.findAll('h1', {'class': 'entry-title'}):
        detail_url.append(i.a.attrs['href'])
    return(detail_url)

# get_category_urls('http://technews.tw/category/tablet/')


# def crawling(max_pages):
#     page = 20106
#     while page <= max_pages:
#         url = 'https://www.thenewboston.com/videos.php?cat=98&video=' + str(page)
#         source_code = requests.get(url)
#         plain_text = source_code.text
#         soup = BeautifulSoup(plain_text, 'html.parser')
#         # print (soup.prettify())
#         for i in soup.findAll('span', {'class': 'text-bold' } ):
#             title = i.string
#             print(title)
#
#         page += 1
#
#     print('---done---')
#
# crawling(20106+5)
