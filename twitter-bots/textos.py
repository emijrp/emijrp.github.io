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

import datetime
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
        'constesp1931': {
            'title': 'Constitución española de 1931', 
            'author': 'Segúnda República', 
            'pages': [1, 31], 
            'pageoffset': 0,
            'pageshow': True,
            'hashtags': ['#TextosPolíticos', '#IIRepública'], 
            'filename': 'constesp1931.pdf',
            'order': 'dayofmonth',
        }, 
        'dicfidel': {
            'title': 'Diccionario de Pensamientos de Fidel Castro', 
            'author': 'Salomón Susi', 
            'pages': [10, 336], 
            'pageoffset': -7,
            'pageshow': True,
            'hashtags': ['#TextosPolíticos', '#Cuba'], 
            'filename': 'dicfidel.pdf',
            'order': 'random',
        }, 
        'dicros': {
            'title': 'Diccionario Filosófico Marxista', 
            'author': 'M. Rosental', 
            'pages': [9, 318], 
            'pageoffset': 0,
            'pageshow': True,
            'hashtags': ['#TextosPolíticos'], 
            'filename': 'dicros.pdf',
            'order': 'random',
        }, 
        'laotraalemania': {
            'title': 'La otra Alemania, la RDA', 
            'author': 'Luis Corvalán & Margot Honecker', 
            'pages': [13, 113], 
            'pageoffset': 0,
            'pageshow': False,
            'hashtags': ['#RDA', '#TextosPolíticos'], 
            'filename': 'laotraalemania.pdf',
            'order': 'random',
        }, 
        'librorojo': {
            'title': 'Citas del Presidente Mao', 
            'author': 'Mao Tse-Tung', 
            'pages': [3, 113], 
            'pageoffset': 0,
            'pageshow': True,
            'hashtags': ['#LibroRojo', '#TextosPolíticos'], 
            'filename': 'librorojo.pdf',
            'order': 'random',
        }, 
        'mancom': {
            'title': 'Manifiesto del Partido Comunista', 
            'author': 'Karl Marx & Friedrich Engels', 
            'pages': [17, 44], 
            'pageoffset': 0,
            'pageshow': True,
            'hashtags': ['#ManifiestoComunista', '#TextosPolíticos'], 
            'filename': 'mancom.pdf',
            'order': 'random',
        }, 
        'tengounsueno': {
            'title': 'Tengo un sueño', 
            'author': 'Martin Luther King', 
            'pages': [2, 4], 
            'pageoffset': -1,
            'pageshow': True,
            'hashtags': ['#TextosPolíticos'], 
            'filename': 'tengounsueno.pdf',
            'url': 'https://web.archive.org/web/20150421021808/https://www.msssi.gob.es/ssi/igualdadOportunidades/noDiscriminacion/documentos/Martin_Luther_King_Tengo_un_sueno.pdf',
            'order': 'random',
        }, 
    }
    
    texto = ''
    if len(sys.argv) > 1:
        texto = sys.argv[1]
        if not texto in textos.keys():
            print('Texto %s no encontrado' % (texto))
            sys.exit()
    else:
        print('No has indicado un texto. Se publicara uno aleatorio')
    
    if texto:
        if not textos[texto]['filename'] or \
           not os.path.exists(textos[texto]['filename']):
            print('Error, el fichero %s no existe' % (textos[texto]['filename']))
            sys.exit()
        
        pagenum = ''
        if textos[texto]['order'] == 'dayofmonth':
            pagenum = datetime.datetime.today().day + (textos[texto]['pages'][0] - 1)
        elif textos[texto]['order'] == 'random':
            pagenum = random.randint(textos[texto]['pages'][0], textos[texto]['pages'][1])
        else:
            pagenum = random.randint(textos[texto]['pages'][0], textos[texto]['pages'][1])
        if not pagenum:
            print('ERROR, no pagenum')
            sys.exit()
        
        os.system('pdftoppm -f %d -singlefile -png %s %s' % (pagenum, textos[texto]['filename'], texto))
        img = open('%s.png' % (texto), 'rb')
        response = twitter.upload_media(media=img)
        if textos[texto]['pageshow']:
            status = '%s\n\n%s\n(%s, página %s)' % (' '.join(textos[texto]['hashtags']), textos[texto]['title'], textos[texto]['author'], (pagenum+textos[texto]['pageoffset']))
        else:
            status = '%s\n\n%s\n(%s)' % (' '.join(textos[texto]['hashtags']), textos[texto]['title'], textos[texto]['author'])
        print(status)
        raw = twitter.update_status(status=status, media_ids=[response['media_id']])
        tweetid = raw['id_str']
        print('Status:',status)
        print('Returned ID:',tweetid)
    else:
        status = '%s\n\n%s\n(%s)\n\n%s' % (' '.join(textos[texto]['hashtags']), textos[texto]['title'], textos[texto]['author'], textos[texto]['url'])
        pass

if __name__ == '__main__':
    main()

