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

name_customer = 'Boris'

text = '<!DOCTYPE html><html><head></head><body>'
#conn = psycopg2.connect(database='properies', host='sql12.your-server.de', user='schweng_2', password = 'v9gyQ62fetFM2jDU')
#conn = psycopg2.connect(database='properties', host='nauticon.de', user='pgadmin', password = 'vGt5Zo$dfres7Zt5%de4XYPIUZjhz')
##conn = psycopg2.connect(database='properties', host='nauticon.de', user='pgadmin' ,  password = 'vGt5Zo$dfres7Zt5%de4XYPIUZjhz', sslmode='verify-ca' , sslcert='/root/.postgresql/postgresql.crt',  sslkey='/root/.postgresql/postgresql.key')
#cur = conn.cursor()
cur, conn = scrap_functions.connect_properties()

cur.execute("""select count(id) from properties where create_date::date = CURRENT_DATE AND "state"='active' """ )
qty = cur.fetchone()
print ('Neue Immobilien gefunden: ' + str(qty))


def excel_export():
        wbk = xlwt.Workbook(encoding='UTF-8')
        sheet = wbk.add_sheet('properties')
        sheet.set_horz_split_pos(1)
        #sheet.set_vert_split_pos(1)
        sheet.panes_frozen = True
        row = col = i = 0
        date_format = xlwt.XFStyle()
        date_format.num_format_str = 'dd.mm.yyyy'

        font = xlwt.Font() # Create the Font
        font.name = 'Arial'
        font.height = 160 # 16 * 20, for 16 point
        style = xlwt.XFStyle() # Create the Style
        style.font = font # Apply the Font to the Style
        #style = xlwt.easyxf('font: bold 1,height 160;')
        style2 = style
        style2.num_format_str = '€#,##0'
        #style2.num_format_str = '€#,##0.00'

        cur.execute("SELECT locations.city,NAME,round(price,0) AS price,(SELECT pro1.url FROM properties pro1,relations WHERE pro1.ID=target_id AND source_id=properties.ID AND site='Minkner' LIMIT 1) AS Minkner,(SELECT pro1.url FROM properties pro1,relations WHERE pro1.ID=target_id AND source_id=properties.ID AND site='Porta Mallorquina' LIMIT 1) AS Porta,(SELECT pro1.url FROM properties pro1,relations WHERE pro1.ID=target_id AND source_id=properties.ID AND site='Firstmallorca' LIMIT 1) AS FIRST FROM properties,locations WHERE location_id=locations.ID AND site='Engel & Völkers' AND price> 30000 ORDER BY city,price DESC")

        rows_data = cur.fetchall()
        header =  ([i[0] for i in cur.description])
        for i in header:
            if i:
                #print (i)
                sheet.write(row, col, i, style)
                sheet.col(col).width = 256 * (len(i) + 1)
                col+=1
        row = 1


        for row_data in rows_data:
                col = 0
                for e in row_data:
                    if col == 2:
                        sheet.write(row, col, e, style2)
                    elif col > 2:
                        if e == '' or e is None:
                            sheet.write(row, col, ' ',style)
                        else:
                            sheet.write(row,col,xlwt.Formula('HYPERLINK("%s";"Link")' % e),style)
                    else:
                        if e == '' or e is None:
                            e = ' '
                        sheet.write(row, col, e,style)
                    col+=1
                row += 1
        sheet.col(0).width = 256 * (10)
        sheet.col(1).width = 256 * (45)
        sheet.col(2).width = 256 * (15)
        sheet.col(3).width = 256 * (15)
        sheet.col(4).width = 256 * (15)
        sheet.col(5).width = 256 * (15)
        #wbk.freeze_panes(1, 1)
        wbk.save(filename_excel)

cur.execute("""SELECT site,COUNT (ID) AS qty_properties,( SELECT COUNT (ID) AS qty_properties FROM properties pro WHERE pro.site=properties.site  AND "state"='active' GROUP BY site) AS active,( SELECT COUNT (ID) AS qty_properties FROM properties pro WHERE pro.site=properties.site AND create_date=CURRENT_DATE AND "state"='active' GROUP BY site) AS today FROM properties  GROUP BY site;""" )
rows = cur.fetchall()
#print (len(rows))
if len(rows) > 0:
    text = text + 'Neue Immobilien wurden gefunden:<br><br><br>'

    text = text + 'Statistik:<br>'#
    text = text + '<table border="1"><tr><td>Site</td><td>Properties total</td><td>Properties active</td><td>Today New</td></tr>'

    for row in rows:
        name = (row[0])
        all = int(row[1])
        active = 0
        try:
            active = int(row[2])
        except:
            pass
        new = 0
        try:
            new = int(row[3])
        except:
            pass
        text = text + '<tr><td align="left">' + name + '</td><td align="right">' + str(all) + '</td><td align="right">' + str(active)  + '</td><td align="right">' + str(new)  + '</td></tr>'
    text = text + '</table><br><br><br>'

#    excel_export()

#else:
#    print ('nix')
#    x = functions.email_html("boris@schwenckner.net", 'Keine neuen Immobilien gefunden', 'text')


cur.execute("""select site,name, ref, price, location , url , create_date from properties where create_date > CURRENT_DATE -1 order by location , price desc limit 1000""" )
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



#print (text)
subject = str(qty[0]) + ' neue Immobilien auf Mallorca gefunden'


emails= []

cur.execute("select email from customer where last_email != current_date and active = 1 and name = '" + name_customer + "' " )
rows = cur.fetchall()
for row in rows:
    emails = row[0].split(",")
    for email in emails:
        email = (email.strip())
        print (email)
        x = scrap_functions.email_html(row[0], subject, text)
        if x == True:
            cur.execute("update customer set last_email = current_date  where active = 1 and name = '" + name_customer + "' " )
            cur.execute("commit;")


#x = scrap_functions.email_html("boris@schwenckner.net", subject, text)






print ('fertig')
conn.close()
