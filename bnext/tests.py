"""
test.py
============================================
testing the correctness of:
	* bnext_parser.parser_page(url)
	* bnext_parser.get_category_urls(url)

link to bnext: http://www.bnext.com.tw/
============================================
"""


# -*- coding: utf-8 -*-

import bnext_parser
import pickle as pkl
import argparse
import os.path
import time
import sys


from requests import ConnectionError
from datetime import datetime
from random import randint

_RETRY_LIMIT = 3

category_url_list = ['http://www.bnext.com.tw/categories/internet/'\
					,'http://www.bnext.com.tw/categories/tech/'    \
					,'http://www.bnext.com.tw/categories/marketing/'\
					,'http://www.bnext.com.tw/categories/startup/' \
					,'http://www.bnext.com.tw/categories/people/'  \
					,'http://www.bnext.com.tw/categories/skill/']



# Uncomment to generate small testcase
# category_url_list = ['http://www.bnext.com.tw/categories/internet/']





# these are for generating testcases, you should never call this unless you are tsaiJN :)
# ========================================================================================
"""
 implementation:
  go through urls provided by generate_get_category_urls_testcase()
"""
def generate_parser_page_testcase(ground_input):
	generating_time = datetime.now()
	ground_truth = []

	for i, url in enumerate(ground_input):
		print('({}/{}) {}'.format(i+1, len(ground_input), url))
		retry = 0
		while retry < _RETRY_LIMIT:
			try:
				ret = bnext_parser.parser_page(url)
				ground_truth.append(ret)
				break
			except ConnectionError:
				retry += 1
				print('({}/{}) retrying...'.format(retry, _RETRY_LIMIT))
				time.sleep(randint(10, 15))

		time.sleep(randint(1, 3))

	with open('./resources/testcase/parser_page_testcase.pkl', 'w') as f:
		obj = {'ground_input': ground_input\
			  ,'ground_truth': ground_truth\
			  ,'generating_time': generating_time}

		pkl.dump(obj, f)






"""
 implementation:
  dense test last 3 page of each category, 40 url each
  most of the old news don't have keyword
"""

def generate_get_category_testcase(ground_input):
	generating_time = datetime.now()
	ground_truth = []

	for url in ground_input:
		ret = bnext_parser.get_category_urls(url, back_counting_offset=3)
		ground_truth.append(ret[-40:])

	obj = {'ground_input': ground_input\
		  ,'ground_truth': ground_truth\
		  ,'generating_time': generating_time}

	with open('./resources/testcase/get_category_urls_testcase.pkl', 'w') as f:
		pkl.dump(obj, f)

	return ground_truth




def generate_testcase_ensemble():
	global category_url_list

	# load category_urls ground truth if already have it
	if os.path.isfile('./resources/testcase/get_category_urls_testcase.pkl'):
		url_list = pkl.load(open('./resources/testcase/get_category_urls_testcase.pkl'))['ground_truth']
	else:
		url_list = generate_get_category_testcase(category_url_list)
	 
	# flatten url_list
	url_list = [url_list_3 for url_list_2 in url_list for url_list_3 in url_list_2]

	generate_parser_page_testcase(url_list)

# ========================================================================================





def print_time(obj):
	print('test_case generating time: ')
	print(obj['generating_time'])
	print('\n')
	return






def test_parser_page(test_file):

	print("\n================================== parser page ==============================================\n")
	print("Testing parser_page(), don't warry if you see some log on the fly,\n\
they are for the porpose of analyzing webpage, the fail of testing would be shown by [assert]\n")

	if os.path.isfile(test_file) == False:
		print("Error: can't find test_file: {}, please check filename or generate new test_file\n".format(test_file))
		return	

	f = open(test_file)
	obj = pkl.load(f)
	print_time(obj)

	ground_input = obj['ground_input']
	ground_truth = obj['ground_truth']

	for i, url in enumerate(ground_input):
		print('({}/{}) {}'.format(i+1, len(ground_input), url))
		retry = 0
		while retry < _RETRY_LIMIT:
			try:
				ret = bnext_parser.parser_page(url)
				break
			except ConnectionError:
				retry += 1
				print('({}/{}) retrying...'.format(retry, _RETRY_LIMIT))
				time.sleep(randint(10, 15))

		if ret != ground_truth[i]:
			print('test failed: {}\n'.format(url))
			return
		
		#time.sleep(randint(1, 3))

	print('\nSuccess')







def test_get_category_urls(test_file):
	print("\n================================== category urls ========================================\n")
	print("Testing get_category_urls(), don't warry if you see some log on the fly,\n\
they are for the porpose of analyzing webpage, the fail of testing would be shown by [assert]\n")

	if os.path.isfile(test_file) == False:
		print("Error: can't find test_file: {}, please check filename or generate new test_file\n".format(test_file))
		return

	f = open(test_file)
	obj = pkl.load(f)
	print_time(obj)

	ground_input = obj['ground_input']
	ground_truth = obj['ground_truth']

	for i, url in enumerate(ground_input):
		retry = 0
		while retry < _RETRY_LIMIT:
			try:
				ret = bnext_parser.get_category_urls(url, back_counting_offset=3)
				ret = ret[-40:]
				if ret != ground_truth[i]:
					print('test failed: {}\n'.format(url))
					return
				break
			except ConnectionError:
				retry += 1
				print('({}/{}) retrying...'.format(retry, _RETRY_LIMIT))
				time.sleep(randint(10, 15))

		sys.stdout.write('.')
		#time.sleep(1)

	print('\nSuccess')







def main():

	parser = argparse.ArgumentParser(description='Test if bnext_parser is working well')
	parser.add_argument(
		'--small',
		action='store_true',
		help='Test on small testcase (40 urls) instead of whole (240 urls)')
	parser.add_argument(
		'--gen',
		action='store_true',
		help='generate testcases instead of testing, the generated testcase will populate ./resources/testcase/* folder'
		)

	args = parser.parse_args()

	if args.gen:
		generate_testcase_ensemble()
		print("Done testcase generation.\n")
		return

	if args.small:
		test_parser_page('./resources/testcase/parser_page_testcase_small.pkl')
		test_get_category_urls('./resources/testcase/get_category_urls_testcase_small.pkl')

	else:
		test_parser_page('./resources/testcase/parser_page_testcase.pkl')
		test_get_category_urls('./resources/testcase/get_category_urls_testcase.pkl')

	print("Done testing.\n")
	return


if __name__ == '__main__':
	main()