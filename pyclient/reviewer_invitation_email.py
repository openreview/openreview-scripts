###############################################################################
# Reviewer invitation python script sends email to all invited reviewers.  PCs 
# can edit the message and run this script themselves.
###############################################################################

import sys
import client
import requests

username = sys.argv[1]
password = sys.argv[2]
include_unconfirmed = True if len(sys.argv) < 4 else sys.argv[3]

## Initialize the client library with username and password
or3 = client.client(username, password)

messageToAll = """
Dear (prospective) reviewer,

For those of you that have accepted, we are pleased that you have decided
to participate as a reviewer for ICLR 2017. 
...
"""

messageToAccepted = """
Dear Reviewer,

Thank you for deciding to serve as a reviewer for ICLR 2017.
...
"""

if include_unconfirmed == True:
    mail = {
        'groups': ['ICLR.cc/2017/reviewers', 'ICLR.cc/2017/reviewers-invited'],
        'subject': 'A message to all invited reviewers',
        'message': messageToAll
    }
else:
    mail = {
        'groups': ['ICLR.cc/2017/reviewers'],
        'subject': 'A message to reviewers',
        'message': messageToAccepted
    }

requests.post(or3.mailUrl, json=mail, headers=or3.headers)
