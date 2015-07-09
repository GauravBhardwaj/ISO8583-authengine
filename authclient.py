
from ISO8583.ISO8583 import ISO8583
from ISO8583.ISOErrors import *
import socket
import sys
import time


class emulator:
    '''
    Connects and sends 8583 package with random account number and amount
    '''
    def __init__(self,serverip, port ):
        '''
        inititate the emulator with config parameters
        '''
        self.port = port
        self.serverip = serverip
        self.sock = None
        self.get_connection()

    def get_connection(self):
        '''
        get a socket connection to the auth server
        '''
        try:
            self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            #sock = socket.socket(af, socktype, proto)
            server_address = (self.serverip,self.port)
            self.sock.connect((server_address))
            print 'connected to %s port %s' % server_address

        except socket.error, msg:
                print "connection issue", msg



    def create_message(self, MTI, account_number, transaction_amount, message):
        '''
        Reads all the account number and creates a random amount transaction
        '''
        iso = ISO8583()
        iso.setMTI(MTI)
        #set the acoount number
        iso.setBit(2,account_number)
        #set the transaction amount
        iso.setBit(4,transaction_amount)
        iso.setBit(63,message)

        return iso

    def send_message(self, iso):
        '''
        '''
        message = iso.getNetworkISO()
        self.sock.send(message+"\n")
        #print ('Sending ... %s' % message)
