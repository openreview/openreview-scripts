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

nips_2016  = Group('NIPS.cc/2016', 
    signatories = ['NIPS.cc/2016'], 
    writers     = ['NIPS.cc/2016'],  
    members     = [],
    readers     = ['NIPS.cc/2016'],       
    signatures  = ['NIPS.cc'])

nips_2016symposium = Group('NIPS.cc/2016/Deep_Learning_Symposium',
    signatories = ['NIPS.cc/2016/Deep_Learning_Symposium'],
    writers     = ['NIPS.cc/2016','NIPS.cc/2016/Deep_Learning_Symposium'],
    members     = [],
    readers     = ['everyone'],
    web         = '../webfield/nips_symposium2016-webfield.html',
    signatures  = ['NIPS.cc/2016'])

nips_2016symposiumpc = Group('NIPS.cc/2016/Deep_Learning_Symposium/PC', 
    signatories = ['NIPS.cc/2016/Deep_Learning_Symposium/PC','spector@cs.umass.edu'], 
    writers     = ['NIPS.cc/2016/Deep_Learning_Symposium'],
    members     = [],
    readers     = ['NIPS.cc/2016/Deep_Learning_Symposium','NIPS.cc/2016/Deep_Learning_Symposium/PC'], 
    signatures  = ['NIPS.cc/2016/Deep_Learning_Symposium'])

nips_2016symposiumpc.add_member('spector@cs.umass.edu')
nips_2016symposiumpc.add_member('rgrosse@cs.toronto.edu')
nips_2016symposiumpc.add_member('ndjaitly@gmail.com')
nips_2016symposiumpc.add_member('mccallum@cs.umass.edu')


groups = [nips, nips_2016, nips_2016symposium, nips_2016symposiumpc]

## Read in a csv file with the names of the program chair(s).
## Each name in the csv will be set as a member of ICLR.cc/2016/pc
if args.programchairs != None:
    program_chairs = []
    
    with open(args.programchairs, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            for email in row:
                nips_2016symposiumpc.add_member(email)
    groups.append(nips_2016symposiumpc)


## Post the groups
for g in groups:
    print "Posting group: "+g.id
    openreview.post_group(g)



## Add the conference group to the host page
## NOTE: Should this be refactored into a "save to homepage" function or something like that?
openreview.post_group(openreview.get_group('host').add_member(nips_2016symposium))
