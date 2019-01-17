import openreview
import icml
import random

client = openreview.Client()

# groups
icml_groups = openreview.tools.build_groups(icml.conference.id)
for group in icml_groups:
    try:
        existing_group = client.get_group(group.id)
    except openreview.OpenReviewException as e:
        posted_group = client.post_group(group)
        print(posted_group.id)

# post the conference group with updated parameters
posted_conference = client.post_group(icml.conference)

reviewers = icml.reviewers
areachairs = icml.area_chairs

# borrow the reviewers and area chairs from AKBC
reviewers.members = client.get_group('AKBC.ws/2019/Conference/Reviewers').members
areachairs.members = client.get_group('AKBC.ws/2019/Conference/Area_Chairs').members

posted_areachairs = client.post_group(areachairs)
posted_reviewers = client.post_group(reviewers)

all_userids = posted_reviewers.members + posted_areachairs.members

# invitations
posted_submission_inv = client.post_invitation(icml.submission_inv)
posted_blind_inv = client.post_invitation(icml.blind_submission_inv)

posted_assignment_inv = client.post_invitation(icml.assignment_inv)
posted_config_inv = client.post_invitation(icml.config_inv)
posted_metadata_inv = client.post_invitation(icml.metadata_inv)
posted_constraint_inv = client.post_invitation(icml.lock_tag_inv)

# repost 20 papers from AKBC 2019 and supporting data notes
for paper in client.get_notes(invitation='AKBC.ws/2019/Conference/-/Submission'):
    new_content = {key: value for key, value in paper.content.items()                    if key in posted_submission_inv.reply['content'].keys()}

    new_writers = [w.replace('AKBC.ws', 'ICML.cc') for w in paper.writers]
    print('new_writers', new_writers)
    posted_submission = client.post_note(openreview.Note(**{
        'writers': new_writers,
        'readers': [icml.CONFERENCE_ID],
        'content': new_content,
        'invitation': icml.SUBMISSION_ID,
        'signatures': [icml.CONFERENCE_ID]
    }))

    papergroup = client.post_group(openreview.Group.from_json({
        'id': 'ICML.cc/2019/Conference/Paper{}'.format(posted_submission.number),
        'readers': ['everyone'],
        'writers': [icml.CONFERENCE_ID],
        'signatures': [icml.CONFERENCE_ID],
        'signatories': [],
        'members': []
    }))

    posted_mask = client.post_note(openreview.Note(**{
        'original': posted_submission.id,
        'forum': None,
        'replyto': None,
        'readers': ['everyone'],
        'writers': [icml.CONFERENCE_ID],
        'signatures': [icml.CONFERENCE_ID],
        'invitation': posted_blind_inv.id,
        'content': {
            key: entry.get('value') or entry.get('values') \
            for key, entry in posted_blind_inv.reply['content'].items() \
            if 'value' in entry or 'values' in entry
       }
    }))

    # simulate some metadata for this paper
    posted_metadata = client.post_note(openreview.Note(**{
        'forum': posted_mask.id,
        'replyto': posted_mask.id,
        'invitation': icml.metadata_inv.id,
        'readers': [
            icml.CONFERENCE_ID,
            posted_areachairs.id
        ],
        'writers': [icml.CONFERENCE_ID],
        'signatures': [icml.CONFERENCE_ID],
        'content': {
            'entries': [{
                'scores': {'affinity': random.random()},
                'userid': userid
            } for userid in all_userids]

        }
    }))

# get all currently submitted papers
icml_submissions = openreview.tools.iterget_notes(client, invitation=icml.BLIND_SUBMISSION_ID)

for paper in icml_submissions:
    # assign one of 5 random area chairs
    random_ac = random.sample(posted_areachairs.members[:5], k=1)[0]
    openreview.tools.assign(client, paper.number, icml.CONFERENCE_ID,
        reviewer_to_add = random_ac,
        parent_label = 'Area_Chairs',
        individual_label = 'Area_Chair')

    original = client.get_note(paper.original)
    original.readers.append('ICML.cc/2019/Conference/Paper{}/Area_Chairs'.format(paper.number))
    client.post_note(original)

print('areachairs assigned:')
for k in posted_areachairs.members[:5]:
    id_group = client.get_group(k)
    print(k, id_group.members)

