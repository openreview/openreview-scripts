#!/usr/bin/python

###############################################################################
# Not to spec
###############################################################################

## Import statements
import argparse
import csv
import getpass
import sys
import re
import openreview
import requests
from uaidata import *

maskAuthorsGroup = CONFERENCE + "/Paper[PAPER_NUMBER]/Authors"
maskReviewerGroup = CONFERENCE + "/Paper[PAPER_NUMBER]/Reviewers"
maskAreaChairGroup = CONFERENCE + "/Paper[PAPER_NUMBER]/Area_Chair"

invitation_invitees = {
	'Open/Comment': { 'byPaper': True, 'invitees': [COCHAIRS, SPC, PC, maskAuthorsGroup] },
	'Review/Open/Comment': { 'byPaper': True, 'invitees': [COCHAIRS, SPC, PC, maskAuthorsGroup] },
	'Confidential/Comment': { 'byPaper': True, 'invitees': [COCHAIRS, maskAreaChairGroup, maskReviewerGroup] },
	'Add/Bid': { 'tags': True, 'byPaper': False, 'invitees': [SPC, PC] },
	'Recommend/Reviewer': { 'tags': True, 'byPaper': True, 'invitees': [maskAreaChairGroup] },
	'Submit/Review': { 'byPaper': True, 'invitees': [maskReviewerGroup] },
	'Meta/Review': { 'byPaper': True, 'invitees': [maskAreaChairGroup] },
	'Add/Revision': { 'byPaper': True, 'invitees': [maskAuthorsGroup] }
}

def get_invitations(invitationId):

	config = invitation_invitees[invitationId]
	if config['byPaper']:
		invitations = client.get_invitations(regex = CONFERENCE + '/-/Paper.*/' + invitationId, tags = config.get('tags'))
		return [i for i in invitations if re.match(CONFERENCE + '/-/Paper[0-9]+/' + invitationId, i.id)]
	else:
		invitation = client.get_invitation(CONFERENCE + '/-/' + invitationId)
		return [invitation]

def prepare_invitees(invitationId, invitees):
	match = re.search('.*\/-\/Paper([0-9]+)\/.*', invitationId)
	if match:
		return [ invitee.replace('[PAPER_NUMBER]', match.group(1)) for invitee in invitees]
	else:
		return invitees

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('invitation', help="invitation id: " + ", ".join(invitation_invitees.keys()))
parser.add_argument('enable', help="true or false")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

if args.invitation in invitation_invitees:
	if args.enable in ['true', 'false']:
		invitationId = args.invitation
		enable = True if args.enable == 'true' else False

		client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

		invitations = get_invitations(invitationId)
		updated = 0

		if invitations:
			for i in invitations:
				i.invitees = prepare_invitees(i.id, invitation_invitees[invitationId]['invitees']) if enable else []
				print 'invitees', i.invitees
				result = client.post_invitation(i)
				print "Invitation updated successfully", result.id
				updated += 1
		else:
			print "Invitation not found", invitationId

		print "#invitations updated", updated

	else:
		print "Invalid enable value", args.enable

else:
	print "Invalid invitation", args.invitation




