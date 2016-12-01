import sys

from openreview import *

sys.path.append(os.path.join(os.getcwd(), "../../dto/uai2017"))
sys.path.append(os.path.join(os.getcwd(), "../../matching"))


def get_all_member_ids(openreview_client):
    """
    Get all the members ids
    :return:
    """
    members = filter(lambda id: id != "~Super_User1" and id != "~",
                     map(lambda x: x.id, openreview_client.get_groups(regex="~.*")))
    return members


def get_notes_submitted_papers(openreview_client, invitation_id):
    """
    Get all the submitted papers
    :return:
    """
    notes = openreview_client.get_notes(invitation=invitation_id)
    return notes


def update_reviewers(openreview_client, conference_reviewer_group, members):
    """
    Update the members of the group
    :param: members
    :return:
    """
    reviewers = openreview_client.get_group(conference_reviewer_group)
    reviewers.members = members
    openreview_client.post_group(reviewers)


def get_all_reviewers(openreview_client, conference_reviewer_group):
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


def get_paper_metadata_notes(openreview_client, conference):
    """
    Get all submitted paper meta data notes
    :return:
    """
    notes = openreview_client.get_notes(invitation=conference + "/-/matching")
    return notes


def get_paper_reviewers_dict(openreview_client, conference):
    """
    Get the set of reviewers for each paper
    :param openreview_client:
    :param conference:
    :return:
    """
    notes = openreview_client.get_notes(invitation=conference + "/-/matching")
    output_dict = {}
    for note in notes:
        for reviewer_info in note.content["reviewers"]:
            if note.forum not in output_dict:
                output_dict[note.forum] = set()
            output_dict[note.forum].add(reviewer_info["reviewer"])
    return output_dict


def get_paper_reviewers_score(openreview_client, conference, paper_number_id_dict):
    """
    Get an dictionary of paper reviewer score. For each paper and reviewer it returns an array of scores which might contan '+Inf' or '-
    :param openreview_client:
    :param conference:
    :return:
    """
    notes = openreview_client.get_notes(invitation=conference + "/-/matching")
    output_dict = {}
    for note in notes:
        for reviewer_info in note.content['reviewers']:
            if (note.forum, reviewer_info['reviewer']) not in output_dict:
                output_dict[(note.forum, reviewer_info['reviewer'])] = []
            output_dict[(note.forum, reviewer_info['reviewer'])].append(reviewer_info['score'])
    notes = openreview_client.get_notes(invitation=conference + "/-/reviewer")
    for note in notes:
        content = note.content
        for paper in content['papers']:
            key = (paper_number_id_dict[int(paper['paper'])], content['name'])
            if key not in output_dict:
                output_dict[key] = []
            output_dict[key].append(paper['score'])
    return output_dict


def get_reviewer_data_notes(openreview_client, conference):
    """
    Get all the reviewer meta data notes
    :return:
    """
    notes = openreview_client.get_notes(invitation=conference + "/-/reviewer")
    return notes


def get_number_id_dict(submitted_paper_notes):
    """
    Get a dictionary mapping of paper number to paper id
    :param submitted_paper_notes:
    :return:
    """
    number_id_dict = {}
    for note in submitted_paper_notes:
        number_id_dict[note.number] = note.id
    return number_id_dict
