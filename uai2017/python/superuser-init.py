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

    if overwrite_allowed('UAI.org'):
        uai = Group('UAI.org',
            readers     = ['everyone'],
            writers     = ['OpenReview.net'],
            signatures  = ['OpenReview.net'],
            signatories = ['UAI.org'],
            members     = [] )
        groups.append(uai)


    if overwrite_allowed('UAI.org/2017'):
        uai2017 = Group('UAI.org/2017',
            readers     = ['everyone'],
            writers     = ['OpenReview.net'],
            signatures  = ['OpenReview.net'],
            signatories = [],
            members     = [])
        groups.append(uai2017)


    if overwrite_allowed('UAI.org/2017/conference'):
        conference = Group('UAI.org/2017/conference',
            readers     = ['everyone'],
            writers     = ['UAI.org/2017/conference'],
            signatures  = ['OpenReview.net'],
            signatories = ['UAI.org/2017/conference'],
            members     = [],
            web         = '../webfield/uai2017conference_webfield.html')
        groups.append(conference)


    if overwrite_allowed('UAI.org/2017/conference/Program_Co-Chairs'):
        Program_Chairs = Group('UAI.org/2017/conference/Program_Co-Chairs',
            readers     = ['everyone'],
            writers     = ['OpenReview.net','UAI.org/2017/conference/Program_Co-Chairs'],
            signatures  = ['OpenReview.net'],
            signatories = ['UAI.org/2017/conference/Program_Co-Chairs'],
            members     = []) #should include Gal and Kristian
        groups.append(Program_Chairs)


    if overwrite_allowed('UAI.org/2017/conference/Senior_Program_Committee'):
        spc = Group('UAI.org/2017/conference/Senior_Program_Committee',
            readers     = ['everyone'],
            writers     = ['UAI.org/2017/conference/Program_Co-Chairs','UAI.org/2017/conference'], #the conference needs to be a writer whenever the process functions need to modify the group
            signatures  = ['UAI.org/2017/conference/Program_Co-Chairs'],
            signatories = ['UAI.org/2017/conference/Program_Co-Chairs'], #it seems like only Gal and Kristian should be able to write notes representing the whole Senior_Program_Committee
            members     = ['UAI.org/2017/conference/Program_Co-Chairs']) #more to be added later, from the list of Senior_Program_Committee members
        groups.append(spc)

    if overwrite_allowed('UAI.org/2017/conference/Senior_Program_Committee/invited'):
        spc_invited = Group('UAI.org/2017/conference/Senior_Program_Committee/invited',
            readers     = ['UAI.org/2017/conference/Program_Co-Chairs','UAI.org/2017/conference'],
            writers     = ['UAI.org/2017/conference/Program_Co-Chairs','UAI.org/2017/conference'],
            signatures  = ['UAI.org/2017/conference/Program_Co-Chairs'],
            signatories = [],
            members     = []) #more to be added later from the SPC invitation process
        groups.append(spc_invited)

    if overwrite_allowed('UAI.org/2017/conference/Senior_Program_Committee/declined'):
        spc_declined = Group('UAI.org/2017/conference/Senior_Program_Committee/declined',
            readers     = ['UAI.org/2017/conference/Program_Co-Chairs','UAI.org/2017/conference'],
            writers     = ['UAI.org/2017/conference/Program_Co-Chairs','UAI.org/2017/conference'],
            signatures  = ['UAI.org/2017/conference/Program_Co-Chairs'],
            signatories = [],
            members     = []) #more to be added later from the SPC invitation process
        groups.append(spc_declined)

    if overwrite_allowed('UAI.org/2017/conference/Senior_Program_Committee/emailed'):
        spc_emailed = Group('UAI.org/2017/conference/Senior_Program_Committee/emailed',
            readers     = ['UAI.org/2017/conference/Program_Co-Chairs'],
            writers     = ['UAI.org/2017/conference/Program_Co-Chairs'],
            signatures  = ['UAI.org/2017/conference/Program_Co-Chairs'],
            signatories = [],
            members     = []) #more to be added later from the SPC invitation process
        groups.append(spc_emailed)

    if overwrite_allowed('UAI.org/2017/conference/Program_Committee'):
        pc = Group('UAI.org/2017/conference/Program_Committee',
            readers     = ['everyone'],
            writers     = ['UAI.org/2017/conference/Senior_Program_Committee'],
            signatures  = ['UAI.org/2017/conference/Senior_Program_Committee'],
            signatories = [], #I think the Program Committee shouldn't have a reason to sign a note representing the entire Program_Committee, so leaving blank
            members     = []) #more to be added later, from the list of Program_Committee members
        groups.append(pc)

    if overwrite_allowed('UAI.org/2017/conference/Program_Committee/invited'):
        pc_invited = Group('UAI.org/2017/conference/Program_Committee/invited', #decided to make this a subgroup of /Program_Committee
            readers=['UAI.org/2017/conference/Senior_Program_Committee'],
            writers=['UAI.org/2017/conference/Senior_Program_Committee'],
            signatures=['UAI.org/2017/conference/Senior_Program_Committee'],
            signatories=[], #nobody should be able to sign as this group
            members=[]) #members to be added by process function
        groups.append(pc_invited)

    if overwrite_allowed('UAI.org/2017/conference/Program_Committee/declined'):
        pc_declined = Group('UAI.org/2017/conference/Program_Committee/declined', #decided to make this a subgroup of /Program_Committee
            readers=['everyone'],
            writers=['UAI.org/2017/conference/Senior_Program_Committee'],
            signatures=['UAI.org/2017/conference/Senior_Program_Committee'],
            signatories=[],
            members=[])
        groups.append(pc_declined)


    ## Post the groups
    for g in groups:
        print "Posting group: ",g.id
        openreview.post_group(g)
    openreview.post_group(openreview.get_group('host').add_member('UAI.org/2017/conference'))

    #########################
    ##  SETUP INVITATIONS  ##
    #########################
    invitations = []

    ## Create the submission invitation, form, and add it to the list of invitations to post
    submission_invitation = Invitation('UAI.org/2017/conference',
        'submission',
        readers=['everyone'],
        writers=['UAI.org/2017/conference'],
        invitees=['~'],
        signatures=['UAI.org/2017/conference'],
        duedate=1507180500000, #duedate is Nov 5, 2017, 17:15:00 (5:15pm) Eastern Time
        process='../process/submissionProcess_uai2017.js')

    #submission process function doesn't do anything yet
    #submission_invitation.process = "function(){done();return true;};"

    submission_invitation.reply = {
        'forum': None,
        'replyto': None,
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values': ['UAI.org/2017/conference',UAIData.get_program_co_chairs(),UAIData.get_program_committee(),UAIData.get_senior_program_committee()] #who should be allowed to read UAI submissions and when?
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

    ## Create SPC recruitment invitation/form, and add it to the list of invitations to post
    spc_invitation = Invitation('UAI.org/2017/conference', 'spc_invitation',
        readers=['everyone'],
        writers=['UAI.org/2017/conference'],
        invitees=['UAI.org/2017/conference/Senior_Program_Committee/invited'],
        signatures=['UAI.org/2017/conference'],
        process='../process/responseInvitationProcess_uai2017.js',
        web='../webfield/web-field-invitation.html')

    spc_invitation.reply = {
        #### Why was this here?
        # 'forum': {
        #     'value-regex': 'UAI.org/2017/conference/Program_Committee/~.*'
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
    spc_registration = Invitation('UAI.org/2017/conference', 'spc_registration',
        readers = ['UAI.org/2017/conference','UAI.org/2017/conference/Program_Co-Chairs'],
        writers = ['UAI.org/2017/conference'],
        invitees = ['OpenReview.net'],
        signatures = ['UAI.org/2017/conference'],
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
            'values': ['UAI.org/2017/conference/Senior_Program_Committee']
        },
        "signatures":{
            'values': ['UAI.org/2017/conference']
        },
        "writers":{
            'values': ['UAI.org/2017/conference']
        }
    }

    invitations.append(spc_registration)


    # ## Create the paper matching invitation
    # paper_invitation_reply = {
    #     'content': {}
    # }

    # paper_meta_invitation = Invitation('UAI.org/2017/conference',
    #                                    'matching',
    #                                    signatures=['UAI.org/2017/conference'],
    #                                    readers=['everyone'],
    #                                    writers=['everyone'], reply=paper_invitation_reply)

    # invitations.append(paper_meta_invitation)


    ## Post the invitations
    for i in invitations:
        print "Posting invitation: "+i.id
        openreview.post_invitation(i)

    ## Create a root note for the spc_registration invitation, so that users can

    #(id=None, number=None, cdate=None, tcdate=None, ddate=None, content=None, forum=None, invitation=None, replyto=None, active=None, readers=None, nonreaders=None, signatures=None, writers=None):

    spc_registration_rootnote = Note(invitation='UAI.org/2017/conference/-/spc_registration',
        readers = ['UAI.org/2017/conference/Senior_Program_Committee'],
        writers = ['UAI.org/2017/conference'],
        signatures = ['UAI.org/2017/conference'])
    spc_registration_rootnote.content = {
        'title': 'Senior Program Commmittee Expertise Registration',
        'description': "Thank you for agreeing to serve as a Senior Program Committee member. Please submit your areas of expertise on this page by clicking on the \"Add SPC Expertise\" button below. You may edit your submission at any time by returning to this page and selecting the \"Edit\" button next to your submission. You can find this page again by going to your Tasks page, scrolling down to your list of submitted posts, and selecting your Senior Program Committee Form Response."
    }

    openreview.post_note(spc_registration_rootnote)

else:
    print "Aborted. User must be Super User."
