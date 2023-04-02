#!/usr/bin/python3
import psycopg2
import sys, csv, re, os
from datetime import datetime
sys.path.append('/prg/')
sys.path.append('../')

import functions
#conn = psycopg2.connect(database='properties', host='nauticon.de', user='postgres' ,  password = 'Webfor:;2014', sslmode='verify-ca' , sslcert='/root/.postgresql/postgresql.crt',  sslkey='/root/.postgresql/postgresql.key')
dirname = os.path.dirname(os.path.abspath(__file__)) + '/'
cur, conn = functions.connect_properties()
files = []
for file in os.listdir(dirname):
    if file.endswith(".csv") and file.startswith("data_"):
        print(os.path.join(dirname, file))
        files.append(dirname + file)
print (files)

#files = [ dirname + 'engel.csv']

for file in files:
    print (file)
    dst = ''
    #dst = ( dirname + 'sicher/' + os.path.basename(file))
    dst = ( dirname + 'sicher/' + os.path.basename(file) + '_' + datetime.strftime(datetime.now(), '%Y_%m_%d'))
    #print (dst)
    if not os.path.exists(file):
        pass
    #    x = functions.email_html("boris@schwenckner.net", 'Scraping File nicht vorhanden: ' + file, ' ')
    else:


        reader = csv.reader(open(file,'r'),delimiter=';')
        try:
            row = next(reader)
        except:
            pass
        for row in reader:
            #print (row)
            try:
            #if 1 > 0:
                site =  row[0]
                name = row[1].strip()
                bedroom = 0
                bathroom = 0
                carpark =''
                price = 0
                country = ''
                aera = ''
                state = ''
                city = ''
                property_type = ''
                offer_type =''

                try:
                    price = row[3]
                except:
                    price = 0
                ref = row[2].strip()
                try:
                    location = row[4].strip()
                except:
                    location = ''
                try:
                    terace = (re.search('[0-9.]+',row[7]).group(0)).replace('.','')
                except:
                    terace = 0
                try:
                    size = (re.search('[0-9.]+',row[8]).group(0)).replace('.','')
                except:
                    size = 0
                try:
                    ground_size = (re.search('[0-9.]+',row[9]).group(0)).replace('.','')
                except:
                    ground_size = 0
                try:
                    carpark = row[10]
                except:
                    carpark = ''
                if carpark =='✓':
                    carpark = 'yes'
                url = row[11]
                try:
                    country = row[12]
                except:
                    country =''
                try:
                    country_state = row[13]
                except:
                    country_state =''
                try:
                    area = row[14]
                except:
                    area =''
                try:
                    city = row[15]
                except:
                    city =''
                #print(city)

                try:
                    property_type = row[16]
                except:
                    property_type =''
                try:
                    offer_type = row[17].replace('Kauf','Buy').replace('Miete','Rent')
                except:
                    offer_type =''
                #print (offer_type)

                try:
                    bedroom = row[5].strip()
                except:
                    bedroom = 0
                if bedroom.isdigit():
                    pass
                else:
                    bedroom = 0
                try:
                    bathroom = row[6].strip()
                except:
                    bathroom = 0
                if bathroom.isdigit():
                    pass
                else:
                    bathroom = 0

                #print (site, name, ref, price, bedroom, bathroom, size, ground_size)
                #print (ref, url, offer_type, property_type, city, aera, country, country_state, site, bathroom, bedroom, price)
                check_ref = 0
                #cur.execute("select id from properties where ref = '" + ref + "' and site = '" + site + "';")
                cur.execute("select id from properties where url = '" + url + "' ;")
                try:
                    check_ref = cur.fetchone()[0]
                except:
                    check_ref = 0


                print (check_ref)
                try:
                    cur.execute("commit;")

                except:
                    pass
                if check_ref > 0:
                    cur.execute("update properties set write_date = current_date , last_scraped_date = current_date ,state = 'active', name  = %s , price = %s, bedroom = %s , bathroom = %s, living_size = %s, ground_size = %s, location = %s , carpark = %s, terace = %s, ref = %s , offer_type = %s , property_type = %s , country_state = %s , area = %s , city = %s , country = %s where id = %s" ,
                    ([name,  price, bedroom, bathroom , size, ground_size, location, carpark, terace, ref,  offer_type, property_type, country_state, area, city , country, check_ref]))
                    cur.execute("commit;")
                    print ('update' , ref , check_ref, price, bedroom, bathroom)
                else:
                    #print ('Delete')
                    #cur.execute("delete from properties where ref = %s and site = %s;", ([ref ,site]))
                    #cur.execute("commit;")
                    print ('insert',ref,  name, site, bedroom, bathroom)

                    cur.execute("INSERT INTO properties ( create_date,write_date, last_scraped_date, state, site, name, ref, price, location, bedroom, bathroom, terace, living_size, ground_size, carpark, url, offer_type, property_type, country_state, area, city, country) \
                    values ( current_date,current_date, current_date,'active', %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)" , ( [site ,name, ref ,price, location,bedroom, bathroom, terace, size, ground_size , carpark, url, offer_type, property_type, country_state, area, city, country]))
                    conn.commit()
                    print ("Insert Done")


            except:
                pass
        from shutil import copyfile
        copyfile(file, dst)
        os.remove(file)

