import requests
import json
import sys
import tvbs_Parser
import sqlite3

# ======== Establish db connection and get page url ========

conn = sqlite3.connect('TestCase.db')
conn.text_factory = str
  
url = sys.argv[1]  # e.g. "http://news.tvbs.com.tw/politics/661869"
    
# ========= Handle request and store response in db =========
  
# ---------------------- page ----------------------
  
sourse_code_request = requests.get(url)
source_code = sourse_code_request.text.encode("utf-8")
  
hash_url = str(hash(url))
conn.execute("insert into ResponseList (NAME, RESULT, ORIGIN) values (?,?,?)", (hash_url , source_code, url)) 
  
# ------------------ fb_like_share -----------------
  
fb_url = "https://api.facebook.com/method/links.getStats?urls=" + url
fb_sourse_code_request = requests.get(fb_url)
fb_source_code = fb_sourse_code_request.text.encode("utf-8")
  
hash_fb_url = str(hash(fb_url))
conn.execute("insert into ResponseList (NAME, RESULT, ORIGIN) values (?,?,?)", (hash_fb_url , fb_source_code, url))
  
# ----------------------- fb_comment ------------------------

def make_fb_comments_dictionary(url):
    fb_comment_sourse_code = requests.get(url).text.encode("utf-8")
      
    hash_fb_comment_url = str(hash(url))
    conn.execute("insert into ResponseList (NAME, RESULT, ORIGIN) values (?,?,?)", (hash_fb_comment_url , fb_comment_sourse_code, url))

      
    fb_comment_sourse_code_dict = json.loads(fb_comment_sourse_code)
    if "next" in fb_comment_sourse_code_dict.get("paging", {}):  # to check whether next page exist
        fb_next_page_url = "http://graph.facebook.com/comments?filter=stream&fields=from,like_count,message,created_time,id,parent.fields(id)&id=" + url + "&after=" + fb_comment_sourse_code_dict["paging"]["cursors"]["after"]
        make_fb_comments_dictionary(fb_next_page_url)
    
fb_comment_url = "http://graph.facebook.com/comments?filter=stream&fields=from,like_count,message,created_time,id,parent.fields(id)&id=" + url
make_fb_comments_dictionary(fb_comment_url)
  
  
# ==================== Store page answer ====================
  
answer_dic = tvbs_Parser.parser_page(url)
  
# ------------------ Handle post time ------------------
answer_dic["post_time"] = answer_dic["post_time"].strftime('%Y/%m/%d %H:%M')
for each_comment in answer_dic["comment"]:
    each_comment["post_time"] = each_comment["post_time"].strftime('%Y-%m-%dT%H:%M:%S+0000')
      
    if len(each_comment["sub_comments"]) != 0:
        for each_sub_comment in each_comment["sub_comments"]:
            each_sub_comment["post_time"] = each_sub_comment["post_time"].strftime('%Y-%m-%dT%H:%M:%S+0000')
  
conn.execute("insert into ResponseList (NAME, RESULT, ORIGIN) values (?,?,?)", (hash_url + "_answer" , json.dumps(answer_dic), url))


# ======== Commit change of db and add testcase list ========

conn.execute("insert into PageList (NAME) values (?)", (url,))

conn.commit()
conn.close()
