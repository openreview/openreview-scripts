# Setup creates the group for the conference and adds a link to it in the parent group webfield
# create PC group
# creates NIPS_Submission invitation


import argparse
import openreview

parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base url")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()

# client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

baseUrl = "http://localhost:3000"
superUser = 'OpenReview.net'
password = 'OpenReview_dev'
client = openreview.Client(baseurl=baseUrl, username=superUser, password=password)


CONFERENCE_ID = 'ML_Reproducibility_Challenge/2020'
PROGRAM_CHAIRS_ID = CONFERENCE_ID + '/Program_Chairs'
SUBMISSION_ID = CONFERENCE_ID + '/-/Submission'
AUTHORS_ID = CONFERENCE_ID + '/Authors'
ACCEPTED_PAPER_ID = CONFERENCE_ID + '/-/Accepted_Papers'

# builder = openreview.builder.ConferenceBuilder(client)
# builder.set_CONFERENCE_ID(CONFERENCE_ID)
# builder.set_conference_name('ML Reproducibility Challenge 2020')

# builder.set_homepage_header({
#     'title': 'NeurIPS 2019 Reproducibility Challenge',
#     'deadline': 'Submission Claims accepted from 2019-Sept-7, to 2019-Nov-1 (GMT)',
#     'date': 'December 13-14, 2019',
#     'website': 'https://reproducibility-challenge.github.io/neurips2019/dates/',
#     'location': 'Vancouver, Canada',
# })

# # WARNING: this submission stage is being set as "Public", even though it really shouldn't be.
# # We're doing this because there are some behaviors that we don't understand about the builder
# # that happen when you set public=False.
# # The Report invitation is being made private manually below.
# builder.set_submission_stage(
#     name='Report',
#     double_blind=True,
#     public=True,
#     additional_fields={
#         'track': {
#            'required': True,
#            'value-dropdown': ['Baseline', 'Ablation', 'Replicability']
#         },
#         'NeurIPS_paper_id': {
#                'required': False,
#                'value-regex': '.*'
#         }
#     },
#     remove_fields=['keywords', 'TL;DR'],
#     start_date=datetime.datetime(2019, 11, 1),
#     due_date=datetime.datetime(2019, 12, 2, 12)
# )

# builder.set_override_homepage(True)
# conference = builder.get_result()

# ~ Everything below is custom to the "Claims" mechanism(s) ~

# replace the builder-generated webfield with the custom webfield
with open('../webfield/conferenceWebfield.js') as f:
    homepage_webfield = f.read()

conference_group = client.get_group(CONFERENCE_ID)
conference_group.web = homepage_webfield
conference_group = client.post_group(conference_group)

# program_chairs = conference.set_program_chairs([])

# add venue to active because it doesn't have an invitation open to everyone
# so it won't show up under Open for Submission
# active_venues = client.get_group("active_venues")
# active_venues.members.append(CONFERENCE_ID)
# client.post_group(active_venues)

# add the "Claimants" group
client.post_group(openreview.Group(
    id=CONFERENCE_ID + '/Claimants',
    readers=[CONFERENCE_ID, PROGRAM_CHAIRS_ID],
    nonreaders=[],
    writers=[CONFERENCE_ID],
    signatories=[CONFERENCE_ID],
    signatures=[CONFERENCE_ID],
    members=[])
)

# modify the "Report" invitation such that only claimants can post
report_invitation = client.get_invitation(SUBMISSION_ID)
report_invitation.invitees = [CONFERENCE_ID+'/Claimants']
report_invitation.noninvitees = [CONFERENCE_ID+'/Authors']
report_invitation.readers = [CONFERENCE_ID+'/Claimants']
report_invitation.nonreaders = [CONFERENCE_ID+'/Authors']
report_invitation.reply['readers'] = {
    'values-copied': [
        CONFERENCE_ID,
        "{content.authorids}",
        "{signatures}",
        CONFERENCE_ID+"/Reviewers",
        PROGRAM_CHAIRS_ID
    ]
}

