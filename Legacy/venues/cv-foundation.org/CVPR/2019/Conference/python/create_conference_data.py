import openreview
from openreview import tools
from cvpr2019 import *

## CVPR 2019 only used OR for creating a match.   They sent files that reprsent reviewers
## papers and other things pertaining to setting up the matcher.   They are in ../data
##  This script creates the necessary db objects for the top-level conference groups, the papers, and
## the reviewer group.   It reads the papers from the o-papers.csv file and the reviewers from the
## o-reviewers.csv file.


client = openreview.Client(baseurl='http://openreview.localhost', username='OpenReview.net', password='d0ntf33dth3tr0lls')
print(client)

## User groups

# post the groups in the conference's path
groups = openreview.tools.build_groups(CONF_ID)
for group in groups:
    try:
        existing_group = client.get_group(group.id)
    except openreview.OpenReviewException as e:
        posted_group = client.post_group(group)
        print(posted_group.id)

# Create groups for PCs, ACs, and reviewers
# N.B. The groups for the conference are included in the list.  The newly created group is last in the list
pcs_group = openreview.tools.build_groups(PC_ID)[-1] # last one in list is the PC group
acs_group = openreview.tools.build_groups(AC_ID)[-1] # AC group is last
reviewers_group = openreview.tools.build_groups(REVIEWERS_ID)[-1] # reviewers group is last
client.post_group(pcs_group)
client.post_group(acs_group)
client.post_group(reviewers_group)
pcs_group = client.get_group(PC_ID)
acs_group = client.get_group(AC_ID)
reviewers_group = client.get_group(REVIEWERS_ID)

# Global group definitions
conference = openreview.Group(**{
    'id': CONF_ID,
    'readers':['everyone'],
    'writers': [CONF_ID],
    'signatures': [],
    'signatories': [CONF_ID],
    'members': [],
    # 'web': os.path.abspath('../webfield/homepage.js')
})

client.post_group(conference)

# Conference Objects

## Paper Invitation

SUBMISSION_DEADLINE = openreview.tools.timestamp_GMT(year=2019, month=9, day=1)

submission_inv = openreview.Invitation(
    id = SUBMISSION_ID,
    duedate = SUBMISSION_DEADLINE,
    readers = ['everyone'],
    signatures = [CONF_ID],
    writers = [CONF_ID],
    invitees = [],
    reply = {
        'readers': {
            'values': [
                CONF_ID
            ]
        },
        'signatures': { 'values': [CONF_ID]
                        },
        'writers': {
            'values': [CONF_ID]
        },
        'content': {
            'title': {'value-regex': '.*'},
            'number': {'value-regex': '.*'}
        }
    }
)
OBJECTS = {}
OBJECTS['conference'] = conference
OBJECTS['submission_invitation'] = submission_inv
inv = client.post_invitation(submission_inv)
print(inv)

## Read the file of reviewers emails and add them as members of the reviewer group.

def read_reviewers_file(path):
    l = []
    file = open(path, 'r')
    for line in file:
        l.append(line.strip())
    return l

reviewer_emails = read_reviewers_file(INPUT_FILES_DIR + "o-reviewers.csv")
print("Read", len(reviewer_emails), "email addresses")

# Add members to the reviewers group
reviewers_group.members = reviewer_emails
client.post_group(reviewers_group)

# Add members to the reviewers group
reviewers_group.members = reviewer_emails
client.post_group(reviewers_group)

# Papers

def read_papers_file(path):
    l = []
    file = open(path, 'r')
    for line in file:
        l.append(line.strip())
    return l
# papers given by CVPR are just numbers and nothing more.
papers = read_papers_file(INPUT_FILES_DIR + "o-papers.csv")
print("Read", len(papers), "papers")

## Paper Notes are very simple in this conference because all we have to identify them is a number.
## A note for a paper will look like:
'''
{   'content': {
        'title': "Paper-3",
        'number': "3"
     },
     'signatures': [CONF_ID],
     'writers': [CONF_ID],
     'readers': [CONF_ID] ,
     'invitation': OBJECTS['submission_invitation']
     
}
'''

n_papers = 0
paper_note_ids = []
for paper in papers:
    n_papers += 1
    content = {
        'title': "Paper-" + paper,
        'number': paper,
    }
    posted_submission = client.post_note(openreview.Note(**{
        'signatures': [CONF_ID],
        'writers': [CONF_ID],
        'readers': [CONF_ID],
        'content': content,
        'invitation': SUBMISSION_ID
    }))
    paper_note_ids.append(posted_submission.id)
print(len(paper_note_ids))

# Final results:  reviewers in a group and paper notes.

reviewers_group = client.get_group(REVIEWERS_ID)
print(len(reviewers_group.members), "reviewers")
cvpr_papers = list(tools.iterget_notes(client, invitation=SUBMISSION_ID))
print(len(cvpr_papers),"papers")

## Should see
# 2840 reviewers
# 5062 papers