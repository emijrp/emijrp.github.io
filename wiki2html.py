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
# que genere un sitemap, y una lista de archivos y un indice de palabras
# hacer un buscador interno en javascript?
# generar jpg con la portada de los pdf

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

def includes(wiki, wikifile):
    wiki = re.sub(r'(?im)<noinclude>(.*?)</noinclude>', r'\1', wiki)
    wiki = re.sub(r'(?im)<includeonly>.*?</includeonly>', r'', wiki)
    
    return wiki

def sections(wiki, wikifile):
    wiki = re.sub(r'(?im)^=\s*([^=]+?)\s*=', r'<h1>\1</h1>', wiki)
    wiki = re.sub(r'(?im)^==\s*([^=]+?)\s*==', r'<h2 id="\1">\1</h2>', wiki)
    wiki = re.sub(r'(?im)^===\s*([^=]+?)\s*===', r'<h3 id="\1">\1</h3>', wiki)
    wiki = re.sub(r'(?im)^====\s*([^=]+?)\s*====', r'<h4 id="\1">\1</h4>', wiki)
    
    return wiki

def templates(wiki, wikifile):
    templates = re.findall(r'(?im)\{\{([^\{\}]+?)\}\}', wiki)
    for template in templates:
        templatename = template.split('|')[0]
        templateparameters = template.split('|')[1:]
        wikitemplate = readwikifile('%s.wiki' % templatename.lower())
        # remove noinclude
        wikitemplate = re.sub(r'(?im)<noinclude>.*?</noinclude>', r'', wikitemplate)
        # clean includeonly
        wikitemplate = re.sub(r'(?im)<includeonly>(.*?)</includeonly>', r'\1', wikitemplate)
        c = 1
        for templateparameter in templateparameters:
            parametername = templateparameter.split('=')[0].strip()
            parametervalue = templateparameter.split('=')[1].strip()
            wikitemplate = wikitemplate.replace('{{{%s}}}' % (parametername), parametervalue)
            wikitemplate = wikitemplate.replace('{{{%s|}}}' % (parametername), parametervalue)
            c += 1
        #remove empty parameters when {{{X|}}}
        wikitemplate = re.sub(r'{{{\d+\|\s*?}}}', '', wikitemplate)
        
        htmltemplate = wiki2html(wikitemplate, wikifile)
        wiki = wiki.replace('{{%s}}' % (template), htmltemplate)
    
    return wiki

def images(wiki, wikifile):
    imagepath = '.'
    if os.path.exists('imagepath.wiki'):
        f = open('imagepath.wiki')
        imagepath = f.read().strip()
        f.close()
    
    images = re.findall(r'(?im)\[\[File:([^\[\]]+?)\]\]', wiki)
    for image in images:
        #print image
        imagename = image.split('|')[0]
        imageparameters = image.split('|')[1:]
        imagewidth = ''
        imageposition = 'right'
        imagedesc = imagename
        for imageparameter in imageparameters:
            imageparameter = imageparameter.strip()
            
            if re.search(r'\d+px', imageparameter):
                imagewidth = imageparameter
            elif re.search(r'(?i)(left|center|right)', imageparameter):
                imageposition = imageparameter
            else:
                imagedesc = imageparameter
        
        if imagename.endswith('.pdf'):
            wiki = wiki.replace('[[File:%s]]' % image, '<a href="%s/%s">%s</a> (PDF)' % (imagepath, imagename, imagedesc))
        else:
            wiki = wiki.replace('[[File:%s]]' % image, '<a href="%s/%s"><img src="%s/%s" width="%s" align="%s" alt="%s" title="%s" /></a>' % (imagepath, imagename, imagepath, imagename, imagewidth, imageposition, imagedesc, imagedesc))
    
    return wiki

def paragraphs(wiki, wikifile):
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
        elif paragraph2.startswith('*') or paragraph2.startswith('#'):
            wiki2 += '%s\n' % (paragraph)
            continue
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

def textformat(wiki, wikifile):
    wiki = re.sub(r'(?im)\'{3}([^\']+?)\'{3}', r'<b>\1</b>', wiki)
    wiki = re.sub(r'(?im)\'{2}([^\']+?)\'{2}', r'<i>\1</i>', wiki)
    #wiki = re.sub(r'(?im)_([^\_]+?)_', r'<u>\1</u>', wiki) # error: reemplaza los _ de las urls
    
    return wiki

