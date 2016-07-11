# -*- coding: utf-8 -*-
from datetime import datetime
import cts_parser
import requests
import os.path
import unittest
from mock import patch
from requests import Response

path = os.path.dirname(os.path.abspath(__file__))

##################################testing parser_page###################################
def get_fake_request_parser_page(url):
    if url == 'http://news.cts.com.tw/cts/general/201605/201605281756574.html#.V4EdH7h942w':
        targetfile = open(path + '/tests/parser_page/fake_page', 'r')
        fake_page_content = targetfile.read()
        targetfile.close()

        fake_page = Response()
        fake_page._content = fake_page_content
        fake_page.encoding = 'iso8859-1'
        return fake_page

    if url == 'https://api.facebook.com/method/links.getStats?urls=http://news.cts.com.tw/cts/general/201605/201605281756574.html#.V4EdH7h942w':
        targetfile = open(path + '/tests/parser_page/fake_page_fb', 'r')
        fake_fb_page_content = targetfile.read()
        targetfile.close()

        fake_fb_page = Response()
        fake_fb_page._content = fake_fb_page_content
        fake_fb_page.encoding = 'utf-8'
        return fake_fb_page

    if url == 'http://graph.facebook.com/comments?filter=stream&fields=from,like_count,message,created_time,id,parent.fields(id)&id=http://news.cts.com.tw/cts/general/201605/201605281756574.html#.V4EdH7h942w':
        targetfile = open(path + '/tests/parser_page/fake_comments', 'r')
        fake_comments_content = targetfile.read()
        targetfile.close()

        fake_comments = Response()
        fake_comments._content = fake_comments_content
        fake_comments.encoding = 'utf-8'
        return fake_comments

def patch_request_get_parser_page():
    global ori_requests_get
    ori_requests_get = requests.get
    requests.get = get_fake_request_parser_page

def unpatch_request_get_parser_page():
    global ori_requests_get
    requests.get = ori_requests_get

