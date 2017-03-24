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

maskPaperGroup = CONFERENCE + "/Paper[PAPER_NUMBER]"
maskAuthorsGroup = maskPaperGroup + "/Authors"


def get_open_comment_invitation(submissionId, number, authorsGroupId):

	allGroups = [COCHAIRS, PC, SPC, authorsGroupId]
	reply = {
    	'forum': submissionId,
      	'signatures': {
        	'values-regex': '|'.join(allGroups),
        	'description': 'How your identity will be displayed with the above content.'
      	},
      		'writers': {
      		'values-regex': '|'.join(allGroups)
      	},
      	'readers': {
        	'values': allGroups,
        	'description': 'The users who will be allowed to read the above content.'
      	},
      	'content': {
        	'title': {
          		'order': 1,
          		'value-regex': '.{1,500}',
          		'description': 'Brief summary of your comment.',
          		'required': True
       		},
        	'comment': {
          		'order': 2,
          		'value-regex': '[\\S\\s]{1,5000}',
          		'description': 'Your comment or reply.',
          		'required': True
        	}
      	}
    }

	invitation = openreview.Invitation(id = CONFERENCE + '/-/Paper' + str(number) + '/Open/Comment',
		signatures = [CONFERENCE],
		writers = [CONFERENCE],
		invitees = [],
		noninvitees = [],
		readers = ['everyone'],
		process = '../process/commentProcess.js',
		reply = reply)

	return invitation

def get_confidential_comment_invitation(submissionId, number, authorsGroupId):

	allGroups = [COCHAIRS, PC, SPC]
	reply = {
    	'forum': submissionId,
      	'signatures': {
        	'values-regex': '|'.join(allGroups),
        	'description': 'How your identity will be displayed with the above content.'
      	},
      		'writers': {
      		'values-regex': '|'.join(allGroups)
      	},
      	'readers': {
        	'values': allGroups,
        	'description': 'The users who will be allowed to read the above content.'
      	},
      	'nonreaders': {
        	'values': [authorsGroupId]
      	},
      	'content': {
        	'title': {
          		'order': 1,
          		'value-regex': '.{1,500}',
          		'description': 'Brief summary of your comment.',
          		'required': True
       		},
        	'comment': {
          		'order': 2,
          		'value-regex': '[\\S\\s]{1,5000}',
          		'description': 'Your comment or reply.',
          		'required': True
        	}
      	}
    }

	invitation = openreview.Invitation(id = CONFERENCE + '/-/Paper' + str(number) + '/Confidential/Comment',
		signatures = [CONFERENCE],
		writers = [CONFERENCE],
		invitees = [],
		noninvitees = [authorsGroupId],
		readers = ['everyone'],
		process = '../process/commentProcess.js',
		reply = reply)

	return invitation


