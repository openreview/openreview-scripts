import argparse
import sys

import openreview
import os

sys.path.append(os.path.join(os.getcwd(), "../../dto/uai2017"))
import note_content
from uaidata import *
from lxml import etree
import xml.etree.ElementTree
import utils
import time
from collections import defaultdict

"""
Parse the arguments for user authentication
"""
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--overwrite', help="If set to true, overwrites existing groups")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--betas', help="The xml file containing the beta values for the paper submissions")
parser.add_argument('--reviewerscores', help="The xml file containing the paper-reviewer affinity scores")
parser.add_argument('--paperscores', help="The xml file containing the paper-paper affinity scores")
parser.add_argument('--bidscores', help="The xml file containing the reviewer bids")


args = parser.parse_args()

if args.username is not None and args.password is not None:
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    client = openreview.Client(baseurl=args.baseurl)

def validate_input(args):
    if args.betas is None:
        raise Exception("No betas file is provided")
    elif not os.path.isfile(args.betas):
        raise Exception("Incorrect file path : %s specified" % args.betas)
    else:
        if not args.betas.endswith(".xml"):
            raise Exception("Incorrect File format")

    if args.reviewerscores is None:
        raise Exception("No reviewer scores file is provided")
    elif not os.path.isfile(args.reviewerscores):
        raise Exception("Incorrect file path : %s specified" % args.reviewerscores)
    else:
        if not args.reviewerscores.endswith(".xml"):
            raise Exception("Incorrect File format")

    if args.paperscores is None:
        raise Exception("No reviewer scores file is provided")
    elif not os.path.isfile(args.paperscores):
        raise Exception("Incorrect file path : %s specified" % args.paperscores)
    else:
        if not args.paperscores.endswith(".xml"):
            raise Exception("Incorrect File format")

    # if args.bidscores is None:
    #     raise Exception("No bid scores file is provided")
    # elif not os.path.isfile(args.bidscores):
    #     raise Exception("Incorrect file path : %s specified" % args.bidscores)
    # else:
    #     if not args.bidscores.endswith(".xml"):
    #         raise Exception("Incorrect File format")


def parse_betas(file_path):
    if not file_path.endswith(".xml"):
        raise Exception("Incorrect File format")

    e = xml.etree.ElementTree.parse(file_path)
    root = e._root
    submissions = root._children

    betas_dict = {}

    for submission in submissions:
        paper_id = int(submission.attrib['submissionId'])
        max_reviewers = int(submission.attrib['maxReviewers'])
        min_reviewers = int(submission.attrib['minReviewers'])
        betas_dict[paper_id] = (min_reviewers, max_reviewers)

    return betas_dict

def parse_bid_scores(file_path):
    """
    Parse an xml file of the affinity scores and return a dictionary of the elements
    The xml file has the following format
    <reviewerbid>
        <reviewer email="jamiesho@microsoft.com" maxPapers="10"  minPapers="2">
            <submission submissionId="6"  score="0.551721716"  source="ReviewerBids" />
        </reviewer>
    </reviwerbid>
    :param file_path:
    :return: a dictionary with key as paper number and values as a list of tuple of reviewer email,affinity score and source
    """
    if not file_path.endswith(".xml"):
        raise Exception("Incorrect File format")
    e = xml.etree.ElementTree.parse(file_path)
    root = e._root
    submissions = root._children
    bid_scores_dict = defaultdict(list)

    for submission in submissions:
        paper_id = int(submission.attrib['submissionId'])

        for score_details in submission._children:

            profile = client.get_profile(score_details.attrib['email'])

            bid_scores_dict[paper_id].append(
                (profile.id, float(score_details.attrib['score']),
                 score_details.attrib['source']))

    return bid_scores_dict

def parse_paper_reviewer_scores(file_path):
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
    affinity_scores_dict = defaultdict(list)

    #email_id_map = utils.get_email_to_id_mapping(openreview)
    for submission in submissions:
        paper_id = int(submission.attrib['submissionId'])

        for score_details in submission._children:

            profile = client.get_profile(score_details.attrib['email'])

            affinity_scores_dict[paper_id].append(
                (profile.id, float(score_details.attrib['score']),
                 score_details.attrib['source']))

    return affinity_scores_dict


def parse_paper_paper_scores(file_path):
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
    similarity_scores_dict = defaultdict(list)
    for submission in submissions:
        paper_id = int(submission.attrib['submissionId'])

        for score_details in submission._children:
            similarity_scores_dict[paper_id].append(
                (int(score_details.attrib['submissionId']), float(score_details.attrib['score']),
                 score_details.attrib['source']))
    return similarity_scores_dict


def create_paper_metadata_note(affinity_scores_dict, betas_dict, paper_similarity_dict, bid_scores_dict=None):
    """
    Using the data from the parsed tpms scores file and paper_similarity_score file populating the paper meta data
    :param affinity_scores_dict:
    :param betas_dict:
    :param paper_similarity_dict:
    :return:
    """
    notes = client.get_notes(invitation=CONFERENCE+"/-/blind-submission")

    print "creating paper metadata note"
    for n in notes:
        print "generating note %s" % n.id

        (min_reviewers, max_reviewers) = betas_dict[n.number]

        reviewers = map(lambda p: note_content.Reviewer(reviewer=p[0], score=p[1], source=p[2]), affinity_scores_dict[n.number])

        if bid_scores_dict:
            bid_scores = map(lambda p: note_content.Reviewer(reviewer=p[0], score=p[1], source=p[2]), bid_scores_dict[n.number])
            reviewers += bid_scores

        papers = map(lambda p: note_content.Paper(paper_number=p[0], score=p[1], source=p[2]), paper_similarity_dict[n.number])


        content = note_content.PaperMetaData(
            minreviewers = min_reviewers,
            maxreviewers = max_reviewers,
            reviewers = reviewers,
            papers = papers
        )

        note = openreview.Note(
            invitation = CONFERENCE + "/-/Paper/Metadata",
            cdate = int(time.time()) * 1000,
            readers=['OpenReview.net'],
            forum=n.id,
            writers=['OpenReview.net'],
            content=content.to_dict(),
            signatures=['OpenReview.net']
        )
        client.post_note(note)


if __name__ == '__main__':
    validate_input(args)
    betas_dict = parse_betas(args.betas)
    affinity_scores_dict = parse_paper_reviewer_scores(args.reviewerscores)
    paper_similarity_scores_dict = parse_paper_paper_scores(args.paperscores)

    bid_scores_dict = None
    if args.bidscores != None:
        bid_scores_dict = parse_bid_scores(args.bidscores)

    create_paper_metadata_note(affinity_scores_dict, betas_dict, paper_similarity_scores_dict, bid_scores_dict)
