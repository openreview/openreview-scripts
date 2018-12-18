'''
Reviewer Assignment Stage:
- Bidding Task / interface is closed.
- Initial paper-reviewer and paper-areachair matches are computed.
- Program chairs browse match using OpenReview Matching System and make hand-adjustments as needed.
- Paper-reviewer and paper-areachair assignments are finalized and deployed.

'''

import argparse
import openreview
import config
import time
import json
import csv
from collections import defaultdict


def clear(client, invitation):
    note_list = list(openreview.tools.iterget_notes(client, invitation = invitation))
    for note in note_list:
        client.delete_note(note)

def _append_manual_conflicts(profile, manual_user_conflicts):
    for conflict_domain in manual_user_conflicts:
        manual_entry = {
            "end": None,
            "start": None,
            "position": "Manual Entry",
            "institution": {
                "name": "Manual Entry",
                "domain": conflict_domain
            }
        }
        profile.content['history'].append(manual_entry)
    return profile


def _build_entries(author_profiles, reviewer_profiles, paper_bid_jsons, scores_by_reviewer, manual_conflicts_by_id):
    entries = []
    for profile in reviewer_profiles:
        bid_score_map = {
            'Very High': 1.0,
            'High': 0.5,
            'Neutral': 0.0,
            'Low': -0.5,
            'Very Low': -1.0
        }
        try:
            reviewer_bids = sorted([t for t in [j for j in paper_bid_jsons if j['tcdate']] if profile.id in t['signatures']], key=lambda t: t.get('tcdate',0), reverse=True)
        except TypeError as e:
            print(paper_bid_jsons)
            raise e
        reviewer_scores = scores_by_reviewer.get(profile.id, {})

        # find conflicts between the reviewer's profile and the paper's authors' profiles
        user_entry = {
            'userid': profile.id,
            'scores': reviewer_scores
        }

        if reviewer_bids:
            bid_score = bid_score_map.get(reviewer_bids[0]['tag'], 0.0)
            if bid_score != 0.0:
                user_entry['scores']['bid'] = bid_score

        manual_user_conflicts = manual_conflicts_by_id.get(profile.id, [])
        if manual_user_conflicts:
            profile = _append_manual_conflicts(profile, manual_user_conflicts)
        conflicts = openreview.tools.get_conflicts(author_profiles, profile)

        if conflicts:
            user_entry['conflicts'] = conflicts

        entries.append(user_entry)

    return entries

