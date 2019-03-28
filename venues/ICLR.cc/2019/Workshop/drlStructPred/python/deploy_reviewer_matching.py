#!/usr/bin/python


import argparse
import openreview
from openreview import tools
import config
import datetime

"""
OPTIONAL SCRIPT ARGUMENTS
	baseurl -  the URL of the OpenReview server to connect to (live site: https://openreview.net)
 	username - the email address of the logging in user
	password - the user's password
"""

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
print('connecting to {0}'.format(client.baseurl))

conference = config.get_conference(client)

conference.set_assignments("Test - Ni")

# Apr 5 (midnight GMT assumed)
conference.open_reviews(due_date = datetime.datetime(2019, 4, 6, 0, 0), additional_fields = {
            'rating': {
                'order': 3,
                'value-dropdown': [
                    '5: Top 15% of accepted papers, strong accept',
                    '4: Top 50% of accepted papers, clear accept',
                    '3: Marginally above acceptance threshold',
                    '2: Marginally below acceptance threshold',
                    '1: Strong rejection'
                ],
                'required': True
            },
            'confidence': {
                'order': 4,
                'value-radio': [
                    '3: The reviewer is absolutely certain that the evaluation is correct and very familiar with the relevant literature',
                    '2: The reviewer is fairly confident that the evaluation is correct',
                    '1: The reviewer\'s evaluation is an educated guess'
                ],
                'required': True
            }
})

# only Program Chairs can see Official Reviews
invites = client.get_invitations(regex=conference.get_id()+'/-/Paper.*/Official_Review')
for invite in invites:
    invite.reply['readers']={'values':[conference.get_program_chairs_id()]}
    client.post_invitation(invite)

subject = '{name} - reviews assigned'.format(name=conference.get_short_name())
message = '''Dear Reviewer,

Thank you for agreeing to review for {workshop_name}. To complete your review, log into openreview.net and go to Tasks <https://openreview.net/tasks>. Reviews are due by {end_time}.

Please make sure that your OpenReview account is updated and lists all the emails you are using.  Visit http://openreview.net/profile after logging in to view and add email addresses. You will need to login using an account that has the address this email was sent to in order to see your assignments.

If you have any OpenReview related questions, please contact info@openreview.net.

If you have workshop policy related questions, please contact {pc_email}.

Regards,
{workshop_name} Program Chairs'''.format(workshop_name=conference.get_short_name(), conf_id=conference.get_id(),
           end_time='April 5th', pc_email='crazydonkey200@gmail.com')


response = client.send_mail(subject, [conference.get_reviewers_id()], message)
print(response)
