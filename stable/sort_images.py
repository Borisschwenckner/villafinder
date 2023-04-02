#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
#import requests, re, time, datetime, psycopg2, sys
import shutil
import datetime
#from urllib.parse import urlparse
#sys.path.append('/prg/')
import scrap_functions as functions

dirname = os.path.dirname(os.path.abspath(__file__)) + '/'
source_folder = '/mnt/video/netz/scraper_images/thumbs/'

cur, conn = functions.connect_properties()

cur.execute("select id , create_date  from properties where image_url is not null" )
images = cur.fetchall()
for image in images:
        #print (image[0], image[1])
        #774324_thumb_1.jpg
        filename = str(image[0]) + '_thumb_1.jpg'
        if  os.path.exists(source_folder + filename):
            #print (filename)
            year = datetime.datetime.strptime(str(image[1]), "%Y-%m-%d").year
#            year = datem.year
            if not os.path.exists(source_folder + str(year)):
                os.mkdir(source_folder + str(year))
            print (source_folder + filename, year, image[1])
            shutil.copy(source_folder + filename, source_folder + str(year) + '/' + filename)
