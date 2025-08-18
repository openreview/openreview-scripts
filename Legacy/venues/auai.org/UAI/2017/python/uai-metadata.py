import argparse
from collections import defaultdict
import imp
import openreview
from openreview_matcher.metadata import generate_metadata_note
from openreview_matcher import utils
import config
import uai_features

# Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--save', help = "the filename (without extension) of the .pkl file to save the downloaded data. Defaults to ./metadata")
parser.add_argument('--overwrite', action='store_true', help = "if present erases the old metadata")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--baseurl', help = "base URL")
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

save_file = './metadata' if args.save == None else args.save

print "getting notes..."
papers = client.get_notes(invitation='auai.org/UAI/2017/-/blind-submission')
program_committee = client.get_group('auai.org/UAI/2017/Program_Committee')

def clear_metadata():
    print "erasing old metadata..."
    paper_metadata = client.get_notes(invitation='auai.org/UAI/2017/-/Paper/Metadata')
    for p in paper_metadata: client.delete_note(p)

if args.overwrite: clear_metadata()

print "getting expertise..."
reviewer_expertise_notes = client.get_notes(invitation = config.CONFERENCE + '/-/Reviewer_Expertise')
areachair_expertise_notes = client.get_notes(invitation = config.CONFERENCE + '/-/SPC_Expertise')

print "getting recommendations..."
recs = []
for p in papers:
    recs += client.get_tags(invitation='auai.org/UAI/2017/-/Paper%s/Recommend/Reviewer' % p.number)

bids = client.get_tags(invitation = config.CONFERENCE + '/-/Add/Bid')

subject_area_overlap_data = {
    'subject_areas': reviewer_expertise_notes + areachair_expertise_notes,
    'papers': papers
}

# Define features
paper_features = [
    uai_features.PrimarySubjectOverlap(name='primary_subject_overlap', data=subject_area_overlap_data),
    uai_features.SecondarySubjectOverlap(name='secondary_subject_overlap', data=subject_area_overlap_data),
    uai_features.BidScore(name='bid_score', data=bids),
    uai_features.ACRecommendation(name='ac_recommendation', data=recs),
]

user_groups = {
    config.PC: client.get_group(config.PC),
    config.SPC: client.get_group(config.SPC)
}

print "generating paper metadata..."

def metadata(forum):
    return generate_metadata_note(groups=user_groups.values(), features=paper_features, note_params={
        'forum': forum,
        'invitation': 'auai.org/UAI/2017/-/Paper/Metadata',
        'readers': ['auai.org/UAI/2017'],
        'writers': ['auai.org/UAI/2017'],
        'signatures': ['auai.org/UAI/2017']
    })

metadata_notes = [metadata(note.forum) for note in papers]

print "Saving OpenReview metadata to %s.pkl" % save_file
utils.save_obj(
    {
        'user_groups': user_groups,
        'papers': papers,
        'paper_metadata': metadata_notes,
    },
    save_file)

post_notes = raw_input("Would you like to post the metadata notes? (y/[n]): ")

if post_notes.lower()=='y':
    print "posting paper metadata..."
    for p in metadata_notes: client.post_note(p)
