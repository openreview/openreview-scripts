import argparse
import sys
import os
import openreview
from collections import defaultdict
from uaidata import *

import utils

sys.path.append(os.path.join(os.getcwd(), "../../dto/uai2017"))

from TotAffMatcher import *

"""
Parse the arguments for user authentication

"""
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--overwrite', help="If set to true, overwrites existing groups")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()
if args.username != None and args.password != None:
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    client = openreview.Client(baseurl=args.baseurl)


paper_metadata_notes = client.get_notes(invitation=CONFERENCE+"/-/Paper/Metadata")
reviewer_metadata_notes = client.get_notes(invitation=CONFERENCE+"/-/Reviewer/Metadata")
reviewers = client.get_group(PC).members
uai_submissions = client.get_notes(invitation=CONFERENCE+"/-/submission")
uai_blind_submissions = client.get_notes(invitation=CONFERENCE+"/-/blind-submission")

def get_hard_constraint_value(score_array):
    """
    A function to check for the presence of Hard Constraints in the score array (+Inf or -Inf) ,
    :param score_array:
    :return:
    """
    for element in score_array:
        if str(element).strip().lower() == '+inf':
            return 1
        if str(element).strip().lower() == '-inf':
            return 0
    return -1


def add_hard_constraint_matcher(matcher, hard_constraint_dict):
    """
    Adding hard constraint for scores where value is either +Inf or -Inf
    :param matcher:
    :param hard_constraint_dict:
    :return:
    """
    constraints =[]
    for (reviewer_index, paper_index), value in hard_constraint_dict:
        constraints.append(reviewer_index, paper_index, value)
    matcher.add_hard_consts(constrs=constraints)


conference = CONFERENCE
conference_reviewer = PC
"""
Using Total Affinity Matcher get the paper reviewer assignment
:param client:
:param conference:
:param conference_reviewer:
:return:
"""

# Getting Paper and Reviewer details
paper_number_forum_dict = {note.number:note.forum for note in uai_blind_submissions}
paper_forum_number_dict = {note.forum:note.number for note in uai_blind_submissions}

reviewer_index_dict = {reviewers[i]: i for i in range(len(reviewers))}
paper_index_dict = {i: paper_forum_number_dict[i]-1 for i in paper_forum_number_dict.keys()}

# Getting paper reviewer score array

#paper_reviewer_score_dict = utils.get_paper_reviewers_score(client, conference, paper_number_forum_dict)
paper_reviewer_score_dict = defaultdict(list)

for note in paper_metadata_notes:
    for reviewer_info in note.content['reviewers']:
        key = (note.forum, reviewer_info['reviewer'])
        paper_reviewer_score_dict[key].append(reviewer_info['score'])

for note in reviewer_metadata_notes:
    for paper in note.content['papers']:
        key = (paper_number_forum_dict[int(paper['paper_number'])], note.content['name'])
        paper_reviewer_score_dict[key].append(paper['score'])

# Defining and Updating the weight matrix
weights = np.zeros((len(reviewers), len(uai_blind_submissions)))
hard_constraint_dict = {}

for (note_id, reviewer), score_array in paper_reviewer_score_dict.iteritems():
    # Separating the infinite ones with the normal scores and get the mean of the normal ones
    hard_constraint_value = get_hard_constraint_value(score_array)
    if hard_constraint_value == -1:
        weights[reviewer_index_dict[reviewer], paper_index_dict[note_id]] = np.mean(np.array(score_array))
    else:
        hard_constraint_dict[reviewer_index_dict[reviewer], paper_index_dict[note_id]] = hard_constraint_value

# Defining the matcher

beta_dict = {note.forum: (note.content['minreviewers'], note.content['maxreviewers']) for note in paper_metadata_notes}
alpha_dict = {note.content['name']: (note.content['minpapers'], note.content['maxpapers']) for note in reviewer_metadata_notes}

totAffMatcher = TotAffMatcher(alpha_dict.values(),beta_dict.values(), weights)
add_hard_constraint_matcher(totAffMatcher, hard_constraint_dict)

totAffMatcher.solve()
solution = totAffMatcher.sol_dict()

# Extracting the paper-reviewer assignment
paper_forum_reviewers_dict = defaultdict(list)
for var_name in solution:

    var_val = var_name.split('x_')[1].split(',')

    reviewer_index, paper_index = (int(var_val[0]), int(var_val[1]))

    match = solution[var_name]

    if match==1:
        paper_forum_reviewers_dict[paper_number_forum_dict[paper_index+1]].append(reviewers[reviewer_index])



## Instead of calling create_paper_assignment_group, send the relevant info to the "assign program committee" script
#create_paper_assignment_group([paper_forum_number_dict], paper_forum_reviewers_dict)

# if __name__ == '__main__':
#     if client.user['id'].lower() == 'openreview.net':

