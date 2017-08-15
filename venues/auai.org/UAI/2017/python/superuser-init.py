#!/usr/bin/python

"""
This is the initialization script for UAI 2017.

It should only be run ONCE to kick off the conference. It can only be run by the Super User.

"""

## Import statements
import openreview
from config import *
import sys, os
import subprocess
import argparse
import config

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--overwrite', help="If set to true, overwrites existing groups")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

overwrite = True if (args.overwrite!=None and args.overwrite.lower()=='true') else False

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

subprocess.call([
    "node",
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../utils/processToFile.js")),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../process/spc_registrationProcess.template")),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../process")),
])

subprocess.call([
    "node",
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../../../utils/processToFile.js")),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../process/pc_registrationProcess.template")),
    os.path.abspath(os.path.join(os.path.dirname(__file__), "../process")),
])

groups = []
if client.user['id'].lower()=='openreview.net':

    #########################
    ##    SETUP GROUPS     ##
    #########################

    if not client.exists('auai.org') or overwrite==True:
        auai = openreview.Group('auai.org',
            readers     = ['everyone'],
            writers     = ['OpenReview.net'],
            signatures  = ['OpenReview.net'],
            signatories = [],
            members     = [] )
        groups.append(auai)


    if not client.exists('auai.org/UAI') or overwrite==True:
        uai = openreview.Group('auai.org/UAI',
            readers     = ['everyone'],
            writers     = ['OpenReview.net'],
            signatures  = ['OpenReview.net'],
            signatories = [],
            members     = [] )
        groups.append(uai)


    if not client.exists(CONFERENCE) or overwrite==True:
        uai2017 = openreview.Group(CONFERENCE,
            readers     = ['everyone'],
            writers     = [CONFERENCE],
            signatures  = ['OpenReview.net'],
            signatories = [CONFERENCE],
            members     = [ADMIN],
            web         = os.path.abspath(os.path.join(os.path.dirname(__file__), '../webfield/uai2017_webfield.html')))
        groups.append(uai2017)


    if not client.exists(COCHAIRS) or overwrite==True:
        Program_Chairs = openreview.Group(COCHAIRS,
            readers     = [CONFERENCE, COCHAIRS, SPC, PC],
            writers     = [CONFERENCE],
            signatures  = [CONFERENCE],
            signatories = [COCHAIRS],
            members     = ["~Alejandro_Molina1", "~Kristian_Kersting1", "~Gal_Elidan1"])
        groups.append(Program_Chairs)


    if not client.exists(SPC) or overwrite==True:
        spc = openreview.Group(SPC,
            readers     = [CONFERENCE, COCHAIRS, SPC, PC],
            writers     = [CONFERENCE], #the conference needs to be a writer whenever the process functions need to modify the group
            signatures  = [CONFERENCE],
            signatories = [SPC],
            members     = [], #more to be added later, from the list of Senior_Program_Committee members
            web         = os.path.abspath(os.path.join(os.path.dirname(__file__), '../webfield/spc_group_webfield.html')))
        groups.append(spc)

    if not client.exists(SPC + '/invited') or overwrite==True:
        spc_invited = openreview.Group(SPC + '/invited',
            readers     = [CONFERENCE, COCHAIRS],
            writers     = [CONFERENCE, COCHAIRS],
            signatures  = [CONFERENCE],
            signatories = [],
            members     = []) #more to be added later from the Senior_Program_Committee invitation process
        groups.append(spc_invited)

    if not client.exists(SPC + '/declined') or overwrite==True:
        spc_declined = openreview.Group(SPC+'/declined',
            readers     = [CONFERENCE, COCHAIRS], #Should cochairs be reader of this group?
            writers     = [CONFERENCE],
            signatures  = [CONFERENCE],
            signatories = [],
            members     = []) #more to be added later from the Senior_Program_Committee invitation process
        groups.append(spc_declined)

    if not client.exists(SPC + '/emailed') or overwrite==True:
        spc_emailed = openreview.Group(SPC + '/emailed',
            readers     = [CONFERENCE, COCHAIRS],
            writers     = [CONFERENCE],
            signatures  = [CONFERENCE],
            signatories = [],
            members     = []) #more to be added later from the Senior_Program_Committee invitation process
        groups.append(spc_emailed)

    if not client.exists(SPC + '/reminded') or overwrite==True:
        spc_emailed = openreview.Group(SPC + '/reminded',
            readers     = [CONFERENCE, COCHAIRS],
            writers     = [CONFERENCE],
            signatures  = [CONFERENCE],
            signatories = [],
            members     = []) #more to be added later from the Senior_Program_Committee invitation process
        groups.append(spc_emailed)

    if not client.exists(PC) or overwrite==True:
        pc = openreview.Group(PC,
            readers     = [CONFERENCE, COCHAIRS, SPC, PC],
            writers     = [CONFERENCE],
            signatures  = [CONFERENCE],
            signatories = [PC],
            members     = []) #more to be added later, from the list of Program_Committee members
        groups.append(pc)

    if not client.exists(PC+'/invited') or overwrite==True:
        pc_invited      = openreview.Group(PC+'/invited',
            readers     = [CONFERENCE, COCHAIRS],
            writers     = [CONFERENCE],
            signatures  = [CONFERENCE],
            signatories = [],
            members     = []) #members to be added by process function
        groups.append(pc_invited)

    if not client.exists(PC+'/declined') or overwrite==True:
        pc_declined     = openreview.Group(PC+'/declined',
            readers     = [CONFERENCE, COCHAIRS],
            writers     = [CONFERENCE, COCHAIRS],
            signatures  = [CONFERENCE],
            signatories = [],
            members     = [])
        groups.append(pc_declined)

    if not client.exists(PC+'/emailed') or overwrite==True:
        pc_emailed     = openreview.Group(PC+'/emailed',
            readers     = [CONFERENCE, COCHAIRS],
            writers     = [CONFERENCE],
            signatures  = [CONFERENCE],
            signatories = [],
            members     = [])
        groups.append(pc_emailed)


    ## Post the groups
    for g in groups:
        print "Posting group: ",g.id
        client.post_group(g)
    client.post_group(client.get_group('host').add_member(CONFERENCE))


    #########################
    ##  SETUP INVITATIONS  ##
    #########################
    invitations = []

    ## Create the submission invitation, form, and add it to the list of invitations to post
    submission_invitation = openreview.Invitation(CONFERENCE+'/-/submission',
        readers = ['everyone'],
        writers = [CONFERENCE],
        invitees = ['~'],
        signatures = [CONFERENCE],
        duedate = 1491044400000, #duedate is March 31, 2017, 23:59:59 Samoa Time
        process = os.path.abspath(os.path.join(os.path.dirname(__file__), '../process/submissionProcess.js')))

    submission_invitation.reply = {
        'forum': None,
        'replyto': None,
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values-copied': [CONFERENCE, COCHAIRS, '{content.authorids}', '{signatures}']
        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values-regex': '~.*'
        },
        'writers': {
            'values': []
        },
        'content': {
            'title': {
                'description': 'Title of paper.',
                'order': 1,
                'value-regex': '.{1,250}',
                'required':True
            },
            'authors': {
                'description': 'Comma separated list of author names.',
                'order': 2,
                'values-regex': "[^;,\\n]+(,[^,\\n]+)*",
                'required':True
            },
            'authorids': {
                'description': 'Comma separated list of author email addresses, lowercased, in the same order as above. For authors with existing OpenReview accounts, please make sure that the provided email address(es) match those listed in the author\'s profile.',
                'order': 3,
                'values-regex': "([a-z0-9_\-\.]{2,}@[a-z0-9_\-\.]{2,}\.[a-z]{2,},){0,}([a-z0-9_\-\.]{2,}@[a-z0-9_\-\.]{2,}\.[a-z]{2,})",
                'required':True
            },
            'subject areas': {
                'description': 'List of areas of expertise.',
                'order': 4,
                'values-dropdown': SUBJECT_AREAS,
                'required':True
            },
            'keywords': {
                'description': 'Comma separated list of keywords.',
                'order': 6,
                'values-regex': "(^$)|[^;,\\n]+(,[^,\\n]+)*"
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
                ],
                'required':True
            }
        }
    }

    invitations.append(submission_invitation)

    blind_submission_invitation = openreview.Invitation(CONFERENCE+'/-/blind-submission',
        readers = ['everyone'],
        writers = [CONFERENCE],
        invitees = ['~'],
        signatures = [CONFERENCE])

    blind_submission_invitation.reply = {
        'forum': None,
        'replyto': None,
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values-regex': 'auai.org/UAI/2017.*' #who should be allowed to read UAI submissions and when?
        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values': [CONFERENCE]
        },
        'writers': {
            'values': [CONFERENCE]
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
    spc_invitation = openreview.Invitation(CONFERENCE+'/-/spc_invitation',
        readers=['everyone'],
        writers=[CONFERENCE],
        invitees=[SPC + '/invited'],
        signatures=[CONFERENCE],
        process=os.path.abspath(os.path.join(os.path.dirname(__file__), '../process/spc_responseInvitationProcess_uai2017.js')),
        web=os.path.abspath(os.path.join(os.path.dirname(__file__), '../webfield/spc_invitation_webfield.html')))

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

    ## Create Program_Committee recruitment invitation/form, and add it to the list of invitations to post
    pc_invitation = openreview.Invitation(CONFERENCE+'/-/pc_invitation',
        readers = ['everyone'],
        writers = [CONFERENCE],
        invitees = [PC + '/invited'],
        signatures = [CONFERENCE],
        process = os.path.abspath(os.path.join(os.path.dirname(__file__), '../process/pc_responseInvitationProcess_uai2017.js')),
        web = os.path.abspath(os.path.join(os.path.dirname(__file__), '../webfield/pc_invitation_webfield.html')))

    pc_invitation.reply = {
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

    invitations.append(pc_invitation)


    ## Create Senior_Program_Committee registration invitation, and add it to the list of invitations to post
    spc_registration = openreview.Invitation(CONFERENCE+'/-/spc_registration',
        readers = [CONFERENCE, COCHAIRS],
        writers = [CONFERENCE],
        invitees = ['OpenReview.net'],
        signatures = [CONFERENCE],
        process = os.path.abspath(os.path.join(os.path.dirname(__file__), '../process/spc_registrationProcess.js'))
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
            'values': [CONFERENCE]
        },
        "writers":{
            'values': [CONFERENCE]
        }
    }

    invitations.append(spc_registration)



    ## Create Senior_Program_Committee registration invitation, and add it to the list of invitations to post
    pc_registration = openreview.Invitation(CONFERENCE+'/-/pc_registration',
        readers = [CONFERENCE, COCHAIRS],
        writers = [CONFERENCE],
        invitees = ['OpenReview.net'],
        signatures = [CONFERENCE],
        process = os.path.abspath(os.path.join(os.path.dirname(__file__), '../process/pc_registrationProcess.js'))
        )

    pc_registration.reply = {
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
            'values': [PC]
        },
        "signatures":{
            'values': [CONFERENCE]
        },
        "writers":{
            'values': [CONFERENCE]
        }
    }

    invitations.append(pc_registration)


    metadata_reply = {
        'forum': None,
        'replyto': None,
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values': [CONFERENCE]
        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values-regex': CONFERENCE
        },
        'writers': {
            'values-regex': CONFERENCE
        },
        'content': {}
    }

    paper_metadata_invitation = openreview.Invitation(config.METADATA,
                                               writers=['OpenReview.net'],
                                               readers=[CONFERENCE],
                                               invitees=[CONFERENCE],
                                               signatures=['OpenReview.net'],
                                               reply=metadata_reply)
    invitations.append(paper_metadata_invitation)


    #Define the matching assignments reply
    assignments_reply = {
        'forum': None,
        'replyto': None,
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values': [CONFERENCE]
        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values-regex': CONFERENCE
        },
        'writers': {
            'values-regex': CONFERENCE
        },
        'content': {}
    }

    #Create the matching assignments invitation
    matching_assignments_invitation = openreview.Invitation(config.ASSIGNMENT,
                                                writers = ['OpenReview.net'],
                                                readers = [CONFERENCE],
                                                invitees = [CONFERENCE],
                                                signatures = ['OpenReview.net'],
                                                reply = assignments_reply)
    invitations.append(matching_assignments_invitation)


    bid_tag_invitation = openreview.Invitation(CONFERENCE+'/-/Add/Bid',
        readers=['everyone'],
        writers=[CONFERENCE],
        invitees=[],
        signatures=[CONFERENCE],
        duedate=1507180500000, #duedate is Nov 5, 2017, 17:15:00 (5:15pm) Eastern Time
        web=os.path.abspath(os.path.join(os.path.dirname(__file__), '../webfield/add_bid_invitation_webfield.html')),
        multiReply=False)

    bid_tag_invitation.reply = {
        'forum': None,
        'replyto': None,
        'invitation': blind_submission_invitation.id,
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values-copied': [CONFERENCE, '{signatures}']
        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values-regex': '~.*'
        },
        'content': {
            'tag': {
                'description': 'Bid description',
                'order': 1,
                'value-dropdown': ['I want to review',
                    'I can review',
                    'I can probably review but am not an expert',
                    'I cannot review',
                    'No bid'],
                'required':True
            }
        }
    }

    invitations.append(bid_tag_invitation)

    ## Post the invitations
    for i in invitations:
        print "Posting invitation: "+i.id
        client.post_invitation(i)

    ## Create a root note for the spc_registration invitation
    spc_registration_rootnote = openreview.Note(invitation='auai.org/UAI/2017/-/spc_registration',
        readers = [SPC],
        writers = [CONFERENCE],
        signatures = [CONFERENCE])
    spc_registration_rootnote.content = {
        'title': 'Senior Program Commmittee Expertise Registration',
        'description': "Thank you for agreeing to serve as a Senior Program Committee member. Please submit your areas of expertise on this page by clicking on the \"Add Senior_Program_Committee Expertise\" button below. You may edit your submission at any time by returning to this page and selecting the \"Edit\" button next to your submission. You can find this page again by going to your Tasks page, scrolling down to your list of submitted posts, and selecting your Senior Program Committee Form Response."
    }

    ## Create a root note for the pc_registration invitation
    pc_registration_rootnote = openreview.Note(invitation='auai.org/UAI/2017/-/pc_registration',
        readers = [PC],
        writers = [CONFERENCE],
        signatures = [CONFERENCE])
    pc_registration_rootnote.content = {
        'title': 'Reviewer Expertise Registration',
        'description': "Thank you for agreeing to serve as a Program Committee member / Reviewer. Please submit your areas of expertise on this page by clicking on the \"Add Reviewer Expertise\" button below. You may edit your submission at any time by returning to this page and selecting the \"Edit\" button next to your submission. You can find this page again by going to your Tasks page, scrolling down to your list of submitted posts, and selecting your Reviewer Form Response."
    }

    #Post the notes above if not present
    spc_notes = client.get_notes(invitation = 'auai.org/UAI/2017/-/spc_registration')
    if not spc_notes:
        print 'Posting root note'
        client.post_note(spc_registration_rootnote)

    pc_notes = client.get_notes(invitation = 'auai.org/UAI/2017/-/pc_registration')
    if not pc_notes:
        print 'Posting root note'
        client.post_note(pc_registration_rootnote)

else:
    print "Aborted. User must be Super User."
