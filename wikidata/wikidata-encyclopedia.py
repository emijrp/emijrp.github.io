#!/usr/bin/env python3
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

import fileinput
import json
import re
import sys
import time
import unicodedata
try:
    from hashlib import md5
except ImportError:             # Python 2.4 compatibility
    from md5 import new as md5

def convertdate(d):
    date = ''
    if d:
        if d[0] == '+':
            d = d[1:]
            date = d[0:4]
        else:
            date = d[0:4]
            date = '%s AC' % (date)
    return date

def convertsitelink(site, title, badges):
    link = ''
    title_ = re.sub(' ', '_', title)
    lang = ''
    for x, y in [['wiki', 'wikipedia'], ['wikiquote', 'wikiquote'], ['wikisource', 'wikisource']]:
        if site.endswith(x):
            lang = re.sub('_', '-', site.split(x)[0])
            link = 'https://%s.%s.org/wiki/%s' % (lang, y, title_)
    link = '<a href="%s">%s</a>%s' % (link, lang, sitelinkbadges(badges))
    return link

def removeaccute(s):
    return ''.join((c for c in unicodedata.normalize('NFD', s) if unicodedata.category(c) != 'Mn'))

def sitelinkbadges(badges):
    if 'Q17437796' in badges:
        return ' (destacado)'
    return ''

def sitelinkshtml(sitelinks):
    sitelinks_ = {'wiki': [], 'wikiquote': [], 'wikisource': [], }
    for s in ['wiki', 'wikiquote', 'wikisource']:
        for site, slprops in sitelinks.items():
            if site.endswith(s):
                sitelinks_[s].append([slprops['site'], slprops['title'], slprops['badges']])
                sitelinks_[s].sort()
    
    html = '<ul>'
    for x, y in [['wiki', 'Wikipedia'], ['wikiquote', 'Wikiquote'], ['wikisource', 'Wikisource']]:
        html += '<li><b>%s:</b> %s</li>' % (y, '&nbsp;<b>&middot;</b>&#32;'.join([convertsitelink(site, title, badges) for site, title, badges in sitelinks_[x]]))
    html += '</ul>'
    return html

