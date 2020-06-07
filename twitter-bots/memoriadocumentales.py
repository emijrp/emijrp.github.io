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
    
    commonsurl = 'https://15mpedia.org/wiki/Usuario:Emijrp/Documentales-memoria?action=raw'
    raw = getURL(url=commonsurl)
    works = re.findall(r'(?im)^\*([^\|\n]+?)\|(http[^\n]+?)\n', raw)
    random.shuffle(works)
    selectedwork = works[0]
    print(selectedwork)
    
    name = selectedwork[0].strip()
    desc = selectedwork[1].strip()
    status = '#MemoriaAntifascista #Documentales\n\n%s\n\n%s' % (name, desc)
    print(status)
    raw = twitter.update_status(status=status)
    tweetid = raw['id_str']
    print('Status:',status)
    print('Returned ID:',tweetid)

if __name__ == '__main__':
    main()
