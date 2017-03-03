# -*- coding:utf-8 -*-
#!/usr/bin/env python

__auther__ = 'xiaohuahu94@gmail.com'
'''
爬害羞组照片
'''
import requests
from bs4 import BeautifulSoup
import urllib,urllib2
import re
import os
import sys,time
requests.adapters.DEFAULT_RETRIES = 5   
def SaveImage(addr):
  try:	                    
 	u=requests.get(addr)  
 	data = u
 	splitPath = addr.split('/')
 	fName = splitPath.pop()
 	now = time.strftime("%Y-%m-%d %H:%M:%S")
	print fName,'saved',now
	sentence = " osascript -e 'display notification \"lol\" with title \"Completed\"' "
	os.system(sentence)
	f= open(fName,'wb')
 	f.write(data.content)
 	f.close()
  except Exception,e:
 	print 'failed : '+str(e)

def GetLinkList():
	start_item = 400    #从第start_item条开始爬
	all_link_list = []
	while(1):
	    time.sleep(1)
	    main_page_url = 'https://www.douban.com/group/haixiuzu/discussion?start='
	    detail_page_url = main_page_url + str(start_item)
	    start_item += 25
	    response_main = requests.get(detail_page_url)
	    re_title_link = re.compile(r'https://www\.douban\.com/group/topic/[0-9]{8}')
	    link_list = re.findall(re_title_link,response_main.content)
	    all_link_list.extend(link_list)
	    if start_item == 500:
	    	return all_link_list
	    	break
def isContinue():
	continue_flag = os.path.isfile('status.txt')
	if(continue_flag):
		print 'continue'
		'''
		todo 把txt的list信息导入到新list 然后断点继续
		'''
		fd = open('status.txt','r')
		list_str = fd.read()
		re_link = re.compile(r'https://www\.douban\.com/group/topic/[0-9]{8}')
		detail_page_list = re.findall(re_link,list_str)
		if detail_page_list == []:
			os.remove('status.txt')
		else:
			main(detail_page_list)
	else:
		detail_page_list = GetLinkList()
		main(detail_page_list)
def main(detail_page_list):
	while(1):
		detail_link = detail_page_list.pop()
		sfile = open('status.txt','w')
		sfile.write(str(detail_page_list))
		sfile.close()
		response_detail = requests.get(detail_link)
		re_img_link = re.compile(r'https://img[0-9]{1}\.doubanio\.com/view/group_topic/large/public/p[0-9]{8}\.jpg')
		img_link_list = re.findall(re_img_link,response_detail.content)
		#print img_link_list
		for i in range(len(img_link_list)):
			time.sleep(0.5)
			SaveImage(img_link_list.pop())
		if detail_page_list == []:
			os.remove('status.txt')
			break
	#print link_list
if __name__ =='__main__':
	isContinue()


