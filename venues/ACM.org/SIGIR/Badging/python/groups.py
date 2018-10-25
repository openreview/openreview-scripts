#!/usr/bin/python

"""
A script for managing groups with parameters that depend on the papers to which
they are attached.

Usage:

python groups.py Reviewers
python groups.py Reviewers --overwrite
"""

import openreview
import argparse
import acm19 as conference_config
import os

import re
import json

# Per-paper group template definitions
papergroup_template = {
    'id': conference_config.PAPER_TEMPLATE_STR,
    'readers':[conference_config.CONFERENCE_ID],
    'writers': [conference_config.CONFERENCE_ID],
    'signatures': [conference_config.CONFERENCE_ID],
    'signatories': [conference_config.CONFERENCE_ID],
    'members': [],
}

authors_template = {
    'id': conference_config.PAPER_AUTHORS_TEMPLATE_STR,
    'readers':[
        conference_config.CHAIRS_ID,
        conference_config.PAPER_AUTHORS_TEMPLATE_STR
    ],
    'writers': [conference_config.CONFERENCE_ID],
    'signatures': [conference_config.CONFERENCE_ID],
    'signatories': [conference_config.PAPER_AUTHORS_TEMPLATE_STR],
    'members': [],
}

reviewers_template = {
    'id': conference_config.PAPER_REVIEWERS_TEMPLATE_STR,
    'readers':[
        conference_config.CONFERENCE_ID,
        conference_config.CHAIRS_ID
    ],
    'writers': [conference_config.CONFERENCE_ID],
    'signatures': [conference_config.CONFERENCE_ID],
    'signatories': [conference_config.CONFERENCE_ID],
    'members': [],
}

review_nonreaders_template = {
    'id': conference_config.PAPER_REVIEW_NONREADERS_TEMPLATE_STR,
    'readers':[
        conference_config.CONFERENCE_ID,
        conference_config.CHAIRS_ID
    ],
    'writers': [conference_config.CONFERENCE_ID],
    'signatures': [conference_config.CONFERENCE_ID],
    'signatories': [conference_config.CONFERENCE_ID],
    'members': [],
}

reviewers_unsubmitted_template = {
    'id': conference_config.PAPER_REVIEWERS_UNSUBMITTED_TEMPLATE_STR,
    'readers':[
        conference_config.CONFERENCE_ID,
        conference_config.CHAIRS_ID,
        conference_config.PAPER_CHAIRS_TEMPLATE_STR
    ],
    'writers': [conference_config.CONFERENCE_ID],
    'signatures': [conference_config.CONFERENCE_ID],
    'signatories': [conference_config.CONFERENCE_ID],
    'members': [],
}

reviewers_submitted_template = {
    'id': conference_config.PAPER_REVIEWERS_SUBMITTED_TEMPLATE_STR,
    'readers':[
        conference_config.CONFERENCE_ID,
        conference_config.CHAIRS_ID,
        conference_config.PAPER_CHAIRS_TEMPLATE_STR
    ],
    'writers': [conference_config.CONFERENCE_ID],
    'signatures': [conference_config.CONFERENCE_ID],
    'signatories': [conference_config.CONFERENCE_ID],
    'members': [],
}

group_templates = {
    'Conference': conference_config.conference.to_json(),
    'Chairs': conference_config.chairs.to_json(),
    'Paper': papergroup_template,
    'Paper/Authors': authors_template,
    'Paper/Reviewers': reviewers_template,
    'Paper/Chairs': chairs_template,
    'Paper/Reviewers/Submitted': reviewers_submitted_template,
    'Paper/Reviewers/Unsubmitted': reviewers_unsubmitted_template,
}

def create_and_post(client, paper, template_key, members=[]):
    group_to_post = openreview.Group.from_json(
        openreview.tools.fill_template(
            group_templates[template_key], paper))

    if members:
        group_to_post.members = members

    return client.post_group(group_to_post)

def update_homepage(client, webfield_file):
    conference_group = client.get_group(conference_config.CONFERENCE_ID)
    conference_group.add_webfield(webfield_file)
    posted_group = client.post_group(conference_group)
    return posted_group

def update_Chair_console(client, webfield_file):
    Chair_group = client.get_group(conference_config.CHAIRS_ID)
    Chair_group.add_webfield(webfield_file)
    posted_group = client.post_group(Chair_group)
    return posted_group

def update_Reviewer_console(client, webfield_file):
    Reviewer_group = client.get_group(conference_config.REVIEWERS_ID)
    Reviewer_group.add_webfield(webfield_file)
    posted_group = client.post_group(Reviewer_group)
    return posted_group

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('groups', nargs='*', help="any of the following: " + ", ".join(group_templates.keys()))
    parser.add_argument('--clear_members', action='store_true', help='if present, removes all members')
    parser.add_argument('--webfield', help='webfield file path')
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
    print('connecting to {}'.format(client.baseurl))
    submissions = list(openreview.tools.iterget_notes(client, invitation=conference_config.SUBMISSION_ID))

    for template_key in args.groups:
        assert template_key in group_templates, 'group template not defined'
        group_template = group_templates[template_key]

        groups_to_process = []
        # this conditional checks to see if the group is a single group
        # (i.e. it has no wildcards) (ignores the webfield)
        wildcard_matches = re.findall('<.*>', json.dumps(
            {k: v for k, v in group_template.items() if k != 'web'}))

        if not wildcard_matches:
            groups_to_process = [openreview.Group.from_json(group_template)]
        else:
            assert submissions, 'no submissions found'
            for paper in submissions:
                new_group = openreview.Group.from_json(
                    openreview.tools.fill_template(group_template, paper))
                groups_to_process.append(new_group)

        for group in groups_to_process:
            try:
                existing_group = client.get_group(group.id)
                group.members = existing_group.members
            except openreview.OpenReviewException as e:
                if 'Group Not Found' in e.args[0][0]:
                    print(e)
                else:
                    raise e

            if args.clear_members:
                group.members = []

            if args.webfield:
                group.add_webfield(args.webfield)

            posted_group = client.post_group(group)
            print('posted new group {}'.format(posted_group.id))
