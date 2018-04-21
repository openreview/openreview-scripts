## Import statements
import argparse
import csv
import config
import openreview
from openreview import tools

def swap_assignment(new_reviewer, papernum):
    recommend_reviewer_notes = client.get_notes(
        invitation = 'MIDL.amsterdam/2018/Conference/Paper{}/-/Recommend_Reviewer'.format(papernum))
    reviewer_invitation_notes = client.get_notes(
        invitation = 'MIDL.amsterdam/2018/Conference/-/Paper{}/Reviewer_Invitation'.format(papernum))

    valid_recommendations = [r for r in recommend_reviewer_notes if r.content['email'] == new_reviewer]
    valid_responses = [r for r in reviewer_invitation_notes if r.content['email'] == new_reviewer]

    assert len(valid_recommendations) == 1, "need exactly one recommendation by different recommenders"
    recommender = valid_recommendations[0].signatures[0]

    tools.assign(
        client,
        papernum,
        config.CONFERENCE_ID,
        reviewer_to_remove = recommender,
        reviewer_to_add = new_reviewer
    )

    paper = client.get_notes(invitation='MIDL.amsterdam/2018/Conference/-/Submission', number=papernum)[0]
    assert paper.number == papernum, "paper number doesn't match retrieved number"

    subject = '[MIDL 2018] You have been assigned to Paper {}'.format(papernum)
    message = '''Dear Reviewer,

Thank you for accepting the invitation to review for MIDL 2018.

Your review assignment can be found here:

https://openreview.net/forum?id={}

Please email the MIDL program chairs for policy questions, and info@openreview.net with technical issues.

Best,
The OpenReview Team

'''.format(paper.forum)

    client.send_mail(subject, [new_reviewer], message)

## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('new_reviewer')
parser.add_argument('papernum')
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

swap_assignment(args.new_reviewer, args.papernum)
