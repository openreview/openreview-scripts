import argparse
import openreview
from collections import defaultdict
import xml.etree.cElementTree as ET
import xml.dom.minidom as minidom
from uaidata import *

# Parse the arguments for user authentication
# .............................................................................

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')

args = parser.parse_args()

if args.username is not None and args.password is not None:
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    client = openreview.Client(baseurl=args.baseurl)


# Organize data
# .............................................................................

reviewers = client.get_group(PC)
reviewer_metadata_notes = client.get_notes(invitation = 'auai.org/UAI/2017/-/Reviewer/Metadata')
reviewer_metadata_by_id = {n.forum:n for n in reviewer_metadata_notes}

print "Generating reviewer metadata..."
for n in reviewer_metadata_notes:
    n.content['maxpapers'] = 3
    n.content['minpapers'] = 0

    reviewer_similarities = []
    for reviewer in reviewers.members:
        reviewer_similarities.append({
            'user': reviewer,
            'score': 1.0 if reviewer == n.content['name'] else 0,
            'source': 'DummyModel'
        })

    n.content['reviewers'] = reviewer_similarities

    client.post_note(n)

areachairs = client.get_group(SPC)
areachair_metadata_notes = client.get_notes(invitation = 'auai.org/UAI/2017/-/Area_Chair/Metadata')
areachair_metadata_by_id = {n.forum:n for n in areachair_metadata_notes}

print "Generating areachair metadata..."
for n in areachair_metadata_notes:
    areachair_similarities = []
    for areachair in areachairs.members:
        areachair_similarities.append({
            'user': areachair,
            'score': 1.0 if areachair == n.content['name'] else 0,
            'source': 'DummyModel'
        })

    n.content['areachairs'] = areachair_similarities
    client.post_note(n)
