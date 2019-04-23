import argparse
import openreview
from openreview import invitations
import datetime
import os
import config

if __name__ == '__main__':
    ## Argument handling
    parser = argparse.ArgumentParser()
    parser.add_argument('--baseurl', help="base url")
    parser.add_argument('--username')
    parser.add_argument('--password')
    args = parser.parse_args()

    client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)
    conference = config.get_conference(client)

    comment_invis = list(openreview.tools.iterget_invitations(client, regex = 'auai.org/UAI/2019/Conference/-/Paper[0-9]+/Comment$'))
    print ('Updating {} comment invitations'.format(len(comment_invis)))

    for invi in comment_invis:
        number = invi.id.split('Paper')[1].split('/')[0]
        invi.reply['readers'] = {
            "description": "All user groups that will be able to read this comment.",
            "value-dropdown-hierarchy": [
                'auai.org/UAI/2019/Conference/Paper{}/Authors'.format(number),
                'auai.org/UAI/2019/Conference/Paper{}/Reviewers/Submitted'.format(number),
                'auai.org/UAI/2019/Conference/Paper{}/Area_Chairs'.format(number),
                'auai.org/UAI/2019/Conference/Program_Chairs'
                ]}
        invi.reply['writers'] = {'values': 'auai.org/UAI/2019/Conference'}
        client.post_invitation(invi)

    comments = list(openreview.tools.iterget_notes(
        client,
        invitation = 'auai.org/UAI/2019/Conference/-/Paper.*/Comment'
    ))
    print ('Updating {} comments'.format(len(comments)))
    for comment in comments:
        comment.writers = 'auai.org/UAI/2019/Conference'
        client.post_note(comment)