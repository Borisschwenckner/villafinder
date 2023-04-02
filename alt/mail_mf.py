#!/usr/bin/python3
# -*- coding: utf-8 -*-

import sys, locale
#sys.path.append('../')
#sys.path.append('/prg/')
import csv
import datetime
import psycopg2
import scrap_functions
import time
from datetime import date,  timedelta

import xlwt

filename_excel = '/prg/scraper/properties.xls'
print (sys.version)
text = '<!DOCTYPE html><html><head></head><body>'
cur, conn = scrap_functions.connect_properties()
##############################################################
name = 'Montfair'
##############################################################


cur.execute("""select count(properties.id) from properties ,sites where sites.site = properties.site and mail_customer like '%Montfair%' and create_date > CURRENT_DATE -1  and offer_type ='Buy' and country_state = 'Mallorca'   and country ='Spanien'""" )
qty = cur.fetchone()

cur.execute("""select count(properties.id) from properties ,sites where sites.site = properties.site and mail_customer like '%Montfair%' and inactive_date > CURRENT_DATE -1   and offer_type ='Buy' and country_state = 'Mallorca'   and country ='Spanien'""" )
qty_sold = cur.fetchone()

cur.execute("""select sites.site,name, ref, price, location , url , create_date from properties , sites where sites.site = properties.site and mail_customer like '%Montfair%' and create_date > CURRENT_DATE -1 AND country_state='Mallorca' and country ='Spanien' AND offer_type='Buy'  order by location , price desc  """ )
rows = cur.fetchall()
if len(rows) > 0:
    text = text + 'Neue Immobilien für ' + name + ' gefunden:<br><br><br>'
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

cur.execute("""SELECT properties.site,NAME,REF,price,LOCATION,url,create_date FROM properties,sites WHERE inactive_date > CURRENT_DATE-1 AND sites.site=properties.site AND country_state='Mallorca' AND country='Spanien' AND offer_type='Buy' AND mail_customer LIKE '%Montfair%' ORDER BY LOCATION,price DESC """ )

rows = cur.fetchall()
if len(rows) > 0:
    text = text + 'Diese Immobilien wurden nicht mehr gefunden:<br>'
    text = text + '____________________________________________<br><br><br>'
    #print (text)
    text = text + '<table border="0">'
    for row in rows:
        price = int(row[3])
        price = "{:,d}".format(price).replace(',','.')
        text = text + '<tr><td>Status</td><td><b>----VERKAUFT----</b></td></tr>'
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
text = text + '</body></html>'

#print (text)

subject = str(qty[0]) + ' neue und '+str(qty_sold[0])+' verkaufte Immobilien auf Mallorca gefunden'
#x = scrap_functions.email_html("boris@schwenckner.net", subject, text)
#x = scrap_functions.email_html("vanessa@montfairestates.com", subject, text)


name = 'Montfair'
cur.execute("select email  from customer  where last_email != current_date  and active = 1 and name = '" + name + "' " )
rows = cur.fetchall()
for row in rows:
    email = ''
    email = row[0]
    print (email)
    x = scrap_functions.email_html(row[0], subject, text)
    if x == True:
        cur.execute("update customer set last_email = current_date  where active = 1 and name = '" + name + "' and email = '" + email + "'" )
        cur.execute("commit;")

print ('fertig')
conn.close()
