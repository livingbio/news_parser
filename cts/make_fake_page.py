import requests
import os.path


path = os.path.dirname(os.path.abspath(__file__))

parser_page_urls = ["http://news.cts.com.tw/cts/general/201605/201605281756574.html#.V4EdH7h942w", "http://news.cts.com.tw/cts/society/201606/201606071760311.html#.V4Rbxbh942w", "http://news.cts.com.tw/nownews/money/201607/201607061770895.html#.V4Rca7h942x"]

fb_count_urls = []
for i in range(len(parser_page_urls)):
	fb_count_url = "https://api.facebook.com/method/links.getStats?urls=" + parser_page_urls[i]
	fb_count_urls.append(fb_count_url)

fb_comments_urls = ["http://graph.facebook.com/comments?filter=stream&fields=from,like_count,message,created_time,id,parent.fields(id)&id=http://news.cts.com.tw/cts/general/201605/201605281756574.html", "http://graph.facebook.com/comments?filter=stream&fields=from,like_count,message,created_time,id,parent.fields(id)&id=http://news.cts.com.tw/cts/society/201606/201606071760311.html", "http://graph.facebook.com/comments?filter=stream&fields=from,like_count,message,created_time,id,parent.fields(id)&id=http://news.cts.com.tw/cts/society/201606/201606071760311.html&after=WTI5dGJXVnVkRjlqZAFhKemIzSTZAPRGs1TVRjMk5ESXdNVGt3TnpBeU9qRTBOamd4TnpReU1EQT0ZD", "http://graph.facebook.com/comments?filter=stream&fields=from,like_count,message,created_time,id,parent.fields(id)&id=http://news.cts.com.tw/nownews/money/201607/201607061770895.html"]

weather_urls = ["http://news.cts.com.tw/weather/index.html#cat_list"]
for i in range(2, 21):
	new_page_url = "http://news.cts.com.tw/weather/index" + str(i) + ".html"
	weather_urls.append(new_page_url)

society_urls = ["http://news.cts.com.tw/society/index.html#cat_list"]
for i in range(2, 21):
	new_page_url = "http://news.cts.com.tw/society/index" + str(i) + ".html"
	society_urls.append(new_page_url)

campus_urls = ["http://news.cts.com.tw/campus/index.html#cat_list"]
for i in range(2, 7):
	new_page_url = "http://news.cts.com.tw/campus/index" + str(i) + ".html"
	campus_urls.append(new_page_url)

total_urls = parser_page_urls + fb_count_urls + fb_comments_urls + weather_urls + society_urls + campus_urls


######################################### Start to make fake pages ###########################################
fake_page_index = 0
for i in range(len(total_urls)):
	fake_page_index += 1
	url = total_urls[i]
	resp = requests.get(url)
	targetfile = open(path + '/tests/fake_page_' + str(fake_page_index), 'w')
	if resp.encoding == 'ISO-8859-1':
		targetfile.write(resp.text.encode('ISO-8859-1'))
	elif resp.encoding == 'UTF-8' or resp.encoding == 'utf-8':
		targetfile.write(resp.text.encode('utf-8'))
	targetfile.close()
	
	#record the fake_page_index
	targetfile = open(path + '/fake_page_dic', 'a')
	targetfile.write("\n" + url + " " + str(fake_page_index))
	targetfile.close()