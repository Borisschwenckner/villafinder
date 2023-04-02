#!/usr/bin/python3
import bs4 as bs
import urllib.request, os, sys, re
from urllib.parse import urlparse
from datetime import datetime
import psycopg2, http.client, urllib, telebot
from urllib.request import urlretrieve

#from PIL import Image, ImageEnhance, ImageFilter
from wand.image import Image as Img
import pysftp


import scrap_functions

#scrap_functions.check_dirs()
#scrap_functions.mail('Minkner')

#scrap_functions.do_sql()

#scrap_functions.get_sitemap_extended('Firstmallorca')
#scrap_functions.get_sitemap_extended('Minkner')
#scrap_functions.get_sitemap_extended('Engel & Völkers')
#scrap_functions.get_sitemap_extended('Porta Mallorquina')
#scrap_functions.get_sitemap_extended('Kensington')
#scrap_functions.get_sitemap_extended('Mallorcagold')
#scrap_functions.get_sitemap_extended('Casanova')
#scrap_functions.get_sitemap_extended('DC-Mallorca')
#scrap_functions.get_sitemap_extended('Remus')
#scrap_functions.get_sitemap_extended('Primehomes')
#scrap_functions.get_sitemap_extended('Lietz')
#scrap_functions.get_sitemap_extended('Privatepropertymallorca')
#scrap_functions.get_sitemap_extended('Sandberg')
#scrap_functions.get_sitemap_extended('Toni Da Silva')
#scrap_functions.get_sitemap_extended('Imperial')
#scrap_functions.get_sitemap_extended('John Taylor')
#scrap_functions.get_sitemap_extended('Neptunus')
#scrap_functions.get_sitemap_extended('Immobilienmallorca')
#scrap_functions.get_sitemap_extended('Living Blue')
#scrap_functions.get_sitemap_extended('Montfair')




#scrap_functions.create_propertys_from_sitemap('Firstmallorca')
#scrap_functions.create_propertys_from_sitemap('Mallorcagold')
#scrap_functions.create_propertys_from_sitemap('Living Blue')
#scrap_functions.create_propertys_from_sitemap('Neptunus')
#scrap_functions.create_propertys_from_sitemap('Immobilienmallorca')
#scrap_functions.create_propertys_from_sitemap('Remus')
#scrap_functions.create_propertys_from_sitemap('Engel & Völkers')



#scrap_functions.get_details('Toni Da Silva')
#scrap_functions.get_details('Primehomes')
#scrap_functions.get_details('Porta Mallorquina')
#scrap_functions.get_details('Remus')
#scrap_functions.get_details('Imperial')
#scrap_functions.get_details('Immobilienmallorca')
#scrap_functions.get_details('Sandberg')
#scrap_functions.get_details('Montfair')
#scrap_functions.get_details('Toni Da Silva')
#scrap_functions.get_details('Lietz')
#scrap_functions.get_details('DC-Mallorca')
#scrap_functions.get_details('Neptunus')
#scrap_functions.get_details('Engel & Völkers')




#scrap_functions.set_locations()
#scrap_functions.get_missing_images()
scrap_functions.get_missing_types()
#scrap_functions.set_inactive()
#scrap_functions.check_types()
#scrap_functions.image_one_download()
#scrap_functions.database_service()
#scrap_functions.db_checks()

#scrap_functions.get_missing_image_immobilienmallorca()
#scrap_functions.mail('Minkner')

#print('https://www.marcelremusrealestate.com/wp-content/uploads/2019/09/Binifald%C3%B3-20_F00-1024x576.jpg'.encode('latin1').decode('utf8') )
#

#link = 'https://www.marcelremusrealestate.com/wp-content/uploads/MARCEL-REMUS©2022.-AlbertBravoPhoto-BRV06200.jpg'
#print (link)
#link = urllib.parse.quote(link).replace('https%3A//','https://') #.encode('utf-8')#.decode('utf8')
#print (link)

def connect_properties():
    conn = psycopg2.connect(database='properies', host='sql12.your-server.de', user='schweng_2', password = 'v9gyQ62fetFM2jDU' , sslmode = 'verify-full', sslrootcert = '/prg/keys/psqlca.pem')
    cur = conn.cursor()
    return cur, conn

cur, conn = scrap_functions.connect_properties()

#cur, conn = connect_properties()


