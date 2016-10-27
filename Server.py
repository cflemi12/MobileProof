#!/usr/bin/python

"""
Server class that creates a threaded server. 
@author Chase Fleming
"""

from ThreadingClass import ClientThread
import socket
import thread

SERVER_IP = '0.0.0.0'
SERVER_PORT = 12345

# Server class
class Server():

    # Initializes a new server
    def __init__(self):
        self.ip = SERVER_IP
        self.port = SERVER_PORT
        self.s = socket.socket()

    # Runs the server forever until keyboard interrupt.
    def run(self):
        self.s.bind((SERVER_IP, SERVER_PORT))
        threads = []
        print "Server listening at " + self.ip + ":" + str(self.port)
        try:
            while True:
                self.s.listen(5)
                c , addr = self.s.accept()
                newthread = ClientThread(c, addr)
                newthread.start()
                threads.append(newthread)
            for t in threads:
                t.join()
        except KeyboardInterrupt:
            print "\nKeyboard Interrupt Recieved. Shutting Down."

if __name__ == "__main__":
    MobileProofServer = Server()
    MobileProofServer.run()