def data_for_parser_page(url):
    target1 = {
        "url": unicode("http://news.cts.com.tw/cts/general/201605/201605281756574.html#.V4EdH7h942w", "utf-8"),
        "source_press": unicode("http://www.cts.com.tw", "utf-8"),
        "title": unicode("首例! 捷運工人集體罹\"絕症\"", "utf-8"),
        "post_time": datetime(2016, 5, 28, 13, 23),
        "journalist": unicode("綜合報導 / 台北市", "utf-8"),
        "content": unicode("你有沒有注意過，在台電大樓跟江子翠捷運站都豎立了「台北捷運潛水夫症工人紀念碑」，這是因為1993年捷運新店線施工過程，不當使用「壓氣工法」，導致數十名工人罹患「潛水夫症」，20年過去，工人們年歲已大，卻仍承受著刺骨病痛，這是全台灣第一件，重大工程的集體職業病案例，採訪小組找到當年的捷運工人，帶您來看他們的故事。張孝忠捷運工人，今年48歲，住在花蓮玉里半山腰簡陋的小平房，跟中風的老母親相依為命，得到潛水夫症，外表看起來，跟一般人無異，但看不到的地方卻是千瘡百孔。張孝忠捷運工人，1993年台北捷運新店線CH221標工地，因為工程滲水下塌，首度引進壓氣工法，在短短220公尺的捷運坑道，強灌進1.3公斤的大氣壓力，阻擋土層崩塌，這是為了降低成本、加速完工，最快的做法，但卻造成幾十個捷運工人，意外得到這一輩子無法痊癒的的絕症、比例高達八成。張孝忠捷運工人，原來在坑道下，異常氣壓環境下作業，時間和程序都有標準，沒正常減壓的工人，血液中形成氮氣泡排不出來，在身體四處流竄、侵入細胞，輕則四肢疼痛，嚴重還會下半身癱瘓、休克甚至死亡。像阿忠沒有工作，不敢結婚，領低薪過活的工人，不只一個，更有人飽受刺骨之痛，撐不下去輕生。顧玉玲人民火大行動聯盟發言人，黃敏祥北市捷運工程局南區工程處主任，抗議，1996年捷運潛水夫症的工人開始集結抗爭長達三年，最後有25人跟資方達成職災和解，並領取70萬元和解金。對長期處於社會底層的工人來說，這是當時，最卑微的選擇。台北捷運，帶領台北市邁向國際化，但卻很少人知道，施工的過程卻是一條血跡斑斑的道路，在潛水夫症紀念碑上，沒有一個捷運工人被留下名字，但他們心中默默期待，未來類似的悲劇不會再重演，而民眾享受捷運便利的同時，會不會有人還記得他們。", "utf-8"),
        "compare": None,
        "keyword": [u'\u53f0\u96fb\u5927\u6a13', u'\u6c5f\u5b50\u7fe0', u'\u6377\u904b\u7ad9', u'\u53f0\u5317\u6377\u904b\u6f5b\u6c34\u592b\u75c7\u5de5\u4eba\u7d00\u5ff5\u7891', u'\u58d3\u6c23\u5de5\u6cd5', u'\u4e0d\u7576\u4f7f\u7528'],
        "fb_like": 7129,
        "fb_share": 674,
        "category": [u'\u7d9c\u5408'],
        "comment": [{'source_type': 'facebook', 'post_time': datetime(2016, 5, 30, 19, 25, 50), 'like': 0, 'dislike': None, 'message': u'\u4ecb\u7d39\u4f4d\u670b\u53cb\u8336\u59d0\u7684\u8cf4\uff1a1217198\n\u4eba\u597d \u5979\u5bb6\u59b9\u59b9\u90fd\u8d85\u6b63\u9ede\u7684\uff0c\u9084\u4e0d\u6703\u5f88\u8cb4 \u55ae\u8eab\u5bc2\u5bde\u7684\u7537\u4eba\u4e0d\u932f\u9996\u9078\n\u5c0f\u8cc7\u4eba\u58eb\uff0c\u5076\u723e\u51fa\u4f86\u653e\u9b06\u653e\u9b06 \u89e3\u89e3\u58d3\u883b\u597d\u7684\u3002\n\u5e6b\u5979\u5c31\u662f\u5f88\u591a\u5ba2\u4eba\u89ba\u5f97\u5979\u5bb6\u7684\u59b9\u4e0d\u932f \u53e3\u7891\u90fd\u5f88\u597d\uff0c\u6240\u4ee5\u6211\u4e5f\u624d\u6562\u5728\u9019\u5ba3\u50b3\uff0c\u53ea\u662f\u4e0d\u5e0c\u671b\u4e00\u4e9b\u4eba\u88ab\u9a19\n\u82b1\u4e00\u4e9b\u8840\u6c57\u9322\u3002', 'id': u'1432744056751842_1434923923200522', 'actor': u'Wei Chen', 'sub_comments': []}, {'source_type': 'facebook', 'post_time': datetime(2016, 6, 22, 1, 51, 6), 'like': 72, 'dislike': None, 'message': u'\u6211\u4e0d\u770b\u83ef\u8996\u65b0\u805e\u5f88\u4e45\u4e86\uff0c\u53bb\u670b\u53cb\u5bb6\u767c\u73fe\u5728\u770b\u83ef\u8996\u65b0\u805e\uff0c\u6211\u4e5f\u6703\u7576\u5834\u5efa\u8b70\u4ed6\u5011\u8f49\u53f0\uff0c\u4e26\u8aaa\u660e\u62d2\u770b\u7684\u7406\u6027\u539f\u56e0\u3002\u83ef\u8996\u65b0\u805e\u7684\u7d20\u8cea\u57282010\u5e74\u5de6\u53f3\u5d29\u843d\uff0c\u7136\u5f8c\u9010\u5e74\u8b8a\u5f97\u66f4\u4f4e\u7d1a\uff0c\u66f4\u7f3a\u5fb7\uff0c\u66f4\u50cf\u500b\u653f\u6cbb\u6253\u624b\u3002\u96d6\u7136\u73fe\u5728\u5df2\u7d93\u662f\u6c11\u9032\u9ee8\u57f7\u653f\uff0c\u4e0d\u904e\u83ef\u8996\u65b0\u805e\u7684\u98a8\u683c\u4f9d\u7136\u6c92\u6709\u4efb\u4f55\u6539\u8b8a\uff0d\uff0d\u83ef\u8996\u65b0\u805e\u57fa\u672c\u4e0a\u662f\u65b0\u5317\u5e02\u653f\u5e9c\u8207\u570b\u6c11\u9ee8\u7684\u65b0\u805e\u767c\u4f48\u7ad9\uff0c\u540c\u6642\u4e5f\u662f\u6587\u904e\u98fe\u975e\u3001\u7c89\u98fe\u570b\u6c11\u9ee8\u3001\u6253\u64ca\u4e00\u5207\u975e\u570b\u6c11\u9ee8\u52e2\u529b\u3001\u898b\u9b3c\u5c31\u62dc\u3001\u898b\u4eba\u5c31\u54ac\u7684\u65b0\u805e\u760b\u72d7\u3002\n\n\u5c31\u4ee5\u9019\u7bc7\u65b0\u805e\u5831\u5c0e\u70ba\u4f8b\uff0c\u6574\u7bc7\u65b0\u805e\u5167\u5bb9\u90fd\u662f\u717d\u60c5\u9732\u9aa8\u7684\u300c\u82e6\u3001\u60b2\u3001\u6dda\u3001\u6068\u300d\uff0c\u770b\u5b8c\u4ee5\u5f8c\uff0c\u9664\u4e86\u4ec7\u6068\u61a4\u6012\u4e4b\u5916\uff0c\u4f60\u751a\u9ebc\u90fd\u4e0d\u77e5\u9053\uff0c\u751a\u9ebc\u90fd\u5f97\u4e0d\u5230\u3002\u89c0\u773e\u770b\u4e86\u9019\u65b0\u805e\uff0c\u4e0d\u6703\u56e0\u6b64\u61c2\u5f97\u554f\u984c\u7684\u4f86\u9f8d\u53bb\u8108\uff0c\u53ea\u6703\u5f97\u5230\u6050\u61fc\u60b2\u60c5\uff0c\u7136\u5f8c\u4e00\u5473\u6050\u614c\u3002\u83ef\u8996\u65b0\u805e\u90e8\u7d93\u7406\uff0c\u5728\u9019\u4e00\u5247\u65b0\u805e\u4e2d\u7684\u89d2\u8272\uff0c\u5c07\u8a18\u8005\u8207\u64ad\u5831\u54e1\u5851\u9020\u70ba\u300c\u6311\u64a5\u96e2\u9593\u3001\u717d\u52d5\u60b2\u60c5\u4ec7\u6068\u7684\u5c0f\u4eba\u300d\u3002\u4ee4\u4eba\u53ad\u60e1\u4e4b\u8655\u5c31\u5728\u9019\u88e1\uff1a\u83ef\u8996\u65b0\u805e\u90e8\u539f\u672c\u53ef\u4ee5\u591a\u82b110\u79d2\u9418\u5de6\u53f3\uff0c\u7528\u7c21\u6613\u5716\u7247\u52d5\u756b\u89e3\u91cb\u6f5b\u6c34\u592b\u75c5\u7684\u4f86\u9f8d\u53bb\u8108\uff0c\u4f7f\u6574\u5247\u65b0\u805e\u7684\u50f9\u503c\u63d0\u9ad810\u500d\u90fd\u4e0d\u6b62\uff0c\u4f46\u83ef\u8996\u65b0\u805e\u90e8\u4e0d\u9858\u610f\u9019\u9ebc\u505a\uff0c\u83ef\u8996\u65b0\u805e\u90e8\u4e0d\u6253\u7b97\u8b93\u89c0\u773e\u8b8a\u8070\u660e\uff0c\u8b8a\u535a\u5b78\u3002\u83ef\u8996\u65b0\u805e\u90e8\u6253\u7b97\u7528\u7121\u8166\u7684\u300c\u7d55\u75c7\u300d\u5169\u5b57\u4f86\u6050\u5687\u89c0\u773e\uff0c\u7a4d\u6975\u717d\u52d5\u90a3\u7a2e\u57fa\u65bc\u7121\u77e5\u8207\u7121\u80fd\u7684\u4ec7\u6068\u3002\u7c21\u55ae\u8b1b\uff0c\u83ef\u8996\u65b0\u805e\u90e8\u5e0c\u671b\u89c0\u773e\u6d17\u8166\u6210\u300c\u8822\u5f97\u8cfd\u8c6c\u7684\u4f4e\u80fd\u5152\u300d\uff0c\u9019\u6a23\u624d\u597d\u64cd\u5f04\u89c0\u773e\u7684\u60c5\u7dd2\u8207\u884c\u70ba\u3002\n\n\u6240\u4ee5\u6211\u624d\u6703\u5728\u6b64\u516c\u958b\u63ed\u767c\u83ef\u8996\u65b0\u805e\u90e8\u3002\u6211\u4e0d\u76f8\u4fe1\u63a1\u8a2a\u6b64\u65b0\u805e\u7684\u8a18\u8005\u6709\u90a3\u9ebc\u8822\uff0c\u6211\u76f8\u4fe1\u63a1\u8a2a\u6b64\u65b0\u805e\u7684\u8a18\u8005\u5df2\u7d93\u63d0\u4ea4\u4e86\u8207\u6f5b\u6c34\u4f15\u75c5\u6709\u95dc\u7684\u79d1\u666e\u8cc7\u6599\u3002\u53ef\u662f\u83ef\u8996\u65b0\u805e\u90e8\u7684\u7d93\u7406\uff0c\u4e0d\u9858\u63a1\u7528\uff0c\u56e0\u70ba\u7528\u4e86\u6703\u8b93\u89c0\u773e\u8b8a\u8070\u660e\u3002\n\n\u83ef\u8996\u65b0\u805e\u90e8\u7d93\u7406\uff0c\u80fd\u5426\u8acb\u4f60\u8d95\u5feb\u53bb\u6b7b\u4e00\u6b7b\uff1f\u4f60\u70ba\u751a\u9ebc\u5c38\u4f4d\u7d20\u9910\uff0c\u76f4\u5230\u73fe\u5728\u9084\u4e0d\u6efe\u51fa\u516c\u53f8\uff1f\u83ef\u8996\u65b0\u805e\u90e8\u9019\u9ebc\u591a\u54e1\u5de5\uff0c\u8981\u56e0\u70ba\u4f60\u7684\u504f\u57f7\u81ea\u79c1\u800c\u4e1f\u6389\u98ef\u7897\u55ce\uff1f\u8acb\u4f60\u8d95\u5feb\u6efe\u86cb\uff0c\u8b1d\u8b1d\u3002', 'id': u'1432744056751842_1454224064603841', 'actor': u'Jeffrey Wang', 'sub_comments': [{'post_time': datetime(2016, 7, 5, 16, 42, 26), 'like': 2, 'actor': u'Norman Shih', 'source_type': 'facebook', 'dislike': None, 'message': u'\u592a\u4e2d\u80af\uff01'}, {'post_time': datetime(2016, 7, 6, 8, 3, 47), 'like': 0, 'actor': u'\u5f90\u656c\u5eb7', 'source_type': 'facebook', 'dislike': None, 'message': u'\u5148\u641e\u6e05\u695a\u963f\u6241\u6642\u4ee3\u83ef\u8996\u7e3d\u7d93\u7406\u662f\u8ab0\uff1f\u73fe\u5728\u53c8\u662f\u8ab0\uff1f\u8ab0\u5728\u64cd\u63a7\u5a92\u9ad4\uff0c\u6478\u8457\u826f\u5fc3\u60f3\u4e00\u60f3\uff01'}, {'post_time': datetime(2016, 7, 7, 0, 0, 55), 'like': 0, 'actor': u'Ming-Ren Yang', 'source_type': 'facebook', 'dislike': None, 'message': u'\u6211\u53ea\u89ba\u5f97\u6587\u7b46\u6709\u5920 \u5dee'}]}, {'source_type': 'facebook', 'post_time': datetime(2016, 7, 2, 12, 11, 55), 'like': 0, 'dislike': None, 'message': u'\u597d\u8f9b\u82e6\uff01\uff01\uff01\uff01\uff1e\uff1c\n\n--\n\u3010\u7626easy\u2764\u3011FB\u641c\u5c0b\u2192\u6e1b\u91cd\u9054\u4eba \u827e\u7433\u6559\u4f60\u8f15\u9b06\u7626', 'id': u'1432744056751842_1463085553717692', 'actor': u'Liou Naomi', 'sub_comments': []}, {'source_type': 'facebook', 'post_time': datetime(2016, 7, 2, 15, 54, 29), 'like': 0, 'dislike': None, 'message': u'\u5c0f\u5f1f\u5403.\u9b5a.\u559d.\u8336.\u5feb1\u5e74\u4e86\uff0c\u6bcf\u6b21\u4f86\u7684\u7d20\u8cea\u8ddf \u8336.\u838a.\u4ecb\u7d39\u5dee\u592a\u591a\uff0c\n\u5c0f\u5f1f\u5f88\u809a\u721b \u6211\u81ea\u8a8d\u70ba\u4e0d\u662f\u4e00\u500b\u5f88\u6a5f\u8eca\u7684\u5ba2\u4eba \n\u4f46\u662f\u4f60\u5225\u6b3a\u9a19\u6211\u5c31\u597d \u53ef\u8336\u838a\u6709\u6642\u5019\u70ba\u4e86\u8cfa\u9322 \n\u4e0d\u9867\u5ba2\u4eba\u73a9\u5f97\u958b\u5fc3\u8207\u5426 \u56e0\u6b64\u5c0f\u5f1f\u4e00\u76f4\u60f3\u5c0b\u8993\u65b0\u7684\u8336.\u838a \n\u65b9\u4fbf\u56fa\u5b9a\u4e0b\u4f86 \u5728\u8ad6\u58c7\u4e5f\u5c0b\u8993\u4e86\u5f88\u4e45 \u7d42\u65bc\u5728XX\u8ad6\u58c7 \u767c\u73fe\u4e86\u4e00\u5bb6\u65b0.\u8336.\u838a \n\u8a66\u63a2\u7684\u5fc3\u53bb\u7d04\u4e86\u4e00\u6b21 \u8d0a \u5927\u8d0a \u6709\u8b93\u5c0f\u5f1f.\u723d.\u5230 \u4e0d\u77e5\u662f\u65b0.\u8336.\u505a\u53e3\u7891\u9084\u662f\u7559\u5ba2\u4eba \n\u6367.\u5834.3\u6b21\u90fd\u73a9\u5f97\u5f88\u958b\u5fc3 \u8336.\u59d0.\u5f88\u7528\u5fc3\u5e6b\u6211\u5b89\u6392 \u611f\u89ba\u5f88\u8212.\u670d \u5c0f\u5f1f\u4e5f\u56fa\u5b9a\u627e\u9019\u5bb6\u4e86\n\u6709\u8ddf\u5c0f\u5f1f\u540c\u6a23\u906d\u9047\u7684\u5927\u5927\u53ef\u4ee5\u8a66\u8a66\u770b\u9019\u5bb6.\u8336.\u838a.\n\u3010L.INE\uff1aLover419   s.kper\uff1ammlove.0510 \u3011\n\u8aaa\u4ed4\u4ed4\u4ecb\u7d39\u9084\u53ef\u770b.\u7167\uff01\u90e8\u5206\u59b9\u59b9\u9084\u6709\u512a.\u60e0\u3002', 'id': u'1432744056751842_1463243240368590', 'actor': u'Pioy Kee', 'sub_comments': []}, {'source_type': 'facebook', 'post_time': datetime(2016, 7, 3, 6, 40, 12), 'like': 8, 'dislike': None, 'message': u'\u6f5b\u6c34\u4f15\u75c7\u4e0d\u662f\u7d55\u75c7  \n\u662f\u6f5b\u6c34\u91ab\u5b78\u7684\u77e5\u8b58\u4e0d\u8db3\u4e5f\u6c92\u7167\u6e1b\u58d3\u7a0b\u5e8f\u6240\u81f4\n\u5f71\u7247\u4e2d\u6240\u8a00\u7684\u7167\u6e1b\u58d3\u7a0b\u5e8f\n\u662f\u7167\u54ea\u500b\u6642\u9593\u6df1\u5ea6\u7684\u8868\u53bb\u4f5c\u7684\u8acb\u67e5\u660e\u4e00\u4e0b\n\u5982\u7167\u9019\u7a2e\u8aaa\u6cd5\n\u6d77\u4e8b\u5de5\u7a0b\u7684\u6f5b\u6c34\u5de5\u4f5c\u8005\u65e9\u5c31\u58de\u5149\u5149\u4e86', 'id': u'1432744056751842_1463756510317263', 'actor': u'Kaku Chun Wa', 'sub_comments': []}, {'source_type': 'facebook', 'post_time': datetime(2016, 7, 3, 13, 36, 30), 'like': 4, 'dislike': None, 'message': u'\u9019\u662f\u771f\u7684\u4e8b\u5be6\uff0c\u90a3\u6642\u5019\u90fd\u662f\u539f\u4f4f\u6c11\u5f9e\u4e8b\u9019\u500b\u5de5\u4f5c\u3002\n\u4ed6\u5011\u5e38\u5e38\u8981\u53bb\u6e1b\u58d3\u5009\u6cbb\u7642\u3002\n\u6211\u7684\u6f5b\u6c34\u6559\u7df4\u5c31\u9047\u904e\u4e00\u6b21\uff0c\u4ed6\u5011\u90fd\u5728\u7f75\u90a3\u6642\u7684\u53f0\u5317\u5e02\u5e02\u9577\u3002\n\u800c\u9019\u5de5\u7a0b\u70ba\u4ec0\u9ebc\u6c92\u6709\u5916\u52de\u5462 ?\u56e0\u70ba\u9019\u6703\u662f\u570b\u969b\u554f\u984c\u3002\u4e0d\u662f\u6578\u5341\u842c\u53ef\u4ee5\u89e3\u6c7a\u7684\u3002', 'id': u'1432744056751842_1463971003629147', 'actor': u'\u5433\u7acb\u4ec1', 'sub_comments': [{'post_time': datetime(2016, 7, 3, 16, 25), 'like': 15, 'actor': u'\u6c5f\u6587\u660e', 'source_type': 'facebook', 'dislike': None, 'message': u'\u77e5\u9053\u7684\u58d3\u6c23\u5de5\u6cd5.\u9032\u51fa\u90fd\u6709\u8a2d\u589e.\u6e1b\u58d3\u8259\u5728\u73fe\u5834\u55ce???\n\u65e5\u672c\u5de5\u7a0b\u5e2b\u9032\u51fa\u90fd\u6309\u7a0b\u5e8f\u589e\u6e1b\u58d3.\u904e\u7a0b\u5404\u7d041\u5c0f\u6642.\n\u800c\u6211\u5011\u5049\u5927\u7684\u52de\u5de5\u5927\u591a\u4e5f\u6709\u7167\u505a.\n\u4f46\u5c31\u662f\u6703\u6709\u4eba\u5acc\u9ebb\u7169\u4e0d\u505a.(\u4f86\u56de\u8981\u82b12\u500b\u5c0f\u6642.\u5acc\u6d6a\u8cbb\u6642\u9593)\n\u767c\u75c5\u7684\u5c31\u662f\u9019\u4e9b\u4eba.\u5927\u817f\u9aa8\u721b\u6389\u4e86.\u63db\u4e0d\u92b9\u92fc\u5927\u817f\u9aa8.(\u50cf\u6a5f\u5668\u6230\u8b66.\u51fa\u570b\u91d1\u5c6c\u6383\u63cf\u90fd\u6703\u53eb)\n\u52de\u5b89\u5728\u7576\u6642\u53c8\u4e0d\u592a\u6ce8\u91cd.\u52de\u5b89\u54e1\u90fd\u6709\u8b1b.\u4f46\u662f\u4e9b\u4eba\u4e0d\u9ce5\u6709\u4ec0\u9ebc\u8fa6\u6cd5\u5462???\n\u8b1b\u96e3\u807d\u9ede.\n\u5c31\u7b97\u73fe\u5728.3\u75335\u4ee4\u5de5\u4f5c\u4e2d\u4e0d\u80fd\u559d\u9152\u7cbe\u6027\u98f2\u6599.\n\u9084\u4e0d\u662f\u4e00\u5806\u559d.\u6293\u4e0d\u52dd\u6293.\n\u53f0\u7063\u5564\u9152\u5305\u67f3\u6a59\u6c41\u5305\u88dd.\u963f\u6bd4\u7528\u4fdd\u7279\u74f6\u88dd.\u9023\u8518\u8338\u9152.\u7af9\u8449\u9752\u90fd\u6709.\n\u60a8\u8aaa\u51fa\u4e8b\u60c5\u8981\u602a\u8ab0.\n\u5de5\u7a0b\u4fdd\u96aa\u559d\u9152\u51fa\u4e8b.\u662f\u4e0d\u8ce0\u7684.'}]}, {'source_type': 'facebook', 'post_time': datetime(2016, 7, 5, 1, 25, 30), 'like': 8, 'dislike': None, 'message': u'1993 \u5e02\u9577\u70ba\u570b\u6c11\u9ee8\u7684\u9ec3\u5927\u6d32\n\u5f88\u660e\u986f\uff0c\u5c31\u662f\u570b\u6c11\u9ee8\u5403\u4e86\u9019\u6848\u5b50\n\u6240\u4ee5\u9019\u4e9b\u53ef\u6190\u7684\u6377\u904b\u5de5\u4eba\u7121\u6cd5\u88ab\u7559\u4e0b\u540d\u5b57\n\u76f4\u52301996\u5e74\u9054\u6210\u548c\u89e3\n\u5c31\u662f\u9673\u6c34\u6241\u7576\u5e02\u9577\u6642\n\u53c8\u662f\u4e00\u500b\u6c11\u9032\u9ee8\u5e6b\u570b\u6c11\u9ee8\u64e6\u5c41\u80a1\u7684\u4f8b\u5b50', 'id': u'1432744056751842_1465242030168711', 'actor': u'\u8521\u5b89\u55ac', 'sub_comments': []}, {'source_type': 'facebook', 'post_time': datetime(2016, 7, 6, 4, 12, 46), 'like': 0, 'dislike': None, 'message': u'\u570b\u8ecd\u9ad8\u96c4\u7e3d\u91ab\u9662\u5de6\u71df\u5206\u9662\u6709\u6f5b\u6c34\u91ab\u5b78\u90e8\uff0c\u4e0d\u59a8\u53ef\u4ee5\u53bb\u5c31\u8a3a\u8a66\u8a66\u770b\u3002', 'id': u'1432744056751842_1466189826740598', 'actor': u'Hong Yo-Chen', 'sub_comments': []}, {'source_type': 'facebook', 'post_time': datetime(2016, 7, 7, 15, 7, 37), 'like': 0, 'dislike': None, 'message': u'\u52a0\u7c5f\uff1abub89 \u7f8e\u7709\u7b49\u4f60\u628a\u5979\u64a9\n\u52a0\u7c5f\uff1abub89 \u7f8e\u7709\u7b49\u4f60\u628a\u5979\u64a9\n\u52a0\u7c5f\uff1abub89 \u7f8e\u7709\u7b49\u4f60\u628a\u5979\u64a9\n\u52a0\u7c5f\uff1abub89 \u7f8e\u7709\u7b49\u4f60\u628a\u5979\u64a9\n\u52a0\u7c5f\uff1abub89 \u7f8e\u7709\u7b49\u4f60\u628a\u5979\u64a9\n\u52a0\u7c5f\uff1abub89 \u7f8e\u7709\u7b49\u4f60\u628a\u5979\u64a9\n\u52a0\u7c5f\uff1abub89 \u7f8e\u7709\u7b49\u4f60\u628a\u5979\u64a9', 'id': u'1432744056751842_1467345719958342', 'actor': u'\u598d\u598d\u5916\u9001\u8336\u52a0\u8cf4\uff1abub89 \u6709\u597d\u5eb7', 'sub_comments': []}, {'source_type': 'facebook', 'post_time': datetime(2016, 7, 7, 15, 7, 43), 'like': 0, 'dislike': None, 'message': u'\u52a0\u7c5f\uff1abub89 \u7f8e\u7709\u7b49\u4f60\u628a\u5979\u64a9\n\u52a0\u7c5f\uff1abub89 \u7f8e\u7709\u7b49\u4f60\u628a\u5979\u64a9\n\u52a0\u7c5f\uff1abub89 \u7f8e\u7709\u7b49\u4f60\u628a\u5979\u64a9\n\u52a0\u7c5f\uff1abub89 \u7f8e\u7709\u7b49\u4f60\u628a\u5979\u64a9\n\u52a0\u7c5f\uff1abub89 \u7f8e\u7709\u7b49\u4f60\u628a\u5979\u64a9\n\u52a0\u7c5f\uff1abub89 \u7f8e\u7709\u7b49\u4f60\u628a\u5979\u64a9\n\u52a0\u7c5f\uff1abub89 \u7f8e\u7709\u7b49\u4f60\u628a\u5979\u64a9', 'id': u'1432744056751842_1467345866624994', 'actor': u'\u598d\u598d\u5916\u9001\u8336\u52a0\u8cf4\uff1abub89 \u6709\u597d\u5eb7', 'sub_comments': []}],
    }
    return target1

