import argparse
from openreview import *
import sys, os
import time
import utils
sys.path.append(os.path.join(os.getcwd(), "../../dto/uai2017"))
print sys.path
from note_content import *
from constants import *

import random
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


def create_paper_groups(notes):
    """
    Creating a group for each paper name
    :param notes:
    :return:
    """
    paper_names = utils.get_paper_names(notes)
    for paper_name in paper_names:
        group_id = CONFERENCE + "/" + paper_name
        g = Group(group_id, readers=['everyone'],
                  writers=[CONFERENCE, CONFERENCE_PCS],
                  signatures=[CONFERENCE],
                  signatories=[CONFERENCE_REVIEWERS])
        print "Posting group: ", g.id
        openreview.post_group(g)


def create_sample_paper_metadata_note(notes):
    """
    Create a new invitation and supporting note for the paper meta data
    :param notes:
    :return:
    """
    papers = utils.get_paper_numbers(notes)
    reviewers = utils.get_all_reviewers(openreview,CONFERENCE_REVIEWERS)
    for i in range(len(notes)):
        inviter = CONFERENCE + "/-/matching"
        note = Note(invitation=inviter, cdate=int(time.time()) * 1000,
                    readers=[CONFERENCE_PCS, CONFERENCE_ACS],
                    forum=notes[i].id,
                    writers=['everyone'], content=PaperMetaData.create_samples(papers,reviewers,1)[0].to_dict(),
                    signatures=[CONFERENCE])
        openreview.post_note(note)


def create_paper_reviewer_group(notes,assignment_matrix=None):
    """
    Creating a reviewer group for each paper name if there is an entry in the assignment matrix
    :param notes:
    :return:
    """
    paper_numbers = utils.get_paper_numbers(notes)
    paper_reviewer_dict=utils.get_paper_reviewers_dict(openreview,CONFERENCE)
    for paper_index in range(len(notes)):
        group_id = CONFERENCE_REVIEWERS + "/Paper" + str(paper_numbers[paper_index])
        g = Group(group_id, readers=['everyone'],
                  writers=[CONFERENCE_REVIEWERS, CONFERENCE_PCS],
                  signatures=[CONFERENCE],
                  signatories=[CONFERENCE_REVIEWERS])
        reviewers = paper_reviewer_dict[notes[paper_index].id]
        assigned_reviewers=[]
        for reviewer in reviewers:
            if assignment_matrix is not None:
                if assignment_matrix[notes[paper_index].id][reviewer] is True:
                    assigned_reviewers.append(reviewer)
            else:
                assigned_reviewers.append(reviewer)
        g.members = assigned_reviewers
        print "Posting group: ", g.id
        openreview.post_group(g)


if __name__ == '__main__':
    if openreview.user['id'].lower() == 'openreview.net':
        notes = utils.get_notes_submitted_papers(openreview,CONFERENCE_SUBMISSION)
        paper_names = utils.get_paper_names(notes)
        # Creating groups for all submitted papers
        create_paper_groups(notes)
        # Creating invitations and notes for all submitted papers
        create_sample_paper_metadata_note(notes)
        #Creating a reviewer group for each paper
        create_paper_reviewer_group(notes)
        # Printing all the paper meta data notes
        notes_meta = utils.get_paper_metadata_notes(openreview,CONFERENCE)
        for note in notes_meta:
            content = note.content
            print json.dumps(note.content)
    else:
        print "Aborted. User must be Super User."