cur.execute("commit;")

#cur.execute("INSERT INTO relations (source_id,target_id) SELECT ID,(SELECT ID FROM properties pro1 WHERE properties.price=pro1.price AND properties.location_id=pro1.location_id AND properties.bedroom=pro1.bedroom AND properties.bathroom=pro1.bathroom AND site<> 'Engel & Völkers' LIMIT 1) FROM properties WHERE site='Engel & Völkers' AND ( SELECT ID FROM properties pro1 WHERE properties.price=pro1.price AND properties.location_id=pro1.location_id AND properties.bedroom=pro1.bedroom AND #properties.bathroom=pro1.bathroom AND site<> 'Engel & Völkers' LIMIT 1) IS NOT NULL ON conflict DO NOTHING;")
#cur.execute("commit;")


cur.execute("update properties set changes_qty =  (select count(id) from changelog where product_id = properties.id and field_name = 'price') where  changes_qty != ((select count(id) from changelog where product_id = properties.id and field_name = 'price')::int)  ;commit; ")



sql = """
Update properties  set property_type = '' where property_type = '0';
Update properties  set property_type = 'Villa' where (name like '%vill%' or name like '%Vill%') and (property_type is null or property_type ='');
Update properties  set property_type = 'Villa' where (name like '%Anwesen%' or name like '%anwesen%') and  (property_type is null or property_type ='');

Update properties  set property_type = 'Wohnung' where (name like '%apartment%' or name like '%Apartment%') and (property_type is null or property_type ='');
Update properties  set property_type = 'Wohnung' where (name like '%wohnung%' or name like '%Wohnung%') and (property_type is null or property_type ='');
Update properties  set property_type = 'Wohnung' where (name like '%sudio%' or name like '%Studio%') and (property_type is null or property_type ='');

Update properties  set property_type = 'Haus' where (name like '%haus%' or name like '%Haus%') and  (property_type is null or property_type ='');

Update properties  set property_type = 'Penthouse' where (name like '%penthouse%' or name like '%Penthouse%') and (property_type != 'Haus' and (property_type is null or property_type =''));
Update properties  set property_type = 'Grundstück' where (name like '%grundstück%' or name like '%Grundstück%') and (property_type is null or property_type ='');
Update properties  set property_type = 'Finca' where (name like '%finca%' or name like '%Finca%') and (property_type is null or property_type ='');

Update properties  set property_type = 'Haus' where (name like '%chalet%' or name like '%Chalet%') and (property_type is null or property_type ='');
Update properties  set property_type = 'Grundstück' where (name like '%grund%' or name like '%Grund%') and (property_type is null or property_type ='');
Update properties  set property_type = 'Wohnung' where (name like '%duplex%' or name like '%Duplex%') and (property_type is null or property_type ='');



-- UPDATE properties  set price_update =  null;
UPDATE properties  set price_update =  (select timestamp::date from changelog where product_id = properties.id and field_name = 'price' order by TIMESTAMP desc limit 1) where (price_update::date !=  (select timestamp::date from changelog where product_id = properties.id and field_name = 'price' order by TIMESTAMP desc limit 1) or price_update is null);

delete from changelog where field_name = 'property_type';
delete from changelog where field_name = 'state';
delete from changelog where field_name = 'last_scraped_date';
delete from changelog where field_name = 'location_id';
delete from changelog where "field_name" = 'price_update';
delete from changelog where "field_name" = 'changes_qty';

update properties set country ='Spanien' where (country is null or country = '');
update properties set country_state ='Mallorca' where (country_state is null or country_state = '') ;

update properties set offer_type = 'Buy' where site = 'Minkner' and ref != 'M%' and (offer_type is null or offer_type = '');
update properties set offer_type = 'Rent' where site = 'Minkner' and ref like 'M%' and (offer_type is null or offer_type = '');
update properties set offer_type = 'Buy' where site != 'Minkner' and price > 30000 and (offer_type is null or offer_type = '');
update properties set offer_type = 'Rent' where site != 'Minkner' and price <= 30000 and (offer_type is null or offer_type = '');
update properties set offer_type = 'Buy' where site != 'Minkner' and price = 0 and (offer_type is null or offer_type = '');

update properties set country = 'Deutschland'  where country = 'Spanien' and site = 'Immobilienscout';
update properties set country = 'Deutschland'  where country = 'Spanien' and site = 'Grossmnann';

delete from properties where site ='4';

commit;
"""
cur.execute(sql)



conn.close()
