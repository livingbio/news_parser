# -*- coding: utf-8 -*-
import technews_parser
import json
import requests
import pickle
import os.path

the_path_of_this_file = os.path.dirname(os.path.abspath(__file__))
print(__file__)
print('**************' + the_path_of_this_file)


def test_parser_page():
    url = 'test'
    result = technews_parser.parser_page(url)
    # assert result == target, 'target error {} != {}'.format(result, target)

    targetfile_read = open(the_path_of_this_file + '/pickle/parser_page/parser_page_pickle', 'r')
    parser_page_target= pickle.load(targetfile_read)

    for i in parser_page_target:
        assert result[i] == parser_page_target[i], i + ' field has error: {} != {}'.format(result[i], parser_page_target[i])

    # print(result['journalist'])
    # print(parser_page_target['journalist'])
    print('done test_parser_page')

# test_parser_page()



def test_get_category_urls():
    url = 'test'
    result = technews_parser.get_category_urls(url)

    targetfile_read = open(the_path_of_this_file + '/pickle/get_category_urls/get_category_urls_pickle', 'r')
    target= pickle.load(targetfile_read)

    for i in range(len(result)):
        assert result[i] == target[i], 'get_category_urls function has error at the result and target\'s list[' + str(i) + '] : {} != {}'.format(result[i], target[i])

    # print(target[3])
    # print(result[3])
    print('done test_get_category_urls')

# test_get_category_urls()


if __name__ == '__main__':
    test_parser_page()
    test_get_category_urls()
