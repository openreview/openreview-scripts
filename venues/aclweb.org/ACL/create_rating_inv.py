import argparse
import openreview
from tqdm import tqdm
import csv
from openreview import tools
import re
from collections import defaultdict

"""
OPTIONAL SCRIPT ARGUMENTS
    baseurl -  the URL of the OpenReview server to connect to (live site: https://openreview.net)
    username - the email address of the logging in user
    password - the user's password
"""
parser = argparse.ArgumentParser()
parser.add_argument('--baseurl', help="base URL")
parser.add_argument('--username')
parser.add_argument('--password')
args = parser.parse_args()
client = openreview.Client(baseurl=args.baseurl, username=args.username, password=args.password)

def create_review_rating_invitation(nonreaders, sac_group, review):
    paper_group = nonreaders[0].split('/Conflicts')[0]
    invitation = openreview.Invitation(id = f'{paper_group}/-/Review{review.number}/Rating',
                                duedate = None,
                                readers = [sac_group],
                                invitees = [sac_group],
                                writers = ['aclweb.org/ACL/2022/Conference'],
                                signatures = ['aclweb.org/ACL/2022/Conference'],
                                multiReply=False,
                                reply = {
                                    'forum': review.forum,
                                    'replyto': review.id,
                                    'readers': {
                                        'description': 'This rating is only visible to the program chairs and area chair',
                                        'values': ['aclweb.org/ACL/2022/Conference/Program_Chairs', sac_group]
                                    },
                                    'nonreaders': {
                                        'values': nonreaders
                                    },
                                    'signatures': {
                                        'description': 'How your identity will be displayed with the above content.',
                                        'values': [sac_group]
                                    },
                                    'writers': {
                                        'description': 'Users that may modify this record.',
                                        'values': [sac_group]
                                    },
                                    'content': {
                                        'outstanding_review': {
                                            'description': 'Please indicate if you consider this an outstanding review.',
                                            'order': 1,
                                            'required': True,
                                            'value-radio': ['Yes', 'No'],
                                            'default': 'No'
                                        }
                                    }
                                }
                                )
    client.post_invitation(invitation)

def create_metareview_rating_invitation(nonreaders, sac_group, metareview):
    paper_group = nonreaders[0].split('/Conflicts')[0]
    invitation = openreview.Invitation(id =f'{paper_group}/-/MetaReview{metareview.number}/Rating',
                                duedate = None,
                                readers = [sac_group],
                                invitees = [sac_group],
                                writers = ['aclweb.org/ACL/2022/Conference'],
                                signatures = ['aclweb.org/ACL/2022/Conference'],
                                multiReply=False,
                                reply = {
                                    'forum': metareview.forum,
                                    'replyto': metareview.id,
                                    'readers': {
                                        'description': 'This rating is only visible to the program chairs and area chair',
                                        'values': ['aclweb.org/ACL/2022/Conference/Program_Chairs', sac_group]
                                    },
                                    'nonreaders': {
                                        'values': nonreaders
                                    },
                                    'signatures': {
                                        'description': 'How your identity will be displayed with the above content.',
                                        'values': [sac_group]
                                    },
                                    'writers': {
                                        'description': 'Users that may modify this record.',
                                        'values': [sac_group]
                                    },
                                    'content': {
                                        'outstanding_meta_review': {
                                            'description': 'Please indicate if you consider this an outstanding meta review.',
                                            'order': 1,
                                            'required': True,
                                            'value-radio': ['Yes', 'No'],
                                            'default': 'No'
                                        }
                                    }
                                }
                                )
    client.post_invitation(invitation)

reviews = list(tools.iterget_notes(client, invitation='aclweb.org/ACL/2022/Conference/-/Official_Review', sort='number:asc'))
print(f'{len(reviews)} posted reviews')

for rev in tqdm(reviews):
    nonreaders = rev.nonreaders
    r = re.compile("aclweb.org/ACL/2022/Conference/.*/Senior_Area_Chairs")
    try:
        sac_group = list(filter(r.match, rev.readers))[0]
        create_review_rating_invitation(nonreaders, sac_group, rev)
    except IndexError:
        print('SACs are not readers of the review, paper ID: ', rev.forum)

metareviews = list(tools.iterget_notes(client, invitation='aclweb.org/ACL/2022/Conference/-/Meta_Review', sort='number:asc'))
print(f'{len(metareviews)} posted metareviews')

for meta in tqdm(metareviews):
    nonreaders = meta.nonreaders
    r = re.compile("aclweb.org/ACL/2022/Conference/.*/Senior_Area_Chairs")
    try:
        sac_group = list(filter(r.match, meta.readers))[0]
        create_metareview_rating_invitation(nonreaders, sac_group, meta)
    except IndexError:
        print('SACs are not readers of the metareview, paper ID: ', meta.forum)