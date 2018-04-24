import argparse
import csv
import config
import openreview
from openreview import tools

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print "connecting to ", client.baseurl

message = '''Dear Reviewer,

The linked paper {} has been submitted for possible presentation at our upcoming conference https://midl.amsterdam . We would greatly appreciate your help in evaluating the submission by May 9th. Given the large number of submission we have received, we aim for an acceptance rate of around 35 - 40%. Of these accepted papers between one-third and half will be considered for the Medical Image Analysis Special Issue. During your review you can indicate whether you think the paper is suitable for this Special Issue. Also please indicate if you feel a paper is specifically suited for oral presentation over poster presentation. Please note that your review will be publicly visible on OpenReview, although you will remain anonymous.

All papers will be reviewed by three reviewers after which the program chairs will make the final decision on all papers. There will be no official rebuttal phase with revisions, but authors are allowed to comment on your reviews and you are allowed to respond.

Last, although we have tried to prevent any conflicts-of-interest, if you feel you have a conflict-of-interest in reviewing this paper, please contact one of the programmer chairs such we can re-assign this paper.

Reviewer instructions:
- To submit a review, log into https://openreview.net using this email address. Select "Tasks" under the dropdown menu under your name.  Select a paper that you've been assigned to review and press the Official Review button.
- Please complete the review by the indicated deadline using the online submission and review system.

Thank you for your help on evaluating this paper.

Sincerely, the program chairs,
Clarisa, Ivana and Geert
'''

submissions = client.get_notes(invitation='MIDL.amsterdam/2018/Conference/-/Submission')

for n in submissions:
	reviewer_group = 'MIDL.amsterdam/2018/Conference/Paper{}/Reviewers'.format(n.number)
	client.send_mail('[MIDL 2018 Conference] Review Assignment: Paper# {}'.format(n.number), [reviewer_group], message.format('https://openreview.net/forum?id='+n.forum))
	print '[MIDL 2018 Conference] Review Assignment: Paper# {}'.format(n.number)
