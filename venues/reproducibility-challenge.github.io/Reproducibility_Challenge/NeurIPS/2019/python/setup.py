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

def set_landing_page(client, group):
    if not group.web:
        # create new webfield using template
        children_groups = client.get_groups(regex = group.id + '/[^/]+/?$')

        links = []
        for children in children_groups:
            if not group.web or (group.web and children.id not in group.web):
                links.append({ 'url': '/group?id=' + children.id, 'name': children.id})

        default_header = {
            'title': group.id,
            'description': ''
        }

        with open(os.path.join(os.path.dirname(__file__), '../webfield/landingWebfield.js')) as f:
            content = f.read()
            content = content.replace("var GROUP_ID = '';", "var GROUP_ID = '" + group.id + "';")
            content = content.replace("var HEADER = {};", "var HEADER = " + json.dumps(default_header) + ";")
            content = content.replace("var VENUE_LINKS = [];", "var VENUE_LINKS = " + json.dumps(links) + ";")
            group.web = content
            return client.post_group(group)

# create challenge groups
groups = openreview.tools.build_groups(conference_id)
for group in groups:
    set_landing_page(client, group)

home_group = groups[-1]
print(home_group.id)

# add group to Active Venues
active_venues_group = client.get_group(id='active_venues')
client.add_members_to_group(active_venues_group, [conference_id])

# create PCs and add to home group
client.post_group(openreview.Group(
    id=conference_id+'/Program_Chairs',
    readers=[conference_id, conference_id+'/Program_Chairs'],
    writers=[conference_id, conference_id+'/Program_Chairs'],
    signatures=[conference_id],
    signatories=[conference_id+'/Program_Chairs'],
    members=['pca@email.com']
))

home_group.members.append(conference_id+'/Program_Chairs')

with open(os.path.join(os.path.dirname(__file__), '../webfield/conferenceWebfield.js')) as f:
    home_group.web = f.read()

home_group = client.post_group(home_group)


# NIPS_Submission invitation
# TODO: use the regular openreview.Invitation class instead
submission_inv = invitations.Submission(
    conference_id = conference_id,
    duedate = tools.datetime_millis(datetime.datetime(2019, 9, 10, 12, 0)),
    reply_params={
        'readers': {'values': ['everyone']},
        'writers': {
                        'values-copied': [
                            conference_id,
                            '{signatures}'
                        ]
                    }
    }
)
del submission_inv.reply['content']['TL;DR']
del submission_inv.reply['content']['pdf']
del submission_inv.reply['content']['keywords']
del submission_inv.reply['content']['authorids']
submission_inv.reply['content']['codelink'] = {'description': 'url for source code',
                                               'value-regex': '.*',
                                               'required': False}
submission_inv.reply['content']['pdf_link'] = {'description': 'url for camera ready submission',
                                               'value-regex': '.*',
                                               'required': False}
submission_inv.id = conference_id+"/-/NeurIPS_Submission"
submission_inv.invitees = [conference_id+'/Program_Chairs']
submission_inv.reply['signatures'] = {'values':[conference_id+'/Program_Chairs']}
submission_inv = client.post_invitation(submission_inv)

client.post_group(openreview.Group(
    id=conference_id+'/Claimants',
    readers=[conference_id, conference_id+'/Program_Chairs'],
    nonreaders=[],
    writers=[conference_id],
    signatories=[conference_id],
    signatures=[conference_id],
    members=[],
    details={ 'writable': True })
)

claim_inv = client.post_invitation(openreview.Invitation(
    id='{}/-/Claim'.format(conference_id),
    readers=['everyone'],
    invitees=['~'],
    nonreaders=[conference_id+'/Claimants'],
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
            'compute_resources': {'description': 'Do you need compute resources?',
                 'order': 3,
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


#TODO PAM fix duedate
# add start date
report_invite = invitations.Submission(conference_id=conference_id,
                                       duedate = tools.datetime_millis(datetime.datetime(2019, 12, 2, 12, 0)))
report_invite.invitees = [conference_id+'/Claimants']
report_invite.readers = [conference_id+'/Claimants']
report_invite.reply['readers']['values'] = [conference_id+'/Program_Chairs']
report_invite.id = conference_id+'/-/Report_Submission'
client.post_invitation(report_invite)