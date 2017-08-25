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

import datetime
from PIL import Image #pip install pillow
from PIL import ImageDraw
from PIL import ImageFont
import os
import re
import sys
import urllib
import urllib.request
from twython import Twython
from twitterbots import *

#config
imagename = 'memoria.png'

def main():
    APP_KEY, APP_SECRET = read_keys()
    OAUTH_TOKEN, OAUTH_TOKEN_SECRET = read_tokens()
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    
    month2name = {'01': 'enero', '02': 'febrero', '03': 'marzo', '04': 'abril', '05': 'mayo', '06': 'junio', 
                  '07': 'julio', '08': 'agosto', '09': 'septiembre', '10': 'octubre', '11': 'noviembre', '12': 'diciembre' }
    
    d = datetime.datetime.now()
    today = '%s de %s' % (int(d.strftime('%d')), month2name[d.strftime('%m')])
    today_ = re.sub(' ', '_', today)
    
    temas = {
        'deportados': {
            'title': 'Campos de concentración nazis',
            'intro': 'Deportados asesinados',
            'outro': 'Que sus nombres no caigan en el olvido.',
            'source': 'Libro Memorial',
            'graph': '15Mpedia',
            'background': (248, 224, 236),
        },
        'fusilados': {
            'title': 'Represión franquista',
            'intro': 'Personas fusiladas',
            'outro': 'Que sus nombres no caigan en el olvido.',
            'source': 'Memoria y Libertad',
            'graph': '15Mpedia',
            'background': (255, 255, 200),
        },
    }
    if len(sys.argv) > 1:
        tema = sys.argv[1]
        if not tema in temas.keys():
            print('Tema %s no encontrado' % (tema))
            sys.exit()
    else:
        print('No has indicado un tema')
        sys.exit()
    
    victimas = []
    if tema == 'deportados':
        query = "[[persona represaliada::+]] [[represor::Nazismo]] [[represión::Campo de concentración]] [[fallecimiento::Sí]] [[fecha string::~*/%s/%s]]" % (d.strftime('%m'), d.strftime('%d'))
        queryurl = 'https://15mpedia.org/w/index.php?title=Especial:Ask&q=%s&p=format%%3Dbroadtable%%2Flink%%3Dall%%2Fheaders%%3Dshow%%2Fsearchlabel%%3D-26hellip%%3B-20siguientes-20resultados%%2Fclass%%3Dsortable-20wikitable-20smwtable&po=%%3FFecha+string%%0A%%3FLugar%%0A&limit=500&eq=no' % (urllib.parse.quote(query))
        raw = urllib.request.urlopen(queryurl).read().decode('utf-8')
        m = re.findall(r'(?im)<td><a href="[^<>]*?" title="[^<>]*?">([^<>]*?)</a></td>\s*<td class="Fecha-string">(\d\d\d\d)[^<>]+?</td>\s*<td class="Lugar">Campo de concentración de ([^<>]*?)</td>', raw)
        victimas = []
        for i in m:
            if not '(' in i[0]:
                victimas.append([i[1],i[0],i[2]])
    elif tema == 'fusilados':
        raw = urllib.request.urlopen('https://15mpedia.org/w/index.php?title=Especial:Ask&q=[[persona+represaliada%%3A%%3A%%2B]]+[[represor%%3A%%3AFranquismo]]+[[represi%%C3%%B3n%%3A%%3AFusilamiento]]+[[fecha+string%%3A%%3A~*%%2F%s%%2F%s]]&p=format%%3Dbroadtable%%2Flink%%3Dall%%2Fheaders%%3Dshow%%2Fsearchlabel%%3D-26hellip%%3B-20siguientes-20resultados%%2Fclass%%3Dsortable-20wikitable-20smwtable&po=%%3FFecha+string%%0A&limit=500&eq=no' % (d.strftime('%m'), d.strftime('%d'))).read().decode('utf-8')
        m = re.findall(r'(?im)<td><a href="[^<>]*?" title="[^<>]*?">([^<>]*?)</a></td>\s*<td class="Fecha-string">(\d\d\d\d)[^<>]+?</td>', raw)
        victimas = []
        for i in m:
            if not '(' in i[0]:
                victimas.append([i[1],i[0],''])
    
    victimas.sort()
    if not victimas:
        sys.exit()
    
    #generar imagen
    victimasnum = len(victimas)
    high = 25
    img = Image.new('RGB', (500, victimasnum*high+220), temas[tema]['background'])
    fonttitle = ImageFont.truetype("OpenSans-Regular.ttf", 25)
    fonttext = ImageFont.truetype("OpenSans-Regular.ttf", 18)
    fontfooter = ImageFont.truetype("OpenSans-Regular.ttf", 15)
    d = ImageDraw.Draw(img)
    d.text((20, high), temas[tema]['title'], fill=(255, 0, 0), font=fonttitle)
    d.text((20, high*3), '%s un %s:' % (temas[tema]['intro'], today), fill=(0, 0, 0), font=fonttext)
    c = 0
    for year, name, place in victimas:
        if place:
            d.text((30, high*c+110), '%d) %s (%s, %s)' % (c+1, name, year, place), fill=(0, 0, 0), font=fonttext)
        else:
            d.text((30, high*c+110), '%d) %s (%s)' % (c+1, name, year), fill=(0, 0, 0), font=fonttext)
        c += 1
    d.text((20, high*c+90+high), temas[tema]['outro'], fill=(0, 0, 255), font=fonttext)
    d.text((260, high*c+130+high), 'Fuente: %s' % (temas[tema]['source']), fill=(0, 0, 0), font=fontfooter)
    d.text((260, high*c+150+high), 'Elaboración gráfica: %s' % (temas[tema]['graph']), fill=(0, 0, 0), font=fontfooter)
    img.save(imagename)
    
    #tuitear imagen
    img = open(imagename, 'rb')
    if tema == 'fusilados':
        status = '#MemoriaAntifascista Un %s el franquismo los fusiló https://15mpedia.org/wiki/%s Que sus nombres no caigan en el olvido' % (today, today_)
    elif tema == 'deportados':
        status = '#MemoriaAntifascista Un %s el nazismo los asesinó https://15mpedia.org/wiki/%s Que sus nombres no caigan en el olvido' % (today, today_)
    print(status)
    response = twitter.upload_media(media=img)
    raw = twitter.update_status(status=status, media_ids=[response['media_id']])
    tweetid = raw['id_str']
    print('Status:',status)
    print('Returned ID:',tweetid)

if __name__ == '__main__':
    main()
