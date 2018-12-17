import openreview
from openreview import tools
from cvpr2019 import *

## CVPR 2019 only used OR for creating a match.   They sent files that reprsent reviewers
## papers and other things pertaining to setting up the matcher.   They are in ../data
##  This script creates the necessary db objects for running the matcher.
## These are invitations for the paper_reviewer_score (previously called "metadata"), config_note
## assignment note.   The notes for assignment config and  paper-reviewer-scores are also built
## csv files were dumped from CMT and provided.  Here is how we use:

# The file o-matching-scores.csv gives the paper num and the score for each reviewer
# We read this in and create paper-reviewer-score notes for each paper and set up entries
# within the content of each note with an entry for each user that gives their userid and score.

# The file o-conflicts.csv gives a paper number and the emails of reviewers that have conflicts with it
#  We use this to add to the paper_reviewer_score note for the paper.   We find the entry for that
# user and add in a value of conflicts: 1  which is enough for the matcher to say that this user
# has a conflict with this paper.

# The file o-max-reviewers-per-paper.csv gives each reviewer followed by the max number of papers
# they are willing to review.  These are read in and are added to the config note as custom_loads
# which inside the content as a dictionary


# They also gave another file which we didn't read because we manually configure the config note
# to have min_users and max_users on each paper of 3 with 5 alternates.

client = openreview.Client(baseurl='http://openreview.localhost', username='OpenReview.net', password='d0ntf33dth3tr0lls')
print(client)

cvpr_paper_notes = list(tools.iterget_notes(client, invitation=SUBMISSION_ID))
reviewers_group = client.get_group(REVIEWERS_ID)
reviewers = reviewers_group.members
print("Num papers", len(cvpr_paper_notes))
print("Num reviewers", len(reviewers))

# Create the invitation for the Paper-Reviewer_Scores note (used to be called meta-data)
inv = openreview.Invitation(
    id = PAPER_REVIEWER_SCORE_ID,
    readers = ['everyone'],
    signatures = [CONF_ID],
    writers = [CONF_ID],
    invitees = [],
    reply = {
        'forum': None,
        'replyto': None,
        'readers': { 'values': [CONF_ID ]
                     },
        'signatures': { 'values': [CONF_ID]
                        },
        'writers': { 'values': [CONF_ID]
                     },
        'content': {  }
    }
)

paper_reviewer_inv = client.post_invitation(inv)
print(paper_reviewer_inv)

## Read the scores file into a dictionary
## { paperNum -> { email1 -> score, email2 -> score ... } ... }

## Each line of the file is paperNum, email, score

# Create a dictionary with a keys that are paper numbers.
# The value will be a dictionary with keys that are email address and values that are tpms scores
def read_paper_reviewer_scores_file (path):
    file = open(path,'r')
    d = {}
    linecount = 0
    for line in file:
        linecount += 1
        paper, email, score  = line.strip().split(',')
        paper = paper.strip()
        email = email.strip()
        score = score.strip()
        val = d.get(paper)
        if val:
            val[email] = score
        else:
            d[paper] = {email: score}
    print(linecount)
    return d

paper_reviewer_scores_dict = read_paper_reviewer_scores_file(INPUT_FILES_DIR + "o-matching-scores.csv")

## Build the paper-reviewer-score notes.

#  We have all the papers and all the reviewers but not all the paper-reviewer score info so we can't
# iterate over all the paper notes.    Instead we have to go through the paper_reviewer_scores_dict keys
# which are the paper numbers.  Currently there are 50 papers that we get scores for.


# First, create a mapping from paper numbers to their note
paper_num_map = {}
for n in cvpr_paper_notes:
    paper_num_map[n.content['number']] = n

# Now we go through all the papers in the dictionary of paper-reviewer scores
paper_nums = paper_reviewer_scores_dict.keys()
paper_reviewer_score_notes = []


