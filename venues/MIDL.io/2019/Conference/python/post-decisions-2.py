#!/usr/bin/python

###############################################################################

###############################################################################

## Import statements
import argparse
import csv
import config
import datetime
from openreview import *
from openreview import tools



## Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('assignments', help="either (1) a csv file containing submission decisions or (2) a string of the format '<paper#>,<decision>' e.g. '23,Reject'")
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

## Initialize the client library with username and password
client = Client(baseurl=args.baseurl, username=args.username, password=args.password)
print("Connecting to "+client.baseurl)
conference = config.get_conference(client)

# gets deleted and regular notes
all_notes = client.get_notes(invitation=conference.get_submission_id(), trash=True)
submissions = {}
for paper in all_notes:
    submissions[str(paper.number)] = paper

all_decisions = client.get_notes(invitation=conference.get_id() + '/-/Paper.*/Decision')
decisions = {}
for note in all_decisions:
    paper_num = note.invitation.split('/Paper')[1].split('/')[0]
    decisions[paper_num] = note

all_meta = client.get_notes(invitation=conference.get_id() + '/-/Paper.*/Meta_Review')
meta_decisions = {}
for note in all_meta:
    paper_num = note.invitation.split('/Paper')[1].split('/')[0]
    meta_decisions[paper_num] = note

subject_line = "MIDL Submission paper visibility"
message ='''Dear Author,

Your paper has been reinstated, but is ONLY visible to you and the Program Chairs.  This way you can see the reviews and the information leading to the decision.
Sincerely,
Program Chairs for MIDL 2019.'''


##############################################################################
def submission_invite_can_hide():
    ## allow readers to just be PCs and authors
    invite = client.get_invitation(id = conference.get_submission_id())
    if 'values' in invite.reply['readers']:
        del invite.reply['readers']['values']
    invite.reply['readers']['values-copied'] = ['everyone',
                                                  conference.get_program_chairs_id(),
                                                  '{content.authorids}']
    client.post_invitation(invite)

def decision_invite_add_comment():
    ## add comments to decision invitations
    invites = client.get_invitations(regex = conference.get_id() + '/-/Paper.*/Decision')
    for invite in invites:
        paper_num = invite.id.split('/Paper')[1].split('/')[0]
        if 'values' in invite.reply['readers']:
            del invite.reply['readers']['values']
        if 'values-copied' in invite.reply['readers']:
            del invite.reply['readers']['values-copied']
        invite.reply['readers']['values-dropdown'] = ['everyone',
                                                    conference.get_program_chairs_id(),
                                                    conference.get_id() + '/Paper' + paper_num + '/Authors']
        invite.reply['content']['comment'] = {
                    'order': 4,
                    'value-regex': '[\\S\\s]{0,5000}',
                    'required': False
                }
        client.post_invitation(invite)

def hide_meta_reviews():
    # make meta-reviews private again
    # update invites
    invites = client.get_invitations(regex=conference.get_id() + '/-/Paper.*/Meta_Review')
    for invite in invites:
        paper_num = invite.id.split('/Paper')[1].split('/')[0]
        invite.reply['readers'] = [conference.get_id(), conference.get_program_chairs_id(),
                                   (conference.get_id() + '/Paper' + paper_num + '/Area_Chairs')]
        client.post_invitation(invite)
    # update notes
    notes = client.get_notes(invitation=conference.get_id() + '/-/Paper.*/Meta_Review')
    for note in notes:
        paper_num = note.invitation.split('/Paper')[1].split('/')[0]
        note.readers = [conference.get_id(), conference.get_program_chairs_id(),
                        (conference.get_id() + '/Paper' + paper_num + '/Area_Chairs')]
        client.post_note(note)

def was_rejected_and_removed(paper_num, decision):
    if paper_num not in submissions.keys():
        print("lost " + paper_num)
        return False
    else:
        paper = submissions[paper_num]
        if (decision == "Reject" or decision == "LP Accept / Borderline") \
                and paper.content.get('remove if rejected', False):
            return True
    return False

def revive_paper(paper_num):
    # change removed papers to secret, seen only by authors and PCs
    paper = submissions[paper_num]
    paper.ddate = None
    paper.readers = [conference.get_program_chairs_id(),
                     conference.get_id() + '/Paper' + paper_num + '/Authors']
    client.post_note(paper)
    print("Revived "+paper_num)


def post_rejection(paper_num, add_text):
    if paper_num in decisions.keys():
        print("Error: Decision already posted: " + paper_num)
    else:
        # post decision
        paperinv = conference.get_id() + '/-/Paper' + paper_num + '/Decision'
        decision_note = openreview.Note(
            invitation=paperinv,
            forum=submissions[paper_num].id,
            signatures=[conference.get_program_chairs_id()],
            writers=[conference.get_id()],
            readers=[conference.get_program_chairs_id(), conference.get_id() + '/Paper' + paper_num + '/Authors'],
            content={'title': 'Acceptance Decision',
                     'decision': 'Reject',
                     'comment': add_text}
        )
        decisions[paper_num] = client.post_note(decision_note)
        print("Post decision "+paper_num)

def add_meta_comment_to_decision(paper_num):
    if paper_num in meta_decisions.keys():
        decision = decisions[paper_num]
        if 'comment' not in decision.content.keys() or not decision.content['comment']:
            meta_note = meta_decisions[paper_num]
            decision.content['comment'] = meta_note.content['metareview']
            print("Add comment to "+paper_num)
            client.post_note(decision)


##################################################################
submission_invite_can_hide()
decision_invite_add_comment()
hide_meta_reviews()
if args.assignments.endswith('.csv'):
    with open(args.assignments, 'r') as csvfile:
        reader = csv.reader(csvfile, delimiter=',')
        # skip header row
        next(reader,None)
        for row in reader:
            paper_number = row[1]
            decision = row[12]
            if len(row) >= 14:
                add_text = row[13]
            else:
                add_text = ""
            if was_rejected_and_removed(paper_number, decision):
                revive_paper(paper_number)
                post_rejection(paper_number, add_text)
                # email removed paper authors
                response = client.send_mail(subject_line, [conference.get_id()+'/Paper'+paper_num+'/Authors'], message)
            # add meta_comment to all papers
            add_meta_comment_to_decision(paper_number)
else:
    paper_number = args.assignments.split(',')[1]
    decision = args.assignments.split(',')[0]
    if was_rejected_and_removed(paper_number, decision):
        revive_paper(paper_number)
        post_rejection(paper_number, "")