def linksinternal(wiki, wikifile):
    wiki = re.sub(r'\[\[(%s)\|([^\]]*?)\]\]' % (wikifile.split('.wiki')[0]), r'<b>\2</b>', wiki)
    wiki = re.sub(r'\[\[(%s)\]\]' % (wikifile.split('.wiki')[0]), r'<b>\1</b>', wiki)
    
    m = re.findall(r'(?im)\[\[([^\[\]\|]+?)\|([^\[\]\|]+?)\]\]', wiki)
    for i in m:
        wiki = re.sub(r'(?im)\[\[%s\|%s\]\]' % (i[0], i[1]), '<a href="%s.html">%s</a>' % (re.sub(' ', '-', i[0].lower()), i[1]), wiki)
    
    m = re.findall(r'(?im)\[\[([^\[\]\|]+?)\]\]', wiki)
    for i in m:
        wiki = re.sub(r'(?im)\[\[%s\]\]' % (i), '<a href="%s.html">%s</a>' % (re.sub(' ', '-', i.lower()), i), wiki)
        
    return wiki

def linksexternal(wiki, wikifile):
    # PDF #buscar icono y quitar lo de PDF
    wiki = re.sub(r'(?im)\[((?:https?://|ftps?://|\./)[^\[\]\| ]+?\.pdf)\s+([^\[\]\|]+?)\]', r'<a href="\1">\2</a> (PDF)', wiki)
    wiki = re.sub(r'(?im)\[((?:https?://|ftps?://|\./)[^\[\]\| ]+?\.pdf)\]', r'<a href="\1">\1</a> (PDF)', wiki)
    
    # other
    wiki = re.sub(r'(?im)\[((?:https?://|ftps?://|\./)[^\[\]\| ]+?)\s+([^\[\]\|]+?)\]', r'<a href="\1">\2</a>', wiki)
    wiki = re.sub(r'(?im)\[((?:https?://|ftps?://|\./)[^\[\]\| ]+?)\]', r'<a href="\1">\1</a>', wiki)
    
    return wiki

def references(wiki, wikifile):
    refs = {}
    m = re.findall(r'(?im)(<ref( name=["\']([^<>]+?)["\'])?>([^<>]+?)</ref>)', wiki)
    c = 1
    for i in m:
        #print i
        ref = i[0]
        refname = i[2]
        refcontent = i[3]
        refnum = c
        if refname:
            refs[refname] = refnum
        wiki = wiki.replace(ref, '<sup>[<a href="#ref%s">%s</a>]</sup>' % (c, c))
        wiki = wiki.replace('<!--/references-->', '<li id="ref%s">%s</li>\n<!--/references-->' % (c, refcontent))
        c += 1
    
    m = re.findall(r'(?im)(<ref( name=["\']([^<>]+?)["\'])?\s*/\s*>)', wiki)
    for i in m:
        #print i
        ref = i[0]
        refname = i[2]
        if refname in refs:
            wiki = wiki.replace(ref, '<sup>[<a href="#ref%s">%s</a>]</sup>' % (refs[refname], refs[refname]))
    
    return wiki

def itemlist(wiki, wikifile):
    c = 10
    while c > 0:
        wiki = re.sub(r'(?im)^%s *([^\n]*?)$' % ('\*'*c), r'%s<li>\1</li>%s' % ('<ul>'*c, '</ul>'*c), wiki)
        c -= 1
    c = 10
    while c > 0:
        wiki = re.sub(r'(?im)%s\n*%s' % ('</ul>'*c, '<ul>'*c), '', wiki)
        c -= 1
    
    c = 10
    while c > 0:
        wiki = re.sub(r'(?im)^%s *([^\n]*?)$' % ('\#'*c), r'%s<li>\1</li>%s' % ('<ol>'*c, '</ol>'*c), wiki)
        c -= 1
    c = 10
    while c > 0:
        wiki = re.sub(r'(?im)%s\n*%s' % ('</ol>'*c, '<ol>'*c), '', wiki)
        c -= 1
    
    return wiki

