#!/usr/bin/python

"""
Setup python script takes as input the CSV files above and creates group for 
ICLR.cc/2017/pc, areachairs, individual ACs, reviewers-invited, and creates 
reviewers-invited.web Javascript for handling reviewer invitations; if they 
accept, their email address is added to group ICLR.cc/2017/reviewers.

"""

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
parser.add_argument('-o','--overwrite', help="the ID of a group to overwrite")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    openreview = Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    openreview = Client(baseurl=args.baseurl)

groups = []
overwrite_group = args.overwrite if args.overwrite!=None else '';

def allow_overwrite(group_id):

    if (group_id and overwrite_group.lower()==group_id.lower()) or (type(openreview.get_group(group_id)!=Group))==True:
        return True
    else:
        return False

if openreview.user['id'].lower()=='openreview.net':
    
    #########################
    ##    SETUP GROUPS     ##
    ######################### 

    if allow_overwrite('ICLR.cc'):
        iclr            = Group('ICLR.cc',      
            readers     = ['OpenReview.net'], 
            writers     = ['OpenReview.net','ICLR.cc/2017/pcs'], 
            signatures  = ['OpenReview.net'], 
            signatories = ['ICLR.cc','ICLR.cc/2017/pcs'], 
            members     = [] )
        groups.append(iclr)

    if allow_overwrite('ICLR.cc/2017'):
        iclr2017        = Group('ICLR.cc/2017', 
            readers     = ['everyone'],       
            writers     = ['ICLR.cc','ICLR.cc/2017','ICLR.cc/2017/pcs'],  
            signatures  = ['ICLR.cc'], 
            signatories = ['ICLR.cc/2017','ICLR.cc/2017/pcs'], 
            members     = ['ICLR.cc/2017/pcs'], 
            web         = '../webfield/iclr2017_webfield.html')
        groups.append(iclr2017)

    if allow_overwrite('ICLR.cc/2017/conference'):
        iclr2017conference = Group('ICLR.cc/2017/conference', 
            readers     = ['everyone'], 
            writers     = ['ICLR.cc/2017','ICLR.cc/2017/conference','ICLR.cc/2017/pcs'], 
            signatures  = ['ICLR.cc/2017'],
            signatories = ['ICLR.cc/2017/conference','ICLR.cc/2017/pcs'], 
            members     = ['ICLR.cc/2017/pcs'],  
            web         = '../webfield/iclr2017conference_webfield.html')
        groups.append(iclr2017conference)

    if allow_overwrite('ICLR.cc/2017/conference/organizers'):
        iclr2017conferenceorganizers = Group('ICLR.cc/2017/conference/organizers',
            readers     = ['everyone'], 
            writers     = ['ICLR.cc/2017/conference','ICLR.cc/2017/conference/organizers','ICLR.cc/2017/pcs'], 
            signatures  = ['ICLR.cc/2017/conference'],
            signatories = ['ICLR.cc/2017/conference','ICLR.cc/2017/pcs', 'ICLR.cc/2017/conference/organizers'], 
            members     = ['ICLR.cc/2017/pcs','ICLR.cc/2017/conference'])
        groups.append(iclr2017conferenceorganizers)

    if allow_overwrite('ICLR.cc/2017/conference/ACs_and_organizers'):
        iclr2017conferenceACsOrganizers = Group('ICLR.cc/2017/conference/ACs_and_organizers',
            readers     = ['everyone'],
            writers     = ['ICLR.cc/2017/conference','ICLR.cc/2017/conference/ACs_and_organizers','ICLR.cc/2017/pcs'],
            signatures  = ['ICLR.cc/2017/conference'],
            signatories = ['ICLR.cc/2017/conference','ICLR.cc/2017/pcs','ICLR.cc/2017/conference/ACs_and_organizers'],
            members     = ['ICLR.cc/2017/pcs','ICLR.cc/2017/areachairs','ICLR.cc/2017/conference']
            )
        groups.append(iclr2017conferenceACsOrganizers)

    if allow_overwrite('ICLR.cc/2017/conference/reviewers_and_ACS_and_organizers'):
        iclr2017reviewersACsOrganizers = Group('ICLR.cc/2017/conference/reviewers_and_ACS_and_organizers',
            readers     = ['everyone'],
            writers     = ['ICLR.cc/2017/conference','ICLR.cc/2017/conference/reviewers_and_ACS_and_organizers','ICLR.cc/2017/pcs'],
            signatures  = ['ICLR.cc/2017/conference'],
            signatories = ['ICLR.cc/2017/conference','ICLR.cc/2017/pcs','ICLR.cc/2017/conference/reviewers_and_ACS_and_organizers'],
            members     = ['ICLR.cc/2017/pcs','ICLR.cc/2017/areachairs','ICLR.cc/2017/conference/reviewers','ICLR.cc/2017/conference']
            )
        groups.append(iclr2017reviewersACsOrganizers)

    if allow_overwrite('ICLR.cc/2017/workshop'):
        iclr2017workshop = Group('ICLR.cc/2017/workshop', 
            readers     = ['everyone'],
            writers     = ['ICLR.cc/2017','ICLR.cc/2017/pcs'],
            signatures  = ['ICLR.cc/2017'], 
            signatories = ['ICLR.cc/2017/workshop'],
            members     = ['ICLR.cc/2017/pcs','ICLR.cc/2017/areachairs'], 
            web         = '../webfield/iclr2017workshop_webfield.html')
        groups.append(iclr2017workshop)

    openreview.post_group(openreview.get_group('host').add_member('ICLR.cc/2017'))

    ## Read in a csv file with the names of the program chair(s).
    ## Each name in the csv will be added as a member of ICLR.cc/2017/pc
    new_program_chairs = []
    if args.programchairs != None: 
        with open(args.programchairs, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                for email in row:
                    new_program_chairs.append(email)

    iclr2017programchairs = openreview.get_group('ICLR.cc/2017/pcs')
    if allow_overwrite('ICLR.cc/2017/pcs'):
        'creating new group for PCs'
        iclr2017programchairs = Group('ICLR.cc/2017/pcs', 
                                    readers=['everyone'], 
                                    writers=['ICLR.cc/2017','ICLR.cc/2017/pcs'],
                                    signatures=['ICLR.cc/2017'],
                                    signatories=['ICLR.cc/2017/pcs'],
                                    members=new_program_chairs)
        groups.append(iclr2017programchairs)
    else:
        if new_program_chairs != []:
            iclr2017programchairs.members += new_program_chairs
            groups.append(iclr2017programchairs)



    ## Read in a csv file with the names of the area chairs.
    new_areachair_members = []
    if args.areachairs != None:
        with open(args.areachairs, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                for email in row:
                    new_areachair_members.append(email)

    iclr2017areachairs = openreview.get_group('ICLR.cc/2017/areachairs')
    if allow_overwrite('ICLR.cc/2017/areachairs'):
        iclr2017areachairs = Group('ICLR.cc/2017/areachairs', 
                                    readers=['everyone'],
                                    writers=['ICLR.cc/2017','ICLR.cc/2017/pcs'],
                                    signatures=['ICLR.cc/2017'],
                                    signatories=['ICLR.cc/2017/areachairs'],
                                    members=new_areachair_members)
        groups.append(iclr2017areachairs)
    else:
        if new_areachair_members != []:
            iclr2017areachairs.members += new_areachair_members
            groups.append(iclr2017areachairs)


    ## Read in a csv file with the names of the reviewers.
    ## Each name will be set as a member of ICLR.cc/2017/reviewers-invited.
    ## groups for 'reviewers' and for 'reviewers-declined' are also generated, but are not yet populated with members.


    reviewers_invited = []
    if args.reviewers != None:    
        with open(args.reviewers, 'rb') as csvfile:
            reader = csv.reader(csvfile, delimiter=',', quotechar='|')
            for row in reader:
                for email in row:
                    reviewers_invited.append(email)

    iclr2017reviewersinvited = openreview.get_group('ICLR.cc/2017/conference/reviewers-invited')

    if allow_overwrite('ICLR.cc/2017/conference/reviewers-invited'):
        iclr2017reviewersinvited    = Group('ICLR.cc/2017/conference/reviewers-invited', 
                                            readers=['ICLR.cc/2017/pcs','ICLR.cc/2017'], 
                                            writers=['ICLR.cc/2017/pcs'],
                                            signatures=['ICLR.cc/2017/pcs'],
                                            signatories=['ICLR.cc/2017/conference/reviewers-invited'],
                                            members=reviewers_invited)
        groups.append(iclr2017reviewersinvited)
    else:
        if reviewers_invited != []:
            iclr2017reviewersinvited.members += reviewers_invited;
            groups.append(iclr2017reviewersinvited)


    if allow_overwrite('ICLR.cc/2017/conference/reviewers'):
        iclr2017reviewers = Group('ICLR.cc/2017/conference/reviewers', 
                                            readers=['everyone'],
                                            writers=['ICLR.cc/2017/conference','ICLR.cc/2017/pcs'],
                                            signatures=['ICLR.cc/2017/conference'],
                                            signatories=['ICLR.cc/2017/conference/reviewers'],
                                            members=[])
        groups.append(iclr2017reviewers)

    if allow_overwrite('ICLR.cc/2017/conference/reviewers-declined'):
        iclr2017reviewersdeclined   = Group('ICLR.cc/2017/conference/reviewers-declined',
                                            readers=['everyone'],
                                            writers=['ICLR.cc/2017/conference','ICLR.cc/2017/pcs'],
                                            signatures=['ICLR.cc/2017/conference'],
                                            signatories=['ICLR.cc/2017/conference/reviewers'],
                                            members=[])
        groups.append(iclr2017reviewersdeclined)


    ## Post the groups
    for g in groups:
        print "Posting group: ",g.id
        openreview.post_group(g)





    #########################
    ##  SETUP INVITATIONS  ##
    ######################### 


    ## Create the submission invitation
    reply = {
        'forum': None,
        'parent': None,
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values': ['everyone']
        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values-regex': '~.*'
        },
        'writers': {
            'values-regex': '~.*'
        },
        'content': {
            'title': {
                'description': 'Title of paper.',
                'order': 1,
                'value-regex': '.{1,100}',
                'required':True
            },
            'authors': {
                'description': 'Comma separated list of author names, as they appear in the paper.',
                'order': 2,
                'value-regex': '[^,\\n]+(,[^,\\n]+)*',
                'required':True
            },
            'author_emails': {
                'description': 'Comma separated list of author email addresses, in the same order as above.',
                'order': 3,
                'value-regex': '[^,\\n]+(,[^,\\n]+)*',
                'required':True
            },
            'TL;DR': {
                'description': '\"Too Long; Didn\'t Read\": a short sentence describing your paper',
                'order': 3,
                'value-regex': '[^\\n]{0,250}',
                'required':False
            },
            'abstract': {
                'description': 'Abstract of paper.',
                'order': 4,
                'value-regex': '[\\S\\s]{1,5000}',
                'required':True
            },
            'pdf': {
                'description': 'Either upload a PDF file or provide a direct link to your PDF on ArXiv (link must begin with http(s) and end with .pdf)',
                'order': 5,
                'value-regex': 'upload|(http|https):\/\/.+\.pdf',
                'required':True
            },
            'keywords': {
                'description': 'Comma separated list of keywords.',
                'order': 6,
                'values-dropdown': [
                    'Theory',
                    'Computer vision',
                    'Speech',
                    'Natural language processing',
                    'Deep learning',
                    'Unsupervised Learning',
                    'Supervised Learning',
                    'Semi-Supervised Learning',
                    'Reinforcement Learning',
                    'Transfer Learning',
                    'Multi-modal learning',
                    'Applications',
                    'Optimization',
                    'Structured prediction',
                    'Games'
                ]

            },
            'conflicts': {
                'description': 'Semi-colon separated list of email domains of people who would have a conflict of interest in reviewing this paper, (e.g., cs.umass.edu;google.com, etc.).',
                'order': 100,
                'value-regex': '([a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*)(\;[a-zA-Z0-9]+(\.[a-zA-Z0-9]+)*)*',
                'required':True
            }
        }
    }

    submission_reply=reply.copy()
    submission_reply['referenti']=['ICLR.cc/2017/conference/-/reference']

    submission_invitation = Invitation( 'ICLR.cc/2017/conference',
        'submission', 
        readers=['everyone'], 
        writers=['ICLR.cc/2017/conference'],
        invitees=['~'], 
        signatures=['ICLR.cc/2017/pcs'], 
        reply=submission_reply,
        #duedate=1873772215,
        process='../process/submissionProcess_iclr2017.js')

    reference_reply=reply.copy()

    reference_invitation = Invitation('ICLR.cc/2017/conference',
        'reference',
        readers=['everyone'], 
        writers=['ICLR.cc/2017/conference'],
        invitees=['~'], 
        signatures=['ICLR.cc/2017/pcs'], 
        reply=reference_reply)


    ## Create 'request for availability to review' invitation
    reviewer_invitation_reply = {
        'content': {
            'email': {
                'description': 'Email address.',
                'order': 1,
                'value-regex': '\\S+@\\S+\\.\\S+'
            },
            'key': {
                'description': 'Email key hash',
                'order': 2,
                'value-regex': '.{0,100}'
            },
            'response': {
                'description': 'Invitation response',
                'order': 3,
                'value-radio': ['Yes', 'No']
            }
        },
        'readers': {
            'values': ['everyone']
        },
        'signatures': {
            'values-regex': '\\(anonymous\\)'
        },
        'writers': {
            'values-regex': '\\(anonymous\\)'
        }
    }

    reviewer_invitation = Invitation('ICLR.cc/2017/conference',
                                    'reviewer_invitation', 
                                    readers=['everyone'],
                                    writers=['ICLR.cc/2017/conference'], 
                                    invitees=['everyone'],
                                    signatures=['ICLR.cc/2017/conference'], 
                                    reply=reviewer_invitation_reply, 
                                    process='../process/responseInvitationProcess_iclr2017.js', 
                                    web='../webfield/web-field-invitation.html')

    invitations = [submission_invitation, reference_invitation, reviewer_invitation]

    ## Post the invitations
    for i in invitations:
        print "Posting invitation: "+i.id
        openreview.post_invitation(i)



else:
    print "Aborted. User must be Super User."
