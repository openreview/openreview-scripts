'''
Reviewer Assignment Stage:
- Bidding Task / interface is closed.
- Initial paper-reviewer and paper-areachair matches are computed.
- Program chairs browse match using OpenReview Matching System and make hand-adjustments as needed.
- Paper-reviewer and paper-areachair assignments are finalized and deployed.

'''

import argparse
import openreview
import iclr19
import invitations
import notes
import groups
import time
import json
import csv
import matcher

def clear(client, invitation):
    for note in openreview.tools.iterget_notes(client, invitation = invitation):
        client.delete_note(note)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('scores_file')
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    print('clearing previous metadata, assignments, and configs...')
    clear(client, iclr19.METADATA_INV_ID)
    clear(client, iclr19.ASSIGNMENT_INV_ID)
    clear(client, iclr19.CONFIG_INV_ID)

    # TODO: update the reviewer and AC consoles to indicate that the bidding phase is over

    blind_submissions = openreview.tools.iterget_notes(client,
        invitation=iclr19.BLIND_SUBMISSION_ID,
        details='original,tags')

    # At this point, all reviewers & ACs should have been
    # converted to profile IDs and deduplicated.
    reviewers_group = client.get_group(iclr19.REVIEWERS_ID)
    if not all(['~' in member for member in reviewers_group.members]):
        print('WARNING: not all reviewers have been converted to profile IDs. Members without profiles will not have metadata created.')
    valid_reviewer_ids = [r for r in reviewers_group.members if '~' in r]

    reviewer_profiles = client.get_profiles(valid_reviewer_ids)

    areachairs_group = client.get_group(iclr19.AREA_CHAIRS_ID)
    if not all(['~' in member for member in areachairs_group.members]):
        print('WARNING: not all area chairs have been converted to profile IDs. Members without profiles will not have metadata created.')
    valid_ac_ids = [r for r in areachairs_group.members if '~' in r]

    ac_profiles = client.get_profiles(valid_ac_ids)

    user_profiles = ac_profiles + reviewer_profiles

    invitations.disable_bids(client)
    groups.update_AC_console(client, '../webfield/areachairWebfieldReviewerAssignmentStage.js')
    groups.update_Reviewer_console(client, '../webfield/reviewerWebfieldReviewerAssignmentStage.js')

    # create metadata
    metadata_inv = client.post_invitation(iclr19.metadata_inv)
    config_inv = client.post_invitation(iclr19.config_inv)
    assignment_inv = client.post_invitation(iclr19.assignment_inv)

    # read in TPMS scores
    paper_scores_by_number = {}

    with open(args.scores_file) as f:
        for row in csv.reader(f):
            paper_number = int(row[0])
            profile_id = row[1]
            score = row[2]
            if paper_number not in paper_scores_by_number:
                paper_scores_by_number[paper_number] = {}
            paper_scores_by_number[paper_number][profile_id] = score

    for blind_note in blind_submissions:
        paper_tpms_scores = paper_scores_by_number[blind_note.number]
        new_metadata_note = notes.post_metadata_note(client, blind_note, user_profiles, metadata_inv, paper_tpms_scores)
