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

import csv
import datetime
import json
import re
import sys
import time
import urllib
from xml.etree import ElementTree as ET # para ver los XMl que devuelve flickrapi con ET.dump(resp)

import flickrapi

def main():
    activity = {}
    originaldates = [] # to avoid count twice a photo, if it is both in commons and flickr
    
    #Commons
    cat = 'Category:Files_by_User:Emijrp'
    api = 'https://commons.wikimedia.org/w/api.php'
    apiquery = '%s?action=query&generator=categorymembers&gcmtitle=%s&format=json' % (api, cat)
    uccontinue = True
    uccontinue_name = 'gcmcontinue'
    c = 0
    rows = []
    while uccontinue:
        sys.stderr.write(".")
        if uccontinue == True:
            json_data = urllib.urlopen(apiquery)
        else:
            json_data = urllib.urlopen(apiquery+'&'+uccontinue_name+'='+uccontinue)
        data = json.load(json_data)
        for pageid in data['query']['pages']:
            pagens = data['query']['pages'][pageid]['ns']
            pagetitle = data['query']['pages'][pageid]['title']
            if pagens != 6:
                continue
            
            #print(pageid, pagens, pagetitle)
            pagetitle_ = pagetitle.replace(' ', '_')
            apiquery2 = '%s?action=query&titles=%s&prop=imageinfo&iiprop=metadata&format=json' % (api, urllib.quote(pagetitle_.encode('utf-8')))
            json_data2 = urllib.urlopen(apiquery2)
            data2 = json.load(json_data2)
            originaldate = ''
            model = ''
            if data2['query']['pages'][pageid]['imageinfo'][0]['metadata']:
                for metadict in data2['query']['pages'][pageid]['imageinfo'][0]['metadata']:
                    if metadict['name'].lower() == 'datetimeoriginal':
                        originaldate = metadict['value'].strip()
                        originaldate = originaldate.split(' ')[0].replace(':', '-') + ' ' + originaldate.split(' ')[1]
                        d1 = originaldate.split(' ')[0]
                        if d1 != '0000:00:00' and d1 != '0000-00-00' and \
                            originaldate not in originaldates:
                            d = datetime.datetime.strptime(d1, "%Y-%m-%d")
                            unixtime = d.strftime('%s')
                            if activity.has_key(unixtime):
                                activity[unixtime] += 1
                            else:
                                activity[unixtime] = 1
                            originaldates.append(originaldate)
                    if metadict['name'].lower() == 'model':
                        model = metadict['value'].strip()
            
            row = ['commons', pageid, pagetitle.encode('utf-8'), model, originaldate]
            rows.append(row)
            c += 1
        json_data.close()

        if data.has_key('continue'):
            uccontinue = data['continue'][uccontinue_name]
        else:
            uccontinue = ''
    print '\n', c, 'files in Commons'
    #save commons csv
    rows.sort()
    with open('photos-commons.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in rows:
            writer.writerow(row)
    
    #Flickr
    with open('flickr.token', 'r') as f:
        api_key, api_secret = f.read().strip().splitlines()
    
    flickr = flickrapi.FlickrAPI(api_key, api_secret)
    flickruserid = '96396586@N07' #it isn't secret, don't worry
    print('Step 1: authenticate')
    if not flickr.token_valid(perms=u'read'):
        flickr.get_request_token(oauth_callback=u'oob')
        authorize_url = flickr.auth_url(perms=u'read')
        print(authorize_url)
        verifier = unicode(raw_input(u'Verifier code: '), 'utf-8')
        flickr.get_access_token(verifier)
    print('Step 2: use Flickr')
    resp = flickr.photosets.getList(user_id=flickruserid)
    xmlraw = ET.tostring(resp, encoding='utf8', method='xml')
    photosets = re.findall(r' id="(\d+)"', xmlraw)
    flickrdone = []
    rows = []
    for photoset in photosets:
        print(photoset)
        resp2 = flickr.photosets.getPhotos(photoset_id=photoset, user_id=flickruserid, extras='date_taken')
        xmlraw2 = ET.tostring(resp2, encoding='utf8', method='xml')
        #print(xmlraw2)
        datetakens = re.findall(r'(?im)datetaken="(\d\d\d\d-\d\d-\d\d \d\d:\d\d:\d\d)"[^<>]*? id="(\d+)"', xmlraw2)
        print(datetakens)
        for datetaken, photoid in datetakens:
            if photoid in flickrdone:
                continue
            else:
                flickrdone.append(photoid)
                row = ['flickr', photoid, datetaken]
                rows.append(row)
            if not datetaken in originaldates:
                d1 = datetaken.split(' ')[0]
                d = datetime.datetime.strptime(d1, "%Y-%m-%d")
                unixtime = d.strftime('%s')
                if activity.has_key(unixtime):
                    activity[unixtime] += 1
                else:
                    activity[unixtime] = 1
                originaldates.append(datetaken)
        time.sleep(0.2)
    #save flickr csv
    rows.sort()
    with open('photos-flickr.csv', 'w') as csvfile:
        writer = csv.writer(csvfile, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
        for row in rows:
            writer.writerow(row)
    
    #save global activity json
    with open('actividad-foto.json', 'w') as outfile:
        outfile.write(json.dumps(activity, indent=4, sort_keys=True))

if __name__ == '__main__':
    main()
