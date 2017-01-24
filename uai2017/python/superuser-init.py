#!/usr/bin/python

"""
This is the initialization script for UAI 2017.

It should only be run ONCE to kick off the conference. It can only be run by the Super User.

"""

## Import statements
import argparse
import csv
import sys
import openreview
from uaidata import *
from subprocess import call

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--overwrite', help="If set to true, overwrites existing groups")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    client = openreview.Client(baseurl=args.baseurl)

groups = []
overwrite = True if (args.overwrite!=None and args.overwrite.lower()=='true') else False
def overwrite_allowed(groupid):
    if not client.exists(groupid) or overwrite==True:
        return True
    else:
        return False

call(["node", "../../scripts/processToFile.js", "../process/submissionProcess.template", "../process"])
call(["node", "../../scripts/processToFile.js", "../process/spc_registrationProcess.template", "../process"])

if client.user['id'].lower()=='openreview.net':

    #########################
    ##    SETUP GROUPS     ##
    #########################

    if overwrite_allowed('auai.org'):
        auai = openreview.Group('auai.org',
            readers     = ['everyone'],
            writers     = ['OpenReview.net'],
            signatures  = ['OpenReview.net'],
            signatories = [],
            members     = [] )
        groups.append(auai)


    if overwrite_allowed('auai.org/UAI'):
        uai = openreview.Group('auai.org/UAI',
            readers     = ['everyone'],
            writers     = ['OpenReview.net'],
            signatures  = ['OpenReview.net'],
            signatories = [],
            members     = [] )
        groups.append(uai)


    if overwrite_allowed('auai.org/UAI/2017'):
        uai2017 = openreview.Group('auai.org/UAI/2017',
            readers     = ['everyone'],
            writers     = ['auai.org/UAI/2017', COCHAIRS],
            signatures  = ['OpenReview.net'],
            signatories = ['auai.org/UAI/2017', COCHAIRS],
            members     = [COCHAIRS],
            web         = '../webfield/uai2017_webfield.html')
        groups.append(uai2017)


    if overwrite_allowed(COCHAIRS):
        Program_Chairs = openreview.Group(COCHAIRS,
            readers     = [COCHAIRS, SPC, PC],
            writers     = ['OpenReview.net',COCHAIRS],
            signatures  = ['OpenReview.net'],
            signatories = [COCHAIRS],
            members     = ["auai.org/UAI/2017","~Alejandro_Molina1","~Kristian_Kersting1","~Gal_Elidan1"]) #should include Gal and Kristian
        groups.append(Program_Chairs)


    if overwrite_allowed(SPC):
        spc = openreview.Group(SPC,
            readers     = [COCHAIRS, SPC, PC],
            writers     = [COCHAIRS,'auai.org/UAI/2017'], #the conference needs to be a writer whenever the process functions need to modify the group
            signatures  = [COCHAIRS],
            signatories = [SPC], #it seems like only Gal and Kristian should be able to write notes representing the whole Senior_Program_Committee
            members     = []) #more to be added later, from the list of Senior_Program_Committee members
        groups.append(spc)

    if overwrite_allowed(SPC+'/invited'):
        spc_invited = openreview.Group(SPC+'/invited',
            readers     = [COCHAIRS,'auai.org/UAI/2017'], #it should *NOT* be broadly known who was invited
            writers     = [COCHAIRS,'auai.org/UAI/2017'],
            signatures  = [COCHAIRS],
            signatories = [],
            members     = []) #more to be added later from the Senior_Program_Committee invitation process
        groups.append(spc_invited)

    if overwrite_allowed(SPC+'/declined'):
        spc_declined = openreview.Group(SPC+'/declined',
            readers     = [COCHAIRS,'auai.org/UAI/2017'], #it should *NOT* be broadly known who declined
            writers     = [COCHAIRS,'auai.org/UAI/2017'],
            signatures  = [COCHAIRS],
            signatories = [],
            members     = []) #more to be added later from the Senior_Program_Committee invitation process
        groups.append(spc_declined)

    if overwrite_allowed(SPC+'/emailed'):
        spc_emailed = openreview.Group(SPC+'/emailed',
            readers     = [COCHAIRS],
            writers     = [COCHAIRS],
            signatures  = [COCHAIRS],
            signatories = [],
            members     = []) #more to be added later from the Senior_Program_Committee invitation process
        groups.append(spc_emailed)

    if overwrite_allowed(SPC+'/reminded'):
        spc_emailed = openreview.Group(SPC+'/reminded',
            readers     = [COCHAIRS],
            writers     = [COCHAIRS],
            signatures  = [COCHAIRS],
            signatories = [],
            members     = []) #more to be added later from the Senior_Program_Committee invitation process
        groups.append(spc_emailed)

    if overwrite_allowed(PC):
        pc = openreview.Group(PC,
            readers     = [COCHAIRS, SPC, PC], #the members of the program committee should be broadly known
            writers     = [COCHAIRS,'auai.org/UAI/2017'], #the conference needs to be a writer whenever the process functions need to modify the group
            signatures  = [COCHAIRS],
            signatories = [PC],
            members     = []) #more to be added later, from the list of Program_Committee members
        groups.append(pc)

    if overwrite_allowed(PC+'/invited'):
        pc_invited      = openreview.Group(PC+'/invited', #decided to make this a subgroup of /Program_Committee
            readers     = [COCHAIRS,'auai.org/UAI/2017'],
            writers     = [COCHAIRS,'auai.org/UAI/2017'],
            signatures  = [COCHAIRS],
            signatories = [], #nobody should be able to sign as this group
            members     = []) #members to be added by process function
        groups.append(pc_invited)

    if overwrite_allowed(PC+'/declined'):
        pc_declined     = openreview.Group(PC+'/declined', #decided to make this a subgroup of /Program_Committee
            readers     = [COCHAIRS,'auai.org/UAI/2017'],
            writers     = [COCHAIRS,'auai.org/UAI/2017'],
            signatures  = [COCHAIRS],
            signatories = [],
            members     = [])
        groups.append(pc_declined)


    ## Post the groups
    for g in groups:
        print "Posting group: ",g.id
        client.post_group(g)
    client.post_group(client.get_group('host').add_member('auai.org/UAI/2017'))


    #########################
    ##  SETUP INVITATIONS  ##
    #########################
    invitations = []

    ## Create the submission invitation, form, and add it to the list of invitations to post
    submission_invitation = openreview.Invitation('auai.org/UAI/2017',
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
            'values': [COCHAIRS] #who should be allowed to read UAI submissions and when?
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
                'values-regex': "([a-z0-9_\-\.]{2,}@[a-z0-9_\-\.]{2,}\.[a-z]{2,},){0,}([a-z0-9_\-\.]{2,}@[a-z0-9_\-\.]{2,}\.[a-z]{2,})",
                'required':True
            },
            'subject areas': {
                'description': 'List of areas of expertise.',
                'order': 4,
                'values-dropdown': SUBJECT_AREAS
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
                'description': 'Is this a student paper?',
                'order': 10,
                'value-radio': [
                    'Yes',
                    'No'
                ]
            }
        }
    }

    invitations.append(submission_invitation)

    blind_submission_invitation = openreview.Invitation('auai.org/UAI/2017',
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
            'values-regex': 'auai.org/UAI/2017.*' #who should be allowed to read UAI submissions and when?
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
                'values-regex': '.*',
                'required':True
            },
            'authorids': {
                'description': 'Comma separated list of author email addresses, in the same order as above.',
                'order': 2,
                'values-regex': '.*',
                'required':True
            }
        }
    }

    invitations.append(blind_submission_invitation)

    ## Create Senior_Program_Committee recruitment invitation/form, and add it to the list of invitations to post
    spc_invitation = openreview.Invitation('auai.org/UAI/2017', 'spc_invitation',
        readers=['everyone'],
        writers=['auai.org/UAI/2017'],
        invitees=[SPC+'/invited'],
        signatures=['auai.org/UAI/2017'],
        process='../process/responseInvitationProcess_uai2017.js',
        web='../webfield/web-field-invitation.html')

    spc_invitation.reply = {
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

    ## Create Senior_Program_Committee registration invitation, and add it to the list of invitations to post
    spc_registration = openreview.Invitation('auai.org/UAI/2017', 'spc_registration',
        readers = ['auai.org/UAI/2017',COCHAIRS],
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
            'values': [SPC]
        },
        "signatures":{
            'values': ['auai.org/UAI/2017']
        },
        "writers":{
            'values': ['auai.org/UAI/2017']
        }
    }

    invitations.append(spc_registration)


    #Create the paper metadata invitation
    paper_metadata_reply = {
        'forum': None,
        'replyto': None,
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values': ['OpenReview.net'] #who should be allowed to read UAI submissions and when?
        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values-regex': 'OpenReview.net'
        },
        'writers': {
            'values-regex': 'OpenReview.net'
        },
        'content': {} #content is blank; this allows for ANYTHING to be placed in the content field.
        #we'll want to change this later one we know what the format will be.
    }
    paper_metadata_invitation = openreview.Invitation('auai.org/UAI/2017','Paper/Metadata',
                                               writers=['OpenReview.net'],
                                               readers=['OpenReview.net'],
                                               invitees=['OpenReview.net'],
                                               signatures=['OpenReview.net'],
                                               reply=paper_metadata_reply)
    invitations.append(paper_metadata_invitation)


    #Create the reviewer metadata invitation
    reviewer_metadata_reply = {
        'forum': None,
        'replyto': None,
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values': ['OpenReview.net'] #who should be allowed to read UAI submissions and when?
        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values-regex': 'OpenReview.net'
        },
        'writers': {
            'values-regex': 'OpenReview.net'
        },
        'content': {} #Content is blank. See above.
    }
    reviewer_metadata_invitation = openreview.Invitation('auai.org/UAI/2017','Reviewer/Metadata',
                                               writers=['OpenReview.net'],
                                               readers=['OpenReview.net'],
                                               invitees=['OpenReview.net'],
                                               signatures=['OpenReview.net'],
                                               reply=reviewer_metadata_reply)
    invitations.append(reviewer_metadata_invitation)


    ## Post the invitations
    for i in invitations:
        print "Posting invitation: "+i.id
        client.post_invitation(i)

    ## Create a root note for the spc_registration invitation
    spc_registration_rootnote = openreview.Note(invitation='auai.org/UAI/2017/-/spc_registration',
        readers = [SPC],
        writers = ['auai.org/UAI/2017'],
        signatures = ['auai.org/UAI/2017'])
    spc_registration_rootnote.content = {
        'title': 'Senior Program Commmittee Expertise Registration',
        'description': "Thank you for agreeing to serve as a Senior Program Committee member. Please submit your areas of expertise on this page by clicking on the \"Add Senior_Program_Committee Expertise\" button below. You may edit your submission at any time by returning to this page and selecting the \"Edit\" button next to your submission. You can find this page again by going to your Tasks page, scrolling down to your list of submitted posts, and selecting your Senior Program Committee Form Response."
    }

    #Create a note if not present
    notes = client.get_notes(invitation = 'auai.org/UAI/2017/-/spc_registration')
    if not notes:
        print 'Posting root note'
        client.post_note(spc_registration_rootnote)


else:
    print "Aborted. User must be Super User."
