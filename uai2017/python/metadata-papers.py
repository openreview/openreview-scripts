import argparse
import openreview
from collections import defaultdict
import xml.etree.cElementTree as ET
import xml.dom.minidom as minidom
from uaidata import *
import match_utils

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
    client = openreview.Client()


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
 'I cannot review': '-inf',
 'No bid': 0.0
}

print "Obtaining reviewer-relevant data..."
## Reviewer-relevant data
reviewers = client.get_group(PC)
bids = client.get_tags(invitation='auai.org/UAI/2017/-/Add/Bid')
metadata_notes = client.get_notes(invitation = 'auai.org/UAI/2017/-/Paper/Metadata')
metadata_by_id = {n.forum:n for n in metadata_notes}

bids_by_number = defaultdict(list)
bids_by_id = defaultdict(list)

print "Processing bids... (this may take a while)"
for b in bids:
    n = client.get_note(b.forum)
    bids_by_number[n.number].append(b)
    bids_by_id[n.forum].append(b)

print "Processing submissions..."
submissions = client.get_notes(invitation='auai.org/UAI/2017/-/blind-submission')
recs = []
for n in submissions:
    recs += client.get_tags(invitation='auai.org/UAI/2017/-/Paper%s/Recommend/Reviewer' % n.number)

recs_by_number = defaultdict(list)
recs_by_id = defaultdict(list)

print "Processing recommendations..."
for r in recs:
    n = client.get_note(r.forum)
    recs_by_number[n.number].append(r)
    recs_by_id[n.forum].append(r)

print "Obtaining areachair-relevant data..."
## Areachair-relevant data
areachairs = client.get_group(SPC)
profile_expertise_by_ac = {}
registered_expertise_by_ac = {}

for a in [x for x in areachairs.members if '~' in x]:
    profile = client.get_profile(a)
    profile_expertise_by_ac[a] = profile.content['expertise']

spc_reg_responses = client.get_notes(invitation='auai.org/UAI/2017/-/SPC_Expertise')
for reg in spc_reg_responses:
    registered_expertise_by_ac[reg.signatures[0]] = reg.content

missing_spc_reg = set()

print "Populating metadata notes..."
# Populate Metadata notes
# .............................................................................

for n in metadata_notes:
    forum = n.forum
    reviewer_metadata = []
    areachair_metadata = []
    paper_metadata = []
    paper_note = client.get_note(forum)

    for bid in bids_by_id[forum]:

        if bid.signatures[0] in reviewers.members:
            reviewer_metadata.append({
                'user': bid.signatures[0],
                'score': bid_score_map[bid.tag],
                'source': 'ReviewerBid'
            })
        if bid.signatures[0] in areachairs.members:
            areachair_metadata.append({
                'user': bid.signatures[0],
                'score': bid_score_map[bid.tag],
                'source': 'AreachairBid'
            })

    for bid in recs_by_id[forum]:
        reviewer_metadata.append({
            'user': bid.tag,
            'score': '+inf',
            'source': 'AreachairRec'
        })

    # The following for loop is needed until we have a real way of getting reviewer-paper scores
    for reviewer in reviewers.members:
        reviewer_metadata.append({
            'user': reviewer,
            'score': 0.5,
            'source': 'DummyModel'
        })

    # The following for loop is needed until we have a real way of getting paper-paper scores
    for m in metadata_notes:
        paper_metadata.append({
            'submissionId': paper_note.number,
            'score': 1.0 if m.forum == n.forum else 0.0,
            'source': 'DummyModel'
        })

    for a in areachairs.members:
        if a in registered_expertise_by_ac.keys():
            registered_ac = a
            ac_affinity = match_utils.subject_area_affinity(
                paper_note.content['subject areas'],
                registered_expertise_by_ac[registered_ac]['primary area'],
                registered_expertise_by_ac[registered_ac]['additional areas'],
                primary_weight = 0.7
            )

            areachair_metadata.append({
                'user': registered_ac,
                'score': ac_affinity,
                'source': 'SubjectAreaOverlap'
            })
        else:
            missing_spc_reg.update([a])

    metadata_by_id[forum].content['minreviewers'] = 1
    metadata_by_id[forum].content['maxreviewers'] = 3
    metadata_by_id[forum].content['minareachairs'] = 0
    metadata_by_id[forum].content['maxareachairs'] = 1
    metadata_by_id[forum].content['reviewers'] = reviewer_metadata
    metadata_by_id[forum].content['areachairs'] = areachair_metadata
    metadata_by_id[forum].content['papers'] = paper_metadata
    metadata_by_id[forum].content['title'] = paper_note.content['title']

    client.post_note(metadata_by_id[forum])

print "Done."
print ''
print "Missing AC registration: "
for spc in list(missing_spc_reg):
    print spc

