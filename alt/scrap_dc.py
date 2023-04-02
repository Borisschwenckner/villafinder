#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os, re, requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import scrap_functions
from datetime import date

cur, conn = scrap_functions.connect_properties()
dirname = os.path.dirname(os.path.abspath(__file__)) + '/'

##############################################################
site = 'DC-Mallorca'
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
    urls = ['https://dc-mallorca.com/de/immobilien/expose/3916/']
    scraped =''


for url in urls:
    #print (url)
    pos_url = url.find("?")
    if pos_url > 0:
        url = (url[0:pos_url])

    try:
    #if 1 > 0:
        if 'dc-mallorca.com/de/immobilien/expose' in url and url[-2].isdigit() and url not in str(scraped) and '?' not in url and 'page' not in url :
            print(url)
            bathroom = '0'
            bedroom = '0'
            terrace = ''
            size = '0'
            groundsize = '0'
            parkplace = ''
            price = 0
            country = ''
            area = ''#
            state = ''
            city = ''
            carpark = ''#

            property_type = ''
            offer_type =''

            headers = {'User-Agent':'Mozilla/5.0'}
            page = requests.get(url)
            #pos_ende = page.text.find('<div data-hook="expose-aside">')
            #page_text = page.text[0:pos_ende]
            soup = BeautifulSoup(page.content,'html.parser')
            #soup = BeautifulSoup(page_text, 'html.parser')
            name= soup.find("h1").get_text().replace(';',' ').replace("\n", " ")
            location = soup.find("h2").get_text().replace(';',' ').replace("\n", " ")
            location = scrap_functions.strip_accents(location)
            country = 'Spanien'
            country_state = 'Mallorca'#


            images = []
            for img in soup.findAll('img'):
                try:
                    if (img['data-big']) != None  :
                        images.append((img['data-big']))
                except:
                    pass
            image = images[0]
            root_url = str(urlparse(url).scheme) + '://' + str(urlparse(url).hostname)
            if image[0:4] != 'http':
                    image = root_url+image

            str_images = (str(images).replace("'",'').replace("[",'').replace("]",''))
            print('#########################################')
            print(str_images)
            print (image)
            print('#########################################')



            tags = soup.findAll("li", class_="list-group-item")
            for tag in tags:
                try:
                    item =  tag.find('div', class_='dt col-sm-5').get_text()
                    value =  tag.find('div', class_='dd col-sm-7').get_text()
                    #print (item, value)
                    if item == 'Wohnfläche ca.':
                        size = (re.search('[0-9.]+',value).group(0)).replace(".","")
                    if item == 'Grund­stück ca.':
                        groundsize = (re.search('[0-9.]+',value).group(0)).replace(".","")
                    if item == 'Schlafzimmer':
                        bedroom = (re.search('[0-9]+',value).group(0))
                    if item == 'Badezimmer':
                        bathroom = (re.search('[0-9]+',value).group(0))
                    if item == 'Objekt ID':
                        ref = value.strip()
                    if item == 'Kaufpreis':
                        price = (re.search('[0-9.]+',value).group(0)).replace(".","")
                    if item == 'Objekttypen':
                        property_type = value

                except:
                    pass


            print ('Name: ', name)
        #    print(bedroom, bathroom, terrace, size, groundsize, parkplace)
            print ('Ref: ',ref)
            print ('Location: ',location)
            print ('Price', price)
            print ('URL', url)
            print ('size', size)
            print ('Groundsize', groundsize)


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
                scrapit = 1
                if price == 0 and size == 0 and bedroom == 0:
                    scrapit = 0
                print (scrapit)
                cur.execute("INSERT INTO scraped ( site, url, scrap_it) values ( %s, %s,%s )" , ( [site ,url, scrapit]))
                cur.execute("commit;")
            except:
                pass
    except:
        pass
#f.close
cur.execute("update sites set last_scraped = current_date where site = '" + site + "' ;")
cur.execute("commit;")
scrap_functions.log( site + ' end')