def urls_for_parser_page(number):
    targetfile = open(path + '/tests/parser_page/test_urls', 'r')
    content = targetfile.read()
    targetfile.close()

    start_index = content.index(str(number)) + len(str(number)) + 1
    target_content = content[start_index:]
    end_index = target_content.index(',')
    return_url = target_content[:end_index]
    print('You are testing url ' + str(number) + ' in test_urls for testing parser_page')
    return return_url


####################################testing get_category_urls###################################
def get_fake_request_get_category_urls(url):
    if url == 'http://news.cts.com.tw/weather/index.html#cat_list':
        targetfile = open(path + '/tests/get_category_urls/fake_page_1', 'r')
        fake_page_content = targetfile.read()
        targetfile.close()

        fake_page = Response()
        fake_page._content = fake_page_content
        fake_page.encoding = 'iso8859-1'
        return fake_page

    else:
        new_url = url[:-5] #delete ".html"
        start_index = url.index("http://news.cts.com.tw/weather/index") + len("http://news.cts.com.tw/weather/index")
        page_index = int(new_url[start_index:])
        if page_index in range(2,21):
            targetfile = open(path + '/tests/get_category_urls/fake_page_' + str(page_index), 'r')
            fake_page_content = targetfile.read()
            targetfile.close()

            fake_page = Response()
            fake_page._content = fake_page_content
            fake_page.encoding = 'iso8859-1'
            return fake_page

