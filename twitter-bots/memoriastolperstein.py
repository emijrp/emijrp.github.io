#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2020 emijrp <emijrp@gmail.com>
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
import urllib
import urllib.request
from twython import Twython
from twitterbots import *

def main():
    APP_KEY, APP_SECRET = read_keys()
    OAUTH_TOKEN, OAUTH_TOKEN_SECRET = read_tokens()
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    
    commonsurl = 'https://15mpedia.org/wiki/Usuario:Emijrp/Stolperstein?action=raw'
    raw = getURL(url=commonsurl)
    works = re.findall(r'(?im)File:([^\|\n]+?)\|([^\n]+?)\n', raw)
    random.shuffle(works)
    selectedwork = works[0]
    print(selectedwork)
    
    imagename = selectedwork[0]
    desc = selectedwork[1]
    x, xx = getCommonsMD5(imagename)
    imgurl = 'https://commons.wikimedia.org/wiki/File:%s' % (re.sub(' ', '_', imagename))
    imgurl2 = 'https://upload.wikimedia.org/wikipedia/commons/%s/%s/%s' % (x, xx, urllib.parse.quote(re.sub(' ', '_', imagename)))
    urllib.request.urlretrieve(imgurl2, 'memoriastolperstein-tempimage.jpg')
    img = open('memoriastolperstein-tempimage.jpg', 'rb')
    
    republicanflag = '🟥🟥🟥🟨🟨🟨🟪🟪🟪'
    status = '%s\n#MemoriaAntifascista #Monumentos\n\n#Stolperstein en recuerdo de...\n%s\n¡Que su nombre no se borre de la historia!\n\n%s' % (republicanflag, desc, imgurl)
    print(status)
    response = twitter.upload_media(media=img)
    raw = twitter.update_status(status=status, media_ids=[response['media_id']])
    tweetid = raw['id_str']
    print('Status:',status)
    print('Returned ID:',tweetid)

if __name__ == '__main__':
    main()
