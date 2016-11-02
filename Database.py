#!/usr/bin/python

import sqlite3
from bs4 import BeautifulSoup
import urllib2

# Define attributes
sqlite_file = 'websites.sqlite'
table_name = 'table_of_websites'
column1  = 'titles'
column2 = 'domains'
column3 = 'html'
field_type = 'TEXT'

# Connect to database
conn = sqlite3.connect("/home/chase/MobileProof/database/"+sqlite_file)
conn.text_factory = str
c = conn.cursor()

# Add columns
c.execute('CREATE TABLE {tn} ({c1} {ft} PRIMARY KEY)'.format(tn=table_name, c1=column1, ft=field_type))
c.execute("ALTER TABLE {tn} ADD COLUMN '{c2}' {ft}".format(tn=table_name, c2=column2, ft=field_type)) 
c.execute("ALTER TABLE {tn} ADD COLUMN '{c3}' {ft}".format(tn=table_name, c3=column3, ft=field_type))

# Get HTML for Pythagoras's Theorem ##########################################
url = 'https://www.proofwiki.org/wiki/Pythagoras\'s_Theorem'
req = urllib2.Request(url)
response = urllib2.urlopen(req)
the_page = response.read()
# make soup and extract important info
soup = BeautifulSoup(str(the_page), 'html.parser')
soup.prettify()
# get title of page
title = soup.title.string
title = title.replace(" - ProofWiki", "").strip()
# remove unimportant info
while soup.find(id="toc") != None:
    soup.find(id="toc").decompose()
while soup.find(id="stub") != None:
    soup.find(id="stub").decompose()
while soup.find(id="siteSub") != None:
    soup.find(id="siteSub").decompose()
while soup.find(class_="adsbygoogle") != None:
    soup.find(class_="adsbygoogle").decompose()
[s.extract() for s in soup('script')]

html = str(soup.find(id="content")).strip()


# Insert Pythagoras's Theorem info into SQLite database
try:
    c.execute("INSERT INTO table_of_websites (titles, domains, html) VALUES(?, ?, ?)", (title, url, html))

except sqlite3.IntegrityError:
    print("Error")
##############################################################################
# Repeatable code for putting in sqlite database


conn.commit()
conn.close()
