import requests
from bs4 import BeautifulSoup
import datetime

def parser_page(url):
    source_code = requests.get(url)
    plain_text = source_code.text
    soup = BeautifulSoup(plain_text, 'html.parser')

    url = url
    source_press = soup.select("div.indent ul li a")[0]['href']
    title = soup.find('h1', {'class': 'entry-title'}).string

    #____get time method 1
    post_time_string = soup.select("header.entry-header table td span.body")[1].string

    #____get time method 2
    # for i in soup.findAll('span', {'class': 'head'}):
    #     # import pdb; pdb.set_trace()
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


    # ans = soup.select("div.indent p")
    # print(ans[2])

    category = []
    for i in soup.select('li.menu-item-has-children'):
        category_title = i.contents[0]
        item = category_title.string
        category.append(item)

parser_page('http://technews.tw/2016/01/04/tiobe-2015-programming-language-index/')
# parser_page('http://technews.tw/2016/01/20/elon-musk-isnt-worried-about-an-apple-electric-car-it-will-expand-the-industry/')


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
