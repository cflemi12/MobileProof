#!/usr/bin/python

"""
Server class that creates a threaded server. 
@author Chase Fleming
"""

from ThreadingClass import ClientThread
import socket
import thread
import sys
import logging

SERVER_IP = '0.0.0.0'
SERVER_PORT = 12345

# Server class
class Server():

    # Initializes a new server
    def __init__(self, passedPort=12345, passedIP='0.0.0.0'):
        self.ip = passedIP
        self.port = passedPort
        self.s = socket.socket()

    # Runs the server forever until keyboard interrupt.
    def run(self):
        self.s.bind((SERVER_IP, SERVER_PORT))
        threads = []
        logging.info("Listening at " + self.ip + ":" + str(self.port))
        try:
            while True:
                self.s.listen(5)
                c , addr = self.s.accept()
                newthread = ClientThread(c, addr)
                newthread.start()
                threads.append(newthread)
            for t in threads:
                t.join()
        except:
            self.s.close()
            e = sys.exc_info()[0]
            logging.info(str(e))
            logging.info("Stopping server!")
            return

if __name__ == "__main__":
    logging.basicConfig(filename="mobileproof.log", level=logging.INFO)
    try:
        logging.info('Started.')
        MobileProofServer = Server()
        MobileProofServer.run()
    except:
        e = sys.exc_info()[0]
        logging.info(str(e))
        logging.info("Stopping server.")
        sys.exit()
