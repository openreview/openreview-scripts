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
import iclr19
import os

import re
import json

# Per-paper group template definitions
papergroup_template = {
    'id': iclr19.PAPER_TEMPLATE_STR,
    'readers':[iclr19.CONFERENCE_ID],
    'writers': [iclr19.CONFERENCE_ID],
    'signatures': [iclr19.CONFERENCE_ID],
    'signatories': [iclr19.CONFERENCE_ID],
    'members': [],
}

authors_template = {
    'id': iclr19.PAPER_AUTHORS_TEMPLATE_STR,
    'readers':[
        iclr19.CONFERENCE_ID,
        iclr19.PROGRAM_CHAIRS_ID
    ],
    'writers': [iclr19.CONFERENCE_ID],
    'signatures': [iclr19.CONFERENCE_ID],
    'signatories': [iclr19.CONFERENCE_ID],
    'members': [],
}

reviewers_template = {
    'id': iclr19.PAPER_REVIEWERS_TEMPLATE_STR,
    'readers':[
        iclr19.CONFERENCE_ID,
        iclr19.PROGRAM_CHAIRS_ID
    ],
    'writers': [iclr19.CONFERENCE_ID],
    'signatures': [iclr19.CONFERENCE_ID],
    'signatories': [iclr19.CONFERENCE_ID],
    'members': [],
}



area_chairs_template = {
    'id': iclr19.PAPER_AREA_CHAIRS_TEMPLATE_STR,
    'readers':[
        iclr19.CONFERENCE_ID,
        iclr19.PROGRAM_CHAIRS_ID
    ],
    'writers': [iclr19.CONFERENCE_ID],
    'signatures': [iclr19.CONFERENCE_ID],
    'signatories': [iclr19.CONFERENCE_ID],
    'members': [],
}

review_nonreaders_template = {
    'id': iclr19.PAPER_REVIEW_NONREADERS_TEMPLATE_STR,
    'readers':[
        iclr19.CONFERENCE_ID,
        iclr19.PROGRAM_CHAIRS_ID
    ],
    'writers': [iclr19.CONFERENCE_ID],
    'signatures': [iclr19.CONFERENCE_ID],
    'signatories': [iclr19.CONFERENCE_ID],
    'members': [],
}

comment_nonreaders_template = {
    'id': iclr19.PAPER_COMMENT_NONREADERS_TEMPLATE_STR,
    'readers':[
        iclr19.CONFERENCE_ID,
        iclr19.PROGRAM_CHAIRS_ID
    ],
    'writers': [iclr19.CONFERENCE_ID],
    'signatures': [iclr19.CONFERENCE_ID],
    'signatories': [iclr19.CONFERENCE_ID],
    'members': [],
}

reviewers_unsubmitted_template = {
    'id': iclr19.PAPER_REVIEWERS_UNSUBMITTED_TEMPLATE_STR,
    'readers':[
        iclr19.CONFERENCE_ID,
        iclr19.PROGRAM_CHAIRS_ID,
        iclr19.PAPER_AREA_CHAIRS_TEMPLATE_STR
    ],
    'writers': [iclr19.CONFERENCE_ID],
    'signatures': [iclr19.CONFERENCE_ID],
    'signatories': [iclr19.CONFERENCE_ID],
    'members': [],
}

reviewers_submitted_template = {
    'id': iclr19.PAPER_REVIEWERS_SUBMITTED_TEMPLATE_STR,
    'readers':[
        iclr19.CONFERENCE_ID,
        iclr19.PROGRAM_CHAIRS_ID,
        iclr19.PAPER_AREA_CHAIRS_TEMPLATE_STR
    ],
    'writers': [iclr19.CONFERENCE_ID],
    'signatures': [iclr19.CONFERENCE_ID],
    'signatories': [iclr19.CONFERENCE_ID],
    'members': [],
}

group_templates = {
    'Area_Chairs': iclr19.area_chairs.to_json(),
    'Paper': papergroup_template,
    'Paper/Authors': authors_template,
    'Paper/Reviewers': reviewers_template,
    'Paper/Area_Chairs': area_chairs_template,
    'Paper/Reviewers/Submitted': reviewers_submitted_template,
    'Paper/Reviewers/Unsubmitted': reviewers_unsubmitted_template,
}

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
    blind_submissions = list(openreview.tools.iterget_notes(client, invitation=iclr19.BLIND_SUBMISSION_ID))

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
            assert blind_submissions, 'no blind submissions found'
            for paper in blind_submissions:
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
                group.add_webfield(webfield_file)

            posted_group = client.post_group(group)
            print('posted new group {}'.format(posted_group.id))
