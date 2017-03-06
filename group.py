# -*- coding:utf-8 -*-
#!/usr/bin/env python

__auther__ = 'xiaohuahu94@gmail.com'

'''
豆瓣小组照片  todo: 
					默认抓取第0-100帖  需改进到命令行参数传入
					默认害羞组  需自动推荐小组
					加入代理池
					多线程
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
	fName = 'images/' + fName
	f = open(fName,'wb')
 	f.write(data.content)
 	f.close()
  except Exception,e:
 	print 'failed : '+str(e)

def GetLinkList(gname):
	start_item = 0    #从第start_item条开始爬
	all_link_list = []
	while(1):
	    time.sleep(2)
	    main_page_url = 'https://www.douban.com/group/'+gname+'/discussion?start='
	    detail_page_url = main_page_url + str(start_item)
	    start_item += 25
	    response_main = requests.get(detail_page_url)
	    re_title_link = re.compile(r'https://www\.douban\.com/group/topic/[0-9]{8}')
	    link_list = re.findall(re_title_link,response_main.content)
	    all_link_list.extend(link_list)
	    if start_item > 100:   
	    	return all_link_list
	    	break
def isContinue():  
	continue_flag = os.path.isfile('status.txt')
	if(continue_flag):
		print 'continue'
		'''
		把txt的list信息导入到新list 然后断点继续
		'''
		fd = open('status.txt','r')
		list_str = fd.read()
		re_link = re.compile(r'https://www\.douban\.com/group/topic/[0-9]{8}')
		detail_page_list = re.findall(re_link,list_str)
		if detail_page_list == []:
			os.remove('status.txt')
		else:
			GetImages(detail_page_list)
	else:
		detail_page_list = GetLinkList('haixiuzu')  # todo 把gname传进来1   
		'''
		无status.txt，则新抓取链接
		'''
		GetImages(detail_page_list)
def GetImages(detail_page_list):
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
			time.sleep(1.5)
			SaveImage(img_link_list.pop())
		if detail_page_list == []:
			os.remove('status.txt')
			break
	#print link_list
def main():
	if  os.path.exists('status.txt'):
		print 'continue' #todo
	else:
 		if len(sys.argv) == 1:
			if not os.path.exists('images'):
				os.mkdir('images')
				print '同级目录下新建立images中'
				print '...'
				time.sleep(2)
				print '新建成功'
			isContinue()
		else:
			if sys.argv[1].startswith('--'):     
				option = sys.argv[1][2:]     
				if (option == 'version'): 
				    print 'version 0.2'    
				elif (option == 'help'):     
				    print '=============豆瓣小组扫图============='
				    print 'Format :'
				    print '1. python group.py #自动推荐小组'
				    print 
				    print '2. python group.py group_name #指定小组名'
			else:
				if len(sys.argv) == 2 :
					gname = sys.argv[1]
			    	all_link_list = GetLinkList(gname)
			    	GetImages(detail_page_list) 
	
if __name__ =='__main__':
	main()


