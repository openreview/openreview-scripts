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

client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

CONFERENCE_ID = 'ML_Reproducibility_Challenge/2020'
PROGRAM_CHAIRS_ID = CONFERENCE_ID + '/Program_Chairs'
SUBMISSION_ID = CONFERENCE_ID + '/-/Submission'
AUTHORS_ID = CONFERENCE_ID + '/Authors'
ACCEPTED_PAPER_ID = CONFERENCE_ID + '/-/Accepted_Papers'

# replace the builder-generated webfield with the custom webfield
with open('../webfield/conferenceWebfield.js') as f:
    homepage_webfield = f.read()

conference_group = client.get_group(CONFERENCE_ID)
conference_group.web = homepage_webfield
conference_group = client.post_group(conference_group)

try:
    claimants_group = client.get_group(CONFERENCE_ID + '/Claimants')
except openreview.OpenReviewException as e:
    # add the "Claimants" group
    print("adding the Claimants group")
    client.post_group(openreview.Group(
        id=CONFERENCE_ID + '/Claimants',
        readers=[CONFERENCE_ID, PROGRAM_CHAIRS_ID],
        nonreaders=[],
        writers=[CONFERENCE_ID],
        signatories=[CONFERENCE_ID],
        signatures=[CONFERENCE_ID],
        members=[])
    )

# post the invitation used to upload accepted RL Accepted papers
rc_accepted_paper_submission_invitation = client.post_invitation(openreview.Invitation(**{
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
                'required': False
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
    invitees=['everyone'],
    writers=[CONFERENCE_ID],
    signatures=[CONFERENCE_ID],
    multiReply=True,
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
                'description': 'Your institution or organization, comma separated if different institutions (max 100 chars)',
                'order': 2,
                'required': True,
                'value-regex': '.{1,100}'
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
            'values-copied': [CONFERENCE_ID, '{signatures}']
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
                'value': 'Claimed',
                'order': 0,
                'required': True
            },
            'plan': {'description': 'Your plan to reproduce results(max 5000 chars).',
                     'order': 1,
                     'required': False,
                     'value-regex': '.*'
                     },
            'institution': {
                'description': 'Your institution or organization(max 100 chars).',
                'order': 2,
                'required': False,
                'value-regex': '.*'
            },
            "team_members": {
                "description": "Comma separated list of team member names.",
                "value-regex": ".*",
                "order": 1,
                "required": False
            },
            "team_emails": {
                "description": "Comma separated list of team member email addresses, lowercased, in the same order as above. For authors with existing OpenReview accounts, please make sure that the provided email address(es) match those listed in the author's profile.",
                "value-regex": ".*",
                "order": 2,
                "required": False
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

report_submission_invitation = client.post_invitation(openreview.Invitation(
    id=SUBMISSION_ID,
    cdate=1601856000000,
    duedate=1607040000000,
    expdate=1607041800000,
    readers=['everyone'],
    invitees= [CONFERENCE_ID + '/Claimants'],
    writers=[CONFERENCE_ID],
    signatures=[CONFERENCE_ID],
    reply={
        'readers': {
            'values-copied': [
                'ML_Reproducibility_Challenge/2020',
                '{content.authorids}',
                '{signatures}'
            ]
        },
        'writers': {
            "values-copied": [
                "ML_Reproducibility_Challenge/2020",
                "{content.authorids}",
                "{signatures}"
            ]
        },
        'signatures': {
            "values-regex": "~.*"
        },
        "content": {
            "title": {
                "description": "Title of paper. Add TeX formulas using the following formats: $In-line Formula$ or $$Block Formula$$",
                "order": 1,
                "value-regex": ".{1,250}",
                "required": True
            },
            "authors": {
                "description": "Comma separated list of author names.",
                "order": 2,
                "values-regex": "[^;,\\n]+(,[^,\\n]+)*",
                "required": True,
                "hidden": True
            },
            "authorids": {
                "description": "Comma separated list of author email addresses, lowercased, in the same order as above. For authors with existing OpenReview accounts, please make sure that the provided email address(es) match those listed in the author's profile.",
                "order": 3,
                "values-regex": "~.*|([a-z0-9_\\-\\.]{1,}@[a-z0-9_\\-\\.]{2,}\\.[a-z]{2,},){0,}([a-z0-9_\\-\\.]{1,}@[a-z0-9_\\-\\.]{2,}\\.[a-z]{2,})",
                "required": True
            },
            "abstract": {
                "description": "Abstract of paper. Add TeX formulas using the following formats: $In-line Formula$ or $$Block Formula$$",
                "order": 8,
                "value-regex": "[\\S\\s]{1,5000}",
                "required": True
            },
            "pdf": {
                "description": "Upload a PDF file that ends with .pdf",
                "order": 9,
                "value-file": {
                    "fileTypes": [
                        "pdf"
                    ],
                    "size": 50
                },
                "required": True
            },
            "paper_url": {
                "description": "Please provide the OpenReview's forum url",
                "required": True,
                "value-regex": "http.*",
                "order": 11
            }
        }
    },
    process='../process/reportProcess.py'
))
