#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2016 emijrp <emijrp@gmail.com>
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
from twython import Twython
from twitterbots import *

def main():
    APP_KEY, APP_SECRET = read_keys()
    OAUTH_TOKEN, OAUTH_TOKEN_SECRET = read_tokens()
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    
    films = []
    for page in range(1, 10):
        time.sleep(1)
        faurl = 'https://www.filmaffinity.com/es/userlist.php?user_id=397713&list_id=1031&page=%d' % (page)
        print('Retrieving', faurl)
        html = ''
        try:
            html = getURL(url=faurl)
        except:
            pass
        if not html:
            break
        #<div class="mc-title"><a  href="/es/film499059.html" title="El capital">El capital</a> (2012) <img src="/imgs/countries/FR.jpg" alt="Francia" title="Francia"></div>
        m = re.finditer(r'(?im)<div class="mc-title">\s*<a\s*href="/es/film(?P<id>\d+)\.html"[^<>]*?>(?P<title>[^<>]*?)</a>\s*\((?P<year>\d+?)\)\s*<img src="/imgs/countries/(?P<countryid>[^<>]+)\.jpg" [^<>]*?title="(?P<country>[^<>]+?)">\s*</div>', html)
        c = 0 #for ratings index
        for i in m:
            filmprops = {}
            filmprops['id'] = i.group('id').strip()
            filmprops['title'] = i.group('title').strip()
            filmprops['year'] = i.group('year').strip()
            filmprops['country'] = i.group('country').strip().split(' (')[0]
            films.append([filmprops['title'], filmprops])
        
    random.shuffle(films)
    selectedfilm = films[0][1]
    print(selectedfilm)
    
    country_ = selectedfilm['country'].replace(' ', '')
    status = '#CinePolítico\n\n%s\n(%s, #%s)\n\nhttp://www.filmaffinity.com/es/film%s.html' % (selectedfilm['title'], selectedfilm['year'], country_, selectedfilm['id'])
    print(status)
    raw = twitter.update_status(status=status)
    tweetid = raw['id_str']
    print('Status:',status)
    print('Returned ID:',tweetid)

if __name__ == '__main__':
    main()
