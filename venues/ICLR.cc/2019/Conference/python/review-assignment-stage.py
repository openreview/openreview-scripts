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
import time
import json

import matcher


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    blind_submissions = openreview.tools.iterget_notes(client, invitation=iclr19.BLIND_SUBMISSION_ID)

    # At this point, all reviewers should have been
    # converted to profile IDs and deduplicated.
    reviewers_group = client.get_group(iclr19.REVIEWERS_ID)
    assert all(['~' in member for member in reviewers_group.members]), 'not all reviewers have been converted to profile IDs'
    reviewer_profiles = client.get_profiles(reviewers_group.members)

    invitations.disable_bids(client)

    # create metadata
    metadata_notes = []
    metadata_inv = client.post_invitation(iclr19.metadata_inv)
    for blind_note in blind_submissions:
        original_note = client.get_note(id=blind_note.original)
        paper_bids = client.get_tags(invitation=iclr19.add_bid.id)
        new_metadata_note = notes.post_metadata_note(client, blind_note, original_note, reviewer_profiles, paper_bids)
        metadata_notes.append(new_metadata_note)

    with open('../data/iclr19-match-config-example.json') as f:
        config = json.load(f)

    # This could be set by hand if reviewers or papers have specific supplies/demands
    supplies = [config['max_papers']] * len(reviewer_profiles)
    demands = [config['max_users']] * len(metadata_notes)

    # run initial match
    encoder = matcher.metadata.Encoder(
        metadata_notes,
        config,
        [r.id for r in reviewer_profiles])

    flow_solver = matcher.Solver(supplies, demands, encoder.cost_matrix, encoder.constraint_matrix)
    solution = flow_solver.solve()
    assignments_by_forum, alternates_by_forum = encoder.decode(solution)

    # create an assignment "configuration"
    config_inv = client.post_invitation(iclr19.config_inv)
    assert config_inv.id == config['config_invitation'],\
        "config invitation {} doesn't match invitation in configuration file {}".format(
            config_inv.id, config['config_invitation'])

    print('posting new config and assignments...')
    post_time = time.time()
    client.post_note(openreview.Note(**{
        'invitation': config_inv.id,
        'readers': config_inv.reply['readers']['values'],
        'writers': config_inv.reply['writers']['values'],
        'signatures': config_inv.reply['signatures']['values'],
        'content': config
    }))

    # create the assignment notes. this populates the matching browser.
    assignment_inv = client.post_invitation(iclr19.assignment_inv)
    assert assignment_inv.id == config['assignment_invitation'],\
        "assignment invitation {} doesn't match invitation in configuration file {}".format(
            assignment_inv.id, config['assignment_invitation'])

    for forum, assignments in assignments_by_forum.items():
        client.post_note(openreview.Note.from_json({
            'forum': forum,
            'invitation': assignment_inv.id,
            'replyto': forum,
            'readers': assignment_inv.reply['readers']['values'],
            'writers': assignment_inv.reply['writers']['values'],
            'signatures': assignment_inv.reply['signatures']['values'],
            'content': {
                'label': config['label'],
                'assignedGroups': assignments,
                'alternateGroups': []
            }
        }))
    print("took {0:.2f} seconds".format(time.time() - post_time))

