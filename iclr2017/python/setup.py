#!/usr/bin/python

###############################################################################
# Setup python script takes as input the CSV files above and creates group for 
# ICLR.cc/2017/pc, areachairs, individual ACs, reviewers-invited, and creates 
# reviewers-invited.web Javascript for handling reviewer invitations; if they 
# accept, their email address is added to group ICLR.cc/2017/reviewers.
###############################################################################

## Import statements
import argparse
import csv
import getpass
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
username = raw_input("OpenReview username (e.g. username@umass.edu): ")
password = getpass.getpass()
if args.baseurl != None:
    or3 = Client(username,password, baseurl=args.baseurl)
else:
    or3 = Client(username,password)



## Initialize the groups list
iclr                        = Group('ICLR.cc',      
                                    readers=['OpenReview.net'], 
                                    writers=['OpenReview.net'], 
                                    signatures=['OpenReview.net'], 
                                    signatories=['ICLR.cc'], 
                                    members=[])
iclr2017                    = Group('ICLR.cc/2017', 
                                    readers=['everyone'],       
                                    writers=['ICLR.cc','ICLR.cc/2017','ICLR.cc/2017/pcs'],  
                                    signatures=['ICLR.cc'], 
                                    signatories=['ICLR.cc/2017','ICLR.cc/2017/pcs'], 
                                    members=[], 
                                    web='../webfield/iclr2017_webfield.html')
iclr2017conference          = Group('ICLR.cc/2017/conference', 
                                    readers=['everyone'], 
                                    writers=['ICLR.cc/2017','ICLR.cc/2017/conference','ICLR.cc/2017/pcs'], 
                                    signatures=['ICLR.cc/2017'],
                                    signatories=['ICLR.cc/2017/conference','ICLR.cc/2017/pcs'], 
                                    members=['ICLR.cc/2017/pcs','ICLR.cc/2017/areachairs'],  
                                    web='../webfield/iclr2017conference_webfield.html')
iclr2017workshop            = Group('ICLR.cc/2017/workshop', 
                                    readers=['everyone'],
                                    writers=['ICLR.cc/2017'],
                                    signatures=['ICLR.cc/2017'], 
                                    signatories=['ICLR.cc/2017/workshop'],
                                    members=['ICLR.cc/2017/pcs','ICLR.cc/2017/areachairs'], 
                                    web='../webfield/iclr2017workshop_webfield.html')
groups = [iclr, iclr2017, iclr2017conference, iclr2017workshop]


## Read in a csv file with the names of the program chair(s).
## Each name in the csv will be set as a member of ICLR.cc/2017/pc
if args.programchairs != None:
    program_chairs = []
    
    with open(args.programchairs, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            for email in row:
                program_chairs.append(email)

    iclr2017programchairs = Group('ICLR.cc/2017/pcs', readers=['everyone'], members=program_chairs, signatories=program_chairs)
    groups.append(iclr2017programchairs)


## Read in a csv file with the names of the area chairs.
## Each row of names will be assigned as a member of a single area chair.
## E.g. if the first row contains "john@openreview.net,sally@openreview.net", then john and sally will both be members of ICLR.cc/2017/areachair0
if args.areachairs != None:
    all_areachair_members = []
    areachair_subgroups = []
    with open(args.areachairs, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            areachair_subgroup_members = []
            for email in row:
                all_areachair_members.append(email)
                areachair_subgroup_members.append(email)
            areachair_subgroups.append(areachair_subgroup_members)

    iclr2017areachairs = Group('ICLR.cc/2017/areachairs', readers=['everyone'], members=all_areachair_members)
    groups.append(iclr2017areachairs)
    
    # Note the singular form "areachair" below; these groups are descendants of ICLR.cc/2017, not ICLR.cc/2017/areachairs, and serve as 
    # anonymizing wrappers for posting notes.
    for count, members in enumerate(areachair_subgroups):
        acgroup = Group('ICLR.cc/2017/areachair'+str(count),
                        readers=['everyone'],
                        writers=['ICLR.cc/2017/areachairs'],
                        signatories=members,
                        signatures=['ICLR.cc/2017/areachairs'],
                        members=members
                        )
        print "Adding members "+str(members)+" as a member of group ICLR.cc/2017/areachair"+str(count)
        groups.append(acgroup)


## Read in a csv file with the names of the reviewers.
## Each name will be set as a member of ICLR.cc/2017/reviewers-invited.
## groups for 'reviewers' and for 'reviewers-declined' are also generated, but are not yet populated with members.
if args.reviewers != None:
    reviewers_invited = []
    
    with open(args.reviewers, 'rb') as csvfile:
        reader = csv.reader(csvfile, delimiter=',', quotechar='|')
        for row in reader:
            for email in row:
                reviewers_invited.append(email)
    
    iclr2017reviewersinvited    = Group('ICLR.cc/2017/conference/reviewers-invited', 
                                        readers=['ICLR.cc/2017/pcs','ICLR.cc/2017'], 
                                        writers=['ICLR.cc/2017/pcs'],
                                        signatures=['ICLR.cc/2017/pcs'],
                                        signatories=['ICLR.cc/2017/conference/reviewers-invited'],
                                        members=reviewers_invited)
    iclr2017reviewers           = Group('ICLR.cc/2017/conference/reviewers', 
                                        readers=['everyone'],
                                        writers=['ICLR.cc/2017/conference'],
                                        signatures=['ICLR.cc/2017/conference'],
                                        signatories=['ICLR.cc/2017/conference/reviewers'],
                                        members=[])
    iclr2017reviewersdeclined   = Group('ICLR.cc/2017/conference/reviewers-declined',
                                        readers=['everyone'],
                                        writers=['ICLR.cc/2017/conference'],
                                        signatures=['ICLR.cc/2017/conference'],
                                        signatories=['ICLR.cc/2017/conference/reviewers'],
                                        members=[])
    groups = groups+[iclr2017reviewersinvited, iclr2017reviewers, iclr2017reviewersdeclined]




## Post the groups
for g in groups:
    print "Posting group: "+g.body['id']
    or3.set_group(g.body)



## Add the conference group to the home page
or3.add_group_member('host',iclr2017.body['id'])
