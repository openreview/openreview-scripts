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

    blind_submissions = openreview.tools.iterget_notes(client,
        invitation=iclr19.BLIND_SUBMISSION_ID,
        details='original,tags')

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
        new_metadata_note = notes.post_metadata_note(client, blind_note, reviewer_profiles)
        metadata_notes.append(new_metadata_note)

