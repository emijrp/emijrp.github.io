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

import re
import sys

def readwikifile(wikifile):
    f = open(wikifile, 'r')
    wiki = f.read().strip()
    f.close()
    
    return wiki

def savehtmlfile(htmlfile, html):
    f = open(htmlfile, 'w')
    f.write(html)
    f.close()

def main():
    if len(sys.argv) < 2:
        print('Error: parameter needed')
    
    wikifile = sys.argv[1]
    wiki = readwikifile(wikifile)

    # {{templates}}
    templates = re.findall(r'(?im)\{\{([^\{\}\n\r]+?)\}\}', wiki)
    for template in templates:
        templatename = template.split('|')[0]
        templateparameters = template.split('|')[1:]
        wikitemplate = readwikifile('%s.wiki' % templatename.lower())
        c = 1
        for templateparameter in templateparameters:
            parametername = templateparameter.split('=')[0]
            parametervalue = templateparameter.split('=')[1]
            wikitemplate = wikitemplate.replace('{{{%s}}}' % (parametername), parametervalue)
            c += 1
        
        wiki = wiki.replace('{{%s}}' % (template), wikitemplate)
    
    # images
    images = re.findall(r'(?im)\[\[File:([^\[\]\|]+?)\]\]', wiki)
    for image in images:
        imagename = image.split('|')[0]
        imageparameters = image.split('|')[1:]
        wiki = wiki.replace('[[File:%s]]' % imagename, '<img src="images/%s" />' % (imagename))
    
    # text style
    wiki = re.sub(r'(?im)\'{3}([^\']+?)\'{3}', r'<b>\1</b>', wiki)
    wiki = re.sub(r'(?im)\'{2}([^\']+?)\'{2}', r'<i>\1</i>', wiki)
    wiki = re.sub(r'(?im)_([^\_]+?)_', r'<u>\1</u>', wiki)
    
    # [[links]]
    wiki = re.sub(r'(?im)\[\[([^\[\]\|]+?)\|([^\[\]\|]+?)\]\]', r'<a href="\1.html">\2</a>', wiki)
    wiki = re.sub(r'(?im)\[\[([^\[\]\|]+?)\]\]', r'<a href="\1.html">\1</a>', wiki)
    
    # [://links links]
    wiki = re.sub(r'(?im)\[((?:https?|ftps?)://[^\[\]\|]+?)\s+([^\[\]\|]+?)\]', r'<a href="\1">\2</a>', wiki)
    wiki = re.sub(r'(?im)\[((?:https?|ftps?)://[^\[\]\|]+?)\]', r'<a href="\1">\1</a>', wiki)
    
    # paragraphs
    paragraphs = wiki.split('\n')
    wiki2 = ''
    skipline = False
    for paragraph in paragraphs:
        paragraph2 = paragraph.strip()
        if skipline:
            wiki2 += '%s\n' % (paragraph)
            continue
        if paragraph2 == '':
            wiki2 += '\n'
        elif paragraph2.startswith('<'):
            if ('<script' in paragraph2 and not '</script>' in paragraph2) or \
                ('<!--' in paragraph2 and not '-->' in paragraph2):
                wiki2 += '%s\n' % (paragraph)
                skipline = True
                continue
            elif '</script>' in paragraph2:
                skipline = False
            
            wiki2 += '%s\n' % (paragraph)
        else:
            wiki2 += '<p>%s</p>\n' % (paragraph)
    wiki = wiki2
    
    html = wiki
    print(html)
    savehtmlfile('%s.html' % wikifile.split('.wiki')[0], html)

if __name__ == '__main__':
    main()

