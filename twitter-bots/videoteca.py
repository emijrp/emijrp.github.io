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
    
    videoteca = {
        'escueladecuadros': {
            'hashtags': ['#VideotecaPolítica'], 
            'url': 'https://15mpedia.org/wiki/Usuario:Emijrp/Videoteca_escueladecuadros?action=raw',
        },
        'feminista': {
            'hashtags': ['#VideotecaFeminista', '#VideotecaPolítica', '#feminismo'], 
            'url': 'https://15mpedia.org/wiki/Usuario:Emijrp/Videoteca_feminista?action=raw',
        },
    }
    
    if len(sys.argv) > 1:
        tema = sys.argv[1]
        if not tema in videoteca.keys():
            print('Tema %s no encontrado' % (tema))
            sys.exit()
    else:
        print('No has indicado un tema')
        sys.exit()
    
    wikiurl = videoteca[tema]['url']
    raw = getURL(url=wikiurl)
    works = re.findall(r'(?im)([^\|\n]+?)\|([^\|\n]+?)\n', raw)
    random.shuffle(works)
    selectedwork = works[0]
    status = '%s https://www.youtube.com/watch?v=%s %s' % (selectedwork[1], selectedwork[0], ' '.join(videoteca[tema]['hashtags']))
    print(status)
    raw = twitter.update_status(status=status)
    tweetid = raw['id_str']
    print('Status:',status)
    print('Returned ID:',tweetid)

if __name__ == '__main__':
    main()
