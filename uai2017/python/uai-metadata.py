#!/usr/bin/python

"""
Initializes the structures used for paper/user metadata
"""

import argparse
from collections import defaultdict

import openreview
import match_utils

from uaidata import *

# Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--download', help = "the filename (without extension) of the .pkl file to save the downloaded data. Defaults to ./metadata")
parser.add_argument('--upload', help = "the .pkl file (with extension) to upload to OpenReview. If \"true\", defaults to ./metadata.pkl")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--baseurl', help = "base URL")

args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

if args.download:
    download = args.download
else:
    download = './metadata'

if not args.upload:
    # API calls
    print "Getting paper notes..."
    paper_notes = client.get_notes(invitation = CONFERENCE + "/-/blind-submission")
    papers_by_forum = {n.forum: n for n in paper_notes}
    originalforum_by_paperforum = {n.forum: n.original for n in paper_notes}

    original_notes = client.get_notes(invitation = CONFERENCE + "/-/submission")
    originals_by_forum = {n.forum: n for n in original_notes}

    print "Getting submission metadata..."
    paper_metadata_notes = client.get_notes(invitation = CONFERENCE + '/-/Paper/Metadata')
    metadata_by_forum = {n.forum: n for n in paper_metadata_notes}

    print "Getting reviewer metadata..."
    reviewer_metadata_notes = client.get_notes(invitation = CONFERENCE + '/-/Reviewer/Metadata')
    metadata_by_reviewer = {u.content['name']: u for u in reviewer_metadata_notes}

    print "Getting areachair metadata..."
    areachair_metadata_notes = client.get_notes(invitation = CONFERENCE + '/-/Area_Chair/Metadata')
    metadata_by_areachair = {u.content['name']: u for u in areachair_metadata_notes}

    print "Getting reviewer expertise..."
    reviewer_expertise_notes = client.get_notes(invitation = CONFERENCE + '/-/Reviewer_Expertise')
    registered_expertise_by_reviewer = {n.signatures[0]: n.content for n in reviewer_expertise_notes}

    print "Getting areachair expertise..."
    areachair_expertise_notes = client.get_notes(invitation = CONFERENCE + '/-/SPC_Expertise')
    registered_expertise_by_ac = {n.signatures[0]: n.content for n in areachair_expertise_notes}

    print "Getting user groups..."
    reviewers_group = client.get_group(PC)
    areachairs_group = client.get_group(SPC)

    print "Getting bids..."
    bids = client.get_tags(invitation = CONFERENCE + '/-/Add/Bid')

    print "Processing bids..."
    bids_by_forum = defaultdict(list)
    deleted_papers = set()
    for b in bids:
        try:
            n = papers_by_forum[b.forum]
            bids_by_forum[n.forum].append(b)
        except KeyError as e:
            deleted_papers.update([b.forum])

    print "Getting areachair recommendations..."
    recs = []
    for n in paper_notes:
        recs += client.get_tags(invitation='auai.org/UAI/2017/-/Paper%s/Recommend/Reviewer' % n.number)

    print "Processing recommendations..."
    recs_by_forum = defaultdict(list)
    for r in recs:
        try:
            n = papers_by_forum[r.forum]
            recs_by_forum[n.forum].append(r)
        except KeyError as e:
            deleted_papers.update([r.forum])

    # Get conflict information
    print "Getting conflict of interesting information... (this may take a while)"
    domains_by_user = defaultdict(set)

    for reviewer in reviewers_group.members:
        if reviewer not in domains_by_user.keys():
            try:
                reviewer_profile = client.get_profile(reviewer)
                domains_by_user[reviewer] = set([p.split('@')[1] for p in reviewer_profile.content['emails']])
            except openreview.OpenReviewException:
                print "Profile not found for reviewer %s" % reviewer
                pass

    for areachair in areachairs_group.members:
        if areachair not in domains_by_user.keys():
            try:
                areachair_profile = client.get_profile(areachair)
                domains_by_user[areachair] = set([p.split('@')[1] for p in areachair_profile.content['emails']])
            except openreview.OpenReviewException:
                print "Profile not found for areachair %s" % areachair
                pass

    domains_by_email = defaultdict(set)

    for n in original_notes:
        author_emails = n.content['authorids']
        for author_email in author_emails:
            try:
                author_profile = client.get_profile(author_email)
                domains_by_email[author_email] = set([p.split('@')[1] for p in author_profile.content['emails']])
            except openreview.OpenReviewException:
                pass


    data = {
        'reviewers_group': reviewers_group,
        'areachairs_group': areachairs_group,
        'papers_by_forum': papers_by_forum,
        'originals_by_forum': originals_by_forum,
        'originalforum_by_paperforum': originalforum_by_paperforum,
        'metadata_by_forum': metadata_by_forum,
        'metadata_by_reviewer': metadata_by_reviewer,
        'metadata_by_areachair': metadata_by_areachair,
        'domains_by_user': domains_by_user,
        'domains_by_email': domains_by_email,
        'bids_by_forum': bids_by_forum,
        'recs_by_forum': recs_by_forum,
        'registered_expertise_by_reviewer': registered_expertise_by_reviewer,
        'registered_expertise_by_ac': registered_expertise_by_ac
    }

    print "Saving OpenReview metadata to %s.pkl" % download
    match_utils.save_obj(data, download)

if args.upload:
    if args.upload.lower() == 'true':
        data = match_utils.load_obj('./metadata.pkl')
    else:
        data = match_utils.load_obj(args.upload)
    print "Uploading metadata to OpenReview"
    metadata_by_forum = data['metadata_by_forum']
    metadata_by_reviewer = data['metadata_by_reviewer']
    metadata_by_areachair = data['metadata_by_areachair']

    for n in metadata_by_forum.values():
        client.post_note(n)

    for n in metadata_by_reviewer.values():
        client.post_note(n)

    for n in metadata_by_areachair.values():
        client.post_note(n)

    print "Done."
