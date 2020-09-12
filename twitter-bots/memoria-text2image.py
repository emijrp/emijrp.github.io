#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (C) 2016-2020 emijrp <emijrp@gmail.com>
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
import time
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

def removeaccuteandcase(s=''):
    return removeaccute(s.lower())

def main():
    APP_KEY, APP_SECRET = read_keys()
    OAUTH_TOKEN, OAUTH_TOKEN_SECRET = read_tokens()
    twitter = Twython(APP_KEY, APP_SECRET, OAUTH_TOKEN, OAUTH_TOKEN_SECRET)
    
    month2name = {
        'ca': { '01': 'gener', '02': 'febrer', '03': 'març', '04': 'abril', '05': 'maig', '06': 'juny', 
                '07': 'juliol', '08': 'agost', '09': 'setembre', '10': 'octubre', '11': 'novembre', '12': 'desembre' }, 
        'en': { '01': 'January', '02': 'February', '03': 'March', '04': 'April', '05': 'May', '06': 'June', 
                '07': 'July', '08': 'August', '09': 'September', '10': 'October', '11': 'November', '12': 'December' }, 
        'es': { '01': 'enero', '02': 'febrero', '03': 'marzo', '04': 'abril', '05': 'mayo', '06': 'junio', 
                '07': 'julio', '08': 'agosto', '09': 'septiembre', '10': 'octubre', '11': 'noviembre', '12': 'diciembre' }, 
        'gl': { '01': 'xaneiro', '02': 'febreiro', '03': 'marzo', '04': 'abril', '05': 'maio', '06': 'xuño', 
                '07': 'xullo', '08': 'agosto', '09': 'setembro', '10': 'outubro', '11': 'novembro', '12': 'decembro' }, 
    }
    d = datetime.datetime.now()
    today = {
        'ca': '%s de %s' % (int(d.strftime('%d')), month2name['ca'][d.strftime('%m')]),
        'en': '%s %s' % (month2name['en'][d.strftime('%m')], int(d.strftime('%d'))), 
        'es': '%s de %s' % (int(d.strftime('%d')), month2name['es'][d.strftime('%m')]), 
        'gl': '%s de %s' % (int(d.strftime('%d')), month2name['gl'][d.strftime('%m')]), 
    }
    today['ca'] = re.sub(r"de abril", r"d'abril", today['ca'])
    today['ca'] = re.sub(r"de agost", r"d'agost", today['ca'])
    today_ = re.sub(' ', '_', today['es'])
    todayprep = {
        'ca': 'un', 
        'en': 'on', 
        'es': 'un', 
    }
    
    todaytag = {
        'ca': '#%s%s' % (int(d.strftime('%d')), month2name['ca'][d.strftime('%m')]),
        'en': '#%s%s' % (int(d.strftime('%d')), month2name['en'][d.strftime('%m')]),
        'es': '#%s%s' % (int(d.strftime('%d')), month2name['es'][d.strftime('%m')]), 
        'gl': '#%s%s' % (int(d.strftime('%d')), month2name['gl'][d.strftime('%m')]), 
    }
    todaytag2 = {
        'ca': '#%sde%s' % (int(d.strftime('%d')), month2name['ca'][d.strftime('%m')]),
        'en': '#%s%s' % (month2name['en'][d.strftime('%m')], int(d.strftime('%d'))), 
        'es': '#%sde%s' % (int(d.strftime('%d')), month2name['es'][d.strftime('%m')]), 
        'gl': '#%sde%s' % (int(d.strftime('%d')), month2name['gl'][d.strftime('%m')]), 
    }
    
    temas = {
        'deportados': {
            'ca': {
                'title': 'Camps de concentració nazis',
                'intro': 'Deportats assassinats',
                'outro': "Que els seus noms no caiguin en l'oblit.",
                'source': 'Libro Memorial',
                'graph': '15Mpedia',
                'background': (248, 224, 236),
            }, 
            'en': {
                'title': 'Nazi concentration camps',
                'intro': 'People killed',
                'outro': 'Forever in our memories.',
                'source': 'Libro Memorial',
                'graph': '15Mpedia',
                'background': (248, 224, 236),
            }, 
            'es': {
                'title': 'Campos de concentración nazis',
                'intro': 'Deportados asesinados',
                'outro': 'Que sus nombres no caigan en el olvido.',
                'source': 'Libro Memorial',
                'graph': '15Mpedia',
                'background': (248, 224, 236),
            }, 
        },
        'fusilados': {
            'ca': {
                'title': 'Repressió franquista',
                'intro': 'Persones afusellades',
                'outro': "Que els seus noms no caiguin en l'oblit.",
                'source': 'Memoria y Libertad',
                'graph': '15Mpedia',
                'background': (255, 255, 200),
            }, 
            'en': {
                'title': 'Francoist repression',
                'intro': 'People killed',
                'outro': 'Forever in our memories.',
                'source': 'Memoria y Libertad',
                'graph': '15Mpedia',
                'background': (255, 255, 200),
            }, 
            'es': {
                'title': 'Represión franquista',
                'intro': 'Personas fusiladas',
                'outro': 'Que sus nombres no caigan en el olvido.',
                'source': 'Memoria y Libertad',
                'graph': '15Mpedia',
                'background': (255, 255, 200),
            }, 
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
    victimas_ = []
    if tema == 'deportados':
        query = "[[persona represaliada::+]] [[represor::Nazismo]] [[represión::Campo de concentración]] [[fallecimiento::Sí]] [[fecha string::~*/%s/%s]]" % (d.strftime('%m'), d.strftime('%d'))
        queryurl = 'https://15mpedia.org/w/index.php?title=Especial:Ask&q=%s&p=format%%3Dbroadtable%%2Flink%%3Dall%%2Fheaders%%3Dshow%%2Fsearchlabel%%3D-26hellip%%3B-20siguientes-20resultados%%2Fclass%%3Dsortable-20wikitable-20smwtable&po=%%3FFecha+string%%0A%%3FLugar%%0A&limit=500&eq=no' % (urllib.parse.quote(query))
        raw = urllib.request.urlopen(queryurl).read().decode('utf-8')
        m = re.findall(r'(?im)<td><a href="[^<>]*?" title="[^<>]*?">([^<>]*?)</a></td>\s*<td class="Fecha-string">(\d\d\d\d)[^<>]+?</td>\s*<td class="Lugar">Campo de concentración de ([^<>]*?)</td>', raw)
        victimas = []
        for i in m:
            if not '(' in i[0] and not removeaccuteandcase(i[0]) in victimas_:
                victimas.append([i[1],i[0],i[2]])
                victimas_.append(removeaccuteandcase(i[0]))
    elif tema == 'fusilados':
        raw = urllib.request.urlopen('https://15mpedia.org/w/index.php?title=Especial:Ask&q=[[persona+represaliada%%3A%%3A%%2B]]+[[represor%%3A%%3AFranquismo]]+[[represi%%C3%%B3n%%3A%%3AFusilamiento]]+[[fecha+string%%3A%%3A~*%%2F%s%%2F%s]]&p=format%%3Dbroadtable%%2Flink%%3Dall%%2Fheaders%%3Dshow%%2Fsearchlabel%%3D-26hellip%%3B-20siguientes-20resultados%%2Fclass%%3Dsortable-20wikitable-20smwtable&po=%%3FFecha+string%%0A&limit=500&eq=no' % (d.strftime('%m'), d.strftime('%d'))).read().decode('utf-8')
        m = re.findall(r'(?im)<td><a href="[^<>]*?" title="[^<>]*?">([^<>]*?)</a></td>\s*<td class="Fecha-string">(\d\d\d\d)[^<>]+?</td>', raw)
        victimas = []
        for i in m:
            if not '(' in i[0] and not removeaccuteandcase(i[0]) in victimas_:
                victimas.append([i[1],i[0],''])
                victimas_.append(removeaccuteandcase(i[0]))
    
    victimas.sort()
    if not victimas:
        sys.exit()
    
    langs = ['es', 'ca', ]
    for lang in langs:
        #generar imagen
        victimasnum = len(victimas)
        high = 25
        img = Image.new('RGB', (500, victimasnum*high+220), temas[tema][lang]['background'])
        fonttitle = ImageFont.truetype("OpenSans-Regular.ttf", 25)
        fonttext = ImageFont.truetype("OpenSans-Regular.ttf", 18)
        fontfooter = ImageFont.truetype("OpenSans-Regular.ttf", 15)
        d = ImageDraw.Draw(img)
        d.text((20, high), temas[tema][lang]['title'], fill=(255, 0, 0), font=fonttitle)
        d.text((20, high*3), '%s %s %s:' % (temas[tema][lang]['intro'], todayprep[lang], today[lang]), fill=(0, 0, 0), font=fonttext)
        c = 0
        for year, name, place in victimas:
            if place:
                d.text((30, high*c+110), '%d) %s (%s, %s)' % (c+1, name, year, place), fill=(0, 0, 0), font=fonttext)
            else:
                d.text((30, high*c+110), '%d) %s (%s)' % (c+1, name, year), fill=(0, 0, 0), font=fonttext)
            c += 1
        d.text((20, high*c+90+high), temas[tema][lang]['outro'], fill=(0, 0, 255), font=fonttext)
        d.text((260, high*c+130+high), 'Fuente: %s' % (temas[tema][lang]['source']), fill=(0, 0, 0), font=fontfooter)
        d.text((260, high*c+150+high), 'Elaboración gráfica: %s' % (temas[tema][lang]['graph']), fill=(0, 0, 0), font=fontfooter)
        img.save(imagename)
        
        #tuitear imagen
        img = open(imagename, 'rb')
        status = ''
        republicanflag = '🟥🟥🟥🟨🟨🟨🟪🟪🟪'
        if tema == 'fusilados':
            if lang == 'ca':
                status = "%s\n#MemoriaAntifeixista #Efemèrides\n\nUn %s el #franquisme els va afusellar https://15mpedia.org/wiki/%s\nQue els seus noms no caiguin en l'oblit!\n\nVíctimes del franquisme: https://15mpedia.org/wiki/Lista_de_personas_fusiladas_por_el_franquismo\n\n#CrimsDelFranquisme #CrimsDelFeixisme %s %s" % (republicanflag, today[lang], today_, todaytag[lang], todaytag2[lang])
            elif lang == 'en':
                pass #"#OnThisDay #OTD"
            elif lang == 'es':
                status = '%s\n#MemoriaAntifascista #Efemérides\n\nUn %s el #franquismo los fusiló https://15mpedia.org/wiki/%s\n¡Que sus nombres no caigan en el olvido!\n\nVíctimas del franquismo: https://15mpedia.org/wiki/Lista_de_personas_fusiladas_por_el_franquismo\n\n#CrímenesDelFranquismo #CrímenesDelFascismo %s %s' % (republicanflag, today[lang], today_, todaytag[lang], todaytag2[lang])
            elif lang == 'gl':
                pass
        elif tema == 'deportados':
            if lang == 'ca':
                status = "%s\n#MemòriaAntifeixista #Efemèrides\n\nUn %s el #nazisme els va assassinar https://15mpedia.org/wiki/%s\nQue els seus noms no caiguin en l'oblit!\n\nVíctimes del nazisme: https://15mpedia.org/wiki/Lista_de_v%%C3%%ADctimas_espa%%C3%%B1olas_del_nazismo\n\n#CrimsDelFeixisme %s %s" % (republicanflag, today[lang], today_, todaytag[lang], todaytag2[lang])
            elif lang == 'en':
                pass #"#OnThisDay #OTD"
            elif lang == 'es':
                status = '%s\n#MemoriaAntifascista #Efemérides\n\nUn %s el #nazismo los asesinó https://15mpedia.org/wiki/%s\n¡Que sus nombres no caigan en el olvido!\n\nVíctimas del nazismo: https://15mpedia.org/wiki/Lista_de_v%%C3%%ADctimas_espa%%C3%%B1olas_del_nazismo\n\n#CrímenesDelFascismo %s %s' % (republicanflag, today[lang], today_, todaytag[lang], todaytag2[lang])
            elif lang == 'gl':
                pass
        if status:
            print(status)
            response = twitter.upload_media(media=img)
            raw = twitter.update_status(status=status, media_ids=[response['media_id']])
            tweetid = raw['id_str']
            print('Status:',status)
            print('Returned ID:',tweetid)
            time.sleep(15)

if __name__ == '__main__':
    main()
