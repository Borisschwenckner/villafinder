#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import requests, re, time
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import date
import scrap_functions
from datetime import date

cur, conn = scrap_functions.connect_properties()
dirname = os.path.dirname(os.path.abspath(__file__)) + '/'

##############################################################
site = 'Sandberg'
##############################################################

scrap_functions.log( site + ' start')
testmode =  scrap_functions.check_testmode(site)

if testmode == False:
    cur.execute("select count(id)  from sites  where last_scraped = current_date and site = '" + site + "' " )
    qty = cur.fetchone()
    if qty[0] > 0:
        scrap_functions.log( site + ' Diese Seite wurde heute schon gescraped - end')
        print('Diese Seite wurde heute schon gescraped')
        exit()
    scrap_functions.get_sitemap_extended(site)
    scrap_functions.create_propertys_from_sitemap(site)


if testmode == True:
    urls = ['https://sandberg-estates.com/properties/finca-on-a-large-plot-for-sale-between-santa-maria-and-bunyola/']
    scraped =''

cur.execute("update sites set last_scraped = current_date where site = '" + site + "' ;")
cur.execute("commit;")
scrap_functions.log( site + ' end')
