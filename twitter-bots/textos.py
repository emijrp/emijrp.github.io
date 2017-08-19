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
    
    textos = {
        'dicfidel': {
            'title': 'Diccionario de Pensamientos de Fidel Castro', 
            'author': 'Salomón Susi', 
            'pages': [10, 336], 
            'pageoffset': -7,
            'pageshow': True,
            'hashtags': ['#TextosPolíticos', '#Cuba'], 
            'filename': 'dicfidel.pdf',
        }, 
        'dicros': {
            'title': 'Diccionario Filosófico Marxista', 
            'author': 'M. Rosental', 
            'pages': [9, 318], 
            'pageoffset': 0,
            'pageshow': True,
            'hashtags': ['#TextosPolíticos'], 
            'filename': 'dicros.pdf',
        }, 
        'laotraalemania': {
            'title': 'La otra Alemania, la RDA', 
            'author': 'Luis Corvalán & Margot Honecker', 
            'pages': [13, 113], 
            'pageoffset': 0,
            'pageshow': False,
            'hashtags': ['#RDA', '#TextosPolíticos'], 
            'filename': 'laotraalemania.pdf',
        }, 
        'librorojo': {
            'title': 'Citas del Presidente Mao', 
            'author': 'Mao Tse-Tung', 
            'pages': [3, 113], 
            'pageoffset': 0,
            'pageshow': True,
            'hashtags': ['#LibroRojo', '#TextosPolíticos'], 
            'filename': 'librorojo.pdf',
        }, 
        'mancom': {
            'title': 'Manifiesto del Partido Comunista', 
            'author': 'Karl Marx & Friedrich Engels', 
            'pages': [17, 44], 
            'pageoffset': 0,
            'pageshow': True,
            'hashtags': ['#ManifiestoComunista', '#TextosPolíticos'], 
            'filename': 'mancom.pdf',
        }, 
    }
    if len(sys.argv) > 1:
        texto = sys.argv[1]
        if not texto in textos.keys():
            print('Texto %s no encontrado' % (texto))
            sys.exit()
    else:
        print('No has indicado un texto')
        sys.exit()
    
    randompagenum = random.randint(textos[texto]['pages'][0], textos[texto]['pages'][1])
    os.system('pdftoppm -f %d -singlefile -png %s %s' % (randompagenum, textos[texto]['filename'], texto))
    img = open('%s.png' % (texto), 'rb')
    response = twitter.upload_media(media=img)
    if textos[texto]['pageshow']:
        status = '%s (%s, página %s) %s' % (textos[texto]['title'], textos[texto]['author'], (randompagenum+textos[texto]['pageoffset']), ' '.join(textos[texto]['hashtags']))
    else:
        status = '%s (%s) %s' % (textos[texto]['title'], textos[texto]['author'], ' '.join(textos[texto]['hashtags']))
    print(status)
    raw = twitter.update_status(status=status, media_ids=[response['media_id']])
    tweetid = raw['id_str']
    print('Status:',status)
    print('Returned ID:',tweetid)

if __name__ == '__main__':
    main()