def post_metadata_note(client,
    note,
    reviewer_profiles,
    metadata_inv,
    paper_tpms_scores,
    manual_conflicts_by_id):

    authorids = note.content['authorids']
    paper_bid_jsons = note.details['tags']
    paper_author_profiles = client.get_profiles(authorids)
    entries = _build_entries(paper_author_profiles, reviewer_profiles, paper_bid_jsons, paper_tpms_scores, manual_conflicts_by_id)

    new_metadata_note = openreview.Note(**{
        'forum': note.id,
        'invitation': metadata_inv.id,
        'readers': metadata_inv.reply['readers']['values'],
        'writers': metadata_inv.reply['writers']['values'],
        'signatures': metadata_inv.reply['signatures']['values'],
        'content': {
            'title': 'Paper Metadata',
            'entries': entries
        }
    })

    return client.post_note(new_metadata_note)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('affinity_score_file')
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    conference = config.get_conference(client)
    CONFERENCE_ID = conference.get_id()
    PROGRAM_CHAIRS_ID = conference.get_program_chairs_id()
    SUBMISSION_ID = conference.get_submission_id()
    METADATA_INV_ID = CONFERENCE_ID + '/-/Paper_Metadata'
    REVIEWERS_ID = conference.get_reviewers_id()
    AREA_CHAIRS_ID = conference.get_area_chairs_id()

    metadata_inv = openreview.Invitation.from_json({
    'id': METADATA_INV_ID,
    'readers': [
        CONFERENCE_ID,
        PROGRAM_CHAIRS_ID
    ],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'reply': {
        'forum': None,
        'replyto': None,
        'invitation': SUBMISSION_ID,
        'readers': {
            'values': [
                CONFERENCE_ID,
            ]
        },
        'writers': {
            'values': [CONFERENCE_ID]
        },
        'signatures': {
            'values': [CONFERENCE_ID]},
        'content': {}
        }
    })

    ASSIGNMENT_INV_ID = CONFERENCE_ID + '/-/Paper_Assignment'

    assignment_inv = openreview.Invitation.from_json({
        'id': ASSIGNMENT_INV_ID,
        'readers': [CONFERENCE_ID],
        'writers': [CONFERENCE_ID],
        'signatures': [CONFERENCE_ID],
        'reply': {
            'forum': None,
            'replyto': None,
            'invitation': SUBMISSION_ID,
            'readers': {'values': [CONFERENCE_ID, PROGRAM_CHAIRS_ID]},
            'writers': {'values': [CONFERENCE_ID]},
            'signatures': {'values': [CONFERENCE_ID]},
            'content': {}
        }
    })


    CONFIG_INV_ID = CONFERENCE_ID + '/-/Assignment_Configuration'

    config_inv = openreview.Invitation.from_json({
        'id': CONFIG_INV_ID,
        'readers': [CONFERENCE_ID, PROGRAM_CHAIRS_ID],
        'writers': [CONFERENCE_ID],
        'signatures': [PROGRAM_CHAIRS_ID],
        'reply': {
            'forum': None,
            'replyto': None,
            'invitation': None,
            'readers': {'values': [CONFERENCE_ID, PROGRAM_CHAIRS_ID]},
            'writers': {'values': [CONFERENCE_ID, PROGRAM_CHAIRS_ID]},
            'signatures': {'values': [PROGRAM_CHAIRS_ID]},
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
                    "value": CONFERENCE_ID,
                    "required": True,
                    "description": "Invitation to get the configuration note",
                    "order": 7
                },
                'paper_invitation': {"value": SUBMISSION_ID,
                                    "required": True,
                                    "description": "Invitation to get the configuration note",
                                    "order": 8
                                    },
                'metadata_invitation': {"value": METADATA_INV_ID,
                                        "required": True,
                                        "description": "Invitation to get the configuration note",
                                        "order": 9
                                        },
                'assignment_invitation': {"value": ASSIGNMENT_INV_ID,
                                        "required": True,
                                        "description": "Invitation to get the configuration note",
                                        "order": 10
                                        },
                'match_group': {
                                "value-radio": [REVIEWERS_ID, AREA_CHAIRS_ID],
                                "required": True,
                                "description": "Invitation to get the configuration note",
                                "order": 11
                                },
                "scores_names": {
                    "values-dropdown": ['affinity', 'bid'],
                    "required": True,
                    "description": "List of scores names",
                    "order": 12
                },
                "scores_weights": {
                    "values-regex": "\\d*\\.?\\d*", # decimal number allowed
                    "required": True,
                    "description": "Comma separated values of scores weigths, should follow the same order than scores_names",
                    "order": 13
                },
                "status": {
                    "value-dropdown": ['Initialized', 'Running', 'Error', 'Failure', 'Complete', 'Deployed']
                }
            }
        }

    })


    print('clearing previous metadata, assignments, and configs...')
    clear(client, METADATA_INV_ID)
    clear(client, ASSIGNMENT_INV_ID)
    clear(client, CONFIG_INV_ID)

    # TODO: update the reviewer and AC consoles to indicate that the bidding phase is over
    # At this point, all reviewers & ACs should have been
    # converted to profile IDs and deduplicated.
    reviewers_group = client.get_group(REVIEWERS_ID)
    if not all(['~' in member for member in reviewers_group.members]):
        print('WARNING: not all reviewers have been converted to profile IDs. Members without profiles will not have metadata created.')
    valid_reviewer_ids = [r for r in reviewers_group.members if '~' in r]

    reviewer_profiles = client.get_profiles(valid_reviewer_ids)

    areachairs_group = client.get_group(AREA_CHAIRS_ID)
    if not all(['~' in member for member in areachairs_group.members]):
        print('WARNING: not all area chairs have been converted to profile IDs. Members without profiles will not have metadata created.')
    valid_ac_ids = [r for r in areachairs_group.members if '~' in r]

    ac_profiles = client.get_profiles(valid_ac_ids)

    user_profiles = ac_profiles + reviewer_profiles


    # create metadata
    metadata_inv = client.post_invitation(metadata_inv)
    config_inv = client.post_invitation(config_inv)
    assignment_inv = client.post_invitation(assignment_inv)

    submissions = list(openreview.tools.iterget_notes(client,
        invitation=conference.get_submission_id(), details='tags'))

    scores_by_reviewer_by_paper = {note.forum: defaultdict(dict) for note in submissions}

    with open(args.affinity_score_file) as f:
        for row in csv.reader(f):
            paper_note_id = row[0]
            profile_id = row[1]
            score = row[2]
            scores_by_reviewer_by_paper[paper_note_id][profile_id].update({'affinity': float(score)})


    for note in submissions:
        scores_by_reviewer = scores_by_reviewer_by_paper[note.id]
        new_metadata_note = post_metadata_note(client, note, user_profiles, metadata_inv, scores_by_reviewer, {})



