#!/usr/bin/python3
import psycopg2
import sys, csv, re, os, time
from datetime import date
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import timedelta
from datetime import datetime
import scrap_functions

dirname = os.path.dirname(os.path.abspath(__file__)) + '/'
something_to_check = 0

start = time.time()
scrap_functions.log('Start Scratching')
cur, conn = scrap_functions.connect_properties()
cur.execute("select site, create_property_from_sitemap, sitemap_items_qty from sites where create_property_from_sitemap >0 and state =1 and last_scraped != current_date order by id; " )
rows = cur.fetchall()
for row in rows:
    site =''
    site = row[0]
    start2 = time.time()
    scrap_functions.log('Start '+site)
    scrap_functions.get_sitemap_extended(site)
    if row[1] ==1:
        scrap_functions.create_propertys_from_sitemap(site)
    elif row[1]==2:
        scrap_functions.get_details(site)
#    duration_site = ('{:5.2f}s'.format(time.time()-start2))
    duration_site = str(scrap_functions.convert_seconds(time.time()-start2))
    scrap_functions.log('End '+site+ ' ' + duration_site)
    qty_in_stitemap_last_time = float(row[2])
    qty_in_sitemap = float(len(scrap_functions.load_sitemap_all(site)))
    if qty_in_sitemap > qty_in_stitemap_last_time *0.8:
        something_to_check = 1
        cur.execute("update sites set last_scraped = current_date , sitemap_items_qty = %s where site = %s ;", ([qty_in_sitemap, site]))
        cur.execute("commit;")
    else:
        subject = 'Nicht genug Einträge in Sitemap ' + site
        x = scrap_functions.email_html("boris@schwenckner.net", subject, ' ')


duration = str(scrap_functions.convert_seconds(time.time()-start))

scrap_functions.log('End  Scratching -----------------------' +duration)



if something_to_check ==1:
    scrap_functions.database_service()
    scrap_functions.set_inactive()
    scrap_functions.set_locations()
    #scrap_functions.images_download()
    scrap_functions.image_one_download()
    scrap_functions.db_checks()
    scrap_functions.mail('Minkner')


duration = str(scrap_functions.convert_seconds(time.time()-start))
print (duration)
scrap_functions.log('End Total Time: ' + duration)

conn.close()
