#!/usr/bin/python3
# -*- coding: utf-8 -*-
#sudo apt-get install python3-requests  python3-bs4 python3-psycopg2 python3-bs4 python3-dev

import bs4 as bs
import urllib.request, os, sys, time
from urllib.parse import urlparse
from datetime import datetime, timedelta, date
import psycopg2, http.client, urllib, telebot
from urllib.request import urlretrieve
#from PIL import Image, ImageEnhance, ImageFilter
from wand.image import Image as Img


import pysftp
cnopts = pysftp.CnOpts()
cnopts.hostkeys = None

day = datetime.today().strftime("%d")
hour = int(datetime.today().strftime("%H"))
dirname = os.path.dirname(os.path.abspath(__file__)) + '/'
dirname_images = os.path.abspath(dirname + "/../../") + '/scraper_images/'
recipient_email="boris_temp@schwenckner.net"

#dirname_images = '/mnt/video/netz/scraper_images/'

logfile =  dirname + 'logfile.log'

def connect_properties():
    conn = psycopg2.connect(database='properies', host='sql12.your-server.de', user='schweng_2', password = 'v9gyQ62fetFM2jDU' , sslmode = 'verify-full', sslrootcert = '/prg/keys/psqlca.pem')
    cur = conn.cursor()
    return cur, conn

    #cur, conn = functions.connect_properties()


def connect_smarthome(): # Gorg
    conn = psycopg2.connect(database='smarthome', host='sql12.your-server.de', user='schweng_1', password = 'L5x2hnuWMHU4FkYN' , sslmode = 'verify-full', sslrootcert = '/prg/keys/psqlca.pem')
    cur = conn.cursor()
    return cur, conn
    #cur, conn = functions.connect_smarthome()


def convert_seconds(seconds):
    m, s = divmod(seconds, 60)
    h, m = divmod(m, 60)
    print(h)
    if h == 0:
        return ("%02d:%02d" % ( m, s))
    else:
        return ("%02d:%02d:%02d" % (h, m, s))


#    return "%d:%02d:%02d" % (hour, minutes, seconds)

def do_sql():
    cur.execute("ALTER TABLE public.sites11 ADD COLUMN scraping_started int2 DEFAULT 0;")
    cur.execute("commit;")
    

def get_text_in_brackets(text):
    x = (text[text.find('(')+1 : text.find(')') ])
    return x

def re_replace(string):
    return re.sub(r' {2,}' , ' ', string)

def log(msg):

    #file = open(logfile,"a")
    #file.write("%s: %s\n" % (time.strftime("%d.%m.%Y %H:%M:%S"), msg))
    #file.close
    #now = time.strftime("%d.%m.%Y %H:%M:%S")
    cur.execute("INSERT INTO log (date, log) values ( CURRENT_TIMESTAMP , %s)" , ( [msg]))
    cur.execute("commit;")
def errorlog(msg):
    cur.execute("INSERT INTO log (date, log, state) values ( CURRENT_TIMESTAMP , %s,3)" , ( [msg]))
    cur.execute("commit;")

def convert_to_float(s):
    s = str(s)
    if '+' in s:
        s = s.split('+')[0]
    s = re.sub(r"[^0-9.,]+", "", s)
    len1 = len(s)
    pos_thoudand= (s.rfind('.'))
    pos_decimal = (s.rfind(','))
#    print (len1)
#    print (pos_decimal)
#    print (pos_thoudand)
    if len1 > 1:


        if len1 - pos_thoudand == 7 and len1 - pos_decimal == 3 and pos_thoudand > 0 and pos_decimal > 0:
            s = s.replace('.','').replace(',','.')
        if len1 - pos_thoudand == 4  and pos_thoudand > 0 and pos_decimal == -1:
            s = s.replace('.','')
        if  pos_thoudand == -1 and pos_decimal > 0:
            s = s.replace('.','').replace(',','.')
    if s == '':
        s = 0
    try:
        s = float(s)
    except :
        s = 0

    return(s)


cur, conn = connect_properties()


def check_dirs():
    print(os.path.exists(dirname_images))
    if not os.path.exists(dirname_images):
        os.makedirs(dirname_images)
    if not os.path.exists(dirname_images + 'images_big/'):
        os.makedirs(dirname_images + 'images_big/')
    if not os.path.exists(dirname_images + 'thumbs/'):
        os.makedirs(dirname_images + 'thumbs/')


def afterscrap():
    set_locations()
    get_missing_images()
    set_inactive()
    check_types()
    image_one_download()
    database_service()
    db_checks()

def get_neptunus_tags(item, searchtag):
        tags = item.find_all('path')
        for tag in tags:
#                            print(tag.get('d'))
        #    print(tag.get('d')[0:10])
            if tag.get('d')[0:10] == 'M43.87,12.':
                groundsize=  (tag.parent.parent.parent.get_text())
                if searchtag == 'groundsize':
                    return(groundsize)
            elif tag.get('d')[0:10] == 'M45.19,17.':
                size=  (tag.parent.parent.parent.get_text())
                if searchtag == 'size':
                    return(size)
            elif tag.get('d')[0:9] == 'M51.6,35.':
                bedroom= (tag.parent.parent.parent.get_text())
                if searchtag == 'bedroom':
                    return(bedroom)
            elif tag.get('d')[0:10] == 'M23.73,38.':
                bathroom= (tag.parent.parent.parent.get_text())
                if searchtag == 'bathroom':
                    return(bathroom)


def check_types():
        start2 = time.time()
        types_temp_act()
        log('Check Types start')
        

        sql = """
        Update properties  set property_type = 'Gewerbe' where  property_type like'Ladenlokal%';
        Update properties  set property_type = 'Gewerbe' where  property_type like'Industrie/Lagerhallen/Produktion%';
        Update properties  set property_type = 'Gewerbe' where  property_type like'Gastronomie%';
        Update properties  set property_type = 'Gewerbe' where  property_type like'Ladenfläche%';
        Update properties  set property_type = 'Gewerbe' where  property_type like'Bürofläche%';
        Update properties  set property_type = 'Gewerbe' where  property_type like'Einzelhandelsladen%';
        Update properties  set property_type = 'Gewerbe' where  property_type like'Investment / Wohn- und Geschäftshäuser%';
        Update properties  set property_type = 'Gewerbe' where  property_type like'Gastgewerbe%';
        Update properties  set property_type = 'Gewerbe' where  property_type like'Commercial property%';
        Update properties  set property_type = 'Gewerbe' where  property_type like'Wohn- und Geschäftshaus%';
        Update properties  set property_type = 'Gewerbe' where  property_type like'Sonstige%';
        Update properties  set property_type = 'Gewerbe' where  property_type like'Hotel%';
        Update properties  set property_type = 'Gewerbe' where  property_type like'Laden/Einzelhandel%';
        Update properties  set property_type = 'Gewerbe' where  property_type ='Verkaufsflaeche';
        Update properties  set property_type = 'Gewerbe' where  property_type ='Land Forstwirtschaft';
        Update properties  set property_type = 'Gewerbe' where  property_type ='Gewerbeimmobilie';
        Update properties  set property_type = 'Gewerbe' where  lower(property_type) like'%business%';



        Update properties  set property_type = 'Grundstück' where  property_type like'GrundstÃ¼ck, WohngrundstÃ¼ck%';
        Update properties  set property_type = 'Grundstück' where  property_type like'Plot';
        Update properties  set property_type = 'Grundstück' where  property_type like'Wohnen%';
        Update properties  set property_type = 'Grundstück' where  property_type like'Gemischt%';
        Update properties  set property_type = 'Grundstück' where  property_type ='Baugrundstück';
        Update properties  set property_type = 'Grundstück' where  property_type ='Land';

       


        Update properties  set property_type = 'Finca' where  property_type ='finca';

        Update properties  set property_type = 'Villa/Haus' where  property_type like'Casa%';
        Update properties  set property_type = 'Villa/Haus' where  property_type like'Bauernhaus%';
        Update properties  set property_type = 'Villa/Haus' where  property_type like'Landhaus%';
        Update properties  set property_type = 'Villa/Haus' where  property_type like'Doppelhaushälfte%';
        Update properties  set property_type = 'Villa/Haus' where  property_type like'Einfamilienhaus%';
        Update properties  set property_type = 'Villa/Haus' where  property_type like'Mehrfamilienhaus%';
        Update properties  set property_type = 'Villa/Haus' where  property_type like'Stadthaus%';
        Update properties  set property_type = 'Villa/Haus' where  property_type like'%Zweifamilienhaus%';
        Update properties  set property_type = 'Villa/Haus' where  property_type like'%Anwesen%';
        Update properties  set property_type = 'Villa/Haus' where  property_type like'%Strandhaus%';
        Update properties  set property_type = 'Villa/Haus' where  property_type like'%Townhouse%';
        Update properties  set property_type = 'Villa/Haus' where  property_type like'%Reihen%';
        Update properties  set property_type = 'Villa/Haus' where  property_type ='Chalet';
        Update properties  set property_type = 'Villa/Haus' where  lower(property_type) like 'Haus, Villa%';
        Update properties  set property_type = 'Villa/Haus' where  property_type like'Bungalow%';
        Update properties  set property_type = 'Villa/Haus' where  lower(property_type) like'% house%';
        Update properties  set property_type = 'Villa/Haus' where  property_type ='Freistehendes Haus';
        Update properties  set property_type = 'Villa/Haus' where  property_type ='besondere Immobilie';
        Update properties  set property_type = 'Villa/Haus' where  property_type ='Building';
        Update properties  set property_type = 'Villa/Haus' where  property_type ='Villa';


        Update properties  set property_type = 'Wohnung' where  property_type like'Erdgeschosswohnung%';
        Update properties  set property_type = 'Wohnung' where  property_type like'Loft-studio-atelier%';
        Update properties  set property_type = 'Wohnung' where  property_type like'Maisonette%';
        Update properties  set property_type = 'Wohnung' where  property_type like'Apart%';
        Update properties  set property_type = 'Wohnung' where  property_type like'Loft-Studio-Atelier%';
        Update properties  set property_type = 'Wohnung' where  property_type like'%Apartment%';
        Update properties  set property_type = 'Wohnung' where  property_type ='Etagenwohnung';
        Update properties  set property_type = 'Wohnung' where  property_type ='Souterrain';
        Update properties  set property_type = 'Wohnung' where  property_type ='Dachgeschoss';
        Update properties  set property_type = 'Wohnung' where  property_type ='Erdgeschoss';

        Update properties  set property_type = 'Neubau' where lower(property_type) like '%neubauprojekt%' ;

        UPDATE properties SET property_type='' WHERE property_type NOT IN (SELECT TYPE FROM property_types) AND property_type IS NOT NULL AND property_type !=''
        
        """
        cur.execute(sql)
        cur.execute("commit;")

       # cur.execute("select id, name, property_type, ref from properties where (property_type is null or property_type ='') and create_date >= current_date-10 and state ='active' order by id desc ;")
        cur.execute("select id, name, property_type, ref from properties where  (property_type is null or property_type ='') and  state ='active'  order by id desc ;")

        rows = cur.fetchall()
        for row in rows:
            id = row[0]
            ref = row[3]
            words_in_names=row[1].replace(',','').replace(' ',' ').split(' ')
            property_type = row[2]
            qty =  len(words_in_names)
            found = 0
            count=0
            for words_in_name in words_in_names:
                if found == 0 and count <= qty:
                    search = words_in_name.lower()
                    print(search)
                    result =''
                    try:
                        cur.execute("select name  from property_types_temp  where search =  '" + search + "' and is_no_type = 0 " )
                        results = cur.fetchone()
                        result = results[0]
                        found = 1

                    except:
                        result =''
                count = count +1

            if result != property_type and result != '':
                print ('Hmmmmm:', result,ref,  'was:', property_type  , row[1]  )
                cur.execute("update properties set property_type = %s where id = %s;", ( [  result, id]))#
                cur.execute("commit;")

        duration = str(convert_seconds(time.time()-start2))
        print(duration)
        log('Check Types end'+ ' ' + duration)


