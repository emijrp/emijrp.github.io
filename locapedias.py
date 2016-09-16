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

import json
import urllib2

def main():
    locapedias = {
        u'Almeriapedia': {
            'api': 'https://almeriapedia.wikanda.es/w/api.php', 
            'dump': 'https://archive.org/details/wiki-almeriapediawikandaes_w', 
            'country': u'España', 
            'region': u'Provincia de Almería', 
        }, 
        u'Arija': {
            'api': 'http://www.arija.org/es/api.php', 
            'dump': 'https://archive.org/details/wiki-arijaorg_es', 
            'country': u'España', 
            'region': u'Arija', 
        }, 
        u'Ateneo de Córdoba': {
            'api': 'http://www.ateneodecordoba.com/api.php', 
            'dump': 'https://archive.org/details/wiki-ateneodecordobacom', 
            'country': u'España', 
            'region': u'Córdoba', 
        }, 
        u'Comuni-Italiani.it': {
            'api': 'http://rete.comuni-italiani.it/w/api.php', 
            'dump': 'https://archive.org/details/wiki-retecomuni_italianiit_w', 
            'country': u'Italia', 
            'region': u'', 
        }, 
        u'Cádizpedia': {
            'api': 'https://cadizpedia.wikanda.es/w/api.php', 
            'dump': 'https://archive.org/details/wiki-cadizpediawikandaes_w', 
            'country': u'España', 
            'region': u'Provincia de Cádiz', 
        }, 
        u'Córdobapedia': {
            'api': 'https://cordobapedia.wikanda.es/w/api.php', 
            'dump': 'https://archive.org/details/wiki-cordobapediawikandaes_w', 
            'country': u'España', 
            'region': u'Provincia de Córdoba', 
        }, 
        u'CTpedia': {
            'api': 'http://www.ctpedia.es/w/api.php', 
            'dump': 'https://archive.org/details/wiki-ctpediaes_w', 
            'country': u'España', 
            'region': u'Cartagena', 
            'stats': 'http://www.ctpedia.es/w/index.php/Special:Statistics?action=raw', 
        }, 
        u'DeLebrija': {
            'api': 'http://www.delebrija.es/index.php/Portada', 
            'dump': '', 
            'country': u'España', 
            'region': u'Lebrija', 
            'status': 'offline', 
        }, 
        u'Enciclopedia Guanche': {
            'api': 'http://www.guanches.org/enciclopedia/api.php', 
            'dump': 'https://archive.org/details/wiki-guanchesorg_enciclopedia', 
            'country': u'España', 
            'region': u'Islas Canarias', 
        }, 
        u'Enciclopedia de Oviedo': {
            'api': 'http://el.tesorodeoviedo.es', 
            'dump': '', 
            'country': u'España', 
            'region': u'Oviedo', 
        }, 
        u'EnnstalWiki': {
            'api': 'http://www.ennstalwiki.at/wiki/api.php', 
            'dump': '', 
            'country': u'Austria', 
            'region': u'Enns river valey', 
        }, 
        u'EnWada': {
            'api': 'http://enwada.es/w/api.php', 
            'dump': 'https://archive.org/details/wiki-enwadaes_w', 
            'country': u'España', 
            'region': u'Provincia de Guadalajara', 
        }, 
        u'Granadapedia': {
            'api': 'https://granadapedia.wikanda.es/w/api.php', 
            'dump': 'https://archive.org/details/wiki-granadapediawikandaes_w', 
            'country': u'España', 
            'region': u'Provincia de Granada', 
        }, 
        u'Huelvapedia': {
            'api': 'https://huelvapedia.wikanda.es/w/api.php', 
            'dump': 'https://archive.org/details/wiki-huelvapediawikandaes_w', 
            'country': u'España', 
            'region': u'Provincia de Huelva', 
        }, 
        u'Jaenpedia': {
            'api': 'https://jaenpedia.wikanda.es/w/api.php', 
            'dump': 'https://archive.org/details/wiki-jaenpediawikandaes_w', 
            'country': u'España', 
            'region': u'Provincia de Jaén', 
        }, 
        u'JerezSiempre': {
            'api': 'http://www.jerezsiempre.com/api.php', 
            'dump': 'https://archive.org/details/wiki-jerezsiemprecom', 
            'country': u'España', 
            'region': u'Jerez de la Frontera', 
        }, 
        u'LeonWiki': {
            'api': 'http://leonwiki.lazorrera.com', 
            'dump': '', 
            'country': u'España', 
            'region': u'León', 
            'status': 'offline', 
        }, 
        u'LinaWiki': {
            'api': 'http://leonwiki.lazorrera.com', 
            'dump': 'https://archive.org/details/enciclopediadelinarescom_wiki-20110427-wikidump.7z', 
            'country': u'España', 
            'region': u'Linares', 
            'status': 'offline', 
        }, 
        u'Madripedia': {
            'api': 'http://www.madripedia.es', 
            'dump': 'https://archive.org/details/wiki-madripediaes_w', 
            'country': u'España', 
            'mirror': 'https://madripedia.wikis.cc', 
            'region': u'Comunidad de Madrid', 
            'status': 'offline', 
        }, 
        u'Málaga Diwiki': {
            'api': 'http://malaga.diwiki.org', 
            'dump': '', 
            'country': u'España', 
            'region': u'Málaga', 
            'status': 'offline', 
        }, 
        u'Málagapedia': {
            'api': 'http://malagapedia.wikanda.es/w/api.php', 
            'dump': 'https://archive.org/details/wiki-malagapediawikandaes_w', 
            'country': u'España', 
            'region': u'Provincia de Málaga', 
        }, 
        u'Malawi360': {
            'api': 'http://www.malawi360.com', 
            'dump': 'https://archive.org/details/wiki-malawi360com_wiki', 
            'country': u'Malawi', 
            'founded': '2007-08-24', 
            'region': u'Malawi', 
        }, 
        u'MiToledo': {
            'api': 'http://wiki.mitoledo.com', 
            'dump': '', 
            'country': u'España', 
            'region': u'Toledo', 
            'status': 'offline', 
        }, 
        u'PlanetNepal': {
            'api': 'http://planetnepal.org/w/api.php', 
            'dump': '', 
            'country': u'Nepal', 
            'founded': '2010-01-31', 
            'region': u'Nepal', 
        }, 
        u'Rosespèdia': {
            'api': 'http://rosespedia.cat/w/api.php', 
            'dump': '', 
            'country': u'España', 
            'region': u'Roses', 
        }, 
        u'Sevillapedia': {
            'api': 'https://sevillapedia.wikanda.es/w/api.php', 
            'dump': 'https://archive.org/details/wiki-sevillapediawikandaes_w', 
            'country': u'España', 
            'region': u'Provincia de Sevilla', 
        }, 
        u'Stadtwiki Karlsruhe': {
            'api': 'https://sevillapedia.wikanda.es/w/api.php', 
            'dump': '', 
            'country': u'Alemania', 
            'founded': '2004-07-22', 
            'region': u'Karlsruhe', 
        }, 
        u'Tarracowiki': {
            'api': 'http://www.tarracowiki.cat/w/api.php', 
            'dump': 'https://archive.org/details/wiki-tarracowikicat_tarracowiki', 
            'country': u'España', 
            'founded': '', 
            'region': u'Tarragona', 
            'stats': 'http://www.tarracowiki.cat/wiki/Special:Statistics?action=raw', 
        }, 
        u'Tomsk Wiki': {
            'api': 'http://towiki.ru/w/api.php', 
            'dump': '', 
            'country': u'Rusia', 
            'founded': '2007-01-29', 
            'region': u'Tomsk', 
        }, 
        u'UgandaWiki': {
            'api': 'http://www.ugandawiki.ug', 
            'dump': '', 
            'country': u'Uganda', 
            'founded': '', 
            'region': u'Uganda', 
            'status': 'offline', 
        }, 
        u'Vilapedia': {
            'api': 'http://www.vila-real.info/vilapedia2015/', 
            'dump': 'https://archive.org/details/vila_realinfo_vilapedia-20110427-wikidump.7z', 
            'country': u'España', 
            'founded': '', 
            'mirror': 'https://vilapedia.wikis.cc', 
            'region': u'Villareal', 
            'status': 'offline', 
        }, 
        u'Wikanda': {
            'api': 'https://www.wikanda.es/w/api.php', 
            'dump': 'https://archive.org/details/wiki-wikandaes_w', 
            'country': u'España', 
            'founded': '', 
            'region': u'Andalucía', 
        }, 
        u'WikiBurgos': {
            'api': 'http://www.wikiburgos.es/api.php', 
            'dump': 'https://archive.org/details/wiki-wikiburgoses', 
            'country': u'España', 
            'founded': '', 
            'region': u'Burgos', 
        }, 
        u'WikiExtremadura': {
            'api': 'http://www.wikiextremadura.org', 
            'dump': '', 
            'country': u'España', 
            'founded': '', 
            'region': u'Extremadura', 
            'status': 'offline', 
        }, 
        u'WikiLleida': {
            'api': 'http://www.wikilleida.cat', 
            'dump': '', 
            'country': u'España', 
            'founded': '', 
            'region': u'Lleida', 
            'status': 'offline', 
        }, 
        u'WikiMurcia': {
            'api': 'http://wikimurcia.com/api.php', 
            'dump': '', 
            'country': u'España', 
            'founded': '', 
            'region': u'Murcia', 
        }, 
        u'WikiPakistan': {
            'api': 'http://pakistan.wikia.com/api.php', 
            'dump': '', 
            'country': u'Pakistán', 
            'founded': '', 
            'region': u'Pakistán', 
        }, 
        u'WikiRioja': {
            'api': 'http://wikirioja.com/api.php', 
            'dump': 'https://archive.org/details/wiki-wikiriojacom', 
            'country': u'España', 
            'founded': '', 
            'region': u'La Rioja', 
        }, 
        u'WikiSalamanca': {
            'api': 'http://www.wikisalamanca.org', 
            'dump': 'https://archive.org/details/wiki-wikisalamancaorg', 
            'country': u'España', 
            'founded': '', 
            'mirror': 'https://wikisalamanca.wikis.cc', 
            'region': u'Provincia de Salamanca', 
            'status': 'offline', 
        }, 
        u'WikiTunisie': {
            'api': 'http://www.wikitunisie.org', 
            'dump': '', 
            'country': u'Túnez', 
            'founded': '', 
            'region': u'Túnez', 
            'status': 'offline', 
        }, 
        u'Xilocapedia': {
            'api': '', 
            'dump': 'https://archive.org/details/wiki-xilocacom_xilocapedia', 
            'country': u'España', 
            'founded': '', 
            'region': u'Valle del Jiloca', 
            'stats': 'http://www.tarracowiki.cat/wiki/Special:Statistics?action=raw', 
        }, 
        u'Zaragoza Diwiki': {
            'api': 'http://zaragoza.diwiki.org', 
            'dump': '', 
            'country': u'España', 
            'founded': '', 
            'region': u'Zaragoza', 
            'status': 'offline', 
        }, 
    }
    locapedias2 = locapedias.copy()
    
    for locapedia, locaprops in locapedias.items():
        locapedias2[locapedia]['name'] = locapedia
        if 'status' in locaprops and locaprops['status'].lower() == 'offline':
            continue
        
        try:
            siteinfourl = '%s?action=query&meta=siteinfo&siprop=general|statistics&format=json' % (locaprops['api'])
            siteinfo = {}
            req = urllib2.Request(siteinfourl, headers={ 'User-Agent': 'Mozilla/5.0' })
            html = unicode(urllib2.urlopen(req).read(), 'utf-8')
            siteinfo = json.loads(html)
            locapedias2[locapedia]['status'] = 'online'
            if 'query' in siteinfo and 'general' in siteinfo['query']:
                for prop in ['base', 'generator', 'lang', 'logo']:
                    locapedias2[locapedia][prop] = prop in siteinfo['query']['general'] and siteinfo['query']['general'][prop] or ''
            else:
                print('Error while retrieving siteinfo for %s %s' % (locapedia, siteinfourl))
            
            if 'query' in siteinfo and 'statistics' in siteinfo['query']:
                for prop in ['articles', 'edits', 'images', 'pages']:
                    locapedias2[locapedia][prop] = prop in siteinfo['query']['statistics'] and siteinfo['query']['statistics'][prop] or ''
            else:
                print('Error while retrieving statistics for %s %s' % (locapedia, siteinfourl))
        except:
            try:
                statsurl = locaprops['stats']
                stats = {}
                req = urllib2.Request(statsurl, headers={ 'User-Agent': 'Mozilla/5.0' })
                html = unicode(urllib2.urlopen(req).read(), 'utf-8')
                for prop, value in [x.split('=') for x in html.split(';')]:
                    if prop == 'total':
                        locapedias2[locapedia]['pages'] = value
                    elif prop == 'good':
                        locapedias2[locapedia]['articles'] = value
                    elif prop == 'edits':
                        locapedias2[locapedia]['edits'] = value
                    elif prop == 'users':
                        locapedias2[locapedia]['users'] = value
                    elif prop == 'images':
                        locapedias2[locapedia]['images'] = value
                locapedias2[locapedia]['status'] = 'online'
            except:
                locapedias2[locapedia]['status'] = 'offline'
    
    locapedias3 = [[v['name'].lower(), v] for k, v in locapedias2.items()]
    locapedias3.sort()
    locarows = []
    locac = 1
    for locapedia, locaprops in locapedias3:
        if locaprops['status'].lower() == 'offline':
            locaprops['status'] = 'Offline'
        elif locaprops['status'].lower() == 'online':
            locaprops['status'] = 'Online'
        locarow = u"""
    <tr>
        <td>%s</td>
        <td><a href="%s">%s</a></td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td>%s</td>
        <td style="background-color: %s;">%s</td>
        <td>%s</td>
        <td>%s</td>
        <td><a href="https://web.archive.org/web/*/%s">IA</a></td>
    </tr>\n""" % (locac, 'base' in locaprops and locaprops['base'] or '', locaprops['name'], 'founded' in locaprops and locaprops['founded'] or '', locaprops['region'], locaprops['country'], 'articles' in locaprops and locaprops['articles'] or '?', 'pages' in locaprops and locaprops['pages'] or '?', 'images' in locaprops and locaprops['images'] or '?', 'users' in locaprops and locaprops['users'] or '?', locaprops['status'].lower() == 'offline' and 'pink' or 'lightgreen', locaprops['status'], 'dump' in locaprops and locaprops['dump'] and '<a href="%s">Dump</a>' % (locaprops['dump']) or '', 'mirror' in locaprops and locaprops['mirror'] and '<a href="%s">Mirror</a>' % (locaprops['mirror']) or '', 'base' in locaprops and locaprops['base'] or '')
        locarows.append(locarow)
        locac += 1
    
    #print table
    table = u"\n<script>sorttable.sort_alpha = function(a,b) { return a[0].localeCompare(b[0], 'es'); }</script>\n"
    table += u'\n<table class="wikitable sortable" style="text-align: center;">\n'
    table += u"""
    <tr>
        <th class="sorttable_numeric">#</th>
        <th class="sorttable_alpha">Locapedia</th>
        <th class="sorttable_alpha">Fundación</th>
        <th class="sorttable_alpha">Región</th>
        <th class="sorttable_alpha">País</th>
        <th class="sorttable_numeric">Artículos</th>
        <th class="sorttable_numeric">Páginas</th>
        <th class="sorttable_numeric">Imágenes</th>
        <th class="sorttable_numeric">Usuarios</th>
        <th class="sorttable_alpha">Estado</th>
        <th class="sorttable_alpha">Dump</th>
        <th class="sorttable_alpha">Mirror</th>
        <th class="sorttable_alpha">IA</th>
    </tr>"""
    locatable = table
    locatable += ''.join(locarows)
    locatable += '</table>\n'
    
    with open('locapedias.wiki', 'r') as f:
        html = unicode(f.read(), 'utf-8')
    with open('locapedias.wiki', 'w') as g:
        html = u'%s<!-- tabla completa -->%s<!-- /tabla completa -->%s' % (html.split(u'<!-- tabla completa -->')[0], locatable, html.split(u'<!-- /tabla completa -->')[1])
        g.write(html.encode('utf-8'))
        
if __name__ == '__main__':
    main()
