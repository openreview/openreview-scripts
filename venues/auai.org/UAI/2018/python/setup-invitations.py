#!/usr/bin/python

"""
A script for managing invitations.

You can create, enable, or disable most invitations in ICLR 2018 from this script.

Usage:

python toggle-invitations.py Public_Comment --enable
python toggle-invitations.py Public_Comment --disable
"""

# Import statements
import argparse
import csv
import getpass
import sys
import re
import openreview
import requests
import config
import pprint
import os

maskAuthorsGroup = config.CONF + "/Paper[PAPER_NUMBER]/Authors"
maskReviewerGroup = config.CONF + "/Paper[PAPER_NUMBER]/Reviewers"
maskAreaChair1Group = config.CONF + "/Paper[PAPER_NUMBER]/Area_Chair[0-9]"
maskAreaChairsGroup = config.CONF + "/Paper[PAPER_NUMBER]/Area_Chairs"
maskAnonReviewerGroup = config.CONF + "/Paper[PAPER_NUMBER]/AnonReviewer[0-9]+"
maskAllUsersGroup = config.CONF + "/Paper[PAPER_NUMBER]/All_Users"
maskUnsubmittedGroup = config.CONF + "/Paper[PAPER_NUMBER]/Reviewers/Unsubmitted"
maskSubmittedGroup = config.CONF + "/Paper[PAPER_NUMBER]/Reviewers/Submitted"
PROGRAM_CHAIRS = 'auai.org/UAI/2018/Program_Chairs'
BLIND_SUBMISSION_INV = 'auai.org/UAI/2018/-/Blind_Submission'

invitation_configurations = {
    'Official_Comment': {
        'byPaper': True,
        'byForum': True,
        'invitees': [maskReviewerGroup, maskAuthorsGroup, maskAreaChairsGroup, PROGRAM_CHAIRS],
        'noninvitees': [maskUnsubmittedGroup],
        'params': config.official_comment_template,
        'signatures': {
            'description': '',
            'values-regex': [
                maskAnonReviewerGroup,
                maskAuthorsGroup,
                maskAreaChair1Group,
                PROGRAM_CHAIRS,
                config.CONF
            ],
        },
        'writers': {
            'description': 'Users that may modify this record.',
            'values-copied':  [config.CONF, '{signatures}']
        },
        'readers': {
            'description': 'Select all user groups that should be able to read this comment. Selecting \'All Users\' will allow paper authors, reviewers, area chairs, and program chairs to view this comment.',
            'values-dropdown': [
                maskAllUsersGroup,
                maskAuthorsGroup,
                maskReviewerGroup,
                maskAreaChairsGroup,
                PROGRAM_CHAIRS
            ]
        },
        'nonreaders': {
            'values': [maskUnsubmittedGroup]
        }
    },
    'Official_Review': {
        'byPaper': True,
        'invitees': [maskReviewerGroup],
        'noninvitees': [maskSubmittedGroup],
        'byForum': True,
        'byReplyTo': True,
        'params': config.official_review_template,
        'signatures': {
            'description': 'How your identity will be displayed with the above content.',
            'values-regex': [maskAnonReviewerGroup]
        },
        'writers': {
            'description': 'Users that may modify this record.',
            'values': ['auai.org/UAI/2018']
        },
        'readers': {
            'description': 'The users who will be allowed to read the reply content.',
            'values': [config.CONF, maskAuthorsGroup, maskReviewerGroup, maskAreaChairsGroup, PROGRAM_CHAIRS]
        },
        'nonreaders': {
            'values': [maskUnsubmittedGroup]
        }
    }
}

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('invitations', nargs='*', help="invitation id: " + ", ".join(invitation_configurations.keys()))
parser.add_argument('--enable', action='store_true', help="if present, enables the given invitation")
parser.add_argument('--disable', action='store_true', help='if present, disables the given invitation')
parser.add_argument('--overwrite', action='store_true')
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

if args.invitations == ['all']:
    invitations_to_process = invitation_configurations.keys()
else:
    invitations_to_process = args.invitations

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

pp = pprint.PrettyPrinter(indent=4)

papers = client.get_notes(invitation = BLIND_SUBMISSION_INV)

