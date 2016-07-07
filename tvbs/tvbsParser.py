from bs4 import BeautifulSoup
import requests
import datetime
import json

def parser_page(url):
    """Get information from tvbs news 
    
    Args: 
        url: tvbs news url
    Return:
        A dict contains information we want
    """

    # -------------- result dictionary --------------
    # this function will return this dictionary 
    # dictionary contains the info of given page
    # -----------------------------------------------
    result = {
        "url": None,
        "source_press": None,
        "title": None,
        "post_time": None,
        "journalist": None,
        "content": None,
        "compare": None,
        "keyword": None,
        "fb_like": None,
        "fb_share": None,
        "category": None,
        "comment": None,
        }
    
    # ----- get text from url page -----
    sourse_code = requests.get(url).text
    soup = BeautifulSoup(sourse_code, "html.parser")
#     print(sourse_code)
    
    # -------------- get result dict item --------------
    # use css selector to get result dict item 
    # --------------------------------------------------
    
    # ------------------- get url -------------------
    url = url
    
    # ------------------ get title ------------------
    try:
        title = soup.select(".reandr_title h2")[0].getText()
    except IndexError:
        title = None
#     print(title)  
    
    # ---------------- get journalist ----------------
    try:
        journalist = soup.select(".fontSize + p > a")[0].getText()
    except IndexError :
        journalist = None
#     print(journalist)
    
    # ----------------- get post_time -----------------
    try:
        post_time_naive = soup.select(".fontSize + p")[0].getText().split("導")[-1].strip()[0:16]
        post_time = datetime.datetime.strptime(post_time_naive, '%Y/%m/%d %H:%M')
    except (IndexError, ValueError) :
        post_time = None
#     print(post_time)
    
    # ------------------ get content ------------------
    content_naive = soup.select(".text_Message > p")
    content = ""
    for c in content_naive:
        content += c.getText()
#     print(content)    
        
    # ------------------ get keyword ------------------
    keywords = soup.select(".tag_box > h3 > a")
    keyword_list = []
    for k in keywords:
        keyword_list.append(k.getText())
#         print(k.getText())

    # ----------------- get category -----------------
    category = soup.select(".current")[0].getText()
#     print(category)
    
    
    # ----- get text from facebook request page (share/like) -----
    fb_sourse_code = requests.get("https://api.facebook.com/method/links.getStats?urls=" + url).text
    fb_soup = BeautifulSoup(fb_sourse_code, "html.parser")
    # ----------------- get fb_like -----------------
    try:
        fb_like = fb_soup.select("like_count")[0].getText()
    except KeyError:
        fb_like = None
#     print(fb_like)
    # ----------------- get fb_share -----------------   
    try:
        fb_share = fb_soup.select("share_count")[0].getText()
    except KeyError:
        fb_share = None
#     print(fb_share) 
  
    # ----- get text from facebook request page (comment) -----
    
    # -----------------  get fb comment -----------------
    # this method will return comment dict in one page  
    # ---------------------------------------------------
    total_comments = []
    def make_fb_comments_dictionary(fb_page_dict):
        page_comments = []
        try:  
            for comment in fb_page_dict["data"]:
                try:
                    if comment["parent"]["id"]:
                         for each_comment in total_comments:
                                if each_comment['id'] == comment['parent']['id']:
                                    add_sub_comment = {
                                        'id': comment['id'],
                                        'actor': comment['from']['name'],
                                        'like': int(comment['like_count']),
                                        'content': comment['message'],
                                        'post_time': datetime.datetime.strptime(comment['created_time'], '%Y-%m-%dT%H:%M:%S+0000'),
                                        'source_type': 'facebook',
                                    }
                                    each_comment['sub_comments'].append(add_sub_comment)
                except KeyError:
                    add_comment = {
                               'id': comment['id'],
                               'actor': comment['from']['name'],
                               'like': int(comment['like_count']),
                               'content': comment['message'],
                               'post_time': datetime.datetime.strptime(comment['created_time'], '%Y-%m-%dT%H:%M:%S+0000'),
                               'source_type': 'Facebook',
                               'sub_comments': [],
                               }    
                    page_comments.append(add_comment)
        except KeyError:
            pass
