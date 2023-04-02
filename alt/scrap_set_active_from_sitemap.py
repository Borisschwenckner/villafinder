#!/usr/bin/python3
import psycopg2
import sys, csv, re, os, time
from bs4 import BeautifulSoup
from urllib.parse import urlparse

from datetime import datetime
sys.path.append('/prg/')
sys.path.append('../')

import functions
dirname = os.path.dirname(os.path.abspath(__file__)) + '/'
logfile = dirname + 'logfile.log'
def log(msg):
    file = open(logfile,"a")
    file.write("%s: %s\n" % (time.strftime("%d.%m.%Y %H:%M:%S"), msg))
    file.close

dirname = os.path.dirname(os.path.abspath(__file__)) + '/'
cur, conn = functions.connect_properties()


log('Set active from sitemp ' + ' start')
try:
    cur.execute("commit;")
except:
    pass
files = []
for file in os.listdir(dirname):
    if file.endswith(".xml"):
        print(os.path.join(dirname, file))
        files.append(dirname + file)
print (files)
#files = [ dirname + 'sitemap_porta.xml']
for file in files:
    sitemap_response = open(file)
    soup = BeautifulSoup(sitemap_response, 'lxml')
    elements = soup.findAll("url")
    urls = [elem.find("loc").string for elem in elements]
    domain = urlparse(urls[0]).netloc
    #print (domain)
    cur.execute("update properties set state = 'inactive', inactive_date = current_date   where url like '%" + domain + "%' and state = 'active' and country ='Spanien'")
    cur.execute("commit;")

    for url in urls:
            try:
                cur.execute("update properties set state = 'active', inactive_date = null  where url = '" + url + "';commit;")
                #print ('update' , url )
            except:
                print ('URL nicht vorhanden')


log('Set active from sitemp ' + ' end')

conn.close()
