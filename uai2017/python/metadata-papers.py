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
parser.add_argument('--bidscores', help="The xml file containing the reviewer bids")
parser.add_argument('--out', help="output file")

args = parser.parse_args()

if args.username is not None and args.password is not None:
    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
else:
    client = openreview.Client(baseurl=args.baseurl)


# Function definitions
# .............................................................................

def prettify(elem):
    """Return a pretty-printed XML string for the Element.
    """
    rough_string = ET.tostring(elem, 'utf-8')
    reparsed = minidom.parseString(rough_string)
    return reparsed.toprettyxml(indent="\t")


# Organize data
# .............................................................................

bid_score_map = {
 'I want to review': 1.0,
 'I can review': 0.75,
 'I can probably review but am not an expert': 0.5,
 'I cannot review': 0.25,
 'No bid': 0.0
}

reviewers = client.get_group(PC)
bids = client.get_tags(invitation='auai.org/UAI/2017/-/Add/Bid')
metadata_notes = client.get_notes(invitation = 'auai.org/UAI/2017/-/Paper/Metadata')
metadata_by_id = {n.forum:n for n in metadata_notes}

bids_by_number = defaultdict(list)
bids_by_id = defaultdict(list)

for b in bids:
    n = client.get_note(b.forum)
    bids_by_number[n.number].append(b)
    bids_by_id[n.forum].append(b)

submissions = client.get_notes(invitation='auai.org/UAI/2017/-/blind-submission')
recs = []
for n in submissions:
    recs += client.get_tags(invitation='auai.org/UAI/2017/-/Paper%s/Recommend/Reviewer' % n.number)

recs_by_number = defaultdict(list)
recs_by_id = defaultdict(list)

for r in recs:
    n = client.get_note(r.forum)
    recs_by_number[n.number].append(r)
    recs_by_id[n.forum].append(r)

# Write data to XML file, if applicable
# .............................................................................

if args.out != None:
    root = ET.Element("reviewerbid")

    # open questions:
    # can "email" field just be tilde ID field? it would make things easier
    # can submission ID be the hash ID, or is it better for it to be the number?
    for n in bids_by_number:
        submission = ET.SubElement(root, "submission", submissionId = str(n))
        for b in bids_by_number[n]:
            profile = client.get_profile(b.signatures[0])
            ET.SubElement(submission, "reviewer", email=profile.content['preferred_email'], score=str(bid_score_map[b.tag]), source=b.invitation)

    #this code writes the file in a "minified" format
    #tree = ET.ElementTree(root)
    #tree.write(args.out)

    #this code writes a pretty version
    with open(out,'w') as f:
        f.write(prettify(root))

# Populate Metadata notes
# .............................................................................

for n in metadata_notes:
    forum = n.forum
    reviewer_metadata = []
    paper_metadata = []
    paper_note = client.get_note(forum)

    for bid in bids_by_id[forum]:
        reviewer_metadata.append({
            'reviewer': bid.signatures[0],
            'score': bid_score_map[bid.tag],
            'source': 'ReviewerBid'
        })

    for bid in recs_by_id[forum]:
        reviewer_metadata.append({
            'reviewer': bid.tag,
            'score': 1.0,
            'source': 'AreachairRec'
        })

    # The following for loop is needed until we have a real way of getting reviewer-paper scores
    for reviewer in reviewers.members:
        reviewer_metadata.append({
            'reviewer': reviewer,
            'score': 0.5,
            'source': 'DummyModel'
        })

    # The following for loop is needed until we have a real way of getting paper-paper scores
    for m in metadata_notes:
        paper_metadata.append({
            'submissionId': m.number,
            'score': 1.0 if m.forum == n.forum else 0.0,
            'source': 'DummyModel'
        })

    metadata_by_id[forum].content['reviewers'] = reviewer_metadata
    metadata_by_id[forum].content['papers'] = paper_metadata
    metadata_by_id[forum].content['minreviewers'] = 1
    metadata_by_id[forum].content['maxreviewers'] = 1
    metadata_by_id[forum].content['title'] = paper_note.content['title']

    client.post_note(metadata_by_id[forum])