def get_or_create_invitations(invitationId, overwrite):
    invitation_config = invitation_configurations[invitationId]
    if invitation_config['byPaper']:

        invitations = client.get_invitations(regex = config.CONF + '/-/Paper.*/' + invitationId, tags = invitation_config.get('tags'))
        if invitations and len(invitations) == len(papers) and not overwrite:
            # TODO: why is this here? why not just return invitations?
            return [i for i in invitations if re.match(config.CONF + '/-/Paper[0-9]+/' + invitationId, i.id)]
        else:
            invitations = []
            for n in papers:
                new_invitation = openreview.Invitation(config.CONF + '/-/Paper{0}/'.format(n.number) + invitationId, **invitation_config['params'])

                if 'original' in invitation_config and invitation_config['original']:
                    forum = n.original
                else:
                    forum = n.forum

                if 'byForum' in invitation_config and invitation_config['byForum']:
                    new_invitation.reply['forum'] = forum

                if 'reference' in invitation_config and invitation_config['reference']:
                    new_invitation.reply['referent'] = forum

                if 'byReplyTo' in invitation_config and invitation_config['byReplyTo']:
                    new_invitation.reply['replyto'] = forum

                for field_type in ['signatures', 'readers', 'writers', 'nonreaders']:
                    if field_type in invitation_config:
                        new_invitation.reply[field_type] = {}
                        new_invitation.reply[field_type]['description'] = invitation_config[field_type].get('description', '')
                        for input_type, field_values in invitation_config[field_type].iteritems():
                            if input_type != 'description':
                                new_invitation.reply[field_type][input_type] = prepare_input(new_invitation.id, input_type, field_values)

                invitations.append(client.post_invitation(new_invitation))
            return invitations
    else:
        try:
            invitation = client.get_invitation(config.CONF + '/-/' + invitationId)
            invitation_exists = True
        except openreview.OpenReviewException as error:
            if error[0][0]['type'].lower() == 'not found':
                invitation_exists = False
            else:
                raise error

        if invitation_exists and not overwrite:
            return [invitation]
        else:
            new_invitation = openreview.Invitation(config.CONF + '/-/' + invitationId, **invitation_config['params'])
            return [client.post_invitation(new_invitation)]

def prepare_input(invitationId, input_type, field_value):
    match = re.search('.*\/-\/Paper([0-9]+)\/.*', invitationId)
    if match:
        if 'values' in input_type and type(field_value) == list:
            if 'regex' in input_type:
                return '|'.join([ val.replace('[PAPER_NUMBER]', match.group(1)) for val in field_value])
            else:
                return [val.replace('[PAPER_NUMBER]', match.group(1)) for val in field_value]
        else:
            return field_value.replace('[PAPER_NUMBER]', match.group(1))

    else:
        return field_value

def prepare_invitees(invitationId, invitees):
    match = re.search('.*\/-\/Paper([0-9]+)\/.*', invitationId)
    if match:
        return [ invitee.replace('[PAPER_NUMBER]', match.group(1)) for invitee in invitees]
    else:
        return invitees

def prepare_regex(invitationId, members):
    match = re.search('.*\/-\/Paper([0-9]+)\/.*', invitationId)
    if match:
        return '|'.join([ member.replace('[PAPER_NUMBER]', match.group(1)) for member in members])
    else:
        return members

for invitationId in invitations_to_process:
    print "processing invitation ", invitationId
    if invitationId in invitation_configurations:
        if args.enable or args.disable:
            enable = args.enable and not args.disable

            invitations = get_or_create_invitations(invitationId, args.overwrite)
            updated = 0

            if invitations:
                for i in invitations:

                    i.invitees = prepare_invitees(i.id, invitation_configurations[invitationId]['invitees']) if enable else []
                    if 'noninvitees' in invitation_configurations[invitationId]:
                        i.noninvitees = prepare_invitees(i.id, invitation_configurations[invitationId]['noninvitees'])
                    result = client.post_invitation(i)

                    pp.pprint({'Invitation ID ..': result.id, 'Invitees .......': i.invitees})
                    print '\n'
                    updated += 1
            else:
                print "Invitation not found: ", invitationId

            print "# Invitations updated: ", updated

        else:
            print "Invalid enable value: ", args.enable

    else:
        print "Invalid invitation: ", invitationId

    print '\n'




