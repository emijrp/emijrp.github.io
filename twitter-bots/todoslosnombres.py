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
import time
import urllib
import urllib.request
#from twython import Twython
#from twitterbots import *
from wikidatafun import *

def unquote(s):
    s = re.sub('&quot;', '"', s)
    return s

def main():
    #APP_KEY, APP_SECRET = read_keys()
    #OAUTH_TOKEN, OAUTH_TOKEN_SECRET = read_tokens()
    #twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    
    temas = ['bios', 'noticias', 'nuevos']
    if len(sys.argv) > 1:
        tema = sys.argv[1]
        if not tema in temas:
            print('Tema %s no encontrado' % (tema))
            sys.exit()
    else:
        print('No has indicado un tema')
        sys.exit()
    
    if tema == 'bios':
        pass
    
    elif tema == 'nuevos':
        tlnurl = 'http://www.todoslosnombres.org'
        html = getURL(url=tlnurl)
        m = re.findall(r'(?im)<span class="field-content">\s*<a href="/content/personas/([^<>]+?)">\s*([^<>]+?)\s*</a>\s*</span>\s*</span>\s*/\s*<span class="views-field views-field-field-municipio-de-residencia">\s*<span class="field-content">([^<>]+?)</span>\s*</span>', html)
        nuevos = []
        with open('todoslosnombres.nuevos.txt', 'r') as f:
            bios = f.read().strip().splitlines()
        for i in m:
            if not i[0] in nuevos:
                status = '[TodosLosNombres] %s (%s) http://www.todoslosnombres.org/content/personas/%s #MemoriaAntifascista' % (unquote(i[1]), unquote(i[2]), i[0])
                print(status)
                """raw = twitter.update_status(status=status)
                tweetid = raw['id_str']
                print('Status:',status)
                print('Returned ID:',tweetid)
                with open('todoslosnombres.nuevos.txt', 'a') as f:
                    f.write('%s\n' % i[0])"""
            time.sleep(5)
    
    elif tema == 'noticias':
        tlnurl = 'http://www.todoslosnombres.org'
        html = getURL(url=tlnurl)
        m = re.findall(r'(?im)<span class="field-content"><a href="/content/noticias/([^<>]+?)">([^<>]+?)</a></span>', html)
        noticias = []
        with open('todoslosnombres.noticias.txt', 'r') as f:
            noticias = f.read().strip().splitlines()
        for i in m:
            if not i[0] in noticias or 1:
                #no poner [TodosLosNombres] de prefijo porq las noticias son refritos de otras webs y así se ahorra caracteres también
                status = '%s http://www.todoslosnombres.org/content/noticias/%s #MemoriaAntifascista #noticia' % (len(unquote(i[1])) > 80 and '%s...' % unquote(i[1])[:80] or unquote(i[1]), i[0])
                print(status)
                tlnurl2 = 'http://www.todoslosnombres.org/content/noticias/%s' % (i[0])
                html2 = getURL(url=tlnurl2)
                n = re.findall('(?im)<img typeof="foaf:Image" src="([^<>\?]+?)\?', html2)
                response = ''
                if n and n[0]:
                    imageurl = n[0]
                    print(imageurl)
                """    urllib.request.urlretrieve(imageurl, 'todoslosnombres.noticias.tempimage.jpg')
                    img = open('todoslosnombres.noticias.tempimage.jpg', 'rb')
                    response = twitter.upload_media(media=img)
                raw = ''
                if response:
                    raw = twitter.update_status(status=status, media_ids=[response['media_id']])
                else:
                    raw = twitter.update_status(status=status)
                tweetid = raw['id_str']
                print('Status:',status)
                print('Returned ID:',tweetid)
                with open('todoslosnombres.noticias.txt', 'a') as f:
                    f.write('%s\n' % i[0])"""
            time.sleep(5)
    
if __name__ == '__main__':
    main()
