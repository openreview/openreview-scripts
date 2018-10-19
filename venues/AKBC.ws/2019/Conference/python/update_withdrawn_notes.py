#!/usr/bin/python

"""
A script for updating notes which were blind but now have been marked as withdrawn

Usage:

python update_withdrawn_notes.py
"""

import openreview
import argparse
import iclr19
import os
import time

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

    withdrawn_submissions = openreview.tools.iterget_notes(client, invitation=iclr19.BLIND_SUBMISSION_ID)

    for paper in blind_submissions:
        for template in args.invitations:
            assert template in invitation_templates, 'invitation template not defined'
            if args.disable:
                new_invitation = disable_invitation(template, target_paper=paper)
            else:
                new_invitation = enable_invitation(template, paper)
            posted_invitation = client.post_invitation(new_invitation)
            print('posted new invitation {} to paper {}'.format(posted_invitation.id, paper.id))
