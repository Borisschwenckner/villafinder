#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
import requests, re, time, datetime, psycopg2, sys
from bs4 import BeautifulSoup
from urllib.parse import urlparse
from urllib.request import urlretrieve
sys.path.append('/prg/')
import scrap_functions

dirname = os.path.dirname(os.path.abspath(__file__)) + '/'
#filename = dirname + 'gorg.csv'

site = 'gorg'
try:
    scraped = open(filename_scraped).readlines()
except:
    scraped =''

scrap_functions.log('NSH start')

urls = ['https://www.nhc.noaa.gov/gtwo.php?basin=atlc&fdays=5']
#cur, conn = scrap_functions.connect_smarthome()

date = str(datetime.datetime.now().strftime("%Y-%m-%d"))

for url in urls:
#    try:

        print (url)
        page = requests.get(url)
        soup = BeautifulSoup(page.text, 'html.parser')
        image = soup.find('img', id='twofig5d').get('src')
        base_url = root_url = str(urlparse(url).scheme) + '://' + str(urlparse(url).hostname) #+'/'
        print (base_url + image)
        urlretrieve(base_url + image, dirname + 'images/pic_nhs.png')
        text = soup.find('div', class_='textproduct').get_text()
        #print (text)
        html = '<!DOCTYPE html><html><head></head><body>'

        html =html + '<img src="'+base_url + image + '" width="700">'
        html =html + '<br>'
        html =html + text

        html = html.replace('\n', '<br>')
        #html = 'HUHU'
        emails= []
       # emails = ['boris@schwenckner.net', 'bella@schwenckner.net']
        emails = ['boris@schwenckner.net']
        
        subject = 'HURRICANE INFO ' + date
        for email in emails:
            email = (email.strip())
            print (email)
            x = scrap_functions.email_html(email, subject, html)
            print (x)
        print (html)
        print (subject)
print ('fertig')

scrap_functions.log('NHS end')