def types_temp_act():
    cur.execute("select count(id) from property_types where update_date >= current_date-1 " )
    qty = cur.fetchone()
    if qty[0] > 0:
        start2 = time.time()
        log('property_types Temp wird aktualisiert ')
        cur.execute("""delete from property_types_temp ;""")
        cur.execute("commit;")

        #geht nicht wegen neubau
        #cur.execute("""insert into property_types_temp ( name, search) (SELECT  type, trim(lower(type)) from property_types WHERE type is NOT NULL order by type ) ;""")
        #cur.execute("commit;")

        cur.execute("""SELECT searchterms, type  from property_types WHERE searchterms is NOT NULL and (searchterms !='' or searchterms !=' ') order by type ;""")
        searchs = cur.fetchall()

        for search in searchs:
            search_splits = str(search[0]).split(',')
            for search_split in search_splits :
                   # print (search[1])
                    if search_split != '':
                        try:
                            cur.execute("insert into property_types_temp (name, search) values (%s, %s);",([ search[1], search_split.lower().strip()]))
                            #cur.execute("commit;")
                        except:
                            #cur.execute("commit;")
                            pass
        cur.execute("commit;")    

        cur.execute("""delete from property_types_temp where name ='';""")
        cur.execute("commit;")
        cur.execute("""delete from property_types_temp where search ='';""")
        cur.execute("commit;")
        duration = str(convert_seconds(time.time()-start2))
        log('property_types Temp fertig' + ' ' + duration)

def mail(site):
    text = '<!DOCTYPE html><html><head></head><body>'
    #name_customer = 'Minkner'

    cur.execute("select count(properties.id) from properties ,sites where sites.site = properties.site and create_date::date = CURRENT_DATE  and offer_type ='Buy' and country_state = 'Mallorca' and mail_customer LIKE '%" + site + "%'  and country ='Spanien'" )
    qty = cur.fetchone()
    print ('Neue Immobilien gefunden: ' + str(qty[0]))

    cur.execute("SELECT properties.site,NAME,REF,price,LOCATION,url,create_date FROM properties,sites WHERE create_date> CURRENT_DATE-1 AND sites.site=properties.site AND country_state='Mallorca' AND country='Spanien' AND offer_type='Buy' AND mail_customer LIKE '%" + site + "%'  ORDER BY LOCATION,price DESC " )
    rows = cur.fetchall()
    if len(rows) > 0:
        text = text + 'Neue Immobilien wurden gefunden:<br><br><br>'
        text = text + '<table border="0">'
        for row in rows:
            price = int(row[3])
            price = "{:,d}".format(price).replace(',','.')

            text = text + '<tr><td>Provider</td><td><b>' + str(row[0]) + '</b></td></tr>'
            text = text + '<tr><td>Name</td><td align="left" ><b>' + str(row[1]) + '</b></td></tr>'
            text = text + '<tr><td>Reference</td><td align="left">' + str(row[2]) + '</td></tr>'
            text = text + '<tr><td>Price</td><td align="left">' + str(price) + '</td></tr>'
            text = text + '<tr><td>Location</td><td align="left">' + str(row[4]) + '</td></tr>'
            text = text + '<tr><td>Date</td><td align="left">' + str(row[6]) + '</td></tr>'
            text = text + '<tr><td>URL:</td><td align="left">' + str(row[5]) + '</td></tr>'
            text = text + '<tr><td> </td><td align="left"> </td></tr>'
            text = text + '<tr><td> </td><td align="left"> </td></tr>'
            text = text + '<tr><td> </td><td align="left"> </td></tr>'
            text = text + '<tr><td> </td><td align="left"> </td></tr>'
            text = text + '<tr><td> </td><td align="left"> </td></tr>'

        text = text + '</table><br><br><br>'

    emails= []
    subject = str(qty[0]) + ' neue Immobilien auf Mallorca gefunden'
    cur.execute("select email from sites where last_email != current_date and site = '" + site + "' " )

    rows = cur.fetchall()
    for row in rows:
        emails = row[0].split(",")
        #emails = ['@schwenckner.net','schwenckner@web.de', 'borisschwenckner@gmail.com']

        for email in emails:
            email = (email.strip())
            print (email)
            x = email_html(email, subject, text)
            print(x)
            if x == True:
                cur.execute("update sites set last_email = current_date  where site = '" + site + "' " )
                cur.execute("commit;")
                log('Mail send to: ' + email + ' ' + str(x))

    print ('fertig')




def create_propertys_from_sitemap(site):
    cur, conn = connect_properties()
    cur.execute("select *  from sitemap  where site = '" + site + "' and url not in (select url from properties) " )
    #cur.execute("select *  from sitemap  where site = '" + site + "' " )
    #log('Start ' + site +  ' create_propertys_from_sitemap')
    rows = cur.fetchall()
    for row in rows:

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
        str_images =''
        country = 'Spanien'
        country_state = 'Mallorca'

        location = row[6]
        url = row[1]
        name = row[7]
        image = row[13]
        property_type =  row[14]
        ref =  row[5]
        price = row[8]
        bedroom = row[9]
        bathroom = row[10]
        size = row[11]
        ground_size = row[12]
        if price <= 30000 and price > 0:
            offer_type = 'Rent'
        else:
            offer_type = 'Buy'

        print ('ref' , ref)
        print ('url' , url)
        print ('name', name)
        print ('price' , price)
        print ('bedroom' , bedroom)
        print ('bathroom' , bathroom)
        print ('location' , location)
        print ('size' , size)
        print ('groundsize' , groundsize)
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
        if check_ref == 0:
            cur.execute("select id from properties where site ='" + site + "' and ref = '" + ref + "' and price = %s  and state ='active' ;", ([price]))
            try:
                    check_ref = cur.fetchone()[0]
            except:
                    check_ref = 0
            print ('Check Ref gefunden über REF mit Preis', check_ref)
        #if check_ref == 0:
    #        cur.execute("select id from properties where site ='" + site + "' and ref = '" + ref + "' and state ='active' ;")
    #        try:
    #                check_ref = cur.fetchone()[0]
    #        except:
    #                check_ref = 0
    #        print ('Check Ref gefunden über REF ohne Preis', check_ref)


