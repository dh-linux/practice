#!/usr/bin/env python
# -*- encoding:utf-8 -*-
import threading
import os, sys, re
import requests
import json
import chardet
from bs4 import BeautifulSoup


global download_to_page_num, pic_path, headers, lock
download_to_page_num = 2015
pic_path = "/data/jiandan/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.93 Safari/537.36", 
    "Connection": "keep-alive",
    "Cookie": "1306034968=9b29tjJUa0EHKrUWKiHWgtOI2e8yF53eEriDcWoI8w; _gat=1; 1306034968=b4caQ358cSssQtKSrehmQ52k0TJqVhuz%2FfbTb2lkFw; jdna=596e6fb28c1bb47f949e65e1ae03f7f5#1466761110690; Hm_lvt_fd93b7fb546adcfbcf80c4fc2b54da2c=1465353483,1465697168,1465785846,1466734300; Hm_lpvt_fd93b7fb546adcfbcf80c4fc2b54da2c=1466761112; _ga=GA1.2.1757610751.1465353483",
}
lock = threading.RLock()

class download():
    def __init__(self):
        pass
    
    def updated_pic_list(self, page):
        url = 'http://jandan.net/ooxx/page-' + str(page) + '#comments'
        response = requests.get(url, headers = headers )
        
        if response.status_code != 200:
            print "Http code wrong ..."
            sys.exit(2)
        
        pic_list = []
        data = response.content
        soup = BeautifulSoup(data, "lxml")
        for i in soup.find_all("a", class_="view_img_link"):
            pic_list.append(i["href"])
        return pic_list

    def read_page(self):
        lock.acquire()
        if not os.path.exists("./page_num.txt"):
            page = 2026
        else:
            with open("./page_num.txt", "r") as f:
                page = int(f.read())
            newpage = page - 1
            with open("./page_num.txt", "w") as f:
                f.write(str(newpage)) 
        lock.release()
        return page
        
    def download_pic(self):
        page = self.read_page()
        thread_name = threading.currentThread().getName()
        while page >= download_to_page_num:
            print "线程" + thread_name + "正在下载第" + str(page) + "页..." 
            pic_list = self.updated_pic_list(page)
            for pic_url in pic_list:
                pic_name = pic_url.split("/")[-1]
                response = requests.get(pic_url, headers = headers, )    
                with open(pic_path + pic_name, "w") as f:
                    f.write(response.content)
            print "已下载完成第" + str(page) + "页..."
            page = self.read_page()
            
    def begin_download(self):
        t1 = threading.Thread(target=self.download_pic)
        t2 = threading.Thread(target=self.download_pic)
        t1.start()
        t2.start()

if __name__ == '__main__':
    download = download()
    download.begin_download()



    
#print response.encoding
#print requests.utils.get_encodings_from_content(data)
#print chardet.detect(data)
