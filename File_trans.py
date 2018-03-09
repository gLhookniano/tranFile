#/usr/bin/env python2
#encoding=utf8
import httplib
import hashlib
import urllib
import random
import json
import os
import re

import File_utile
from googletrans import Translator

src_path = r'H:\WHM_en\text\db'
dst_path = r'H:\WHM_zh\text\db'
loc_fileName2trans = r'./transFile.txt'

class transGoogle():
    def __init__(self, src_path, dst_path, loc_fileName2trans):
        self.google_TS_url = ['translate.google.cn', ]
        self.fromLang = 'en'
        self.toLang = 'zh-CN'
        
        self.src_path = src_path
        self.dst_path = dst_path
        self.loc_fileName2trans = loc_fileName2trans

    def trans(src_file, dst_file):
        try:
            translator = Translator(service_urls=self.google_TS_url)
            fp_s = open(src_file, 'r')
            fp_d = open(dst_file, 'w')


            de_str = ' '
            while de_str != '':
                de_str = fp_s.readline()
                tran_str = re.sub(r'"(.*)"\t"(.*)"\t"(.*)"\n', lambda _ : _.group(2), de_str)
                translations = translator.translate(tran_str, src=fromLang, dest=toLang)
                de_str = re.sub(r'"(.*)"\t"(.*)"\t"(.*)"\n', lambda _:'"'+_.group(1)+'"\t"'+translations.text+'"\t"'+_.group(3)+'"\n', de_str)
                fp_d.write(de_str.encode('utf-8'))
            fp_s.close()
            fp_d.close()
        except Exception, e:
            print e


    def list_trans(self):
        if self.src_path[-1] != '\\':
            self.src_path = self.src_path + '\\'
        if self.dst_path[-1] != '\\':
            self.dst_path = self.dst_path + '\\'
        fp_lf = open(self.loc_fileName2trans, 'r')
        
        file = ' '
        while file != '':
            file = fp_lf.readline().strip()
            trans(src_path+file, dst_path+file)
        
        fp_lf.close()


class transBaidu():
    def __init__(self, src_path, dst_path, loc_fileName2trans):
        self.appid = 'XXX'
        self.secretKey = 'XXX'
        self.baidu_TS_url = '/api/trans/vip/translate'
        self.fromLang = 'en'
        self.toLang = 'zh'
        self.src_path = src_path
        self.dst_path = dst_path
        self.loc_fileName2trans = loc_fileName2trans

    def trans(src_file, dst_file):
        try:
            httpClient = httplib.HTTPConnection('api.fanyi.baidu.com')
            fp_s = open(src_file, 'r')
            fp_d = open(dst_file, 'w')

            de_str = 'head'
            while de_str != '':
                de_str = fp_s.readline()
                tran_str = re.sub(r'"(.*)"\t"(.*)"\t"(.*)"\n', lambda _ : _.group(2), de_str)
                
                salt = random.randint(32768, 65536)
                sign = self.appid+tran_str+str(salt)+self.secretKey
                m1 = hashlib.md5(sign)
                sign = m1.hexdigest()
                TS_url = self.baidu_TS_url+'?self.appid='+self.appid+'&q='+urllib.quote(tran_str)+'&from='+self.fromLang+'&to='+self.toLang+'&salt='+str(salt)+'&sign='+sign
                httpClient.request('GET', TS_url)
                response = httpClient.getresponse() #response是HTTPResponse对象
                rs_str = response.read()
                json_str = json.loads(rs_str)
                tran_str = json_str['trans_result'][0]['dst']
                
                de_str = re.sub(r'"(.*)"\t"(.*)"\t"(.*)"\n', lambda _:'"'+_.group(1)+'"\t"'+tran_str+'"\t"'+_.group(3)+'"\n', de_str)
                fp_d.write(de_str.encode('utf-8'))
            fp_s.close()
            fp_d.close()
        except Exception, e:
            print e
        finally:
            if httpClient:
                httpClient.close()

    def list_trans(self):
        if self.src_path[-1] != '\\':
            self.src_path = self.src_path + '\\'
        if self.dst_path[-1] != '\\':
            self.dst_path = self.dst_path + '\\'
        fp_lf = open(self.loc_fileName2trans, 'r')
            
        file = fp_lf.readline().strip()
        while file:
            trans(src_path+file, dst_path+file)
            file = fp_lf.readline().strip()
                
        fp_lf.close()
        
if __name__ == '__main__':
    transGoogle(src_path, trans_path, list_file).list_trans()
    #transBaidu(src_path, trans_path, list_file).list_trans()
    
    #correct the trans
    correct_dict = {r'＃':'#', r'％':'%', r'\r': '', r'\n':'', r'导弹':'投射',
    r'/默认':'/default', r'TR':'tr', r'IMG':'img', r'UI':'ui', r'警察':'守卫', r'小兽人':'兽人', r'占位符描述':'PLACEHOLDER', r'Karaz-A-卡拉克':'卡拉兹-阿-卡拉克', r'购物车':'运输车'
    }
    print correct_dict
    File_utile.correct_lf(os.listdir(trans_path), trans_path, correct_dict)
    File_utile.update_lf(os.listdir(trans_path), dst_path, trans_path)