#         print(len(page_comments))
        return page_comments
    
    # ----------------------- fb_comment page one ------------------------
    fb_comment_sourse_code = requests.get("http://graph.facebook.com/comments?filter=stream&fields=from,like_count,message,created_time,id,parent.fields(id)&id=" + url).text
    fb_comment_sourse_code_dict = json.loads(fb_comment_sourse_code)
    
    total_comments.extend(make_fb_comments_dictionary(fb_comment_sourse_code_dict))
    
    # ----------------------- fb_comment other page ------------------------
    try:
        while fb_comment_sourse_code_dict["paging"]["next"]:
            fb_comment_sourse_code = requests.get("http://graph.facebook.com/comments?filter=stream&fields=from,like_count,message,created_time,id,parent.fields(id)&id=" + url + "&after=" + fb_comment_sourse_code_dict["paging"]["cursors"]["after"]).text
            fb_comment_sourse_code_dict = json.loads(fb_comment_sourse_code)
            
            total_comments.extend(make_fb_comments_dictionary(fb_comment_sourse_code_dict))
    except KeyError:
        pass
    
#     print(len(total_comments))
    
    
    
    # ----------------------- result ------------------------
    # get all the data above in a dictionary called result
    # return with {'key1': 'value1', 'key2': 'value2',...}
    # -------------------------------------------------------
    result['url'] = url
    result['title'] = title
    result['post_time'] = post_time
    result['journalist'] = journalist
    result['content'] = content
    result['keyword'] = keyword_list
    result['fb_like'] = fb_like
    result['fb_share'] = fb_share
    result['category'] = category
    result['comment'] = total_comments
    
#     print(result)
    return result
    
def get_category_urls(category_url):
    """Get all urls of tvbs news in certain category 
    
    Args: 
        category_url: tvbs news category url e.g. http://news.tvbs.com.tw/pets/
    Return:
        A list of all urls of tvbs news in certain category 
    """
    
    # -------------- urls list --------------
    # this function will return this list
    # list contains all news url of category 
    # ---------------------------------------
    detail_urls = []
    
    # ------- get text from url page ------
    source_code = requests.get(category_url).text
    soup = BeautifulSoup(source_code, 'html.parser')
#     print(source_code)

    # --------- get category name ---------
    try:
        category_name = category_url.split('/')[-2]
    except IndexError:
        pass
#     print(category_name)


    # -------- get first page list --------
    fpage_source_code = requests.get("http://news.tvbs.com.tw/opencms/system/modules/com.thesys.project.tvbs/pages/news/ajax-news-time-list.jsp?dataFolder=%2Fnews%2F" + category_name + "%2F").text
    fpage_soup = BeautifulSoup(fpage_source_code, 'html.parser')
    urls = fpage_soup.select("li > a")
    for url in urls:
        detail_urls.append(url["href"])
    
    pageNum = int(fpage_soup.select(".last")[0]["ref"])
#     print(pageNum)


    # -------- get other page list --------
    for i in range(2, pageNum + 1):
        opage_source_code = requests.get("http://news.tvbs.com.tw/opencms/system/modules/com.thesys.project.tvbs/pages/news/ajax-news-time-list.jsp?pageCount=" + str(pageNum) + "&dataFolder=%2Fnews%2F" + category_name + "%2F&pageIndex=" + str(i)).text
        opage_soup = BeautifulSoup(opage_source_code, 'html.parser')
        urls = opage_soup.select("li > a")
        for url in urls:
            detail_urls.append(url["href"])

#     print(len(detail_urls))
#     print(detail_urls)
    
    return detail_urls

# parser_page("http://news.tvbs.com.tw/pets/news-662016/")
# get_category_urls("http://news.tvbs.com.tw/pets/")