def get_sitemap_extended_local(site):
    import json
    from urllib.request import Request, urlopen
    cur.execute("select count(id)  from sitemap  where create_date = current_date and site = '" + site + "' " )
    qty = cur.fetchone()
    print('qty', qty[0])
    if qty[0] < 3000:
        cur.execute("delete from sitemap  where site = '" + site + "' ")
        cur.execute("commit;")
        sites = ''
        sitemap_url_suffix =''
        cur.execute("select * from sites  where site = '" + site + "' ")
        result = cur.fetchone()
        sitemap_url = result[3]
        sitemap_url_suffix = result[4]
        sitemap_selector = result[5]
        objects_per_page = result[7]

        if sitemap_url_suffix ==None:
            sitemap_url_suffix =''
        max =  10
        root_url = str(urlparse(sitemap_url).scheme) + '://' + str(urlparse(sitemap_url).hostname) #+'/'
        if root_url[-1] != '/':
            root_url += '/'
        index = 1
        proxies = {'https': 'https://79.147.46.239:8080'}
#        proxies = {"http": "http://10.10.1.10:3128",
#           "https": "http://10.10.1.10:1080"}
        search_url = []
        search_urls = sitemap_url.split(",")
        for search_url in search_urls:
            sitemap_url = (search_url.strip())
            print(sitemap_url)
            for seite in range(1,max): #
                print("Loop " + str(seite) + " startet.")
                if seite ==1 :
                    index = 1
                else:
                    index = seite * objects_per_page

                #seite = 3
                request_headers = {
                                "Accept-Language": "en-US,en;q=0.5",
                                "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
                                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                                "Referer": "https://google.com",
                                "Connection": "keep-alive"}

                request_headers = {'Accept-Language': 'en-US,en;q=0.5',}
                if 1 > 0:
                #try:
                    links_found = 0
                    new_links = 0
                    #try:
                    print("Aktuelle Seite: "+sitemap_url + str(seite) + sitemap_url_suffix)
                    url = (sitemap_url + str(index) + sitemap_url_suffix)

                    if site == 'Mallorcagold' :
                        try:
                            print('Mallorcagold erkannt html parser)')
                            import requests
                            page = requests.get(url)
                            soup = bs.BeautifulSoup(page.text,'html.parser')
                        except:
                            pass
                    else:
                        #try:
                            headers = {'User-Agent': 'Mozilla/5.0'}
                            request = Request(url, headers=headers)
                            soup = bs.BeautifulSoup(urlopen(request).read(),'html.parser')
                        #except:
                        #    pass

#                    print (soup.prettify())
    #                site_json=json.loads(soup.text)
                    response = urlopen(url)
                    content = response.read()           
                    soup = bs.BeautifulSoup(content,'html.parser',from_encoding='utf-8')
                    #res = soup.find('script', id='__NEXT_DATA__') #.get_text()
#                    res = soup.find_all('ref')
                    #print (res)
                    #json_object = json.loads(res.contents[0])
                    #print ((json_object['properties']['texts']['en'])['title'])
                    #for language in json_object['de']:
                    #    print('{}: {}'.format(language['title'], language['ref']))
                    print (soup.prettify())
                    #newDictionary = json.loads(str(soup))['de']
                    #print(newDictionary)
                    #print([d.get('title') for d in site_json['de'] if d.get('title')])
                    items = eval(result[18])

                    for item in items:
                        print (item.prettify())
                        ref = 'xx'
                        price = 0
                        location =''
                        bedroom = 0
                        bathroom = 0
                        size = 0
                        groundsize = 0
                        name =''
                        link = ''
                        image =''
                        type = ''
                        #print(x[x.find('(')+1 : x.find(')') ])

                            #    image = item.find('div', class_='immoloop-image').get('style')[item.find('div', class_='immoloop-image').get('style').find('(')+1 : item.find('div', class_='immoloop-image').get('style').find(')') ]

                        #image = get_text_in_brackets(item.find('div', class_='immoloop-image').get('style'))
                        #print (image)
                        try:
                            image =   eval(result[20])
                            print('Image      :',image)
                        except:
                            image =''
                        print (image[0:4])
                        if image[0:4] != 'http':
                                image = root_url+image
                                print ('Image      :',image)
                        #print (image)
                        #try:
                        link=  eval(result[21])
                        pos_link1 = link.find("&cHash")
                        if pos_link1 > 0:
                            link = (link[0:pos_link1])
                        print (link)
