#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2017 emijrp <emijrp@gmail.com>
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import os
import random
import re
import sys
import time
import urllib
import urllib.request
from twython import Twython
from twitterbots import *

def loadOldNews():
    oldnews = []
    with open('noticias.oldnews.txt', 'r') as f:
        oldnews = f.read().strip().splitlines()
    return oldnews

def saveOldNews(oldnews=[]):
    with open('noticias.oldnews.txt', 'w') as f:
        f.write('\n'.join(oldnews))

def getNews(url=''):
    news = []
    if not url:
        return news
    raw = getURL(url=url)
    if not raw:
        return news
    #print(raw[:1000])
    rsslimit = 10
    
    if 'hispantv' in url:
        m = re.findall('(?im)<title>([^<>]+?)</title>\s*<link>([^<>]+?)</link>', raw)
        for item in m[1:rsslimit]:
            title, url = item
            oldnews = loadOldNews()
            if not url in oldnews:
                news.append({'title':re.sub('  +', ' ', title.strip()),'url':url.strip()})
                oldnews.append(url.strip())
            saveOldNews(oldnews=oldnews)
    elif 'telesurtv' in url:
        m = re.findall('(?im)<title><!\[CDATA\[([^<>]+?)\]\]></title>\s*<link>([^<>]+?)</link>', raw)
        for item in m[:rsslimit]:
            title, url = item
            oldnews = loadOldNews()
            if not url in oldnews:
                news.append({'title':re.sub('  +', ' ', title.strip()),'url':url.strip()})
                oldnews.append(url.strip())
            saveOldNews(oldnews=oldnews)
    
    return news

def addHashtags(s=''):
    s = re.sub('DD\.?HH\.?', 'DDHH', s)
    s = re.sub('EE\.?UU\.?', 'EEUU', s)
    rr = [ #para eliminar espacios para hashtags
        'Costa Rica', 
        'El Salvador',
        'Estados Unidos',
        'Puerto Rico',
        'República Dominicana',
        
        'Buenos Aires',
    ]
    for r in rr:
        s = re.sub(r, re.sub(' ', '', r), s)
    s = re.sub(r'(?m)(Argentina|Bolivia|Brasil|Chile|Colombia|CostaRica|Cuba|Ecuador|ElSalvador|España|EstadosUnidos|Guatemala|Honduras|M[eé][jx]ico|Nicaragua|Panam[áa]|Paraguay|Per[úu]|PuertoRico|Rep[úu]blicaDominicana|Rusia|Uruguay|Venezuela)', r'#\1', s)
    s = re.sub(r'(?m)(BuenosAires|Caracas|Quito|Washington)', r'#\1', s)
    s = re.sub(r'(?m)(Lula|Macri|Maduro|Moreno|Temer|Trump)', r'#\1', s)
    s = re.sub(r'(?m)(Parlasur)', r'#\1', s)
    s = re.sub(r'(?im)(bloqueo|constituyente|educa|energía|huelga|injerencias?|paro|petróle|reformas?|sanciones|salud|tarifazo|trabajo|transport)', r'#\1', s)
    s = re.sub(r'(?m)([A-Z]{3,})', r'#\1', s) #ONU, OEA, ALBA, DDHH, EEUU, etc
    return s

def main():
    APP_KEY, APP_SECRET = read_keys()
    OAUTH_TOKEN, OAUTH_TOKEN_SECRET = read_tokens()
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    
    medios = {
        'hispantv-latinoamerica': {
            'rss': 'http://www.hispantv.com/services/news.asmx/Rss?category=51,52,54,55,56,57,58,59,110,148,149',
            'hashtags': ['#Noticia', '#AméricaLatina'],
        },
        'telesur-latinoamerica': {
            'rss': 'http://www.telesurtv.net/rss/RssLatinoamerica.html',
            'hashtags': ['#Noticia', '#AméricaLatina'],
        },
    }
    medio = ''
    if len(sys.argv) > 1:
        medio = sys.argv[1]
        if not medio in medios.keys():
            print('Medio %s no encontrado' % (medio))
            sys.exit()
    else:
        print('No has indicado un medio, se leeran todos')
    
    if medio:
        mediosaleer = [medio]
    else:
        mediosaleer = medios.keys()
    
    noticias = []
    for medio in mediosaleer:
        noticias += getNews(url=medios[medio]['rss'])
    
    titlelimit = 75
    for noticia in noticias:
        title = len(noticia['title']) >= titlelimit and '%s...' % (noticia['title'][:titlelimit]) or noticia['title']
        title = addHashtags(s=title)
        status = '%s\n\n%s\n\n%s' % (' '.join(medios[medio]['hashtags']), title, noticia['url'])
        print(status)
        try:
            raw = twitter.update_status(status=status)
            tweetid = raw['id_str']
            print('Status:',status)
            print('Returned ID:',tweetid)
            time.sleep(3000/len(noticias))
        except:
            print('Error, demasiado largo?')
            time.sleep(5)
            pass
    
if __name__ == '__main__':
    main()