def toc(wiki, wikifile):
    if '__notoc__' in wiki.lower():
        wiki = re.sub(r'(?im)__NOTOC__', '', wiki)
        return wiki
    
    m = re.findall(r'(?im)<h([234]) id="([^<>]*?)">([^<>]*?)</h[234]>', wiki)
    l2 = 0
    l3 = 0
    l4 = 0
    if len(m) >= 2:
         toc = '<table id="toc" class="wikitable">\n'
         toc += '<th>Tabla de contenidos</th>\n'
         toc += '<tr><td>\n'
         for i in m:
             if int(i[0]) == 2:
                 l2 += 1
                 l3 = 0
                 l4 = 0
                 toc += '&nbsp;%s. <a href="#%s">%s</a><br/>\n' % (l2, i[1], i[2])
             elif int(i[0]) == 3:
                 l3 += 1
                 l4 = 0
                 toc += '&nbsp;&nbsp;&nbsp;&nbsp;%s.%s <a href="#%s">%s</a><br/>\n' % (l2, l3, i[1], i[2])
             elif int(i[0]) == 4:
                 l4 += 1
                 toc += '&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;%s.%s.%s <a href="#%s">%s</a><br/>\n' % (l2, l3, l4, i[1], i[2])
         
         toc += '</td></tr>\n'
         toc += '</table>\n'
         wiki = re.sub('<h2', '%s\n<h2' % (toc), wiki, count=1)
    
    return wiki

def sitemap(wikilist):
    if not os.path.exists('sitemap.wiki'):
        return 
    
    wikilist.sort()
    table = u"\n<script>sorttable.sort_alpha = function(a,b) { return a[0].localeCompare(b[0], 'es'); }</script>\n"
    table += u'\n<table class="wikitable sortable" style="text-align: center;">\n'
    table += u"""
    <tr>
        <th class="sorttable_numeric">#</th>
        <th class="sorttable_alpha">Página HTML</th>
        <th class="sorttable_alpha">Página wiki</th>
        <th class="sorttable_numeric">Tamaño (bytes)</th>
    </tr>"""
    sitemaprows = []
    c = 1
    for i in wikilist:
        j = i.split('.wiki')[0]
        row = u"""
    <tr>
        <td>%s</td>
        <td><a href="%s.html">%s.html</a></td>
        <td><a href="%s.wiki">%s.wiki</a></td>
        <td>%d</td>
    </tr>\n""" % (c, j, j, j, j, len(readwikifile(i)))
        sitemaprows.append(row)
        c += 1
    
    table += u''.join(sitemaprows)
    table += u'</table>\n'
    
    f = open('sitemap.wiki', 'r')
    wikicode = unicode(f.read(), 'utf-8')
    f.close()
    f = open('sitemap.wiki', 'w')
    wikicode = u'%s<!-- tabla completa -->%s<!-- /tabla completa -->%s' % (wikicode.split(u'<!-- tabla completa -->')[0], table, wikicode.split(u'<!-- /tabla completa -->')[1])
    f.write(wikicode.encode('utf-8'))
    f.close()

def wiki2html(wiki, wikifile):
    wiki = includes(wiki, wikifile)
    wiki = sections(wiki, wikifile)
    wiki = templates(wiki, wikifile)
    wiki = images(wiki, wikifile)
    wiki = paragraphs(wiki, wikifile)
    wiki = references(wiki, wikifile)
    wiki = textformat(wiki, wikifile)
    wiki = linksinternal(wiki, wikifile)
    wiki = linksexternal(wiki, wikifile)
    wiki = itemlist(wiki, wikifile)
    wiki = toc(wiki, wikifile)
    
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
        sitemap(wikifiles)
    else:
        wikifiles = [sys.argv[1]]
    
    for wikifile in wikifiles:
        wiki = readwikifile(wikifile)
        try:
            html = wiki2html(wiki, wikifile)
            #print(html)
            htmlfile = '%s.html' % wikifile.split('.wiki')[0]
            print 'Saving', wikifile, 'in', htmlfile
            savehtmlfile(htmlfile, html)
        except:
            print 'Error parsing', wikifile

if __name__ == '__main__':
    main()

