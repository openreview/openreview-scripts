#!/usr/bin/python

###############################################################################
# Setup python script takes as input the CSV files above and creates group for 
# ICLR.cc/2016/pc, areachairs, individual ACs, reviewers-invited, and creates 
# reviewers-invited.web Javascript for handling reviewer invitations; if they 
# accept, their email address is added to group ICLR.cc/2016/reviewers.
###############################################################################

## Import statements
import argparse
import csv
import sys
sys.path.append('../..')
from client import *

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('-p','--programchairs', help="csv file containing the email addresses of the program chair(s)")
parser.add_argument('-a','--areachairs', help="csv file containing the email addresses of the area chairs")
parser.add_argument('-r','--reviewers', help="csv file containing the email addresses of the candidate reviewers")
parser.add_argument('-u','--baseurl', help="base URL for the server to connect to")
args = parser.parse_args()

## Initialize the client library with username and password

openreview = Client(config='./nips_symposium2016_config.ini')

nips            = Group('NIPS',      
    signatories = ['NIPS'], 
    writers     = ['OpenReview.net'], 
    members     = [],
    readers     = ['OpenReview.net'], 
    signatures  = ['OpenReview.net'])

nips_symposium  = Group('NIPS/Symposium', 
    signatories = ['NIPS/Symposium'], 
    writers     = ['NIPS/Symposium'],  
    members     = [],
    readers     = ['NIPS/Symposium'],       
    signatures  = ['NIPS'])

nips_symposium2016  = Group('NIPS/Symposium/2016',
    signatories = ['NIPS/Symposium/2016'],
    writers     = ['NIPS/Symposium/2016'],
    members     = [],
    readers     = ['everyone'],
    web         = '../webfield/nips_symposium2016-webfield.html',
    signatures  = ['NIPS/Symposium'])

nips_symposium2016pc  = Group('NIPS/Symposium/2016/PC', 
    signatories = ['NIPS/Symposium/2016/PC'], 
    writers     = ['NIPS/Symposium/2016'],
    members     = [],
    readers     = ['NIPS/Symposium/2016/PC'], 
    signatures  = ['NIPS/Symposium/2016'])

groups = [nips, nips_symposium, nips_symposium2016, nips_symposium2016pc]

## Read in a csv file with the names of the program chair(s).
## Each name in the csv will be set as a member of ICLR.cc/2016/pc
if args.programchairs != None:
    program_chairs = []
    
    with open(args.programchairs, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            for email in row:
                nips_symposium2016pc.add_member(email)
    groups.append(nips_symposium2016pc)


## Post the groups
for g in groups:
    print "Posting group: "+g.id
    openreview.save_group(g)



## Add the conference group to the host page
## NOTE: Should this be refactored into a "save to homepage" function or something like that?
openreview.save_group(openreview.get_group('host').add_member(nips_symposium2016))