def main():
    preferedlangs = ['es', 'en', 'ca', 'gl', 'pt', 'it', 'fr', 'de', 'eu', 'cz', 'hu', 'nl', 'sv', 'no', 'fi', 'ro', 'eo', 'da','sk', 'tr']
    c = 0
    t1 = time.time()
    items = {}
    for line in fileinput.input():
        line = line.strip().rstrip(',')
        if not line.startswith('{'):
            continue
        js = json.loads(line)
        if js['type'] != 'item':
            continue
        
        q = js['id']
        P31 = ''
        sex = ''
        country = ''
        birthdate = '' #P569
        birthdateprec = ''
        deathdate = '' #P570
        deathdateprec = ''
        occupations = []
        images = [] #P18
        label = ''
        viaf = '' #P214
        
        if not q:
            continue
        
        #labels
        if 'labels' in js:
            for preflang in preferedlangs:
                if preflang in js['labels']:
                    label = js['labels'][preflang]['value']
                    break
        if not label:
            continue
        #claims
        if 'claims' in js and 'P31' in js['claims']:
            P31 = 'Q%s' % js['claims']['P31'][0]['mainsnak']['datavalue']['value']['numeric-id']
            if P31 != 'Q5':
                continue
        else:
            continue
        if 'claims' in js and 'P21' in js['claims'] and 'datavalue' in js['claims']['P21'][0]['mainsnak']:
            sex = 'Q%s' % js['claims']['P21'][0]['mainsnak']['datavalue']['value']['numeric-id']
        if 'claims' in js and 'P27' in js['claims'] and 'datavalue' in js['claims']['P27'][0]['mainsnak']:
            country = 'Q%s' % js['claims']['P27'][0]['mainsnak']['datavalue']['value']['numeric-id']
        if 'claims' in js and 'P569' in js['claims'] and 'datavalue' in js['claims']['P569'][0]['mainsnak']:
            birthdate = js['claims']['P569'][0]['mainsnak']['datavalue']['value']['time'].split('T')[0]
            birthdateprec = js['claims']['P569'][0]['mainsnak']['datavalue']['value']['precision']
        if 'claims' in js and 'P570' in js['claims'] and 'datavalue' in js['claims']['P570'][0]['mainsnak']:
            deathdate = js['claims']['P570'][0]['mainsnak']['datavalue']['value']['time'].split('T')[0]
            deathdateprec = js['claims']['P570'][0]['mainsnak']['datavalue']['value']['precision']
        if 'claims' in js and 'P106' in js['claims']:
            for claim in js['claims']['P106']:
                if 'datavalue' in claim['mainsnak']:
                    occupations.append('Q%s' % claim['mainsnak']['datavalue']['value']['numeric-id'])
        if 'claims' in js and 'P18' in js['claims']:
            for claim in js['claims']['P18']:
                if 'datavalue' in claim['mainsnak']:
                    images.append(claim['mainsnak']['datavalue']['value'])
        #identifiers
        if 'claims' in js and 'P214' in js['claims'] and 'datavalue' in js['claims']['P214'][0]['mainsnak']:
            viaf = js['claims']['P214'][0]['mainsnak']['datavalue']['value']
        
        items[q] = {'q': q, 'label': label, 'sex': sex, 'country': country, 'birthdate': birthdate, 'deathdate': deathdate, 'occupations': occupations, 'images': images, 'viaf': viaf, 'sitelinks': js['sitelinks']}
        
        #print(json.dumps(js['claims']['P18'], indent=4, sort_keys=True))
        
        if not images:
            continue
        
        #output
        htmltitle = '%s - Enciclopedia WD' % (label)
        htmlimgsize= '250px'
        htlmimgname = re.sub(' ', '_', images[0])
        md5sum = md5(htlmimgname.encode('utf-8')).hexdigest()
        htmlimgurl = 'https://upload.wikimedia.org/wikipedia/commons/thumb/%s/%s/%s/%s-%s' % (md5sum[0], md5sum[0:2], htlmimgname, htmlimgsize, htlmimgname)
        htmlimg = '<img src="%s" align="center" width="%s" title="%s" />' % (htmlimgurl, htmlimgsize, htmltitle)
        birthdate_ = convertdate(birthdate)
        deathdate_ = convertdate(deathdate)
        intro = ''
        if items[q]['deathdate']:
            intro += 'Fue %s ' % (items[q]['sex'] == 'Q6581072' and 'una' or 'un')
        else:
            intro += 'Es %s ' % (items[q]['sex'] == 'Q6581072' and 'una' or 'un')
        if occupations:
            intro += ', '.join(occupations)
        sitelinks_ = sitelinkshtml(items[q]['sitelinks'])
        htmlbody = """
<h1>%s</h1>
<table class="wikitable" align="right" style="font-size: 90%%;">
<tr><td colspan="2" style="text-align: center;">%s</td></tr>
<tr><td colspan="2" style="text-align: center;">%s</td></tr>
<tr><td><b>Nacimiento</td><td>...</td></tr>
<tr><td><b>Fallecimiento</td><td>...</td></tr>
<tr><td><b>Padre</td><td>...</td></tr>
<tr><td><b>Madre</td><td>...</td></tr>
<tr><td><b>Hermano(s)</td><td>...</td></tr>
<tr><td><b>Hermana(s)</td><td>...</td></tr>
<tr><td><b>Cónyuge(s)</td><td>...</td></tr>
<tr><td><b>Hijo(s)</td><td>...</td></tr>
<tr><td><b>Ocupación</td><td>...</td></tr>
</table>
<p><b>%s</b> (%s - %s). %s.</p>

<p>Fue miembro de ...</p>

<p>Recibió el galardón ...</p>

<p>Trabajó en ...</p>

<p>Fue enterrado en ...</p>

<table class="wikitable">
<tr><td><b><i>Enlaces a sitios Wikimedia</i></b><br/>%s</td></tr>
</table>

<ul>
    <li>Wikidata: <a href="https://www.wikidata.org/wiki/%s">%s</a></li>
    <li>VIAF: <a href="https://viaf.org/viaf/%s">%s</a></li>
</ul>""" % (htmltitle, label, htmlimg, label, birthdate_, deathdate_, intro, sitelinks_, q, q, viaf, viaf)
        output = """<!DOCTYPE html>
<html lang="es" dir="ltr">
<head>
    <meta charset="UTF-8"/>
    <title>%s</title>
    <meta property="og:title" content="%s" />
    <meta property="og:description" content=""/>
    <meta property="og:image" content=""/>
    <link rel="stylesheet" href="../style.css" />
    <link rel="stylesheet" href="mediawiki-shared.css" />
</head>
<body>
%s
</body>
</html>""" % (htmltitle, htmltitle, htmlbody)
        
        #save
        labelplain = re.sub(' ', '-', removeaccute(label))
        filename = '%s-%s.html' % (labelplain.lower(), q.lower())
        with open(filename, 'w') as f:
            f.write(output)
        
        #stats
        c += 1
        if c % 1000 == 0:
            print(len(items.keys()), q, label, sex, country, birthdate, birthdateprec, deathdate, deathdateprec, occupations, images, viaf)
            print('%d items/sec' % (c/(time.time()-t1)))
            c = 0
            t1 = time.time()
            sys.exit()
        
if __name__ == '__main__':
    main()
