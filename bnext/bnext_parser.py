# -*- coding: utf-8 -*-

import time
import requests
import urllib
import HTMLParser


from random import randint
from datetime import datetime
from bs4 import BeautifulSoup


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
				,'category'		: None \
				,'popularity'   : None \
				,'commentsbox_count': None}

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
	hyper_info_box = soup.find('div', {'class': 'info_box'})
	info_box = hyper_info_box.findAll('span', {'class': 'info'})
	if len(info_box) == 2:
		author    = info_box[0].text
		post_time = info_box[1].text

		#return author

		if ':' in author:
			author = author.split(':')[1]
		if u'：' in author:
			author = author.split(u'：')[1]
		page_info['journalist'] = author

		if ':' in post_time:
			post_time = post_time.split(':')[1]
		if u'：' in post_time:
			post_time = post_time.split(u'：')[1]

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
	if len(keyword_box) == 1:
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
# buggy solution
# -----------------------------------------------------------
#	prefix_like  = 'http://www.facebook.com/v2.1/plugins/like.php?action=like&'
#	prefix_share = 'https://www.facebook.com/v2.1/plugins/share_button.php?'
#	app_id = soup.find('meta', {'property': 'fb:app_id'})['content']	
#	peudo_dict = {'href': url, 'app_id': app_id, 'layout': 'button_count'}
#
#	ret = requests.get(prefix_like+urllib.urlencode(peudo_dict))
#	like_soup = BeautifulSoup(ret.content)
#	try:
#		like = like_soup.find('span', {'class': 'pluginCountTextDisconnected'}).text
#		like = int(like.replace(',', ''))
#		page_info['fb_like'] = like
#	except:
#		print('[fb_like] can\'t find fb like: {}\n'.format(url))
#
#	return prefix_share+urllib.urlencode(peudo_dict)
#
#	ret = requests.get(prefix_share+urllib.urlencode(peudo_dict))
#	share_soup = BeautifulSoup(ret.content)
#	try:
#		share = share_soup.find('span', {'class': 'pluginCountTextDisconnected'}).text
#		share = int(share.replace(',', ''))
#		page_info['fb_share'] = share
#	except:
#		print('[fb_share] can\'t find fb share: {}\n'.format(url))


# ---------------- fb_like & fb_share -----------------------
# facebook api solution
# -----------------------------------------------------------
	utility_string = 'https://graph.facebook.com/fql?q=SELECT%20like_count,%20total_count,%20share_count,%20click_count,%20commentsbox_count%20FROM%20link_stat%20WHERE%20url%20=%20%22{}%22'
	utility_string.format('url')

	res = requests(utility_string)
	page_info['fb_like'] = res.json()['data'][0]['like_count']
	page_info['fb_share'] = res.json()['data'][0]['share_count']
	page_info['fb_commentsbox_count'] = res.json()['data'][0]['commentsbox_count']

	return page_info


def get_category_urls(category_url):
	detail_urls = []
	prefix = 'http://www.bnext.com.tw'
	res  = requests.get(category_url)
	soup = BeautifulSoup(res.content)
	page_list = soup.find('ul', 'pagination')
	last_page = page_list.findAll('a')[-1]['href']
	midfix = '?p='
	last_page = int(last_page.split('=')[-1])

	for page in range(1, last_page+1):
		time.sleep(randint(1,3))

		res = requests.get(category_url+midfix+str(page))
		soup = BeautifulSoup(res.content)

		container = soup.find('div', {'id': 'categories_list', 'class': 'main_list_sty01'})
		article_list = container.findAll('div', {'class': 'div_tab item_box'})
		for article in article_list:
			sufix = article.find('a', {'class': 'item_title block_link'})['href']
			detail_urls.append(prefix+sufix)
			#print ('found url: {}\n'.format(prefix+sufix))

	return detail_urls