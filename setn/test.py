import requests
import pickle
import datetime
import time

from argparse import ArgumentParser
from bs4 import BeautifulSoup
from setn_parser import get_category_urls, parser_page


categories = [2, 4, 5, 6, 7, 8, 9, 15, 17, 18, 19, 31, 34, 41, 42]
parser = ArgumentParser()
parser.add_argument('--categories', type=list, default=categories,
                    help='Categories to test, available: 2,4,5,6,7,8,9,15,17,18,19,31,34,41,42.')
parser.add_argument('--num', type=int, default=40,
                    help='Number of pages to test, max: 40')

args = parser.parse_args()
cats = args.categories
test_num = args.num
test_categ = list(map(lambda x: int(x), cats[::2])) if type(
    cats[0]) == str else cats


with open('target.pickle', 'rb') as f:
    data = pickle.load(f)

with open('resps.pickle', 'rb') as f:
    resps = pickle.load(f)


def test_requests(url):
    return resps[url]


def find_start_url(category_url, min_step=3, init=32):
    step = init
    now = 1 + int(init / 2)
    page_url = category_url + '&p=' + str(now)
    while True:
        soup = BeautifulSoup(requests.get(page_url).text, 'html.parser')
        num_urls = len(soup.select("ol a"))
        if step / 2 <= min_step:
            break

        if num_urls == 0:
            step = int(step / 2)
            now -= step
        else:
            step = int(step / 2) if step != init else init
            now += step

        page_url = category_url + '&p=' + str(now)

    ans = now - step - 2 if num_urls == 0 else now - 2
    return 1 if ans < 1 else ans


def test_parser_page(group_id, N):
    old_req = requests.get
    requests.get = test_requests

    count = 1
    total = len(group_id) * N
    result = {}
    target = {}
    for gid in group_id:
        result[gid] = []
        for page_url in data[0][gid][-N:]:
            result[gid].append(parser_page(page_url))
            print("({0}/{1}) parsing: {2}".format(count, total, page_url))
            count += 1
        target[gid] = data[1][gid][-N:]

    requests.get = old_req
    assert result == target, "test failed."


def test_get_category_urls(group_id, N):
    old_req = requests.get
    requests.get = test_requests

    count = 1
    total = len(group_id)
    result = {}
    target = {}
    for gid in group_id:
        url = 'http://www.setn.com/ViewAll.aspx?PageGroupID=' + str(gid)
        result[gid] = get_category_urls(url, find_start_url(url))[-N:]
        target[gid] = data[0][gid][-N:]
        print("({0}/{1}) parsing: {2}".format(count, total, url))
        count += 1

    requests.get = old_req
    assert result == target, "test failed."
    print('get-category-urls verified.')


def main():
    print("Test case generated time:", data[2], "\nStart testing...")
    print('===================testing parser page========================')
    start_time = time.clock()
    test_parser_page(test_categ, test_num)
    print('Done testing parser-page, using %.4f seconds.' %
          (time.clock() - start_time))

    print('================testing get category urls=====================')
    start_time = time.clock()
    test_get_category_urls(test_categ, test_num)
    print('Done testing get-category-urls, using %.4f seconds.' %
          (time.clock() - start_time))
    print("Test case generated time:", data[2], "\nDone testing.")

if __name__ == '__main__':
    main()