#        try:
#            cur.execute("commit;")
#        except:
#            pass

        if check_ref > 0:
            print ('Update')
            try:
            #if 1> 0:
                cur.execute("update properties set write_date = current_date , last_scraped_date = current_date ,state = 'active',  url  = %s ,name  = %s , price = %s, bedroom = %s , bathroom = %s, living_size = %s, ground_size = %s, location = %s , carpark = %s, terace = %s, ref = %s , offer_type = %s , property_type = %s , country_state = %s , area = %s , city = %s , country = %s , image_url = %s, images = %s where id = %s" ,
                ([url, name,  price, bedroom, bathroom , size, groundsize, location, carpark, terrace, ref,  offer_type, property_type, country_state, area, city , country, image, str_images, check_ref]))
                cur.execute("commit;")
                print ('update done' , ref , check_ref, price, bedroom, bathroom)
            except:
                pass
        else:
            print ('insert',ref,  name, site, bedroom, bathroom)
            try:
                cur.execute("INSERT INTO properties ( create_date,write_date, last_scraped_date, state, site, name, ref, price, location, bedroom, bathroom, terace, living_size, ground_size, carpark, url, offer_type, property_type, country_state, area, city, country, image_url, images) \
                values ( current_date,current_date, current_date,'active', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" , ( [site ,name, ref ,price, location,bedroom, bathroom, terrace, size, groundsize , carpark, url, offer_type, property_type, country_state, area, city, country, image, str_images]))
                conn.commit()
                print ("Insert Done")
            except:
                cur.execute("commit;")
        #try:
    #        cur.execute("commit;")
#        except:
#            pass
    #    try:
    #        cur.execute("INSERT INTO scraped ( site, url) values ( %s, %s)" , ( [site ,url]))
    #        cur.execute("commit;")
    #    except:
    #        pass

#-------------------------end update

    #cur.execute("update sites set last_scraped = current_date where site = '" + site + "' ;")
    #cur.execute("commit;")
    #log('End ' + site +  ' create_propertys_from_sitemap')


def get_xml_sitemap(site, sitemap_url):
    import requests
#    sitemap_url = 'https://www.montfairestates.com/sitemap.xml'

    cur.execute("delete from sitemap  where site = '" + site + "' ")
    cur.execute("commit;")
    #normale sitemap
    sitemap_response = requests.get(sitemap_url)
    soup = bs.BeautifulSoup(sitemap_response.content, 'html.parser')
    elements = soup.findAll("url")
    urls = [elem.find("loc").string for elem in elements]
    for url in urls:

        if (url)[-4].isdigit():
            print (url)
            cur.execute("INSERT INTO sitemap ( site, url) values ( %s, %s)" , ( [site ,url]))
    cur.execute("commit;")

def get_sitemap(site):
    cur.execute("select count(id)  from sitemap  where create_date = current_date and site = '" + site + "' " )
    qty = cur.fetchone()
    print('qty', qty[0])
    if qty[0] < 3000:
        cur.execute("delete from sitemap  where site = '" + site + "' ")
        cur.execute("commit;")
        dirname = os.path.dirname(os.path.abspath(__file__)) + '/'
        sitemap_xml =   dirname + 'sitemap_' + site.lower() + '.xml'
        print(site, sitemap_xml)
        sites = ''
        sitemap_url_suffix =''
        cur.execute("select * from sites  where site = '" + site + "' ")
        result = cur.fetchone()
        sitemap_url = result[3]
        sitemap_url_suffix = result[4]
        sitemap_selector = result[5]
        objects_per_page = result[7]
        print(sitemap_url)
        print (sitemap_url_suffix)
        if sitemap_url_suffix ==None:
            sitemap_url_suffix =''

        links_for_db = []
        max =  500
        root_url = str(urlparse(sitemap_url).scheme) + '://' + str(urlparse(sitemap_url).hostname) #+'/'
#        print (root_url)
        if root_url[-1] != '/':
            root_url += '/'
        index = 1
        search_url = []
        #if ',' in sitemap_url:
        search_urls = sitemap_url.split(",")
        print(search_urls)
        for search_url in search_urls:
            sitemap_url = (search_url.strip())
            print(sitemap_url)
            for seite in range(1,max): #
                print("Loop " + str(seite) + " startet.")
                if seite ==1 :
                    index = 1
                else:
                    index = seite * objects_per_page
                request_headers = {
                                "Accept-Language": "en-US,en;q=0.5",
                                "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
                                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                                "Referer": "https://google.com",
                                "Connection": "keep-alive"}
                #if 1 > 0:
                try:
                    links_found = 0
                    new_links = 0
                    try:
                        headers = request_headers
                        soup = bs.BeautifulSoup(urllib.request.urlopen(sitemap_url + str(index) + sitemap_url_suffix ).read(),'html.parser')
                    except:
                        pass
                    print("Aktuelle Seite: "+sitemap_url + str(seite) + sitemap_url_suffix)

                    for links in soup.find_all("a" ):
                        #print (links)
                        if eval(sitemap_selector):
                            links_found += 1
                            link =  (links.get("href"))
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
                                links_for_db.append(link)
                                new_links += 1
                    print (links_found, new_links)
                    if new_links == 0 and seite > 8 : #10
                        print('keine neuen Links gefunden')
                        for link_for_db in links_for_db:
                            cur.execute("INSERT INTO sitemap ( site, url) values ( %s, %s)" , ( [site ,link_for_db]))
                        cur.execute("commit;")
                        break
                except:
                    pass

def get_sitemap_extended(site):
    from urllib.request import Request, urlopen

    cur.execute("select count(id)  from sitemap  where create_date = current_date and site = '" + site + "' " )
    qty = cur.fetchone()
    print('qty', qty[0])
    if qty[0] < 6000:
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
        max =  500
        root_url = str(urlparse(sitemap_url).scheme) + '://' + str(urlparse(sitemap_url).hostname) #+'/'
        if root_url[-1] != '/':
            root_url += '/'
        index = 1
        search_url = []
        search_urls = sitemap_url.split(",")
        for search_url in search_urls:
            sitemap_url = (search_url.strip())
            for seite in range(1,max): #
                print("Loop " + str(seite) + " startet.")
                if seite ==1 :
                    index = 1
                else:
                    index = seite * objects_per_page
                request_headers = {
                                "Accept-Language": "en-US,en;q=0.5",
                                "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
                                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                                "Referer": "https://google.com",
                                "Connection": "keep-alive"}
                #if 1 > 0:
                try:
                    links_found = 0
                    new_links = 0
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
                        try:
                            headers = {'User-Agent': 'Mozilla/5.0'}
                            request = Request(url, headers=headers)
                            soup = bs.BeautifulSoup(urlopen(request).read(),'html.parser')
                        except:
                            pass



                    print("Aktuelle Seite: "+sitemap_url + str(seite) + sitemap_url_suffix)
                    #print (soup.prettify())

                    items = eval(result[18])

                    for item in items:
                        #print (item.prettify())

                        ref = ''
                        price = 0
                        location =''
                        bedroom = 0
                        bathroom = 0
                        size = 0
                        groundsize = 0
                        name =''
                        link = ''
                        image =''

                        try:
                            image =   eval(result[20])
                            print('Image      :',image)
                            if image[0:4] != 'http':
                                if image[1] != '/':
                                    image = '/' + image
                                image = root_url[:-1]+image
                                print ('Image      :',image)
                        except:
                            image =''
                        link= eval(result[21])
                        if link[0:4] != 'http':
                                link = root_url[:-1]+link
                        pos_link1 = link.find("&cHash")
                        if pos_link1 > 0:
                            link = (link[0:pos_link1])

                        print ('Link       :',link)
                        try:
                            price =  eval(result[11])
                            price = convert_to_float(price)
                            print ('Price      :', price)
                        except:
                            price = 0
                        try:
                            name =   eval(result[19])
                            name = re_replace(name)
                            print ('Name       :',name)
                        except:
                            name = ''

                        try:
                            name2 =   eval(result[41])
                            name2 = re_replace(name2)
                            #print ('Name2      :',name2)
                            name = name + ' ' + name2
                            print ('Name       :',name)
                        except:
                            name2 = ''
                        try:
                            ref =  eval(result[13])
                            print ('Ref        :',ref)
                        except:
                            ref =''
                        try:
                            location = eval(result[12])
                            location = strip_accents(location)
                            print ('Location   :',location)
                        except:
                            location =''
                        try:
                            type =eval(result[22])
                            print ('Type       :' , type)
                        except:
                            type =''

                        try:
                            bedroom =  eval(result[14])
                            #bedroom = (re.search('[0-9.]+',bedroom).group(0)).replace('.','')
                            bedroom = convert_to_float(bedroom)#(re.search('[0-9.]+',bedroom).group(0)).replace('.','')
                            print ('Bedroom    :',bedroom)
                        except:
                            bedroom = 0
                        try:
                            bathroom =  eval(result[15])
                            bathroom = convert_to_float(bathroom)
                            #bathroom = (re.search('[0-9.]+',bathroom).group(0)).replace('.','')
                            print ('Bathroom   :',bathroom)
                        except:
                            bathroom = 0
                        try:
                            size =  eval(result[16])
                            #size = (re.search('[0-9.]+',size).group(0)).replace('.','')
                            size = convert_to_float(size)
                            print ('Size       :', size)
                        except:
                            size=0
                        try:
                            groundsize = eval(result[17])
                            if 'ha' in groundsize:
                                groundsize = groundsize.replace('ha','').strip().replace(',','.')
                                groundsize = str(float(groundsize)*10000)
                            #groundsize = (re.search('[0-9.]+',groundsize).group(0)).replace('.','')
                            groundsize = convert_to_float(groundsize)
                            print ('Groundsize :',groundsize)
                        except:
                            groundsize=0
                        print ('--------------------------------------')
                        print ()
                        if size =='':
                            size=0
                        #print (eval(sitemap_selector))
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
                    if new_links == 0 and seite > 3 :
                        print('keine neuen Links gefunden')
                        break
                except:
                    pass

def missing_urls_try_again(site):
    try:
        urls=[]
        cur.execute("select url from sitemap sp where url not in (select url from properties where url = sp.url ) and site = '" + site + "' ")
        rows = cur.fetchall()

        for row in rows:
            print(row[0])
            urls.append(row[0])
    except:
        urls =[]
    return urls



