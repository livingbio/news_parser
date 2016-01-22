import requests
import newtalk

class FakeResponse():
    content = ''
    def __init__(self, content):
        self.content = content


def test_parser_page(url):

    fake_response = FakeResponse(page_data)


    old_requests = requests.get
    requests.get = fake_requests_get


    result = parser_page(url)

    assert result == page_data, "..."

    requests.get = old_requests


def test_get_category_urls():

    fake_response = FakeResponse(detail_urls)

    old_requests = requests.get
    requests.get = fake_requests_get

    result = get_catetgory_urls(url)

    assert result == detail_urls, "..."



if __name__ == '__main__':
    test_parser_page()
    test_get_category_urls()
