# Setup creates the group for the conference and adds a link to it in the parent group webfield
# create PC group
# creates NIPS_Submission invitation


import argparse
import openreview
from openreview import tools
from openreview import invitations
import os
import json
import datetime

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

conference_id = 'reproducibility-challenge.github.io/Reproducibility_Challenge/NeurIPS/2019'

builder = openreview.builder.ConferenceBuilder(client)
builder.set_conference_id(conference_id)
builder.set_conference_name('NeurIPS 2019 Reproducibility Challenge')

builder.set_homepage_header({
    'title': 'NeurIPS 2019 Reproducibility Challenge',
    'deadline': 'Submission Claims accepted from 2019-Sept-7, to 2019-Nov-1 (GMT)',
    'date': 'December 13-14, 2019',
    'website': 'https://reproducibility-challenge.github.io/neurips2019/dates/',
    'location': 'Vancouver, Canada',

})

# WARNING: this submission stage is being set as "Public", even though it really shouldn't be.
# We're doing this because there are some behaviors that we don't understand about the builder
# that happen when you set public=False.
# The Report invitation is being made private manually below.
## PAM TODO set start time to Nov 1
builder.set_submission_stage(name='Report', double_blind=True, public=True, additional_fields = { 'track': {
                   'required': True,
                   'value-dropdown': ['Baseline', 'Ablation', 'Replicability']
            }, 'NeurIPS_paper_id': {
                   'required': False,
                   'value-regex': '.*'
            }}, remove_fields = ['keywords','TL;DR'])
builder.set_review_stage(start_date = datetime.datetime(2019, 12, 2), due_date = datetime.datetime(2019, 12, 6, 12),
                         release_to_authors = True)
builder.set_decision_stage(options=['Accept','Reject'], start_date = datetime.datetime(2019, 12, 5),
                           release_to_authors = True, release_to_reviewers = True)
builder.set_override_homepage(True)
conference = builder.get_result()

# replace the builder-generated webfield with the custom webfield
with open('../webfield/conferenceWebfield.js') as f:
    homepage_webfield = f.read()

conference_group = client.get_group(conference.get_id())
conference_group.web = homepage_webfield
conference_group = client.post_group(conference_group)

program_chairs = conference.set_program_chairs(['pca@email.com'])

# add venue to active because it doesn't have an invitation open to everyone
# so it won't show up under Open for Submission
active_venues = client.get_group("active_venues")
active_venues.members.append(conference_id)
client.post_group(active_venues)

# add the "Claimants" group
client.post_group(openreview.Group(
    id=conference_id + '/Claimants',
    readers=[conference_id, conference.get_program_chairs_id()],
    nonreaders=[],
    writers=[conference_id],
    signatories=[conference_id],
    signatures=[conference_id],
    members=[])
)

# modify the "Report" invitation such that only claimants can post
report_invitation = client.get_invitation(conference.get_submission_id())
report_invitation.invitees = [conference_id+'/Claimants']
report_invitation.noninvitees = [conference_id+'/Authors']
report_invitation.readers = [conference_id+'/Claimants']
report_invitation.nonreaders = [conference_id+'/Authors']
report_invitation.reply['readers'] = {
    'values-copied': [
        conference_id,
        "{content.authorids}",
        "{signatures}",
        conference_id+"/Reviewers",
        conference.get_program_chairs_id()
    ]
}

with open('../process/reportProcess.py') as f:
    report_invitation.process = f.read()

report_invitation = client.post_invitation(report_invitation)

# post the invitation used to upload accepted NeurIPS papers
neurips_submission_invitation = client.post_invitation(openreview.Invitation(**{
    'id': '{}/-/NeurIPS_Submission'.format(conference_id),
    'invitees': [conference.get_program_chairs_id()],
    'readers': ['everyone'],
    'writers': [conference.get_id()],
    'signatures': [conference.get_id()],
    'reply': {
        'content': {
            'title': {
                'value-regex': '.*',
                'required': True,
            },
            'abstract': {
                'value-regex': '.*',
                'required': True
            },
            'authors': {
                'description': 'Comma separated list of author names.',
                'values-regex': '.*',
                'required': True
            },
            'authorsids': {
                'description': 'Comma separated list of author email addresses, lowercased, in the same order as above. For authors with existing OpenReview accounts, please make sure that the provided email address(es) match those listed in the author\'s profile.',
                'values-regex': "([a-z0-9_\-\.]{1,}@[a-z0-9_\-\.]{2,}\.[a-z]{2,},){0,}([a-z0-9_\-\.]{1,}@[a-z0-9_\-\.]{2,}\.[a-z]{2,})",
                'required': False
            },
            'code_link': {
                'description': 'url for source code',
                'values-regex': '.*',
                'required': False
            },
            'pdf_link': {
                'description': 'url for camera ready submission',
                'values-regex': '.*',
                'required': False
            },
        },
        'forum': None,
        'replyto': None,
        'signatures': {
            'values': [conference.get_program_chairs_id()]
        },
        'writers': {
            'values': [conference.get_id()]
        },
        'readers': {
            'values': ['everyone']
        }
    }
}))

claim_inv = client.post_invitation(openreview.Invitation(
    id='{}/-/Claim'.format(conference_id),
    readers=['everyone'],
    invitees=['~'],
    noninvitees=[conference_id + '/Claimants'],
    writers=[conference_id],
    signatures=[conference_id],
    reply={
        'content': {
            'title': {
                'value': 'Claim',
                'order': 0,
                'required': True
            },
            'plan': {'description': 'Your plan to reproduce results(max 5000 chars).',
                'order': 1,
                'required': True,
                'value-regex': '[\\S\\s]{1,5000}'
            },
            'institution': {
                'description': 'Your institution or organization(max 100 chars).',
                'order': 2,
                'required': True,
                'value-regex': '.{1,100}'
            },
            'track': {
                   'order': 3,
                   'required': True,
                   'value-dropdown': ['Baseline', 'Ablation', 'Replicability']
            },
            'compute_resources': {'description': 'Do you need compute resources?',
                 'order': 4,
                 'required': True,
                 'value-radio': ['yes','no']
            }
        },
        'invitation': '{}/-/NeurIPS_Submission'.format(conference_id),
        'signatures': {
            'description': 'Your authorized identity to be associated with the above content.',
            'values-regex': '~.*'
        },
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values-copied': [conference_id + '/Program_Chairs', '{signatures}']
        },
        'writers': {
            'values-copied': [conference_id,'{signatures}']
        }
    },
    process='../process/claimProcess.py'
))


claim_hold_inv = client.post_invitation(openreview.Invitation(
    id='{}/-/Claim_Hold'.format(conference_id),
    readers=[],
    invitees=['~'],
    writers=[conference_id],
    signatures=[conference_id],
    reply={
        'content': {
            'title': {
                'value-regex': '.{1,120}',
                'order': 0,
                'required': True
            }
        },
        'invitation': '{}/-/NeurIPS_Submission'.format(conference_id),
        'signatures': {'values': [conference_id]},
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values': ['everyone']
        },
        'writers': {
            'values-copied': [conference_id]
        }
    }
))


with open('../webfield/pcWebfield.js') as f:
    program_chairs = client.get_group(conference.get_program_chairs_id())
    program_chairs.web = f.read()
    program_chairs = client.post_group(program_chairs)

with open('../webfield/authorWebfield.js') as f:
    authors = client.get_group(conference.get_authors_id())
    authors.web = f.read()
    authors = client.post_group(authors)