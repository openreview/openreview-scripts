import argparse
import sys
import os
import openreview
from collections import defaultdict
from uaidata import *

sys.path.append(os.path.join(os.getcwd(), "../../dto/uai2017"))

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
parser.add_argument('--alphas', help="The xml from which reviewer bid scores are to be read")
parser.add_argument('--bidscores', help="The xml from which reviewer similarity scores are to be read")
parser.add_argument('--reviewerscores', help="The xml from which reviewer similarity scores are to be read")
parser.add_argument('--titles', help="The xml from which reviewer paper titles")

args = parser.parse_args()
if args.alphas is None:
    raise Exception("No reviewer bid scores file is provided")
elif not os.path.isfile(args.alphas):
    raise Exception("Incorrect file path : %s specified" % args.alphas)
else:
    if not args.alphas.endswith(".xml"):
        raise Exception("Incorrect File format")

# if args.bidscores is None:
#     raise Exception("No reviewer similarity scores file is provided")
# elif not os.path.isfile(args.bidscores):
#     raise Exception("Incorrect file path : %s specified" % args.bidscores)
# else:
#     if not args.bidscores.endswith(".xml"):
#         raise Exception("Incorrect File format")

if args.reviewerscores is None:
    raise Exception("No reviewer similarity scores file is provided")
elif not os.path.isfile(args.reviewerscores):
    raise Exception("Incorrect file path : %s specified" % args.reviewerscores)
else:
    if not args.reviewerscores.endswith(".xml"):
        raise Exception("Incorrect File format")

if args.username != None and args.password != None:
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    client = openreview.Client(baseurl=args.baseurl)


def parse_alphas(file_path):
    if not file_path.endswith(".xml"):
        raise Exception("Incorrect File format")
    e = xml.etree.ElementTree.parse(file_path)
    root = e._root
    reviewers = root._children
    bid_scores_dict = defaultdict(list)
    alphas_dict = {}

    for reviewer in reviewers:
        profile = client.get_profile(reviewer.attrib['email'])
        reviewer_id = profile.id
        max_papers = int(reviewer.attrib['maxPapers'])
        min_papers = int(reviewer.attrib['minPapers'])
        alphas_dict[reviewer_id] = (min_papers, max_papers)

    return alphas_dict

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
    reviewers = root._children
    bid_scores_dict = defaultdict(list)

    #email_id_map = utils.get_email_to_id_mapping(client)
    for reviewer in reviewers:
        profile = client.get_profile(reviewer.attrib['email'])
        reviewer_id = profile.id
        for score_details in reviewer._children:
            bid_scores_dict[reviewer_id].append(
                (int(score_details.attrib['submissionId']), float(score_details.attrib['score']), score_details.attrib['source']))
    return bid_scores_dict

def parse_titles(file_path):
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
    reviewers = root._children
    titles_dict = defaultdict(list)

    #email_id_map = utils.get_email_to_id_mapping(client)
    for reviewer in reviewers:
        profile = client.get_profile(reviewer.attrib['email'])
        reviewer_id = profile.id
        for paper in reviewer._children:
            titles_dict[reviewer_id].append(
                (paper.attrib['title'], float(paper.attrib['score']), paper.attrib['source']))
    return titles_dict

def parse_reviewer_reviewer_similarity_details(file_path):
    """
    Parse an xml file of the affinity scores and return a dictionary of the elements
    The xml file has the following format
    <reviewersimilarity>
        <reviewer email="jamiesho@microsoft.com">
            <reviewer email="az@robots.ox.ac.uk" score="0.593668455"  source="ReviewerSimilarity" />
        </reviewer >
        <reviewer email="quan@cse.ust.hk">1.00" />
            <reviewer email="stephen.gould@anu.edu.au" score="0.320136938" source="ReviewerSimilarity" />
        </reviewer >
    </reviewersimilarity>
    :param file_path:
    :return: a dictionary with key as reviewer id and values as a list of tuple of reviewer id , similarity score and source
    """
    if not file_path.endswith(".xml"):
        raise Exception("Incorrect File format")
    e = xml.etree.ElementTree.parse(file_path)
    root = e._root
    #email_id_map = utils.get_email_to_id_mapping(client)
    reviewers = root._children
    similarity_scores_dict = {}
    for reviewer in reviewers:
        reviewer_id = client.get_profile(reviewer.attrib['email']).id
        if reviewer_id not in similarity_scores_dict:
            similarity_scores_dict[reviewer_id] = []
        for score_details in reviewer._children:
            similarity_scores_dict[reviewer_id].append(
                (client.get_profile(score_details.attrib['email']).id, float(score_details.attrib['score']),
                 score_details.attrib['source']))
    return similarity_scores_dict


def create_reviewer_metadata_note(alphas_dict, reviewer_similarity_dict, bids_scores_dict=None, titles_dict=None):
    """
    Using the openreview data data from the parsed reviewer bid score and reviewer_similarity_score file populating the reviewer meta data
    :param bids_scores_dict
    :param alphas_dict
    :param reviewer_similarity_dict
    :return None
    """

    reviewers = alphas_dict.keys()
    print "creating reviewer metadata note"
    for reviewer_id in reviewers:
        print "generating note for %s" % reviewer_id

        (min_paper, max_papers) = alphas_dict[reviewer_id]

        reviewers = [{'reviewer':x[0], 'score':x[1], 'source':x[2]} for x in reviewer_similarity_dict[reviewer_id]]

        papers = []
        if bid_scores_dict != None:
            papers = [{'paper_number': x[0], 'score': x[1], 'source': x[2]} for x in bids_scores_dict[reviewer_id]]

        authored_papers = []
        if titles_dict != None:
            authored_papers = [{'title': x[0], 'score': x[1], 'source': x[2]} for x in titles_dict[reviewer_id]]

        content = {
            'name': reviewer_id,
            'minpapers': min_paper,
            'maxpapers': max_papers,
            'papers': papers,
            'authored_papers': authored_papers,
            'reviewers': reviewers
        }

        note = openreview.Note(
            invitation=CONFERENCE + "/-/Reviewer/Metadata",
            cdate=int(time.time()) * 1000,
            readers=['OpenReview.net',COCHAIRS],
            writers=['OpenReview.net'],
            content=content,
            signatures=['OpenReview.net']
        )

        client.post_note(note)

if __name__ == '__main__':
    alphas_dict = parse_alphas(args.alphas)

    bid_scores_dict = None
    if args.bidscores != None:
        bid_scores_dict = parse_bid_scores(args.bidscores)

    titles_dict = None
    if args.titles != None:
        titles_dict = parse_titles(args.titles)

    similarity_scores_dict = parse_reviewer_reviewer_similarity_details(args.reviewerscores)
    create_reviewer_metadata_note(alphas_dict, similarity_scores_dict, bid_scores_dict, titles_dict)
