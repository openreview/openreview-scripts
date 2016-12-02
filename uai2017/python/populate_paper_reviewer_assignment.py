import argparse
import sys

from openreview import *

import utils

sys.path.append(os.path.join(os.getcwd(), "../../dto/uai2017"))
print sys.path
from constants import *
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
    openreview = Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    openreview = Client(baseurl=args.baseurl)


def get_hard_constraint_value(score_array):
    """
    A function to check for the presence of Hard Constraints in the score array (+Inf or -Inf) ,
    :param score_array:
    :return:
    """
    for element in score_array:
        if element == '+Inf':
            return 1
        if element == '-Inf':
            return -1
    return 0


def add_hard_constraint_matcher(matcher, hard_constraint_dict):
    """
    Adding hard constraint for scores where value is either +Inf or -Inf
    :param matcher:
    :param hard_constraint_dict:
    :return:
    """
    for (reviewer_index, paper_index), value in hard_constraint_dict:
        matcher.add_hard_const(reviewer_index, paper_index, value)
    return None


def create_paper_assignment_group(paper_id_number_dict, paper_id_reviewers_dict):
    """
    Creating a group for each paper id
    :param notes:
    :return:
    """
    for paper_id in paper_id_number_dict:
        group_id = CONFERENCE_REVIEWERS + "/" + "Paper" + str(paper_id_number_dict[paper_id])
        g = Group(group_id, readers=['everyone'],
                  writers=[CONFERENCE, CONFERENCE_PCS],
                  signatures=[CONFERENCE],
                  signatories=[CONFERENCE_REVIEWERS])
        g.members = paper_id_reviewers_dict[paper_id]
        print "Posting group: ", g.id
        openreview.post_group(g)



def update_paper_reviewer_weights(openreview_client, conference, conference_reviewer, submission_invitation_id):
    """
    Using Total Affinity Matcher get the paper reviewer assignment
    :param openreview_client:
    :param conference:
    :param conference_reviewer:
    :param submission_invitation_id:
    :return:
    """
    # Getting reviewers details
    reviewers = utils.get_all_reviewers(openreview_client, conference_reviewer)
    reviewer_index_dict = {reviewers[i]: i for i in range(len(reviewers))}

    # Getting Paper details
    submitted_papers_notes = utils.get_notes_submitted_papers(openreview_client, submission_invitation_id)
    paper_ids = [paper_note.id for paper_note in submitted_papers_notes]
    paper_number_id_dict = utils.get_number_id_dict(submitted_papers_notes)
    paper_id_number_dict = {paper_number_id_dict[paper_number]: paper_number for paper_number in paper_number_id_dict}
    paper_index_dict = {paper_ids[i]: i for i in range(len(paper_ids))}

    # Getting paper reviewer score array
    paper_reviewer_score_dict = utils.get_paper_reviewers_score(openreview_client, conference, paper_number_id_dict)

    # Defining and Updating the weight matrix
    weights = np.zeros((len(reviewers), len(paper_ids)))
    hard_constraint_dict = {}
    for (note_id, reviewer), score_array in paper_reviewer_score_dict.iteritems():
        # Separating the infinite ones with the normal scores and get the mean of the normal ones
        hard_constraint_value = get_hard_constraint_value(score_array)
        if hard_constraint_value == 0:
            weights[reviewer_index_dict[reviewer], paper_index_dict[note_id]] = np.mean(np.array(score_array))
        else:
            hard_constraint_dict[reviewer_index_dict[reviewer], paper_index_dict[note_id]] = hard_constraint_value

    # Defining the matcher
    totAffMatcher = TotAffMatcher([2, 3], [1, 1, 1], weights)
    add_hard_constraint_matcher(totAffMatcher, hard_constraint_dict)
    totAffMatcher.solve()
    solution = totAffMatcher.sol_dict()

    # Extracting the paper-reviewer assignment
    paper_id_reviewers_dict = {}
    for var_name in solution:
        reviewer_index, paper_index = totAffMatcher.inverse_var_name(var_name)
        if paper_ids[paper_index] not in paper_id_reviewers_dict:
            paper_id_reviewers_dict[paper_ids[paper_index]] = []
        paper_id_reviewers_dict[paper_ids[paper_index]].append(reviewers[reviewer_index])

    # Creating the paper- reviewer assignment group
    create_paper_assignment_group(paper_id_number_dict, paper_id_reviewers_dict)


if __name__ == '__main__':
    if openreview.user['id'].lower() == 'openreview.net':
        update_paper_reviewer_weights(openreview, CONFERENCE, CONFERENCE_REVIEWERS, CONFERENCE_SUBMISSION)
