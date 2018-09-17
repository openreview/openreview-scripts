#!/usr/bin/python

"""
A script for managing invitations with parameters that depend on the papers to which
they are attached.

You can create, enable, or disable most invitations in ICLR 2018 from this script.

Usage:

python toggle-invitations.py Public_Comment --enable
python toggle-invitations.py Public_Comment --disable
"""

import openreview
import argparse
import iclr19

# Per-paper group template definitions
papergroup_template = {
    'id': iclr19.PAPER_TEMPLATE_STR,
    'readers':[iclr19.CONFERENCE_ID],
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
    'Paper': papergroup_template,
    'Reviewers': reviewers_template,
    'Area_Chairs': area_chairs_template,
    'Reviewers/Submitted': reviewers_submitted_template,
    'Reviewers/Unsubmitted': reviewers_unsubmitted_template,
}

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('groups', nargs='*', help="any of the following: " + ", ".join(group_templates.keys()))
    parser.add_argument('--overwrite', action='store_true', help="if present, overwrites the members of the groups")
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    blind_submissions = openreview.tools.iterget_notes(client, invitation=iclr19.BLIND_SUBMISSION_ID)

    for paper in blind_submissions:
        for template in args.groups:
            assert template in group_templates, 'group template not defined'

            # note that the function below is being used for an nonstandard purpose. it should be refactored.
            new_group = openreview.Group.from_json(
                openreview.tools.fill_template(group_templates[template], paper))
            if not args.overwrite:
                try:
                    existing_group = client.get_group(new_group.id)
                    new_group.members = existing_group.members
                except openreview.OpenReviewException as e:
                    # TODO: replace this with the correct conditional
                    if 'Group Not Found' in e.args[0][0]:
                        pass
                    else:
                        raise e

            posted_group = client.post_group(new_group)
            print('posted new group {} for paper {}'.format(posted_group.id, paper.id))
