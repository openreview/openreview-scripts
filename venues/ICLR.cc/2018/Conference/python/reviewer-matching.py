import argparse
import openreview
import openreview_matcher
import config
from collections import defaultdict

# Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--metadata', action='store_true', help = "if present, builds metadata notes")
parser.add_argument('--assignments', action='store_true', help = "if present, builds assignments note")
parser.add_argument('--overwrite', action='store_true', help = "if present, erases the old metadata and/or assignments")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--baseurl', help = "base URL")
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

class BidScore(openreview_matcher.metadata.OpenReviewFeature):
    def __init__(self, name, papers, bids):
        """
        @data - a dict which has the following attributes:
            'bids': a dictionary of openreview.Tag objects that represent bids, keyed by user signature
            'bid_score_map': a dictionary of numerical scores, keyed by strings that represent possible bid responses
        """
        self.name = name

        self.bid_score_map ={
            "I want to review": 1.0,
            "I can review": 0.75,
            "I can probably review but am not an expert": 0.5,
            "I cannot review": 0.25,
            "No bid": 0.0
        }
        self.scores = { n.forum: { bid.signatures[0]: self.bid_score_map[bid.tag] for bid in bids if bid.forum == n.forum} for n in papers }


    def score(self, signature, forum):
        """
        @signature - tilde ID of user
        @forum - forum of paper

        """

        try:
            return self.scores[forum][signature]
        except:
            return 0.0

def clear(inv):
    print "clearing notes from ", inv
    configs = client.get_notes(invitation=inv)
    for n in configs:
        client.delete_note(n)

if args.metadata:
    group_ids = [
        config.REVIEWERS,
        config.AREA_CHAIRS
    ]

    print "getting data..."
    all_papers = client.get_notes(invitation = config.BLIND_SUBMISSION)
    withdrawn_papers = [n for n in all_papers if ('withdrawal' in n.content)]
    papers = [n for n in all_papers if (not 'withdrawal' in n.content)]
    groups = [client.get_group(g) for g in group_ids]
    bids = client.get_tags(invitation = config.CONF + '/-/Add_Bid')

    if args.overwrite: clear(config.METADATA)

    # Define features
    print "building feature models..."
    paper_features = [
        BidScore(name='bid_score', bids=bids, papers=papers)
    ]

    print "generating paper metadata..."
    def metadata(forum):
        return openreview_matcher.metadata.generate_metadata_note(groups=groups, features=paper_features, note_params={
            'forum': forum,
            'invitation': config.METADATA,
            'readers': [config.CONF],
            'writers': [config.CONF],
            'signatures': [config.CONF]
        })
    metadata_notes = [metadata(note.forum) for note in papers]

    print "posting paper metadata..."
    for p in metadata_notes: client.post_note(p)



if args.assignments:

    if args.overwrite: clear(config.ASSIGNMENTS)

    reviewer_configuration = {
        "label": 'reviewers',
        "group": config.REVIEWERS,
        "submission": config.BLIND_SUBMISSION,
        "exclude": [],
        "metadata": config.METADATA,
        "minusers": 1,
        "maxusers": 3,
        "minpapers": 2,
        "maxpapers": 5,
        "weights": {
            "bid_score": 1
        }
    }

    area_chair_configuration = {
        "label": 'areachairs',
        "group": config.AREA_CHAIRS,
        "submission": config.BLIND_SUBMISSION,
        "exclude": [],
        "metadata": config.METADATA,
        "minusers": 1,
        "maxusers": 1,
        "minpapers": 1,
        "maxpapers": 10,
        "weights": {
            "bid_score": 1
        }
    }

    # define note parameters for the configuration note
    note_params = {
        'invitation': config.ASSIGNMENTS,
        'readers': [config.CONF],
        'writers': [config.CONF],
        'signatures': [config.CONF],
    }

    reviewer_note = client.post_note(openreview.Note(
        content = {'configuration': reviewer_configuration}, **note_params))

    area_chair_note = client.post_note(openreview.Note(
        content = {'configuration': area_chair_configuration}, **note_params))

    print "reviewer assignments: {0}".format(reviewer_note.id)
    print "area chair assignments: {0}".format(area_chair_note.id)
