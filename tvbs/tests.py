# -*- coding: utf-8 -*-
import tvbs_Parser
import datetime
import pickle
import requests
import os.path
import unittest
category_url_list = ['http://news.tvbs.com.tw/health',
                     'http://news.tvbs.com.tw/travel',
                     'http://news.tvbs.com.tw/supercars',
                     'http://news.tvbs.com.tw/tech',
                     'http://news.tvbs.com.tw/travel',
                     'http://news.tvbs.com.tw/hipster',]

news_url = ['http://news.tvbs.com.tw/politics/661869',
            'http://news.tvbs.com.tw/life/662570',
            'http://news.tvbs.com.tw/politics/662684',
            'http://news.tvbs.com.tw/politics/662521',]

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

 
class TvbsParserTest(unittest.TestCase):
  
    def test_parser_page(self):
        try:
            news_dict = tvbs_Parser.parser_page(news_url[0])
            answer_dict = {
                'comment': [],
                'title': '誤射飛彈懲處出爐\u3000從上到下7人遭記過', 
                'journalist': '何宜信', 
                'category': '政經', 
                'keyword': ['雄三飛彈', '誤射', '懲處'], 
                'content': '海軍金江艦誤射雄三飛彈釀1死3傷意外，懲處名單晚間出爐，上從上將司令下到飛彈中士等7人被記過，海軍表示意外發生的原因，最主要是飛彈中士高嘉駿今天獨自進行測試時，艦上其他的軍官正在開會，他原本應該用模擬模式，沒想到選成作戰模式才會導致飛彈誤，是把責任全推個一個中士嗎？海軍司令黃曙光強調上級督導不周一樣有責任不會逃避，行政院長林全也升高層級，明天上午將召開跨部會議。一三一艦隊長胡志政：「由於未按照程序實施測試，而且沒有幹部在場督導，所以在8點15分的時候飛彈發射離架。」飛彈究竟為什麼誤射，海軍司令部點名罪魁禍首飛彈中士高嘉駿。一三一艦隊長胡志政：「飛彈中士高嘉駿，沒有依照我們規定的保養修理執行裝備的測試。」實在有夠誇張，發射飛彈至少得經過三道關卡，怎麼感覺全推個一個中士，當時到底艦長幹什麼，而被記者問到金江艦艦長背景，艦隊長語塞說不出話場面一度尷尬。一三一艦隊長胡志政：「他是在今年的5月份接任金江艦艦長。」海軍司令黃曙光：「我軍官不負責，我士官去找軍官去拿相關火線的時候，我的軍官竟然沒有做管制也沒有跟艦長報告。」強調絕對不會卸責，海軍祭出第一波懲處名單共7位，包括司令黃曙光自請處分記過一次，艦指部中將指揮官蕭維民記過二次，一三一艦隊長胡志政記過兩次，金江艦艦長林伯澤記大過一次，兵器長許博為記大過一次，射控士官長陳明修記大過二次，飛彈中士高嘉駿記大過二次。海軍司令黃曙光：「我已經向部長…，提出…自行處分，部長會做一個裁決。」釀出1死3傷意外，艦長、兵器長、士官長、和中士高嘉駿等4人也被帶回高雄地檢署偵訊，發射操演SOP大出包震驚全國，行政院長林全決定拉高層級，要求國防部、陸委會和外交部等相關單位，2日上午10點到行政院報告來釐清。圖／TVBS', 
                'post_time': datetime.datetime(2016, 7, 1, 22, 3), 
                'fb_like': 0, 
                'compare': None, 
                'source_press': None, 
                'url': 'http://news.tvbs.com.tw/politics/661869', 
                'fb_share': 0}
             
            if compare_dict(news_dict,answer_dict):
                print("parser_page success")
            else:
                print("parser_page failed")
        except ConnectionError:
            pass
         
        
    def test_get_category_urls(self):
        try:
            category_urls = tvbs_Parser.get_category_urls(category_url_list[0])
            answer_urls = ['http://news.tvbs.com.tw/health/661577','http://news.tvbs.com.tw/health/661425',
                           'http://news.tvbs.com.tw/health/660389','http://news.tvbs.com.tw/health/659709',
                           'http://news.tvbs.com.tw/health/659048','http://news.tvbs.com.tw/health/656590',
                           'http://news.tvbs.com.tw/health/656394','http://news.tvbs.com.tw/health/655845']
            if len(set(category_urls).intersection(set(answer_urls))) == 8:
                print("get_category_urls success")
            else:
                print("get_category_urls failed")
        except ConnectionError:
            pass
     
 
if __name__ == '__main__':
    unittest.main() 
