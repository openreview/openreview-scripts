import argparse
import openreview
from datetime import datetime
from datetime import timedelta

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

args = parser.parse_args()
baseurl=args.baseurl
venue_id=args.venue
commitee_group_id=f'{venue_id}/Reviewers'
submission_invitation_id = f'{venue_id}/-/Submission'
currentMonth = datetime.now().strftime("%B")
cycle = venue_id.split('/')[-1]


client = openreview.Client(baseurl=baseurl, username=args.username, password=args.password)


active_submissions=list(openreview.tools.iterget_notes(client, invitation=submission_invitation_id))

all_reviewers = set()

for paper in active_submissions:
    reviewer_group = client.get_group(f'{venue_id}/Paper{paper.number}/Reviewers')
    all_reviewers.update(reviewer_group.members)

subject = f'[ACL ARR] Reviews Due Soon ({currentMonth} 13)'
message = f'''Dear ACL ARR Reviewers,

Thank you very much for helping out with the reviewing process in ACL ARR! This is just a reminder that your reviews are due on {currentMonth} 13th.

If you have not completed the reviews, please log in through the following console and submit the reviews as soon as possible:
https://openreview.net/group?id={commitee_group_id}

If you have any questions you can contact the action editor assigned to your paper by adding a comment on the page for the corresponding paper and selecting the \"Area Chair\" as the reader.

Thank you,
ACL ARR Editors'''

all_reviewers = list(all_reviewers)

print(f'Reminding {len(all_reviewers)} assigned reviewers for {venue_id}')

client.post_message(subject, all_reviewers, message, parentGroup=commitee_group_id)

print('Done.')