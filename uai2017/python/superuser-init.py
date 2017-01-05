#!/usr/bin/python

"""
This is the initialization script for UAI 2017.

It should only be run ONCE to kick off the conference. It can only be run by the Super User.

"""

## Import statements
import argparse
import csv
import sys
from openreview import *
from uaidata import *

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--overwrite', help="If set to true, overwrites existing groups")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    openreview = Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    openreview = Client(baseurl=args.baseurl)

groups = []
overwrite = True if (args.overwrite!=None and args.overwrite.lower()=='true') else False
def overwrite_allowed(groupid):
    if not openreview.exists(groupid) or overwrite==True:
        return True
    else:
        return False

if openreview.user['id'].lower()=='openreview.net':

    #########################
    ##    SETUP GROUPS     ##
    #########################

    if overwrite_allowed('auai.org'):
        auai = Group('auai.org',
            readers     = ['everyone'],
            writers     = ['OpenReview.net'],
            signatures  = ['OpenReview.net'],
            signatories = [],
            members     = [] )
        groups.append(auai)


    if overwrite_allowed('auai.org/UAI'):
        uai = Group('auai.org/UAI',
            readers     = ['everyone'],
            writers     = ['OpenReview.net'],
            signatures  = ['OpenReview.net'],
            signatories = [],
            members     = [] )
        groups.append(uai)


    if overwrite_allowed('auai.org/UAI/2017'):
        uai2017 = Group('auai.org/UAI/2017',
            readers     = ['everyone'],
            writers     = ['auai.org/UAI/2017'],
            signatures  = ['OpenReview.net'],
            signatories = ['auai.org/UAI/2017'],
            members     = [],
            web         = '../webfield/uai2017_webfield.html')
        groups.append(uai2017)


    if overwrite_allowed('auai.org/UAI/2017/Chairs'):
        Program_Chairs = Group('auai.org/UAI/2017/Chairs',
            readers     = ['everyone'],
            writers     = ['OpenReview.net','auai.org/UAI/2017/Chairs'],
            signatures  = ['OpenReview.net'],
            signatories = ['auai.org/UAI/2017/Chairs'],
            members     = ["~Alejandro_Molina1","~Kristian_Kersting1","~Gal_Elidan1"]) #should include Gal and Kristian
        groups.append(Program_Chairs)


    if overwrite_allowed('auai.org/UAI/2017/SPC'):
        spc = Group('auai.org/UAI/2017/SPC',
            readers     = ['everyone'], #it should be broadly known who is a member of the Senior Program Committee
            writers     = ['auai.org/UAI/2017/Chairs','auai.org/UAI/2017'], #the conference needs to be a writer whenever the process functions need to modify the group
            signatures  = ['auai.org/UAI/2017/Chairs'],
            signatories = ['auai.org/UAI/2017/Chairs'], #it seems like only Gal and Kristian should be able to write notes representing the whole SPC
            members     = ['auai.org/UAI/2017/Chairs']) #more to be added later, from the list of SPC members
        groups.append(spc)

    if overwrite_allowed('auai.org/UAI/2017/SPC/invited'):
        spc_invited = Group('auai.org/UAI/2017/SPC/invited',
            readers     = ['auai.org/UAI/2017/Chairs','auai.org/UAI/2017'], #it should *NOT* be broadly known who was invited
            writers     = ['auai.org/UAI/2017/Chairs','auai.org/UAI/2017'],
            signatures  = ['auai.org/UAI/2017/Chairs'],
            signatories = [],
            members     = []) #more to be added later from the SPC invitation process
        groups.append(spc_invited)

    if overwrite_allowed('auai.org/UAI/2017/SPC/declined'):
        spc_declined = Group('auai.org/UAI/2017/SPC/declined',
            readers     = ['auai.org/UAI/2017/Chairs','auai.org/UAI/2017'], #it should *NOT* be broadly known who declined
            writers     = ['auai.org/UAI/2017/Chairs','auai.org/UAI/2017'],
            signatures  = ['auai.org/UAI/2017/Chairs'],
            signatories = [],
            members     = []) #more to be added later from the SPC invitation process
        groups.append(spc_declined)

    if overwrite_allowed('auai.org/UAI/2017/SPC/emailed'):
        spc_emailed = Group('auai.org/UAI/2017/SPC/emailed',
            readers     = ['auai.org/UAI/2017/Chairs'],
            writers     = ['auai.org/UAI/2017/Chairs'],
            signatures  = ['auai.org/UAI/2017/Chairs'],
            signatories = [],
            members     = []) #more to be added later from the SPC invitation process
        groups.append(spc_emailed)

    if overwrite_allowed('auai.org/UAI/2017/PC'):
        pc = Group('auai.org/UAI/2017/PC',
            readers     = ['everyone'], #the members of the program committee should be broadly known
            writers     = ['auai.org/UAI/2017/Chairs','auai.org/UAI/2017'], #the conference needs to be a writer whenever the process functions need to modify the group
            signatures  = ['auai.org/UAI/2017/Chairs'],
            signatories = [], #I think the Program Committee shouldn't have a reason to sign a note representing the entire PC, so leaving blank
            members     = []) #more to be added later, from the list of PC members
        groups.append(pc)

    if overwrite_allowed('auai.org/UAI/2017/PC/invited'):
        pc_invited      = Group('auai.org/UAI/2017/PC/invited', #decided to make this a subgroup of /PC
            readers     = ['auai.org/UAI/2017/Chairs','auai.org/UAI/2017'],
            writers     = ['auai.org/UAI/2017/Chairs','auai.org/UAI/2017'],
            signatures  = ['auai.org/UAI/2017/Chairs'],
            signatories = [], #nobody should be able to sign as this group
            members     = []) #members to be added by process function
        groups.append(pc_invited)

    if overwrite_allowed('auai.org/UAI/2017/PC/declined'):
        pc_declined     = Group('auai.org/UAI/2017/PC/declined', #decided to make this a subgroup of /PC
            readers     = ['auai.org/UAI/2017/Chairs','auai.org/UAI/2017'],
            writers     = ['auai.org/UAI/2017/Chairs','auai.org/UAI/2017'],
            signatures  = ['auai.org/UAI/2017/Chairs'],
            signatories = [],
            members     = [])
        groups.append(pc_declined)


    ## Post the groups
    for g in groups:
        print "Posting group: ",g.id
        openreview.post_group(g)
    openreview.post_group(openreview.get_group('host').add_member('auai.org/UAI/2017'))

    #########################
    ##  SETUP INVITATIONS  ##
    #########################
    invitations = []

    ## Create the submission invitation, form, and add it to the list of invitations to post
    submission_invitation = Invitation('auai.org/UAI/2017',
        'submission',
        readers=['everyone'],
        writers=['auai.org/UAI/2017'],
        invitees=['~'],
        signatures=['auai.org/UAI/2017'],
        duedate=1507180500000, #duedate is Nov 5, 2017, 17:15:00 (5:15pm) Eastern Time
        process='../process/usersubmissionProcess.js')

    #submission process function doesn't do anything yet
    #submission_invitation.process = "function(){done();return true;};"

    submission_invitation.reply = {
        'forum': None,
        'replyto': None,
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values': [UAIData.get_program_co_chairs()] #who should be allowed to read UAI submissions and when?
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
                'value-regex': '.{1,250}',
                'required':True
            },
            'authors': {
                'description': 'Comma separated list of author names, as they appear in the paper.',
                'order': 2,
                'values-regex': "[^;,\\n]+(,[^,\\n]+)*",
                'required':True
            },
            'authorids': {
                'description': 'Comma separated list of author email addresses, in the same order as above.',
                'order': 3,
                'values-regex': "[^;,\\n]+(,[^,\\n]+)*",
                'required':True
            },
            'subject areas': {
                'description': 'List of areas of expertise.',
                'order': 4,
                'values-dropdown': UAIData.get_subject_areas()
            },
            'keywords': {
                'description': 'Comma separated list of keywords.',
                'order': 6,
                'values-regex': "[^;,\\n]+(,[^,\\n]+)*"
            },
            'TL;DR': {
                'description': '\"Too Long; Didn\'t Read\": a short sentence describing your paper',
                'order': 7,
                'value-regex': '[^\\n]{0,250}',
                'required':False
            },
            'abstract': {
                'description': 'Abstract of paper.',
                'order': 8,
                'value-regex': '[\\S\\s]{1,5000}',
                'required':True
            },
            'pdf': {
                'description': 'Upload a PDF file that ends with .pdf)',
                'order': 9,
                'value-regex': 'upload',
                'required':True
            },
            'student paper': {
                'description': 'Is it a student paper?',
                'order': 10,
                'value-radio': [
                    'Yes',
                    'No'
                ]
            }
        }
    }

    invitations.append(submission_invitation)

    blind_submission_invitation = Invitation('auai.org/UAI/2017',
        'blind-submission',
        readers=['everyone'],
        writers=['auai.org/UAI/2017'],
        invitees=['~'],
        signatures=['auai.org/UAI/2017'],
        duedate=1507180500000, #duedate is Nov 5, 2017, 17:15:00 (5:15pm) Eastern Time
        process='../process/submissionProcess.js')

    blind_submission_invitation.reply = {
        'forum': None,
        'replyto': None,
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values': [UAIData.get_program_co_chairs(), UAIData.get_senior_program_committee(), UAIData.get_program_committee()] #who should be allowed to read UAI submissions and when?
        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values': ['auai.org/UAI/2017']
        },
        'writers': {
            'values': ['auai.org/UAI/2017']
        },
        'content': {
            'authors': {
                'description': 'Comma separated list of author names, as they appear in the paper.',
                'order': 1,
                'values': [],
                'required':True
            },
            'authorids': {
                'description': 'Comma separated list of author email addresses, in the same order as above.',
                'order': 2,
                'values': [],
                'required':True
            }
        }
    }

    invitations.append(blind_submission_invitation)

    ## Create SPC recruitment invitation/form, and add it to the list of invitations to post
    spc_invitation = Invitation('auai.org/UAI/2017', 'spc_invitation',
        readers=['everyone'],
        writers=['auai.org/UAI/2017'],
        invitees=['auai.org/UAI/2017/SPC/invited'],
        signatures=['auai.org/UAI/2017'],
        process='../process/responseInvitationProcess_uai2017.js',
        web='../webfield/web-field-invitation.html')

    spc_invitation.reply = {
        #### Why was this here?
        # 'forum': {
        #     'value-regex': 'auai.org/UAI/2017/PC/~.*'
        # },
        'content': {
            'username': {
                'description': 'OpenReview username (e.g. ~Alan_Turing1)',
                'order': 1,
                'value-regex': '~.*'
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
            'values': ['OpenReview.net']
        },
        'signatures': {
            'values-regex': '\\(anonymous\\)'
        },
        'writers': {
            'values-regex': '\\(anonymous\\)'
        }
    }

    invitations.append(spc_invitation)

    ## Create SPC registration invitation, and add it to the list of invitations to post
    spc_registration = Invitation('auai.org/UAI/2017', 'spc_registration',
        readers = ['auai.org/UAI/2017','auai.org/UAI/2017/Chairs'],
        writers = ['auai.org/UAI/2017'],
        invitees = ['OpenReview.net'],
        signatures = ['auai.org/UAI/2017'],
        process = '../process/spc_registrationProcess.js'
        )


    spc_registration.reply = {
        "content": {
            'title': {
                'description': 'Title of paper.',
                'order': 1,
                'value-regex': '.{1,250}',
                'required':True
            },
            'description': {
                'order': 2,
                'value-regex': '[\\S\\s]{1,5000}',
                'required':True
            },
        },
        "readers":{
            'values': ['auai.org/UAI/2017/SPC']
        },
        "signatures":{
            'values': ['auai.org/UAI/2017']
        },
        "writers":{
            'values': ['auai.org/UAI/2017']
        }
    }

    invitations.append(spc_registration)


    # ## Create the paper matching invitation
    # paper_invitation_reply = {
    #     'content': {}
    # }

    # paper_meta_invitation = Invitation('auai.org/UAI/2017',
    #                                    'matching',
    #                                    signatures=['auai.org/UAI/2017'],
    #                                    readers=['everyone'],
    #                                    writers=['everyone'], reply=paper_invitation_reply)

    # invitations.append(paper_meta_invitation)


    ## Post the invitations
    for i in invitations:
        print "Posting invitation: "+i.id
        openreview.post_invitation(i)

    ## Create a root note for the spc_registration invitation, so that users can

    #(id=None, number=None, cdate=None, tcdate=None, ddate=None, content=None, forum=None, invitation=None, replyto=None, active=None, readers=None, nonreaders=None, signatures=None, writers=None):

    spc_registration_rootnote = Note(invitation='auai.org/UAI/2017/-/spc_registration',
        readers = ['auai.org/UAI/2017/SPC'],
        writers = ['auai.org/UAI/2017'],
        signatures = ['auai.org/UAI/2017'])
    spc_registration_rootnote.content = {
        'title': 'Senior Program Commmittee Expertise Registration',
        'description': "Thank you for agreeing to serve as a Senior Program Committee member. Please submit your areas of expertise on this page by clicking on the \"Add SPC Expertise\" button below. You may edit your submission at any time by returning to this page and selecting the \"Edit\" button next to your submission. You can find this page again by going to your Tasks page, scrolling down to your list of submitted posts, and selecting your Senior Program Committee Form Response."
    }

    openreview.post_note(spc_registration_rootnote)

else:
    print "Aborted. User must be Super User."
