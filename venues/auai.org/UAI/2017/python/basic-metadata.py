import argparse
import openreview
import openreview_matcher
import config


# Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--overwrite', action='store_true', help = "if present, erases the old metadata")
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--baseurl', help = "base URL")
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

group_ids = [
    config.PC,
    config.SPC
]

print "getting notes..."
papers = client.get_notes(invitation=config.SUBMISSION)
groups = [client.get_group(g) for g in group_ids]

if args.overwrite:
    print "erasing old metadata..."
    paper_metadata = client.get_notes(invitation=config.METADATA)
    for p in paper_metadata: client.delete_note(p)

# Define features
print "building feature models..."
paper_features = [
    openreview_matcher.metadata.BasicAffinity(
        name='basic_affinity',
        client=client,
        groups=groups,
        papers=papers
    )
]

print "generating paper metadata..."
def metadata(forum):
    return openreview_matcher.metadata.generate_metadata_note(groups=groups, features=paper_features, note_params={
        'forum': forum,
        'invitation': config.METADATA,
        'readers': [config.CONFERENCE],
        'writers': [config.CONFERENCE],
        'signatures': [config.CONFERENCE]
    })
metadata_notes = [metadata(note.forum) for note in papers]

post_notes = raw_input("Would you like to post the metadata notes? (y/[n]): ")

if post_notes.lower()=='y':
    print "posting paper metadata..."
    for p in metadata_notes: client.post_note(p)