for paper_num in paper_nums:
    # Get the paper note for paper number
    paper_note = paper_num_map[paper_num]

    # Get the dictionary of reviewer-email->score for this paper number
    reviewer_scores = paper_reviewer_scores_dict[paper_num]
    entries = []
    # Create a list of entries for each user.  Each entry has scores.
    for reviewer in reviewer_scores.keys():
        entry = {'userid': reviewer, 'scores': {'tpms': reviewer_scores[reviewer]}}
        entries.append(entry)
        scores = entry['scores']

    note = openreview.Note(forum=paper_note.id,
                           replyto=paper_note.id,
                           invitation=PAPER_REVIEWER_SCORE_ID,
                           readers=[CONF_ID],
                           writers=[CONF_ID],
                           signatures=[CONF_ID],
                           content={'entries': entries})
    paper_reviewer_score_notes.append(note)
    client.post_note(note)


print("Number of paper_review_notes is ", len(paper_reviewer_score_notes))

## Create the Paper Assignment Invitation

paper_assignment_inv = openreview.Invitation(
    id = ASSIGNMENT_ID,
    readers = [CONF_ID],
    signatures = [CONF_ID],
    writers = [CONF_ID],
    invitees = [],
    reply = {
        'forum': None,
        'replyto': None,
        'readers': { 'values': [CONF_ID ]
                     },
        'signatures': { 'values': [CONF_ID]
                        },
        'writers': { 'values': [CONF_ID]
                     },
        'content': {}
    }
)
client.post_invitation(paper_assignment_inv)
print(paper_assignment_inv)


## Configuration Invitation
# Create the invitation for the Paper-Reviewer_Scores note (used to be called meta-data)
config_inv = openreview.Invitation(
    id = CONFIG_ID,
    readers = ['everyone'],
    signatures = [CONF_ID],
    writers = [CONF_ID],
    invitees = [],
    reply = {
        'forum': None,
        'replyto': None,
        'readers': { 'values': [CONF_ID ]
                     },
        'signatures': { 'values': [CONF_ID]
                        },
        'writers': { 'values': [CONF_ID]
                     },
        'content': {
            "label": {
                "value-regex": ".{1,250}",
                "required": True,
                "description": "Title of the configuration.",
                "order": 1
            },
            "max_users": {
                "value-regex": "[0-9]+",
                "required": True,
                "description": "Max number of reviewers that can review a paper",
                "order": 2
            },
            "min_users": {
                "value-regex": "[0-9]+",
                "required": True,
                "description": "Min number of reviewers required to review a paper",
                "order": 3
            },
            "max_papers": {
                "value-regex": "[0-9]+",
                "required": True,
                "description": "Max number of reviews a person has to do",
                "order": 4
            },
            "min_papers": {
                "value-regex": "[0-9]+",
                "required": True,
                "description": "Min number of reviews a person should do",
                "order": 5
            },
            "alternates": {
                "value-regex": "[0-9]+",
                "required": True,
                "description": "Number of alternate reviewers for a paper",
                "order": 6
            },
            "config_invitation": {
                "value": CONFIG_ID,
                "required": True,
                "description": "Invitation to get the configuration note",
                "order": 3
            },
            "scores_names": {
                "values-dropdown": ['tpms', 'recommendation'],
                "required": True,
                "description": "List of scores names",
                "order": 3
            },
            "scores_weights": {
                "values-regex": "\\d*\\.?\\d*",
                "required": True,
                "description": "Comma separated values of scores weigths, should follow the same order than scores_names",
                "order": 3
            },
            "status": {
                "value-dropdown": ['Initialized', 'Running', 'Error', 'Failure', 'Complete', 'Deployed']
            },
            'paper_invitation': {"value": SUBMISSION_ID,
                                 "required": True,
                                 "description": "Invitation to get the configuration note",
                                 "order": 8
                                 },
            'metadata_invitation': {"value": PAPER_REVIEWER_SCORE_ID,
                                    "required": True,
                                    "description": "Invitation to get the configuration note",
                                    "order": 9
                                    },
            'assignment_invitation': {"value": ASSIGNMENT_ID,
                                      "required": True,
                                      "description": "Invitation to get the configuration note",
                                      "order": 10
                                      },
            'match_group': {"value": REVIEWERS_ID,
                            "required": True,
                            "description": "Invitation to get the configuration note",
                            "order": 11
                            }

        }
    }
)
client.post_invitation(config_inv)

