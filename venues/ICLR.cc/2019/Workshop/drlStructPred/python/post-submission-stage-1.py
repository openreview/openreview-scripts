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

conference.close_submissions()
conference.set_authors()

print('replacing members with IDs')
reviewers_group = client.get_group(conference.get_reviewers_id())
openreview.tools.replace_members_with_ids(client, reviewers_group)

conference.create_blind_submissions()

conference.open_bids(due_date = datetime.datetime(2019, 3, 25, 23, 59))

subject = 'Subject: {name} - Reviewer bidding'.format(name=conference.get_short_name())
message = '''Dear Reviewer,

This is to inform you that the bidding for {workshop_name} has begun. You are requested to place your bids by {end_time}.  To bid, please login on openreview.net and use this link: https://openreview.net/invitation?id={conf_id}/-/Bid.

Please make sure that your OpenReview account is updated and lists all the emails you are using.  Visit http://openreview.net/profile after logging in to view and add email addresses. You will need to login using an account that has the address this email was sent to in order to see your assignments.

Please reach out to us at {pc_email} if you have any policy questions.
For any OpenReview related issues please reach out at info@openreview.net.

Thank you!
{workshop_name} Program Chairs
'''.format(workshop_name=conference.get_short_name(), conf_id=conference.get_id(),
           end_time='March 25 23:59 GMT', pc_email='crazydonkey200@gmail.com ')

response = client.send_mail(subject, [conference.get_reviewers_id()], message)
print(response)