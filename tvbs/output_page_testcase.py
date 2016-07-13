import requests
import json
import datetime
import sys
import os
import tvbs_Parser


# ============= Get page url and make directory ============

url = sys.argv[1]    # e.g. http://news.tvbs.com.tw/politics/661869
dir = "./" + "_".join(url.split("/")[-2:])

if not os.path.exists(dir):
    os.makedirs(dir)
    
    
# =================== Output page request ===================

# ---------------------- page ----------------------

sourse_code_request = requests.get(url)
source_code = sourse_code_request.text.encode("utf-8")

hash_url = str(hash(url))
file = open(dir + "/" + hash_url, "w")
file.write(source_code)

# ------------------ fb_like_share -----------------

fb_url = "https://api.facebook.com/method/links.getStats?urls=" + url
fb_sourse_code_request = requests.get(fb_url)
fb_source_code = fb_sourse_code_request.text.encode("utf-8")

hash_fb_url = str(hash(fb_url))
fb_file = open(dir + "/" + hash_fb_url, "w")
fb_file.write(fb_source_code)


# ----------------------- fb_comment ------------------------
def make_fb_comments_dictionary(url):
    fb_comment_sourse_code = requests.get(url).text
    
    hash_fb_comment_url = str(hash(url))
    fb_comment_file = open(dir + "/" + hash_fb_comment_url, "w")
    fb_comment_file.write(fb_comment_sourse_code)
    
    fb_comment_sourse_code_dict = json.loads(fb_comment_sourse_code)
    if "next" in fb_comment_sourse_code_dict.get("paging", {}): # to check whether next page exist
        fb_next_page_url = "http://graph.facebook.com/comments?filter=stream&fields=from,like_count,message,created_time,id,parent.fields(id)&id=" + url + "&after=" + fb_comment_sourse_code_dict["paging"]["cursors"]["after"]
        make_fb_comments_dictionary(fb_next_page_url)
  
fb_comment_url = "http://graph.facebook.com/comments?filter=stream&fields=from,like_count,message,created_time,id,parent.fields(id)&id=" + url
make_fb_comments_dictionary(fb_comment_url)


# ==================== Output page answer ====================

file_name = "_".join(url.split("/")[-2:]) # e.g. category_newsID
answer_dic = tvbs_Parser.parser_page(url)

# ------------------ Handle post time ------------------
answer_dic["post_time"] = answer_dic["post_time"].strftime('%Y/%m/%d %H:%M')
for each_comment in answer_dic["comment"]:
    each_comment["post_time"] = each_comment["post_time"].strftime('%Y-%m-%dT%H:%M:%S+0000')
    
    if len(each_comment["sub_comments"]) != 0:
        for each_sub_comment in each_comment["sub_comments"]:
            each_sub_comment["post_time"] = each_sub_comment["post_time"].strftime('%Y-%m-%dT%H:%M:%S+0000')

output_file = open(dir + "/" + file_name + "_answer", "w")
output_file.write(json.dumps(answer_dic))

