import argparse
import sys

from openreview import *

sys.path.append(os.path.join(os.getcwd(), "../../dto/uai2017"))
print sys.path
from note_content import *
from constants import *
from lxml import etree
import xml.etree.ElementTree
import utils
import time

"""
Parse the arguments for user authentication
"""
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--overwrite', help="If set to true, overwrites existing groups")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--file1', help="The xml from which tpms scores are to be read")
parser.add_argument('--file2', help="The xml from which paper similarity scores are to be read")

args = parser.parse_args()
if args.file1 is None:
    raise Exception("No tpms file is provided")
elif not os.path.isfile(args.file1):
    raise Exception("Incorrect file path : %s specified" % args.file1)
else:
    if not args.file1.endswith(".xml"):
        raise Exception("Incorrect File format")

if args.file2 is None:
    raise Exception("No Paper Similarity score file is provided")
elif not os.path.isfile(args.file2):
    raise Exception("Incorrect file path : %s specified" % args.file2)
else:
    if not args.file2.endswith(".xml"):
        raise Exception("Incorrect File format")

if args.username is not None and args.password is not None:
    openreview = Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    openreview = Client(baseurl=args.baseurl)


def get_paper_names(notes):
    """
    Getting paper name using the following logic: If note.number is NONE then throw an error else 'Paper' followed by its number
    :param notes:
    :return:
    """
    list_paper_name = []
    for note in notes:
        if (note.number is None):
            raise ValueError("No note number for note id : %s" % (note.id))
        else:
            list_paper_name.append("Paper" + str(note.number))
    return list_paper_name


def get_notes_submitted_papers():
    """
    Get all the submitted papers
    :return:
    """
    notes = openreview.get_notes(invitation=CONFERENCE_SUBMISSION)
    return notes


def get_paper_metadata_notes(paper_names):
    """
    Get all submitted paper meta data notes
    :return:
    """
    notes = [openreview.get_notes(invitation=CONFERENCE + "/" + paper_name + "/-/matching")[0] for paper_name in
             paper_names]
    return notes


def get_submitted_paper_details(submitted_paper_notes):
    """
    Get details of all the papers submitted in a list
    :param submitted_paper_notes:
    :return:
    """
    paper_details_list = []
    paper_details_list.append(
        ["Paper ID", "Paper Title", "Abstract", "Author Names", "Author Emails", "Subject Areas", "Conflict Reasons",
         "Files", "Supplementary File", "Related Submissions", "AC suggestions",
         "Toronto Paper Matching System Agreement"])
    for note in submitted_paper_notes:
        paper_id = note.id
        paper_title = note.content["title"]
        paper_abstract = note.content["abstract"]
        author_names = ";".join(note.content["authors"])
        author_emails = ";".join(note.content["authorids"])
        subject_areas = note.content["TL;DR"]
        conflict_reasons = ";".join(note.content["conflicts"])
        files = note.content["pdf"]
        supplementary_files = ""
        related_submission = ""
        ac_suggestions = ""
        toronto_paper_matching_system_agreement = ""
        paper_details_list.append([paper_id, paper_title, paper_abstract, author_names, author_emails,
                                   subject_areas, conflict_reasons, files, supplementary_files, related_submission,
                                   ac_suggestions, toronto_paper_matching_system_agreement])
    return paper_details_list


def get_paper_reviewer_score_tree(submitted_paper_notes, dict_reviewers_email):
    """
    Get an XML tree for paper reviewer score
    :param submitted_paper_notes:
    :param dict_reviewers_email:
    :return:
    """
    root = etree.Element("reviewermatching")
    meta_data_notes = get_paper_metadata_notes(get_paper_names(submitted_paper_notes))
    for index in range(len(submitted_paper_notes)):
        paper_id = submitted_paper_notes[index].id
        paper_element = etree.Element("submission", submissionId=str(paper_id))
        reviewers_score = {x["reviewer"]: x["score"] for x in meta_data_notes[index].content["reviewers"]}
        for reviewer, data in dict_reviewers_email.iteritems():
            score = 0
            if reviewer in reviewers_score:
                score = reviewers_score[reviewer]
            paper_element.append(etree.Element("metareviewer", email=data[3], score=str(score)))
        root.append(paper_element)
    return etree.ElementTree(root)


