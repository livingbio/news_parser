import requests
from bs4 import BeautifulSoup
import HTMLParser
import time
from datetime import datetime
from random import randint

strange_url_set = set()

def parser_page(url):
	global strange_url_set

	page_info = {'url'			: url  \
				,'source_press'	: None \
				,'title'		: None \
				,'post_time'	: None \
				,'journalist'	: None \
				,'content' 		: None \
				,'compare' 		: None \
				,'keyword' 		: None \
				,'fb_like' 		: None \
				,'fb_share' 	: None \
				,'category'		: None }

	res  = requests.get(url)
	soup = BeautifulSoup(res.content)

# --------------------- missing info ------------------------
# source_press
# popularity
# compare
# category
# -----------------------------------------------------------


# --------------------- title -------------------------------
# <div class="main_title">2015全球PC出貨持續衰退，Apple一枝獨秀成長5.8%</div>
# -----------------------------------------------------------
	title = soup.findAll('div', {'class':'main_title'})
	if len(title) > 1:
		print('[title] multiple title:  {}\n'.format(url))
		strange_url_set.add(url)
	elif len(title) == 0:
		print('[title] title not found: {}\n'.format(url))
		strange_url_set.add(url)
	
	title = title[0].text
	page_info['title'] = title



# --------------- author & post time ------------------------
# <div class="info_box">
# 		<span  class="info"> 撰文者: XXX    </span>
# 		<span  class="info"> 發表日期: XXX  </span>
# </div>
# -----------------------------------------------------------
	info_box = soup.findAll('div', {'class': 'info_box'})
	if len(info_box) == 2:
		author    = info_box[0].text
		post_time = info_box[1].text

		if ':' in author:
			author = author.split(':')[1]
		if '：' in author:
			author = author.split('：')[1]
		page_info['journalist'] = author

		if ':' in post_time:
			post_time = post_time.split(':')[1]
		if '：' in post_time:
			post_time = post_time.split('：')[1]

		try:
			date = datetime.strptime(post_time, '%Y/%m/%d')
			page_info['post_time'] = date
		except ValueError:
			print('[time] wrong format of time {}: {}\n'.format(post_time, url))
			strange_url_set.add(url)
		except Exception:
			print('[time] wierd things happened {}: {}\n'.format(post_time, url))
			strange_url_set.add(url)

	else:
		print('[author & time] {} info_box: {}\n'.format(len(info_box), url))
		strange_url_set.add(url)


# --------------------- content -----------------------------
# <div class='content htmlview'> ... </div>
# -----------------------------------------------------------
	content = soup.findAll('div', {'class': 'content htmlview'})
	if len(content) == 1:
		page_info['content'] = content[0].text
	else:
		print('[content] {} content: {}\n'.format(len(content), url))
		strange_url_set.add(url)



# --------------------- keywords ----------------------------
# <div class="tag_box">
# 		<a class="tag_link" href="/search/tag/Apple">Apple</a>
# 		<a class="tag_link" href="/search/tag/iAd">iAd</a>
# </div>
# -----------------------------------------------------------
	page_info['keyword'] = []

	keyword_box = soup.findAll('div', {'class': 'tag_box'})
	if len(tag_box) == 1:
		keywords = keyword_box[0].findAll('a', {'class': 'tag_link'})
		if len(keywords) == 0:
			print('[keywords] no keyword in tag_box: {}\n'.format(url))
			strange_url_set.add(url)
		else:
			for keyword in keywords:
				page_info['keyword'].append(keyword.text)
	else:
		print('[keywords] no tag_box field: {}\n'.format(url))
		strange_url_set.add(url)


# ---------------- fb_like & fb_share -----------------------
# <div class='content htmlview'> ... </div>
# -----------------------------------------------------------
	

http://www.facebook.com/v2.1/plugins/like.php?action=like&app_id=982292261797820&channel=http%3A%2F%2Fstaticxx.facebook.com%2Fconnect%2Fxd_arbiter.php%3Fversion%3D42%23cb%3Df19115a94%26domain%3Dwww.bnext.com.tw%26origin%3Dhttp%253A%252F%252Fwww.bnext.com.tw%252Ff1ee975b74%26relation%3Dparent.parent&container_width=91&href=http%3A%2F%2Fwww.bnext.com.tw%2Farticle%2Fview%2Fid%2F38474&layout=button_count&locale=zh_TW&sdk=joey&share=false&show_faces=false


	return page_info


def get_category_urls(category_url):
	detail_urls = []
	return detail_urls