#
#  if link[0:4] != 'http':
#                            link = root_url+link
                        print ('Link       :',link)
                        #print ('Link: ',link)
                        #except:
                        #    link =''
                        #try:
                        #price =  parent#.text #eval(result[11])
                        ref = eval(result[13])
                        print ('Ref        :',ref)

                        price =  eval(result[11])
                        print ('Price      :', price)
                        price = scrap_functions.convert_to_float(price) #(re.search('[0-9.]+',price).group(0)).replace('.','')
                        print ('Price      :', price)
                        #except:
                        #    price = 0
                        #try:
                        name = eval(result[19])
                        #print (name.encode().decode('utf-8', 'ignore'))
                        #name =name.decode('utf-8', 'ignore')
                        #name =   eval(result[19])
                        print ('Name       :',name)
                        #except:
                        #    name = ''
                        #try:
                        #except:
                        #    ref =''
                        #try:
                        #location = item.find('span', class_='properties__address-city').string.strip() #.string.strip()  #eval(result[12])
                        location = eval(result[12])
                        location = scrap_functions.strip_accents(location)
                        print ('Location: ',location)
                        #except:
                        #    location =''
                        #try:
                        #bedroom = item.find(text=re.compile('Bedrooms:')).parent.parent.find('span',class_='properties__param-value').get_text().strip() #eval(result[14])
                        bedroom = eval(result[14])
                        bedroom = scrap_functions.convert_to_float(bedroom)
                        print ('Bedroom    :',bedroom)

                        #bedroom = scrap_functions.convert_to_float(bedroom)
                        #print ('Bedroom: ',bedroom)
                        #except:
                    #        bedroom = 0

                        #type = item.find('span', class_='properties__param-type').string.strip() #.string.strip()  #eval(result[12])
                        #print ('Type:' , type)


                        #bathroom = eval(result[15])
                        #bathroom = scrap_functions.convert_to_float(bathroom) #(re.search('[0-9.]+',bathroom).group(0)).replace('.','')
                        #print ('Bathroom   : ',bathroom)
                        #except:
                        #    bathroom = 0
                        #try:

                        #tags =  item.find_all('div',class_='immoloop-props-item')#.find('path').get('d')[0:6] # == 'M45.61'.get_text() #.find(text=re.compile('M45.61')).get_text() #eval(result[16])
                        #for tag in tags:
                                #print (tag)

                        size =  eval(result[16])
                        size = scrap_functions.convert_to_float(str(size)) #(re.search('[0-9.]+',size).group(0)).replace('.','')
                        print ('Size       :', size)


                        try:
                            groundsize = eval(result[17])
                            #print(groundsize)
                            if 'ha' in groundsize:
                                groundsize = groundsize.replace('ha','').strip()#.replace(',','.')
                                groundsize = str(float(groundsize)*10000)
                            #groundsize = (re.search('[0-9.]+',groundsize).group(0))#.replace('.','')
                            groundsize = scrap_functions.convert_to_float(groundsize)
                            print ('Groundsize : ',groundsize)
                        except:
                            groundsize=0
                        print ('-----------------------')
                        print ()

                        if eval(sitemap_selector):
                            links_found += 1
                            pos_link = 0
                            pos_link = link.find("?pageno")
                            if pos_link > 0:
                                link = (link[0:pos_link])
                            if link[0:4] != 'http':
                                link = root_url+link
                            link= link.replace('//','/')
                            link= link.replace('https:/','https://')
                            link= link.replace('http:/','http://')

                            if link != None and  link not in str(sites) :
                                sites = sites + ('<url><loc>' + link + '</loc></url>\n')
                                new_links += 1
                            #    print(site ,link, ref, name, location, image, bedroom, bathroom, size, groundsize)
                                cur.execute("INSERT INTO sitemap ( site, url, ref, name, location, image, bedroom, bathroom, size, groundsize, price, type) values ( %s, %s,%s, %s,%s, %s,%s, %s,%s, %s,%s,%s)" , ( [site ,link, ref, name, location, image, bedroom, bathroom, size, groundsize, price, type]))
                            cur.execute("commit;")

                    print ('Links found: ', links_found, 'New Links: ', new_links)
                    print ()
                    if new_links == 0 and seite > 8 :
                        print('keine neuen Links gefunden')
                        break
                #except:
                #    pass


def get_details_test(site):
    import requests, time
    from bs4 import BeautifulSoup

    #log( site + ' start')
    testmode =  scrap_functions.check_testmode(site)

