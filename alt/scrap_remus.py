#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os, time
import requests #, psycopg2
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.request import urlretrieve
import re
import scrap_functions
from datetime import date

cur, conn = scrap_functions.connect_properties()
dirname = os.path.dirname(os.path.abspath(__file__)) + '/'

##############################################################
site = 'Remus'
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
    urls = ['https://marcelremusrealestate.com/immobilien/sol-de-mallorca-villa-in-einzigartiger-lage-in-sol-de-mallorca-40484/']
    scraped =''


for url in urls:
    try:
    #if 1 > 0:
        if 'marcelremusrealestate' in url  and url + '\n' not in scraped and '?' not in url :
            print (url)
            headers = {'User-Agent':'Mozilla/5.0'}
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')
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
            country_state = 'Mallorca'#
            property_type = ''
            offer_type =''

            name =  soup.find("h1", class_="expose__title").get_text().replace(';',' ').strip()
            if name == None:
                name =  soup.find("title").get_text().replace(';',' ').strip()
            print ("name:" , name)
            location = ''
            location = soup.find("div", class_="col-6 expose__details__item expose__details__item--value border-bottom").get_text().replace(';',' ').replace(':',' ').strip()
            print (location)
            location = scrap_functions.strip_accents(location)
            country = 'Spanien'
            price = 0
            try:
                price = soup.find("div", class_="expose__details__main-item-value expose__details__main-item-value--price").get_text().replace(';',' ').replace(':',' ').strip()
                print (price)
                price = (re.search('[0-9.]+',price).group(0)).replace('.','')
                print (price)
            except:
                price = 0
            print ('price', price)
            ref = soup.find("div", class_="expose__details__main-item-value"  ).get_text().replace(';',' ').replace(':',' ').strip()
            #pos1 = ref.find("Ref:")+4
            #ref =  (ref[pos1:20].strip())
            print ('ref',ref)
            tags = soup.find("div", class_="listing-details-box")
            groundsize = soup.find("div", class_="col-6 col-md-5 expose__details__item expose__details__item--value border-bottom").get_text().replace(';',' ').replace(':',' ').replace('m2','').strip()
            try:
                groundsize = ''.join([n for n in groundsize if n.isdigit()]).replace('²','')
            except:
                groundsize = 0
            print (groundsize)
            size = soup.find("div", class_="col-6 expose__details__item expose__details__item--value").get_text().replace(';',' ').replace(':',' ').replace('m2','').strip()
            try:
                size = ''.join([n for n in size if n.isdigit()]).replace('²','')
            except:
                size = 0
            print (size)
            bedroom = soup.find("div", class_="col-6 col-md-4 expose__details__item expose__details__item--value border-bottom").get_text().replace(';',' ').replace(':',' ').strip()
            print (bedroom)
            bathroom = soup.find("div", class_="col-6 col-md-4 expose__details__item expose__details__item--value border-bottom").get_text().replace(';',' ').replace(':',' ').strip()
            print (bathroom)

            #img = soup.findAll("div", class_="expose__main-image") #.get_text().replace(';',' ').replace(':',' ').strip()
            image_meta = soup.find("meta",  {"property":"og:image"})
            image = (image_meta["content"] if image_meta else None)

            images=[]
            for img in soup.findAll("div", class_="expose__main-image") :
                #print(img)
                try:
                    images.append( img.get('style').replace("background-image: url('",'').replace("');",""))
                except:
                    pass
            root_url = str(urlparse(url).scheme) + '://' + str(urlparse(url).hostname)
            if image[0:4] != 'http':
                    image = root_url+image

            image = images[0]
            str_images = (str(images).replace("'",'').replace("[",'').replace("]",''))
            print('#########################################')
            #print(str_images)
            print (image)
            print('#########################################')


            if groundsize == '':
                groundsize = 0
            if bedroom == '':
                bedroom = 0
            if bathroom == '':
                bathroom = 0
            if size == '':
                size = 0


#------------------------------start update procedere
            check_ref = 0
            cur.execute("select id from properties where url = '" + url + "' ;")
            try:
                check_ref = cur.fetchone()[0]
            except:
                check_ref = 0
            print ( 'Check Ref mit wwww', check_ref)

            if check_ref == 0:
                cur.execute("select id from properties where url like '" + url.replace('www.','').replace('https://','%') + "' ;")
                try:
                        check_ref = cur.fetchone()[0]
                except:
                        check_ref = 0
                print ('Check Ref ohne wwww', check_ref)

            try:
                cur.execute("commit;")
            except:
                pass

            if check_ref > 0:
                print ('Update')
                try:
                #if 1> 0:
                    cur.execute("update properties set write_date = current_date , last_scraped_date = current_date ,state = 'active',  url  = %s ,name  = %s , price = %s, bedroom = %s , bathroom = %s, living_size = %s, ground_size = %s, location = %s , carpark = %s, terace = %s, ref = %s , offer_type = %s , property_type = %s , country_state = %s , area = %s , city = %s , country = %s , image_url = %s, images = %s where id = %s" ,
                    ([url, name,  price, bedroom, bathroom , size, groundsize, location, carpark, terrace, ref,  offer_type, property_type, country_state, area, city , country, image, str_images, check_ref]))
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
#-------------------------end update

    except:
        pass
#f.close
cur.execute("update sites set last_scraped = current_date where site = '" + site + "' ;")
cur.execute("commit;")
scrap_functions.log( site + ' end')
