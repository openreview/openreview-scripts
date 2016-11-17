from openreview import *
import numpy as np
import sys
sys.path.append(os.path.join(os.getcwd(), "../../dto/uai2017"))
from note_content import *
from constants import *
sys.path.append(os.path.join(os.getcwd(), "../../matching"))
from TotAffMatcher import *


def get_all_member_ids(openreview_client):
    """
    Get all the members ids
    :return:
    """
    members = filter(lambda id: id != "~Super_User1" and id != "~",
                     map(lambda x: x.id, openreview_client.get_groups(regex="~.*")))
    return members


def get_notes_submitted_papers(openreview_client,invitation_id):
    """
    Get all the submitted papers
    :return:
    """
    notes = openreview_client.get_notes(invitation=invitation_id)
    return notes


def update_reviewers(openreview_client,conference_reviewer_group,members):
    """
    Update the members of the group
    :param: members
    :return:
    """
    reviewers = openreview_client.get_group(conference_reviewer_group)
    reviewers.members = members
    openreview_client.post_group(reviewers)


def get_all_reviewers(openreview_client,conference_reviewer_group):
    """

    :param openreview_client:
    :param conference_reviewer_group:
    :return:
    """
    reviewers = openreview_client.get_group(conference_reviewer_group)
    return reviewers.members

def get_paper_names(notes):
    """
    Getting paper name using the following logic: If note.number is NONE then throw an Error
    :param notes:
    :return:
    """
    list_paper_name = []
    for note in notes:
        if note.number is None:
            raise ValueError("Incorrect note number")
        else:
            list_paper_name.append("Paper" + str(note.number))
    return list_paper_name


def get_paper_numbers(notes):
    """
    Getting paper number using the following logic: If note.number is NONE then throw an Error
    :param notes:
    :return:
    """
    list_paper_number = []
    for note in notes:
        if note.number is None:
            raise ValueError("Incorrect note number")
        else:
            list_paper_number.append(note.number)
    return list_paper_number


def get_paper_metadata_notes(openreview_client,conference):
    """
    Get all submitted paper meta data notes
    :return:
    """
    notes = openreview_client.get_notes(invitation=conference + "/-/matching")
    return notes


def get_paper_reviewers_dict(openreview_client,conference):
    """
    Get the set of reviewers for each paper
    :param openreview_client:
    :param conference:
    :return:
    """
    notes = openreview_client.get_notes(invitation=conference+ "/-/matching")
    output_dict={}
    for note in notes:
        for reviewer_info in note.content["reviewers"]:
            if note.forum not in output_dict:
                output_dict[note.forum] =set()
            output_dict[note.forum].add(reviewer_info["reviewer"])
    return output_dict


def get_paper_reviewers_score(openreview_client,conference):
    """
    Get an dictionary of paper reviewer score
    :param openreview_client:
    :param conference:
    :return:
    """
    notes = openreview_client.get_notes(invitation=conference+ "/-/matching")
    output_dict={}
    for note in notes:
        for reviewer_info in note.content['reviewers']:
            if (note.forum,reviewer_info['reviewer']) not in output_dict:
                output_dict[(note.forum,reviewer_info['reviewer'])] = []
            output_dict[(note.forum, reviewer_info['reviewer'])].append(reviewer_info['score'])
    return output_dict



def get_reviewer_data_notes(openreview_client,conference):
    """
    Get all the reviewer meta data notes
    :return:
    """
    notes = openreview_client.get_notes(invitation=conference + "/-/reviewer")
    return notes


def get_paper_reviewer_weights(openreview_client,conference,conference_reviewer,submission_invitation_id):
    reviewers = get_all_reviewers(openreview_client,conference_reviewer)
    submitted_papers_notes = get_notes_submitted_papers(openreview_client,submission_invitation_id)
    paper_ids = [paper_note.id for paper_note in submitted_papers_notes]
    weights = np.zeros((len(reviewers),len(paper_ids)))
    paper_index_dict = {paper_ids[i]:i for i in range(len(paper_ids))}
    reviewer_index_dict = {reviewers[i]:i for i in range(len(reviewers))}
    paper_reviewer_score_dict = get_paper_reviewers_score(openreview_client,conference)
    for (note_id,reviewer),score_array in paper_reviewer_score_dict.iteritems():
        weights[reviewer_index_dict[reviewer],paper_index_dict[note_id]] = np.mean(np.array(score_array))
    totAffMatcher = TotAffMatcher(200.0,100.0,weights)
    totAffMatcher.solve()
