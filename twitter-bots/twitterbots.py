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

try:
    from hashlib import md5
except ImportError:             # Python 2.4 compatibility
    from md5 import new as md5
import os
import re
import time
import urllib
import urllib.request
import unicodedata

def removeaccute(s):
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))
    
def read_keys():
    f = open('%s/.twitter_keys' % (os.path.dirname(os.path.realpath(__file__))), 'r')
    w = f.read()
    APP_KEY = re.findall(r'(?im)^AP[IP]_KEY\s*=\s*([^\n]+?)\s*$', w)[0].strip()
    APP_SECRET = re.findall(r'(?im)^AP[IP]_SECRET\s*=\s*([^\n]+?)\s*$', w)[0].strip()
    return APP_KEY, APP_SECRET

def read_tokens():
    f = open('%s/.twitter_tokens' % (os.path.dirname(os.path.realpath(__file__))), 'r')
    w = f.read()
    OAUTH_TOKEN = re.findall(r'(?im)^OAUTH_TOKEN\s*=\s*([^\n]+?)\s*$', w)[0].strip()
    OAUTH_TOKEN_SECRET = re.findall(r'(?im)^OAUTH_TOKEN_SECRET\s*=\s*([^\n]+?)\s*$', w)[0].strip()
    return OAUTH_TOKEN, OAUTH_TOKEN_SECRET

def getURL(url=''):
    raw = ''
    req = urllib.request.Request(url, headers={ 'User-Agent': 'Mozilla/5.0' })
    try:
        raw = urllib.request.urlopen(req).read()
        try:
            raw = raw.strip().decode('utf-8')
        except:
            try:
                raw = raw.strip().decode('latin-1')
            except:
                pass
    except:
        sleep = 10 # seconds
        maxsleep = 100
        while sleep <= maxsleep:
            print('Error while retrieving: %s' % (url))
            print('Retry in %s seconds...' % (sleep))
            time.sleep(sleep)
            raw = urllib.request.urlopen(req).read()
            try:
                raw = raw.strip().decode('utf-8')
            except:
                try:
                    raw = raw.strip().decode('latin-1')
                except:
                    pass
            sleep = sleep * 2
    return raw

def getCommonsMD5(filename=''):
    filename = re.sub(' ', '_', filename)
    md5sum = md5(filename.encode('utf-8')).hexdigest()
    return md5sum[0], md5sum[0:2]
