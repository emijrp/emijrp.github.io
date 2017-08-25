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
    rsslimit = 25
    
    if 'hispantv' in url:
        m = re.findall('(?im)<title>([^<>]+?)</title>\s*<link>([^<>]+?)</link>', raw)
        for item in m[1:rsslimit]:
            title, url = item
            oldnews = loadOldNews()
            if not url in oldnews:
                news.append({'title':title.strip(),'url':url.strip()})
                oldnews.append(url.strip())
            saveOldNews(oldnews=oldnews)
    elif 'telesurtv' in url:
        m = re.findall('(?im)<title><!\[CDATA\[([^<>]+?)\]\]></title>\s*<link>([^<>]+?)</link>', raw)
        for item in m[:rsslimit]:
            title, url = item
            oldnews = loadOldNews()
            if not url in oldnews:
                news.append({'title':title.strip(),'url':url.strip()})
                oldnews.append(url.strip())
            saveOldNews(oldnews=oldnews)
    
    return news

def main():
    APP_KEY, APP_SECRET = read_keys()
    OAUTH_TOKEN, OAUTH_TOKEN_SECRET = read_tokens()
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    
    medios = {
        'hispantv-latinoamerica': {
            'rss': 'http://www.hispantv.com/services/news.asmx/Rss?category=51,52,54,55,56,57,58,59,110,148,149',
            'hashtags': ['#LatinoAmérica'],
        },
        'telesur-latinoamerica': {
            'rss': 'http://www.telesurtv.net/rss/RssLatinoamerica.html',
            'hashtags': ['#LatinoAmérica'],
        },
    }
    
    if len(sys.argv) > 1:
        medio = sys.argv[1]
        if not medio in medios.keys():
            print('Medio %s no encontrado' % (medio))
            sys.exit()
    else:
        print('No has indicado un medio')
        sys.exit()
    
    noticias = getNews(url=medios[medio]['rss'])
    titlelimit = 75
    for noticia in noticias:
        status = '#Noticia %s %s %s' % (len(noticia['title']) >= titlelimit and '%s...' % (noticia['title'][:titlelimit]) or noticia['title'], noticia['url'], ' '.join(medios[medio]['hashtags']))
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

