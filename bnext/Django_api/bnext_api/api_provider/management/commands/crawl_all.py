from django.core.management.base import BaseCommand, CommandError
from random import randint

import datetime
import time

from _bnext_parser import get_category_urls, parser_page
from requests import ConnectionError
from api_provider.models import Article, Comment, SubComment

_RETRY_LIMIT = 3

category_url_list = ['http://www.bnext.com.tw/categories/internet/',
                     'http://www.bnext.com.tw/categories/tech/',
                     'http://www.bnext.com.tw/categories/marketing/',
                     'http://www.bnext.com.tw/categories/startup/',
                     'http://www.bnext.com.tw/categories/people/',
                     'http://www.bnext.com.tw/categories/skill/']

category_name = ['internet', 'technology', 'marketing', 'startup', 'people', 'skill']

def parser_page_with_retry(url):
    retry = 0
    while retry < _RETRY_LIMIT:
        try:
            page_info = parser_page(url)
            break
        except ConnectionError:
            retry += 1
            print('({}/{}) retrying...'.format(retry, _RETRY_LIMIT))
            time.sleep(randint(10, 15))

            assert retry < _RETRY_LIMIT, 'maximum retry reached'
    return page_info



def get_category_urls_with_retry(url, page):
    retry = 0
    while retry < _RETRY_LIMIT:
        try:
            url_list = get_category_urls(url, straight_counting_offset=page)
            break
        except ConnectionError:
            retry += 1
            print('({}/{}) retrying...'.format(retry, _RETRY_LIMIT))
            time.sleep(randint(10, 15))

            assert retry < _RETRY_LIMIT, 'maximum retry reached'
    return url_list


class Command(BaseCommand):
    help = 'Crawl all posts in the website: http://www.bnext.com.tw/'

    def add_arguments(self, parser):
        parser.add_argument(
            '--page',
            type=int,
            default=0,
            help='Specify the amount of page in a category you want to crawl. Default: all'
        )
        parser.add_argument(
            '--category',
            type=int,
            nargs='+',
            default=[0,1,2,3,4,5],
            help=''.join([
                "Specify which categories you wish to crawl.\n",
                '0: internet\n',
                '1: technology\n',
                '2: marketing\n',
                '3: startup\n',
                '4: people\n',
                '5: skill\n',
                'sample input: 1 2 3 4\n',
                'default: 0 1 2 3 4 5'
            ])
        )

    def handle(self, *args, **options):

        category_list = options['category']

        if max(category_list) > len(category_name):
            self.stdout.write('category not valid.\n')
            return

        for category in category_list:
            self.stdout.write('\nCrawling category {}...\n'.format(category))
            url_list = get_category_urls_with_retry(category_url_list[category], options['page'])
            
            for i, url in enumerate(url_list):
                self.stdout.write('({}/{}) {}\n'.format(i+1, len(url_list), url))
                page_info = parser_page_with_retry(url)

                article = Article(
                        category    = category_name[category],
                        url         = page_info['url'],
                        title       = page_info['title'],
                        post_time   = page_info['post_time'],
                        journalist  = page_info['journalist'],
                        content     = page_info['content'],
                        keywords    = ','.join(page_info['keyword']),
                        fb_like     = page_info['fb_like'],
                        fb_share    = page_info['fb_share']
                    )
                article.save()

                for comment in page_info['comment']:
                    comment_object = article.comment_set.create(
                                    content     = comment['content'],
                                    actor       = comment['actor'],
                                    fb_like     = comment['like'],
                                    post_time   = comment['post_time'],
                                    source_type = comment['source_type']
                                )
                    for subcomment in comment['sub_comments']:
                        subcomment_object = comment_object.subcomment_set.create(
                                    content = subcomment['content'],
                                    actor = subcomment['actor'],
                                    fb_like = subcomment['like'],
                                    post_time = subcomment['post_time'],
                                    source_type = subcomment['source_type']
                            )