def load_sitemap_all(site):

    urls=[]
    #cur.execute("select url from sitemap sp where site = '" + site + "' and url not in (select url from properties WHERE url = sp.url and last_scraped_date !=current_date)")
    #cur.execute("select url  from sitemap  where site = '" + site + "' and url not in (select url from properties) " )

    cur.execute("select url from sitemap sp where site = '" + site + "' ")
    rows = cur.fetchall()
    for row in rows:
        urls.append(row[0])

    qty_elements=  (len(urls))
    #log(site + ' '+ str(qty_elements)+' Elemente in Sitemap')
    return urls


def load_sitemap(site):

    urls=[]
    #cur.execute("select url from sitemap sp where site = '" + site + "' and url not in (select url from properties WHERE url = sp.url and last_scraped_date !=current_date)")
    cur.execute("select url  from sitemap  where site = '" + site + "' and url not in (select url from properties) " )

    #cur.execute("select url from sitemap sp where site = '" + site + "' ")
    rows = cur.fetchall()
    for row in rows:
        urls.append(row[0])

    qty_elements=  (len(urls))
    #log(site + ' '+ str(qty_elements)+' Elemente in Sitemap')
    return urls

def load_scraped(site):
    cur.execute("select * from sites  where site = '" + site + "' ")
    result = cur.fetchone()
    scraped_delete = result[6]
    print (day, scraped_delete)
    if (str(day) in str(scraped_delete)) :
        print ('delete scraped')
        cur.execute("select count(id)  from scraped   where create_date = current_date and site = '" + site + "' " )
        qty = cur.fetchone()

        if qty[0] < 30:
            cur.execute("delete from scraped  where site = '" + site + "' and scrap_it = 1  ")
            cur.execute("commit;")
            log(site + ' Scraped geloescht')

    try:
        cur.execute("select  url from scraped  where site = '" + site + "' and scrap_it = 1 ")
        rows = cur.fetchall()
        scraped = ''
        for row in rows:
            scraped = scraped + row[0] + '\n'
    except:
        scraped =''
    qty_elements=  (len(rows))
    log(site + ' '+ str(qty_elements)+' Elemente in Scraped')
    return scraped



def email_html(to, subject, body):
    try:
    #if 1 > 0:
        import smtplib
        import datetime
        from email.mime.multipart import MIMEMultipart
        from email.mime.text import MIMEText
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = 'info@schwenckner.net'
        msg['To'] = to
        msg['Content-Type'] = "text/html; charset=utf-8"
        fromaddr = 'info@schwenckner.net'
        toaddrs  = to
        part1 = MIMEText(body, 'plain')
        part2 = MIMEText(body.encode('utf-8'), 'html','utf-8')
        msg.attach(part1)
        msg.attach(part2)
        date = datetime.datetime.now().strftime( "%m/%d/%Y %H:%M" )
        server = smtplib.SMTP('mail.your-server.de')
        #server.set_debuglevel(1)
        server.starttls()
        server.ehlo()
        server.login('info@schwenckner.net', 'Info$%001')
        server.sendmail(fromaddr, toaddrs, msg.as_string())
        server.quit()
        return True
    except:
        pass
        return False


def database_service():
    log('Database Service start')



    sql = """
    UPDATE properties set offer_type = 'Buy' where (offer_type = 'Kauf' or offer_type = 'Zu verkaufen' or offer_type = 'For Sale');
    UPDATE properties set offer_type = 'Rent' where (offer_type = 'Miete' or offer_type = 'Mieten' or offer_type = 'Mieten' or offer_type = 'For Rent') ;

    Update properties  set property_type = '' where property_type = '0';


    Update properties  set property_type = '' where  property_type like'Not specified';
    Update properties  set property_type = '' where  property_type like'Low level';


    update properties set location = replace(location, 'Ponça', 'Ponca') where location like '%Ponça%' ;
    update properties set location = replace(location, 'Ponca', 'Ponsa') where location like '%Ponca%' ;

    --UPDATE properties  set price_update =  (select timestamp::date from changelog where product_id = properties.id and field_name = 'price' order by TIMESTAMP desc limit 1) where (price_update::date !=  (select timestamp::date from changelog where product_id = properties.id and field_name = 'price' order by TIMESTAMP desc limit 1) or price_update is null);
    UPDATE properties  SET price_update=( SELECT TIMESTAMP :: DATE FROM changelog WHERE product_id=properties.ID AND field_name='price' ORDER BY TIMESTAMP DESC LIMIT 1) WHERE (price_update !=(SELECT TIMESTAMP :: DATE FROM changelog WHERE product_id=properties.ID AND field_name='price' ORDER BY TIMESTAMP DESC LIMIT 1) OR price_update IS NULL AND (SELECT COUNT (ID) FROM changelog WHERE product_id=properties.ID AND field_name='price')> 0);

    delete from changelog where field_name = 'property_type';
    delete from changelog where field_name = 'state';
    delete from changelog where field_name = 'last_scraped_date';
    delete from changelog where field_name = 'location_id';
    delete from changelog where field_name = 'price_update';
    delete from changelog where field_name = 'changes_qty';

    update properties set country ='Spanien' where (country is null or country = '');
    update properties set country_state ='Mallorca' where (country_state is null or country_state = '') ;
    --UPDATE properties set country_state = trim(split_part(location , ',',2))   where country_state ='Mallorca' and site ='Engel & Völkers' and "location" not like '%Mallorca%';

    update properties set offer_type = 'Buy' where site = 'Minkner' and ref != 'M%' and (offer_type is null or offer_type = '');
    update properties set offer_type = 'Rent' where site = 'Minkner' and ref like 'M%' and offer_type != 'Rent' ;
    update properties set offer_type = 'Buy' where site != 'Minkner' and price > 30000 and (offer_type is null or offer_type = '');
    update properties set offer_type = 'Rent' where site != 'Minkner' and price <= 30000 and (offer_type is null or offer_type = '');
    update properties set offer_type = 'Buy' where site != 'Minkner' and price = 0 and (offer_type is null or offer_type = '');
    update properties set offer_type = 'Buy' where site = 'Porta Mallorquina' and name like '%kaufen%' and offer_type != 'Buy';
    update properties set offer_type = 'Buy' where price >100000 and offer_type ='Rent';

    UPDATE properties SET offer_type=CASE WHEN (REF LIKE 'MPH-V%') THEN 'Rent' ELSE 'Buy' END WHERE site='Primehomes' AND STATE='active' AND offer_type !=CASE WHEN (REF LIKE 'MPH-V%') THEN 'Rent' ELSE 'Buy' END;
    update properties set offer_type ='Buy'  where offer_type ='Rent' and price =0 and state ='active' and site !='Primehomes'  and(ref not like 'M%') and(ref not like 'R%');


    delete from properties where site ='4';
    update properties set offer_type ='Buy' where offer_type ='Sold';
    update changelog set old_value = 0 where old_value is null;
    update changelog set new_value = 0 where new_value is null;
    delete from changelog where (old_value is null or old_value ='' or old_value =' ');
    delete from changelog where (new_value is null or new_value ='' or new_value =' ');

    UPDATE properties SET image_url=NULL,image_download_state=0 WHERE image_url LIKE '%blank.gif%';


    commit;
    """
    cur.execute(sql)
    try:
        cur.execute("commit;")
    except:
        pass

    try:
        cur.execute("delete from sitemap WHERE create_date < CURRENT_DATE-10;") # nur sicherheitshalber wegen der ID
        cur.execute("commit;")
    except:
        pass

    try:
        cur.execute("delete from properties where ref = '0'") # nur sicherheitshalber wegen der ID
        cur.execute("commit;")
    except:
        pass

    try:
        cur.execute("""
           -- delete from relations;
            INSERT INTO relations (source_id,target_id)
            SELECT properties.ID, pro1.id
            FROM properties ,properties pro1
            WHERE
            properties.id!=pro1.id
            and properties.price > 0
            and pro1.price > 0
            and properties.price=pro1.price
            and properties.site != pro1.site
            AND properties.location_id = pro1.location_id
            AND properties.bedroom = pro1.bedroom
            and properties.bathroom = pro1.bathroom
            AND properties.property_type=pro1.property_type
            AND properties.state = 'active'
            AND pro1.state = 'active'
            and pro1.offer_type ='Buy' and properties.offer_type ='Buy'
            ON conflict DO NOTHING;
            """)
        cur.execute("commit;")

    except:
        pass

    try:
        cur.execute("""
           -- delete from relations;
            INSERT INTO relations (source_id,target_id)
            SELECT properties.ID, pro1.id
            FROM properties ,properties pro1
            WHERE
            properties.id!=pro1.id
            and properties.price > 0
            and pro1.price > 0
            and properties.price=pro1.price
            and properties.site != pro1.site
            AND properties.location_id = pro1.location_id
            AND properties.living_size = pro1.living_size
            AND properties.property_type=pro1.property_type
            AND properties.state = 'active'
            AND pro1.state = 'active'
            and pro1.offer_type ='Buy' and properties.offer_type ='Buy'
            ON conflict DO NOTHING;
            """)
        cur.execute("commit;")

    except:
        pass
    try:
        cur.execute("""
            INSERT INTO relations (source_id,target_id)
            SELECT properties.ID, pro1.id
            FROM properties ,properties pro1
            WHERE
            properties.id!=pro1.id
            and properties.price > 0
            and pro1.price > 0
            and properties.price=pro1.price
            and properties.site != pro1.site
			AND properties.location_id=pro1.location_id
			AND properties.bedroom=pro1.bedroom
			and properties.bathroom> 0
            AND properties.property_type=pro1.property_type
		    and pro1.site = 'Mallorcagold'
            and properties.site != 'Mallorcagold'
		    AND properties.state = 'active' AND pro1.state = 'active'
			and pro1.offer_type ='Buy' and properties.offer_type ='Buy'
            ON conflict DO NOTHING;
            """)
        cur.execute("commit;")

    except:
        pass
    try:
        cur.execute("""
           INSERT INTO relations (source_id,target_id)
            SELECT pro1.id, properties.ID
            FROM properties ,properties pro1
            WHERE
            properties.id!=pro1.id
            and properties.price > 0
            and pro1.price > 0
            and properties.price=pro1.price
            and properties.site != pro1.site
			AND properties.location_id=pro1.location_id
			AND properties.bedroom=pro1.bedroom
            AND properties.property_type=pro1.property_type
			and properties.bathroom> 0
		    and pro1.site = 'Mallorcagold'
            and properties.site != 'Mallorcagold'
		    AND properties.state = 'active' AND pro1.state = 'active'
			and pro1.offer_type ='Buy' and properties.offer_type ='Buy'
            ON conflict DO NOTHING;
            """)
        cur.execute("commit;")

    except:
        pass
    try:
        cur.execute("""
        UPDATE properties set competitors_qty = 0 where competitors_qty != 0 or competitors_qty is null;

        UPDATE properties set competitors_qty =
        (select count(id) from relations where source_id = properties.id)
        where (select count(id) from relations where source_id = properties.id) > 0
        ;
            """)
        cur.execute("commit;")

    except:
        pass


    cur.execute("delete from log where date < current_date -5;")

    print ('DB Service done')
    log('Database Service end')

