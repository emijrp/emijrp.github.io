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
import urllib
import urllib.request
from twython import Twython
from twitterbots import *

def main():
    APP_KEY, APP_SECRET = read_keys()
    OAUTH_TOKEN, OAUTH_TOKEN_SECRET = read_tokens()
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    
    sellos = {
        'rda': {
            'title': 'Sellos de la República Democrática Alemana', 
            'hashtags': ['#SellosRDA', '#GDRstamps', '#RDA', '#GDR', '#sellos', '#stamps'], 
            'url': 'https://commons.wikimedia.org/wiki/User:Emijrp/Sellos_RDA?action=raw',
        },
        'urss': {
            'title': 'Sellos de la Unión Soviética', 
            'hashtags': ['#SellosURSS', '#USSRstamps', '#URSS', '#USSR', '#sellos', '#stamps'], 
            'url': 'https://commons.wikimedia.org/wiki/User:Emijrp/Sellos_URSS?action=raw',
        },
    }
    
    if len(sys.argv) > 1:
        tema = sys.argv[1]
        if not tema in sellos.keys():
            print('Tema %s no encontrado' % (texto))
            sys.exit()
    else:
        print('No has indicado un tema')
        sys.exit()
    
    commonsurl = sellos[tema]['url']
    raw = getURL(url=commonsurl)
    works = re.findall(r'(?im)File:([^\|\n]+?)\n', raw)
    random.shuffle(works)
    selectedworks = works[0:4]
    print(selectedworks)
    
    media_ids = []
    for selectedwork in selectedworks:
        imagename = selectedwork
        x, xx = getCommonsMD5(imagename)
        imgurl = 'https://commons.wikimedia.org/wiki/File:%s' % (re.sub(' ', '_', imagename))
        imgurl2 = 'https://upload.wikimedia.org/wikipedia/commons/%s/%s/%s' % (x, xx, urllib.parse.quote(re.sub(' ', '_', imagename)))
        print(imgurl2)
        urllib.request.urlretrieve(imgurl2, 'sellos-tempimage.jpg')
        img = open('sellos-tempimage.jpg', 'rb')
        response = twitter.upload_media(media=img)
        media_ids.append(response['media_id'])
    status = '%s %s' % (sellos[tema]['title'], ' '.join(sellos[tema]['hashtags']))
    print(status)
    raw = twitter.update_status(status=status, media_ids=media_ids)
    tweetid = raw['id_str']
    print('Status:',status)
    print('Returned ID:',tweetid)

if __name__ == '__main__':
    main()