def patch_request_get_category_urls():
    global ori_requests_get
    ori_requests_get = requests.get
    requests.get = get_fake_request_get_category_urls

def unpatch_request_get_category_urls():
    global ori_requests_get
    requests.get = ori_requests_get

def data_for_category_urls(url):
    targetfile = open(path + '/tests/get_category_urls/test_data', 'r')
    content = targetfile.read()
    targetfile.close()
    
    start_index = content.index(url) + len(url) + 1  #after the category url
    target_content = content[start_index:]
    end_index = target_content.index(';')            #before next category url
    target_content = target_content[:end_index]      #target content that we want
    number = target_content.count(',') + 1

    detail_urls = []
    for i in range(number):
        index = target_content.index('.html') + len('.html')
        detail_urls.append(target_content[0:index])
        target_content = target_content[index+1:]
    return detail_urls

def urls_for_category_urls(number):
    targetfile = open(path + '/tests/get_category_urls/test_urls', 'r')
    content = targetfile.read()
    targetfile.close()

    start_index = content.index(str(number)) + len(str(number)) + 1
    target_content = content[start_index:]
    end_index = target_content.index(',')
    return_url = target_content[:end_index]
    print('You are testing url ' + str(number) + ' in test_urls for testing get_category_urls')
    return return_url


