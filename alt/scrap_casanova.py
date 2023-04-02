#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import requests, re
import scrap_functions
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from datetime import date

cur, conn = scrap_functions.connect_properties()
dirname = os.path.dirname(os.path.abspath(__file__)) + '/'

##############################################################
site = 'Casanova'
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
    urls = ['https://www.mallorcaimmobilien.com/de/immobilien-mallorca/expose-1303203']
    scraped =''
    #scrap_functions.log(site + ' ----------------------------TESTMODUS --------------------------------------')



for url in urls:
    pos_url = 0
    pos_url = url.find("?")
    if pos_url > 0:
        url = (url[0:pos_url])
        print (url)
    try:
    #if 1>0:
        print(url)
        if  url[-6].isdigit() and 'expose' in url and url not in str(scraped) and '?' not in url :
            print (url)
            price = ''
            page = requests.get(url)
            print (page.encoding)
            soup = BeautifulSoup(page.text,'html.parser') #page.text statt page.content  After getting response, take response.content instead of response.text and that will be of encoding utf-8.
            name = soup.find('h1').get_text().strip()
            print('Name1: ',name)

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
            country_state = 'Mallorca'#
            country = 'Spanien'
            property_type = ''
            offer_type =''


            ref = soup.find('h5').get_text().replace('#','').strip() # soup.find("ul", class_="facilities-list clearfix").get_text().strip()
            print (ref)
            location = soup.find("i",class_="fa fa-map-marker").next_element.get_text().strip()
            location = scrap_functions.strip_accents(location)
            try:
                price =   soup.find("h3").get_text().strip()
                price = (re.search('[0-9.]+',price).group(0)).replace('.','')
            except:
                price = 0

            tags = soup.find_all("li")
            for tag in tags:
                if 'Schlafzimmer:' in (tag.get_text()):
                    bedroom = tag.get_text().replace('Schlafzimmer:','').strip()

                if 'Badezimmer:' in (tag.get_text()):
                    bathroom = tag.get_text().replace('Badezimmer:','').strip()

                if 'Grundstück:' in (tag.get_text()):
                    groundsize = tag.get_text().replace('Grundstück:','').strip()
                    groundsize = (re.search('[0-9.]+',groundsize).group(0)).replace('.','')

                if 'Wohnfläche:' in (tag.get_text()):
                    size = tag.get_text().replace('Wohnfläche:','').strip()
                    size = (re.search('[0-9.]+',size).group(0)).replace('.','')

            if 'mieten' not in url:
                offer_type ='Buy'
            else:
                offer_type ='Rent'
            print (offer_type)
            images = []
            for a in soup.find_all("a" , href=True):
                if a["href"][a["href"].rfind(".")+1:] in ["jpeg", "png", "jpg"]:
                    images.append(a["href"])

            image = images[0]#.replace('1.jpg','6.jpg')
            root_url = str(urlparse(url).scheme) + '://' + str(urlparse(url).hostname)
            str_images = (str(images).replace("'",'').replace("[",'').replace("]",''))
            #print('#########################################')
    #        print(str_images)
            print (image)
            print (ref)
            print (price)
            print (bedroom)
            print (location)
            print (size)
            print (bathroom)
            print (groundsize)
            #f.write(site +';' + str(name) +';' + str(ref) +';' + str(price) +';' + str(location) + ';' + str(bedroom) + ';' + str(bathroom) + ';' + str(terrace) + ';' + str(size) + ';' + str(groundsize) + ';' + str(parkplace) + ';' + url + ';' + str(country) + ';' + str(state) + ';' + str(area) + ';' + str(city) + ';' + str(property_type) + ';' + str(offer_type) + '\n')
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
