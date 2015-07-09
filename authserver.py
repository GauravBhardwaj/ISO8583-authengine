"""

(C) Copyright 2009 Igor V. Custodio

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.

"""


from ISO8583.ISO8583 import ISO8583
from ISO8583.ISOErrors import *
from socket import *
import csv
import sys
import threading
import time


class authserver:

    def __init__(self, dict, port = 8583, serverip = ''):
        self.port = port
        self.serverip = serverip
        self.accountdetails_dict = dict
        self.sock = None

        thread = threading.Thread(target=self.run_server, args=())
        thread.daemon = True  # Daemonize thread
        thread.start()



    def run_server(self):
        '''
        Run the server on socket and accept connections
        '''
        #create socket
        self.sock = socket(AF_INET, SOCK_STREAM)
        #bind it on a port
        self.sock.bind(('', self.port))
        #accept maximum two connections from client
        self.sock.listen(2)


        while True:
            conn, address = self.sock.accept()
            while True:
                iso = conn.recv(2048)
                #print "Recieved isooooooooooooo", iso
                if iso:
                    pack = ISO8583()
                    #parse ISO
                    pack.setNetworkISO(iso)
                    if not pack.getMTI() == '0200':
    					#print "Cool, thats the format we are accepting connections in "
                        print ("PLease send the message MTI as 0200 ")




                    v1 = pack.getBitsAndValues()
    				#comment out this part, for debugging
                    accno, amt, srid = None, None, None
                    for v in v1:
                        #print ('Bit %s of type %s with value = %s' % (v['bit'],v['type'],v['value']))


                        if v['bit'] == '2' :
                            accno = v['value']
                        if v['bit'] == '4' :
                            amt = v['value']
                        if v['bit'] == '63' :
                            srid = v['value']
    					    #print ('Bit %s of type %s with value = %s' % (v['bit'],v['type'],v['value']))
                    #print accno, amt, srid


                    #accno = accno[2:]

                    if self.accountdetails_dict[accno[2:]] >= int(amt)/100.0 :
                        print "SerialId: ", srid[3:], " Account No.: ",accno[2:]," Available Balance: ",self.accountdetails_dict[accno[2:]]," Transaction Amount: ",str(int(amt)/100.0)," Status: ","Approved"
                    else:
                        print "SerialId: ", srid[3:], " Account No.: ",accno[2:]," Available Balance: ",self.accountdetails_dict[accno[2:]]," Transaction Amount: ",str(int(amt)/100.0)," Status: ","Rejected"



            

    def validate_transaction(self):
        '''
        Approves or denies a transaction by checking against suffucient funds
        '''
        pass




'''
# Configure the server
serverIP = "127.0.0.1"
serverPort = 8583
maxConn = 5
bigEndian = True
#bigEndian = False


# Create a TCP socket
s = socket(AF_INET, SOCK_STREAM)
# bind it to the server port
s.bind((serverIP, serverPort))
# Configure it to accept up to N simultaneous Clients waiting...
s.listen(maxConn)


# Run forever
while 1:
	#wait new Client Connection
	connection, address = s.accept()
	while 1:
		# receive message
		isoStr = connection.recv(2048)
		if isoStr:
			print ("\nInput ASCII |%s|" % isoStr)
			pack = ISO8583()
			#parse the iso
			try:
				if bigEndian:
					pack.setNetworkISO(isoStr)
				else:
					pack.setNetworkISO(isoStr,False)

				v1 = pack.getBitsAndValues()
				for v in v1:
					print ('Bit %s of type %s with value = %s' % (v['bit'],v['type'],v['value']))

				if pack.getMTI() == '0200':
					print ("\tThat's great !!! The client send a correct message !!!")
				else:
					print ("The client dosen't send the correct message!")
					break


			except InvalidIso8583, ii:
				print ii
				break
			except:
				print ('Something happened!!!!')
				break
            #send answer
            pack.setMTI('0210')
            pack.setBit(63,'This is sample response from server')
            if bigEndian:
                ans = pack.getNetworkISO()
            else:
                ans = pack.getNetworkISO(False)

			print ('Sending answer %s' % ans)
			connection.send(ans)

		else:
			break
	# close socket
	connection.close()
	print ("Closed...")
'''
