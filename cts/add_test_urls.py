import requests
import os.path
import json
import time
import cts_parser
from bs4 import BeautifulSoup
from requests import Response

path = os.path.dirname(os.path.abspath(__file__))

def add_test_url(url):

    def add_to_test_urls(a_url):
        if '#cat_list' in url:
            test_urls_dic = {}
            with open(path + '/test_urls/get_category_urls') as f:
                for line in f:
                    (key, value) = line.split()
                    test_urls_dic[key] = value
                current_length = len(test_urls_dic)
            targetfile = open(path + '/test_urls/get_category_urls', 'a')
            targetfile.write("\n" + str(current_length) + " " + a_url)
            targetfile.close()
        else:
            test_urls_dic = {}
            with open(path + '/test_urls/parser_page') as f:
                for line in f:
                    (key, value) = line.split()
                    test_urls_dic[key] = value
                current_length = len(test_urls_dic)
            targetfile = open(path + '/test_urls/parser_page', 'a')
            targetfile.write("\n" + str(current_length) + " " + a_url)
            targetfile.close()
    """
    def add_to_url_dict(a_url):
        hashkey = hash(a_url)
        targetfile = open(path + '/url_dict', 'a')
        targetfile.write("\n" + a_url + " " + str(hashkey))
        targetfile.close()
    """
    def add_to_fake_pages(a_url):
        hashkey = hash(a_url)
        resp = requests.get(a_url)
        if resp.encoding == 'ISO-8859-1':
            content = resp.text.encode('ISO-8859-1')
        elif resp.encoding == 'UTF-8' or resp.encoding == 'utf-8':
            content = resp.text.encode('utf-8')
        a_dict = {str(hashkey): content}
        with open(path + '/fake_pages') as f:
            all_pages = json.load(f)
        all_pages.update(a_dict)
        with open(path + '/fake_pages', 'w') as f:
            json.dump(all_pages, f)
        

    ######## start to make fake pages #########
    #add_to_url_dict(url)
    add_to_test_urls(url)
    #------------- url for get_category_urls ----------------
    if '#cat_list' in url:
        add_to_fake_pages(url)

        #find how many pages
        page = 1
        while page < 2:
            try:
                resp = requests.get(url)
                content = resp.text.encode('ISO-8859-1')
                soup = BeautifulSoup(content.decode('utf-8'), 'html.parser')
                pages = soup.select('.btn')                    #the last page
                last_page = pages[len(pages) - 1]['href'][:-5] #delete ".html"
                index = last_page.index("index") + 5           #get the index of the page
                total = int(last_page[index:])
                page += 1
            except requests.ConnectionError:
                time.sleep(2)
                print "page with problem: ", page
                continue
        #for the rest category fake pages
        page = 2
        while page <= total:
            try:
                print page
                length = len(".html#cat_list")
                page_url = url[:-length] + str(page) + ".html" #add page index and ".html"
                #add_to_url_dict(page_url)
                add_to_fake_pages(page_url)
                page += 1
            except requests.ConnectionError:
                time.sleep(2)
                print "page with problem: ", page
                continue
    #---------------- urls for parser_page --------------------
    else:
        add_to_fake_pages(url)

        #create the fb_count fake page
        fb_count_url = 'https://api.facebook.com/method/links.getStats?urls=' + url
        #add_to_url_dict(fb_count_url)
        add_to_fake_pages(fb_count_url)

        #create the first fb_comments fake page
        partial_url = 'http://graph.facebook.com/comments?filter=stream&fields=from,like_count,message,created_time,id,parent.fields(id)&id='
        end_url_index = url.index("#")
        pure_url = url[:end_url_index]
        fb_comments_url = partial_url + pure_url
        #add_to_url_dict(fb_comments_url)
        add_to_fake_pages(fb_comments_url)

        #find whether there are more than one fb_comments page
        def get_fb_comments_after(fb_comments_url):
            resp = requests.get(fb_comments_url)
            content = resp.text.encode('utf-8')
            comment_soup = BeautifulSoup(content.decode('utf-8'), 'html.parser')
            comment_string = str(comment_soup)
            comment_json_page = json.loads(comment_string)
            if 'paging' in comment_json_page.keys():
                if "next" in comment_json_page['paging'].keys():
                    after = comment_json_page['paging']['cursors']['after']
                else:
                    after = ''
                return after
            else:
            	after = ''
            	return after

        #create the rest fb_comments page
        while get_fb_comments_after(fb_comments_url) != '':
            after_url = partial_url + pure_url + "&after=" + get_fb_comments_after(fb_comments_url)
            #add_to_url_dict(after_url)
            add_to_fake_pages(after_url)
            fb_comments_url = after_url
    
    
    targetfile = open(path + '/fake_pages', 'r')
    content = targetfile.read()
    targetfile.close()
    global fake_pages_dict
    fake_pages_dict = json.loads(content)

    def get_fake_request(url):
        global fake_pages_dict
        hashkey = hash(url)
        if str(hashkey) in fake_pages_dict.keys():
            fake_page = Response()
            fake_page_content = fake_pages_dict[str(hashkey)].encode('utf-8')
            fake_page._content = fake_page_content
            if "facebook" in url:
                fake_page.encoding = 'utf-8'
            else:
                fake_page.encoding = 'iso8859-1'
            return fake_page
        else:
            print "The url is not supported."

    def patch_request_get():
        global ori_requests_get
        ori_requests_get = requests.get
        requests.get = get_fake_request

    def unpatch_request_get():
        global ori_requests_get
        requests.get = ori_requests_get
    
    def add_to_target(a_url):
        patch_request_get()
        
        hashkey = hash(a_url)
        if '#cat_list' in url:
            target = cts_parser.get_category_urls(a_url)
        else:
            target = cts_parser.parser_page(a_url)
            #process the post-time
            def turn_datetime_to_string(post_time):
                post_time = post_time.strftime('%Y-%m-%dT%H:%M:%S')
                return post_time
            target["post_time"] = turn_datetime_to_string(target["post_time"])
            length = len(target["comment"])
            for i in range(length):
                target["comment"][i]["post_time"] = turn_datetime_to_string(target["comment"][i]["post_time"])
                length2 = len(target["comment"][i]["sub_comments"])
                for j in range(length2):
                    target["comment"][i]["sub_comments"][j]["post_time"] = turn_datetime_to_string(target["comment"][i]["sub_comments"][j]["post_time"])
        
        #add the answer to the target file
        a_dict = {str(hashkey): target}
        with open(path + '/target') as f:
            all_pages = json.load(f)
        all_pages.update(a_dict)
        with open(path + '/target', 'w') as f:
            json.dump(all_pages, f)
        
        unpatch_request_get()

    ######## start to add answers #########
    add_to_target(url)
    

#add_test_url("http://news.cts.com.tw/cts/general/201605/201605281756574.html#.V4EdH7h942w")
#add_test_url("http://news.cts.com.tw/cts/society/201606/201606071760311.html#.V4Rbxbh942w")
#add_test_url("http://news.cts.com.tw/nownews/money/201607/201607061770895.html#.V4Rca7h942x")
#add_test_url("http://news.cts.com.tw/weather/index.html#cat_list")
#add_test_url("http://news.cts.com.tw/society/index.html#cat_list")
#add_test_url("http://news.cts.com.tw/campus/index.html#cat_list")

#create a list of urls to be added
#for loop: call add_test_url