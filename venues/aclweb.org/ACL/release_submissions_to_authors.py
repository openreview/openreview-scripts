import argparse
from importlib.util import decode_source
from re import sub
import openreview
from tqdm import tqdm
import csv
import tracks

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

# Get all Ethics Review invitations 
acl_ethics_review_invitations = list(openreview.tools.iterget_invitations(client, regex= 'aclweb.org/ACL/2022/Conference/Paper.*/-/Ethics_Review'))
acl_decision_invitations = list(openreview.tools.iterget_invitations(client, regex= 'aclweb.org/ACL/2022/Conference/Paper.*/-/Decision'))

acl_ethics_reviews = list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/ACL/2022/Conference/Paper.*/-/Ethics_Review'))
acl_decisions = list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/ACL/2022/Conference/Paper.*/-/Decision'))

acl_decisions_dict = {d.invitation: d for d in acl_decisions}
acl_ethics_dict = {d.invitation: d for d in acl_ethics_reviews}


invitations_by_forum = {}
original_acl_invitation = client.get_invitation('aclweb.org/ACL/2022/Conference/-/Submission')
original_acl_invitation.reply['readers'] = {"values-regex": ".*"
  }
client.post_invitation(original_acl_invitation)
for acl_decision_invitation in acl_decision_invitations: 
    invitations_by_forum[acl_decision_invitation.reply['forum']] = {'decision': acl_decision_invitation}

for acl_ethics_review_invitation in acl_ethics_review_invitations: 
    invitations_by_forum[acl_ethics_review_invitation.reply['forum']]['ethics'] = acl_ethics_review_invitation
    


acl_blind_submissions = list(openreview.tools.iterget_notes(client, invitation = 'aclweb.org/ACL/2022/Conference/-/Blind_Submission'))

# For each submission, add the authors of the original ARR submission to the readers of the blind submission 
for acl_blind_submission in tqdm(acl_blind_submissions): 
    author_group = f'aclweb.org/ACL/2022/Conference/Paper{acl_blind_submission.number}/Authors'
    # Need to add authors to ethics review invitation as readers
    invitations = invitations_by_forum[acl_blind_submission.forum]
    ethics = invitations.get('ethics')
    if ethics: 
        if author_group not in ethics.reply['readers']['values-copied']:
            ethics.reply['readers']['values-copied'].append(author_group)
            client.post_invitation(ethics)
        # Add authors as readers of ethics review 
        ethics_review = acl_ethics_dict.get(ethics.id)
        if ethics_review:
            if author_group not in ethics_review.readers:
                ethics_review.readers.append(author_group)
                client.post_note(ethics_review)

    # Need to add authors to decision invitation as readers
    decision = invitations['decision']
    if author_group not in decision.reply['readers']['values']:
        decision.reply['readers']['values'].append(author_group)
        client.post_invitation(decision)
    
    # Add authors as readers of blind submission
    if author_group not in acl_blind_submission.readers:
        acl_blind_submission.readers.append(author_group)
        acl_blind_submission.content = {
                    "authorids" : [f"aclweb.org/ACL/2022/Conference/Paper{acl_blind_submission.number}/Authors"],
                    "authors":["Anonymous"]
                }
        client.post_note(acl_blind_submission)
    
    

    # Add authors as readers of the decision note 
    decision_note = acl_decisions_dict.get(decision.id)
    if decision_note:
        if author_group not in decision_note.readers: 
            decision_note.readers.append(author_group)
            client.post_note(decision_note)
   
   # Add authors as readers of original submission
    original_submission = client.get_note(acl_blind_submission.original)
    if author_group not in original_submission.readers:
        original_submission.readers.append(author_group)
        client.post_note(original_submission)
    
    # Make authors signatories and readers of the author group 
    group = client.get_group(author_group)
    group.signatories = ['aclweb.org/ACL/2022/Conference', author_group]
    group.readers = ['aclweb.org/ACL/2022/Conference', author_group]
    client.post_group(group)

    
        