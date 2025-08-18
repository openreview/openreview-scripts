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

maskAuthorsGroup = config.CONF + "/Paper[PAPER_NUMBER]/Authors"
maskReviewerGroup = config.CONF + "/Paper[PAPER_NUMBER]/Reviewers"
maskAreaChairGroup = config.CONF + "/Paper[PAPER_NUMBER]/Area_Chair"
maskAnonReviewerGroup = config.CONF + "/Paper[PAPER_NUMBER]/AnonReviewer[0-9]+"
maskAuthorsPlusGroup = config.CONF + "/Paper[PAPER_NUMBER]/Authors_and_Higher"
maskReviewersPlusGroup = config.CONF + "/Paper[PAPER_NUMBER]/Reviewers_and_Higher"
maskACPlusGroup = config.CONF + "/Paper[PAPER_NUMBER]/Area_Chairs_and_Higher"

invitation_configurations = {
    'Add_Revision': {
        'byPaper': True,
        'invitees': [maskAuthorsGroup],
        'params': config.add_revision_params,
        'byForum': True,
        'reference': True,
        'original': True
    },
    'Public_Comment': {
        'byPaper': True,
        'byForum': True,
        'invitees': ['~'],
        'noninvitees': [maskAuthorsGroup, maskReviewerGroup, maskAreaChairGroup],
        'params': config.public_comment_params,
        'readers': ['everyone', maskAuthorsPlusGroup, maskReviewersPlusGroup, maskACPlusGroup, config.PROGRAM_CHAIRS]
    },
    'Official_Comment': {
        'byPaper': True,
        'byForum': True,
        'invitees': [maskReviewerGroup, maskAuthorsGroup, maskAreaChairGroup, config.PROGRAM_CHAIRS],
        'signatures': [maskAnonReviewerGroup, maskAuthorsGroup, maskAreaChairGroup, config.PROGRAM_CHAIRS],
        'params': config.official_comment_params,
        'readers': ['everyone', maskAuthorsPlusGroup, maskReviewersPlusGroup, maskACPlusGroup, config.PROGRAM_CHAIRS]
    },
    'Official_Review': {
        'byPaper': True,
        'invitees': [maskReviewerGroup],
        'signatures': [maskAnonReviewerGroup],
        'byForum': True,
        'byReplyTo': True,
        'params': config.official_review_params
    },
    'Meta_Review': {
        'byPaper': True,
        'byForum': True,
        'byReplyTo': True,
        'invitees': [maskAreaChairGroup],
        'signatures': [maskAreaChairGroup],
        'params': config.meta_review_params,
        'nonreaders': [maskAuthorsGroup]
    },
    'Acceptance_Decision': {
        'byPaper': False,
        'byForum': False,
        'params': config.acceptance_decision_params,
        'invitees': []
    },
    'Add_Bid': {
        'tags': True,
        'byPaper': False,
        'invitees': [config.REVIEWERS, config.AREA_CHAIRS],
        'params': config.add_bid_params
    },
    'Withdraw_Paper': {
        'byPaper': True,
        'invitees': [maskAuthorsGroup],
        'byForum': True,
        'reference': True,
        'params': config.withdraw_paper_params
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


papers = client.get_notes(invitation = config.BLIND_SUBMISSION)

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

                if 'signatures' in invitation_config:
                    new_invitation.reply['signatures']['values-regex'] = prepare_regex(new_invitation.id, invitation_config['signatures'])
                    new_invitation.reply['writers']['values-regex'] = prepare_regex(new_invitation.id, invitation_config['signatures'])

                if 'readers' in invitation_config:
                    new_invitation.reply['readers']['value-dropdown'] = prepare_invitees(new_invitation.id, invitation_config['readers'])

                if 'nonreaders' in invitation_config:
                    new_invitation.reply['nonreaders']['values'] = prepare_invitees(new_invitation.id, invitation_config['nonreaders'])

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




