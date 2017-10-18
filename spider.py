# -*- coding: utf-8 -*-
"""
Created on Tue Oct 17 15:23:56 2017

@author: wkzheng
"""

from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from bs4 import BeautifulSoup
import time
import datetime
import os, urllib2

start = datetime.datetime.now()

user_agent = 'Mozilla/5.0 (Windows NT 10.0; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.81 Safari/537.36'
dcap = dict(DesiredCapabilities.PHANTOMJS)
dcap["phantomjs.page.settings.userAgent"] = (user_agent)
driver = webdriver.PhantomJS()
driver.set_window_size(1124, 850)  # 设置窗口大小，解决某些元素不可视问题
driver.get('http://hs.blizzard.cn/cards/')

# 获取卡牌库的导航栏
ul = driver.find_element_by_css_selector("#cards_data > ul[class='tabs_hero clearFix']")
litags = ul.find_elements_by_tag_name("li")

for li in litags:
    li.click()
    
    time.sleep(1)  # 休眠一下，便于页面触发AJAX，从而进行页面切换
    
    title = driver.find_element_by_css_selector("#cards_data > h3").text
    
    print(title)
    
    path = "./result/" + title
    if not os.path.exists(path):
        os.makedirs(path)

    while True:
         # 下一页按钮
        # https://github.com/ariya/phantomjs/issues/11637
        # 设置窗口大小解决：ElementNotVisibleException: {"errorMessage":"Element is not currently visible and may not be manipulated"
    
        try:
            print('ready to click')
            driver.find_element_by_css_selector("#cards_data > a[class='cards_next']").click()
            print('clicked')
            time.sleep(1) # 休眠一下，便于页面触发AJAX，跳转到下一页
        except Exception: # 找不到那个元素，说明已经到最后一页
            break
            
    print("finish.")
    
    soup = BeautifulSoup(driver.page_source, 'lxml')
    cards_data = soup.find(id='cards_data')
    
    cards = cards_data.find_all("div", class_="cards_place")
    
    for card in cards:
        card_content = card.find("img", class_="card_img")
        card_title = card_content['alt']
        card_img_src = card_content['src']
                    
        print(card_title)
        print(card_img_src)
        '''
        f.write(card_title.encode('utf-8'))
        f.write('\r\n')
        f.write(card_src.encode('utf-8'))
        f.write('\r\n')
        '''
        
        filename = card_title + os.path.splitext(card_img_src)[1]
        with open(path+'/'+filename, 'wb') as f:
            request = urllib2.Request(card_img_src)
            response = urllib2.urlopen(request)
            f.write(response.read())


driver.close()
print('done.')

end = datetime.datetime.now()

print((end - start).seconds)