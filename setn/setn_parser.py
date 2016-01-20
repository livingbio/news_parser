import datetime
import requests

from bs4 import BeautifulSoup


def get_category_urls(category_url, start_page='', limit=None):
    def catch_requests(url):
        count = 1
        while count < 4:
            try:
                return old_requests(url)
            except:
                print('Retrying({}/3)...'.format(count))
                count += 1
        raise

    old_requests = requests.get
    requests.get = catch_requests

    result = []
    count = 0
    page_url = category_url + '&p=' + str(start_page)
    while True:
        # print(page_url)
        soup = BeautifulSoup(requests.get(page_url).text, 'html.parser')
        urls = ['http://www.setn.com' +
                soup.select("ol a")[i].attrs['href'] for i in range(len(soup.select("ol a")))]
        result.extend(urls)
        next_link = soup.find_all("div", attrs={'class': 'pager'})[
            0].find_all('a')[-1]['href']
        if page_url == 'http://www.setn.com' + next_link or len(urls) == 0:
            break

        count += 1
        if limit != None and count >= limit:
            break

        page_url = 'http://www.setn.com' + next_link

    requests.get = old_requests
    return result


def parser_page(url):
    """
    parser page method 
    主要用於抓取新聞detail頁面資訊

    page_data = parser_page(news detail url)
    """
    def catch_requests(url):
        count = 1
        while count < 4:
            try:
                return old_requests(url)
            except:
                print('Retrying({}/3)...'.format(count))
                count += 1
        raise

    old_requests = requests.get
    requests.get = catch_requests

    soup = BeautifulSoup(requests.get(url).text, 'html.parser')
    search = lambda typ, seed: soup.find_all("meta", attrs={typ: seed})[
        0].attrs['content']
    inputs = [("property", "og:url"), ("property", "og:title"),
              ("name", "pubdate"), ("name", "Keywords"), ("name", "section")]

    parse = [search(typ, seed) for typ, seed in inputs]
    post_time = datetime.datetime.strptime(parse[2], '%Y-%m-%dT%H:%M:%S')

    article = soup.select("article div > p")
    content = []
    journalist = None
    for i in range(len(article)):
        if len(article[i].attrs) == 0 and not journalist:
            journalist = article[i].text
        else:
            content.append(article[i].text)
    content = "".join(content)

    fb_url = 'https://graph.facebook.com/fql?q=SELECT%20like_count,%20total_count,%20share_count,' + \
        '%20click_count,%20comment_count%20FROM%20link_stat%20WHERE%20url%20=%20%22' + \
        parse[0] + '%22'

    res_data = requests.get(fb_url).json()['data'][0]
    fb_like = res_data['like_count']
    fb_share = res_data['share_count']
    fb_com = res_data['comment_count']

    ######facebook comments#######
    tree = {}
    fb_com_url = 'http://graph.facebook.com/comments?id=' + parse[0] + \
                 '&limit=100&filter=stream&fields=parent.fields%28id%29,message,from,like_count,created_time,parent'
    fb_data = requests.get(fb_com_url).json()
    while True:
        if len(fb_data["data"]) == 0:
            break
        for comment in fb_data['data']:
            one_com = {}
            one_com["post_time"] = datetime.datetime.strptime(
                comment['created_time'][:-5], '%Y-%m-%dT%H:%M:%S')
            one_com["actor"] = comment['from']['name']
            one_com["like"] = comment['like_count']
            one_com["content"] = comment['message']
            one_com["source_type"] = "facebook"
            one_com["dislike"] = None
            if 'parent' in comment:
                tree[comment['parent']['id']]["sub_comments"].append(one_com)
            else:
                one_com["sub_comments"] = []
                tree[comment['id']] = one_com

        fb_next_url = fb_com_url + '&after=' + \
            fb_data['paging']['cursors']['after']
        fb_data = requests.get(fb_next_url).json()
    ######facebook comments#######
    requests.get = old_requests

    return {
        "url": parse[0],
        "source_press": None,
        "title": parse[1],
        "post_time": post_time,
        "journalist": journalist,
        "content": content,
        "compare": None,
        "keyword": parse[3].split(','),
        "fb_like": fb_like,
        "fb_share": fb_share,
        "fb_comment_count": fb_com,
        "category": parse[4].split(','),
        "comment": [tree[key] for key in sorted(tree.keys())]
    }


def main():
    url = 'http://www.setn.com/ViewAll.aspx?pagegroupid=5'
    urls = get_category_urls(url, 69)

    import numpy as np
    parse_content = [parser_page(urls[i]) for i in np.random.choice(
        len(urls), 10, replace=False)]
    print(parse_content)

if __name__ == '__main__':
    main()
