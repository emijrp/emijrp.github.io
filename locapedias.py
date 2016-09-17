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
import re
import urllib2

def main():
    locapedias = {
        u'Almeriapedia': {
            'api': 'https://almeriapedia.wikanda.es/w/api.php', 
            'dump': 'https://archive.org/details/wiki-almeriapediawikandaes_w', 
            'country': u'España', 
            'region': u'Provincia de Almería', 
        }, 
        u'Aragopedia': {
            'api': 'http://opendata.aragon.es/aragopedia/api.php', 
            'dump': 'https://archive.org/details/wiki-opendataaragones_aragopedia', 
            'country': u'España', 
            'region': u'Aragón', 
        }, 
        u'Arija': {
            'api': 'http://www.arija.org/es/api.php', 
            'dump': 'https://archive.org/details/wiki-arijaorg_es', 
            'country': u'España', 
            'region': u'Arija', 
        }, 
        u'Asturpedia': {
            'api': 'http://asturias.wikia.com/api.php', 
            'base': 'http://asturias.wikia.com/wiki/Portada', 
            'dump': '', 
            'country': u'España', 
            'region': u'Principado de Asturias', 
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
            'base': 'http://www.ctpedia.es', 
            'dump': 'https://archive.org/details/wiki-ctpediaes_w', 
            'country': u'España', 
            'region': u'Cartagena', 
            'stats': 'http://www.ctpedia.es/w/index.php/Special:Statistics?action=raw', 
        }, 
        u'DeLebrija': {
            'api': 'http://www.delebrija.es/api.php', 
            'base': 'http://www.delebrija.es/index.php/Portada', 
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
            'api': 'http://el.tesorodeoviedo.es/api.php', 
            'base': 'http://el.tesorodeoviedo.es/index.php?title=Portada', 
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
            'base': 'http://enwada.es/wiki/P%C3%A1gina_Principal', 
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
            'api': 'http://www.enciclopediadelinares.com/wiki/api.php', #'http://leonwiki.lazorrera.com', 
            'base': 'http://www.enciclopediadelinares.com/wiki', 
            'dump': 'https://archive.org/details/enciclopediadelinarescom_wiki-20110427-wikidump.7z', 
            'country': u'España', 
            'region': u'Linares', 
            'status': 'offline', 
        }, 
        u'Madripedia': {
            'api': 'http://www.madripedia.es', 
            'base': 'http://madripedia.es/wiki/Portada', 
            'dump': 'https://archive.org/details/wiki-madripediaes_w', 
            'country': u'España', 
            'mirror': 'https://madripedia.wikis.cc', 
            'region': u'Comunidad de Madrid', 
            'status': 'offline', 
        }, 
        u'Málaga Diwiki': {
            'api': 'http://malaga.diwiki.org', 
            'base': 'http://malaga.diwiki.org', 
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
            'api': 'http://www.malawi360.com/wiki/api.php', 
            'base': 'http://www.malawi360.com', 
            'dump': 'https://archive.org/details/wiki-malawi360com_wiki', 
            'country': u'Malawi', 
            'founded': '2007-08-24', 
            'region': u'Malawi', 
        }, 
        u'MiToledo': {
            'api': 'http://wiki.mitoledo.com/api.php', 
            'base': 'http://wiki.mitoledo.com/mediawiki/index.php/Portada', 
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
            'base': 'http://www.rosespedia.cat/index.php/P%C3%A0gina_principal', 
            'dump': '', 
            'country': u'España', 
            'region': u'Roses', 
            'stats': 'http://rosespedia.cat/index.php/Especial:Estad%C3%ADstiques', 
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
            'base': 'http://www.tarracowiki.cat/wiki/Portada', 
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
            'base': 'http://www.ugandawiki.ug', 
            'dump': '', 
            'country': u'Uganda', 
            'founded': '', 
            'region': u'Uganda', 
            'status': 'offline', 
        }, 
        u'Vilapedia': {
            'api': 'http://www.vila-real.info/vilapedia2015/', 
            'base': 'http://www.vila-real.info/vilapedia2015/', 
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
        u'Wiki-Anjou': {
            'api': 'http://www.wiki-anjou.fr/api.php', 
            'dump': '', 
            'country': u'Francia', 
            'founded': '', 
            'region': u'Maine-et-Loire', 
        }, 
        u'Wiki-Brest': {
            'api': 'http://www.wiki-brest.net/api.php', 
            'dump': '', 
            'country': u'Francia', 
            'founded': '', 
            'region': u'Pays de Brest', 
        }, 
        u'Wiki-Grenoble': {
            'api': 'http://www.wiki-grenoble.fr/api.php', 
            'base': 'http://wiki-grenoble.fr/index.php/Accueil', 
            'dump': '', 
            'country': u'Francia', 
            'founded': '', 
            'region': u'Grenoble', 
            'status': 'offline', 
        }, 
        u'Wiki-Massilia': {
            'api': 'http://wikimassilia.org/api.php', 
            'base': 'http://wikimassilia.org/index.php/Accueil', 
            'dump': '', 
            'country': u'Francia', 
            'founded': '', 
            'region': u'Marseille', 
            'status': 'offline', 
        }, 
        u'Wiki-Nanterre': {
            'api': 'http://www.wiki-nanterre.net/api.php', 
            'base': 'http://www.wiki-nanterre.net/index.php/Accueil', 
            'dump': '', 
            'country': u'Francia', 
            'founded': '', 
            'region': u'Nanterre', 
            'status': 'offline', 
        }, 
        u'Wiki-Narbonne': {
            'api': 'http://www.wiki-narbonne.fr/api.php', 
            'base': 'http://www.wiki-narbonne.fr/index.php?title=Accueil', 
            'dump': 'https://archive.org/details/wiki-wiki_narbonnefr', 
            'country': u'Francia', 
            'founded': '', 
            'region': u'Narbonne', 
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
            'base': 'http://www.wikiextremadura.org', 
            'dump': '', 
            'country': u'España', 
            'founded': '', 
            'region': u'Extremadura', 
            'status': 'offline', 
        }, 
        u'WikiLleida': {
            'api': 'http://www.wikilleida.cat', 
            'base': 'http://www.wikilleida.cat', 
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
            'base': 'http://www.wikisalamanca.org', 
            'dump': 'https://archive.org/details/wiki-wikisalamancaorg', 
            'country': u'España', 
            'founded': '', 
            'mirror': 'https://wikisalamanca.wikis.cc', 
            'region': u'Provincia de Salamanca', 
            'status': 'offline', 
        }, 
        u'WikiTunisie': {
            'api': 'http://www.wikitunisie.org', 
            'base': 'http://www.wikitunisie.org', 
            'dump': '', 
            'country': u'Túnez', 
            'founded': '', 
            'region': u'Túnez', 
            'status': 'offline', 
        }, 
        u'Xilocapedia': {
            'api': 'http://xiloca.org/xilocapedia/api.php', 
            'base': 'http://xiloca.org/xilocapedia/index.php?title=P%C3%A1gina_principal', 
            'dump': 'https://archive.org/details/wiki-xilocacom_xilocapedia', 
            'country': u'España', 
            'founded': '', 
            'region': u'Valle del Jiloca', 
            'stats': 'http://xiloca.org/xilocapedia/index.php?title=Especial:Estad%C3%ADsticas', 
        }, 
        u'Zaragoza Diwiki': {
            'api': 'http://zaragoza.diwiki.org', 
            'base': 'http://zaragoza.diwiki.org', 
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
            html = unicode(urllib2.urlopen(req).read(), 'utf-8').strip()
            siteinfo = json.loads(html)
            locapedias2[locapedia]['status'] = 'online'
            if 'query' in siteinfo and 'general' in siteinfo['query']:
                for prop in ['base', 'generator', 'lang', 'logo']:
                    locapedias2[locapedia][prop] = prop in siteinfo['query']['general'] and siteinfo['query']['general'][prop] or ''
            else:
                print('Error while retrieving siteinfo API for %s %s' % (locapedia, siteinfourl))
            
            if 'query' in siteinfo and 'statistics' in siteinfo['query']:
                for prop in ['articles', 'edits', 'images', 'pages', 'users']:
                    locapedias2[locapedia][prop] = prop in siteinfo['query']['statistics'] and siteinfo['query']['statistics'][prop] or ''
            else:
                print(u'Error while retrieving statistics API for %s %s' % (locapedia, siteinfourl))
                raise Exception(u'Error while retrieving statistics')
        except:
            if 'stats' in locaprops and locaprops['stats']:
                try:
                    req = urllib2.Request(locaprops['stats'], headers={ 'User-Agent': 'Mozilla/5.0' })
                    html = unicode(urllib2.urlopen(req).read(), 'utf-8').strip()
                    if html.startswith('total='):
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
                    elif 'mw-statistics-table' in html:
                        mwtable = html.split('mw-statistics-table')[1].split('</table>')[0]
                        print(statsurl)
                        print(mwtable.split('mw-statistics-pages')[1].split('</td></tr>')[0])
                        locapedias2[locapedia]['pages'] = mwtable.split('mw-statistics-pages')[1].split('</td></tr>')[0].split('>')[1].strip()
                        locapedias2[locapedia]['articles'] = mwtable.split('mw-statistics-articles')[1].split('</td></tr>')[0].split('>')[1].strip()
                        locapedias2[locapedia]['edits'] = mwtable.split('mw-statistics-edits')[1].split('</td></tr>')[0].split('>')[1].strip()
                        locapedias2[locapedia]['users'] = mwtable.split('mw-statistics-users')[1].split('</td></tr>')[0].split('>')[1].strip()
                        locapedias2[locapedia]['images'] = mwtable.split('mw-statistics-files')[1].split('</td></tr>')[0].split('>')[1].strip()
                    locapedias2[locapedia]['status'] = 'online'
                except:
                    msg = u'Error while retrieving statistics PLAIN for %s %s' % (locapedia, locaprops['stats'])
                    print(msg.encode('utf-8'))
                    locapedias2[locapedia]['status'] = 'offline'
        #get dump date
        if 'dump' in locaprops and 'archive.org' in locaprops['dump']:
            itemname = locaprops['dump'].split('/details/')[1].split('/')[0]
            iaurl = 'https://archive.org/download/%s/%s_files.xml' % (itemname, itemname)
            req = urllib2.Request(iaurl, headers={ 'User-Agent': 'Mozilla/5.0' })
            html = unicode(urllib2.urlopen(req).read(), 'utf-8').strip()
            filedates = [x for x, y in re.findall(ur'name="[^\"]+?-(\d{8})-(wikidump|history)', html)]
            if filedates:
                filedates.sort()
                filedates.reverse()
                locapedias2[locapedia]['dumpdate'] = '%s-%s-%s' % (filedates[0][0:4], filedates[0][4:6], filedates[0][6:8])
            else:
                locapedias2[locapedia]['dumpdate'] = ''
        print(locapedias2[locapedia])
    
    locapedias3 = [[v['name'].lower(), v] for k, v in locapedias2.items()]
    locapedias3.sort()
    locarows = []
    locac = 1
    for locapedia, locaprops in locapedias3:
        if 'status' in locaprops:
            if locaprops['status'].lower() == 'offline':
                locaprops['status'] = 'Offline'
            elif locaprops['status'].lower() == 'online':
                locaprops['status'] = 'Online'
            else:
                locaprops['status'] = 'Desconocido'
        else:
            locaprops['status'] = 'Desconocido'
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
        <td style="background-color: %s;">%s</td>
        <td>%s</td>
        <td><a href="https://web.archive.org/web/*/%s">IA</a></td>
        <td>%s</td>
    </tr>\n""" % (locac, 'base' in locaprops and locaprops['base'] or '', locaprops['name'], 'founded' in locaprops and locaprops['founded'] or '', locaprops['region'], locaprops['country'], 'articles' in locaprops and locaprops['articles'] or '?', 'pages' in locaprops and locaprops['pages'] or '?', 'images' in locaprops and locaprops['images'] or '?', 'users' in locaprops and locaprops['users'] or '?', locaprops['status'].lower() == 'offline' and 'pink' or 'lightgreen', locaprops['status'], locaprops['dump'] and 'lightgreen' or 'pink', locaprops['dump'] and u'<a href="%s">%s</a>' % (locaprops['dump'], 'dumpdate' in locaprops and locaprops['dumpdate'] or u'Sin fecha') or u'No', 'mirror' in locaprops and locaprops['mirror'] and u'<a href="%s">Sí</a>' % (locaprops['mirror']) or 'No', 'base' in locaprops and locaprops['base'] or '', 'generator' in locaprops and locaprops['generator'].split('MediaWiki ')[1] or u'?')
        locarows.append(locarow)
        locac += 1
    
    #print table
    table = u'\n<script type="text/javascript">sorttable.sort_alpha = function(a,b) { return a[0].localeCompare(b[0], "es"); }</script>\n'
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
        <th class="sorttable_alpha">MW</th>
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
