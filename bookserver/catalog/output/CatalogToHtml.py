#!/usr/bin/env python

"""
Copyright(c)2008 Internet Archive. Software license AGPL version 3.

This file is part of bookserver.

    bookserver is free software: you can redistribute it and/or modify
    it under the terms of the GNU Affero General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    bookserver is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU Affero General Public License for more details.

    You should have received a copy of the GNU Affero General Public License
    along with bookserver.  If not, see <http://www.gnu.org/licenses/>.
    
    The bookserver source is hosted at http://github.com/internetarchive/bookserver/
"""

from CatalogRenderer import CatalogRenderer
from .. import Entry

import lxml.etree as ET

class CatalogToHtml(CatalogRenderer):
    """
    The HTML page is organised thus:
        PageHeader
        Navigation
        Search
        CatalogHeader
        EntryList
        PageFooter
    """
        
    def __init__(self, catalog):
        CatalogRenderer.__init__(self)
        self.processCatalog(catalog)
        
    def processCatalog(self, catalog):
        html = self.createHtml(catalog)
        html.append(self.createHead(catalog))
        body = self.createBody(catalog)
        html.append(body)
        body.append(self.createHeader(catalog))
        body.append(self.createNavigation(catalog._navigation))
        body.append(self.createSearch(catalog._opensearch))
        body.append(self.createCatalogHeader(catalog))
        body.append(self.createEntryList(catalog._entries))
        body.append(self.createFooter(catalog))
        
        self.html = html
        return self
        
    def createHtml(self, catalog):
        return ET.Element('html')
        
    def createHead(self, catalog):
        # XXX flesh out
        # updated
        # atom link
        
        head = ET.Element('head')
        titleElement = ET.SubElement(head, 'title')
        titleElement.text = catalog._title
        head.append(self.createStyleSheet('/static/catalog.css'))
        
        return head
        
    def createStyleSheet(self, url):
        # TODO add ?v={version}
        return ET.Element('link', {
            'rel':'stylesheet',
            'type':'text/css', 
            'href':url
        })
        
    def createBody(self, catalog):
        return ET.Element('body')
        
    def createHeader(self, catalog):
        div = ET.Element( 'div', {'class':'opds-header'} )
        div.text = 'OPDS Header' # XXX
        return div
        
    def createNavigation(self, navigation):
        div = ET.Element( 'div', {'class':'opds-navigation'} )
        div.text = 'Navigation div' # XXX
        return div
        
    def createSearch(self, opensearch):
        div = ET.Element( 'div', {'class':'opds-search'} )
        div.text = 'Search div' # XXX
        return div
        
    def createCatalogHeader(self, catalog):
        div = ET.Element( 'div', {'class':'opds-catalog-header'} )
        title = ET.SubElement(div, 'h1', {'class':'opds-catalog-header-title'} )
        title.text = catalog._title # XXX
        return div
                
    def createEntry(self, entry):
        e = ET.Element('p')
        e.set('class', 'entry')
        title = ET.SubElement(e, 'h2', {'class':'opds-entry-title'} )
        title.text = entry.get('title')
        
        # TODO sort for display order
        for key in Entry.valid_keys.keys():
            formattedEntryKey = self.createEntryKey(key, entry.get(key))
            if (formattedEntryKey):
                e.append( formattedEntryKey )
        
        return e
        
    def createEntryKey(self, key, value):
        if not value:
            # empty
            return None
        
        # XXX handle lists, pretty format key, order keys
        e = ET.Element('span', { 'class': 'opds-entry' })
        keyName = ET.SubElement(e, 'em', {'class':'opds-entry-key'})
        keyName.text = unicode(key, 'utf-8') + ':'
        keyName.tail = ' '
        keyValue = ET.SubElement(e, 'span', { 'class': 'opds-entry-value opds-entry-%s' % key })
        keyValue.text = unicode(value)
        ET.SubElement(e, 'br')
        return e
        
    def createEntryList(self, entries):
        list = ET.Element( 'ul', {'class':'opds-entry-list'} )
        for entry in entries:
            item = ET.SubElement(list, 'li', {'class':'opds-entry-list-item'} )
            item.append(self.createEntry(entry))
            list.append(item)
        return list
        
    def createFooter(self, catalog):
        div = ET.Element('div', {'class':'opds-footer'} )
        div.text = 'Page Footer Div' # XXX
        return div
        
    def toString(self):
        return self.prettyPrintET(self.html)
        
    