def get_all_members_data():
    """
    Get a dictionary of each member with its details
    :param members:
    :return:
    """
    members = utils.get_all_member_ids()
    dict_reviewer_data = {}
    for member in members:
        member_note = openreview.get_note(id=member)
        member_first_name = member_note.content["names"][0]["first"]
        member_last_name = member_note.content["names"][0]["last"]
        member_email = member_note.content["preferred_email"]
        member_organization = member_note.content["history"][0]["institution"]["name"]
        member_url = openreview.baseurl + "/notes?id=" + member
        dict_reviewer_data[member] = [member_first_name, member_last_name, member_organization, member_email, member,
                                      member_url]
    return dict_reviewer_data


def parse_paper_reviewer_affinity_details(file_path):
    """
    Parse an xml file of the affinity scores and return a dictionary of the elements
    The xml file has the following format
    <reviewermatching>
        <submission submissionId="3" maxReviewers="10"  minReviewers="1">
            <reviewer email="" score="" source=""/>
        </submission>
    </reviewermatching>
    :param file_path:
    :return: a dictionary with key as paper number and values as a list of tuple of reviewer email,affinity score and source
    """
    if not file_path.endswith(".xml"):
        raise Exception("Incorrect File format")
    e = xml.etree.ElementTree.parse(file_path)
    root = e._root
    submissions = root._children
    affinity_scores_dict = {}
    betas_dict = {}
    email_id_map = utils.get_email_to_id_mapping(openreview)
    for submission in submissions:
        paper_id = int(submission.attrib['submissionId'])
        max_reviewers = int(submission.attrib['maxReviewers'])
        min_reviewers = int(submission.attrib['minReviewers'])
        betas_dict[paper_id] = (min_reviewers, max_reviewers)
        if paper_id not in affinity_scores_dict:
            affinity_scores_dict[paper_id] = []
        for score_details in submission._children:
            affinity_scores_dict[paper_id].append(
                (email_id_map[score_details.attrib['email']], float(score_details.attrib['score']),
                 score_details.attrib['source']))
    return affinity_scores_dict, betas_dict


def parse_paper_paper_similarity_details(file_path):
    """
    Parse an xml file of the affinity scores and return a dictionary of the elements
    The xml file has the following format
    <papersimilarity>
        <submission submissionId="">
            <submission submissionId=""  score="" source="" />
        </submission>
    </papersimilarity>
    :param file_path:
    :return: a dictionary with key as paper number and values as a list of tuple of paper id , similarity score and source
    """
    if not file_path.endswith(".xml"):
        raise Exception("Incorrect File format")
    e = xml.etree.ElementTree.parse(file_path)
    root = e._root
    submissions = root._children
    similarity_scores_dict = {}
    for submission in submissions:
        paper_id = int(submission.attrib['submissionId'])
        if paper_id not in similarity_scores_dict:
            similarity_scores_dict[paper_id] = []
        for score_details in submission._children:
            similarity_scores_dict[paper_id].append(
                (int(score_details.attrib['submissionId']), float(score_details.attrib['score']),
                 score_details.attrib['source']))
    return similarity_scores_dict


def create_paper_metadata_note(affinity_scores_dict, betas_dict, paper_similarity_dict):
    """
    Using the data from the parsed tpms scores file and paper_similarity_score file populating the paper meta data
    :param affinity_scores_dict:
    :param betas_dict:
    :param paper_similarity_dict:
    :return:
    """
    notes = utils.get_notes_submitted_papers(openreview, CONFERENCE_SUBMISSION)
    papers_number_list = utils.get_paper_numbers(notes)
    for i in range(len(notes)):
        inviter = CONFERENCE + "/-/matching"
        paper_number = papers_number_list[i]
        (min_reviewers, max_reviewers) = betas_dict[paper_number]
        reviewers = map(lambda x: Reviewer(reviewer=x[0], score=x[1], source=x[2]), affinity_scores_dict[paper_number])
        papers = map(lambda x: Paper(paper=x[0], score=x[1], source=x[2]), paper_similarity_dict[paper_number])
        content = PaperMetaData(minreviewers=min_reviewers, maxreviewers=max_reviewers, reviewers=reviewers,
                                papers=papers)
        note = Note(invitation=inviter, cdate=int(time.time()) * 1000,
                    readers=[CONFERENCE_PCS, CONFERENCE_ACS],
                    forum=notes[i].id,
                    writers=['everyone'],
                    content=content.to_dict(),
                    signatures=[CONFERENCE])
        openreview.post_note(note)


if __name__ == '__main__':
    affinity_scores_dict, betas_dict = parse_paper_reviewer_affinity_details(args.file1)
    paper_similarity_scores_dict = parse_paper_paper_similarity_details(args.file2)
    create_paper_metadata_note(affinity_scores_dict, betas_dict,paper_similarity_scores_dict)