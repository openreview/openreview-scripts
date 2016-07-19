#!/usr/bin/python

###############################################################################
# Individual reviewer invitation python script allows PCs to invite an 
# additional individual reviewer, taking any number of email addresses as 
# arguments. the script will add the email address to the reviewers-invited 
# group, and send an invitation email to the person.  PCs can run this as 
# needed.
###############################################################################

## Import statements
import argparse
import csv
import getpass
import re
import sys
sys.path.append('../..')
from client import *

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('-i','--invitee', help="the group that will be invited to review")
args = parser.parse_args()

## Initialize the client library with username and password
username = raw_input("OpenReview username (e.g. username@umass.edu): ")
password = getpass.getpass("Password: ")
or3 = Client(username,password)

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
    
    message = """You have been invited to serve as a reviewer for the International Conference on Learning Representations (ICLR) 2017 Conference.

    To ACCEPT the invitation, please click on the following link:
    
    """+url+"""Yes

    To DECLINE the invitation, please click on the following link:

    """+url+"""No

    Thank you,
    The ICLR 2017 Program Chairs

    """

    or3.send_mail("OpenReview invitation response", [reviewer], message)


