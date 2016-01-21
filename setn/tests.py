import requests
import pickle
import datetime
import unittest

from mock import patch
from bs4 import BeautifulSoup
from setn_parser import get_category_urls, parser_page


class TestParser(unittest.TestCase):

    def setUp(self):
        with open('./setn/resources/resps.pickle', 'rb') as f:
            self.resps = pickle.load(f)
        with open('./setn/resources/target.pickle', 'rb') as f:
            self.data = pickle.load(f)
        self.categories = [2, 4, 5, 6, 7, 8, 9, 15, 17, 18, 19, 31, 34, 41, 42]
        self.test_num = 40

    def test_parser_page(self):
        print('\n==================testing parser page====================\n')
        with patch.object(requests, 'get') as mock_method:
            mock_method.side_effect = lambda url: self.resps[url]

            count = 1
            total = len(self.categories)*self.test_num
            result = {}
            target = {}
            for gid in self.categories:
                result[gid] = []
                for page_url in self.data[0][gid][-self.test_num:]:
                    result[gid].append(parser_page(page_url))
                    print("({0}/{1}) parsing: {2}".format(
                        count, total, page_url))
                    count += 1
                target[gid] = self.data[1][gid][-self.test_num:]

            self.assertEqual(result, target)
        print("Test case generated time:", self.data[2], "\nDone testing.")

    def find_start_url(self, category_url, min_step=3, init=32):
        step = init
        now = 1 + int(init / 2)
        page_url = category_url + '&p=' + str(now)

        while True:
            soup = BeautifulSoup(requests.get(page_url).text, 'html.parser')
            num_urls = len(soup.select("ol a"))

            if step/2 <= min_step:
                break

            step = int(step / 2) if num_urls == 0 or step != init else init
            now = now - step if num_urls == 0 else now + step
            page_url = category_url + '&p=' + str(now)

        ans = (now - step - 2) if num_urls == 0 else now - 2
        return 1 if ans < 1 else ans

    def test_get_category_urls(self):
        print('\n===============testing get category urls=================\n')
        with patch.object(requests, 'get') as mock_method:
            mock_method.side_effect = lambda url: self.resps[url]

            count = 1
            total = len(self.categories)
            result = {}
            target = {}

            for gid in self.categories:
                url = 'http://www.setn.com/ViewAll.aspx?PageGroupID='+str(gid)
                urls = get_category_urls(url, self.find_start_url(url))
                result[gid] = urls[-self.test_num:]
                target[gid] = self.data[0][gid][-self.test_num:]
                print("({0}/{1}) parsing: {2}".format(count, total, url))
                count += 1

            self.assertTrue(result, target)
        print("Test case generated time:", self.data[2], "\nDone testing.")


if __name__ == '__main__':

    alltests = unittest.TestSuite()
    alltests.addTest(unittest.makeSuite(TestParser))
    result = unittest.TextTestRunner(verbosity=2).run(alltests)