# Assignment Configuration
# First the invitation
config_invitation = client.get_invitation(id = CONFIG_ID)

config_note = client.post_note(openreview.Note(**{
    'invitation': CONFIG_ID,
    'readers': [CONF_ID],
    'writers': [CONF_ID],
    'signatures': [CONF_ID],
    'content': {
        'label': 'cvpr-reviewers',
        'scores_names': ['tpms', 'recommendation'],
        'scores_weights': ['1', '0'],
        'max_users': '3', # max number of reviewers a paper can have
        'min_users': '3', # min number of reviewers a paper can have
        'max_papers': '15', # max number of papers a reviewer can review
        'min_papers': '8', # min number of papers a reviewer can review
        'alternates': '5',
        'constraints': {},
        "config_invitation": CONFIG_ID,
        'paper_invitation': SUBMISSION_ID,
        'metadata_invitation': PAPER_REVIEWER_SCORE_ID,
        'assignment_invitation': ASSIGNMENT_ID,
        'match_group': REVIEWERS_ID,
        'status': 'Initialized'
    }
}))

print(config_note)

## Read the conflicts of interest file and add constraints to the paper-reviewer-scores notes

### Note:  We changed how this works.  Originally we were reading
### the conflicts and storing them in the config note as constraints
### where constraints is a dict mapping a paper num to another dict
### containing email: '-inf'.    This conference has 5000+ papers and
### ~3000 reviewers and so this constraints dict gets so large that it
### then impossible to save the config note with this size dict in it
### failure occurs in openreview-py.client.post_note.
###
### Solution:  We are now adding each list of emails for
### a paper to the paper-reviewer-score note as a conflict in its
### list of conflicts.
### So each prs note will have a list of emails and it might be several
### hundred users, but at least this information is distributed across
### many prs notes rather than being concentrated in the single
### config note.
### It still takes awhile to do this because all these prs notes have to
### be posted.

config_notes = client.get_notes(invitation=CONFIG_ID)
len(config_notes)

cvpr_paper_notes = list(tools.iterget_notes(client, invitation=SUBMISSION_ID))
cvpr_prs_notes = list(tools.iterget_notes(client, invitation=PAPER_REVIEWER_SCORE_ID))

# First, create a mapping from paper numbers to their notes
paper_num_map = {}

for n in cvpr_paper_notes:
    paper_num_map[n.content['number']] = n

# Create a map from paper ids (forum) to paper reviewer score notes
prs_num_map = {}
for n in cvpr_prs_notes:
    prs_num_map[n.forum] = n


# Read in the file of conflicts which is a structured as
# paperNum, email
#  Go into the paper-reviewer-score note for that paper and install
# a conflict in the user entry record.
modified_prs_notes = {}
file = open(INPUT_FILES_DIR + "o-conflicts.csv",'r')
for line in file:
    paper, email = line.strip().split(',')
    paper = paper.strip()
    email = email.strip()
    paper_note = paper_num_map.get(paper)
    paperid = paper_note.id
    # get the prs note for this paper
    prs_note = prs_num_map.get(paperid)
    entries = prs_note.content.get('entries')
    # Find the entry for the user
    for e in entries:
        if e['userid'] == email:
            break
    # add a small list to this entry for conflicts.
    # This will tell the matcher not to assign this user to this paper
    e['conflicts'] = 1 # matcher just checks for the presence of a value in the conflicts field
    # Save the number->prs_note in a dictionary
    modified_prs_notes[paper] = prs_note
# All prs-notes have now had conflicts added so post them
# Go through the dictionary of prs-notes that were modified and post them
for prs_note in modified_prs_notes.values():
    client.post_note(prs_note)


## Read in the max reviews a user can do and put into config as a custom_load
file = open(INPUT_FILES_DIR + "o-max-reviewers-per-paper.csv",'r')
config_note = client.get_notes(invitation=CONFIG_ID)[0]
custom_loads = {}
for line in file:
    email, max_revs = line.strip().split(',')
    email = email.strip()
    max_revs = max_revs.strip()
    custom_loads[email] = int(max_revs)
config_note.content['custom_loads'] = custom_loads
client.post_note(config_note)


