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
commitee_group_id=f'{venue_id}/Area_Chairs'
submission_invitation_id = f'{venue_id}/-/Blind_Submission'
cycle=venue_id.split('/')[-1]


client = openreview.Client(baseurl=baseurl, username=args.username, password=args.password)


active_submissions=list(openreview.tools.iterget_notes(client, invitation=f'{venue_id}/-/Blind_Submission'))

all_action_editors = set()

for paper in active_submissions:
    ac_group = client.get_group(f'{venue_id}/Paper{paper.number}/-/Area_Chairs')
    all_action_editors.update(ac_group.members)

subject = f'[ACL ARR] Reviews and Meta-reviews Due Soon ({cycle} 13th and 18th)'
message = '''Dear ACL ARR Action Editors,

Thank you very much for helping out with the reviewing process in ACL ARR! This is just a reminder that reviews are due in two days on {cycle} 13th, and meta-reviews will be due on {cycle} 18th.

Please monitor the reviewing process by logging in through the following console:
https://openreview.net/group?id={commitee_group_id}

If after the submission deadline passes you have a full slate of reviews, please proceed to write a short meta-review summarizing the result. If you notice that reviewers have not finished their reviews, please contact them ASAP using the OpenReview commenting functionality and get an ETA for them completing the reviews. If you need to assign an extra emergency reviewer, you can do so through the \"Modify Reviewer Assignments\" link in the console above. If you are not sure how to do anything, you can contact the editors at the email address below.

Thank you,
ACL ARR Editors
editors@aclrollingreview.org
'''

all_action_editors = list(all_action_editors)

print(f'Reminding {len(all_action_editors)} assigned action editors for {venue_id}')

client.post_message(subject, all_action_editors, message, parentGroup=commitee_group_id)

print('Done.')