def db_checks():


    log('Check urls in DB start')

    sites =''
    count = 0

    cur.execute("select url from sitemap sp , sites where sites.site = sp.site and sites.state = 1 and url not in (select url from properties where url = sp.url ); " )
    rows = cur.fetchall()
    for row in rows:
        sites = sites + (str(row[0]) + '\n<br>')
        errorlog('URL not in Propertys: ' + str(row[0]))
        count =+ 1


    log_mail = ''
    cur.execute("select log, date  from log  where date > current_date order by id desc " )
    rows = cur.fetchall()
    for row in rows:
        log_mail += str(row[1]) +' '+ str(row[0]) + '<br>\n'

    cur.execute("select count(id) from properties where image_download_state = 0 and state = 'active';")
    qty_witout_image = str(cur.fetchone()[0])
    log('Propertys without Image: ' + qty_witout_image)
    errorlog('Propertys without Image: ' + qty_witout_image)

    if count > 0:
        subject = 'Missing URLs - Probleme gefunden. ' + qty_witout_image + ' ohne Bild'
        x = email_html(recipient_email, subject, sites + '\n<br><br><br>' + str(log_mail))
    else:
        print ('Keine Probleme')
        #subject = 'Missing URLs - keine Probleme. ' + qty_witout_image + ' ohne Bild'
        #x = email_html(recipient_email, subject, '')

    log('Check urls in DB end')


    log("Check for missing new objects start")

    cur.execute("select site, (select max(create_date) from properties where sites.site = properties.site) from sites where (select max(create_date) from properties where sites.site = properties.site) < CURRENT_DATE - warn_days ;")
    rows = cur.fetchall()
    missing = ''
    found = 0
    for row in rows:
        name =  row[0]
        date_max =  row[1]
        print (name, date_max)
        errorlog('Missing new Objects from ' + name + ' ' + str(date_max))
        missing = missing + name + ' ' + str(date_max) + '<br>\n'
        found = found + 1
    if found > 0:
        subject = 'Mallorca: Missing new Objects from ' + str(found) + ' Suppliers'
        x = email_html(recipient_email, subject,  str(missing))

    log('Check for missing new objects end')

    cur.execute("select location, id from properties where location_id is null and state ='active'  ")
    rows = cur.fetchall()
    text = ''
    for row in rows:
        text = text + row[0] + '<br>\n'
        errorlog('Location not found: ' + row[0])

    cur.execute("select name, id from properties where (property_type is null or property_type ='') and state ='active' and create_date > current_date -10 ")
    rows = cur.fetchall()
    text = ''
    for row in rows:
        errorlog('Property Type not found: ' + row[0])

    cur.execute("select site  from sites  where last_scraped != current_date and state = 1  " )#and active = 1
    rows = cur.fetchall()
    text = ''
    for row in rows:
        text = text + row[0] + '<br>\n'
        errorlog('Site not scanned today: ' + row[0])



    cur.execute("select count(properties.id) from properties ,sites where sites.site = properties.site and create_date::date = CURRENT_DATE  and offer_type ='Buy' and country_state = 'Mallorca'  and country ='Spanien'" )
    qty = cur.fetchone()
    errorlog ('Neue Immobilien gefunden: ' + str(qty[0]))

        #print (text)
#    if text != '':
#        subject = 'Mallorca: Objects not scanned today'
#        x = email_html(recipient_email, subject,  str(text))

    print ('fertig')








def set_inactive():
    log('Set Active and inacive start')

    #Set inactive
    cur.execute("UPDATE properties pt SET STATE='inactive',inactive_date=CURRENT_DATE FROM sites WHERE sites.site=pt.site AND sites.last_scraped=CURRENT_DATE AND pt.STATE='active' AND url NOT IN (SELECT url FROM sitemap WHERE url=pt.url) AND country='Spanien'")
    cur.execute("commit;")

    #Set Active
    cur.execute("update properties pt set state = 'active', inactive_date = null where state !='active' and url in (select url from sitemap where url = pt.url) and country ='Spanien'")
    cur.execute("commit;")

    #Preise
    cur.execute("UPDATE properties SET price=sitemap.price,price_update=CURRENT_DATE FROM sitemap WHERE sitemap.url=properties.url AND properties.price !=sitemap.price AND sitemap.price IS NOT NULL;")
    cur.execute("commit;")

    #Changes QTY
    cur.execute("update properties set changes_qty =  (select count(id) from changelog where product_id = properties.id and field_name = 'price') where  changes_qty != ((select count(id) from changelog where product_id = properties.id and field_name = 'price')::int)  or changes_qty is null; ")
    cur.execute("commit;")

    #Bedroom
    cur.execute("UPDATE properties  SET bedroom = sitemap.bedroom FROM sitemap WHERE sitemap.url = properties.url AND (properties.bedroom != sitemap.bedroom or properties.bedroom is null) and sitemap.bedroom > 0;")
    cur.execute("commit;")

    #bathroom
    cur.execute("UPDATE properties  SET bathroom = sitemap.bathroom FROM sitemap WHERE sitemap.url = properties.url AND (properties.bathroom != sitemap.bathroom or properties.bathroom is null) and sitemap.bathroom > 0;")
    cur.execute("commit;")

    #Size
    cur.execute("UPDATE properties  SET living_size = sitemap.size  FROM sitemap  WHERE sitemap.url = properties.url  AND (properties.living_size != sitemap.size  or properties.living_size is null) AND sitemap.price IS NOT NULL and sitemap.size > 0;")
    cur.execute("commit;")

    #GroundSize
    cur.execute("UPDATE properties  SET ground_size=sitemap.groundsize FROM sitemap WHERE sitemap.url=properties.url AND (properties.ground_size !=sitemap.groundsize or properties.ground_size is null) AND sitemap.price IS NOT NULL AND sitemap.groundsize> 0;")
    cur.execute("commit;")

    #REF
    cur.execute("UPDATE properties SET ref=sitemap.ref FROM sitemap WHERE sitemap.url=properties.url AND (properties.ref !=sitemap.ref or properties.ref is null) AND (sitemap.ref IS NOT NULL and sitemap.ref !='')")
    cur.execute("commit;")

    #images
    cur.execute("UPDATE sitemap set image ='' where image like '%base64,%' ")
    cur.execute("commit;")
    cur.execute("UPDATE properties set image_url ='' where image_url like '%base64,%' ")
    cur.execute("commit;")
    cur.execute("UPDATE properties SET image_url=sitemap.image,image_download_state=0 FROM sitemap WHERE sitemap.url=properties.url AND sitemap.image != '' AND  sitemap.image is not null AND (properties.image_url is null or properties.image_url = '') AND properties.STATE='active' ")
    cur.execute("commit;")
    cur.execute("UPDATE properties SET image_url=sitemap.image,image_download_state=0 FROM sitemap WHERE sitemap.url=properties.url AND image<> properties.image_url AND sitemap.image !='' AND sitemap.image is not null AND properties.STATE='active' AND image_download_state !=1;")
    cur.execute("commit;")

    #Name Porta Mallorcina
    cur.execute("UPDATE properties SET name = sitemap.name FROM sitemap   WHERE sitemap.url=properties.url AND properties.STATE='active' and properties.name =	'Porta Mallorquina - Immobilien Mallorca';")
    cur.execute("commit;")

    #Name
    cur.execute("UPDATE properties SET NAME=sitemap.NAME FROM sitemap WHERE sitemap.url=properties.url AND properties.STATE='active' AND sitemap.NAME !='' AND properties.NAME='' ")
    cur.execute("commit;")

    print ('Set Active and inacive done')
    log('Set Active and inacive end')


