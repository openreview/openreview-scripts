import openreview
import icml
import random

client = openreview.Client()

posted_areachairs = client.get_group(icml.AREA_CHAIRS_ID)
posted_reviewers = client.get_group(icml.REVIEWERS_ID)

all_userids = posted_reviewers.members + posted_areachairs.members

# get all currently submitted papers
icml_submissions = openreview.tools.iterget_notes(client, invitation=icml.BLIND_SUBMISSION_ID)

for paper in icml_submissions:
    # assign one of 5 random area chairs
    random_ac = random.sample(posted_areachairs.members[:5], k=1)[0]
    openreview.tools.assign(client, paper.number, icml.CONFERENCE_ID,
        reviewer_to_add = random_ac,
        parent_label = 'Area_Chairs',
        individual_label = 'Area_Chair')

    assigned_ac_id = 'ICML.cc/2019/Conference/Paper{}/Area_Chairs'.format(paper.number)
    original = client.get_note(paper.original)
    if assigned_ac_id not in original.readers:
        original.readers.append(assigned_ac_id)
        client.post_note(original)

    posted_metadata = client.post_note(openreview.Note(**{
        'forum': paper.id,
        'replyto': paper.id,
        'invitation': icml.metadata_inv.id,
        'readers': [
            icml.CONFERENCE_ID,
            icml.AREA_CHAIRS_ID
        ],
        'writers': [icml.CONFERENCE_ID],
        'signatures': [icml.CONFERENCE_ID],
        'content': {
            'entries': [{
                'scores': {'affinity': random.random()},
                'userid': userid
            } for userid in posted_reviewers.members]
        }
    }))

print('areachairs assigned:')
for k in posted_areachairs.members[:5]:
    id_group = client.get_group(k)
    print(k, id_group.members)

