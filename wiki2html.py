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
# que admita como parametro de entrada *.html
# que ponga icono de PDF a los enlaces PDF
# que genere un sitemap

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
    templates = re.findall(r'(?im)\{\{([^\{\}\n\r]+?)\}\}', wiki)
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
            parametername = templateparameter.split('=')[0]
            parametervalue = templateparameter.split('=')[1]
            wikitemplate = wikitemplate.replace('{{{%s}}}' % (parametername), parametervalue)
            wikitemplate = wikitemplate.replace('{{{%s|}}}' % (parametername), parametervalue)
            c += 1
        #remove empty parameters when {{{X|}}}
        wikitemplate = re.sub(r'{{{\d+\|\s*?}}}', '', wikitemplate)
        
        htmltemplate = wiki2html(wikitemplate)
        wiki = wiki.replace('{{%s}}' % (template), htmltemplate)
    
    return wiki

def images(wiki):
    images = re.findall(r'(?im)\[\[File:([^\[\]\|]+?)\]\]', wiki)
    for image in images:
        imagename = image.split('|')[0]
        imageparameters = image.split('|')[1:]
        wiki = wiki.replace('[[File:%s]]' % imagename, '<img src="images/%s" />' % (imagename))
    
    return wiki

def paragraphs(wiki):
    paragraphs = wiki.split('\n')
    wiki2 = ''
    skipline = False
    for paragraph in paragraphs:
        paragraph2 = paragraph.strip()
        if skipline:
            if '</script>' in paragraph2 or \
                '-->' in paragraph2:
                wiki2 += '%s\n' % (paragraph)
                skipline = False
            else:
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
            wiki2 += '%s\n' % (paragraph)
        else:
            wiki2 += '<p>%s</p>\n' % (paragraph)
    wiki = wiki2
    
    return wiki

def textformat(wiki):
    wiki = re.sub(r'(?im)\'{3}([^\']+?)\'{3}', r'<b>\1</b>', wiki)
    wiki = re.sub(r'(?im)\'{2}([^\']+?)\'{2}', r'<i>\1</i>', wiki)
    wiki = re.sub(r'(?im)_([^\_]+?)_', r'<u>\1</u>', wiki)
    
    return wiki

def linksinternal(wiki):
    wiki = re.sub(r'(?im)\[\[([^\[\]\|]+?)\|([^\[\]\|]+?)\]\]', r'<a href="\1.html">\2</a>', wiki)
    wiki = re.sub(r'(?im)\[\[([^\[\]\|]+?)\]\]', r'<a href="\1.html">\1</a>', wiki)
    
    return wiki

def linksexternal(wiki):
    # PDF #buscar icono y quitar lo de PDF
    wiki = re.sub(r'(?im)\[((?:https?|ftps?)://[^\[\]\| ]+?\.pdf)\s+([^\[\]\|]+?)\]', r'<a href="\1">\2</a> (PDF)', wiki)
    wiki = re.sub(r'(?im)\[((?:https?|ftps?)://[^\[\]\| ]+?\.pdf)\]', r'<a href="\1">\1</a> (PDF)', wiki)
    
    # other
    wiki = re.sub(r'(?im)\[((?:https?|ftps?)://[^\[\]\| ]+?)\s+([^\[\]\|]+?)\]', r'<a href="\1">\2</a>', wiki)
    wiki = re.sub(r'(?im)\[((?:https?|ftps?)://[^\[\]\| ]+?)\]', r'<a href="\1">\1</a>', wiki)
    
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
    if len(sys.argv) < 2:
        print('Error: parameter needed')
    
    wikifile = sys.argv[1]
    wiki = readwikifile(wikifile)
    html = wiki2html(wiki)
    #print(html)
    savehtmlfile('%s.html' % wikifile.split('.wiki')[0], html)

if __name__ == '__main__':
    main()

