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
            writers     = ['OpenReview.net'],
            signatures  = ['OpenReview.net'],
            signatories = [],
            members     = [],
            web         = '../webfield/uai2017conference_webfield.html')
        groups.append(conference)


    if overwrite_allowed('UAI.org/2017/conference/ProgramChairs'):
        programchairs = Group('UAI.org/2017/conference/ProgramChairs',
            readers     = ['everyone'],
            writers     = ['OpenReview.net','UAI.org/2017/conference/ProgramChairs'],
            signatures  = ['OpenReview.net'],
            signatories = ['UAI.org/2017/conference/ProgramChairs'],
            members     = []) #should include Gal and Kristian
        groups.append(programchairs)


    if overwrite_allowed('UAI.org/2017/conference/SrProgramCommittee'):
        spc = Group('UAI.org/2017/conference/SrProgramCommittee',
            readers     = ['everyone'],
            writers     = ['UAI.org/2017/conference/ProgramChairs','UAI.org/2017/conference'], #the conference needs to be a writer whenever the process functions need to modify the group
            signatures  = ['UAI.org/2017/conference/ProgramChairs'],
            signatories = ['UAI.org/2017/conference/ProgramChairs'], #it seems like only Gal and Kristian should be able to write notes representing the whole SrProgramCommittee
            members     = ['UAI.org/2017/conference/ProgramChairs']) #more to be added later, from the list of SrProgramCommittee members
        groups.append(spc)

    if overwrite_allowed('UAI.org/2017/conference/SrProgramCommittee/invited'):
        spc_invited = Group('UAI.org/2017/conference/SrProgramCommittee/invited',
            readers     = ['UAI.org/2017/conference/ProgramChairs','UAI.org/2017/conference'],
            writers     = ['UAI.org/2017/conference/ProgramChairs','UAI.org/2017/conference'],
            signatures  = ['UAI.org/2017/conference/ProgramChairs'],
            signatories = [],
            members     = []) #more to be added later from the SPC invitation process
        groups.append(spc_invited)

    if overwrite_allowed('UAI.org/2017/conference/SrProgramCommittee/declined'):
        spc_declined = Group('UAI.org/2017/conference/SrProgramCommittee/declined',
            readers     = ['UAI.org/2017/conference/ProgramChairs','UAI.org/2017/conference'],
            writers     = ['UAI.org/2017/conference/ProgramChairs','UAI.org/2017/conference'],
            signatures  = ['UAI.org/2017/conference/ProgramChairs'],
            signatories = [],
            members     = []) #more to be added later from the SPC invitation process
        groups.append(spc_declined)

    if overwrite_allowed('UAI.org/2017/conference/SrProgramCommittee/emailed'):
        spc_emailed = Group('UAI.org/2017/conference/SrProgramCommittee/emailed',
            readers     = ['UAI.org/2017/conference/ProgramChairs'],
            writers     = ['UAI.org/2017/conference/ProgramChairs'],
            signatures  = ['UAI.org/2017/conference/ProgramChairs'],
            signatories = [],
            members     = []) #more to be added later from the SPC invitation process
        groups.append(spc_emailed)

    if overwrite_allowed('UAI.org/2017/conference/ProgramCommittee'):
        pc = Group('UAI.org/2017/conference/ProgramCommittee',
            readers     = ['everyone'],
            writers     = ['UAI.org/2017/conference/SrProgramCommittee'],
            signatures  = ['UAI.org/2017/conference/SrProgramCommittee'],
            signatories = [], #I think the Program Committee shouldn't have a reason to sign a note representing the entire ProgramCommittee, so leaving blank
            members     = []) #more to be added later, from the list of ProgramCommittee members
        groups.append(pc)

    if overwrite_allowed('UAI.org/2017/conference/ProgramCommittee/invited'):
        pc_invited = Group('UAI.org/2017/conference/ProgramCommittee/invited', #decided to make this a subgroup of /ProgramCommittee
            readers=['UAI.org/2017/conference/SrProgramCommittee'],
            writers=['UAI.org/2017/conference/SrProgramCommittee'],
            signatures=['UAI.org/2017/conference/SrProgramCommittee'],
            signatories=[], #nobody should be able to sign as this group
            members=[]) #members to be added by process function
        groups.append(pc_invited)

    if overwrite_allowed('UAI.org/2017/conference/ProgramCommittee/declined'):
        pc_declined = Group('UAI.org/2017/conference/ProgramCommittee/declined', #decided to make this a subgroup of /ProgramCommittee
            readers=['everyone'],
            writers=['UAI.org/2017/conference/SrProgramCommittee'],
            signatures=['UAI.org/2017/conference/SrProgramCommittee'],
            signatories=['UAI.org/2017/Reviewers'],
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
        duedate=1578380500000)#, #duedate is Nov 5, 2017, 17:15:00 (5:15pm) Eastern Time
        #process='../process/submissionProcess_uai2017.js')

    #submission process function doesn't do anything yet
    submission_invitation.process = "function(){done();return true;};"

    submission_invitation.reply = {
        'forum': None,
        'replyto': None,
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values': ['everyone'] #who should be allowed to read UAI submissions and when?
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
                'description': 'Comma separated list of email domains of people who would have a conflict of interest in reviewing this paper, (e.g., cs.umass.edu;google.com, etc.).',
                'order': 100,
                'values-regex': "[^;,\\n]+(,[^,\\n]+)*",
                'required':True
            }
        }
    }

    invitations.append(submission_invitation)

    ## Create SPC recruitment invitation/form, and add it to the list of invitations to post
    spc_invitation = Invitation('UAI.org/2017/conference', 'spc_invitation',
        readers=['everyone'],
        writers=['UAI.org/2017/conference'],
        invitees=['UAI.org/2017/conference/SrProgramCommittee/invited'],
        signatures=['UAI.org/2017/conference'],
        process='../process/responseInvitationProcess_uai2017.js',
        web='../webfield/web-field-invitation.html')

    spc_invitation.reply = {
        #### Why was this here?
        # 'forum': {
        #     'value-regex': 'UAI.org/2017/conference/ProgramCommittee/~.*'
        # },
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
        readers = ['UAI.org/2017/conference','UAI.org/2017/conference/ProgramChairs'],
        writers = ['UAI.org/2017/conference'],
        invitees = ['OpenReview.net'],
        signatures = ['UAI.org/2017/conference']
        )
    spc_registration.process ="function(){done();return true;};"


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
            'values': ['UAI.org/2017/conference/ProgramChairs']
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
        readers = ['UAI.org/2017/conference/ProgramChairs'],
        writers = ['UAI.org/2017/conference'],
        signatures = ['UAI.org/2017/conference'])
    spc_registration_rootnote.content = {
        'title': 'Senior Program Commmittee Expertise Registration',
        'description': "This is a note."
    }

    openreview.post_note(spc_registration_rootnote)

else:
    print "Aborted. User must be Super User."
