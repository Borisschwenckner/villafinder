#!/usr/bin/python3
# -*- coding: utf-8 -*-
import bs4 as bs
import urllib.request, os, time
from datetime import date
import requests
today = date.today()
day = today.strftime("%d")
print(day)




def only_new():
      dirname = os.path.dirname(os.path.abspath(__file__)) + '/'
      site = 'First'
      sitemap_xml =   dirname + 'sitemap_' + site.lower() + '.xml'
      print(site, sitemap_xml)
      sites = ''
#      if os.path.exists(sitemap_xml):
#            f = open(sitemap_xml, "r")
#            for line in f:
#                sites = sites + line
#            f.close
#      sites = ''
      max = 10
      request_headers = {
            "Accept-Language": "en-US,en;q=0.5",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Referer": "http://thewebsite.com",
            "Connection": "keep-alive"}
      for seite in range(0,max): #
            print("Loop " + str(seite) + " startet.")
            try:
            #if 1 > 0:
              #print (seite)
              headers = request_headers
              page = requests.get("https://www.firstmallorca.com/de/neu-gelistet/" +str(seite))
              soup = bs.BeautifulSoup(page.content,'lxml')
              print("Aktuelle Seite only NEW: "+"https://www.firstmallorca.com/de/neu-gelistet/" + str(seite))
              for links in soup.find_all("a"):
                 # print (links)
                  if str(links.get("href"))[-2].isdigit() and (str(links.get("href"))[-7] == '/' or str(links.get("href"))[-6] == '/' or str(links.get("href"))[-5] == '/' or str(links.get("href"))[-8] == '/'):
                      link =  ('https://www.firstmallorca.com' + links.get("href").split("#")[0])
                      if link not in str(sites):
                          sites = sites + ('<url><loc>' + link + '</loc></url>\n')
            except:
                pass
            g = open(sitemap_xml, "w")#
            g.write(sites)
            g.close

def fullscan():
    dirname = os.path.dirname(os.path.abspath(__file__)) + '/'
    site = 'First'
    sitemap_xml =   dirname + 'sitemap_' + site.lower() + '.xml'
    sites = ''
    max = 1000

    request_headers = {
            "Accept-Language": "en-US,en;q=0.5",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Referer": "http://thewebsite.com",
            "Connection": "keep-alive"}

    search_urls =['https://www.firstmallorca.com/de/mieten/','https://www.firstmallorca.com/de/kaufen/']
#    search_urls =['https://www.firstmallorca.com/de/mieten/']
    for search_url in search_urls:
        for seite in range(0,max): #
            print("Loop " + str(seite) + " startet.")
            try:
                links_found = 0
                new_links = 0
                headers = request_headers
                page = requests.get(search_url + str(seite))
                soup = bs.BeautifulSoup(page.content,'lxml')
                print("Aktuelle Seite fullscan: "+ search_url + str(seite))

                for links in soup.find_all("a"):

                    if str(links.get("href"))[-2].isdigit() and (str(links.get("href"))[-7] == '/' or str(links.get("href"))[-6] == '/' or str(links.get("href"))[-5] == '/' or str(links.get("href"))[-8] == '/'):
                        links_found += 1
                        link =  ('https://www.firstmallorca.com' + links.get("href").split("#")[0])
                        if link not in str(sites):
                            sites = sites + ('<url><loc>' + link + '</loc></url>\n')
                            new_links += 1
                #    else:
                #        print ('Link NOT to Sitemap: ', str(links.get("href")))

                print (links_found, new_links)
                if new_links == 0 and seite > 10:
                    print('keine neuen Links gefunden 2')
                    g = open(sitemap_xml, "w")
                    g.write(sites)
                    g.close
                    break
            except:
                pass



if __name__== "__main__":
      #if (day == '02' or day == '12' or  day == '22' ):
      fullscan()
      #only_new()
      print("FERTIG!")
