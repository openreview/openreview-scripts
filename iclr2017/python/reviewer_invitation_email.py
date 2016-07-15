###############################################################################
# Reviewer invitation python script sends email to all invited reviewers.  PCs 
# can edit the message and run this script themselves.
###############################################################################

import sys
sys.path.append('/Users/michaelspector/projects/openreview/or3scripts/')
from client import *

## Import statements and argument handling
import argparse
parser = argparse.ArgumentParser()
parser.add_argument('username', help="your OpenReview username (e.g. michael@openreview.net)")
parser.add_argument('password', help="your OpenReview password (e.g. abcd1234)")
parser.add_argument('--recipients', help="the group that will recieve this message")
parser.add_argument('--subject', help="your email's subject line in string form (e.g. 'this is a subject line')")
parser.add_argument('--message', help="your email's message in string form (e.g. 'this is a message')")
args = parser.parse_args()


## Initialize the client library with username and password
or3 = Client(args.username, args.password)

message = """
Dear invited reviewer,

Thank you for deciding to participate as a reviewer for ICLR 2017! 
You will be notified of further instructions shortly.

Sincerely,
the ICLR 2017 program chairs
...
""" if args.message == None else args.message

subject = 'A message to reviewers' if args.subject == None else args.subject,
recipients = ['ICLR.cc/2017/reviewers'] if args.recipients == None else [args.recipients]

or3.send_mail(subject, recipients, message)