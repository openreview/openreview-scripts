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
import matcher

def clear(client, invitation):
    note_list = list(openreview.tools.iterget_notes(client, invitation = invitation))
    for note in note_list:
        client.delete_note(note)

def split_reviewers_by_experience(client, reviewers_group):
    questionnaire_responses = openreview.tools.iterget_notes(
        client, invitation=conference_config.CONFERENCE_ID + '/-/Reviewer_Questionnaire_Response')

    experience_by_signature = {r.signatures[0]: r.content['Reviewing Experience'] for r in questionnaire_responses}

    senior_reviewers = []
    junior_reviewers = []

    valid_reviewer_ids = [r for r in reviewers_group.members if '~' in r]
    for reviewer in valid_reviewer_ids:
        experience = experience_by_signature.get(reviewer, '')
        if experience in [
            '5-10 times  - active community citizen',
            '10+ times  - seasoned reviewer'
        ]:
            senior_reviewers.append(reviewer)
        else:
            junior_reviewers.append(reviewer)

    return senior_reviewers, junior_reviewers

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('scores_file')
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

    blind_submissions = openreview.tools.iterget_notes(client,
        invitation=conference_config.BLIND_SUBMISSION_ID,
        details='original,tags')

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

    # read in manual conflicts
    # manual_conflicts_by_id is keyed on tilde IDs, and values are each a list of domains.
    manual_conflicts_by_id = {}
    if args.constraints_file:
        with open(args.constraints_file) as f:
            for row in csv.reader(f):
                id = row[0]
                conflicts = row[1:]
                manual_conflicts_by_id[id] = conflicts

    for blind_note in blind_submissions:
        paper_tpms_scores = paper_scores_by_number[blind_note.number]
        new_metadata_note = notes.post_metadata_note(client, blind_note, user_profiles, metadata_inv, paper_tpms_scores, manual_conflicts_by_id)

    senior_reviewer_ids, junior_reviewer_ids = split_reviewers_by_experience(client, reviewers_group)
    conference_config.senior_reviewers.members = senior_reviewer_ids
    conference_config.junior_reviewers.members = junior_reviewer_ids
    client.post_group(conference_config.senior_reviewers)
    client.post_group(conference_config.junior_reviewers)