def check_testmode(site):
    cur.execute("select testmode , state from sites  where site = '" + site + "' ")
    result = cur.fetchone()
    if result[0] == 1:
        testmode = True
        print ('-----------------TESTMODE-----------------')
        log(site + ' ----------------------------TESTMODUS --------------------------------------')
    elif  result[0] == 2: #All
        testmode = 'All'
        print ('-----------------ALL-----------------')
        log(site + ' ----------------------------ALL --------------------------------------')

    else:
        testmode = False

    return testmode
def reset_scraping_started():
    if hour < 6:
        cur.execute("update sites set scraping_started = 0 ;")
        cur.execute("commit;")
        print('Sites scraping_started reset')
    else:
        print ('Sites scraping_started nicht zurückgesetzt')

def reset_testmode():
    if hour < 24:
        cur.execute("update sites set testmode = 0 where testmode = 1;")
        cur.execute("commit;")
        print('Sites Testmode reset')
    else:
        print ('nix gemacht')

def reset_testmode_all(site):
        cur.execute("update sites set testmode = 0 where testmode = 2 and site = '" + site + "' ;")
        cur.execute("commit;")
        print('Sites Testmode All reset')

def image_one_download():
        log('Image One download start')#
        import urllib.request, datetime
        print(day)
        if day =='01':
            cur.execute("UPDATE properties set image_download_state = 0 where image_download_state = 2 and state ='active';")
            cur.execute("commit;")

        cur.execute("select image_url, id , create_date, url from properties where image_download_state = 0  and image_url is not null and state ='active';")

        rows = cur.fetchall()
        for row in rows:
            #if 1 > 0:
            try:
                url = urllib.parse.quote(row[0]).replace('https%3A//','https://') #.encode('utf-8')#.decode('utf8')
                url = row[0].replace('©','%C2%A9')
                try:
                    url = row[0].encode('latin1').decode('utf8') #.replace('©','%C2%A9')
                except:
                    pass
                imagename = str(row[1])+'_1.jpg'
                imagename_thumb = str(row[1])+'_thumb_1.jpg'
                filename_thumb = str(row[1])+'_thumb_1.jpg'

                year = str(datetime.datetime.strptime(str(row[2]), "%Y-%m-%d").year)

                print (imagename, url , imagename_thumb, row[3])
                imagename = dirname_images + 'images_big/' + imagename
                imagename_thumb = dirname_images + 'thumbs/' + imagename_thumb
                try:
                    print('opener.retrieve')
                    opener = urllib.request.URLopener()
                    opener.addheader('User-Agent', 'Mozilla/5.0')
                    filename, headers = opener.retrieve(url, imagename)
                except:
                    pass


                if not os.path.exists(imagename):
                    print ('urlretrieve')
                    try:
                        urlretrieve(url, imagename)
                    except:
                        pass
                #if os.path.exists(imagename_thumb):
                #    os.remove(imagename_thumb)
                if os.path.exists(imagename):
                    with Img(filename=imagename , resolution=80) as img:
                        width = img.width
                        height = img.height
                        ratio = int(200 * (height/width))
                        print(width, height, ratio)
                        img.resize(200, ratio)
                        img.save(filename=imagename_thumb)


                    with pysftp.Connection('www28.your-server.de', username='schweng_8', password='cacJ5rPrqJAWP1u1', cnopts=cnopts ) as sftp:
                        with sftp.cd('/'):             # temporarily chdir to public
                            try:
                                sftp.mkdir(year, mode=777)
                            except:
                                pass
                            print (year, imagename_thumb)
                            #sftp.cd('/' + year)
                            #sftp.put(imagename_thumb)
                            sftp.put(imagename_thumb, '/'+ year + '/' + filename_thumb)


                    cur.execute("update properties set image_download_state = 1 where id = %s;", ( [ row[1] ]))
                    cur.execute("commit;")
                else:
                    print (imagename, 'File existiert local nicht'  )
            except:
                pass
        cur.execute("update properties set image_download_state = 2 where image_download_state = 0 and image_url is not null and state ='active' and create_date < CURRENT_DATE-10;")
        cur.execute("commit;")

        log('Image One download end')

def images_download():
        cur.execute("select images, id from properties where images_download_state = 0 and country_state ='Mallorca' and images is not null order by id limit 100;")
        rows = cur.fetchall()
        for row in rows:
            id = row[1]
            images=row[0].split(',')
            #print (images)
            print ('Images in Array: ' , str(len(images)))
            count = 2
            for image in images:
                imagename = str(id)+'_' + str(count) + '.jpg'
                count +=1
                print(imagename, image)
                imagename = dirname + 'images_all/' + imagename
                urlretrieve(image, imagename)

            #count = 2
            #for image in images:
            #    imagename = str(id)+'_' + str(count) + '.jpg'
            #    count +=1
            #    print(imagename, 'Upload')
            #    imagename = dirname + 'images_all/' + imagename
                #if os.path.exists(imagename):
                #    with pysftp.Connection('www28.your-server.de', username='schweng_8', password='cacJ5rPrqJAWP1u1', cnopts=cnopts ) as sftp:
                #        with sftp.cd('/images_all/'):             # temporarily chdir to public
                #            sftp.put(imagename)

            cur.execute("update properties set images_download_state = 1 where id = %s;", ( [ id ]))
            cur.execute("commit;")

import re
import unicodedata

def strip_accents1(text):
    try:
        text = unicode(text, 'utf-8')
    except (TypeError, NameError): # unicode is a default on python 3
        pass
    text = unicodedata.normalize('NFD', text)
    text = text.encode('ascii', 'ignore')
    text = text.decode("utf-8")
    print (text)
    return ''.join(c for c in unicodedata.normalize('NFD', text)
        if not unicodedata.name(c).endswith('ACCENT'))
    #return str(text)

def strip_accents(s):
    try:
        return ''.join(c for c in unicodedata.normalize('NFD', s)
              if not unicodedata.name(c).endswith('ACCENT'))
    except:
        return(s)

def strip_accents_from_db():

    cur.execute("""select id, location , site from properties where  site ='Kensington' and  create_date = current_date order by  location""")

    rows = cur.fetchall()
    for row in rows:
        id = row[0]
        location =''
        location = strip_accents(row[1])
        print (location)

        cur.execute("update properties set location = %s where id = %s;", ( [ location, id ]))
        cur.execute("commit;")

def locations_temp_act():
    cur, conn = connect_properties()
    import time

    cur.execute("select count(id)  from locations  where update_date >= current_date-1 " )
    qty = cur.fetchone()
    if qty[0] > 0:
        start2 = time.time()
        log('Locations Temp wird aktualisiert ')
        cur.execute("""delete from locations_temp ;""")
        cur.execute("commit;")

        cur.execute("""insert into locations_temp (location_id, name) (SELECT  id , trim(lower(city)) from locations WHERE city is NOT NULL order by city ) ;""")
        cur.execute("commit;")

        cur.execute("""SELECT searchterms, id  from locations WHERE searchterms is NOT NULL and (searchterms !='' or searchterms !=' ') order by city ;""")
        searchs = cur.fetchall()

        for search in searchs:
            search_split = str(search[0]).split(',')
            for city2 in search_split :
                    if city2 != '':
                        try:
                            cur.execute("insert into locations_temp (location_id, name) values (%s, %s);",([ search[1], city2.lower().strip()]))
                            cur.execute("commit;")
                        except:
                            cur.execute("commit;")


        cur.execute("""delete from locations_temp where name ='';""")
        cur.execute("commit;")
        duration = str(convert_seconds(time.time()-start2))
        log('Locations Temp fertig' + ' ' + duration)


def set_locations():
    log('Locations start')
    import time
    start2 = time.time()

    locations_temp_act()
    print('Locations Temp fertig')
    cur, conn = connect_properties()
    sql = """
    update locations set country = 'Spanien' where country is null;
    update locations set country_state = 'Mallorca' where country_state is null;
    UPDATE properties set location_id = 0 where location_id is null;

    UPDATE properties set location = trim(split_part(location,'/', 2)) where site ='Kensington' and "location" like '%/%' and state = 'active';
    UPDATE properties set location = trim(split_part(location,'-', 1)) where site ='Casanova' and "location" like '%-%' and state = 'active';
    UPDATE properties set location = trim(split_part(location,'-', 2)) where site ='DC-Mallorca' and "location" like '%-%' and state = 'active';
    UPDATE properties set location = trim(split_part(location,'-', 1)) where site ='Immobilienmallorca'  and "location" like '%/%' and state = 'active';
    UPDATE properties set location = trim(split_part(location,'-', 1)) where site ='Mallorcagold'   and "location" like '%-%' and state = 'active';
    UPDATE properties set location = trim(split_part(location,'/', 2)) where site ='Primehomes'   and "location" like '%/%' and state = 'active';
    UPDATE properties set location = trim(split_part(location,'/', 2)) where site ='Sandberg'    and "location" like '%/%' and state = 'active';
    UPDATE properties set location = trim(split_part(location,'/', 2)) where site ='Toni Da Silva'    and "location" like '%/%' and state = 'active';
    UPDATE properties set location = trim(split_part(location,',', 4)) where site ='Engel & Völkers'    and "location" like '%,%' and state = 'active';
    UPDATE properties set location = trim(split_part(location,'-', 2)) where site ='Minkner' and "location" like '%-%' and state = 'active';
    delete from locations_temp where name ='';
    UPDATE properties SET location=split_part(LOWER (NAME),' in ',4) WHERE site='Neptunus' AND split_part(LOWER (NAME),' in ',4) !='' AND location=''  AND (location_id IS NULL OR location_id=0) and state = 'active';
    UPDATE properties SET location=split_part(LOWER (NAME),' in ',3) WHERE site='Neptunus' AND split_part(LOWER (NAME),' in ',3) !='' AND location='' AND (location_id IS NULL OR location_id=0) and state = 'active';
    UPDATE properties SET location=split_part(LOWER (NAME),' in ',2) WHERE site='Neptunus' AND split_part(LOWER (NAME),' in ',2) !='' AND location='' AND (location_id IS NULL OR location_id=0) and state = 'active';
    UPDATE properties SET location=split_part(LOWER (NAME),' von ',2) WHERE site='Neptunus' AND split_part(LOWER (NAME),' von ',2) !='' AND location='' AND (location_id IS NULL OR location_id=0) and state = 'active';
    -- UPDATE properties SET location_id=(SELECT location_id FROM locations_temp WHERE LOWER (properties.NAME) LIKE '%' || locations_temp.NAME  LIMIT 1) WHERE site='Neptunus' AND location='' AND (location_id IS NULL OR location_id=0);

    -- UPDATE properties  SET location_id=( SELECT location_id FROM locations_temp WHERE LOWER (properties.NAME) LIKE '%' || locations_temp.NAME LIMIT 1) WHERE (location_id IS NULL OR location_id=0) AND (SELECT location_id FROM locations_temp WHERE LOWER (properties.NAME) LIKE '%' || locations_temp.NAME LIMIT 1)> 0;


    commit;
    """
    cur.execute(sql)
    print('Trim Location fertig')


