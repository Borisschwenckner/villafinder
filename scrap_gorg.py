#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import requests, re, time, datetime, psycopg2, sys
from bs4 import BeautifulSoup
from urllib.parse import urlparse
sys.path.append('/prg/')
import scrap_functions

dirname = os.path.dirname(os.path.abspath(__file__)) + '/'
filename = dirname + 'gorg.csv'

site = 'gorg'
try:
    scraped = open(filename_scraped).readlines()
except:
    scraped =''

scrap_functions.log('Gorg start')

urls = ['https://www.emaya.es/ciclo-agua/ciclo-integral-del-agua/captacion/']
cur, conn = scrap_functions.connect_smarthome()

if not os.path.isfile(filename):
    g = open(filename, "w")#
    headers = "site;date; percent;gorg;cuber\n"
    g.write(headers)
    g.close

f = open(filename, "a")
date = str(datetime.datetime.now().strftime("%Y-%m-%d"))

for url in urls:
    try:

        print (url)
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        percent = soup.find("span", id="total").get_text()
        print (percent)
        gorg = soup.find("input", type="hidden", id="gorg")
        cuber = soup.find("input", type="hidden", id="cuber")
        print (gorg['value'], cuber['value'])


        f.write(site +';' + percent +';' + date +';' + gorg['value'] +';' + cuber['value'] + '\n')
        try:
        #if 1>0:
            cur.execute("INSERT INTO log_gorg_blau ( site,  percent,  date, gorg, cuber) \
            values ( %s, %s, %s, %s, %s)" , ( [site,percent,date,gorg['value'], cuber['value']]))
            cur.execute("commit;")
        except:
            pass
    except:
        pass
f.close
scrap_functions.log('Gorg end')
conn.close