# with open('../process/reportProcess.py') as f:
#     report_invitation.process = f.read()

report_invitation = client.post_invitation(report_invitation)

# post the invitation used to upload accepted RL Accepted papers
rl_accepted_paper_submission_invitation = client.post_invitation(openreview.Invitation(**{
    'id': ACCEPTED_PAPER_ID,
    'invitees': [PROGRAM_CHAIRS_ID],
    'readers': ['everyone'],
    'writers': [CONFERENCE_ID],
    'signatures': [CONFERENCE_ID],
    'reply': {
        'content': {
            'title': {
                'value-regex': '.*',
                'required': True,
            },
            'authors': {
                'description': 'Comma separated list of author names.',
                'values-regex': '.*',
                'required': True
            },
            'pdf': {
                'description': 'PDF url',
                'value-regex': '.*',
                'required': True
            },
            'html': {
                'description': 'PWC url',
                'value-regex': '.*',
                'required': True
            },
            'venueid': {
                'description': 'ID of the venue in OpenReview',
                'value-regex': '.*',
                'required': True
            },
            'venue': {
                'value-regex': '.*',
                'required': True
            },
        },
        'forum': None,
        'replyto': None,
        'signatures': {
            'values': [PROGRAM_CHAIRS_ID]
        },
        'writers': {
            'values': [CONFERENCE_ID, PROGRAM_CHAIRS_ID]
        },
        'readers': {
            'values': ['everyone']
        }
    }
}))

claim_inv = client.post_invitation(openreview.Invitation(
    id='{}/-/Claim'.format(CONFERENCE_ID),
    readers=['everyone'],
    invitees=['~'],
    noninvitees=[CONFERENCE_ID + '/Claimants'],
    writers=[CONFERENCE_ID],
    signatures=[CONFERENCE_ID],
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
            },
            "team_members": {
                "description": "Comma separated list of team member names.",
                "values-regex": ".*",
                "order": 1,
                "required": False
            },
            "team_emails": {
                "description": "Comma separated list of team member email addresses, lowercased, in the same order as above. For authors with existing OpenReview accounts, please make sure that the provided email address(es) match those listed in the author's profile.",
                "values-regex": ".*",
                "order": 2,
                "required": False
            }
        },
        'invitation': ACCEPTED_PAPER_ID,
        'signatures': {
            'description': 'Your authorized identity to be associated with the above content.',
            'values-regex': '~.*'
        },
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values-copied': [PROGRAM_CHAIRS_ID, '{signatures}']
        },
        'writers': {
            'values-copied': [CONFERENCE_ID,'{signatures}']
        }
    },
    process='../process/claimProcess.py'
))


claim_hold_inv = client.post_invitation(openreview.Invitation(
    id='{}/-/Claim_Hold'.format(CONFERENCE_ID),
    readers=[],
    invitees=[CONFERENCE_ID],
    writers=[CONFERENCE_ID],
    signatures=[CONFERENCE_ID],
    reply={
        'content': {
            'title': {
                'value-regex': '.{1,120}',
                'order': 0,
                'required': True
            }
        },
        'invitation': ACCEPTED_PAPER_ID,
        'signatures': {'values': [CONFERENCE_ID]},
        'readers': {
            'description': 'The users who will be allowed to read the above content.',
            'values': ['everyone']
        },
        'writers': {
            'values-copied': [CONFERENCE_ID]
        }
    }
))


with open('../webfield/pcWebfield.js') as f:
    program_chairs = client.get_group(PROGRAM_CHAIRS_ID)
    program_chairs.web = f.read()
    program_chairs = client.post_group(program_chairs)

with open('../webfield/authorWebfield.js') as f:
    authors = client.get_group(AUTHORS_ID)
    authors.web = f.read()
    authors = client.post_group(authors)