#    forbiden_words=['mallorca', 'spanien', 'nord', 'süd', 'südwest', 'südost', 'inselmitte', 'nordost', 'west' ,'zentrum', 'nordosten', 'norden', 'südwesten', 'südosten']

#    regions_list=[]
#    cur.execute("""SELECT name, id  from regions order by name ;""")
#    regions = cur.fetchall()
#    for region in regions:
#        regions_list.append(region[0])
    #print(regions_list)

    locations_dict= {'xxxx':0}
    cur.execute("""SELECT city, id  from locations WHERE city is NOT NULL order by city limit 1000 ;""")
    citys = cur.fetchall()
    for city in citys:
        if city not in locations_dict:# and city not in regions_list:
            locations_dict.update({city[0].lower(): city[1]})

    cur.execute("""SELECT searchterms, id  from locations WHERE searchterms is NOT NULL and searchterms !='' order by city ;""")
    searchs = cur.fetchall()

    for search in searchs:
        search_split = str(search[0]).split(',')
        for city2 in search_split:
            if city2.strip() not in locations_dict and city2 != '':# and city not in regions_list:
                locations_dict.update({city2.lower().strip(): search[1]})




    cur.execute("""select id, location , location_id , city from properties where
    id > 0
    -- (location_id is null or location_id = 0)
     and state = 'active'
    --and id=760960
    --order by location
     limit 1000000 """)



    rows = cur.fetchall()
    for row in rows:
        id = row[0]
        location_id = 0
        search_locations =[]
        location_id_org = row[2]
        city = row[3].lower().strip()
        location = strip_accents(row[1]).lower()
        search_location = location.split(',',1)[0].strip()
        search_city = city.rsplit(',',1)[0].strip()


        if search_location in locations_dict:
            location_id = locations_dict.get(search_location.strip(), 0)

        elif search_city !='' and search_city in locations_dict :
            location_id = locations_dict.get(search_city.strip(), 0)


        if location_id == 0:
            print('Nicht gefunden: ',  search_location,  location_id_org, id)
        #print(location_id, search_location)
        #if location_id != location_id_org and location_id !=0:

        if location_id > 0 and location_id != location_id_org:
            print(location_id, search_location, search_city, location_id_org, id)
            cur.execute("update properties set location_id = %s where id = %s;", ( [ location_id, id ]))
            cur.execute("commit;")


    cur.execute("UPDATE properties SET location_search=locations.area from locations WHERE location_id=locations.ID AND (location_search !=locations.area OR location_search IS NULL); ")
    cur.execute("commit;")
    cur.execute("UPDATE properties SET region=regions.NAME FROM locations,regions WHERE locations.region_id=regions.ID AND location_id=locations.ID AND (region !=regions.NAME OR region IS NULL);")
    cur.execute("commit;")
    cur.execute("UPDATE properties SET city=locations.city FROM locations WHERE location_id=locations.ID AND (properties.city !=locations.city OR location_search IS NULL);")
    cur.execute("commit;")
    cur.execute("update properties set location_search = location where location_id is null;")
    cur.execute("commit;")
    cur.execute("update locations set qty_active =  (select count (id) from properties where locations.id = location_id and state = 'active') ;")
    cur.execute("commit;")


    duration = str(convert_seconds(time.time()-start2))
    log('Locations fertig' + ' ' + duration)
def export_csv():
    dirname = os.path.dirname(os.path.abspath(__file__)) + '/'
    filename = dirname + 'immo.csv'

    if os.path.isfile(filename):
        os.remove(filename)
    g = open(filename, "w")#
    headers = "id;area;city;site;ref;price;bedroom;bathroom;ground_size;offer_type;image_url;name;size;url\n"
    g.write(headers)
    g.close

    cur.execute("""
        SELECT locations.ID,locations.area,locations.city,properties.site,properties.REF,properties.price,properties.bedroom,properties.bathroom,properties.ground_size,properties.offer_type,properties.image_url,NAME,living_size, url FROM properties JOIN locations ON properties.location_id=locations.id WHERE state='active' LIMIT 10;
     """)
    rows = cur.fetchall()
    for row in rows:
        print(row)



        g = open(filename, "a")
        g.write(str(row[0]) +';' + row[1]  +';' + row[2] +';' + row[3] +';' + row[4] +';'+  str(row[5]) +';'+ str(row[6]) +';'+ str(row[7]) +';'+ str(row[8]) +';'+ row[9] + ';'+ row[10] +';'+ row[11] +';'+ str(row[12]) +';'+ str(row[13]) +  '\n')
        g.close

    with pysftp.Connection('www28.your-server.de', username='schweng_8', password='cacJ5rPrqJAWP1u1', cnopts=cnopts ) as sftp:
        with sftp.cd('/immo/'):             # temporarily chdir to public
            #sftp.put(imagename)
                sftp.put(filename)


def get_details(site):
    import requests
    from bs4 import BeautifulSoup
    testmode =  check_testmode(site)
    urls=[]

    if testmode == False or testmode == 'All':
        cur.execute("select * from sites  where site = '" + site + "' ")
        result = cur.fetchone()

        if testmode == 'All':
            urls = load_sitemap_all(site)
            reset_testmode_all(site)
        else:
            urls= load_sitemap(site)


    if testmode == True:
            cur.execute("select * from sites  where  site = '" + site + "' ")
            result = cur.fetchone()
            urls.append(result[35])
    scraped =''

    for url in urls:
        try:
        #if 1 > 0:
            if   url  not in str(scraped)  :
                print ('URL        :',url)
                page = requests.get(url)
                soup = BeautifulSoup(page.content,'html.parser')
                if len(result[31]) > 5:
                    soup = eval(result[31])   #soup.find('div', class_='grid grid-66 clearfix')

                #print (soup.prettify())
                name = eval(result[32]) #
                print ('Name       :',name)
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

                try:
                    size = eval(result[29])
                    size = convert_to_float(size)
                    print ('Size       :',size)
                except:
                    pass
                try:
                    groundsize = eval(result[30])
                    groundsize = convert_to_float(groundsize)
                    print ('Groundsize :', groundsize)
                except:
                    pass
                try:
                    ref = eval(result[26]) #soup.find(text=re.compile('ImmoNr')).next_element.next_element.get_text().strip()
                    print ('Ref        :', ref)
                except:
                    pass
                try:
                    bedroom = eval(result[27])
                    bedroom = convert_to_float(bedroom)
                    print ('Bedroom    :',bedroom)
                except:
                    bedroom = 0

                try:
                    bathroom =  eval(result[28])
                    bathroom = convert_to_float(bathroom)
                    print ('Bathroom   :',bathroom)
                except:
                    bathroom = 0
                try:
                    offer_type = eval(result[34])
                    print ('Offer Type :',offer_type)
                except:
                    pass
                try:
                    property_type = eval(result[40])
                    print ('Type       :',property_type)
                except:
                    pass

                try:
                    price = eval(result[24]) #soup.find(text=re.compile('Warmmiete')).next_element.next_element.get_text().strip()
                    #print ('Price      :',price)
                    price = convert_to_float(price)
                    print ('Price      :',price)

                except:
                    price = 0
                    pass


                try:
                    location = eval(result[25]) #soup.find(text=re.compile('Ort')).next_element.next_element.get_text().strip()
                    print ('Location   :',location)
                    location = strip_accents(location)
                except:
                    pass

                if offer_type == '':
                    if price <= 30000 and price > 0:
                        offer_type = 'Rent'
                    else:
                        offer_type = 'Buy'


                country = 'Spanien'
                root_url = str(urlparse(url).scheme) + '://' + str(urlparse(url).hostname)

                try:
                    image = eval(result[33])

                    #Sandberg
                    pos_img = image.find('static.jpg')
                    if pos_img > 0:
                        pos_img = pos_img +10
                        image = (image[0:pos_img])

                    if image[0:4] != 'http':
                        image = root_url[:-1]+image
                        print ('Image      :',image)

                    print ('Image      :',image)

                except:
                    image =''

                images = []
                #for img in soup.find_all('div', class_='fotorama'):
                #    try:
                #        if  'https://smart.onoffice.de/smart20/Dateien/LietzImmobilien/smartSite20/multi_banner'in str(img['src']) :
                #            images.append(img.get('src'))
                #    except:
                #        pass
                #image = images[0]
                str_images = '' #(str(images).replace("'",'').replace("[",'').replace("]",''))
            #    print('#########################################')
                #print(str_images)
            #    print (image)
            #    print('#########################################')




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


        #------------------------------start update procedere
                check_ref = 0
                cur.execute("select id from properties where url = '" + url + "' ;")
                try:
                    check_ref = cur.fetchone()[0]
                except:
                    check_ref = 0
                print ( 'Check Ref1 :', check_ref)

                if check_ref == 0:
                    cur.execute("select id from properties where url like '" + url.replace('www.','').replace('https://','%') + "' ;")
                    try:
                            check_ref = cur.fetchone()[0]
                    except:
                            check_ref = 0
                    print ('Check Ref2 :', check_ref)



                if check_ref > 0:
                   # print (' ')
                    try:
                    #if 1> 0:
                        cur.execute("update properties set write_date = current_date , last_scraped_date = current_date ,state = 'active',  url  = %s ,name  = %s , price = %s, bedroom = %s , bathroom = %s, living_size = %s, ground_size = %s, location = %s , carpark = %s, terace = %s, ref = %s , offer_type = %s , property_type = %s , country_state = %s , area = %s , city = %s , country = %s , image_url = %s, images = %s where id = %s" ,
                        ([url, name,  price, bedroom, bathroom , size, groundsize, location, carpark, terrace, ref,  offer_type, property_type, country_state, area, city , country, image, str_images, check_ref]))
                        cur.execute("commit;")
                        print ('Update     :' , ref , check_ref, price, bedroom, bathroom)
                    except:
                        pass
                else:
                    print ('insert',ref,  name, site, bedroom, bathroom)
                    cur.execute("INSERT INTO properties ( create_date,write_date, last_scraped_date, state, site, name, ref, price, location, bedroom, bathroom, terace, living_size, ground_size, carpark, url, offer_type, property_type, country_state, area, city, country, image_url, images) \
                    values ( current_date,current_date, current_date,'active', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" , ( [site ,name, ref ,price, location,bedroom, bathroom, terrace, size, groundsize , carpark, url, offer_type, property_type, country_state, area, city, country, image, str_images]))
                    conn.commit()
                    print ("Insert     : Done")

                try:
                    cur.execute("commit;")
                except:
                    pass

                print ( '--------------------------------------------------------------------')
    #-------------------------end update


        except:
            pass



