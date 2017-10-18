# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 09:20:58 2017

@author: wkzheng
"""

# 尝试直接抓取AJAX

# 爬一段时间后，会出现连接中断 ConnectionError: ('Connection aborted.', error(10054, ''))
# http://ask.csdn.net/questions/348140
# 在headers中添加上 keep-alive=false，奏效
# 然而，再多爬几次，又不行了。。。

# https://stackoverflow.com/questions/10115126/python-requests-close-http-connection#comment22579942_10115553
# 使用 requests.post
# 在headers中添加 {'Connection':'close'}


import requests, urllib2
import json
import time, datetime
import os
import random



# 由于多次爬页面会发生 connection aborted 问题
# 考虑使用 user_agent 轮询方式
def getHeaders():
    user_agent = [
                  'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240',
                  'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/8.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; Zoom 3.6.0)'
                  ]
    
    headers = {'User-Agent': user_agent[random.randint(0, 2)], 
           'Referer': 'http://hs.blizzard.cn/cards/',
           'Cookie': '_ntes_nnid=4669facd3c478451e5ef2309e5b7e4f9,1508205173137',
           'X-Requested-With': 'XMLHttpRequest',
           'Connection': 'close'
           }
    
    return headers


start = datetime.datetime.now()


r = requests.post('http://hs.blizzard.cn/action/cards/query', headers=getHeaders())

#print(r.text)

data = json.loads(r.text)

# 为了获取总共有多少cardclass
totalPerClass = data['totalPerClass']

for key in totalPerClass:
    print('CardClass:', key)
    
    path = "./result_json/" + key
    if not os.path.exists(path):
        os.makedirs(path)
    
    counter = 1  # 设置初始页码
    while True:
        payload = {'cardClass':key, 'p':counter, 'standard':1} 
        r = requests.post('http://hs.blizzard.cn/action/cards/query', headers=getHeaders(), params=payload)
        data = json.loads(r.text)

        cards = data['cards']
        
        for card in cards:
            card_name = card['name']
            card_img_url = card['imageUrl']
            
            print(card_name)
            print(card_img_url)
            
            filename = card_name + os.path.splitext(card_img_url)[1]
            with open(path+'/'+filename, 'wb') as f:
                '''
                response = requests.post(card_img_url, headers=getHeaders())
                f.write(response.content)
                '''
                request = urllib2.Request(card_img_url)
                response = urllib2.urlopen(request)
                f.write(response.read())
                
            '''
            print('cardCode:', card['cardCode'])
            print('code:', card['code'])
            print('name:', card['name'])
            print('description:', card['description'])
            print('imgUrl:', card['imageUrl'])
            '''
        
        counter += 1
        if counter > data['totalPage']:
            break
        
        time.sleep(1)
    
end = datetime.datetime.now()

print((end - start).seconds)