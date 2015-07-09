# define Configuration parameters, like server ports, ips
# Read the pre populated data from file
# Run the auth server with that pre-populated data
# Run the Transation emulator with random data
#
import authserver as authserver
import authclient as authclient
import util as util
import random as random


#constants
SERVER_IP = ''
SERVER_PORT = 8583
MAX_ATTEMPTS = 1
TIME_BETWEEN_RECONNECTS = 2 #seconds
IS_BIG_ENDIAN = True #
MTI = '0200'
FILE_NAME = 'MOCK_DATA.csv'

#populate account detials
accountdetails_dict = util.populate_accountdb(FILE_NAME)

#initialize the server
server = authserver.authserver(accountdetails_dict)

#initialize the emulator
emu = authclient.emulator(SERVER_IP,SERVER_PORT)

#create messages with random  amount against the account numbers from demo data
message = 1
for account_no, amt in accountdetails_dict.items():
    if len(account_no) <= 19:
        random_transaction_amount = random.randint(1,99999999)
        #print "account number is: ", account_no
        iso = emu.create_message(MTI, account_no, random_transaction_amount, str(message))
        emu.send_message(iso)
        message += 1
        if message == 200:
            break