def get_missing_images():
    import requests
    from bs4 import BeautifulSoup
    urls=[]
    something_found =0
    cur.execute("select properties.id, url, properties.site from properties , sites where image_download_state !=1 and properties.state = 'active' and sites.site = properties.site and (create_property_from_sitemap = 2 or length(details_selector_image) > 5)")
    rows = cur.fetchall()
    for row in rows:
        urls.append(row[1])
        site=row[2]
        id = row[0]

        cur.execute("select * from sites  where site = '" + site + "' ")
        result = cur.fetchone()

        for url in urls:
                log('Try to find missing image: ' + url)
                page = requests.get(url)
                soup = BeautifulSoup(page.content,'html.parser')
                if len(result[31]) > 5:
                    soup = eval(result[31])   #soup.find('div', class_='grid grid-66 clearfix')
                    print (soup.prettify())
                try:
                    image = eval(result[33])

                    #Sandberg
                    pos_img = image.find('static.jpg')
                    if pos_img > 0:
                        pos_img = pos_img +10
                        image = (image[0:pos_img])

                    if image[0:4] != 'http':
                        root_url =''
                        root_url = str(urlparse(url).scheme) + '://' + str(urlparse(url).hostname)
                        image = root_url[:-1]+image
                except:
                    image =''

                try:
                    cur.execute("commit;")
                except:
                    pass

                if id > 0 and image !='':
                    try:
                        log('Missing image found: ' + url)
                        cur.execute("update properties set  image_url = %s where id = %s" ,
                        ([image, id]))
                        cur.execute("commit;")
                        print ('Update     :' , id, image)
                        something_found =1
                    except:
                        pass
    if something_found ==1:
        image_one_download()



def get_missing_types():
    import requests
    from bs4 import BeautifulSoup
    urls=[]
    log('Get Missing Types start')
    something_found =0
    cur.execute("SELECT properties.ID,url,properties.site FROM properties,sites WHERE (property_type='' OR property_type IS NULL) AND properties.STATE='active' AND sites.site=properties.site AND LENGTH (details_selector_type)> 5")
    rows = cur.fetchall()
    for row in rows:
        try:
            url=(row[1])
            site=row[2]
            id = row[0]
            cur.execute("select * from sites  where site = '" + site + "' ")
            result = cur.fetchone()

            log('Try to find missing type: ' + url)
            page = requests.get(url)
            soup = BeautifulSoup(page.content,'html.parser')
            property_type = eval(result[40])
            print ('Type       :',property_type)

            try:
                cur.execute("commit;")
            except:
                pass

            if id > 0 and property_type !='':
                try:
                    log('Type  found: ' + url)
                    cur.execute("update properties set  property_type = %s where id = %s" ,([property_type, id]))
                    cur.execute("commit;")
                    print ('Update     :' , id, property_type)

                except:
                    pass
        except:
            pass
    log('Get Missing Types end')

def get_image_immobilienmallorca(url):
    #url = 'https://www.immobilienmallorca.com/de/deia/1137-wohnung'
    #url = 'https://www.immobilienmallorca.com' +url

    from urllib.request import Request, urlopen
    import bs4 as bs, time, re

    headers = {'User-Agent': 'Mozilla/5.0'}
    request = Request(url, headers=headers)

    soup = bs.BeautifulSoup(urlopen(request).read(),'html.parser')
    image = soup.find('img', key=re.compile('c-6-slider')).get('key').strip()
    image = image[-4:]
    #https://www.immobilienmallorca.com/img/estate/3/3479_c-6___-1.jpg'
    prefix ='https://www.immobilienmallorca.com/img/estate/'
    suffix = '_c-6___-1.jpg'
    #print (image)
    image_url = prefix + image[0]+'/'+image + suffix
    #print (image_url)
    return image_url

def get_missing_image_immobilienmallorca():
    cur, conn = connect_properties()
    cur.execute("select id, site, image_url, url from properties where site = 'Immobilienmallorca' and (image_url ='' or image_url is null) " )
    rows = cur.fetchall()
    for row in rows:
        url =''
        url = row[3]
        id = row[0]
        print (id, url)
        image = ''
        image = get_image_immobilienmallorca(url)
        print('Image: ' , image)
        try:
            cur.execute("commit;")
        except:
            pass
        cur.execute("update properties set image_url = %s where id = %s ;", ([image, id]))
        cur.execute("commit;")

def scrap():

    something_to_check = 0
    start = time.time()
    log('Start Scraping')
    cur, conn = connect_properties()
    cur.execute("select site, create_property_from_sitemap, sitemap_items_qty from sites where create_property_from_sitemap >0 and state =1 and scraping_started = 0 and last_scraped != current_date order by id; " )
    rows = cur.fetchall()
    for row in rows:
        site =''
        site = row[0]
        start2 = time.time()
        log('Start '+site)
        cur.execute("update sites set scraping_started = 1 where site = %s ;", ([site]))
        cur.execute("commit;")
        if site == 'Montfair':
            get_xml_sitemap('Montfair', 'https://www.montfairestates.com/sitemap.xml')
        else:
            get_sitemap_extended(site)
        if row[1] ==1:
            create_propertys_from_sitemap(site)
        elif row[1]==2:
            get_details(site)
        duration_site = str(convert_seconds(time.time()-start2))
        log('End '+site+ ' ' + duration_site)
        qty_in_stitemap_last_time = float(row[2])
        qty_in_sitemap = float(len(load_sitemap_all(site)))
        if qty_in_sitemap > qty_in_stitemap_last_time *0.8:
            something_to_check = 1
            cur.execute("update sites set last_scraped = current_date ,scraping_started = 0, sitemap_items_qty = %s where site = %s ;", ([qty_in_sitemap, site]))
            cur.execute("commit;")
        else:
            subject = 'Nicht genug Einträge in Sitemap ' + site + ' ' + str(qty_in_sitemap) +' Einträge statt letztes mal: ' + str(qty_in_stitemap_last_time)
            x = email_html(recipient_email, subject, ' ')
            cur.execute("update sites set scraping_started = 0 where site = %s ;", ([site]))
            cur.execute("commit;")


    duration = str(convert_seconds(time.time()-start))

    log('End  Scraping -----------------------' +duration)

    conn.close



    if 1> 0:
#    if something_to_check ==1:
        strip_accents_from_db()
        get_missing_image_immobilienmallorca()
        check_types()
        database_service()
        set_inactive()
        set_locations()
        #images_download()
        image_one_download()
        get_missing_images()
        get_missing_types()
        mail('Minkner')
    if something_to_check ==1:
        db_checks()


    duration = str(convert_seconds(time.time()-start))
    print (duration)
    log('End Total Time: ' + duration)

    conn.close()




if __name__ == "__main__":
    reset_testmode()
    reset_scraping_started()
    check_dirs()
    scrap()
