
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
    data = {}

    data['papers_by_forum'] = {n.forum: n for n in client.get_notes(invitation='auai.org/UAI/2017/-/blind-submission')}
    data['metadata_by_forum'] = {n.forum: n for n in client.get_notes(invitation='auai.org/UAI/2017/-/Paper/Metadata')}

    data['user_groups'] = [client.get_group(PC),client.get_group(SPC)]

    reviewer_expertise_notes = client.get_notes(invitation = CONFERENCE + '/-/Reviewer_Expertise')
    areachair_expertise_notes = client.get_notes(invitation = CONFERENCE + '/-/SPC_Expertise')
    data['subjectareas_by_signature'] = {n.signatures[0]: n.content for n in areachair_expertise_notes+reviewer_expertise_notes}

    data['bids_by_signature'] = {bid.signatures[0]: bid for bid in client.get_tags(invitation = CONFERENCE + '/-/Add/Bid') if bid.forum in data['papers_by_forum']}

    data['bid_score_map'] = {
        "I want to review": 1.0,
        "I can review": 0.75,
        "I can probably review but am not an expert": 0.5,
        "I cannot review": 0.25,
        "No bid": 0.0
    }

    print "Getting areachair recommendations..."
    recs = []
    for n in data['papers_by_forum'].values():
        recs += client.get_tags(invitation='auai.org/UAI/2017/-/Paper%s/Recommend/Reviewer' % n.number)

    data['recs_by_forum'] = defaultdict(list)
    for r in recs:
        if r.forum in data['papers_by_forum']:
            n = data['papers_by_forum'][r.forum]
            data['recs_by_forum'][n.forum].append(r)
        else:
            deleted_papers.update([r.forum])

    print "Saving OpenReview metadata to %s.pkl" % download
    match_utils.save_obj(data, download)

if args.upload:
    if args.upload.lower() == 'true':
        data = match_utils.load_obj('./metadata.pkl')
    else:
        data = match_utils.load_obj(args.upload)
    print "Uploading metadata to OpenReview"


    for n in data['metadata_by_forum'].values():
        client.post_note(n)

    print "Done."
