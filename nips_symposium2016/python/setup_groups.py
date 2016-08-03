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
from openreview import *

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('-p','--programchairs', help="csv file containing the email addresses of the program chair(s)")
parser.add_argument('-a','--areachairs', help="csv file containing the email addresses of the area chairs")
parser.add_argument('-r','--reviewers', help="csv file containing the email addresses of the candidate reviewers")
parser.add_argument('-u','--baseurl', help="base URL for the server to connect to")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    openreview = Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    openreview = Client(baseurl=args.baseurl)

nips            = Group('NIPS.cc',      
    signatories = ['NIPS.cc'], 
    writers     = ['OpenReview.net'], 
    members     = [],
    readers     = ['OpenReview.net'], 
    signatures  = ['OpenReview.net'])

nips_symposium  = Group('NIPS.cc/Symposium', 
    signatories = ['NIPS.cc/Symposium'], 
    writers     = ['NIPS.cc/Symposium'],  
    members     = [],
    readers     = ['NIPS.cc/Symposium'],       
    signatures  = ['NIPS.cc'])

nips_symposium2016 = Group('NIPS.cc/Symposium/2016',
    signatories = ['NIPS.cc/Symposium/2016'],
    writers     = ['NIPS.cc/Symposium','NIPS.cc/Symposium/2016'],
    members     = [],
    readers     = ['everyone'],
    web         = '../webfield/nips_symposium2016-webfield.html',
    signatures  = ['NIPS.cc/Symposium'])

nips_symposium2016pc = Group('NIPS.cc/Symposium/2016/PC', 
    signatories = ['NIPS.cc/Symposium/2016/PC'], 
    writers     = ['NIPS.cc/Symposium/2016'],
    members     = [],
    readers     = ['NIPS.cc/Symposium/2016','NIPS.cc/Symposium/2016/PC'], 
    signatures  = ['NIPS.cc/Symposium/2016'])

nips_symposium2016pc.add_member('spector@cs.umass.edu')

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
    openreview.post_group(g)



## Add the conference group to the host page
## NOTE: Should this be refactored into a "save to homepage" function or something like that?
openreview.post_group(openreview.get_group('host').add_member(nips_symposium2016))
