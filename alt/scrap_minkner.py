#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os, time
import requests #, psycopg2
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import re
import scrap_functions
from datetime import date

cur, conn = scrap_functions.connect_properties()
dirname = os.path.dirname(os.path.abspath(__file__)) + '/'


##############################################################
site = 'Minkner'
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
    scraped = scrap_functions.load_scraped(site)
    scrap_functions.get_sitemap_extended(site)
    urls= scrap_functions.load_sitemap(site)
    #print (urls)


if testmode == True:
    urls = ['https://www.minkner.com/expose/642832/']
    scraped =''


for url in urls:
    #if 1 > 0:
    try:
        url = url.replace('minkner.es', 'minkner.com')
        if 'minkner' in url and url[-2].isdigit() and url + '\n' not in scraped and '?' not in url :
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
            soup = BeautifulSoup(page.text, 'html.parser')
            name = (soup.title).get_text().replace(';',' ')
            #print (name)
            location = soup.find("span", class_="location").get_text().replace(';',' ')
            location = scrap_functions.strip_accents(location)
            country = 'Spanien'

            image_meta = soup.find("meta",  {"property":"og:image"})
            image = (image_meta["content"] if image_meta else None)

            images = []
            for img in soup.findAll('img'):
                #print(img)
                try:
                    if (img['data-lazy-src']) != None and 'uploads' in str(img['data-lazy-src']) and (str(img['data-lazy-src'])[-6].isdigit() or str(img['data-lazy-src'])[-12].isdigit() )  and ('.jpg'  in str(img['data-lazy-src']) or '.webp'  in str(img['data-lazy-src']))   and 'Katalog' not in str(img['data-lazy-src']) :
                        images.append((img['data-lazy-src']))
                except:
                    pass
            root_url = str(urlparse(url).scheme) + '://' + str(urlparse(url).hostname)
            if image == None:
                try:
                    image = images[0]
                    if image[0:4] != 'http':
                        image = root_url+image
                except:
                    pass

            str_images = (str(images).replace("'",'').replace("[",'').replace("]",''))
            print('#########################################')
            print(str_images)
            print (image)
            print('#########################################')



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
                print ('Update')
                try:
                #if 1> 0:
                    cur.execute("update properties set write_date = current_date , last_scraped_date = current_date ,state = 'active', name  = %s , price = %s, bedroom = %s , bathroom = %s, living_size = %s, ground_size = %s, location = %s , carpark = %s, terace = %s, ref = %s , offer_type = %s , property_type = %s , country_state = %s , area = %s , city = %s , country = %s , image_url = %s, images = %s where id = %s" ,
                    ([name,  price, bedroom, bathroom , size, groundsize, location, carpark, terrace, ref,  offer_type, property_type, country_state, area, city , country, image, str_images, check_ref]))
                    cur.execute("commit;")
                    print ('update' , ref , check_ref, price, bedroom, bathroom)
                except:
                    pass
            else:
                print ('insert',ref,  name, site, bedroom, bathroom)
                cur.execute("INSERT INTO properties ( create_date,write_date, last_scraped_date, state, site, name, ref, price, location, bedroom, bathroom, terace, living_size, ground_size, carpark, url, offer_type, property_type, country_state, area, city, country, image_url, images) \
                values ( current_date,current_date, current_date,'active', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" , ( [site ,name, ref ,price, location,bedroom, bathroom, terrace, size, groundsize , carpark, url, offer_type, property_type, country_state, area, city, country, image, str_images]))
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

cur.execute("update sites set last_scraped = current_date where site = '" + site + "' ;")
cur.execute("commit;")
scrap_functions.log( site + ' end')
