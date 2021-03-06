import sys, os
import argparse
import openreview
import config

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print('connecting to {0}'.format(client.baseurl))

conference = config.get_conference(client)

formatted_acs = []

title = 'MIDL 2019: Invitation to Review'
message = '''
Dear {name},

We are organizing the second Medical Imaging with Deep Learning conference in London. This year, we wanted to create an exclusive list of reviewers, hand-picked by the area chairs. You have been nominated by the area chairs of the International Conference on Medical Imaging with Deep Learning (MIDL), and we send this message to invite you to serve as a reviewer.  As a respected researcher in this area, we hope you will accept and help us make the conference a success.

Reviewers are also welcome to submit papers, so please also consider submitting to the conference!

Key facts:
Conference web site: https://2019.midl.io/
Paper submission deadline: December 13
Review deadline: January 28
Rebuttal and discussion: January 28 - February 4
Discussion between ACs and reviewers: February 4 - February 13
Release of final decisions: February 20

We will be using OpenReview.net and a reviewing process that we hope will be engaging and inclusive of the whole MIDL community.

The success of MIDL depends on the quality of the reviewing process and ultimately on the quality and dedication of the reviewers. We hope you will accept our invitation.

To ACCEPT the invitation, please click on the following link:

{accept_url}

To DECLINE the invitation, please click on the following link:

{decline_url}

Please answer within 10 days.

If you accept, please make sure that your OpenReview account is updated and lists all the emails you are using.  Visit http://openreview.net/profile after logging in.

If you have any questions, please contact the program chairs at program-chairs@midl.io.

Cheers!

Ipek Oguz, Gozde Unal and Ender Konukoglu
Program Chairs for Medical Imaging with Deep Learning 2019

'''

group = client.get_group(id = conference.get_reviewers_id())

group.writers = [conference.id, conference.get_program_chairs_id(), conference.get_area_chairs_id()]

formatted_members = [m.lower() if '@' in m else m for m in group.members]
group.members = formatted_members

group = client.post_group(group)

print('Reviewers to invite {0}'.format(len(group.members)))
conference.recruit_reviewers(emails = group.members, title = title, message = message, reviewer_accepted_name = 'Accepted')
