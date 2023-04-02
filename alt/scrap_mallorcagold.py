#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import requests, re, time
from bs4 import BeautifulSoup
from urllib.parse import urlparse
import scrap_functions
from datetime import date

cur, conn = scrap_functions.connect_properties()
dirname = os.path.dirname(os.path.abspath(__file__)) + '/'



##############################################################
site = 'Mallorcagold'
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
    urls=['https://mallorcagold.com/de/immobilien/expose/large-townhouse-in-the-beating-heart-of-palmas-old-town']
    scraped =''

request_headers = {
                "Accept-Language": "en-US,en;q=0.5",
                "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Referer": "https://google.com",
                "Connection": "keep-alive"}



for url in urls:
    #print (url)
    try:
    #if 1 > 0:
    #    url = url.replace('\n', '').replace('print/','')
        if  'https://mallorcagold.com/de/immobilien/expose' in url and url  not in str(scraped) and '?' not in url :
            print (url)

            price = ''
            headers = request_headers
            page = requests.get(url)
            soup = BeautifulSoup(page.content,'html.parser')
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
            name = ''
            names = soup.find_all('h1')#.get_text().strip()
            for name in names:
                #print (name.get_text().strip())
                name = name.get_text().strip().replace(';',' ')
            try:
                print (name.decode('utf-8', 'ignore'))
            except:
                pass

            ref =  soup.find("p", class_="h1top").get_text()[4:10].strip()
            try:
                price =   soup.find("li", class_="price").get_text().strip()
                price = (re.search('[0-9.]+',price).group(0)).replace('.','')
            except:
                price = 0
            try:
                location = soup.find('h2').get_text().replace('\n', '').replace('	', ' ').replace('  ', ' ').strip()
            except:
                location = ''
            country = 'Spanien'
            print (location)
            location = scrap_functions.strip_accents(location)

            root_url = str(urlparse(url).scheme) + '://' + str(urlparse(url).hostname)
            print(root_url)
            images = []
            for img in soup.findAll('img', class_="social_media_image"):
                if img.get('src') != None:
                    images.append(img.get('src'))
            image = 'https://mallorcagold.com'+str(images[0])
            str_images = (str(images).replace("'",'').replace("[",'').replace("]",''))
            print('Image: ', image)
            print('Image: ', str_images)

            images = []
            print('--------------------------------------------')
            #for img in soup.findAll("ul", class_="slides"):
            for img in soup.findAll("li"):
                if str(img)[0:33] == '<li style="background-image: url(':
                    images.append(str(img)[33:-8])
            image = str(images[0])
            root_url = str(urlparse(url).scheme) + '://' + str(urlparse(url).hostname)
            print(root_url)
            if image[0:4] != 'http':
                    image = root_url+image
            str_images = (str(images).replace("'",'').replace("[",'').replace("]",''))
            print('Image: ', image)
            #print('Image: ', str_images)


            for li_tag in soup.find_all('ul', {'class':'objectkeydata'}):
                for span_tag in li_tag.find_all('li'):
                    value = span_tag.get_text().replace ('  ',' ').replace ('  ',' ').replace ('  ',' ').replace ('  ',' ').replace ('  ',' ').replace ('  ',' ').replace ('  ',' ').replace('	', '').replace('\n', '').strip()
                #    print (value)
                    if value[:12] =='Schlafzimmer' and bedroom == 0:
                        try:
                            bedroom = value[12:20].strip()
                        except:
                            bedroom = 0
                    if value[:10] =='Wohnfläche' and size == 0:
                        try:
                            size = value[10:30].strip()
                            #print ('size', size)
                            size = (re.search('[0-9.]+',size).group(0)).replace('.','')
                        except:
                            size = 0
                    if value[:10] =='Grundstück' and groundsize == 0:
                        try:
                            groundsize = value[10:40].strip()
                            #print ('groundsize', groundsize)
                            groundsize = (re.search('[0-9.]+',groundsize).group(0)).replace('.','')
                        except:
                            groundsize = 0
            print ('ref' , ref)
            print ('url' , url)
            print ('name', name)
            print ('price' , price)
            print ('bedroom' , bedroom)
            print ('location' , location)
            print ('size' , size)
            print ('groundsize' , groundsize)
    #        print ('terrace' , terrace)
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
