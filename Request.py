#!/usr/bin/python
import urllib2
import sqlite3

# Simple Request that sends the contents of Pythagoras's Theorem from SQLite
def do_request(req):
    # Connect to Database that already exists
    conn = sqlite3.connect("/home/chase/MobileProof/database/websites.sqlite")
    conn.text_factory = str
    c = conn.cursor()
    # Search database for Pythagoras's Theorem
    c.execute("SELECT html from table_of_websites where titles=?",("Pythagoras's Theorem",))
    # Send Response and close
    response = c.fetchone()
    conn.close()
    return response[0]

