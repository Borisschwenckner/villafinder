#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os, time
import requests #, psycopg2
import scrap_minkner_get_sitemap
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
from datetime import date

import sys
sys.path.append('/prg/')
sys.path.append('../')
import functions
cur, conn = functions.connect_properties()


today = date.today()
day = today.strftime("%d")
print(day)
dirname = os.path.dirname(os.path.abspath(__file__)) + '/'

#---------------------------------------------
testmode = False
#testmode = True

if testmode == True:
    print ('-----------------TESTMODE-----------------')
#---------------------------------------------
##############################################################
site = 'Minkner'
site_short = site.lower()# .split("-")[0]
sitemap_xml =   dirname + 'sitemap_' + site_short + '.xml'
##############################################################

filename = dirname + 'data_' + site_short + '.csv'
filename_scraped = dirname + 'scraped_' + site_short + '.csv'

logfile = dirname + 'logfile.log'
def log(msg):
    file = open(logfile,"a")
    file.write("%s: %s\n" % (time.strftime("%d.%m.%Y %H:%M:%S"), msg))
    file.close


if (day == '02' or day == '12' or  day == '22' ):
    cur.execute("delete from scraped  where site = '" + site + "' and scrap_it = 1 ")
    cur.execute("commit;")
    log(site_short + ' Scraped geloescht')

try:
    #scraped = open(filename_scraped).readlines()
    cur.execute("select url from scraped  where site = '" + site + "' ")
    rows = cur.fetchall()
    scraped = ''
    for row in rows:
        scraped = scraped + row[0] + '\n'
except:
    scraped =''


if testmode == True:
    scraped =''
    log(site_short + ' ----------------------------TESTMODUS --------------------------------------')

log(site_short + ' start')

if testmode != True:
    scrap_minkner_get_sitemap.fullscan()



#locale sitemap
sitemap_response = open(sitemap_xml)
soup = BeautifulSoup(sitemap_response, 'lxml')
elements = soup.findAll("url")
urls = [elem.find("loc").string for elem in elements]

if testmode == True:
    urls = ['https://www.minkner.com/expose/567960/']

#if not os.path.isfile(filename):
#    f = open(filename, "w")#
#    headers = "site;name;ref;price;location;bedroom;bathroom;terrace;size;groundsize;parkplace;url;country;state;area;city;property_type;offer_type\n"
#    f.write(headers)
#    f.close
#f = open(filename, "a")


for url in urls:
    #if 1 > 0:
    try:
        url = url.replace('minkner.es', 'minkner.com')
        if 'minkner' in url and url[-2].isdigit() and url + '\n' not in scraped and '?' not in url :

            #i = open(filename_scraped, "a")
            #i.write (url + '\n')
            #i.close
            price = ''
            bathroom = 0
            bedroom = 0
            terrace = ''
            size = 0
            groundsize = 0
            parkplace = ''
            country = ''
            location = ''
            area = ''
            state = ''
            city = ''
            carpark = ''#
            country_state = ''#
            property_type = ''
            offer_type =''

            print (url)
            headers = {'User-Agent':'Mozilla/5.0'}
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'lxml')
            name = (soup.title).get_text().replace(';',' ')
            print (name)
            location = soup.find("span", class_="location").get_text().replace(';',' ')
            print (location)
            country = 'Spanien'

            try:
                price = soup.find("span", class_="listing-price-value").get_text()
                print (price)
                price = (re.search('[0-9.]+',price).group(0)).replace('.','')
                print (price)
            except:
                price = 0
            ref = soup.find("div", class_="wpsight-listing-id"  ).get_text()
            pos1 = ref.find("Ref:")+4
            ref =  (ref[pos1:20].strip())
            print (ref, pos1)
            tags = soup.find("div", class_="listing-details-box")
            groundsize = soup.find("div", class_="listing-details-box listing-details-box-details_3").get_text().strip()
            print (groundsize)
            size = soup.find("div", class_="listing-details-box listing-details-box-details_4").get_text().strip()
            print (size)
            bedroom = soup.find("div", class_="listing-details-box listing-details-box-details_1").get_text().strip()
            print (bedroom)
            bathroom = soup.find("div", class_="listing-details-box listing-details-box-details_2").get_text().strip()
            print (bathroom)
            #f.write(site +';' + name +';' + str(ref) +';' + str(price) +';' + str(location) + ';' + str(bedroom) + ';' + str(bathroom) + ';' + str(terrace) + ';' + str(size) + ';' + str(groundsize) + ';' + str(parkplace) + ';' + url + '\n')

            if groundsize == '':
                groundsize = 0
            if bedroom == '':
                bedroom = 0
            if bathroom == '':
                bathroom = 0
            if size == '':
                size = 0

            check_ref = 0
            cur.execute("select id from properties where url = '" + url + "' ;")
            try:
                check_ref = cur.fetchone()[0]
            except:
                check_ref = 0


            print (check_ref)
            #print (name,  price, bedroom, bathroom , size, groundsize, location, carpark, terrace, ref,  offer_type, property_type, country_state, area, city , country, check_ref)
            try:
                cur.execute("commit;")
            except:
                pass
            if check_ref > 0:
                try:
                #if 1 >0:
                    cur.execute("update properties set write_date = current_date , last_scraped_date = current_date ,state = 'active', name  = %s , price = %s, bedroom = %s , bathroom = %s, living_size = %s, ground_size = %s, location = %s , carpark = %s, terace = %s, ref = %s , offer_type = %s , property_type = %s , country_state = %s , area = %s , city = %s , country = %s where id = %s" ,
                    ([name,  price, bedroom, bathroom , size, groundsize, location, carpark, terrace, ref,  offer_type, property_type, country_state, area, city , country, check_ref]))
                    cur.execute("commit;")
                    print ('update' , ref , check_ref, price, bedroom, bathroom)
                except:
                    pass
            else:
                print ('insert',ref,  name, site, bedroom, bathroom)
                cur.execute("INSERT INTO properties ( create_date,write_date, last_scraped_date, state, site, name, ref, price, location, bedroom, bathroom, terace, living_size, ground_size, carpark, url, offer_type, property_type, country_state, area, city, country) \
                values ( current_date,current_date, current_date,'active', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" , ( [site ,name, ref ,price, location,bedroom, bathroom, terrace, size, groundsize , carpark, url, offer_type, property_type, country_state, area, city, country]))
                conn.commit()
                print ("Insert Done")

            try:
                cur.execute("commit;")
            except:
                pass
            try:
                cur.execute("INSERT INTO scraped ( site, url) values ( %s, %s)" , ( [site ,url]))
                cur.execute("commit;")
            except:
                pass




    except:
        pass
#f.close
log(site_short + ' end')
