import csv
import argparse
import openreview
from openreview import tools
import config

parser = argparse.ArgumentParser()
parser.add_argument('reviewer_file')
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print('connecting to {0}'.format(client.baseurl))

conference = config.get_conference(client)

title = 'LLD @ ICLR 2019: Invitation to Review'
message = '''Dear {name},

You have been nominated by the organizers of the 2nd Learning from Limited Labeled Data (LLD) Workshop: Representation Learning for Weak Supervision and Beyond to serve as a reviewer.  As a respected researcher in the area, we hope you will accept and help us make the conference a success.

Reviewers are also welcome to submit papers, so please also consider submitting to the conference!

Key facts:
Workshop website: https://lld-workshop.github.io/
Paper submission deadline: March 15, 2019, 11.59pm, GMT+1
Review deadline: April 3, 2019
Internal discussion: April 3-5, 2019
Release of final decisions: April 5, 2019

Invited Speakers: Anima Anandkumar, Luna Dong, Alon Halevy, Luke Zettlemoyer, Stefano Ermon, Joan Bruna + more TBA

We will be using OpenReview.net and a reviewing process that we hope will be engaging and inclusive of the whole LLD community.

The success of LLD depends on the quality of the reviewing process and ultimately on the quality and dedication of the reviewers. We hope you will accept our invitation.

To ACCEPT the invitation, please click on the following link:

{accept_url}

To DECLINE the invitation, please click on the following link:

{decline_url}

Please answer within 10 days.

If you accept, please make sure that your OpenReview account is updated and lists all the emails you are using.  Visit http://openreview.net/profile after logging in.

If you have any questions, please contact the program chairs at lld2019@googlegroups.com.

Cheers!

LLD 2019 Workshop Organizers:
Isabelle Augenstein
Stephen Bach
Matthew Blaschko
Eugene Belilovsky
Edouard Oyallon
Anthony Platanios
Alex Ratner
Christopher Re
Xiang Ren
Paroma Varma

Contact:
Email: lld2019@googlegroups.com
Website: https://lld-workshop.github.io
'''

suggested_reviewers = []
with open(args.reviewer_file) as f:
    for row in csv.reader(f):
        suggested_reviewers.append(row[0])

formatted_emails=[m.lower() for m in suggested_reviewers]

ids = []
for member in formatted_emails:
    profile = tools.get_profile(client, member)
    if profile:
        ids.append(profile.id)
        formatted_emails.remove(member)

members = ids + formatted_emails

#print(members)
print('Reviewers to invite {0}'.format(len(members)))
conference.recruit_reviewers(emails = members, title = title, message = message)
