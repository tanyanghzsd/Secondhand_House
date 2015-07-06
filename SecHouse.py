# -*- coding: utf-8 -*-
import urllib,urllib2,time
from bs4 import BeautifulSoup
import sys,os
import MySQLdb
reload(sys)
sys.setdefaultencoding('utf8')

def addData(name,price):
	conn=MySQLdb.connect(
        host='127.0.0.1',
        port=3306,
        user='root',
        passwd='123',
        db='demo',
        charset='utf8'
    	)

	cur=conn.cursor()
	sql="insert into sechouse(name,price)values('%s','%s')"%(name,price)
	cur.execute(sql)
	conn.commit()
	cur.close()
	conn.close()


	

def get_page(num):
    url='http://cs.anjuke.com/community/W0QQpZ'+str(num)
    headers={'User-Agent':'Mozilla/5.0 (Windows NT 6.1; rv:38.0) Gecko/20100101 Firefox/38.0'}
    req=urllib2.Request(url,headers=headers)
    response=urllib2.urlopen(req)
    page=response.read()
    return page
        
def get_content(page):
    soup=BeautifulSoup(page)
    names=soup.find_all('a',class_='t')
    prices=soup.find_all('span',class_='sp1')
    Names=[]
    Prices=[]
    for name in names:
        name=name.string
        Names.append(name)
        
    for price in prices:
        price=price.string
        Prices.append(price)
    return Names,Prices


for num in range(1,402):
    page=get_page(num)
    Names,Prices=get_content(page)
    for i in range(1,10):
        try:
            print Names[i]+Prices[i]
            addData(Names[i], Prices[i])
        except IndexError:
            print 'list index out of range'
