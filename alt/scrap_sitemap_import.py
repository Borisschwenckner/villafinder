#!/usr/bin/python3
import psycopg2
import sys, csv, re, os, time
from datetime import datetime
from bs4 import BeautifulSoup
sys.path.append('/prg/')
sys.path.append('../')

import functions
#conn = psycopg2.connect(database='properties', host='nauticon.de', user='postgres' ,  password = 'Webfor:;2014', sslmode='verify-ca' , sslcert='/root/.postgresql/postgresql.crt',  sslkey='/root/.postgresql/postgresql.key')
dirname = os.path.dirname(os.path.abspath(__file__)) + '/'
cur, conn = functions.connect_properties()
files = []
for file in os.listdir(dirname):
    if file.endswith(".xml") and file.startswith("sitemap_"):
#        print(os.path.join(dirname, file))
        files.append(dirname + file)
#print (files)
site = 'DC-Mallorca'
files = [ dirname + 'sitemap_dc.xml']
cur.execute("delete from sitemap  where site = '" + site + "' ")
cur.execute("commit;")

for file in files:
    print (file)
    csv_filename = os.path.basename(file) +'.csv'
    print(csv_filename)

    dst = ''
    dst = ( dirname + 'sicher/' + os.path.basename(file) + '_' + datetime.strftime(datetime.now(), '%Y_%m_%d'))

    sitemap_response = open(file)
    soup = BeautifulSoup(sitemap_response, 'lxml')
    elements = soup.findAll("url")
    urls = [elem.find("loc").string for elem in elements]
    start = time.time()
    f = open(csv_filename, "a")
    for url in urls:
        f.write(url +';\n')
        cur.execute("INSERT INTO sitemap ( site, url) values ( %s, %s)" , ( [site ,url]))

    f.close
    cur.execute("commit;")
    ende = time.time()
    print('{:5.3f}s'.format(ende-start))

#    print (urls)
conn.close()
