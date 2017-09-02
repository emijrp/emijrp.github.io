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

import json
import os
import random
import re
import sys
import time
import urllib
import urllib.parse
import urllib.request
from twython import Twython
from twitterbots import *
from wikidatafun import *

countrynames = { 
    'albania': 'Albania', 
    'algeria': 'Algeria', 
    'andorra': 'Andorra', 
    'antarctica': 'Antarctica', 
    'argentina': 'Argentina', 
    'armenia': 'Armenia', 
    'armenia-nagorno': 'Armenia', 
    'aruba': 'Aruba', 
    'austria': 'Austria', 
    'australia': 'Australia', 
    'azerbaijan': 'Azerbaijan', 
    'bangladesh': 'Bangladesh', 
    'belarus': 'Belarus', 
    'belgium': 'Belgium', 
    'bolivia': 'Bolivia', 
    'brazil': 'Brazil', 
    'bulgaria': 'Bulgaria', 
    'cambodia': 'Cambodia', 
    'cameroon': 'Cameroon', 
    'canada': 'Canada', 
    'chile': 'Chile', 
    'china': 'China', 
    'colombia': 'Colombia', 
    'croatia': 'Croatia', 
    'czechrepublic': 'Czech Republic', 
    'denmark': 'Denmark', 
    'dutch-caribbean': 'Dutch Caribbean', 
    'egypt': 'Egypt', 
    'elsalvador': 'El Salvador', 
    'estonia': 'Estonia', 
    'finland': 'Finland', 
    'france': 'France', 
    'georgia': 'Georgia', 
    'germany': 'Germany', 
    'ghana': 'Ghana', 
    'greece': 'Greece', 
    'hongkong': 'Hong Kong', 
    'hungary': 'Hungary', 
    'india': 'India', 
    'iran': 'Iran', 
    'iraq': 'Iraq', 
    'ireland': 'Ireland', 
    'israel': 'Israel', 
    'italy': 'Italy', 
    'jordan': 'Jordan', 
    'kenya': 'Kenya', 
    'kosovo': 'Kosovo', 
    'latvia': 'Latvia', 
    'lebanon': 'Lebanon', 
    'liechtenstein': 'Liechtenstein', 
    'luxembourg': 'Luxembourg', 
    'macedonia': 'Macedonia', 
    'madagascar': 'Madagascar', 
    'malaysia': 'Malaysia', 
    'malta': 'Malta', 
    'mexico': 'Mexico', 
    'morocco': 'Morocco', 
    'nepal': 'Nepal', 
    'netherlands': 'Netherlands', 
    'nigeria': 'Nigeria', 
    'norway': 'Norway', 
    'pakistan': 'Pakistan', 
    'palestine': 'Palestine', 
    'panama': 'Panama', 
    'per': 'Peru', 
    'philippines': 'Philippines', 
    'poland': 'Poland', 
    'portugal': 'Portugal', 
    'qatar': 'Qatar', 
    'romania': 'Romania', 
    'russia': 'Russia', 
    'saudiarabia': 'Saudi Arabia', 
    'serbia': 'Serbia', 
    'slovakia': 'Slovakia', 
    'southafrica': 'South Africa', 
    'southkorea': 'South Korea', 
    'southtyrol': 'South Tyrol', 
    'spain': 'Spain', 
    'sweden': 'Sweden', 
    'switzerland': 'Switzerland', 
    'syria': 'Syria', 
    'taiwan': 'Taiwan', 
    'thailand': 'Thailand', 
    'tunisia': 'Tunisia', 
    'turkey': 'Turkey', 
    'uganda': 'Uganda', 
    'ukraine': 'Ukraine', 
    'unitedkingdom': 'United Kingdom', 
    'unitedstates': 'United States', 
    'uruguay': 'Uruguay', 
    'venezuela': 'Venezuela', 
}

def imageHasBeenTweetedBefore(image=''):
    images = []
    with open('wlm.tweeted.images.txt', 'r') as f:
        images = f.read().strip().splitlines()
    if image in images:
        return True
    return False

def tweetImage(image='', props={}, twitter=''):
    imagename = image
    tempfilename = 'wlm-tempimage.jpg'
    x, xx = getCommonsMD5(imagename)
    imgurl = 'https://commons.wikimedia.org/wiki/File:' + re.sub(' ', '_', imagename)
    imgurl_ = 'https://commons.wikimedia.org/wiki/File:' + urllib.parse.quote(re.sub(' ', '_', imagename))
    imagenamequoted = urllib.parse.quote(re.sub(' ', '_', imagename))
    try:
        imgurl2 = 'https://upload.wikimedia.org/wikipedia/commons/thumb/%s/%s/%s/1200px-%s' % (x, xx, imagenamequoted, imagenamequoted)
        print(imgurl2)
        urllib.request.urlretrieve(imgurl2, tempfilename)
    except:
        print('Error bajando')
        try:
            imgurl2 = 'https://upload.wikimedia.org/wikipedia/commons/%s/%s/%s' % (x, xx, imagenamequoted)
            print(imgurl2)
            urllib.request.urlretrieve(imgurl2, tempfilename)
        except:
            print('Error bajando')
            return
    
    img = open(tempfilename, 'rb')
    response = twitter.upload_media(media=img)
    
    title = re.sub('_', ' ', '.'.join(image.split('.')[:-1]))
    title = len(title) > 60 and ('%s...' % title[:70]) or title
    hashtagcountry = '#' + re.sub(' ', '', countrynames[props['country']])
    status = '#WikiLovesMonuments #WLM2017\n\n%s %s\n\n%s' % (hashtagcountry, title, imgurl_)
    print(status)
    raw = twitter.update_status(status=status, media_ids=[response['media_id']])
    tweetid = raw['id_str']
    print('Status:',status)
    print('Returned ID:',tweetid)
    with open('wlm.tweeted.images.txt', 'a') as f:
        f.write('\n'+image)

def main():
    APP_KEY, APP_SECRET = read_keys()
    OAUTH_TOKEN, OAUTH_TOKEN_SECRET = read_tokens()
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    
    if len(sys.argv) > 1:
        param = sys.argv[1]
    else:
        print("Error, no indicaste parametro")
        sys.exit()
    
    jsonfilename = 'files-2017.json'
    jsonurl = 'https://tools.wmflabs.org/wlm-stats/' + jsonfilename
    urllib.request.urlretrieve(jsonurl, jsonfilename)
    json1 = {}
    with open(jsonfilename, 'r') as f:
        json1 = json.loads(f.read())
        
    if param == 'recent':
        images = []
        countries = []
        for image, props in json1.items():
            if not props['country'] in countries:
                if not imageHasBeenTweetedBefore(image=image):
                    images.append(image)
                    countries.append(props['country'])
        for image in images:
            tweetImage(image=image, props=json1[image], twitter=twitter)
            time.sleep(60)

if __name__ == '__main__':
    main()

