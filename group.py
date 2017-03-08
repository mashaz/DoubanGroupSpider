# -*- coding:utf-8 -*-
#!/usr/bin/env python

__auther__ = 'xiaohuahu94@gmail.com'

'''
豆瓣小组图片爬虫  todo: 	加入代理池
						多线程
'''

import requests
from bs4 import BeautifulSoup
import urllib,urllib2
import re
import os
import sys,time,platform
import random

requests.adapters.DEFAULT_RETRIES = 5 

def SaveImage(addr):
  try:	                    
 	u=requests.get(addr)  
 	data = u
 	splitPath = addr.split('/')
 	fName = splitPath.pop()
 	now = time.strftime("%Y-%m-%d %H:%M:%S")
	print fName,'saved',now
	#macOS右上角弹窗脚本
	#sentence = " osascript -e 'display notification \"lol\" with title \"Completed\"' "
	#os.system(sentence)
	fName = 'images/' + fName
	f = open(fName,'wb')
 	f.write(data.content)
 	f.close()
  except Exception,e:
 	print 'failed : '+str(e)

def GetLinkList(gname,endnum):
	start_item = 0    #从第start_item条开始爬
	all_link_list = [gname]
	while(1):
	    time.sleep(2)
	    main_page_url = 'https://www.douban.com/group/'+gname+'/discussion?start='
	    detail_page_url = main_page_url + str(start_item)
	    start_item += 25
	    response_main = requests.get(detail_page_url)
	    re_title_link = re.compile(r'https://www\.douban\.com/group/topic/[0-9]{8}')
	    link_list = re.findall(re_title_link,response_main.content)
	    all_link_list.extend(link_list)
	    if start_item >= endnum:   
	    	return all_link_list
	    	break
def statusContinue():  
	'''
	把txt的list信息导入到新list 然后断点继续
	'''
	fd = open('status.txt','r')
	list_str = fd.read()
	re_link = re.compile(r'https://www\.douban\.com/group/topic/[0-9]{8}')
	gname_list = list_str.split(',');
	gname = gname_list[0].strip('"').strip("[").strip("'")
	detail_page_list = [str(gname)]
	detail_page_list.extend(re.findall(re_link,list_str)) 
	if detail_page_list == []:
		print 'status.txt无信息,删除ed'
		os.remove('status.txt')
	else:
		gname = detail_page_list[0]
		print '继续爬取%s小组...'%(gname)
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
		if len(detail_page_list) == 1: #剩gname
			os.remove('status.txt')
			break

def main():
	if not os.path.exists('images'):
			os.mkdir('images')
			print '同级目录下新建立images中'
			print '...'
			time.sleep(2)
			print '新建成功'
 	if len(sys.argv) == 1:          
 		if  os.path.exists('status.txt'):  #有status继续
			statusContinue()
		else:
			gname_list = ['haixiuzu','505473','515923','tsgwk','600490','505137','503413',
			'511274','rouniu','qfatty','368701','36093','103485','miniskirtlegs','515085']
			gname = random.choice(gname_list)
			print '爬取%s小组,默认爬取300条记录'%(gname)
			all_link_list = GetLinkList(gname,'300')
			GetImages(all_link_list) 
	else:  
	#长度不为1
		if sys.argv[1].startswith('--'):     
			option = sys.argv[1][2:]     
			if (option == 'version'): 
			    print 'version 0.2'    
			elif (option == 'help'):     
			    print '=============豆瓣小组扫图============='
			    print 'Format :'
			    print '1. python group.py #自动推荐小组开始爬or继续爬'
			    print 
			    print '2. python group.py group_name #指定小组名开始爬or继续爬'
			    print
			    print '3. python group.py  group_name -number #指定小组名 指定帖子条目数开始爬'
		else:
			if len(sys.argv) == 2 :  #指定小组，先判断status
				gname = sys.argv[1]
				fd = open('status.txt','r')
				fd_str = fd.read()
				gname_list = fd_str.split(',');
				gname_status = gname_list[0].strip('"').strip("[").strip("'")
				if gname == gname_status:
					print '继续爬取%s小组'%(gname)
					statusContinue()
				else:
					os.remove('status.txt')
					print '开始爬取%s小组'%(gname)
		    		all_link_list = GetLinkList(gname,'300')
		    		GetImages(all_link_list) 
			if len(sys.argv) == 3 : 
				gname = sys.argv[1]
				endnum = sys.argv[2]
				if endnum[0]!='-':
					print '无效参数!'
				else:
					if os.path.exists('status.txt'):
						os.remove('status.txt')
					endnum = endnum.lstrip('-')
					print '爬取%s小组%s条记录'%(gname,endnum)
					endnum=int(endnum)
					all_link_list = GetLinkList(gname,endnum)
		    		GetImages(all_link_list) 
if __name__ =='__main__':
	main()


