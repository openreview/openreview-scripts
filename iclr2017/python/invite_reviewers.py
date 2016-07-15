###############################################################################
# Individual reviewer invitation python script allows PCs to invite an 
# additional individual reviewer, taking any number of email addresses as 
# arguments. the script will add the email address to the reviewers-invited 
# group, and send an invitation email to the person.  PCs can run this as 
# needed.
###############################################################################

import sys
sys.path.append('../..')
from client import *
import re

## Import statements and argument handling
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('username', help="your OpenReview username (e.g. michael@openreview.net)")
parser.add_argument('password', help="your OpenReview password (e.g. abcd1234)")
parser.add_argument('invitee', help="the group that will be invited to review")
args = parser.parse_args()


## Initialize the client library with username and password
or3 = Client(args.username, args.password)

email_addresses=[]

if re.match(r"[^@]+@[^@]+\.[^@]+", args.invitee):
    email_addresses.append(args.invitee)
else:
    print "Invalid email address: "+arg

invitation_id = 'ICLR.cc/2017/-/reviewer_invitation'


## For each candidate reviewer, send an email asking them to confirm or reject the request to review
for count, reviewer in enumerate(email_addresses):
    or3.add_group_member('ICLR.cc/2017/reviewers-invited',reviewer)
    hashKey = or3.get_hash(reviewer, invitation_id)
    url = "http://localhost:3000/invitation?id=" + invitation_id + "&email=" + reviewer + "&key=" + hashKey + "&response="
    message = "You have been invited to serve as a reviewer for the International Conference on Learning Representations (ICLR) 2017 Conference.\n\n"
    message = message+ "To ACCEPT the invitation, please click on the following link: \n\n"
    message = message+ url + "Yes\n\n"
    message = message+ "To DECLINE the invitation, please click on the following link: \n\n"
    message = message+ url + "No\n\n" + "Thank you"
    or3.send_mail("OpenReview invitation response", [reviewer], message)