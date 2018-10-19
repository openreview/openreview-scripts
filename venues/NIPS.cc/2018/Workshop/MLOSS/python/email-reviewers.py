#!/usr/bin/python

"""
Sends an email to the members of the group of your choice.

"""

## Import statements
import argparse
import config
import csv

from openreview import *

## Handle the arguments
parser = argparse.ArgumentParser()
parser.add_argument('assignments', help="a csv file containing reviewer assignments ")
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

## Initialize the client library with username and password
if args.username!=None and args.password!=None:
    client = Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
	client = Client(baseurl=args.baseurl)

print(client.baseurl)
#################################################
#                                               #
#   EDIT YOUR MESSAGE AND SUBJECT LINE BELOW    #
#                                               #
#################################################


subjectline = "Machine Learning Open Source Software 2018: paper review reminder"
def reviewer_email_message():
    message = """Dear reviewers,

Thank you again for being a reviewer for the MLOSS workshop at NIPS 2018.

We received an impressive 29 submissions. Since this number is higher than we expected, we are aiming for only 2 reviews per submission, which means that the number of assignments per reviewer is limited to roughly 4. The review process will be dealt using OpenReview.net.

If you feel that you can’t review one more more your assigned submissions (too many submissions, conflict of interest, or any other reason) please let us know as soon as possible. We ask you to finish your reviews by Saturday 20 October.

Note that our workshop is a bit different to classical NIPS workshops: it is all about software and communities. The submissions do not require thorough math and grammar checking. Instead, we have prepared a set of aspects that you might want to consider. These aspects include:
- Open-source. The presented software should be open-source. This means a) it should be accessible by you b) it should have a proper LICENSE file or some other notion of open-source license. This is mandatory.
- Matching the workshop topic. Please evaluate whether the submission showcases sustainability and/or community aspects. In particular those that might be interesting to learn from for other projects. Submissions that solely describe a new software package, but do not touch on the workshop topic are also welcome, though should receive a slightly lower score.
- Suitability for talk/demo. Is the submission a good candidate to have a 15-20 minute talk? Would you like to see it presented as part of the demo session?
- Content feedback. What aspects of the submission would you like to see presented by the authors?
- Questions. Please write down one or two questions you have about the project.

We will invite some of the submissions to be presented as posters, as talks, and as demos. In these reviews, we will need your help to identify the best submissions and what would be their best presentation style. Each paper should be assigned the standard score and confidence. In addition, we ask you for recommendations on the type of presentations, where you can choose
- Poster spotlight
- Talk
- Demo

All accepted submissions will be invited to present a poster.

To submit a review in OpenReview, log in at https://openreview.net/login. Select \"Tasks\" from the top menubar.  Select \"Show pending tasks\", then select a task to see the paper and the review form.

Thanks a lot for your help,
MLOSS at NIPS 2018 chairs
"""
    return message

reminder_msg = """Dear reviewers,

Thank you for being a reviewer for the MLOSS workshop at NIPS 2018.

This is a friendly reminder that the review due is Saturday 20 Oct 2018. If you're unable to submit your review or you can't review some of submission to whatever reason, please contact Sergey Lisitsyn <lisitsyn.s.o@gmail.com> or Heiko Strathmann <heiko.strathmann@gmail.com>.

If you have already completed your reviews, please ignore this mail.

Thank you for your help,
MLOSS 2018 chairs"""
#################################################
#                                               #
#               END OF MESSAGE                  #
#                                               #
#################################################


## send email to each reviewer
email_addrs = []
with open(args.assignments, 'r') as csvfile:
    reader = csv.reader(csvfile, delimiter=',')
    for row in reader:
        email_addrs.append(row[0])
email_set = set(email_addrs)
email_addrs = list(email_set)

response = client.send_mail(subjectline, email_addrs, reminder_msg)
#response = client.send_mail(subjectline, ['pmandler@umass.edu'], reminder_msg)
print(response)