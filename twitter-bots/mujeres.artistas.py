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
from twython import Twython
from twitterbots import *
from wikidatafun import *

def main():
    APP_KEY, APP_SECRET = read_keys()
    OAUTH_TOKEN, OAUTH_TOKEN_SECRET = read_tokens()
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    
    queryplain = """
    SELECT ?work ?workLabel ?creatorLabel ?date ?image
    WHERE {
        ?work wdt:P31 wd:Q3305213.
        ?work wdt:P170 ?creator.
        ?creator wdt:P21 wd:Q6581072.
        ?work wdt:P571 ?date.
        ?work wdt:P18 ?image.
        SERVICE wikibase:label { bd:serviceParam wikibase:language "[AUTO_LANGUAGE],en". }
    }
    #LIMIT 100
    """
    queryurl = 'https://query.wikidata.org/bigdata/namespace/wdq/sparql?query=%s' % (urllib.parse.quote(queryplain))
    queryurl = '%s&format=json' % (queryurl)
    print("Loading...", queryurl)
    sparql = getURL(url=queryurl)
    json1 = loadSPARQL(sparql=sparql)
    qlist = []
    for result in json1['results']['bindings']:
        q = 'work' in result and result['work']['value'].split('/entity/')[1] or ''
        label = result['workLabel']['value']
        label = label.split(' (')[0]
        creator = result['creatorLabel']['value']
        creator = creator.split(' (')[0]
        date = result['date']['value']
        image = result['image']['value']
        
        if re.search('[Qt]\d+', label) or \
            re.search('[Qt]\d+', creator) or \
            re.search('[Qt]\d+', date) or \
            re.search('[Qt]\d+', image):
            continue
        
        if len(label) < 5 or \
            len(creator) < 5:
            continue
        
        year = date.split('-')[0]
        if not q in [x[0] for x in qlist]:
            if re.search(r'(?im)(baron|duch|duchess|king|marques|mon[jk]|nun|prince|princess|queen|virgin)', label):
                continue
            if re.search(r'(?im)^self[ -]*portrait$', label):
                label = 'Autorretrato'
            if int(year) > 1980:
                continue
            qlist.append([q, label, creator, year, image])
    
    print(len(qlist))
    random.shuffle(qlist)
    
    for work in qlist[:1]:
        print(work)
        imagename = urllib.parse.unquote(work[4].split('/Special:FilePath/')[1])
        x, xx = getCommonsMD5(imagename)
        imgurl = 'https://commons.wikimedia.org/wiki/File:%s' % (re.sub(' ', '_', imagename))
        imagenamequoted = urllib.parse.quote(re.sub(' ', '_', imagename))
        try:
            imgurl2 = 'https://upload.wikimedia.org/wikipedia/commons/thumb/%s/%s/%s/1200px-%s' % (x, xx, imagenamequoted, imagenamequoted)
            print(imgurl2)
            urllib.request.urlretrieve(imgurl2, 'mujeresartistas-tempimage.jpg')
        except:
            print('Error bajando')
            try:
                imgurl2 = 'https://upload.wikimedia.org/wikipedia/commons/%s/%s/%s' % (x, xx, imagenamequoted)
                print(imgurl2)
                urllib.request.urlretrieve(imgurl2, 'mujeresartistas-tempimage.jpg')
            except:
                print('Error bajando')
                continue
        
        img = open('mujeresartistas-tempimage.jpg', 'rb')
        response = twitter.upload_media(media=img)
        
        title = len(work[1]) > 30 and ('%s...' % work[1][:30]) or work[1]
        status = '%s (%s, %s) %s #ArteFemenino #ArteMujer #WomenArt' % (title, work[2], work[3], imgurl)
        print(status)
        raw = twitter.update_status(status=status, media_ids=[response['media_id']])
        tweetid = raw['id_str']
        print('Status:',status)
        print('Returned ID:',tweetid)

if __name__ == '__main__':
    main()
