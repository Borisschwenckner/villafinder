#!/usr/bin/python3
# -*- coding: utf-8 -*-
import bs4 as bs
import urllib.request, os
from datetime import date
today = date.today()
day = today.strftime("%d")
print(day)




def fullscan():
    dirname = os.path.dirname(os.path.abspath(__file__)) + '/'
    site = 'Porta'
    sitemap_xml =   dirname + 'sitemap_' + site.lower() + '.xml'
    print(site)
    sites = ''
    if os.path.exists(sitemap_xml):
        os.remove(sitemap_xml)

    max = 1000
    for seite in range(1,max): #1835 Haus kaufen
      print("Loop " + str(seite) + " startet.")
      links_found = 0
      new_links = 0
      try:
          soup = bs.BeautifulSoup(urllib.request.urlopen("https://www.porta-mallorquina.de/immobilien/suche-preis_desc/" + str(seite) ).read(),'lxml')
          print("Aktuelle Seite FULLSCAN: "+"https://www.porta-mallorquina.de/immobilien/suche-preis_desc/' + str(seite) ")
          for links in soup.find_all("a"):
              #print (links)
              if r"/immobilien/" in str(links.get("href")) and '.html' in str(links.get("href")) :
                #  print (str(links.get("href")))
                  link =  ('https://www.porta-mallorquina.de' + links.get("href").split("#")[0])
                  links_found += 1
                  if link not in str(sites):
                      new_links += 1
                      sites = sites + ('<url><loc>' + link + '</loc></url>\n')
          print (links_found, new_links)
          if new_links == 0 and seite > 10:
              print('keine neuen Links gefunden 2')
              g = open(sitemap_xml, "w")#
              g.write(sites)
              g.close
              break

      except:
          pass


def only_new():
    dirname = os.path.dirname(os.path.abspath(__file__)) + '/'
    site = 'Porta'
    sitemap_xml =   dirname + 'sitemap_' + site.lower() + '.xml'
    print(site)
    sites = ''
    lines = 0
    if os.path.exists(sitemap_xml):
        f = open(sitemap_xml)
        for line in f:
            sites = sites + line
            lines +=1
    max = int(lines/60) + 1
    print(max)

    for seite in range(1,2):
        print("Loop " + str(seite) + " startet.")
        try:
          soup = bs.BeautifulSoup(urllib.request.urlopen("https://www.porta-mallorquina.de/immobilien/aktuell/").read(),'lxml')
          print("Aktuelle Seite only NEW: "+"https://www.porta-mallorquina.de/immobilien/aktuell/")
          for links in soup.find_all("a"):
              #print (links)
              if r"/immobilien/" in str(links.get("href")) and '.html' in str(links.get("href")) :
                 # print (str(links.get("href")))
                  link =  ('https://www.porta-mallorquina.de' + links.get("href").split("#")[0])
                  #print (link)
                  if link not in str(sites):
                      sites = sites + ('<url><loc>' + link + '</loc></url>\n')
        except:
            pass
    g = open(sitemap_xml, "w")#
    g.write(sites)
    g.close


if __name__== "__main__":
      #if (day == '02' or day == '12' or  day == '22' ):
      fullscan()
      #only_new()
      print("FERTIG!")
