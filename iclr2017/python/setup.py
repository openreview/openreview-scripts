###############################################################################
# Setup python script takes as input the CSV files above and creates group for 
# ICLR.cc/2017/pc, areachairs, individual ACs, reviewers-invited, and creates 
# reviewers-invited.web Javascript for handling reviewer invitations; if they 
# accept, their email address is added to group ICLR.cc/2017/reviewers.
###############################################################################


import os, sys
import csv
import pydash
import requests

import params

sys.path.append('/Users/michaelspector/projects/openreview/or3scripts/')
print sys.path 
from client import *

import argparse
parser = argparse.ArgumentParser()
parser.add_argument('username', help="your OpenReview username (e.g. michael@openreview.net)")
parser.add_argument('password', help="your OpenReview password (e.g. abcd1234)")
parser.add_argument('programchairs', help="csv file containing the email addresses of the program chair(s)")
parser.add_argument('areachairs', help="csv file containing the email addresses of the area chairs")
parser.add_argument('reviewers', help="csv file containing the email addresses of the candidate reviewers")
args = parser.parse_args()

pcs_arg = args.programchairs
acs_arg = args.areachairs
reviewer_candidates_arg = args.reviewers

## Initialize the client library with username and password
or3 = client(args.username,args.password)

## Read in and save the program chairs, area chairs, and reviewer candidates from csv files
with open(pcs_arg, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        for email in row:
            params.iclr2017programchairs['members'].append(email)

with open(acs_arg, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        for email in row:
            params.iclr2017areaChairs['members'].append(email)

with open(reviewer_candidates_arg, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        for email in row:
            params.iclr2017reviewersInvited['members'].append(email)

print "program chairs: "+str(params.iclr2017programchairs['members'])
print "area chairs: "+str(params.iclr2017areaChairs['members'])
print "reviewers invited: "+str(params.iclr2017reviewersInvited['members'])


## Collect groups to be generated
groups = [  params.iclr,
            params.iclr2017,
            params.iclr2017programchairs,
            params.iclr2017areaChairs,
            params.iclr2017reviewers,
            params.iclr2017reviewersInvited,
            params.iclr2017reviewersDeclined,
            params.iclr2017conference
            ]

## Create groups for individual area chairs and add them to list of groups
for count, ac in enumerate(params.iclr2017areaChairs['members']):
    acGroup = {
        'id': params.iclr2017['id']+'/areachair'+str(count), #Note the singular form of "areachair"
        'signatures':[params.iclr2017areaChairs['id']],
        'writers':[params.iclr2017areaChairs['id']],
        'readers':['everyone'],
        'members': [ac],
        'signatories': [params.iclr2017areaChairs['id']+str(count), ac]
    }
    groups.append(acGroup)

## Post the groups
for g in groups:
    or3.set_group(g)

or3.add_group_member('host',params.iclr2017conference['id'])

## Collect invitations to be generated
invitations = [ or3.create_submission_invitation(params.subInvitationBody) ]

## Create 'request for availability to review' invitations

requestForReviewerId = params.iclr2017['id'] + '/-/request/to/review/invitation'
requestForReviewerBody = {
    'id': requestForReviewerId,
    'signatures': [params.iclr2017['id']],
    'writers': [params.iclr2017['id']],
    'readers': ['everyone'],
    'invitees': ['everyone'],
    'reply' : { 
        'readers': { 'values': ['everyone'] }, 
        'signatures': { 'values-regex': '\\(anonymous\\)' }, 
        'writers': { 'values-regex': '\\(anonymous\\)' }, 
        'content': {
            'email': {
                'order': 1,
                'value-regex': '\\S+@\\S+\\.\\S+',
                'description': 'Email address.'
            },
            'key': {
                'order': 2,
                'value-regex': '.{0,100}',
                'description': 'Email key hash'
            },
            'response': {
                'order': 3,
                'value-radio': ['Yes', 'No'],
                'description': 'Invitation response'
            }
        }
    }
}
with open('../process/submissionProcess_iclr2017.js') as f: 
    requestForReviewerBody['process'] = f.read()

with open('../webfield/web-field-invitation.html') as f: 
    requestForReviewerBody['web'] = f.read()
    
invitations.append(or3.create_base_invitation(requestForReviewerBody))

## Post the invitations
for i in invitations:
    or3.set_invitation(i)

## For each candidate reviewer, send an email asking them to confirm or reject the request to review
for count, reviewer in enumerate(params.iclr2017reviewersInvited['members']):
    print 'reviewer:' + str(reviewer)
    hashkey = or3.get_hash(reviewer, requestForReviewerId)
    print 'hash:' + str(hashkey)
    url = "http://localhost:3000/invitation?id=" + requestForReviewerId + "&email=" + reviewer + "&key=" + hashkey + "&response="
    message = "You have been invited to serve as a reviewer for the International Conference on Learning Representations (ICLR) 2017 Conference.\n\n"
    message = message+ "To ACCEPT the invitation, please click on the following link: \n\n"
    message = message+ url + "Yes\n\n"
    message = message+ "To DECLINE the invitation, please click on the following link: \n\n"
    message = message+ url + "No\n\n" + "Thank you"
    or3.send_mail("OpenReview invitation response", [reviewer], message)





## Post a sample note
or3.set_note(params.note1)




