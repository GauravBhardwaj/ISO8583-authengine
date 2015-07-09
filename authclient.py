#create message
#open socket and connect on port and ip
#close socket


from ISO8583.ISO8583 import ISO8583
from ISO8583.ISOErrors import *
import socket
import sys
import time


class emulator:
    '''
    Connects and sends 8583 package with random account number and amount
    '''
    def __init__(self, port, serverip):
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
            server_address = (self.port, self.serverip)
            self.sock.connect(server_address)
            print 'connected to %s port %s' % server_address

        except socket.error, msg:
            print msg




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
        #print "senders isooooooooooooo",message
        self.sock.send(message+"\n")
        #print ('Sending ... %s' % message)






'''
# Configure the client
serverIP = "127.0.0.1"
serverPort = 8583
numberEcho = 1
timeBetweenEcho = 5 # in seconds

bigEndian = True
#bigEndian = False

s = None
for res in socket.getaddrinfo(serverIP, serverPort, socket.AF_UNSPEC, socket.SOCK_STREAM):
    af, socktype, proto, canonname, sa = res
    try:
		s = socket.socket(af, socktype, proto)
    except socket.error, msg:
	s = None
	continue
    try:
		s.connect(sa)
    except socket.error, msg:
	s.close()
	s = None
	continue
    break
if s is None:
    print ('Could not connect :('')
    sys.exit(1)



for req in range(0,numberEcho):
    iso = ISO8583(debug=True)
    iso.setMTI('0200')

    #set the acoount number
    iso.setBit(2,'1234567890123456789')
    #set the transaction amount
    iso.setBit(4,'13990')
    iso.setBit(63,'This is a Test Message')
    if bigEndian:
        try:

            message = iso.getNetworkISO()
            print ('The Message Type Indication is = %s' %iso.getMTI())
            print ('The Bitmap is = %s' %iso.getBitmap())
            iso.showIsoBits()
            print ('This is the ISO8583 complete package %s' % iso.getRawIso())
            print ('This is the ISO8583 complete package to sent over the TCPIP network %s' % iso.getNetworkISO())
            s.send(message)
            print ('Sending ... %s' % message)
            ans = s.recv(2048)
            print ("\nInput ASCII |%s|" % ans)
            isoAns = ISO8583()
            isoAns.setNetworkISO(ans)
            v1 = isoAns.getBitsAndValues()
            for v in v1:
                print ('Bit %s of type %s with value = %s' % (v['bit'],v['type'],v['value']))
            if isoAns.getMTI() == '0210':
                print ("\tThat's great !!! The server understand my message !!!")
            else:
                print ("The server dosen't understand my message!")

        except InvalidIso8583, ii:
            print ii
            break

        time.sleep(timeBetweenEcho)

    else:
		try:
			message = iso.getNetworkISO(False)
			s.send(message)
			print ('Sending ... %s' % message)
			ans = s.recv(2048)
			print ("\nInput ASCII |%s|" % ans)
			isoAns = ISO8583()
			isoAns.setNetworkISO(ans,False)
			v1 = isoAns.getBitsAndValues()
			for v in v1:
				print ('Bit %s of type %s with value = %s' % (v['bit'],v['type'],v['value']))

			if isoAns.getMTI() == '0810':
				print ("\tThat's great !!! The server understand my message !!!")
			else:
				print ("The server dosen't understand my message!")

		except InvalidIso8583, ii:
			print ii
			break

		time.sleep(timeBetweenEcho)



print ('Closing...')
s.close()
'''