def get_recommend_reviewer_invitation(submissionId, number):

	reply = {
    	'forum': submissionId,
      	'signatures': {
        	'values-regex': '~.*',
        	'description': 'How your identity will be displayed with the above content.'
      	},
      		'writers': {
      		'values-regex': '~.*'
      	},
      	'readers': {
        	'values': '~.*',
        	'description': 'The users who will be allowed to read the above content.'
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

	invitation = openreview.Invitation(id = CONFERENCE + '/-/Paper' + str(number) + '/Recommend/Reviewer',
		duedate = 1507180500000,
		signatures = [CONFERENCE],
		writers = [CONFERENCE],
		invitees = [],
		noninvitees = [],
		readers = ['everyone'],
		multiReply = True,
		reply = reply)

	return invitation

def get_official_review_invitation(submissionId, number, authorsGroupId, reviewerNonReadersGroupId):

	reply = {
    	'forum': submissionId,
      	'replyto': submissionId,
      	'writers': {
      		'values': [CONFERENCE]
      	},
      	'signatures': {
      		'values-regex': CONFERENCE + '/Paper' + str(number) + '/AnonReviewer[0-9]+'
      	},
      	'readers': {
        	'values': [COCHAIRS, SPC, PC, authorsGroupId],
        	'description': 'The users who will be allowed to read the above content.'
      	},
	    'nonreaders': {
	    	'values': [reviewerNonReadersGroupId]
	    },
      	'content': {
        	'title': {
          		'order': 1,
          		'value-regex': '.{1,500}',
          		'description': 'Brief summary of your review.',
          		'required': True
        	},
        	'review': {
         		'order': 2,
          		'value-regex': '[\\S\\s]{1,5000}',
          		'description': 'Please provide an evaluation of the quality, clarity, originality and significance of this work, including a list of its pros and cons.',
          		'required': True
        	},
        	'rating': {
          		'order': 3,
          		'value-dropdown': [
		            '10: Top 5% of accepted papers, seminal paper',
		            '9: Top 15% of accepted papers, strong accept',
		            '8: Top 50% of accepted papers, clear accept',
		            '7: Good paper, accept',
		            '6: Marginally above acceptance threshold',
		            '5: Marginally below acceptance threshold',
		            '4: Ok but not good enough - rejection',
		            '3: Clear rejection',
		            '2: Strong rejection',
		            '1: Trivial or wrong'
          		],
          		'required': True
        	},
        	'confidence': {
          	'order': 4,
          	'value-radio': [
	            '5: The reviewer is absolutely certain that the evaluation is correct and very familiar with the relevant literature',
	            '4: The reviewer is confident but not absolutely certain that the evaluation is correct',
	            '3: The reviewer is fairly confident that the evaluation is correct',
	            '2: The reviewer is willing to defend the evaluation, but it is quite likely that the reviewer did not understand central parts of the paper',
	            '1: The reviewer\'s evaluation is an educated guess'
          	],
          	'required': True
        }
      }
    }

	invitation = openreview.Invitation(id = CONFERENCE + '/-/Paper' + str(number) + '/Official/Review',
		duedate = 1507180500000,
		signatures = [CONFERENCE],
		writers = [CONFERENCE],
		invitees = [],
		noninvitees = [],
		readers = ['everyone'],
		process = '../process/reviewProcess.js',
		reply = reply)

	return invitation

def get_meta_review_invitation(submissionId, number, authorsGroupId, areachairGroupId):

	reply = {
    	'forum': submissionId,
      	'replyto': submissionId,
      	'writers': {
      		'values-regex': areachairGroupId
      	},
      	'signatures': {
      		'values-regex': areachairGroupId
      	},
      	'readers': {
        	'values': [COCHAIRS, authorsGroupId],
        	'description': 'The users who will be allowed to read the above content.'
      	},
      	'content': {
        	'title': {
          		'order': 1,
		        'value-regex': '.{1,500}',
		        'description': 'Brief summary of your review.',
		        'required': True
        	},
        	'metareview': {
          		'order': 2,
          		'value-regex': '[\\S\\s]{1,5000}',
          		'description': 'Please provide an evaluation of the quality, clarity, originality and significance of this work, including a list of its pros and cons.',
          		'required': True
        	},
        	'recommendation': {
          		'order': 3,
          		'value-dropdown': [
            		'Accept',
            		'Reject'
          		],
          		'required': True
        	},
        	'format': {
          		'order': 4,
          		'value-radio': [
            		'Poster',
            		'Oral'
          		],
          		'required': True
        	},
        	'best paper':{
          		'order': 5,
          		'description': 'Nominate as best paper (if student paper, nominate for best student paper)',
          		'value-radio': [
            		'Yes',
            		'No'
          		],
          		'required': True
        	}
      	}
    }

	invitation = openreview.Invitation(id = CONFERENCE + '/-/Paper' + str(number) + '/Meta/Review',
		duedate = 1507180500000,
		signatures = [CONFERENCE],
		writers = [CONFERENCE],
		invitees = [],
		noninvitees = [],
		readers = [CONFERENCE, SPC, COCHAIRS],
		process = '../process/metaReviewProcess.js',
		reply = reply)

	return invitation


## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()


client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)


try:

  submissions = client.get_notes(invitation = SUBMISSION)

  for submission in submissions:

  	print "Processing submission", submission.number

  	paper_group = client.get_group(id = maskPaperGroup.replace('[PAPER_NUMBER]', str(submission.number)))

  	if paper_group:

  		author_group = client.get_group(id = maskAuthorsGroup.replace('[PAPER_NUMBER]', str(submission.number)))

  		if author_group:
  			# Post the necessary groups
  			reviewers_group = openreview.Group(id = paper_group.id + '/Reviewers',
  				signatures = [CONFERENCE],
  				writers = [CONFERENCE],
  				members = [],
  				readers = [CONFERENCE, COCHAIRS, SPC, paper_group.id + '/Reviewers'],
  				signatories = [])

  			client.post_group(reviewers_group)

  			reviewers_nonreaders_group = openreview.Group(id = reviewers_group.id + '/NonReaders',
  				signatures = [CONFERENCE],
  				writers = [CONFERENCE],
  				members = [],
  				readers = [CONFERENCE, COCHAIRS, SPC, reviewers_group.id + '/NonReaders'],
  				signatories = [])

  			client.post_group(reviewers_nonreaders_group)

  			areachair_group = openreview.Group(id = paper_group.id + '/Area_Chair',
  				signatures = [CONFERENCE],
  				writers = [CONFERENCE],
  				members = [],
  				readers = [CONFERENCE, COCHAIRS, SPC],
  				signatories = [CONFERENCE, paper_group.id + '/Area_Chair'])

  			client.post_group(areachair_group)

  			#Post open comment invitation
  			client.post_invitation(get_open_comment_invitation(submission.id, submission.number, author_group.id))
  			#Post confidential comment invitation
  			client.post_invitation(get_confidential_comment_invitation(submission.id, submission.number, author_group.id))
  			#Post recommend reviewer invitation
  			client.post_invitation(get_recommend_reviewer_invitation(submission.id, submission.number))
  			#Post official review invitation
  			client.post_invitation(get_official_review_invitation(submission.id, submission.number, author_group.id, reviewers_nonreaders_group.id))
  			#Post meta review invitation
  			client.post_invitation(get_meta_review_invitation(submission.id, submission.number, author_group.id, areachair_group.id))
  		else:
  			print "Author group not found", submission.number
  	else:
  		print "Paper group not found ", submission.number
except openreview.OpenReviewException as e:
    print "There was an error running the script: ", e






