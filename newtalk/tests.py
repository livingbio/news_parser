import requests
import newtalk
from bs4 import BeautifulSoup


class FakeResponse():
    content = ''
    def __init__(self, content):
        self.content = content


def test_parser_page(url):

    url = 'http://newtalk.tw/news/view/2016-01-14/69148'
    data = urllib2.urlopen(url)
    soup = BeautifulSoup(data, 'html5lib')

    # 實作 MOCK
    # fake_response = FakeResponse(page_data)
    # old_requests = requests.get(url)
    # requests.get = fake_requests_get

    # def fake_requests_get(url):
    #     return fake_response

    page_data['url'] = str(soup.select('meta[property="og:url"]'))[16:60]
    result = parser_page(url)
    assert result == page_data['url'], "The {} of newtalk is not correct.".format('url')

    page_data['title'] = soup.find('div', {'class': 'content_title'}).text
    result = parser_page(title)
    assert result == page_data['title'], "The {} of newtalk is not correct.".format('title')

    parser_page[]
    result = parser_page(url)
    assert result == page_data['url'], "The {} of newtalk is not correct.".format('url')


    requests.get = old_requests


def test_get_category_urls():

    fake_response = FakeResponse(detail_urls)

    old_requests = requests.get
    requests.get = fake_requests_get


    google_urls = xxx

    result = get_catetgory_urls(google)

    assert result == google_urls, "..."

    yahoo_urls = yyy

    result = get_category_urls(yahoo)

    assert result == yahoo_urls, "..."


if __name__ == '__main__':
    test_parser_page()
    test_get_category_urls()
