import csv
import sys
import random
import collections

def populate_accountdb(filename):
    '''
    Reads the csv file and creates a demo database of account number and names
    '''
    accountdetails_dict = collections.OrderedDict()

    with open(filename, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        for row in reader:
            accountdetails_dict[row[0]] = float(row[1])

    print "file reading done"
    return accountdetails_dict
