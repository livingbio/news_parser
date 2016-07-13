import requests
import os.path
import cts_parser

path = os.path.dirname(os.path.abspath(__file__))

######################## Add an url and a target for testing get_category_urls ######################
def add_category_url(url):
    test_urls_dic = {}
    with open(path + '/tests/get_category_urls/test_urls') as f:
        for line in f:
           (key, value) = line.split()
           test_urls_dic[key] = value
    current_length = len(test_urls_dic)
    #add a new url for testing get_category_urls
    targetfile = open(path + '/tests/get_category_urls/test_urls', 'a')
    targetfile.write("\n" + str(current_length + 1) + " " + url)
    targetfile.close()
    print "Add a new url for testing get_category_urls"

#add the target of get_category_urls
def add_test_data_for_category(url):
	answer = cts_parser.get_category_urls(url)
	targetfile = open(path + '/tests/get_category_urls/test_data', 'a')
	targetfile.write(url + ":")
	for i in range(len(answer) - 1):
		targetfile.write(str(answer[i]) + ',')
	targetfile.write(str(answer[len(answer) - 1]))
	targetfile.write(";")
	targetfile.close()
	print "Add a new target for testing get_category_urls"

########################### Add an url and a target for testing parser_page #######################
def add_page_url(url):
    test_urls_dic = {}
    with open(path + '/tests/parser_page/test_urls') as f:
        for line in f:
           (key, value) = line.split()
           test_urls_dic[key] = value
    current_length = len(test_urls_dic)
    #add a new url for testing get_category_urls
    targetfile = open(path + '/tests/parser_page/test_urls', 'a')
    targetfile.write("\n" + str(current_length + 1) + " " + url)
    targetfile.close()
    print "Add a new url for testing parser_page"

#add the target of parser_page