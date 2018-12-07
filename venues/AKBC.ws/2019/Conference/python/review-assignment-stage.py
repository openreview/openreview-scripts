'''
Reviewer Assignment Stage:
- Bidding Task / interface is closed.
- Initial paper-reviewer and paper-areachair matches are computed.
- Program chairs browse match using OpenReview Matching System and make hand-adjustments as needed.
- Paper-reviewer and paper-areachair assignments are finalized and deployed.

'''

import argparse
import openreview
import akbc19 as conference_config
import invitations
import notes
import groups
import time
import json
import csv
from collections import defaultdict


def clear(client, invitation):
    note_list = list(openreview.tools.iterget_notes(client, invitation = invitation))
    for note in note_list:
        client.delete_note(note)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('affinity_score_file')
    parser.add_argument('ac_score_file')
    parser.add_argument('subject_score_file')
    parser.add_argument('-c','--constraints_file')
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    print('clearing previous metadata, assignments, and configs...')
    clear(client, conference_config.METADATA_INV_ID)
    clear(client, conference_config.ASSIGNMENT_INV_ID)
    clear(client, conference_config.CONFIG_INV_ID)

    # TODO: update the reviewer and AC consoles to indicate that the bidding phase is over

    # At this point, all reviewers & ACs should have been
    # converted to profile IDs and deduplicated.
    reviewers_group = client.get_group(conference_config.REVIEWERS_ID)
    if not all(['~' in member for member in reviewers_group.members]):
        print('WARNING: not all reviewers have been converted to profile IDs. Members without profiles will not have metadata created.')
    valid_reviewer_ids = [r for r in reviewers_group.members if '~' in r]

    reviewer_profiles = client.get_profiles(valid_reviewer_ids)

    areachairs_group = client.get_group(conference_config.AREA_CHAIRS_ID)
    if not all(['~' in member for member in areachairs_group.members]):
        print('WARNING: not all area chairs have been converted to profile IDs. Members without profiles will not have metadata created.')
    valid_ac_ids = [r for r in areachairs_group.members if '~' in r]

    ac_profiles = client.get_profiles(valid_ac_ids)

    user_profiles = ac_profiles + reviewer_profiles

    invitations.disable_bids(client)
    groups.update_AC_console(client, '../webfield/areachairWebfieldReviewerAssignmentStage.js')
    groups.update_Reviewer_console(client, '../webfield/reviewerWebfieldReviewerAssignmentStage.js')

    # create metadata
    metadata_inv = client.post_invitation(conference_config.metadata_inv)
    config_inv = client.post_invitation(conference_config.config_inv)
    assignment_inv = client.post_invitation(conference_config.assignment_inv)

    blind_submissions = openreview.tools.iterget_notes(client, invitation=conference_config.BLIND_SUBMISSION_ID)

    scores_by_reviewer_by_paper = {note.forum: defaultdict(dict) for note in blind_submissions}
    # read in TPMS scores
    with open(args.affinity_score_file) as f:
        for row in csv.reader(f):
            paper_note_id = row[0]
            profile_id = row[1]
            score = row[2]
            scores_by_reviewer_by_paper[paper_note_id][profile_id].update({'affinity': float(score)})

    with open(args.subject_score_file) as f:
        for row in csv.reader(f):
            paper_note_id = row[0]
            profile_id = row[1]
            score = row[2]
            scores_by_reviewer_by_paper[paper_note_id][profile_id].update({'subject_area_score': float(score)})

    with open(args.ac_score_file) as f:
        for row in csv.reader(f):
            paper_note_id = row[0]
            profile_id = row[1]
            score = row[2]
            scores_by_reviewer_by_paper[paper_note_id][profile_id].update({'areachair_score': float(score)})

    # read in manual conflicts
    # manual_conflicts_by_id is keyed on tilde IDs, and values are each a list of domains.
    manual_conflicts_by_id = {}
    if args.constraints_file:
        with open(args.constraints_file) as f:
            for row in csv.reader(f):
                id = row[0]
                conflicts = row[1:]
                manual_conflicts_by_id[id] = conflicts

    for blind_note in openreview.tools.iterget_notes(
        client,
        invitation=conference_config.BLIND_SUBMISSION_ID,
        details='original,tags'
        ):

        scores_by_reviewer = scores_by_reviewer_by_paper[blind_note.id]

        new_metadata_note = notes.post_metadata_note(
            client,
            blind_note,
            user_profiles,
            metadata_inv,
            scores_by_reviewer,
            manual_conflicts_by_id
        )



