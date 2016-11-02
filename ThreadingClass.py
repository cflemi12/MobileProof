#!/usr/bin/python

"""
A threaded client class for MobileProof application.
@author Chase Fleming
"""

import socket
from threading import Thread
from Request import do_request
import logging

# Multithreaded Python socket server. 
class ClientThread(Thread):

    # Initializes a new client to be threaded
    def __init__(self, sock, addr):
        Thread.__init__(self)
        self.clientsock = sock 
        self.ip = addr[0]
        self.port = addr[1]
        logging.info("New socket thread for "+self.ip+":"+str(self.port))

    # The request handler for each threaded client
    def run(self):
        try:
            data = self.clientsock.recv(1024)
            logging.info("Request recieved: "+ data.strip())
            resp = do_request(data)
            self.clientsock.send(resp+'\n')
            self.clientsock.close()
        except IOError as e:
            if e.errno == errno.EPIPE:
                logging.info("Borken Pipe. Client closed connection.")
