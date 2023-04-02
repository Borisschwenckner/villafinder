#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import requests, re, time
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import date
import scrap_functions

cur, conn = scrap_functions.connect_properties()
dirname = os.path.dirname(os.path.abspath(__file__)) + '/'

##############################################################
site = 'Engel & Völkers'
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
    missing_urls = scrap_functions.missing_urls_try_again(site)
    urls += missing_urls
    #print (urls)


if testmode == True:
    urls = ['https://www.engelvoelkers.com/de-es/exposes/eklektische-villa-mit-aussergewoehnlichem-spa-in-den-son-vida-hills-palma-de-2100800.1286317_exp/']
    scraped =''



for url in urls:
    try:
    #if 1 > 0:
        if '_exp' in url  and url + '\n' not in scraped and '?' not in url :
            print (url)
            price = 0
            bathroom = 0
            bedroom = 0
            name = ''
            ref = ''
            location =''
            terrace = ''
            size = 0
            groundsize = 0
            parkplace = ''
            country = ''
            area = ''
            state = ''
            city = ''
            property_type = ''
            country_state = ''
            offer_type =''
            carpark =''
            page = requests.get(url)
            soup = BeautifulSoup(page.text, 'html.parser')
            name = soup.find(class_="ev-exposee-title ev-exposee-headline").get_text().strip().replace(';',' ')
            try:
                location =  soup.find("div", class_="ev-teaser-subtitle").get_text().replace(';',' ')
            except:
                location = ''
            if location == '':
                print ('Location ist leer')
                try:
                    location =  soup.find("div", class_="ev-exposee-content ev-exposee-subtitle").get_text().replace(';',' ').strip().split("|")[1]
                except:
                    location = ''
            location = scrap_functions.strip_accents(location)
            try:
                country = (location.split(","))[0].strip()
            except:
                country = 'Spanien'
            try:
                country_state = (location.split(","))[1].strip()
            except:
                country_state = ''
            try:
                area = (location.split(","))[2].strip()
            except:
                area = ''
            try:
                city = (location.split(","))[3].strip()
            except:
                city = ''

            try:
                offer_type =   soup.find("div", class_="ev-exposee-content ev-exposee-subtitle").get_text().split("|")[0].split(",")[1].strip()
                offer_type = offer_type.replace('Kauf','Buy').replace('Miete','Rent')
            except:
                offer_type = ''



            image_meta = soup.find("meta",  {"property":"og:image"})
            image = (image_meta["content"]+'.jpg' if image_meta else None)

            images=[]
            for img in soup.findAll("img", class_="ev-image-gallery-image") :
                try:
                    images.append( img.get('src')+'.jpg')#.replace("background-image: url('",'').replace("');",""))
                except:
                    pass
            image = images[0]
            root_url = str(urlparse(url).scheme) + '://' + str(urlparse(url).hostname)
            if image[0:4] != 'http':
                    image = root_url+image
            str_images = (str(images).replace("'",'').replace("[",'').replace("]",''))
            print('#########################################')
            #print(str_images)
            print (image)
            print('#########################################')




            try:
                property_type =  soup.find("div", class_="ev-exposee-content ev-exposee-subtitle").get_text().split("|")[0].split(",")[0].strip()
            except:
                property_type = ''

            scrapit = 0
            if 'Mallorca' in location:
                scrapit = 1
            print(scrapit)
            try:
                ref =  soup.find("span", class_="displayId hidden").get_text()
            except:
                ref = 'unknown'
            print (ref)
            refs = []

            #description = soup.find(itemprop="description").get_text()
            price = 0
            try:
                price = soup.findAll('span', itemprop="price")[0].text.replace(',','.')
                price = (re.search('[0-9.]+',price).group(0)).replace('.','')
            except:
                price = 0
            print (price)

            tags = soup.find("div", class_="ev-key-facts")


            country = 'Spanien'
            for tag in tags:
                #print ('Tag: ', tag)
                try:
                        items = tag.find('div', class_='ev-key-fact-title').get_text() , tag.find('div', class_='ev-key-fact-value').get_text()
                        print (items)
                        if items[0] =='Schlafzimmer':
                            bedroom = (re.search('[0-9.]+',items[1]).group(0)).replace('.','').replace(',','.')
                        if items[0] =='Badezimmer':
                            bathroom = (re.search('[0-9.]+',items[1]).group(0)).replace('.','').replace(',','.')
                        if items[0] =='Wohnfläche ca.' or items[0] =='Gesamtfl. ca.':
                            size = (re.search('[0-9.]+',items[1]).group(0)).replace('.','').replace(',','.')
                        #    size = size.replace(',','.')
                        if items[0] =='Grundstück ca.':
                            groundsize = (re.search('[0-9.]+',items[1]).group(0)).replace('.','').replace(',','.')

                        if items[0] =='Objektunterart':
                            print(items[1])
                        if items[0] =='E&V ID':
                            ref = (items[1])

                except:
                    pass

            print ('ref' , ref)
            print ('url' , url)
            print ('name', name)
            print ('price' , price)
            print ('bedroom' , bedroom)
            print ('bathroom' , bathroom)
            print ('location' , location)
            print ('size' , size)
            print ('groundsize' , groundsize)
            print ('terrace' , terrace)
            print ('offer_type',offer_type)

            print ('country_state',country_state)
            #print (site +';' + str(name) +';' + str(ref) +';' + str(price) +';' + str(location) + ';' + str(bedroom) + ';' + str(bathroom) + ';' + str(terrace) + ';' + str(size) + ';' + str(groundsize) + ';' + str(parkplace) + ';' + url + ';' + str(country) + ';' + str(state) + ';' + str(aera) + ';' + str(city) + ';' + str(property_type) + ';' + str(offer_type) + '\n')

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
cur.execute("update sites set last_scraped = current_date where site = '" + site + "' ;")
cur.execute("commit;")
scrap_functions.log( site + ' end')
