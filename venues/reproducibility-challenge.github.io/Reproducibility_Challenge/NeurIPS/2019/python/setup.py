# Setup creates the group for the conference and adds a link to it in the parent group webfield
# create PC group
# creates NIPS_Submission invitation


import openreview
from openreview import tools
from openreview import invitations
import os
import json
import datetime

# live
#client = openreview.Client(baseurl='https://openreview.net')
# dev site
#client = openreview.Client(baseurl='https://dev.openreview.net', username='OpenReview.net', password='OpenReview_dev')
client = openreview.Client()
print(client.baseurl)
conference_id='reproducibility-challenge.github.io/Reproducibility_Challenge/NeurIPS/2019'


def build_groups(conference_id):
    path_components = conference_id.split('/')
    paths = ['/'.join(path_components[0:index + 1]) for index, path in enumerate(path_components)]
    groups = []

    for p in paths:
        group = tools.get_group(client, id=p)
        if group is None:
            group = client.post_group(openreview.Group(
                id=p,
                readers=['everyone'],
                nonreaders=[],
                writers=[p],
                signatories=[p],
                signatures=['~Super_User1'],
                members=[],
                details={'writable': True})
            )

        groups.append(group)

    return groups

def set_landing_page(group):
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
groups = build_groups(conference_id)
for group in groups:
    set_landing_page(group)

home_group = groups[-1]
print(home_group.id)

# add group to Active Venues
active = client.get_group(id = 'active_venues')
client.add_members_to_group(active, [conference_id])

# create PCs and add to home group
client.post_group(openreview.Group(
                id = conference_id+'/Program_Chairs',
                readers = [conference_id, conference_id+'/Program_Chairs'],
                writers = [conference_id, conference_id+'/Program_Chairs'],
                signatures = [conference_id],
                signatories = [conference_id+'/Program_Chairs'],
                members = ['pca@email.com']))
home_group.members.append(conference_id+'/Program_Chairs')
home_group = client.post_group(home_group)



submission_start_date_str = "August 7, 2019"
submission_due_date_str = "November 1, 2019"
conference_start_date_str = "December 13/14, 2019"

with open(os.path.join(os.path.dirname(__file__), '../webfield/conferenceWebfield.js')) as f:
    file_content = f.read()

    content = file_content.replace("var CONFERENCE_ID = '';", "var CONFERENCE_ID = '" + conference_id + "';")
    content = content.replace("var HEADER = {};", "var HEADER = " + json.dumps({
        'title': 'Reproducibility Challenge 2019',
        'subtitle': 'A NeurIPS Workshop',
        'deadline': 'Submission Claims Start: ' + submission_start_date_str + ' GMT, End: ' + submission_due_date_str+' GMT',
        'date': conference_start_date_str,
        'website': 'https://reproducibility-challenge.github.io/neurips2019/dates/',
        'location': 'Vancouver, Canada'
        }) + ";")
    content = content.replace("var REVIEWERS_NAME = '';", "var REVIEWERS_NAME = '"+conference_id+"/Reviewers';")
    content = content.replace("var SUBMISSION_ID = '';", "var SUBMISSION_ID = '"+conference_id+"/-/NeurIPS_Submission';")
    content = content.replace("var BLIND_SUBMISSION_ID = '';", "var BLIND_SUBMISSION_ID = '"+conference_id+"/-/NeurIPS_Submission';")
    content = content.replace("var DECISION_INVITATION_REGEX = '';", "var DECISION_INVITATION_REGEX = '"+conference_id+"/-/Decision';")
    content = content.replace("var REVIEWERS_ID = '';", "var REVIEWERS_ID = '"+conference_id+"/Reviewers';")
    content = content.replace("var PROGRAM_CHAIRS_ID = '';", "var PROGRAM_CHAIRS_ID = '"+conference_id+"/Program_Chairs';")
    content = content.replace("var AUTHORS_ID = '';", "var AUTHORS_ID = '"+conference_id+"/Authors';")
    content = content.replace("var DECISION_HEADING_MAP = {};", "var DECISION_HEADING_MAP = {'Unclaimed':'Unclaimed', 'Claimed':'Claimed'};")
    home_group.web = content
    home_group = client.post_group(home_group)



# NIPS_Submission invitation

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
submission_inv.id = conference_id+"/-/NeurIPS_Submission"
submission_inv.invitees = [conference_id+'/Program_Chairs']
submission_inv.reply['signatures'] = {'values':[conference_id+'/Program_Chairs']}
submission_inv =client.post_invitation(submission_inv)


