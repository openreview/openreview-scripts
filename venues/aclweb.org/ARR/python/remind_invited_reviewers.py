import argparse
import openreview
from Crypto.Hash import HMAC, SHA256


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
parser.add_argument('-v','--venue', required=True)
parser.add_argument('-s','--seed', required=True)

args = parser.parse_args()
baseurl=args.baseurl
venue_id=args.venue
seed=args.seed
commitee_group_id=f'{venue_id}/Reviewers'
recruitment_invitation_id = f'{commitee_group_id}/-/Assignment_Recruitment'
cycle=venue_id.split('/')[-1]


client = openreview.Client(baseurl=baseurl, username=args.username, password=args.password)


invited_edges=list(openreview.tools.iterget_edges(client, invitation=f'{commitee_group_id}/-/Invite_Assignment', label='Invitation Sent'))

print(f'Reminding {len(invited_edges)} invited reviewers for {venue_id}')

for edge in invited_edges:

    submission = client.get_note(edge.head)

    hashkey = HMAC.new(seed.encode('utf-8'), msg=edge.tail.encode('utf-8'), digestmod=SHA256).hexdigest()

    # build the URL to send in the message
    url = f'https://openreview.net/invitation?id={recruitment_invitation_id}&user={edge.tail}&key={hashkey}&submission_id={edge.head}&inviter={edge.tauthor}&response='

    subject = f'[ARR 2021 - {cycle}] Reminder invitation to review paper titled {submission.content["title"]}'
    message = f'''Dear {{{{fullname}}}},

Thank you as always for your help as a reviewer for ACL Rolling Review.

You have been assigned to be a reviewer for paper number: {submission.number}, title: {submission.content['title']}.
Abstract: {submission.content['abstract']}

If you will be able to review the paper by the deadline of *September 15th* please click below:
{url}Yes

If you are unavailable or not qualified to review the paper, you can indicate this by clicking the link below, and we will assign a separate reviewer (although of course we hope that you can assist!):
{url}No

Thanks again,
ACL ARR Editors'''

    client.post_message(subject, [edge.tail], message, parentGroup=commitee_group_id)

print('Done.')