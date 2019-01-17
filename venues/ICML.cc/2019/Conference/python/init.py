'''
Setup ICML matching
'''
import os
import csv, json
import openreview
import icml
import random
import argparse

def main(client, processed_files_dir):
    def fullpath(path):
        return os.path.join(processed_files_dir, path)

    # groups
    icml_groups = openreview.tools.build_groups(icml.conference.id)
    for group in icml_groups:
        try:
            existing_group = client.get_group(group.id)
        except openreview.OpenReviewException as e:
            posted_group = client.post_group(group)
            print(posted_group.id)

    # post the conference group with updated parameters
    posted_conference = client.post_group(icml.conference)

    reviewers = icml.reviewers
    with open(fullpath('reviewers.csv')) as f:
        reviewers.members = [row[0] for row in csv.reader(f)]

    expert_reviewers = icml.expert_reviewers
    with open(fullpath('expert_reviewers.csv')) as f:
        expert_reviewers.members = [row[0] for row in csv.reader(f)]

    areachairs = icml.area_chairs
    with open(fullpath('areachairs.csv')) as f:
        areachairs.members = [row[0] for row in csv.reader(f)]

    senior_areachairs = icml.senior_area_chairs
    with open(fullpath('senior_areachairs.csv')) as f:
        senior_areachairs.members = [row[0] for row in csv.reader(f)]

    posted_areachairs = client.post_group(areachairs)
    posted_senior_areachairs = client.post_group(senior_areachairs)
    posted_reviewers = client.post_group(reviewers)
    posted_expert_reviewers = client.post_group(expert_reviewers)

    # invitations
    posted_submission_inv = client.post_invitation(icml.submission_inv)
    posted_blind_inv = client.post_invitation(icml.blind_submission_inv)
    posted_jrac_placeholder_inv = client.post_invitation(icml.jrac_placeholder_inv)

    posted_assignment_inv = client.post_invitation(icml.assignment_inv)
    posted_config_inv = client.post_invitation(icml.config_inv)
    posted_metadata_inv = client.post_invitation(icml.metadata_inv)
    posted_jrac_metadata_inv = client.post_invitation(icml.jrac_metadata_inv)
    posted_constraint_inv = client.post_invitation(icml.lock_tag_inv)

    posted_sac_bid_inv = client.post_invitation(icml.sac_bid_inv)

    '''
    post JrAC placeholders
    '''
    placeholders_by_jrac = {}
    for jrac_id in areachairs.members:
        jrac_placeholder = client.post_note(openreview.Note(**{
            'invitation': icml.jrac_placeholder_inv.id,
            'readers': [icml.CONFERENCE_ID],
            'writers': [icml.CONFERENCE_ID],
            'signatures': [icml.CONFERENCE_ID],
            'forum': None,
            'replyto': None,
            'content': {
                'title': jrac_id
            }
        }))

        placeholders_by_jrac[jrac_id] = jrac_placeholder

    with open(fullpath('sac_ac_bids.jsonl')) as f:
        for line in f.readlines():
            tag_obj = json.loads(line.rstrip())
            jrac_id = tag_obj.pop('jrac_id')
            placeholder_id = placeholders_by_jrac[jrac_id].id
            tag_obj['forum'] = placeholder_id
            tag_obj['replyto'] = placeholder_id
            tag_obj['invitation'] = icml.sac_bid_inv.id
            tag = openreview.Tag(**tag_obj)
            client.post_tag(tag)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--processed_files_dir', default='../data/icml-sheets-processed')
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
    print('connecting to {} with username {}'.format(client.baseurl, client.username))

    main(client, args.processed_files_dir)
