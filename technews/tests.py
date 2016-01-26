# -*- coding: utf-8 -*-
import technews_parser
# import requests
# from bs4 import BeautifulSoup

def test_parser_page(url):
    result = technews_parser.parser_page(url)
    # assert result == target, 'target error {} != {}'.format(result, target)



    assert result['url'] == input_url, 'url error {} != {}'.format(result['url'], input_url)
    assert result['source_press'] == input_source_press, 'source_press error {} != {}'.format(result['source_press'], input_source_press)
    assert result['title'] == input_title, 'title error {} != {}'.format(result['title'], input_title)
    assert result['post_time'] == input_post_time, 'post_time error {} != {}'.format(result['post_time'], input_post_time)
    assert result['journalist'] == input_journalist, 'journalist error {} != {}'.format(result['journalist'], input_journalist)
    assert result['content'] == input_content, 'content error {} != {}'.format(result['content'], input_content)
    assert result['keyword'] == input_keyword, 'keyword error {} != {}'.format(result['keyword'], input_keyword)
    assert result['fb_like'] == input_fb_like, 'fb_like error {} != {}'.format(result['fb_like'], input_fb_like)
    assert result['fb_share'] == input_fb_share, 'fb_share error {} != {}'.format(result['fb_share'], input_fb_share)
    assert result['category'] == input_category, 'category error {} != {}'.format(result['category'], input_category)
    assert result['comment'] == input_comment, 'comment error {} != {}'.format(result['comment'], input_comment)


    page_data['title'] = soup.find('div', {'class': 'content_title'}).text
    result = parser_page(title)
    assert result == page_data['title'], "The {} of newtalk is not correct.".format('title')
    return(result)

test_result = test_parser_page('http://technews.tw/2015/11/26/apple-iphone-2018-oled-﻿panel/')
print(test_result)

# page_data = parser_page('http://technews.tw/2016/01/04/tiobe-2015-programming-language-index/')
# page_data = parser_page('http://technews.tw/2016/01/06/iphone-6s-no-good-apple/')
# page_data = parser_page('http://technews.tw/2015/11/26/apple-iphone-2018-oled-﻿panel/')
