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
action_editors = f'{venue_id}/Area_Chairs'
submission_invitation_id = f'{venue_id}/-/Blind_Submission'
cycle = venue_id.split('/')[-1]

client = openreview.Client(baseurl=baseurl, username=args.username, password=args.password)

active_submissions=list(openreview.tools.iterget_notes(client, invitation=submission_invitation_id))
print(len(active_submissions))

ac_assignments = { e['id']['head']: openreview.Edge.from_json(e['values'][0]) for e in client.get_grouped_edges(invitation=f'{action_editors}/-/Assignment', groupby='head', select=None)}

no_action_editor = ''
incomplete_reviewers = ''

for submission in active_submissions:
    ac_group = client.get_group(f'{venue_id}/Paper{submission.number}/Area_Chairs')
    if not ac_group.members:
        title = submission.content['title']
        no_action_editor+=f'\n*Paper#{submission.number} {title}: https:openreview.net/forum?id={submission.id}'
    revs_group = client.get_group(f'{venue_id}/Paper{submission.number}/Reviewers')
    if ac_group.members and len(revs_group.members) < 3:
        title = submission.content['title']
        assigned_ac = ac_assignments[submission.id].tail
        incomplete_reviewers+=f'\n*Paper#{submission.number} {title}, Action Editor: {assigned_ac}, https:openreview.net/forum?id={submission.id}'
        

subject = f'ARR {cycle} Review Deadline Soon'

message = f'''Dear ACL Rolling Review Editors in Chief,

Please note that the following papers for August (where reviews are due in two days) do not yet have an action editor who has accepted the invitation. It is likely that we will need to recruit an emergency action editor for the paper. As a reminder, you can find potential action editors by going to the Program Chair Console (https://openreview.net/group?id=aclweb.org/ACL/ARR/2021/{cycle}/Program_Chairs)
{no_action_editor}

Note that the following papers have an action editor but do not have enough reviewers and may need to recruit an emergency reviewer. A reminder has already been sent to the relevant action editor, but you may want to monitor the progress of these papers to make sure they stay on track.
{incomplete_reviewers}

ACL Rolling Review Staff'''

client.post_message(subject, ['editors@aclrollingreview.org'], message)