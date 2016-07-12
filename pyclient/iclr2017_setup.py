import os, sys
import csv

import client
import pydash
import requests
import iclr2017_params

pcs_arg = sys.argv[1]
acs_arg = sys.argv[2]
reviewer_candidates_arg = sys.argv[3]

## Read in and save the program chairs, area chairs, and reviewer candidates from csv files
with open(pcs_arg, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        for email in row:
            iclr2017_params.iclr2017programChairs['members'].append(email)

with open(acs_arg, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        for email in row:
            iclr2017_params.iclr2017areaChairs['members'].append(email)

with open(reviewer_candidates_arg, 'rb') as csvfile:
    reader = csv.reader(csvfile, delimiter=',', quotechar='|')
    for row in reader:
        for email in row:
            iclr2017_params.iclr2017reviewersInvited['members'].append(email)

print "program chairs: "+str(iclr2017_params.iclr2017programChairs['members'])
print "area chairs: "+str(iclr2017_params.iclr2017areaChairs['members'])
print "reviewers invited: "+str(iclr2017_params.iclr2017reviewersInvited['members'])





## Initialize the client library with username and password
or3 = client.client('OpenReview.net','12345678')





## Collect groups to be generated
groups = [  iclr2017_params.iclr,
            iclr2017_params.iclr2017,
            iclr2017_params.iclr2017programChairs,
            iclr2017_params.iclr2017areaChairs,
            iclr2017_params.iclr2017reviewers,
            iclr2017_params.iclr2017reviewersInvited,
            iclr2017_params.iclr2017reviewersDeclined,
            iclr2017_params.iclr2017conference
            ]

## Create groups for individual area chairs and add them to list of groups
for count, ac in enumerate(iclr2017_params.iclr2017areaChairs['members']):
    acGroup = {
        'id': iclr2017_params.iclr2017['id']+'/areachair'+str(count), #Note the singular form of "areachair"
        'signatures':[iclr2017_params.iclr2017areaChairs['id']],
        'writers':[iclr2017_params.iclr2017areaChairs['id']],
        'readers':['everyone'],
        'members': [ac],
        'signatories': [iclr2017_params.iclr2017areaChairs['id']+str(count), ac]
    }
    groups.append(acGroup)

## Post the groups
for g in groups:
    requests.post(or3.grpUrl, json=g, headers=or3.headers)
or3.addGroupMember('host',iclr2017_params.iclr2017conference['id'])





## Collect invitations to be generated
invitations = [ or3.createSubmissionInvitation(iclr2017_params.subInvitationBody) ]

## Create 'request for availability to review' invitations

requestForReviewerId = iclr2017_params.iclr2017['id'] + '/-/request/to/review/invitation'
requestForReviewerBody = {
    'id': requestForReviewerId,
    'signatures': [iclr2017_params.iclr2017['id']],
    'writers': [iclr2017_params.iclr2017['id']],
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
with open('./process/responseInvitationProcess_iclr2017.js') as f: 
    requestForReviewerBody['process'] = f.read()
with open('../iclr2017/web-field-invitation.html') as f:
    requestForReviewerBody['web'] = f.read()

invitations.append(or3.createBaseInvitation(requestForReviewerBody))

## Post the invitations
for i in invitations:
    requests.post(or3.inviteUrl, json=i, headers=or3.headers)

## For each candidate reviewer, send an email asking them to confirm or reject the request to review
for count, reviewer in enumerate(iclr2017_params.iclr2017reviewersInvited['members']):
    print 'reviewer:' + str(reviewer)
    hashKey = or3.createHash(reviewer, requestForReviewerId)
    print 'hash:' + str(hashKey)
    url = "http://localhost:3000/invitation?id=" + requestForReviewerId + "&email=" + reviewer + "&key=" + hashKey + "&response="
    message = "You have been invited to serve as a reviewer for the International Conference on Learning Representations (ICLR) 2017 Conference.\n\n"
    message = message+"To ACCEPT the invitation, please click on the following link: \n\n"
    message = message+url + "Yes\n\n"
    message = message+ "To DECLINE the invitation, please click on the following link: \n\n"
    message = message+ url + "No\n\n" + "Thank you"
    requests.post(or3.mailUrl, json={ 'groups': [reviewer], 'subject': "OpenReview invitation response" , 'message': message}, headers=or3.headers);





## Post a sample note
requests.post(or3.notesUrl, json=iclr2017_params.note1, headers=or3.headers)