def compare_dict(dict1, dict2):
    if dict1 == None or dict2 == None:
        return False
    if type(dict1) is not dict or type(dict2) is not dict:
        return False
    if not (len(dict1.keys()) == len(dict2.keys())):
        return False
    dicts_equal = True
    for key in dict1.keys():
        if dict1[key] != dict2[key]:
            dicts_equal = False
            break
    return dicts_equal


class TestCtsnews(unittest.TestCase):
    def test_get_parser_page(self):
        #with patch.object(requests, 'get', side_effect = get_fake_request_parser_page) as requests.get:
        patch_request_get_parser_page()
        for i in range(1):
            test_url = urls_for_parser_page(i + 1)
            result = cts_parser.parser_page(test_url)
            target = data_for_parser_page(test_url)
                
            if compare_dict(result, target) == True:
                print "Parser_page: Succeed"
            else:
                print "Parser_page: Fail"
        unpatch_request_get_parser_page()

    def test_get_category_urls(self):
        #with patch.object(requests, 'get', side_effect = get_fake_request_get_category_urls) as requests.get:
        patch_request_get_category_urls()
        for i in range(1):
            test_url = urls_for_category_urls(i + 1)
            result = cts_parser.get_category_urls(test_url)
            target = data_for_category_urls(test_url)
            equal = True
            for i in range(len(result)):
                if result[i] != target[i]:
                    equal = False
                    print "Get_category_urls: Fail"
                    break
            else:
                print "Get_category_urls: Succeed"
            #self.assertEqual(target, result)
        unpatch_request_get_category_urls()

if __name__ == '__main__':
    unittest.main()