#!/usr/bin/python
from bs4 import BeautifulSoup
import urllib2

# Simple Request that sends the contents of Pythagoras's Theorem from proof
# wiki
def do_request(req):
    url = 'https://www.proofwiki.org/wiki/Pythagoras\'s_Theorem'
    req = urllib2.Request(url)
    response = urllib2.urlopen(req)
    the_page = response.read()
    soup = BeautifulSoup(str(the_page), 'html.parser')
    soup.prettify()
    return str(soup.find(id="content"))

