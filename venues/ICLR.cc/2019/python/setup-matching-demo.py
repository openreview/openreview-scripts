'''
A throwaway script to setup the matching demo.

Before using, make sure that your local instance has a copy of the LIVE database,
otherwise you might run into problems.
'''

import openreview
import argparse
import iclr19
import random
from matcher import metadata, utils

def canonicalize_reviewers(client, reviewers_group_id):
    reviewers_group = client.get_group(reviewers_group_id)
    reviewer_profiles = client.get_profiles(reviewers_group.members)
    reviewer_ids = list(set([r.id for r in reviewer_profiles.values()]))
    reviewers_group.members = reviewer_ids
    return client.post_group(reviewers_group), reviewer_profiles

def clear(client, invitation):
    for note in openreview.tools.iterget_notes(client, invitation = invitation):
        client.delete_note(note)

def submit_papers(client, old_papers_inv, new_papers_inv):
    for paper in openreview.tools.iterget_notes(client, invitation=old_papers_inv):
        new_content = paper.content
        new_content['subject areas'] = ['Algorithms: Approximate Inference']
        new_paper = openreview.Note(**{
            'invitation': new_papers_inv.id,
            'writers': paper.signatures,
            'readers': [iclr19.CONFERENCE_ID],
            'signatures': paper.signatures,
            'content': new_content
        })

        try:
            p = client.post_note(new_paper)
            print("{} -> {}".format(paper.id, p.id))
        except openreview.OpenReviewException as e:
            pass

def metadata_note(paper, metadata_inv, entries=[]):
    metadata_params = {
        'forum': paper.forum,
        'invitation': metadata_inv.id,
        'readers': metadata_inv.reply['readers']['values'],
        'writers': metadata_inv.reply['writers']['values'],
        'signatures': metadata_inv.reply['signatures']['values'],
        'content': {
                'entries': entries
            }
    }
    return openreview.Note(**metadata_params)


# these arguments should be retrievable by a get_profiles call
def build_entries(paper, author_profiles, reviewer_profiles):
    entries = []
    for reviewer_email in reviewer_profiles:
        reviewer_profile = reviewer_profiles[reviewer_email]

        # find conflicts between the reviewer's profile and the paper's authors' profiles
        user_entry = {
            'userId': reviewer_profile.id,
            'scores': {
                'tpms_score': random.random()
            }
        }

        conflicts = utils.get_conflicts(author_profiles, reviewer_profile)

        if conflicts:
            user_entry['scores']['conflict_score'] = '-inf'
            user_entry['conflicts'] = conflicts

        entries.append(user_entry)

    return entries

def generate_metadata(client, metadata_inv, papers_by_forum, reviewer_profiles):
    metadata_by_forum = {}
    for forum in papers_by_forum:
        paper = papers_by_forum[forum]
        paper_author_profiles = client.get_profiles(paper.content['authorids'])
        entries = build_entries(paper, paper_author_profiles, reviewer_profiles)
        new_metadata_note = client.post_note(metadata_note(paper, metadata_inv, entries=entries))
        metadata_by_forum[forum] = new_metadata_note
        print(new_metadata_note.id)

    return metadata_by_forum

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="openreview base URL")
    parser.add_argument('--username')
    parser.add_argument('--password')

    args = parser.parse_args()

    ## Initialize the client library with username and password
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
    print("connecting to", client.baseurl)

    print('clearing existing metadata')
    clear(client, iclr19.METADATA_INV_ID)
    metadata_inv = client.post_invitation(iclr19.metadata_inv)

    print('clearing existing assignments')
    clear(client, iclr19.ASSIGNMENT_INV_ID)
    client.post_invitation(iclr19.assignment_inv)

    print('clearing existing configurations')
    clear(client, iclr19.CONFIG_INV_ID)
    client.post_invitation(iclr19.config_inv)

    print('converting reviewers to profile IDs')
    reviewers_group, reviewer_profiles = canonicalize_reviewers(client, iclr19.REVIEWERS_ID)

    print('posting ICLR 19 submission invitation')
    submission_inv = iclr19.submission_inv
    submission_inv.process = ''
    submission_inv_no_process = client.post_invitation(submission_inv)

    print('posting ICLR 18 submissions to ICLR 19')
    submit_papers(client, 'ICLR.cc/2018/Conference/-/Submission', submission_inv_no_process)

    print('get new ICLR 19 papers')
    papers_by_forum = { paper.forum: paper
        for paper in openreview.tools.iterget_notes(client, invitation=submission_inv_no_process.id) }

    print('generating and posting metadata notes')
    generate_metadata(client, metadata_inv, papers_by_forum, reviewer_profiles)

    papers_by_forum = {p.forum: p for p in openreview.tools.iterget_notes(client, invitation=submission_inv.id)}
