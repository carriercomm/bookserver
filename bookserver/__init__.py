#!/usr/bin/env python

"""
Copyright(c)2009 Internet Archive. Software license AGPL version 3.

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

>>> import catalog
>>> urn = 'urn:x-internet-archive:bookserver:catalog'
>>> c = catalog.Catalog(title='Internet Archive OPDS', urn=urn)

>>> e = catalog.Entry({'urn'     : 'x-internet-archive:item:itemid',
...                    'url'     : 'http://archive.org/details/itemid',
...                    'title'   : u'test item',
...                    'updated' : '2009-01-01T00:00:00Z'})
>>> c.addEntry(e)

>>> start    = 0
>>> numFound = 2
>>> numRows  = 1
>>> urlBase  = '/alpha/a/'
>>> n = catalog.Navigation(start, numRows, numFound, urlBase)
>>> c.addNavigation(n)

>>> osDescription = 'http://bookserver.archive.org/opensearch.xml'
>>> o = catalog.OpenSearch(osDescription)
>>> c.addOpenSearch(o)

>>> r = catalog.output.CatalogToAtom(c)
>>> str = r.toString()
>>> print str
<feed xmlns="http://www.w3.org/2005/Atom" xmlns:dcterms="http://purl.org/dc/terms/" xmlns:dc="http://purl.org/dc/elements/1.1/">
  <title>Internet Archive OPDS</title>
  <id>urn:x-internet-archive:bookserver:catalog</id>
  <updated/>
  <link rel="self" type="application/atom+xml" href="http://bookserver.archive.org/catalog/"/>
  <author>
    <name>Internet Archive</name>
    <uri>http://www.archive.org</uri>
  </author>
  <link rel="search" type="application/atom+xml" href="http://bookserver.archive.org/opensearch.xml"/>
  <link rel="next" type="application/atom+xml" href="/alpha/a/1" title="Next results"/>
  <entry>
    <title>test item</title>
    <id>x-internet-archive:item:itemid</id>
    <updated>2009-01-01T00:00:00Z</updated>
    <link href="http://archive.org/details/itemid" type="application/atom+xml"/>
  </entry>
</feed>

>>> h = catalog.output.CatalogToHtml(c)
>>> html = h.toString()
>>> # print html

>>> pubInfo = {
...    'name'     : 'Internet Archive',
...    'uri'      : 'http://www.archive.org',
...    'opdsroot' : 'http://bookserver.archive.org/catalog',
...    'mimetype' : 'application/atom+xml;profile=opds',
...    'urlroot'  : '/catalog',
...    'urnroot'  : 'urn:x-internet-archive:bookserver:catalog',
... }
>>> solrUrl = 'http://se.us.archive.org:8983/solr/select?q=mediatype%3Atexts+AND+format%3A(LuraTech+PDF)&fl=identifier,title,creator,oai_updatedate,date,contributor,publisher,subject,language,month&sort=month+desc&rows=50&wt=json'
>>> ingestor = catalog.ingest.SolrToCatalog(pubInfo, solrUrl, urn)
>>> c = ingestor.getCatalog()
>>> print c._title
Internet Archive OPDS

"""

"""
bookserver/
    __init__.py
    
    catalog/
        __init__.py
        Catalog.py
        Entry.py
        Navigation.py
        OpenSearch.py
    
        ingest/
            __init__.py
            SolrToCatalog.py
            AtomToCatalog.py (future)

    output/
        __init__.py
        CatalogRenderer.py
        CatalogToXml.py
        CatalogToHtml.py
        CatalogToJson.py


>>> import bookserver.catalog as catalog
>>> c = catalog.Catalog()

>>> d = {'urn': 'x-internet-archive:item:itemid'}
>>> e = catalog.Entry(d)
>>> c.addEntry(e)

>>> nexturl = 'http://bookserver.archive.org/catalog/alpha/a/1'
>>> prevurl = None
>>> n = catalog.Navigation(nexturl, prevurl)
>>> c.addNavigation(n)

>>> osDescription = 'http://bookserver.archive.org/opensearch.xml'
>>> o = catalog.OpenSearch(osDescription)
>>> c.addOpenSearch(o)

>>> r = CatalogToXml()
>>> r.render(c)

"""

import catalog

if __name__ == '__main__':
    import doctest
    doctest.testmod()