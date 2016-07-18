#!/usr/bin/python

###############################################################################
# Setup python script takes as input the CSV files above and creates group for 
# ICLR.cc/2017/pc, areachairs, individual ACs, reviewers-invited, and creates 
# reviewers-invited.web Javascript for handling reviewer invitations; if they 
# accept, their email address is added to group ICLR.cc/2017/reviewers.
###############################################################################



## Import statements and argument handling
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('username', help="your OpenReview username (e.g. michael@openreview.net)")
parser.add_argument('password', help="your OpenReview password (e.g. abcd1234)")
parser.add_argument('programchairs', help="csv file containing the email addresses of the program chair(s)")
parser.add_argument('areachairs', help="csv file containing the email addresses of the area chairs")
parser.add_argument('reviewers', help="csv file containing the email addresses of the candidate reviewers")
args = parser.parse_args()

import os, sys
import csv
import requests

sys.path.append('../..')
from client import *



## Read in and set the membership for program chairs, area chairs, and reviewer candidates from csv files
program_chairs = []
with open(args.programchairs, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        for email in row:
            program_chairs.append(email)
area_chairs = []
with open(args.areachairs, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        for email in row:
            area_chairs.append(email)
reviewers_invited = []
with open(args.reviewers, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        for email in row:
            reviewers_invited.append(email)

## Initialize the client library with username and password
or3 = Client(args.username,args.password)



## Initialize the groups
iclr                        = Group('ICLR.cc', writers=['OpenReview.net'])
iclr2017                    = Group('ICLR.cc/2017', readers=['everyone'], writers=['ICLR.cc'], web='../webfield/iclr2017_webfield.html')
iclr2017programchairs       = Group('ICLR.cc/2017/pc', readers=['everyone'], members=program_chairs)
iclr2017areachairs          = Group('ICLR.cc/2017/areachairs', readers=['everyone'], members=area_chairs)
iclr2017reviewers           = Group('ICLR.cc/2017/reviewers', readers=['everyone'])
iclr2017reviewersinvited    = Group('ICLR.cc/2017/reviewers-invited', readers=['ICLR.cc/2017/pc','ICLR.cc/2017'], members=reviewers_invited)
iclr2017reviewersdeclined   = Group('ICLR.cc/2017/reviewers-declined', readers=['ICLR.cc/2017/pc'])
iclr2017conference          = Group('ICLR.cc/2017/conference', readers=['everyone'], members=['ICLR.cc/2017/pcs','ICLR.cc/2017/areachairs'], web='../webfield/iclr2017conference_webfield.html')
iclr2017workshop            = Group('ICLR.cc/2017/workshop', readers=['everyone'], members=['ICLR.cc/2017/pcs','ICLR.cc/2017/areachairs'], web='../webfield/iclr2017workshop_webfield.html')
groups = [iclr, iclr2017, iclr2017programchairs, iclr2017areachairs, iclr2017reviewers, iclr2017reviewersinvited, iclr2017reviewersdeclined, iclr2017conference, iclr2017workshop]

## Create groups for individual area chairs and add them to the groups dict
for count, ac in enumerate(iclr2017areachairs.body['members']):
    acgroup = Group('ICLR.cc/2017/areachair'+str(count), 
                    writers=['ICLR.cc/2017/areachairs'],
                    readers=['everyone'],
                    members=[ac])
    print "Adding area chair "+str(ac)+" as a member of group ICLR.cc/2017/areachair"+str(count)
    groups.append(acgroup)

## Post the groups
for g in groups:
    print "Posting group: "+g.body['id']
    or3.set_group(g.body)



## Add the conference group to the home page
or3.add_group_member('host',iclr2017.body['id'])
