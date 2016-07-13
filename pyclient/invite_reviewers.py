###############################################################################
# Individual reviewer invitation python script allows PCs to invite an 
# additional individual reviewer, taking any number of email addresses as 
# arguments. the script will add the email address to the reviewers-invited 
# group, and send an invitation email to the person.  PCs can run this as 
# needed.
###############################################################################

import sys
import re
import client
import requests

username = sys.argv[1]
password = sys.argv[2]

## Initialize the client library with username and password
or3 = client.client(username, password)

email_addresses=[]

for arg in sys.argv[3:len(sys.argv)]:
    if re.match(r"[^@]+@[^@]+\.[^@]+", arg):
        email_addresses.append(arg)
    else:
        print "Invalid email address: "+arg

requestForReviewerId = 'ICLR.cc/2017/-/request/to/review/invitation'


## For each candidate reviewer, send an email asking them to confirm or reject the request to review
for count, reviewer in enumerate(email_addresses):
    or3.addGroupMember('ICLR.cc/2017/reviewers-invited',reviewer)
    hashKey = or3.createHash(reviewer, requestForReviewerId)
    url = "http://localhost:3000/invitation?id=" + requestForReviewerId + "&email=" + reviewer + "&key=" + hashKey + "&response="
    message = "You have been invited to serve as a reviewer for the International Conference on Learning Representations (ICLR) 2017 Conference.\n\n"
    message = message+ "To ACCEPT the invitation, please click on the following link: \n\n"
    message = message+ url + "Yes\n\n"
    message = message+ "To DECLINE the invitation, please click on the following link: \n\n"
    message = message+ url + "No\n\n" + "Thank you"
    requests.post(or3.mailUrl, json={'groups': [reviewer], 'subject': "OpenReview invitation response" , 'message': message}, headers=or3.headers)
