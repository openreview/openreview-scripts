import argparse
import openreview
import openreview_matcher

# Argument handling
parser = argparse.ArgumentParser()
parser.add_argument('--username')
parser.add_argument('--password')
parser.add_argument('--baseurl', help="base URL")
args = parser.parse_args()

client = openreview.Client(username=args.username, password=args.password, baseurl=args.baseurl)

reviewers_group = client.get_group('cv-foundation.org/ECCV/2018/Demo/Reviewers')
metadata_invitation = client.get_invitation('cv-foundation.org/ECCV/2018/Demo/-/Paper_Metadata')
submission_invitation = client.get_invitation('cv-foundation.org/ECCV/2018/Demo/-/Submission')
assignment_invitation = client.get_invitation('cv-foundation.org/ECCV/2018/Demo/-/Paper_Assignments')

papers = client.get_notes(invitation='cv-foundation.org/ECCV/2018/Demo/-/Submission')

affinity_feature = openreview_matcher.metadata.BasicAffinity('affinity_score', client, [reviewers_group], papers)

def get_metadata(forum):
    return openreview_matcher.metadata.generate_metadata_note(
        #reviewers=reviewers_group.members,
        groups = [reviewers_group],
        features=[affinity_feature],
        note_params={
                'forum': forum,
                'invitation': metadata_invitation.id,
                'readers': ['everyone'],
                'writers': ['~Super_User1'],
                'signatures': ['~Super_User1']
            })

metadata_notes = [get_metadata(note.forum) for note in papers]

for p in metadata_notes: client.post_note(p)

reviewer_configuration = {
    "label": 'reviewers',
    "group": reviewers_group.id,
    "submission": submission_invitation.id,
    "exclude": [],
    "metadata": metadata_invitation.id,
    "minusers": 1,
    "maxusers": 3,
    "minpapers": 0,
    "maxpapers": 5,
    "weights": {
        "affinity_score": 1
    }
}

note_params = {
    'invitation': assignment_invitation.id,
    'readers': ['everyone'],
    'writers': ['~Super_User1'],
    'signatures': ['~Super_User1'],
}

reviewer_note = client.post_note(openreview.Note(
    content = {'configuration': reviewer_configuration}, **note_params))

print reviewer_note.id
