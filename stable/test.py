#!/usr/bin/python3

url = 'https://www.immobilienmallorca.com/de/deia/1137-wohnung'


from urllib.request import Request, urlopen
#import pyppdf.patch_pyppeteer
import bs4 as bs, time, re

headers = {'User-Agent': 'Mozilla/5.0'}
request = Request(url, headers=headers)

soup = bs.BeautifulSoup(urlopen(request).read(),'html.parser')
        #except:
        #    pass
print (soup.prettify())

image = soup.find('img', key=re.compile('c-6-slider')).get('key').strip()
image = image[-4:]

#https://www.immobilienmallorca.com/img/estate/3/3479_c-6___-1.jpg'
# c-6-slider5194
prefix ='https://www.immobilienmallorca.com/img/estate/'
suffix = '_c-6___-1.jpg'
print (image)
image_url = prefix + image[0]+'/'+image + suffix
print (image_url)