#cur.execute("select * from sites  where last_scraped != current_date and site = '" + site + "' ")
    cur.execute("select * from sites  where site = '" + site + "' ")

    result = cur.fetchone()

    urls=[]
    if testmode == False:
    #    cur.execute("select count(id)  from sites  where last_scraped = current_date and site = '" + site + "' " )
    #    qty = cur.fetchone()
    #    if qty[0] > 0:
    #        scrap_functions.log( site + ' Diese Seite wurde heute schon gescraped - end')
    #        print('Diese Seite wurde heute schon gescraped')
    #        exit()
    #    scraped = scrap_functions.load_scraped(site)
    #    scrap_functions.get_sitemap_extended(site)
        cur.execute("select url  from sitemap  where site = '" + site + "' " )

            #cur.execute("select url from sitemap sp where site = '" + site + "' ")
        rows = cur.fetchall()
        for row in rows:
            urls.append(row[0])

            #log(site + ' '+ str(qty_elements)+' Elemente in Sitemap')
            #äreturn urls

        #print (urls)

    if testmode == True:
        urls.append(result[35])
        scraped =''

    scraped =''
    print (urls)

    for url in urls:

    #    try:
        #if 1 > 0:
        if   url  not in str(scraped)  :
                print ('URL        :',url)
                page = requests.get(url)
                soup = BeautifulSoup(page.content,'html.parser')
                if len(result[31]) > 5:
                    soup = eval(result[31])   #soup.find('div', class_='grid grid-66 clearfix')

                print (soup.prettify())

                name = eval(result[32]) #
                #name = soup.find("h1", class_="expose__title").get_text().strip()  + ' ' + soup.find('div', class_='expose__subtitle').get_text().strip()
                print ('Name: ', name)

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
                count = 1



                property_type = eval(result[40])
                print ('Type       :',property_type)

                bedroom = eval(result[27])
                #bedroom =soup.find('Gruppe 55').parent.parent.parent.string.strip()

               # print (bedroom)
                #print ('__________')
                bedroom = scrap_functions.convert_to_float(bedroom)
                print ('Bedrooom ', bedroom)

                ref = eval(result[26]) #soup.find(text=re.compile('ImmoNr')).next_element.next_element.get_text().strip()
                #ref = soup.find('div', class_='property-container').get('id').strip()
                print ('Ref ', ref)


                size = eval(result[29])
                print ('Size ',size)
                size = scrap_functions.convert_to_float(size)
                print ('Size ',size)


                groundsize = eval(result[30])
                groundsize = scrap_functions.convert_to_float(groundsize)
                print ('Groundsize ', groundsize)


                bathroom =  eval(result[28])
                bathroom = scrap_functions.convert_to_float(bathroom)
                print ('Bathroom ', bathroom)

                price = eval(result[24]) #soup.find(text=re.compile('Warmmiete')).next_element.next_element.get_text().strip()
                print ('Price ', price)
                price = scrap_functions.convert_to_float(price)
                print ('Price ', price)

                location = eval(result[25]) #soup.find(text=re.compile('Ort')).next_element.next_element.get_text().strip()
                print ('Location ',location)
                location = scrap_functions.strip_accents(location)


                image = eval(result[33])
                print('Image :', image)

                #offer_type = eval(result[34])
                #print (offer_type)
                pos_img = image.find('static.jpg')
                if pos_img > 0:
                    pos_img = pos_img +10
                    image = (image[0:pos_img])

                print('------------------------------------')
                print (image)


                country = 'Spanien'


                #image_meta = soup.find("meta",  {"property":"og:image"})
                #image = eval(result[33])
                #.find('div', 'data-img')

                root_url = str(urlparse(url).scheme) + '://' + str(urlparse(url).hostname)
                if image[0:4] != 'http':
                        image = root_url+image

                images = []
                for img in soup.find_all('div', class_='fotorama'):
                    try:
                        if  'https://smart.onoffice.de/smart20/Dateien/LietzImmobilien/smartSite20/multi_banner'in str(img['src']) :
                            images.append(img.get('src'))
                    except:
                        pass
                #image = images[0]
                str_images = '' #(str(images).replace("'",'').replace("[",'').replace("]",''))
            #    print('#########################################')
                #print(str_images)
            #    print (image)
            #    print('#########################################')



#get_sitemap_extended_local('Immobilienmallorca')
#get_details_test('Engel & Völkers')

    #print ('fertig')
conn.close
