#!/usr/bin/env python

import copy, os, re, sqlite3, string, urllib
from bs4 import BeautifulSoup, NavigableString, Tag

DOCUMENTS_DIR = os.path.join('Microformats.docset', 'Contents', 'Resources', 'Documents')
MICROFORMATS_DIR = os.path.join('microformats.org/profile')
XFN_DIR = os.path.join('gmpg.org/xfn')

db = sqlite3.connect('Microformats.docset/Contents/Resources/docSet.dsidx')
cur = db.cursor()

try: cur.execute('DROP TABLE searchIndex;')
except: pass
cur.execute('CREATE TABLE searchIndex(id INTEGER PRIMARY KEY, name TEXT, type TEXT, path TEXT);')
cur.execute('CREATE UNIQUE INDEX anchor ON searchIndex (name, type, path);')

# build search index and tables of contents
for filename in os.listdir(os.path.join(DOCUMENTS_DIR, MICROFORMATS_DIR)):
    path = os.path.join(DOCUMENTS_DIR, MICROFORMATS_DIR, filename)
    if os.path.isdir(path):
        # skip directories
        continue

    page = open(os.path.join(DOCUMENTS_DIR, MICROFORMATS_DIR, filename)).read()

    soup = BeautifulSoup(page, 'html5lib')

    # add each Microformat object
    title = soup.find('title').text.strip()
    m = re.search('([^\s]*)', title)
    title = m.group(0)

    if len(title) > 0:
        path = os.path.join(MICROFORMATS_DIR, filename)
        cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (title, 'Object', path))
        print 'title: %s, path: %s' % (title, path)

    # add each Microformat properties
    for tag in soup.find_all('dt'):
        dashAnchor = tag.find('a', class_='dashAnchor')
        if dashAnchor:
            continue

        text = tag.text.strip()

        #print 'adding toc tag for section: %s' % text
        name = '//apple_ref/cpp/Property/' + urllib.quote(text, '')
        dashAnchor = BeautifulSoup('<a name="%s" class="dashAnchor"></a>' % name).a
        tag.insert(0, dashAnchor)
        print 'name: %s, path: %s' % (text, path)

    fp = open(os.path.join(DOCUMENTS_DIR, MICROFORMATS_DIR, filename), 'w')
    fp.write(str(soup))
    fp.close()

page = open(os.path.join(DOCUMENTS_DIR, XFN_DIR, "11.html")).read()

soup = BeautifulSoup(page, 'html5lib')

# add XFN
title = soup.find('title').text.strip()
m = re.search('([^\s]*)', title)
title = m.group(0)

# add XFN object
if len(title) > 0:
    path = os.path.join(XFN_DIR, "11.html")
    cur.execute('INSERT OR IGNORE INTO searchIndex(name, type, path) VALUES (?,?,?)', (title, 'Object', path))
    print 'title: %s, path: %s' % (title, path)

# add each Microformat properties
for tag in soup.find_all('dt'):
    dashAnchor = tag.find('a', class_='dashAnchor')
    if dashAnchor:
        continue

    text = tag.text.strip()

    #print 'adding toc tag for section: %s' % text
    name = '//apple_ref/cpp/Property/' + urllib.quote(text, '')
    dashAnchor = BeautifulSoup('<a name="%s" class="dashAnchor"></a>' % name).a
    tag.insert(0, dashAnchor)
    print 'name: %s, path: %s' % (text, path)

fp = open(os.path.join(DOCUMENTS_DIR, XFN_DIR, "11.html"), 'w')
fp.write(str(soup))
fp.close()

page = open(os.path.join(DOCUMENTS_DIR, MICROFORMATS_DIR, filename)).read()

db.commit()
db.close()
