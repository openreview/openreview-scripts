#!/usr/bin/python

"""
This is the initialization script for RSS 2017.

It should only be run ONCE to kick off the conference. It can only be run by the Super User.

"""

## Import statements
import argparse
import csv
import sys
import openreview
from rssdata import *
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

# PAM processToFile somehow converts the given template to a js file
# but they don't resemble each other
call(["node", "../../scripts/processToFile.js", "../process/submissionProcess.template", "../process"])
call(["node", "../../scripts/processToFile.js", "../process/spc_registrationProcess.template", "../process"])

if client.user['id'].lower()=='openreview.net':

    #########################
    ##    SETUP GROUPS     ##
    #########################
    # PAM why would these groups already exist?  Is this in case the script is called multiple times
    # what does each group represent?
    # this looks like the top levels can be seen by anyone, but can only be written by the superuser
    # what is the difference between the two?
    if overwrite_allowed('roboticsfoundation.org'):
        a_rss = openreview.Group('roboticsfoundation.org',
            readers     = ['everyone'],
            writers     = ['OpenReview.net'],
            signatures  = ['OpenReview.net'],
            signatories = [],
            members     = [] )
        groups.append(a_rss)


    if overwrite_allowed('roboticsfoundation.org/RSS'):
        rss = openreview.Group('roboticsfoundation.org/RSS',
            readers     = ['everyone'],
            writers     = ['OpenReview.net'],
            signatures  = ['OpenReview.net'],
            signatories = [],
            members     = [] )
        groups.append(rss)

    # PAM these all caps values are set in rssdata.py
    # CONFERENCE basically means anyone that has logged in - right?
    # if so, under 'readers' why have CONFERENCE, COCHAIRS, SPC, PC
    #   if you logged in as COCHAIR it still means you've logged in.
    # also since there aren't area chairs, does that mean
    # COHAIRS and SPCs go away?
    if overwrite_allowed(CONFERENCE):
        rss2017 = openreview.Group(CONFERENCE,
            readers     = ['everyone'],
            writers     = [CONFERENCE],
            signatures  = ['OpenReview.net'],
            signatories = [CONFERENCE],
            members     = [ADMIN],
            web         = '../webfield/rss2017_webfield.html')
        groups.append(rss2017)

    # PAM change to Karthik and Shayegan when have official id's
    if overwrite_allowed(COCHAIRS):
        Program_Chairs = openreview.Group(COCHAIRS,
            readers     = [CONFERENCE, COCHAIRS, SPC, PC],
            writers     = [CONFERENCE],
            signatures  = [CONFERENCE],
            signatories = [COCHAIRS],
            members     = ["~Alejandro_Molina1", "~Kristian_Kersting1", "~Gal_Elidan1"])
        groups.append(Program_Chairs)


    if overwrite_allowed(SPC):
        spc = openreview.Group(SPC,
            readers     = [CONFERENCE, COCHAIRS, SPC, PC],
            writers     = [CONFERENCE], #the conference needs to be a writer whenever the process functions need to modify the group
            signatures  = [CONFERENCE],
            signatories = [SPC],
            members     = []) #more to be added later, from the list of Senior_Program_Committee members
        groups.append(spc)

    # PAM why all of these sub-groups rather than 'invited', 'declined' info tagged to individuals in the group
    if overwrite_allowed(SPC + '/invited'):
        spc_invited = openreview.Group(SPC + '/invited',
            readers     = [CONFERENCE, COCHAIRS],
            writers     = [CONFERENCE, COCHAIRS],
            signatures  = [CONFERENCE],
            signatories = [],
            members     = []) #more to be added later from the Senior_Program_Committee invitation process
        groups.append(spc_invited)

    if overwrite_allowed(SPC + '/declined'):
        spc_declined = openreview.Group(SPC+'/declined',
            readers     = [CONFERENCE, COCHAIRS], #Should cochairs be reader of this group?
            writers     = [CONFERENCE],
            signatures  = [CONFERENCE],
            signatories = [],
            members     = []) #more to be added later from the Senior_Program_Committee invitation process
        groups.append(spc_declined)

    if overwrite_allowed(SPC + '/emailed'):
        spc_emailed = openreview.Group(SPC + '/emailed',
            readers     = [CONFERENCE, COCHAIRS],
            writers     = [CONFERENCE],
            signatures  = [CONFERENCE],
            signatories = [],
            members     = []) #more to be added later from the Senior_Program_Committee invitation process
        groups.append(spc_emailed)

    if overwrite_allowed(SPC + '/reminded'):
        spc_emailed = openreview.Group(SPC + '/reminded',
            readers     = [CONFERENCE, COCHAIRS],
            writers     = [CONFERENCE],
            signatures  = [CONFERENCE],
            signatories = [],
            members     = []) #more to be added later from the Senior_Program_Committee invitation process
        groups.append(spc_emailed)

    if overwrite_allowed(PC):
        pc = openreview.Group(PC,
            readers     = [CONFERENCE, COCHAIRS, SPC, PC],
            writers     = [CONFERENCE],
            signatures  = [CONFERENCE],
            signatories = [PC],
            members     = []) #more to be added later, from the list of Program_Committee members
        groups.append(pc)

    if overwrite_allowed(PC+'/invited'):
        pc_invited      = openreview.Group(PC+'/invited',
            readers     = [CONFERENCE, COCHAIRS],
            writers     = [CONFERENCE],
            signatures  = [CONFERENCE],
            signatories = [],
            members     = []) #members to be added by process function
        groups.append(pc_invited)

    if overwrite_allowed(PC+'/declined'):
        pc_declined     = openreview.Group(PC+'/declined',
            readers     = [CONFERENCE, COCHAIRS],
            writers     = [CONFERENCE, COCHAIRS],
            signatures  = [CONFERENCE],
            signatories = [],
            members     = [])
        groups.append(pc_declined)

    if overwrite_allowed(PC+'/emailed'):
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
    submission_invitation = openreview.Invitation(CONFERENCE,
        'submission',
        readers = ['everyone'],
        writers = [CONFERENCE],
        # PAM what does ~ mean?
        invitees = ['~'],
        signatures = [CONFERENCE],
        # PAM I think this duedate is off by a month - Oct, probably need to change it in UAI
        # think we should use datetime here instead for easier debugging
        # also should be defined once at the top - used in 4 places
        #duedate = 1507180500000, #duedate is Nov 5, 2017, 17:15:00 (5:15pm) Eastern Time
        duedate=TIMESTAMP_DUE,
        process = '../process/usersubmissionProcess.js')

    submission_invitation.reply = {
        'forum': None,
        'replyto': None,
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values': [CONFERENCE, COCHAIRS]
        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values-regex': '~.*'
        },
        'writers': {
            'value-copied': '{content.authorids}'
        },
        'content': {
            'title': {
                'description': 'Title of paper.',
                'order': 1,
                'value-regex': '.{1,250}',
                'required':True
            },
            # PAM what happens if the input doesn't match the regex?
            # [^;,\\n] means all chars except ';' ',' and '\n'
            'authors': {
                'description': 'Comma separated list of author names, as they appear in the paper.',
                'order': 2,
                'values-regex': "[^;,\\n]+(,[^,\\n]+)*",
                'required':True
            },
            'authorids': {
                'description': 'Comma separated list of author email addresses, in the same order as above.',
                'order': 3,
                # PAM put as a 'constant' up top
                # 2 or more lower case letters, numbers, _'s, -'s or .'s
                # then @
                # then 2 or more letters/numbers (like before)
                # then a .
                # then 2 or more letters only
                # then shows that with a comma for zero or more times followed by at least one proper expression
                # i.e. a list of email addresses
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
                # up to 250 chars with no line return
                'value-regex': '[^\\n]{0,250}',
                'required':False
            },
            'abstract': {
                'description': 'Abstract of paper.',
                'order': 8,
                # PAM is this up to 5,000 words, because \\S is not white space followed by \\s which is white space
                'value-regex': '[\\S\\s]{1,5000}',
                'required':True
            },
            'pdf': {
                'description': 'Upload a PDF file that ends with .pdf)',
                'order': 9,
                # PAM is this a GUI special word that gets coded as a button?
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

    blind_submission_invitation = openreview.Invitation(CONFERENCE,
        'blind-submission',
        readers = ['everyone'],
        writers = [CONFERENCE],
        invitees = ['~'],
        signatures = [CONFERENCE],
        #duedate = 1507180500000, #duedate is Nov 5, 2017, 17:15:00 (5:15pm) Eastern Time
        duedate = TIMESTAMP_DUE,
        process = '../process/submissionProcess.js')

    blind_submission_invitation.reply = {
        'forum': None,
        'replyto': None,
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values-regex': 'roboticsfoundation.org/RSS/2017.*' #who should be allowed to read RSS submissions and when?
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
            #PAM this is a lot more trusting than the regex for submission authorids
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
    spc_invitation = openreview.Invitation(CONFERENCE,
        'spc_invitation',
        readers=['everyone'],
        writers=[CONFERENCE],
        invitees=[SPC + '/invited'],
        signatures=[CONFERENCE],
        process='../process/spc_responseInvitationProcess_rss2017.js',
        web='../webfield/spc_invitation_webfield.html')

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
    pc_invitation = openreview.Invitation('roboticsfoundation.org/RSS/2017', 'pc_invitation',
        readers = ['everyone'],
        writers = [CONFERENCE],
        invitees = [PC + '/invited'],
        signatures = [CONFERENCE],
        process = '../process/pc_responseInvitationProcess_rss2017.js',
        web = '../webfield/pc_invitation_webfield.html')

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
    spc_registration = openreview.Invitation(CONFERENCE, 'spc_registration',
        readers = [CONFERENCE, COCHAIRS],
        writers = [CONFERENCE],
        invitees = ['OpenReview.net'],
        signatures = [CONFERENCE],
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
            'values': [CONFERENCE]
        },
        "writers":{
            'values': [CONFERENCE]
        }
    }

    invitations.append(spc_registration)

    # PAM can we remove all metada
    #Create the paper metadata invitation
    paper_metadata_reply = {
        'forum': None,
        'replyto': None,
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values': ['OpenReview.net', CONFERENCE] #who should be allowed to read RSS submissions and when?
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
    paper_metadata_invitation = openreview.Invitation(CONFERENCE,
        'Paper/Metadata',
        writers = ['OpenReview.net'],
        readers = ['OpenReview.net',CONFERENCE],
        invitees = ['OpenReview.net'],
        signatures = ['OpenReview.net'],
        reply = paper_metadata_reply)

    invitations.append(paper_metadata_invitation)


    #Create the reviewer metadata invitation
    reviewer_metadata_reply = {
        'forum': None,
        'replyto': None,
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values': ['OpenReview.net', CONFERENCE] #who should be allowed to read RSS submissions and when?
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

    reviewer_metadata_invitation = openreview.Invitation(CONFERENCE,
        'Reviewer/Metadata',
        writers=['OpenReview.net'],
        readers=['OpenReview.net', CONFERENCE],
        invitees=['OpenReview.net'],
        signatures=['OpenReview.net'],
        reply=reviewer_metadata_reply)

    invitations.append(reviewer_metadata_invitation)

    # PAM how do bid tags work?
    bid_tag_invitation = openreview.Invitation(CONFERENCE,
        'Add/Bid',
        readers=['everyone'],
        writers=[CONFERENCE],
        invitees=[PC],
        signatures=[CONFERENCE],
        #duedate=1507180500000, #duedate is Nov 5, 2017, 17:15:00 (5:15pm) Eastern Time
        duedate=TIMESTAMP_DUE,
        web='../webfield/web-field-bid-tag-invitation.html',
        multiReply=False,
        taskCompletionCount=50)

    bid_tag_invitation.reply = {
        'forum': None,
        'replyto': None,
        'invitation': blind_submission_invitation.id,
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'value-regex': '~.*'
        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'value-regex': '~.*'
        },
        'writers': {
            'value-regex': '~.*'
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

    recommendation_tag_invitation = openreview.Invitation(CONFERENCE,
        'Recommend/Reviewer',
        readers=['everyone'],
        writers=[CONFERENCE],
        invitees=[SPC],
        signatures=[CONFERENCE],
        #duedate=1507180500000, #duedate is Nov 5, 2017, 17:15:00 (5:15pm) Eastern Time
        duedate=TIMESTAMP_DUE,
        web='../webfield/web-field-recommendation-tag-invitation.html',
        multiReply=True,
        taskCompletionCount=50)

    recommendation_tag_invitation.reply = {
        'forum': None,
        'replyto': None,
        'invitation': blind_submission_invitation.id,
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'value-regex': '~.*'
        },
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'value-regex': '~.*'
        },
        'writers': {
            'value-regex': '~.*'
        },
        'content': {
            'tag': {
                'description': 'Recommendation description',
                'order': 1,
                'values-url': '/groups?id=' + PC,
                'required': True
            }
        }
    }

    invitations.append(recommendation_tag_invitation)


    ## Post the invitations
    for i in invitations:
        print "Posting invitation: "+i.id
        client.post_invitation(i)

    ## Create a root note for the spc_registration invitation
    spc_registration_rootnote = openreview.Note(invitation='roboticsfoundation.org/RSS/2017/-/spc_registration',
        readers = [SPC],
        writers = [CONFERENCE],
        signatures = [CONFERENCE])
    spc_registration_rootnote.content = {
        'title': 'Senior Program Commmittee Expertise Registration',
        'description': "Thank you for agreeing to serve as a Senior Program Committee member. Please submit your areas of expertise on this page by clicking on the \"Add Senior_Program_Committee Expertise\" button below. You may edit your submission at any time by returning to this page and selecting the \"Edit\" button next to your submission. You can find this page again by going to your Tasks page, scrolling down to your list of submitted posts, and selecting your Senior Program Committee Form Response."
    }

    #Create a note if not present
    notes = client.get_notes(invitation = 'roboticsfoundation.org/RSS/2017/-/spc_registration')
    if not notes:
        print 'Posting root note'
        client.post_note(spc_registration_rootnote)


else:
    print "Aborted. User must be Super User."
