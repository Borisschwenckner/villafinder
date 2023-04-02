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
site = 'Porta Mallorquina'
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
    urls = ['https://www.porta-mallorquina.de/immobilien/cala-pi-haus-077520.html']
    scraped =''




for url in urls:
    pos_url = 0
    pos_url = url.find("?")
    if pos_url > 0:
        url = (url[0:pos_url])
    try:
    #if 1 > 0:
        if  url[-7].isdigit() and url  not in str(scraped) and '.html' in url and '?' not in url :
            print (url)
            #i = open(filename_scraped, "a")
            #i.write (url + '\n')
            #i.close
            page = requests.get(url)
            soup = BeautifulSoup(page.content,'html.parser')
            #name = soup.find(class_="h2 exposee").get_text().replace("\n", " ")
            name = (soup.title).get_text().replace(';',' ').replace("\n", " ")
            print (name)
            try:
                print (name.decode('utf-8', 'ignore'))
            except:
                pass
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

            lefts = (soup.find_all("p", class_="hf_links"))
            rights = (soup.findAll("p", class_="hf_rechts"))
            i = 0
            for left in lefts:
                #print (left.get_text())
                if (left.get_text())== 'Objekt-Nr.:':
                    ref = rights[i].get_text()
                if (left.get_text())=='Ort:':
                    location = rights[i].get_text()
                if (left.get_text())=='Konstruktionsfläche:':
                    size = rights[i].get_text().strip().split()[0]
                if (left.get_text())=='Grundstück:':
                    groundsize = rights[i].get_text().strip().split()[0]
                if (left.get_text())=='Schlafzimmer:':
                    bedroom = rights[i].get_text()
#                    bedroom = (re.search('[0-9.]+',bedroom).group(0)).replace('.','')
                if (left.get_text())=='Badezimmer:':
                    bathroom = rights[i].get_text()
#                    bathroom = (re.search('[0-9.]+',bathroom).group(0)).replace('.','')

                if (left.get_text())=='Kaufpreis:':
                    price = rights[i].get_text()


                i = i+1
            location = scrap_functions.strip_accents(location)

            try:
                price = (re.search('[0-9.]+',price).group(0)).replace('.','')
            except:
                price = 0
            country = 'Spanien'


            image_meta = soup.find("meta",  {"property":"og:image"})
            image = (image_meta["content"] if image_meta else None)
            root_url = str(urlparse(url).scheme) + '://' + str(urlparse(url).hostname)
            if image[0:4] != 'http':
                    image = root_url+image

            images = []
            for img in soup.findAll('img'):
            #    print(img)
                try:
                    if (img['rel']) != None  and '.jpg'  in str(img['rel'])  and '/immobilien/'in str(img['rel']) :
                        images.append((img['rel']))
                except:
                    pass
            #image = images[0]
            str_images = (str(images).replace("'",'').replace("[",'').replace("]",''))
            print('#########################################')
            print(str_images)
            print (image)
            print('#########################################')




            if groundsize == '':
                groundsize = 0
            if groundsize == '-':
                groundsize = 0
            if bedroom == '':
                bedroom = 0
            if bedroom == '-':
                bedroom = 0
            if bathroom == '':
                bathroom = 0
            if bathroom == '-':
                bathroom = 0
            if size == '':
                size = 0
            if size == '-':
                size = 0


            print (ref, location, size, groundsize, bedroom, bathroom, price)

            #f.write(site +';' + str(name) +';' + str(ref) +';' + str(price) +';' + str(location) + ';' + str(bedroom) + ';' + str(bathroom) + ';' + str(terrace) + ';' + str(size) + ';' + str(groundsize) + ';' + str(parkplace) + ';' + url + ';' + str(country) + ';' + str(state) + ';' + str(aera) + ';' + str(city) + ';' + str(property_type) + ';' + str(offer_type) + '\n')
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
#f.close
cur.execute("update sites set last_scraped = current_date where site = '" + site + "' ;")
cur.execute("commit;")
scrap_functions.log( site + ' end')
