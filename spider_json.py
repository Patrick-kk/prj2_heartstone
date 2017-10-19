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


import requests
import time, datetime
import os
import random



# 由于多次爬页面会发生 connection aborted 问题
# 考虑使用 user_agent 轮询方式
def getHeaders():
    user_agent = [
                  'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36',
                  'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.10240',
                  'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 10.0; WOW64; Trident/8.0; .NET4.0C; .NET4.0E; .NET CLR 2.0.50727; .NET CLR 3.0.30729; .NET CLR 3.5.30729; Zoom 3.6.0)',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64; rv:34.0) Gecko/20100101 Firefox/34.0',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) ',
                  'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Maxthon/4.4.3.4000 Chrome/30.0.1599.101 Safari/537.3',
                  'Mozilla/5.0 (Windows NT 5.1) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.84 Safari/535.11 SE 2.X MetaSr 1.0'
                  ]
    
    headers = {'User-Agent': user_agent[random.randint(0, len(user_agent)-1)], 
#           'Referer': 'http://hs.blizzard.cn/cards/',
#           'Cookie': '_ntes_nnid=4669facd3c478451e5ef2309e5b7e4f9,1508205173137',
#           'X-Requested-With': 'XMLHttpRequest',
           'Connection': 'close'
           }
    
    return headers


start = datetime.datetime.now()


r = requests.get('http://hs.blizzard.cn/action/cards/query')

#print(r.text)

data = r.json()

# 为了获取总共有多少cardclass
totalPerClass = data['totalPerClass']

for key in totalPerClass:
    print('CardClass:', key)
    
    path = "./result_json/" + key
    if not os.path.exists(path):
        os.makedirs(path)
    
    counter = 1  # 设置初始页码
    while True:

        try_counter = 5
        while True:
            try:
                payload = {'cardClass':key, 'p':counter, 'standard':1} 
                r = requests.post('http://hs.blizzard.cn/action/cards/query', params=payload, headers=getHeaders())
                break
            except Exception:
                print('======== failed to connect...')
                if try_counter < 0:
                    r = None
                    break
        
        if r == None:
            print('发生连接错误，超出重试次数，退出程序')
            break
        
        data = r.json()

        cards = data['cards']
        
        for card in cards:
            card_name = card['name']
            card_img_url = card['imageUrl']
            
            print(card_name)
            print(card_img_url)
            
            filename = card_name + os.path.splitext(card_img_url)[1]
            with open(path+'/'+filename, 'wb') as f:
                response = requests.get(card_img_url)
                f.write(response.content)

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