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

import os
import re
import sys

# ideas:
# que ponga icono de PDF a los enlaces PDF
# mostrar icono de Wayback Machine al hacer hover sobre enlace
# que genere un sitemap
# hacer un buscador interno en javascript?

def readwikifile(wikifile):
    if os.path.exists(wikifile):
        f = open(wikifile, 'r')
        wiki = f.read().strip()
        f.close()
    else:
        wiki = '<span style="text-color: #FF0000;">[Página %s no encontrada]</span>' % (wikifile)
    
    return wiki

def savehtmlfile(htmlfile, html):
    f = open(htmlfile, 'w')
    f.write(html)
    f.close()

def sections(wiki):
    wiki = re.sub(r'(?im)^=\s*([^=]+?)\s*=', r'<h1>\1</h1>', wiki)
    wiki = re.sub(r'(?im)^==\s*([^=]+?)\s*==', r'<h2 id="\1">\1</h2>', wiki)
    wiki = re.sub(r'(?im)^===\s*([^=]+?)\s*===', r'<h3 id="\1">\1</h3>', wiki)
    wiki = re.sub(r'(?im)^====\s*([^=]+?)\s*====', r'<h4 id="\1">\1</h4>', wiki)
    
    return wiki

def templates(wiki):
    templates = re.findall(r'(?im)\{\{([^\{\}]+?)\}\}', wiki)
    for template in templates:
        templatename = template.split('|')[0]
        templateparameters = template.split('|')[1:]
        wikitemplate = readwikifile('%s.wiki' % templatename.lower())
        # remove noinclude
        wikitemplate = re.sub(r'(?im)<noinclude>.*?</noinclude>', '', wikitemplate)
        # clean includeonly
        wikitemplate = re.sub(r'(?im)<includeonly>(.*?)</includeonly>', '\1', wikitemplate)
        c = 1
        for templateparameter in templateparameters:
            parametername = templateparameter.split('=')[0].strip()
            parametervalue = templateparameter.split('=')[1].strip()
            wikitemplate = wikitemplate.replace('{{{%s}}}' % (parametername), parametervalue)
            wikitemplate = wikitemplate.replace('{{{%s|}}}' % (parametername), parametervalue)
            c += 1
        #remove empty parameters when {{{X|}}}
        wikitemplate = re.sub(r'{{{\d+\|\s*?}}}', '', wikitemplate)
        
        htmltemplate = wiki2html(wikitemplate)
        wiki = wiki.replace('{{%s}}' % (template), htmltemplate)
    
    return wiki

def images(wiki):
    imagepath = '.'
    if os.path.exists('imagepath.wiki'):
        f = open('imagepath.wiki')
        imagepath = f.read().strip()
        f.close()
    
    images = re.findall(r'(?im)\[\[File:([^\[\]\|]+?)\]\]', wiki)
    for image in images:
        imagename = image.split('|')[0]
        imageparameters = image.split('|')[1:]
        wiki = wiki.replace('[[File:%s]]' % imagename, '<a href="%s/%s"><img src="%s/%s" width="300px" /></a>' % (imagepath, imagename, imagepath, imagename))
    
    return wiki

def paragraphs(wiki):
    paragraphs = wiki.split('\n')
    wiki2 = ''
    skipline = False
    for paragraph in paragraphs:
        paragraph2 = paragraph.strip()
        if skipline:
            if '</script>' in paragraph2 or \
                '-->' in paragraph2 or \
                '</pre>' in paragraph2 or \
                '</ul>' in paragraph2:
                wiki2 += '%s\n' % (paragraph)
                skipline = False
            else:
                wiki2 += '%s\n' % (paragraph)
            continue
        if paragraph2 == '':
            wiki2 += '\n'
        elif paragraph2.startswith('<'):
            if ('<script' in paragraph2 and not '</script>' in paragraph2) or \
                ('<!--' in paragraph2 and not '-->' in paragraph2) or \
                ('<pre' in paragraph2 and not '</pre>' in paragraph2) or \
                ('<ul>' in paragraph2 and not '</ul>' in paragraph2):
                wiki2 += '%s\n' % (paragraph)
                skipline = True
                continue
            wiki2 += '%s\n' % (paragraph)
        else:
            wiki2 += '<p>%s</p>\n' % (paragraph)
    wiki = wiki2
    
    return wiki

def textformat(wiki):
    wiki = re.sub(r'(?im)\'{3}([^\']+?)\'{3}', r'<b>\1</b>', wiki)
    wiki = re.sub(r'(?im)\'{2}([^\']+?)\'{2}', r'<i>\1</i>', wiki)
    #wiki = re.sub(r'(?im)_([^\_]+?)_', r'<u>\1</u>', wiki) # error: reemplaza los _ de las urls
    
    return wiki

def linksinternal(wiki):
    m = re.findall(r'(?im)\[\[([^\[\]\|]+?)\|([^\[\]\|]+?)\]\]', wiki)
    for i in m:
        wiki = re.sub(r'(?im)\[\[%s\|%s\]\]' % (i[0], i[1]), '<a href="%s.html">%s</a>' % (re.sub(' ', '-', i[0].lower()), i[1]), wiki)
    
    m = re.findall(r'(?im)\[\[([^\[\]\|]+?)\]\]', wiki)
    for i in m:
        wiki = re.sub(r'(?im)\[\[%s\]\]' % (i), '<a href="%s.html">%s</a>' % (re.sub(' ', '-', i.lower()), i), wiki)
        
    return wiki

def linksexternal(wiki):
    # PDF #buscar icono y quitar lo de PDF
    wiki = re.sub(r'(?im)\[((?:https?://|ftps?://|\./)[^\[\]\| ]+?\.pdf)\s+([^\[\]\|]+?)\]', r'<a href="\1">\2</a> (PDF)', wiki)
    wiki = re.sub(r'(?im)\[((?:https?://|ftps?://|\./)[^\[\]\| ]+?\.pdf)\]', r'<a href="\1">\1</a> (PDF)', wiki)
    
    # other
    wiki = re.sub(r'(?im)\[((?:https?://|ftps?://|\./)[^\[\]\| ]+?)\s+([^\[\]\|]+?)\]', r'<a href="\1">\2</a>', wiki)
    wiki = re.sub(r'(?im)\[((?:https?://|ftps?://|\./)[^\[\]\| ]+?)\]', r'<a href="\1">\1</a>', wiki)
    
    return wiki

def wiki2html(wiki):
    wiki = sections(wiki)
    wiki = templates(wiki)
    wiki = images(wiki)
    wiki = paragraphs(wiki)
    wiki = textformat(wiki)
    wiki = linksinternal(wiki)
    wiki = linksexternal(wiki)
    
    html = wiki
    return html

def main():
    wikifiles = []
    
    if len(sys.argv) < 2:
        print('Error: parameter needed')
        sys.exit()
    
    if sys.argv[1] == '--all':
        listdir = os.listdir('.')
        for filename in listdir:
            if filename.endswith('.wiki'):
                wikifiles.append(filename)
    else:
        wikifiles = [sys.argv[1]]
    
    for wikifile in wikifiles:
        wiki = readwikifile(wikifile)
        try:
            html = wiki2html(wiki)
            #print(html)
            htmlfile = '%s.html' % wikifile.split('.wiki')[0]
            print 'Saving', wikifile, 'in', htmlfile
            savehtmlfile(htmlfile, html)
        except:
            print 'Error parsing', wikifile

if __name__ == '__main__':
    main()

