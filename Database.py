#!/usr/bin/python

import sqlite3
from bs4 import BeautifulSoup
import urllib2

def clean_html(url):
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    the_page = response.read()
    soup = BeautifulSoup(str(the_page), 'html.parser')
    soup.prettify()
    title = soup.title.string.replace(" - ProofWiki", "").strip()
    soup = soup.find(id="content")
    # remove unimportant info
    while soup.find(id="toc") != None:
        soup.find(id="toc").decompose()
    while soup.find(id="jump-to-nav") != None:
        soup.find(id="jump-to-nav").decompose()
    while soup.find(id="stub") != None:
        soup.find(id="stub").decompose()
    while soup.find(id="siteSub") != None:
        soup.find(id="siteSub").decompose()
    while soup.find(class_="adsbygoogle") != None:
        soup.find(class_="adsbygoogle").decompose()
    while soup.find(id="catlinks") != None:
        soup.find(id="catlinks").decompose()
    while soup.find(id="Also_see") != None:
        soup.find(id="Also_see").decompose()
    while soup.find(class_="printfooter") != None:
        soup.find(class_="printfooter").decompose()
    [s.extract() for s in soup('script')]
    return str(url).strip(), str(title).strip(), soup

def get_categories(url, parent, categories=[]):
    soup = clean_html(url)[2]
    cats = soup.find("div", {"class":"mw-category"})
    if cats is None :
        return
    cats = cats.find_all('a')
    for cat in cats:
        if cat != None \
                and cat.get('href') != None \
                and "wiki" in cat.get('href') \
                and "Category" in cat.get('href') \
                and "Definition" not in cat.get('href') \
                and parent != "https://proofwiki.org" + cat.get('href') \
                and cat.get('href') not in categories \
                and "//" not in cat.get('href'):
            print cat.get('href')
            categories.append(cat.get('href'))
            get_categories("https://proofwiki.org"+cat.get('href'), url, categories)
    return categories

def get_proofs(url, proofs=[]):
    soup = clean_html(url)[2]
    proofs = soup.find("div", {"id":"mw-pages"})
    if proofs is None:
        return
    proofs = soup.find_all('a')
    for proof in proofs:
        if proof != None \
                and proof.get('href') != None \
                and "wiki" in proof.get('href') \
                and "Category" not in proof.get('href') \
                and proof.get('href') not in proofs \
                and "//" not in proof.get('href'):
            print proof.get('href')
            proof.append(proof.get('href'))
    return proofs

# Define attributes
sqlite_file = 'websites.sqlite'
table_name = 'table_of_websites'
column1  = 'titles'
column2 = 'domain'
column3 = 'html'
field_type = 'TEXT'

# Connect to database
conn = sqlite3.connect("/home/chase/MobileProof/database/"+sqlite_file)
conn.text_factory = str
c = conn.cursor()

# Add columns
c.execute("CREATE TABLE table_of_websites ('titles' TEXT PRIMARY KEY)")
c.execute("ALTER TABLE table_of_websites ADD COLUMN 'domain' TEXT") 
c.execute("ALTER TABLE table_of_websites ADD COLUMN 'html' TEXT")

base_url = "https://proofwiki.org"
cat_url = "/wiki/Category:Proofs"
categories = []
#categories = get_categories(base_url+cat_url, cat_url, categories)

proofs=[]
abstract_algebra = get_proofs(base_url + "/wiki/Category:Abstract_Algebra", "/wiki/Category:Abstract_Algebra")

# Insert Pythagoras's Theorem info into SQLite database
#try:
#    c.execute("INSERT INTO table_of_websites (titles, domain, html) VALUES(?, ?, ?)",(title, url, html))
#except sqlite3.IntegrityError:
#    print("Error, entry already exists")
# Repeatable code for putting in sqlite database

conn.commit()
conn.close()
