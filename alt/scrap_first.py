#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import requests
from bs4 import BeautifulSoup
import scrap_functions
from urllib.parse import urlparse
import re
from datetime import date

cur, conn = scrap_functions.connect_properties()
dirname = os.path.dirname(os.path.abspath(__file__)) + '/'

##############################################################
site = 'Firstmallorca'
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
    urls = ['https://www.firstmallorca.com/de/mieten/finca-in-puerto-de-andratx/154838']
    scraped =''


for url in urls:
    pos_url = 0
    pos_url = url.find("?")
    if pos_url > 0:
        url = (url[0:pos_url])
        print (url)
    try:
    #if 1 > 0:
        print (url)
        if 'https://www.firstmallorca.com/de/' in url and url[-2].isdigit() and url not in str(scraped) and '?' not in url :
            print (url)
            headers = {'User-Agent':'Mozilla/5.0'}
            page = requests.get(url)
            pos_ende = page.text.find('button active')
            page_text = page.text[0:pos_ende]
            soup = BeautifulSoup(page_text, 'html.parser')
            #print (soup)

            price = 0
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
            country = 'Spanien'
            country_state = 'Mallorca'#
            property_type = ''
            offer_type =''
            image =''

#            name = soup.find(itemprop="name").get_text().replace(';',' ').replace('\n', '')
            name = (soup.title).get_text().replace(';',' ')
            location = soup.find("div", class_="location").get_text().replace(';',' ')
            location = scrap_functions.strip_accents(location)

            images = []
            for img in soup.findAll('img'):
                if img.get('data-src') != None:
                    images.append(img.get('data-src'))
            image = images[0]
            root_url = str(urlparse(url).scheme) + '://' + str(urlparse(url).hostname)
            if image[0:4] != 'http':
                    image = root_url+image

            str_images = (str(images).replace("'",'').replace("[",'').replace("]",''))

            try:
                price = soup.find("div", class_="currency").get_text()
                price = (re.search('[0-9.]+',price).group(0)).replace('.','')
            except:
                price = 0
#            print (price)

            ref = soup.find("div", class_="ref_id right").get_text()
            ref = ref.split()[2].strip()
            tags = soup.find("div", class_="c_property_icons")
            for tag in tags:
                #print tag
                items = tag.find('div', class_='label').get_text() , tag.find('div', class_='detail').get_text()
                #print (items)
                if items[0] =='Schlafzimmer':
                    bedroom = items[1]
                if items[0] =='Badezimmer':
                    bathroom = items[1]
                if items[0] =='Terrasse':
                    terrace = items[1]
                if items[0] =='Bebaute Fläche':
                    size = items[1]
                    size = (re.search('[0-9.]+',size).group(0)).replace('.','')
                if items[0] =='Grundstück':
                    groundsize = items[1]
                    groundsize = (re.search('[0-9.]+',groundsize).group(0)).replace('.','')
                if items[0] =='Parkplatz':
                    parkplace = items[1]

            print ('Name: ', name)
            #print(bedroom, bathroom, terrace, size, groundsize, parkplace)
            print ('Ref: ',ref)
            print ('Location: ',location)
            print ('Price', price)
            print ('URL', url)

            #f.write(site +';' + str(name) +';' + str(ref) +';' + str(price) +';' + str(location) + ';' + str(bedroom) + ';' + str(bathroom) + ';' + str(terrace) + ';' + str(size) + ';' + str(groundsize) + ';' + str(parkplace) + ';' + url + ';' + str(country) + ';' + str(state) + ';' + str(area) + ';' + str(city) + ';' + str(property_type) + ';' + str(offer_type) + '\n')

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
                    print ('update' , ref , check_ref, price, bedroom, bathroom, size)
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
#f.close
cur.execute("update sites set last_scraped = current_date where site = '" + site + "' ;")
cur.execute("commit;")
scrap_functions.log( site + ' end')
